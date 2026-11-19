# Exports querie's results to XML/JSON files 

from abc import ABC, abstractmethod 
import xml.etree.ElementTree as ET
import json 


class BaseExporter(ABC) :
    @abstractmethod
    def export (self, data : dict, file_path : str ) -> None :
        pass

class JSONExporter(BaseExporter) :
    def export(self, data : dict,  file_path : str ) -> None :
        with open(file_path, "w", encoding="utf-8") as file: # "w" mode creates file if it doesnt exists 
            json.dump(data, file, indent = 4, ensure_ascii=False) # just file.write(data) can write only strings

class XMLExporter(BaseExporter):
    """This part i wrore with AI, but learn also how to work with XML"""
    def export (self, data : dict , file_path :str ) -> None :
        root = ET.Element("report") # create root element 
        for section_name, rows in data.items():
            section = ET.SubElement(root, section_name) 
            for row in rows :
                room = ET.SubElement(section, "room")
                for key, value in row.items():
                    field = ET.SubElement(room, str(key))
                    field.text = str(value)
        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ") # 4 indents 
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
