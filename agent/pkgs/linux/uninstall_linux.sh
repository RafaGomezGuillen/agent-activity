#!/bin/bash

# Linux uninstall script — stops and disables the systemd service, removes
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

APP_NAME="$(PROJECT_ROOT="$PROJECT_ROOT" python3 - 2>/dev/null <<'PY'
import os, sys
sys.path.insert(0, os.environ["PROJECT_ROOT"])
from config.settings import APP_NAME
print(APP_NAME)
PY
)" || APP_NAME=""

if [ -z "$APP_NAME" ]; then
  echo "ERROR: Could not determine APP_NAME. Aborting."
  exit 1
fi

INSTALL_USER="${SUDO_USER:-$USER}"
INSTALL_HOME="$(eval echo ~"$INSTALL_USER")"
SERVICE_FILE="/etc/systemd/system/$APP_NAME.service"
INSTALL_BIN="/usr/local/bin/$APP_NAME"
INSTALL_DIR="/usr/local/lib/$APP_NAME"
DATA_DIR="$INSTALL_HOME/.local/share/$APP_NAME"
LOCK_FILE="/tmp/$APP_NAME.lock"

echo "Uninstalling $APP_NAME..."

# ---------------------------------------------------------------------------
# Stop and disable the systemd service
# ---------------------------------------------------------------------------
if systemctl is-active --quiet "$APP_NAME" 2>/dev/null; then
  echo "Stopping $APP_NAME service..."
  systemctl stop "$APP_NAME"
fi

if systemctl is-enabled --quiet "$APP_NAME" 2>/dev/null; then
  echo "Disabling $APP_NAME service..."
  systemctl disable "$APP_NAME"
fi

# ---------------------------------------------------------------------------
# Kill any remaining processes (covers edge cases where the service may have
# been launched outside systemd)
# ---------------------------------------------------------------------------
echo "Killing any remaining $APP_NAME processes..."
pkill -9 -f "$APP_NAME" 2>/dev/null || true
sleep 1

# ---------------------------------------------------------------------------
# Remove systemd service file
# ---------------------------------------------------------------------------
if [ -f "$SERVICE_FILE" ]; then
  echo "Removing service file $SERVICE_FILE ..."
  rm -f "$SERVICE_FILE"
  systemctl daemon-reload
fi

# ---------------------------------------------------------------------------
# Remove installed binary and optional application directory
# ---------------------------------------------------------------------------
if [ -f "$INSTALL_BIN" ]; then
  echo "Removing binary $INSTALL_BIN ..."
  rm -f "$INSTALL_BIN"
fi

if [ -d "$INSTALL_DIR" ]; then
  echo "Removing application directory $INSTALL_DIR ..."
  rm -rf "$INSTALL_DIR"
fi

# ---------------------------------------------------------------------------
# Remove lock file
# ---------------------------------------------------------------------------
rm -f "$LOCK_FILE"

# ---------------------------------------------------------------------------
# Remove user data directory
# ---------------------------------------------------------------------------
if [ -d "$DATA_DIR" ]; then
  echo "Removing $DATA_DIR ..."
  rm -rf "$DATA_DIR"
fi

echo ""
echo "Uninstallation of $APP_NAME completed."
