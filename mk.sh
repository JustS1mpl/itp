#!/bin/bash
cd "$(dirname "$0")"
# если build.py упал, не собирать дальше из старого out.html
set -o pipefail
python3 build.py 2>&1 | tail -2 && cp out.html base43.html && python3 build5.py 2>&1 | tail -2
