#!/usr/bin/env bash

# Set script to exit on error
set -e

VERSION_LIST_FILE=$1
BEARER_DIR=/bearer

# Create directory if it doesn't exist
if [[ ! -e $BEARER_DIR ]]; then
    mkdir -p $BEARER_DIR
fi

# Function to download, extract and setup codeql version
fetch_bearer() {
    echo "Downloading $name from $link"
    cd $BEARER_DIR
    wget -q "$link" -O bearer.tar.gz
    tar -xzf bearer.tar.gz -C "$BEARER_DIR"
    chmod +x bearer
}

# Process VERSION_LIST_FILE using Python3 to fetch name and link
python - <<END | while read name link ; do fetch_bearer ; done
import yaml

with open("$VERSION_LIST_FILE", 'r') as stream:
    versions = yaml.safe_load(stream)['versions']
for version in versions:
    if "name" in versions[version] and "link" in versions[version]:
        print(versions[version]['name'], versions[version]['link'])
END
