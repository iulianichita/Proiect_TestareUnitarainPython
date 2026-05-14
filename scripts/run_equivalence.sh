#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

TEST_DIR="${ROOT_DIR}/tests/equivalence"
TEST_FILE="${TEST_DIR}/test_equivalence.py"

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
"${PYTHON_BIN}" -m pip install pytest

if [[ ! -d "${TEST_DIR}" ]]; then
  echo "Eroare: directorul de teste ${TEST_DIR} nu a fost gasit"
  exit 1
fi

cd "${ROOT_DIR}"

# Permite transmiterea unor argumente suplimentare catre pytest
if [[ $# -gt 0 ]]; then
  EXTRA_ARGS="$@"
else
  EXTRA_ARGS="-q --tb=short"
fi

echo "Execut testele de echivalenta in ${TEST_DIR}"
"${PYTHON_BIN}" -m pytest "${TEST_FILE}" ${EXTRA_ARGS}

echo "Teste echivalenta rulate." 
