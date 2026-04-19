#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/mutation/proba.toml"
SESSION_FILE="$ROOT_DIR/config/mutation/tutorial.sqlite"
REPORT_DIR="$ROOT_DIR/reports/mutation"
TARGET_FILE="$ROOT_DIR/sistemrezervareavion.py"

TMP_BACKUP="$(mktemp)"
cp "$TARGET_FILE" "$TMP_BACKUP"

cleanup() {
    echo "Restaurare fisier original..."
    cp "$TMP_BACKUP" "$TARGET_FILE"
    rm -f "$TMP_BACKUP"
}
trap cleanup EXIT

cd "$ROOT_DIR"

mkdir -p "$REPORT_DIR"

echo "Stergere fisiere vechi de sesiune/raport..."
rm -f "$SESSION_FILE"
rm -f "$REPORT_DIR/report.html"

echo "Initializare sesiune Cosmic Ray..."
cosmic-ray init "$CONFIG_FILE" "$SESSION_FILE"

echo "Rularea testelor de mutatie..."
cosmic-ray exec "$CONFIG_FILE" "$SESSION_FILE"

echo "Afisare rezumat..."
cosmic-ray dump "$SESSION_FILE"

if command -v cr-html >/dev/null 2>&1; then
    echo "Generare raport HTML..."
    cr-html "$SESSION_FILE" > "$REPORT_DIR/report.html"
    echo "Raport HTML generat la: $REPORT_DIR/report.html"
else
    echo "cr-html nu a fost gasit. Instaleaza-l cu:"
    echo "pip install 'cosmic-ray[report]'"
fi

echo "Gata."