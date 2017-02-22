#!/bin/sh

#########################################################
# Build a stand-alone executable for Windows            #
# Wine is required : sudo apt install wine-development  #
#########################################################
# Requirements
PYTHON344_MSI_NAME="python-3.4.4.msi"
PYTHON344_MSI_URL="https://www.python.org/ftp/python/3.4.4/$PYTHON344_MSI_NAME"
LXML_WHL_NAME="lxml-3.7.3-cp34-cp34m-win32.whl"
LXML_REFERER='http://www.lfd.uci.edu/~gohlke/pythonlibs/'
LXML_URL='http://www.lfd.uci.edu/~gohlke/pythonlibs/tugh5y6j/$LXML_WHL_NAME'
REPORTLAB_PYPI='https://www.reportlab.com/pypi/simple/'
REPORTLAB_PKG="reportlab==3.3.34"
DOCOPT_PKG="docopt==0.6.2"
# Wine
TMP_FOLDER="/tmp/xml-archive-to-pdf_win32_build"
WINEARCH="win32"
WINEPREFIX="$TMP_FOLDER/wine"
WINE_CMD="wine-development"
# Python
PYTHON_FOLDER="c:\\Python3"
PYTHON_LIBS_FOLDER="c:\\Python3\\Lib\\site-packages"
PYTHON_SCRIPT_MAIN="xml_archive_to_pdf/main.py"
# Exe
EXE_NAME="xml-archive-to-pdf.exe"
EXE_DIST="dist"

mkdir $TMP_FOLDER
wget -c -O $TMP_FOLDER/$PYTHON344_MSI_NAME $PYTHON344_MSI_URL
wget -c -O $TMP_FOLDER/$LXML_WHL_NAME --user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" --referer=$LXML_REFERER $LXML_URL
WINEARCH=$WINEARCH WINEPREFIX=$WINEPREFIX $WINE_CMD msiexec /i $TMP_FOLDER/$PYTHON344_MSI_NAME /qn TARGETDIR=$PYTHON_FOLDER
WINEARCH=$WINEARCH WINEPREFIX=$WINEPREFIX $WINE_CMD py -3.4 -m pip install --upgrade pip
WINEARCH=$WINEARCH WINEPREFIX=$WINEPREFIX $WINE_CMD pip install $TMP_FOLDER/$LXML_WHL_NAME $DOCOPT_PKG pyinstaller
WINEARCH=$WINEARCH WINEPREFIX=$WINEPREFIX $WINE_CMD pip install -i $REPORTLAB_PYPI $REPORTLAB_PKG
WINEARCH=$WINEARCH WINEPREFIX=$WINEPREFIX $WINE_CMD pyinstaller --specpath=$TMP_FOLDER --name $EXE_NAME --workpath $TMP_FOLDER --onefile --paths $PYTHON_LIBS_FOLDER $PYTHON_SCRIPT_MAIN
WINEARCH=$WINEARCH WINEPREFIX=$WINEPREFIX $WINE_CMD $EXE_DIST/$EXE_NAME --help
