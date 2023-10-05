import json
import xml
from lxml import etree
from doc_to_xml import *
from xml_to_json import *
import re


    xml_path = "James_xml_only.xml"
    sectioned_xml = parse_xml(xml_path)
    result = parse_xml(xml_path)
    with open('james5.json', 'w') as json_file:
        json.dump(result, json_file, indent=2)