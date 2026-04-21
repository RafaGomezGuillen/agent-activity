"""
Runtime path setup for Linux bundled app.
"""

import os
import sys
from pathlib import Path

from config.settings import APP_NAME, LOGS_DIR, DATA_DIR


if getattr(sys, "frozen", False):
    app_data_root = Path.home() / ".local" / "share" / APP_NAME
    app_data_root.mkdir(parents=True, exist_ok=True)
    os.chdir(app_data_root)

    data_dir = app_data_root / DATA_DIR
    data_dir.mkdir(parents=True, exist_ok=True)

    logs_dir = app_data_root / LOGS_DIR
    logs_dir.mkdir(parents=True, exist_ok=True)
