# -*- mode: python ; coding: utf-8 -*-
"""
Auto-detecting spec launcher
This file automatically redirects to the appropriate platform-specific spec file

Build scripts:
  macOS:   bash build/build_mac.sh
  Windows: bash build/build_windows.bat
  Linux:   bash build/build_linux.sh
"""

import sys
import os

# This file tells you which spec file to use based on your platform
platform_name = sys.platform

if platform_name.startswith("linux"):
    raise RuntimeError(
        "ERROR: Use 'pyinstaller build/build_linux.spec' directly\n"
        "Or run: bash build/build_linux.sh"
    )
elif platform_name == "darwin":
    raise RuntimeError(
        "ERROR: Use 'pyinstaller build/build_mac.spec' directly\n"
        "Or run: bash build/build_mac.sh"
    )
elif platform_name == "win32":
    raise RuntimeError(
        "ERROR: Use 'pyinstaller build\\build_windows.spec' directly\n"
        "Or run: bash build\\build_windows.bat"
    )
else:
    raise RuntimeError(
        f"ERROR: Unknown platform '{platform_name}'\n"
        "Please use the platform-specific spec file directly:\n"
        "- macOS:   build/build_mac.spec\n"
        "- Windows: build/build_windows.spec\n"
        "- Linux:   build/build_linux.spec"
    )
