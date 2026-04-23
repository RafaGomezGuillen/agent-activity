# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for macOS builds
"""

import sys
import os
import platform

# SPECPATH is the directory that contains this spec file: agent/pkgs/mac
SPEC_DIR = SPECPATH

# Go up 2 levels to reach project root: agent/
PROJECT_ROOT = os.path.dirname(os.path.dirname(SPEC_DIR))

# Add parent directory to path for imports
sys.path.insert(0, PROJECT_ROOT)

from pkgs.pyinstaller_config import COMMON_ARGS, PLATFORM_CONFIG, HIDDEN_IMPORTS, BINARIES, DATAS

block_cipher = None
platform_config = PLATFORM_CONFIG["mac"]

# Detect current architecture to avoid fat binary issues
current_arch = platform.machine()
if current_arch == "arm64":
    target_arch = "arm64"
elif current_arch == "x86_64":
    target_arch = "x86_64"
else:
    target_arch = None  # Let PyInstaller choose

a = Analysis(
    [os.path.join(SPEC_DIR, "main_mac.py")],
    pathex=[PROJECT_ROOT],
    binaries=BINARIES,
    datas=DATAS,
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    runtime_hooks=[os.path.join(SPEC_DIR, "runtime_mac_paths.py")],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

if COMMON_ARGS["onefile"]:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=COMMON_ARGS["name"],
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=COMMON_ARGS["console"],
        target_arch=target_arch,
        codesign_identity=None,
        entitlements_file=None,
    )

    bundle_target = exe
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=COMMON_ARGS["name"],
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=COMMON_ARGS["console"],
        target_arch=target_arch,
        codesign_identity=None,
        entitlements_file=None,
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name=COMMON_ARGS["name"],
    )
    bundle_target = coll

app = BUNDLE(
    bundle_target,
    name=f"{COMMON_ARGS['name']}.app",
    icon=platform_config.get("icon"),
    bundle_identifier=platform_config.get("osx_bundle_identifier"),
    info_plist={
        "CFBundleDisplayName": COMMON_ARGS["name"],
        "NSPrincipalClass": "NSApplication",
        "NSHighResolutionCapable": "True",
        "LSUIElement": "True",
    },
    dist_path=platform_config["distpath"],
    build_path=platform_config["workpath"],
)
