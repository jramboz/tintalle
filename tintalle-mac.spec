# -*- mode: python ; coding: utf-8 -*-

import os


codesign_identity = os.environ.get("MACOS_CODESIGN_IDENTITY")
entitlements_file = os.environ.get("MACOS_ENTITLEMENTS_FILE")


a = Analysis(
    ["app.py"],
    pathex=[],
    binaries=[],
    datas=[("img", "img"),
           ("OpenCore_OEM", "OpenCore_OEM"),
           ("translations", "translations"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Tintalle",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch="universal2",
    codesign_identity=codesign_identity,
    entitlements_file=entitlements_file,
    icon=["img/tintalle.png"],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Tintalle",
)

app = BUNDLE(
    coll,
    name="Tintalle.app",
    icon="img/tintalle.png",
    bundle_identifier="com.sublunarysphere.tintalle",
    info_plist={
        "NSPrincipalClass": "NSApplication",
        "NSAppleScriptEnabled": False,
        "CFBundleShortVersionString": "0.6.1",
        "CFBundleDevelopmentRegion": "en",
        "CFBundleLocalizations": [
            "en",
            "es",
            "ca",
        ],
    },
)
