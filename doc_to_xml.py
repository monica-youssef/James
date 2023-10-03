from docx import Document
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def convert_docx_to_xml(docx_path, xml_path):
    # Load DOCX file
    doc = Document(docx_path)

    # Create XML root element
    xml_root = Element("document")

    current_section = None
    previous_bold_content = None

    # Iterate through paragraphs in the DOCX
    for paragraph in doc.paragraphs:
        # Iterate through runs in the paragraph
        for run in paragraph.runs:
            if run.bold:
                bold_content = run.text.strip()

                # Check if it's a new section or continues the previous one
                if current_section is None or bold_content != previous_bold_content:
                    current_section = SubElement(xml_root, "section")
                    current_run = SubElement(current_section, "run", {"bold": "true"})
                    current_run.text = bold_content

                previous_bold_content = bold_content
            elif current_section is not None:
                # If the run is not bold and there's an active section, add the text to the current section
                current_run.text += run.text

    # Create an XML tree
    xml_tree = ElementTree(xml_root)

    # Save the XML file
    xml_tree.write(xml_path, encoding="utf-8", xml_declaration=True)
