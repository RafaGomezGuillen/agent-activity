"""
Runtime path setup for Windows bundled app.

When running as a PyInstaller executable, redirect relative paths so
logs and data are stored under %APPDATA%/<APP_NAME>.
"""

import os
import sys
from pathlib import Path

from config.settings import APP_NAME, LOGS_DIR, DATA_DIR


if getattr(sys, "frozen", False) and os.name == "nt":
    appdata = os.environ.get("APPDATA")
    if appdata:
        app_root = Path(appdata) / APP_NAME
    else:
        app_root = Path.home() / "AppData" / "Roaming" / APP_NAME

    app_root.mkdir(parents=True, exist_ok=True)
    os.chdir(app_root)

    (app_root / DATA_DIR).mkdir(parents=True, exist_ok=True)
    (app_root / LOGS_DIR).mkdir(parents=True, exist_ok=True)
