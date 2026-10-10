#!/bin/bash
# Скачивает ядро Pyodide 0.29.3 в pyo/pyodide/ (нужно для сборки, в git не хранится).
set -e
cd "$(dirname "$0")"
if [ -f pyo/pyodide/pyodide.asm.wasm ]; then echo "pyo/pyodide уже на месте"; exit 0; fi
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
curl -fL -o "$TMP/core.tar.bz2" https://github.com/pyodide/pyodide/releases/download/0.29.3/pyodide-core-0.29.3.tar.bz2
mkdir -p "$TMP/x" pyo
tar -xjf "$TMP/core.tar.bz2" -C "$TMP/x"
cp -r "$TMP/x/pyodide" pyo/
echo "готово: $(ls pyo/pyodide | wc -l) файлов в pyo/pyodide"
