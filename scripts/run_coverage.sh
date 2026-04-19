#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

TEST_FILE="${ROOT_DIR}/tests/coverage/test_coverage.py"
REPORT_DIR="${ROOT_DIR}/reports/coverage/report"

if command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "Eroare: Python nu este instalat sau nu se afla in PATH."
  exit 1
fi

echo "Folosind interpretatorul: ${PYTHON_BIN}"

# Instalare dependinte necesare
"${PYTHON_BIN}" -m pip install --upgrade pip
"${PYTHON_BIN}" -m pip install coverage pytest

if [[ ! -f "${TEST_FILE}" ]]; then
  echo "Eroare: fisierul de testare a acoperirii nu a fost gasit la ${TEST_FILE}"
  exit 1
fi

mkdir -p "${REPORT_DIR}"

cd "${ROOT_DIR}"

# Executa testele de acoperire si genereaza raportul HTML
"${PYTHON_BIN}" -m coverage erase
"${PYTHON_BIN}" -m coverage run -m pytest "${TEST_FILE}" -v
"${PYTHON_BIN}" -m coverage html -d "${REPORT_DIR}"

echo "Raportul HTML de acoperire a fost generat in: ${REPORT_DIR}"
echo "Deschide: ${REPORT_DIR}/index.html"
