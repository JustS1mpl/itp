#!/bin/bash
cd "$(dirname "$0")"
# если build.py упал, не собирать дальше из старого out.html
set -o pipefail
# на Windows: PY=py bash mk.sh
PY=${PY:-python3}
# учебный план: порядок, стиль названий, таблицы в docs/CURRICULUM.md
"$PY" tests/curriculum_check.py || exit 1
"$PY" build.py 2>&1 | tail -2 || exit 1
# структура данных и «всё, что используется, введено раньше»: с нарушениями версия не собирается
"$PY" tests/coverage_check.py || exit 1
cp out.html base43.html && "$PY" build5.py 2>&1 | tail -2
