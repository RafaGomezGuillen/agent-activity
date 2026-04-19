# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Windows builds.
"""

import os
import sys

# SPECPATH is the directory that contains this spec file: agent/pkgs/windows
SPEC_DIR = SPECPATH
# Go up 2 levels to reach project root: agent/
PROJECT_ROOT = os.path.dirname(os.path.dirname(SPEC_DIR))

sys.path.insert(0, PROJECT_ROOT)

from pkgs.pyinstaller_config import COMMON_ARGS, PLATFORM_CONFIG, HIDDEN_IMPORTS, BINARIES, DATAS

platform_config = PLATFORM_CONFIG["windows"]

a = Analysis(
    [os.path.join(SPEC_DIR, "main_windows.py")],
    pathex=[PROJECT_ROOT],
    binaries=BINARIES,
    datas=DATAS,
    hiddenimports=HIDDEN_IMPORTS,
    hookspath=[],
    runtime_hooks=[os.path.join(SPEC_DIR, "runtime_windows_paths.py")],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure)

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
        icon=platform_config.get("icon"),
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
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console=COMMON_ARGS["console"],
        icon=platform_config.get("icon"),
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
