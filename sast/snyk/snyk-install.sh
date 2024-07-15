#!/usr/bin/env bash

# Set script to exit on error
set -e

VERSION_LIST_FILE=$1
SNYK_DIR=/snyk

# Create directory if it doesn't exist
if [[ ! -e $SNYK_DIR ]]; then
    mkdir -p $SNYK_DIR
fi

# Function to download, extract and setup codeql version
fetch_snyk() {
    echo "Downloading $name from $link"
    cd $SNYK_DIR
    wget -q "$link" -O snyk
    chmod +x snyk
}

# Process VERSION_LIST_FILE using Python3 to fetch name and link
python - <<END | while read name link ; do fetch_snyk ; done
import yaml

with open("$VERSION_LIST_FILE", 'r') as stream:
    versions = yaml.safe_load(stream)['versions']
for version in versions:
    if "name" in versions[version] and "link" in versions[version]:
        print(versions[version]['name'], versions[version]['link'])
END
