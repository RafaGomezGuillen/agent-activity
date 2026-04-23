#!/bin/bash

# macOS build script
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

echo "Building $APP_NAME for macOS..."
echo "Project root: $PROJECT_ROOT"

# Clean up old build and dist directories
echo "Cleaning old build artifacts..."
rm -rf "$PROJECT_ROOT/build/mac" "$PROJECT_ROOT/dist/mac"

# Create build directories
mkdir -p "$PROJECT_ROOT/build/mac" "$PROJECT_ROOT/dist/mac"

# Run PyInstaller
echo "Running PyInstaller..."
cd "$PROJECT_ROOT"
python3 -m PyInstaller \
    "$SCRIPT_DIR/build_mac.spec" \
    --distpath "$PROJECT_ROOT/dist/mac" \
    --workpath "$PROJECT_ROOT/build/mac" \
    --noconfirm

APP_PATH="$PROJECT_ROOT/dist/mac/$APP_NAME.app"
DMG_STAGE_DIR="$PROJECT_ROOT/build/mac/dmg"
DMG_PATH="$PROJECT_ROOT/dist/mac/$APP_NAME.dmg"
DMG_VOLUME_NAME="$APP_NAME Installer"

if [ ! -d "$APP_PATH" ]; then
  echo "Build finished but app bundle was not generated."
  exit 1
fi

echo "Preparing DMG contents..."
rm -rf "$DMG_STAGE_DIR" "$DMG_PATH"
mkdir -p "$DMG_STAGE_DIR"
cp -R "$APP_PATH" "$DMG_STAGE_DIR/"
ln -s /Applications "$DMG_STAGE_DIR/Applications"

echo "Creating DMG..."
hdiutil create \
    -volname "$DMG_VOLUME_NAME" \
    -srcfolder "$DMG_STAGE_DIR" \
    -ov \
    -format UDZO \
    "$DMG_PATH"

echo "Build completed successfully!"
echo "App bundle: $APP_PATH"
echo "DMG package: $DMG_PATH"
echo "Users can open the DMG and drag $APP_NAME to Applications."
