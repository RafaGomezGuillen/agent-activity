# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Linux builds
"""

import sys
import os

# SPECPATH is the directory that contains this spec file: agent/pkgs/linux
SPEC_DIR = SPECPATH

# Go up 2 levels to reach project root: agent/
PROJECT_ROOT = os.path.dirname(os.path.dirname(SPEC_DIR))

# Add project root to path for imports
sys.path.insert(0, PROJECT_ROOT)

from pkgs.pyinstaller_config import COMMON_ARGS, PLATFORM_CONFIG, HIDDEN_IMPORTS, BINARIES, DATAS

block_cipher = None
platform_config = PLATFORM_CONFIG["linux"]

a = Analysis(
    [os.path.join(SPEC_DIR, "main_linux.py")],
    pathex=[PROJECT_ROOT],
    binaries=BINARIES,
    datas=DATAS,
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    runtime_hooks=[os.path.join(SPEC_DIR, "runtime_linux_paths.py")],
    excludes=[
        "rumps",
        "win32api",
        "win32con",
        "win32event",
        "win32gui",
        "winerror",
        "pywintypes",
        "pystray._win32",
        "pystray._util.win32",
    ],
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
        strip=True,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=COMMON_ARGS["name"],
        debug=False,
        bootloader_ignore_signals=False,
        strip=True,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=True,
    )

    coll = COLLECT(
        exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=True,
        upx=True,
        upx_exclude=[],
        name=COMMON_ARGS["name"],
    )
