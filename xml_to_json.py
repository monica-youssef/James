import xml
from lxml import etree
from doc_to_xml import *
import re

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

    number_bool = False

    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Iterate through sections
    for section in root.iter('section'):
        # print("Section:")
        # if the first word of the string is "Overview", dump skip over it
        if section[0].text.split()[0] == "Overview":
            continue
        #  COLLECT CHAPTER AND VERSE
        # if the first word of the string is a number, it's a new chapter and verse

        elif section[0].text[0].isdigit():
            chapter, verse = section[0].text.split(":")
            number_bool = True
            # delete the next section after the chapter and verse
            continue

        # COLLECT AUTHOR
        elif section[0].text.__contains__(":"):
            title_and_author = section[0].text.split(":")[0]
            if title_and_author.__contains__("."):
                author = title_and_author.split(".")[1]

            # COLLECT TEXT AND SOURCE
            # if there is a number at the end drop it because it is a superscript
            commentary_and_source = section[0].text.split(":")[1:]
            commentary_and_source = ":".join(commentary_and_source)
            commentary_and_source = re.split(r'[!?\.]', commentary_and_source)
            if commentary_and_source[-1].isdigit():
                commentary_and_source = commentary_and_source[:-1]

            # with the superscript gone, now we need to split commentary and source
            last_sentence = commentary_and_source[-1]
            numbers = ""
            while last_sentence.isdigit() or last_sentence == "James":
                if len(last_sentence) > 1:
                    numbers += commentary_and_source.pop()[::-1] + "."
                else:
                    numbers += commentary_and_source.pop() + "."
                last_sentence = commentary_and_source[-1].strip() if len(commentary_and_source) > 0 else ""

            # append the numbers from the end
            source = last_sentence + numbers[::-1]
            print(source)
            if len(source) > 1 and not source[0].isalpha():
                pattern = re.compile(r'^["\d ]+')
                if pattern.match(source):
                    source = source[1:]
            print(source)

        # COLLECT AUTHOR

        # COLLECT AUTHOR
        # elif

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
    # print(sectioned_xml)
