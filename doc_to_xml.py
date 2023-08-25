import json
import re
from docx import Document

# load doc
original_document = Document("James.docx")


# function takes in a docx file, makes sections based off of where Overview is (to omit it)
# first item in each list is the chapter and verse with the theme title
def docx_to_list(doc):
    overview_reached = False
    sections = []
    current_section = []

    for paragraph in doc.paragraphs:
        if "Overview:" in paragraph.text:
            if current_section:
                sections.append(current_section)
                current_section = []
            overview_reached = True
            continue

        if overview_reached:
            current_section.append(paragraph.text)

    if current_section:
        sections.append(current_section)

    processed_sections = []
    for section in sections:
        for index, paragraph in enumerate(section):
            if re.match(r"^\d", paragraph):
                processed_sections.append(section[index:])
                break
    return processed_sections


unformatted_sections = docx_to_list(original_document)

text = ""
chapter = ""
verse = ""
author = ""
source = ""
result = []

# for loop to format list into json
for item in unformatted_sections:

    # Case 1: if the string starts with a digit it means it's a new chapter and verse
    for string in item:
        if string[0].isdigit():
            cur_chap, cur_verse = string.split(":")
            cur_verse = cur_verse.split()[0]

        # Case 2: if it doesn't start with a digit it means it's a commentary
        else:
            # first extract the author and scrap the title
            title_author = string.split(":")[0]
            author = re.split(r'[!?\.]', title_author)[-1].strip(" ")
            commentary = string.split(":")[-1]

            # get rid of the subscript at the end of each commentary
            while (commentary[-1] != ".") and len(commentary) > 1:
                commentary = commentary[:-1]

            # the process of getting the source text
            # in this chunk we split the commentary into sentences and get the last sentence
            sentences = re.split(r'[.!?]', commentary)
            last_sentence = sentences[-2].strip() if len(sentences) >= 2 else sentences[0].strip()

            # this while loop checks to see if the last sentence is a digit,
            # if it is, it means it's part of the source text,
            # and we have to add it into the source text
            numbers = ""
            while last_sentence.isdigit() or last_sentence == "James":
                if len(last_sentence) > 1:
                    numbers += sentences.pop()[::-1] + "."
                else:
                    numbers += sentences.pop() + "."
                last_sentence = sentences[-1].strip() if len(sentences) > 0 else ""

            # append the numbers from the end
            source = last_sentence + numbers[::-1]

            # clean up the text
            text = re.sub(r'\d+', '', commentary)

            # ignore ValueError: empty separator
            try:
                text = text.split(source)[0]
            except ValueError:
                pass
            text = text.strip()


            # now i had to make a choice... either change "St." to Saint everywhere in the original doc
            # or make a case to handle St. when it's in the source text
            if source.startswith("Concerning the Epistle of St. James"):
                source = re.sub(r'\.\d+', '', source)

            # TO-DO: fix the source if it caught the superscript from sentence before it


            # append the result
            if text != "":
                result.append({
                    'text': text,
                    'chapter': cur_chap,
                    'verse': cur_verse,
                    'author': author,
                    'source': source
                })

        # save as json
        with open('james.json', 'w') as json_file:
            json.dump(result, json_file, indent=2)
