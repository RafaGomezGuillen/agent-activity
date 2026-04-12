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

if [ $? -eq 0 ]; then
  echo "Build completed successfully!"
  echo "App location: $PROJECT_ROOT/dist/mac/$APP_NAME.app"
  
  # Copy app to Applications folder
  echo "Copying app to /Applications..."
  rm -rf "/Applications/$APP_NAME.app"
  cp -r "$PROJECT_ROOT/dist/mac/$APP_NAME.app" "/Applications/"
  echo "App installed to /Applications/$APP_NAME.app"
else
  echo "Build failed!"
  exit 1
fi

