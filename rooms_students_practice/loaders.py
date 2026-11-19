# Read JSON files (or other format, access to inheritant from BaseLoader class) 

from abc import ABC, abstractmethod
import json 
import logging 

logger = logging.getLogger(__name__)

class BaseLoader(ABC) :
    @abstractmethod
    def load_file(self):
        pass

class JSONLoader(BaseLoader) :
    def __init__(self, file_path ):
        self.file_path = file_path
    def load_file(self):
        with open(self.file_path, mode="r", encoding = "utf-8") as file :
            return json.load(file)



if __name__ ==  "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    rooms_path = 'rooms.json'
    students_path = 'students.json'

    roomsLoader = JSONLoader(rooms_path)
    studentsLoader = JSONLoader(students_path)

    try :
        loadedRooms = roomsLoader.load_file()
        logger.info(f"Loaded successfully, {len(loadedRooms)} objects")
    except FileNotFoundError as e: 
        logger.error(f"File isn't founded : {e}")
    except json.JSONDecodeError as e:
        logger.error(f"File is broken : {e}")

    try :
        loadedStudents = studentsLoader.load_file()
        logger.info(f"Loaded successfully, {len(loadedStudents)} objects")
    except FileNotFoundError as e: 
        logger.error(f"File isn't founded : {e}")
    except json.JSONDecodeError as e:
        logger.error(f"File is broken : {e}")
