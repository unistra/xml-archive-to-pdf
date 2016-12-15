"""
All utils
"""
from lxml import etree
# from io import StringIO, BytesIO
from .settings import ENCODING


def build_pdf(xml, encoding=ENCODING):
    root = etree.fromstring(xml.encode(encoding))

    res = etree.tostring(root, encoding=encoding, xml_declaration=True).decode(encoding)

    return res
