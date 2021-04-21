#!/bin/bash

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MAIN_DIR="${SCRIPT_DIR}/../.."

# Fetch all the branches
git fetch origin 'refs/heads/*:refs/remotes/origin/*'

# Move to the main folder
cd ${MAIN_DIR}

# Fill the generate.yml
echo ${GENERATE_YML_BASE64} | base64 -d > generate.yml

# Generate
python generate.py --local-generation
