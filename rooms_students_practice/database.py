# Connect script to db

import pyodbc 
from abc import ABC , abstractmethod
import logging 

logger = logging.getLogger(__name__)

def show_drivers() :
    """Shows a list of drivers installed locally"""
    return pyodbc.drivers()

class BaseDatabase(ABC) :
    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def close(self) :
        pass

class MSSQLDatabase (BaseDatabase) :
    def __init__(self, server : str , database : str ) :
        self.server = server 
        self.database = database
        self.connection = None 
    def connect(self) :
        connection_string = fr'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;TrustServerCertificate=yes;'    
        self.connection = pyodbc.connect(connection_string)
        return self.connection
    def close(self) :
        if self.connection is not None :
            self.connection.close()
            self.connection = None 


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    my_server = r"localhost\SQLEXPRESS01"
    my_database = "students_db"
    myDatabase = MSSQLDatabase(server=my_server, database=my_database)

    try :
        myDatabase.connect()
        logger.info("Connection is successed")
    except pyodbc.Error as e:
        logger.error(f"Something goes wrong : {e}")
    finally :
        myDatabase.close()
        logger.info("Connection was closed")



