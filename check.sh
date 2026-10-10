#!/bin/bash
# Сборка и все проверки. Нужны: python3, пакет playwright (pip install playwright), Chromium.
#   ./check.sh          быстрые проверки (около 2 минут)
#   ./check.sh full     то же плюс обход всех островков через интерфейс (около 15 минут)
set -e
cd "$(dirname "$0")"
./fetch_pyodide.sh
./mk.sh
python3 tests/xc5.py
python3 tests/cpython_check.py
python3 tests/gen_fuzz.py
python3 tests/state_fuzz.py
if [ "$1" = "full" ]; then python3 tests/crawl.py; fi
echo "Все проверки пройдены"
