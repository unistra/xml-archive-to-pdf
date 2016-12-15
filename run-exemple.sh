#!/bin/zsh
set -e
myvalidxml=`xmllint --schema tests/data/pathfinder_v1.xsd tests/data/pathfinder_1.xml 2>/dev/null`
xml-archive-to-pdf $myvalidxml
