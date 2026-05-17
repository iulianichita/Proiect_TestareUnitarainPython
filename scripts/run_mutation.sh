#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

CONFIG_FILE="$ROOT_DIR/config/mutation/proba.toml"
SESSION_FILE="$ROOT_DIR/config/mutation/tutorial.sqlite"

REPORT_DIR="$ROOT_DIR/reports/mutation/report"
REPORT_FILE="$REPORT_DIR/newReport.html"

TARGET_FILE="$ROOT_DIR/sistemrezervareavion.py"

mkdir -p "$REPORT_DIR"

TMP_BACKUP="$(mktemp)"
cp "$TARGET_FILE" "$TMP_BACKUP"

cleanup() {
    echo ""
    echo "Restaurare fisier original..."
    cp "$TMP_BACKUP" "$TARGET_FILE"
    rm -f "$TMP_BACKUP"

    if [[ -n "${PROGRESS_PID:-}" ]]; then
        kill "$PROGRESS_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

cd "$ROOT_DIR"

echo "Stergere sesiune anterioara..."
rm -f "$SESSION_FILE"
rm -f "$REPORT_FILE"

echo "Initializare sesiune Cosmic Ray..."
cosmic-ray init "$CONFIG_FILE" "$SESSION_FILE"

echo "Pornire monitor progres..."

progress_monitor() {
    while true; do
        clear
        echo "=============================="
        echo " PROGRES MUTATII COSMIC RAY"
        echo "=============================="
        echo ""

        cr-report "$SESSION_FILE" || grep pending

        echo ""
        echo "Actualizare la fiecare 15 secunde..."
        sleep 15
    done
}

progress_monitor &
PROGRESS_PID=$!

echo "Executie mutatii..."
cosmic-ray exec "$CONFIG_FILE" "$SESSION_FILE"

echo ""
echo "Mutatii finalizate."

kill "$PROGRESS_PID" 2>/dev/null || true

echo ""
echo "Rezumat final:"
cosmic-ray dump "$SESSION_FILE"

if command -v cr-html >/dev/null 2>&1; then
    echo ""
    echo "Generare raport HTML..."
    cr-html "$SESSION_FILE" > "$REPORT_FILE"

    echo "Raport generat:"
    echo "$REPORT_FILE"
else
    echo ""
    echo "cr-html lipseste."
    echo "Instalare:"
    echo "pip install 'cosmic-ray[report]'"
fi

echo ""
echo "Gata."