#!/usr/bin/env bash

# Set script to exit on error
set -e

VERSION_LIST_FILE=$1
SEMGREP_DIR=/semgrep

# Create directory if it doesn't exist
if [[ ! -e $SEMGREP_DIR ]]; then
    mkdir -p $SEMGREP_DIR
fi

# Function to download, extract and setup codeql version
fetch_semgrep() {
    echo "Installing $name from $link"
    cd $SEMGREP_DIR
    pip install semgrep
    ln -s /usr/local/bin/semgrep ./semgrep
}

# Process VERSION_LIST_FILE using Python3 to fetch name and link
python - <<END | while read name link ; do fetch_semgrep ; done
import yaml

with open("$VERSION_LIST_FILE", 'r') as stream:
    versions = yaml.safe_load(stream)['versions']
for version in versions:
    if "name" in versions[version] and "link" in versions[version]:
        print(versions[version]['name'], versions[version]['link'])
END
