"""
Runtime path setup for macOS bundled app.
"""

import os
import sys
from pathlib import Path
from config.settings import APP_NAME, LOGS_DIR, DATA_DIR


if getattr(sys, "frozen", False):
    app_support_root = Path.home() / "Library" / "Application Support" / APP_NAME
    app_support_root.mkdir(parents=True, exist_ok=True)
    os.chdir(app_support_root)

    data_dir = app_support_root / DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)

    logs_dir = app_support_root / LOGS_DIR
    logs_dir.mkdir(parents=True, exist_ok=True)
