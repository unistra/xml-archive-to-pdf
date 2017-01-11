"""
All utils
"""
import xml.etree.cElementTree as ET
import re
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


def get_bare_tag(elem):
    """ Get the tag name without namespace """
    return elem.tag.rsplit('}', 1)[-1]


def get_clean_text(elem):
    """ return value without line breaker chars """
    return re.sub(r"[\f\n\r\t\v]", "", elem.text).strip()


def get_doc(pdf_file):
    """ get the pdf doc """
    return SimpleDocTemplate(pdf_file, pagesize=letter, rightMargin=24,
                             leftMargin=24, topMargin=24, bottomMargin=24)


def get_title_style(level):
    """ get title style by level """
    if level == 0:
        return "Title"
    elif level in [1, 2, 3, 4, 5, 6]:
        return "{}{}".format("Heading", str(level))
    else:
        return "Normal"


def get_styles():
    """
    get styles for the pdf, default are :
    ‘Title’: <ParagraphStyle ‘Title’>
    ‘Heading1’: <ParagraphStyle ‘Heading1’>
    ‘Heading2’: <ParagraphStyle ‘Heading2’>
    ‘Heading3’: <ParagraphStyle ‘Heading3’>
    ‘Heading4’: <ParagraphStyle ‘Heading4’>
    ‘Heading5’: <ParagraphStyle ‘Heading5’>
    ‘Heading6’: <ParagraphStyle ‘Heading6’>
    ‘Bullet’: <ParagraphStyle ‘Bullet’>
    ‘Definition’: <ParagraphStyle ‘Definition’>
    ‘Normal’: <ParagraphStyle ‘Normal’>
    ‘Italic’: <ParagraphStyle ‘Italic’>
    ‘BodyText’: <ParagraphStyle ‘BodyText’>
    ‘Code’: <ParagraphStyle ‘Code’>
    """
    styles = getSampleStyleSheet()
    # styles.add(ParagraphStyle(name='justify', alignment=TA_JUSTIFY, leftIndent=130))
    # styles.add(ParagraphStyle(name='right', alignment=TA_RIGHT, rightIndent=50))
    # styles.add(ParagraphStyle(name='left', alignment=TA_LEFT, leftIndent=50))
    return styles


def build_pdf(xml_file, pdf_file):
    # pdf buffer
    doc = get_doc(pdf_file)
    styles = get_styles()
    Story = []

    # events and level for lxml
    level = 0
    # Parse the full xml
    for action, e in ET.iterparse(xml_file, events=("start", "end")):
        # If a new element is encountered
        if ET.iselement(e) and action == 'start':
            # get label and value
            label = e.attrib.get("name") if e.attrib.get("name") is not None else get_bare_tag(e)
            value = get_clean_text(e)
            has_children = True if e.getchildren() else False

            # Gestion des titres, un titre est un élément avec des enfants
            if has_children:
                print(label)
                Story.append(Paragraph(label, styles[get_title_style(level)]))
                Story.append(Spacer(1, 6))
            # C'est un element de type clé-valeur
            else:
                Story.append(Paragraph("{}: {}".format(label, value), styles["Normal"]))

        # Calcul the level
        if (action == 'start'):
            level += 1
        elif (action == 'end'):
            level -= 1

    doc.build(Story)
