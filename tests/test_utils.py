import unittest
import os.path
from xml_archive_to_pdf.utils import get_bare_tag, get_clean_text, get_doc, \
registerFont, get_label, has_children, add_logo, ptTomm
import xml.etree.cElementTree as ET
from xml_archive_to_pdf.settings import *
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.flowables import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, Indenter

"""
Utils unit tests
"""


class UtilsTest(unittest.TestCase):

    def setUp(self):
        self.xml_file = "tests/data/pathfinder_1.xml"
        self.tree = ET.parse(self.xml_file)
        self.pdf_file = "tests/data/pathfinder_1.pdf"
        self.font_folder = "tests/data/CustomFont"
        self.logo_file = "tests/data/logo.png"

    def test_get_bare_tag(self):
        elem = self.tree.find(".//{fr:unistra:di:archive:pathfinder:v1}element")
        bare_tag = get_bare_tag(elem)
        self.assertEqual(bare_tag, "element")

    def test_get_clean_text(self):
        elem = self.tree.find(".//{fr:unistra:di:archive:pathfinder:v1}qualite")
        clean_text = get_clean_text(elem)
        self.assertEqual(clean_text, "très bonne")

    def test_get_doc(self):
        doc = get_doc(self.pdf_file)
        self.assertEqual(doc.pagesize, (612.0, 792.0))
        self.assertEqual(doc.bottomMargin, SPACE_UNIT*2)
        self.assertEqual(doc.topMargin, SPACE_UNIT*2)
        self.assertEqual(doc.leftMargin, SPACE_UNIT*2)
        self.assertEqual(doc.rightMargin, SPACE_UNIT*2)

    def test_registerFont(self):
        registerFont("CustomFont", self.font_folder)
        self.assertIsNotNone(pdfmetrics.getFont("CustomFont"))

    def test_get_label(self):
        elem = self.tree.find(".//{fr:unistra:di:archive:pathfinder:v1}element")
        self.assertEqual(get_label(elem), "élément")
        elem = self.tree.find(".//{fr:unistra:di:archive:pathfinder:v1}niveau")
        self.assertEqual(get_label(elem), "niveau")
        elem = self.tree.findall(".//{fr:unistra:di:archive:pathfinder:v1}classe")[1]
        self.assertEqual(get_label(elem), "")

    def test_has_children(self):
        elem = self.tree.find(".//{fr:unistra:di:archive:pathfinder:v1}element")
        self.assertFalse(has_children(elem))
        elem = self.tree.find(".//{fr:unistra:di:archive:pathfinder:v1}classes")
        self.assertTrue(has_children(elem))

    def test_add_logo(self):
        Story = []
        add_logo(Story, self.logo_file)
        self.assertTrue(isinstance(Story[0], Image))
        self.assertTrue(isinstance(Story[1], Spacer))

    def test_ptTomm(self):
        r = ptTomm(3)
        self.assertEqual(r, 1.0583339999999999)
