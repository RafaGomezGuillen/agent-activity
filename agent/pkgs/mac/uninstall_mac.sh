#!/bin/bash

# macOS uninstall script
set -e

# Define paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
APP_NAME="$(PROJECT_ROOT="$PROJECT_ROOT" python3 - <<'PY'
import os
import sys

sys.path.insert(0, os.environ["PROJECT_ROOT"])
from config.settings import APP_NAME

print(APP_NAME)
PY
)"

echo "Uninstalling $APP_NAME..."

# Stop and kill any running app processes
echo "Stopping $APP_NAME processes..."
pkill -f "$APP_NAME" 2>/dev/null || true
sleep 1

# Remove app from Applications folder
if [ -d "/Applications/$APP_NAME.app" ]; then
  echo "Removing app from /Applications..."
  rm -rf "/Applications/$APP_NAME.app"
else
  echo "App not found in /Applications"
fi

# Remove application support files
if [ -d "$HOME/Library/Application Support/$APP_NAME" ]; then
  echo "Removing application support files..."
  rm -rf "$HOME/Library/Application Support/$APP_NAME"
fi

echo "Uninstallation completed successfully!"