"""
xml-archive-to-pdf

Usage:
    xml-archive-to-pdf <xml>

Options:
    -h --help  aide
"""

from docopt import docopt
#from .settings import *
from .utils import build_pdf
import sys


def main():
    try:
        args = docopt(__doc__)
        xml = args["<xml>"]
        pdf = build_pdf(xml)
        sys.stdout.write(pdf)
    except Exception as e:
        sys.stderr.write(str(e))

if __name__ == "__main__":
    main()
