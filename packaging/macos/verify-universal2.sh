#!/usr/bin/env bash

set -euo pipefail

APP_PATH="${1:-dist/Tintalle.app}"

if [[ ! -d "${APP_PATH}" ]]; then
    echo "Error: application bundle not found: ${APP_PATH}" >&2
    exit 1
fi

mach_o_count=0
invalid_count=0

while IFS= read -r -d '' file_path; do
    if ! file "${file_path}" | grep -q "Mach-O"; then
        continue
    fi

    mach_o_count=$((mach_o_count + 1))
    architectures="$(lipo -archs "${file_path}" 2>/dev/null || true)"
    relative_path="${file_path#"${APP_PATH}"/}"

    printf '%-90s %s\n' \
        "${relative_path}" \
        "${architectures}"

    if [[ " ${architectures} " != *" x86_64 "* ]] ||
       [[ " ${architectures} " != *" arm64 "* ]]; then
        echo "::error file=${file_path}::Not a Universal2 binary: ${architectures}"
        invalid_count=$((invalid_count + 1))
    fi
done < <(
    find "${APP_PATH}" \
        -type f \
        -print0
)

if [[ "${mach_o_count}" -eq 0 ]]; then
    echo "Error: no Mach-O binaries were found in ${APP_PATH}." >&2
    exit 1
fi

if [[ "${invalid_count}" -ne 0 ]]; then
    echo
    echo "${invalid_count} Mach-O file(s) are missing an architecture." >&2
    exit 1
fi

echo
echo "All ${mach_o_count} Mach-O files contain x86_64 and arm64 slices."
