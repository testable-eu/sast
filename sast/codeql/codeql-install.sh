#!/usr/bin/env bash

# Set script to exit on error
set -e

VERSION_LIST_FILE=$1
CODEQL_DIR=/codeql

# Create directory if it doesn't exist
if [[ ! -e $CODEQL_DIR ]]; then
    mkdir -p $CODEQL_DIR
fi

# Function to download, extract and setup codeql version
fetch_codeql() {
    echo "Downloading $name from $link"
    wget -q "$link" -O codeql-bundle.tar.gz
    tar -xzf codeql-bundle.tar.gz -C "$CODEQL_DIR"
    mv "$CODEQL_DIR/codeql" "$CODEQL_DIR/$name"
    "$CODEQL_DIR/$name/codeql" resolve languages
    "$CODEQL_DIR/$name/codeql" resolve qlpacks
    rm codeql-bundle.tar.gz
}

# Process VERSION_LIST_FILE using Python3 to fetch name and link
python - <<END | while read name link ; do fetch_codeql ; done
import yaml

with open("codeql-versions-list.yaml", 'r') as stream:
    versions = yaml.safe_load(stream)['versions']
for version in versions:
    if "name" in versions[version] and "link" in versions[version]:
        print(versions[version]['name'], versions[version]['link'])
END
