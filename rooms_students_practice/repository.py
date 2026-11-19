# Execute SQL queries 

import pyodbc 
from abc import ABC, abstractmethod
import logging 


logger = logging.getLogger(__name__)

class BaseStorage(ABC) :
    @abstractmethod 
    def create_tables(self) -> None :
        pass 
    @abstractmethod 
    def insert_rooms(self, rooms : list[dict]) -> None :
        pass 
    @abstractmethod 
    def insert_students(self, students : list[dict]) -> None :
        pass 

class BaseAnalytics(ABC):
    @abstractmethod 
    def get_rooms_count_students (self) -> list[dict] :
        pass 
    @abstractmethod 
    def get_5rooms_smallest_avg_age(self) -> list[dict] :
        pass 
    @abstractmethod 
    def get_5rooms_largest_age_diff(self) -> list[dict] :
        pass 
    @abstractmethod 
    def get_rooms_mixed_sex(self) :
        pass 

class MSSQLRepository(BaseStorage, BaseAnalytics) :
    def __init__(self, connection : pyodbc.Connection ) :
        self.connection = connection 
    def create_tables(self) -> None:
        commands = [
            "DROP TABLE IF EXISTS students;",
            "DROP TABLE IF EXISTS rooms;",
            """
            CREATE TABLE rooms (
                id INT PRIMARY KEY,
                name NVARCHAR(100) NOT NULL
            );
            """,
            """
            CREATE TABLE students (
                id INT PRIMARY KEY,
                name NVARCHAR(100) NOT NULL,
                birthday DATETIME2 NOT NULL,
                room INT NOT NULL FOREIGN KEY REFERENCES rooms(id),
                sex CHAR(1) NOT NULL
            );
            """,
            "CREATE INDEX idx_students_room ON students(room);",
            "CREATE INDEX idx_students_birthday ON students(birthday);",
            "CREATE INDEX idx_students_sex ON students(sex);"
        ]

        with self.connection.cursor() as cursor:
            for command in commands:
                cursor.execute(command)
        self.connection.commit()
        logger.info("Tables and indexes created successfully")

    def insert_rooms(self, rooms: list[dict]) -> None:
        if not rooms:
            return

        query = "INSERT INTO rooms (id, name) VALUES (?, ?);"
        params = [(room["id"], room["name"]) for room in rooms]

        with self.connection.cursor() as cursor:
            cursor.executemany(query, params)
        self.connection.commit()
        logger.info(f"Inserted {len(rooms)} rooms into database")

    def insert_students(self, students: list[dict]) -> None:
        if not students:
            return

        query = "INSERT INTO students (id, name, birthday, room, sex) VALUES (?, ?, ?, ?, ?);"
        params = [
            (
                student["id"],
                student["name"],
                student["birthday"],
                student["room"],
                student["sex"]
            )
            for student in students
        ]

        with self.connection.cursor() as cursor:
            cursor.executemany(query, params)
        self.connection.commit()
        logger.info(f"Inserted {len(students)} students into database.")

    def _execute_select(self, query: str) -> list[dict]: # not to duplicate code
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_rooms_count_students(self) -> list[dict]:
        query = """
        SELECT 
            r.id, 
            r.name, 
            COUNT(s.id) AS student_count
        FROM rooms r
        LEFT JOIN students s ON r.id = s.room
        GROUP BY r.id, r.name
        ORDER BY r.id;
        """
        return self._execute_select(query)

    def get_5rooms_smallest_avg_age(self) -> list[dict]:
        query = """
        SELECT TOP 5 
            r.id, 
            r.name, 
            ROUND(CAST(AVG(DATEDIFF(DAY, s.birthday, GETDATE()) / 365.25) AS FLOAT), 2) AS avg_age
        FROM rooms r
        INNER JOIN students s ON r.id = s.room
        GROUP BY r.id, r.name
        ORDER BY avg_age ASC;
        """
        return self._execute_select(query)

    def get_5rooms_largest_age_diff(self) -> list[dict]:
        query = """
        SELECT TOP 5 
            r.id, 
            r.name, 
            ROUND(
                CAST(
                    MAX(DATEDIFF(DAY, s.birthday, GETDATE()) / 365.25) - 
                    MIN(DATEDIFF(DAY, s.birthday, GETDATE()) / 365.25) 
                AS FLOAT), 
            2) AS age_diff
        FROM rooms r
        INNER JOIN students s ON r.id = s.room
        GROUP BY r.id, r.name
        ORDER BY age_diff DESC;
        """
        return self._execute_select(query)

    def get_rooms_mixed_sex(self) -> list[dict]:
        query = """
        SELECT 
            r.id, 
            r.name
        FROM rooms r
        INNER JOIN students s ON r.id = s.room
        GROUP BY r.id, r.name
        HAVING COUNT(DISTINCT s.sex) > 1
        ORDER BY r.id;
        """
        return self._execute_select(query)







