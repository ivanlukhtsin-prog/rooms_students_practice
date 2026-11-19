# As i understood SOLID rules, no SQL, no dependecies, only modules isolated orcestation here 

import argparse
import json
import logging
from pathlib import Path
import pyodbc

from database import MSSQLDatabase
from exporters import JSONExporter, XMLExporter
from loaders import JSONLoader
from repository import MSSQLRepository

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process rooms and students data.")
    parser.add_argument("--rooms", required=True, help="Path to rooms JSON file")
    parser.add_argument("--students", required=True, help="Path to students JSON file")
    parser.add_argument("--format", choices=["xml", "json"], required=True, help="Output format")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    exporters = {
        "json": JSONExporter(),
        "xml": XMLExporter()
    }
    exporter = exporters[args.format]

    rooms_loader = JSONLoader(args.rooms)
    students_loader = JSONLoader(args.students)

    try:
        loaded_rooms = rooms_loader.load_file()
        logging.info(f"Rooms loaded successfully: {len(loaded_rooms)} records.")

        loaded_students = students_loader.load_file()
        logging.info(f"Students loaded successfully: {len(loaded_students)} records.")
    except FileNotFoundError as e:
        logging.error(f"Input file not found: {e}")
        return
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format: {e}")
        return

    local_server = r"localhost\SQLEXPRESS01"
    local_database = "students_db"
    db = MSSQLDatabase(server=local_server, database=local_database)

    try:
        connection = db.connect()
        logging.info("Database connection established.")
    except pyodbc.Error as e:
        logging.error(f"Database connection failed: {e}")
        return

    try:
        repository = MSSQLRepository(connection)

        repository.create_tables()
        repository.insert_rooms(loaded_rooms)
        repository.insert_students(loaded_students)

        dataset = {
            "rooms_with_student_count": repository.get_rooms_count_students(),
            "top_smallest_avg_age_rooms": repository.get_5rooms_smallest_avg_age(),
            "top_largest_age_diff_rooms": repository.get_5rooms_largest_age_diff(),
            "mixed_sex_rooms": repository.get_rooms_mixed_sex()
        }

        output_path = Path("output") / f"report.{args.format}"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        exporter.export(dataset, str(output_path))
        logging.info(f"Report successfully exported to {output_path}")

    except pyodbc.Error as e:
        logging.error(f"Database operation error: {e}")
    finally:
        connection.close()
        logging.info("Database connection closed.")


if __name__ == "__main__":
    main()