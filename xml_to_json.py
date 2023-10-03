import xml
from lxml import etree
from doc_to_xml import *

convert_docx_to_xml("James.docx", "James_xml_only.xml")

import xml.etree.ElementTree as ET


def parse_xml(xml_path):
    # for the json file later
    text = ""
    chapter = ""
    verse = ""
    author = ""
    source = ""
    result = []

    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Iterate through sections
    for section in root.iter('section'):
        print("Section:")
        # if the first word of the string is "Overview", dump skip over it
        if section[0].text.split()[0] == "Overview":
            continue
        #  COLLECT CHAPTER AND VERSE
        # if the first word of the string is a number, it's a new chapter and verse
        elif section[0].text[0].isdigit():
            chapter, verse = section[0].text.split(":")
            print(chapter, verse)

        # COLLECT AUTHOR
        elif




            # if text != "":
            #     result.append({
            #         'text': text,
            #         'chapter': chapter,
            #         'verse': verse,
            #         'author': author,
            #         'source': source
            #     })



        # Iterate through runs within each section
        # for run in section.iter('run'):
        #     print(f"{run.text}")


if __name__ == "__main__":
    xml_path = "James_xml_only.xml"
    sectioned_xml = parse_xml(xml_path)
    print(sectioned_xml)
