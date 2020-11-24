#!/bin/bash

set -e
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
MAIN_DIR="${SCRIPT_DIR}/../.."


BRANCH=$( git branch | grep '*' | cut -f 2 -d ' ' )
UNIT_TESTS_DIR="${SCRIPT_DIR}/../tests/unit/${BRANCH}"

pip install pytest==6.1.2
pytest ${UNIT_TESTS_DIR}
