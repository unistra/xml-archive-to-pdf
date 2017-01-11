"""
All utils
"""
import xml.etree.cElementTree as ET
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


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


def get_title_style(styles, level):
    """ get title style by level """
    if level == 0:
        return styles["cTitle"]
    elif level in [1, 2, 3, 4, 5, 6]:
        return styles["{}{}".format("cHeading", str(level))]
    else:
        return styles["Italic"]


def get_normal_style(styles, level):
    """ get title style by level """
    if level == 0:
        return styles["cNormal"]
    elif level in [1, 2, 3, 4, 5, 6]:
        return styles["{}{}".format("cNormal", str(level))]
    else:
        return styles["cNormal6"]


def get_styles():
    """
    get styles for the pdf, default are :
    Title: <ParagraphStyle ‘Title’>
    Heading1: <ParagraphStyle ‘Heading1’>
    Heading2: <ParagraphStyle ‘Heading2’>
    Heading3: <ParagraphStyle ‘Heading3’>
    Heading4: <ParagraphStyle ‘Heading4’>
    Heading5: <ParagraphStyle ‘Heading5’>
    Heading6: <ParagraphStyle ‘Heading6’>
    Bullet: <ParagraphStyle ‘Bullet’>
    Definition: <ParagraphStyle ‘Definition’>
    Normal: <ParagraphStyle ‘Normal’>
    Italic: <ParagraphStyle ‘Italic’>
    BodyText: <ParagraphStyle ‘BodyText’>
    Code: <ParagraphStyle ‘Code’>
    """
    styles = getSampleStyleSheet()
    # Titles
    styles.add(ParagraphStyle(name='cTitle', parent=styles['Title'], spaceAfter=24))
    styles.add(ParagraphStyle(name='cHeading1', parent=styles['Heading1'], spaceBefore=10,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#668cff"), backColor=colors.HexColor("#668cff")))
    styles.add(ParagraphStyle(name='cHeading2', parent=styles['Heading2'], spaceBefore=10, leftIndent=12,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#809fff"), backColor=colors.HexColor("#809fff")))
    styles.add(ParagraphStyle(name='cHeading3', parent=styles['Heading3'], spaceBefore=10, leftIndent=24,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#99b3ff"), backColor=colors.HexColor("#99b3ff")))
    styles.add(ParagraphStyle(name='cHeading4', parent=styles['Heading4'], spaceBefore=10, leftIndent=36,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#b3c6ff"), backColor=colors.HexColor("#b3c6ff")))
    styles.add(ParagraphStyle(name='cHeading5', parent=styles['Heading5'], spaceBefore=10, leftIndent=48,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#ccd9ff"), backColor=colors.HexColor("#ccd9ff")))
    styles.add(ParagraphStyle(name='cHeading6', parent=styles['Heading6'], spaceBefore=10, leftIndent=60,
        borderRadius=5, borderWidth=1, borderPadding=4, borderColor=colors.HexColor("#e6ecff"), backColor=colors.HexColor("#e6ecff")))
    # Normals
    styles.add(ParagraphStyle(name='cNormal', parent=styles['Normal']))
    styles.add(ParagraphStyle(name='cNormal1', leftIndent=12, parent=styles['Normal']))
    styles.add(ParagraphStyle(name='cNormal2', leftIndent=24, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal3', leftIndent=36, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal4', leftIndent=48, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal5', leftIndent=60, parent=styles['Normal'])),
    styles.add(ParagraphStyle(name='cNormal6', leftIndent=72, parent=styles['Normal'])),

    return styles


def write_elem(Story, e, level, styles):
    """ write element in the pdf """
    # get label and value
    label = e.attrib.get("name") if e.attrib.get("name") is not None else get_bare_tag(e)
    value = get_clean_text(e)
    has_children = True if e.getchildren() else False
    # Gestion des titres: un titre est un élément avec des enfants
    if has_children:
        # Si on a un label non vide, on l'affiche
        if label:
            Story.append(Paragraph(label, get_title_style(styles, level)))
        # Si on a forcé le nom du label à vide, on met juste un petit espace
        else:
            Story.append(Spacer(1, 6))
    # C'est un element de type clé-valeur, on l'affiche normalement
    else:
        if label or value:
            Story.append(Paragraph("{}: {}".format(label, value), get_normal_style(styles, level)))
    return Story


def build_pdf(xml_file, pdf_file):
    # Build the doc and the story
    doc = get_doc(pdf_file)
    styles = get_styles()
    Story = []
    # events and level for lxml
    level = 0
    # Parse the full xml
    for action, e in ET.iterparse(xml_file, events=("start", "end")):
        # If a new element is encountered
        if ET.iselement(e) and action == 'start':
            Story = write_elem(Story, e, level, styles)
        # Calcul the level
        if (action == 'start'):
            level += 1
        elif (action == 'end'):
            level -= 1
    doc.build(Story)
