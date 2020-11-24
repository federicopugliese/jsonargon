#!/bin/bash

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MAIN_DIR="${SCRIPT_DIR}/../../"

SONS_FILE="${MAIN_DIR}/devops/branches/sons.txt"

# -----

# Get current branch
current=$( git branch | grep '*' | cut -f 2 -d ' ' )

# Get its sons
sons=$( cat ${SONS_FILE} | grep "${current}:" | cut -f 2 -d ':' )

# For each son check for merge conflicts
for son in ${sons}; do

    echo "Merging into ${son}"
    git fetch origin "+refs/heads/${son}:refs/remotes/origin/${son}"
    git checkout ${son}
    git merge --no-edit --no-ff ${son}

done

# If this is reached, there were no conflicts: push all the merges.
git push --all
