"""
xml-archive-to-pdf

Usage:
    xml-archive-to-pdf (-i <xml_file>) (-o <pdf_file>)
    xml-archive-to-pdf (-i <xml_file>) (-o <pdf_file>) -l <logo_file>

Options:
    -h --help  aide
    -i <xml_file>, --input <xml_file>
    -o <pdf_file>, --output <pdf_file>
    -l <logo_file>, --logo <logo_file>
"""

from docopt import docopt
from .utils import build_pdf
import sys


def main():
    try:
        args = docopt(__doc__)
        xml_file = args["--input"]
        pdf_file = args["--output"]
        logo_file = args.get("--logo")
        build_pdf(xml_file, pdf_file, logo_file)
    except Exception as e:
        sys.stderr.write(str(e))

if __name__ == "__main__":
    main()
