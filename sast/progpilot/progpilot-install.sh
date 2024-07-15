#!/usr/bin/env bash

# Set script to exit on error
set -e

VERSION_LIST_FILE=$1
PROGPILOT_DIR=/progpilot

# Create directory if it doesn't exist
if [[ ! -e $PROGPILOT_DIR ]]; then
    mkdir -p $PROGPILOT_DIR
fi

# Function to download, extract and setup codeql version
fetch_progpilot() {
    echo "Downloading $name from $link"
    cd $PROGPILOT_DIR
    wget -q "$link" -O progpilot
    chmod +x progpilot
}

# Process VERSION_LIST_FILE using Python3 to fetch name and link
python - <<END | while read name link ; do fetch_progpilot ; done
import yaml

with open("$VERSION_LIST_FILE", 'r') as stream:
    versions = yaml.safe_load(stream)['versions']
for version in versions:
    if "name" in versions[version] and "link" in versions[version]:
        print(versions[version]['name'], versions[version]['link'])
END
