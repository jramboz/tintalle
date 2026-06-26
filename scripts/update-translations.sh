#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

if [[ "$#" -eq 0 ]]; then
    echo "Usage: $0 <translation.ts> [translation.ts ...]" >&2
    exit 1
fi

pyside6-lupdate \
    app.py \
    firmware.py \
    dialogs.py \
    $(find . -name '*.ui' -print) \
    -ts "$@"
