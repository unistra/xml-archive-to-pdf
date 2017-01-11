#!/bin/zsh
xmllint --schema tests/data/pathfinder_v1.xsd tests/data/pathfinder_1.xml && xml-archive-to-pdf -i tests/data/pathfinder_1.xml -o /tmp/pathfinder_1.pdf
