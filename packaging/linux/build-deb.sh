#!/usr/bin/env bash

set -euo pipefail

VERSION="${1:-0.1.0}"
ARCH="$(dpkg --print-architecture)"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PACKAGE_NAME="tintalle"
PACKAGE_ROOT="${PROJECT_ROOT}/build/deb/${PACKAGE_NAME}_${VERSION}_${ARCH}"
OUTPUT_DIR="${PROJECT_ROOT}/dist-packages"

PYINSTALLER_DIR="${PROJECT_ROOT}/dist/Tintalle"

MAINTAINER_NAME="${DEBFULLNAME:-Helios}"
MAINTAINER_EMAIL="${DEBEMAIL:-}"

if [[ -z "${MAINTAINER_EMAIL}" ]]; then
    echo "Error: define DEBEMAIL antes de construir el paquete."
    echo 'Ejemplo: export DEBEMAIL="correo@example.com"'
    exit 1
fi

MAINTAINER="${MAINTAINER_NAME} <${MAINTAINER_EMAIL}>"

if [[ ! -x "${PYINSTALLER_DIR}/Tintalle" ]]; then
    echo "Error: no se encuentra el ejecutable de PyInstaller:"
    echo "  ${PYINSTALLER_DIR}/Tintalle"
    echo
    echo "Genera primero la distribución con:"
    echo "  pyinstaller --clean --noconfirm tintalle-linux.spec"
    exit 1
fi

rm -rf "${PACKAGE_ROOT}"

mkdir -p \
    "${PACKAGE_ROOT}/DEBIAN" \
    "${PACKAGE_ROOT}/usr/lib/tintalle" \
    "${PACKAGE_ROOT}/usr/bin" \
    "${PACKAGE_ROOT}/usr/share/applications" \
    "${PACKAGE_ROOT}/usr/share/icons/hicolor/512x512/apps" \
    "${PACKAGE_ROOT}/usr/share/doc/tintalle" \
    "${PACKAGE_ROOT}/usr/share/man/man1" \
    "${OUTPUT_DIR}"

# Copia la distribución completa generada por PyInstaller.
cp -a \
    "${PYINSTALLER_DIR}/." \
    "${PACKAGE_ROOT}/usr/lib/tintalle/"

# Elimina metadatos generados por Windows.
find "${PACKAGE_ROOT}/usr/lib/tintalle" \
    -type f \
    -iname "Thumbs.db" \
    -delete

# Elimina rutas de construcción privadas introducidas por Pyenv.
if ! command -v patchelf >/dev/null 2>&1; then
    echo "Error: patchelf no está instalado."
    echo "Instálalo con: sudo apt install patchelf"
    exit 1
fi

while IFS= read -r -d '' elf_file; do
    if file "${elf_file}" | grep -q "ELF"; then
        current_rpath="$(patchelf --print-rpath "${elf_file}" 2>/dev/null || true)"

        if [[ "${current_rpath}" == *"/.pyenv/"* ]]; then
            echo "Eliminando RUNPATH privado de: ${elf_file#${PACKAGE_ROOT}/}"
            patchelf --remove-rpath "${elf_file}"
        fi
    fi
done < <(
    find "${PACKAGE_ROOT}/usr/lib/tintalle" \
        -type f \
        -print0
)

# Lanzador disponible como comando `tintalle`.
install -m 0755 \
    "${PROJECT_ROOT}/packaging/linux/tintalle" \
    "${PACKAGE_ROOT}/usr/bin/tintalle"

# Entrada del menú de aplicaciones.
install -m 0644 \
    "${PROJECT_ROOT}/packaging/linux/io.github.jramboz.tintalle.desktop" \
    "${PACKAGE_ROOT}/usr/share/applications/io.github.jramboz.tintalle.desktop"

# Icono.
install -m 0644 \
    "${PROJECT_ROOT}/img/tintalle.png" \
    "${PACKAGE_ROOT}/usr/share/icons/hicolor/512x512/apps/tintalle.png"

# Documentación.
install -m 0644 \
    "${PROJECT_ROOT}/README.md" \
    "${PACKAGE_ROOT}/usr/share/doc/tintalle/README"

INSTALLED_SIZE="$(du -sk "${PACKAGE_ROOT}/usr" | cut -f1)"

gzip -9n -c \
    "${PROJECT_ROOT}/packaging/linux/tintalle.1" \
    > "${PACKAGE_ROOT}/usr/share/man/man1/tintalle.1.gz"

chmod 0644 \
    "${PACKAGE_ROOT}/usr/share/man/man1/tintalle.1.gz"

# Changelog propio del paquete Debian.
cat > "${PACKAGE_ROOT}/usr/share/doc/tintalle/changelog.Debian" <<EOF
tintalle (${VERSION}) unstable; urgency=medium

  * Initial Debian package for Linux.

 -- ${MAINTAINER}  $(LC_ALL=C date -R)
EOF

gzip -9n \
    "${PACKAGE_ROOT}/usr/share/doc/tintalle/changelog.Debian"

cat > "${PACKAGE_ROOT}/DEBIAN/control" <<EOF
Package: ${PACKAGE_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Maintainer: ${MAINTAINER}
Depends: libc6, libxcb-cursor0, libxcb-icccm4, libxcb-image0, libxcb-keysyms1, libxcb-render-util0
Installed-Size: ${INSTALLED_SIZE}
Description: graphical manager for OpenCore-based lightsabers
 Tintalle is a graphical application for managing compatible
 OpenCore-based lightsabers, including colors, sounds and files.
EOF

# Normaliza permisos del paquete.
find "${PACKAGE_ROOT}/usr" \
    -type d \
    -exec chmod 0755 {} +

find "${PACKAGE_ROOT}/usr" \
    -type f \
    -exec chmod 0644 {} +

# Restaura el permiso de ejecución únicamente a programas y scripts.
while IFS= read -r -d '' package_file; do
    file_type="$(file "${package_file}")"
    file_header="$(head -c 2 "${package_file}" 2>/dev/null || true)"

    if [[ "${file_type}" == *"ELF"*"executable"* ]] ||
       [[ "${file_header}" == "#!" ]]; then
        chmod 0755 "${package_file}"
    fi
done < <(
    find "${PACKAGE_ROOT}/usr" \
        -type f \
        -print0
)

# Asegura explícitamente los dos lanzadores principales.
chmod 0755 \
    "${PACKAGE_ROOT}/usr/bin/tintalle" \
    "${PACKAGE_ROOT}/usr/lib/tintalle/Tintalle"

# Los ficheros del paquete deben pertenecer a root.
dpkg-deb \
    --root-owner-group \
    --build "${PACKAGE_ROOT}" \
    "${OUTPUT_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo
echo "Paquete generado:"
echo "  ${OUTPUT_DIR}/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
