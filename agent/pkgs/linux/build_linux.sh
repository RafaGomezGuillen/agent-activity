#!/bin/bash

# Linux build script — compiles the agent with PyInstaller
set -e

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

APP_NAME="$(PROJECT_ROOT="$PROJECT_ROOT" python3 - <<'PY'
import os, sys
sys.path.insert(0, os.environ["PROJECT_ROOT"])
from config.settings import APP_NAME
print(APP_NAME)
PY
)"

INSTALL_BIN="/usr/local/bin/$APP_NAME"
SERVICE_FILE="/etc/systemd/system/$APP_NAME.service"
INSTALL_USER="${SUDO_USER:-$USER}"
INSTALL_HOME="$(eval echo ~"$INSTALL_USER")"
LOG_DIR="$INSTALL_HOME/.local/share/$APP_NAME/logs"

run_as_root() {
  if [ "$(id -u)" -eq 0 ]; then
    "$@"
  else
    sudo "$@"
  fi
}

if [ "$(id -u)" -ne 0 ] && ! command -v sudo >/dev/null 2>&1; then
  echo "ERROR: Root privileges are required to install to /usr/local and /etc/systemd/system."
  echo "Please run this script as root or install sudo."
  exit 1
fi

echo "Building $APP_NAME for Linux..."
echo "Project root : $PROJECT_ROOT"
echo "Install user : $INSTALL_USER"

# ---------------------------------------------------------------------------
# Clean old artifacts
# ---------------------------------------------------------------------------
echo "Cleaning old build artifacts..."
rm -rf "$PROJECT_ROOT/build/linux" "$PROJECT_ROOT/dist/linux"
mkdir -p "$PROJECT_ROOT/build/linux" "$PROJECT_ROOT/dist/linux"

# ---------------------------------------------------------------------------
# PyInstaller
# ---------------------------------------------------------------------------
echo "Running PyInstaller..."
cd "$PROJECT_ROOT"
python3 -m PyInstaller \
    "$SCRIPT_DIR/build_linux.spec" \
    --distpath "$PROJECT_ROOT/dist/linux" \
    --workpath "$PROJECT_ROOT/build/linux" \
    --noconfirm

echo "Build completed."

# ---------------------------------------------------------------------------
# Determine built binary path (onefile → single file, else directory)
# ---------------------------------------------------------------------------
ONEFILE="$(PROJECT_ROOT="$PROJECT_ROOT" python3 - <<'PY'
import os, sys
sys.path.insert(0, os.environ["PROJECT_ROOT"])
from pkgs.pyinstaller_config import COMMON_ARGS
print("yes" if COMMON_ARGS["onefile"] else "no")
PY
)"

if [ "$ONEFILE" = "yes" ]; then
  BUILT_BIN="$PROJECT_ROOT/dist/linux/$APP_NAME"
else
  BUILT_BIN="$PROJECT_ROOT/dist/linux/$APP_NAME/$APP_NAME"
fi

if [ ! -f "$BUILT_BIN" ]; then
  echo "ERROR: Built binary not found at $BUILT_BIN"
  exit 1
fi

# ---------------------------------------------------------------------------
# Install binary
# ---------------------------------------------------------------------------
echo "Installing binary to $INSTALL_BIN ..."
run_as_root cp "$BUILT_BIN" "$INSTALL_BIN"
run_as_root chmod +x "$INSTALL_BIN"

if [ "$ONEFILE" = "no" ]; then
  INSTALL_DIR="/usr/local/lib/$APP_NAME"
  echo "Installing application directory to $INSTALL_DIR ..."
  run_as_root rm -rf "$INSTALL_DIR"
  run_as_root cp -r "$PROJECT_ROOT/dist/linux/$APP_NAME" "$INSTALL_DIR"

  WRAPPER_FILE="$(mktemp)"
  cat > "$WRAPPER_FILE" <<WRAPPER
#!/bin/bash
exec "$INSTALL_DIR/$APP_NAME" "\$@"
WRAPPER
  run_as_root cp "$WRAPPER_FILE" "$INSTALL_BIN"
  run_as_root chmod +x "$INSTALL_BIN"
  rm -f "$WRAPPER_FILE"
fi

# ---------------------------------------------------------------------------
# Create log directory for the install user
# ---------------------------------------------------------------------------
mkdir -p "$LOG_DIR"
chown -R "$INSTALL_USER":"$INSTALL_USER" "$(dirname "$LOG_DIR")" 2>/dev/null || true

# ---------------------------------------------------------------------------
# Create systemd service unit
# ---------------------------------------------------------------------------
echo "Creating systemd service $SERVICE_FILE ..."
SERVICE_TMP_FILE="$(mktemp)"
cat > "$SERVICE_TMP_FILE" <<SERVICE
[Unit]
Description=$APP_NAME activity agent
After=network.target

[Service]
Type=simple
User=$INSTALL_USER
ExecStart=$INSTALL_BIN
Restart=on-failure
RestartSec=10
KillMode=control-group
StandardOutput=append:$LOG_DIR/service.log
StandardError=append:$LOG_DIR/service.log

[Install]
WantedBy=multi-user.target
SERVICE
run_as_root cp "$SERVICE_TMP_FILE" "$SERVICE_FILE"
rm -f "$SERVICE_TMP_FILE"

# ---------------------------------------------------------------------------
# Enable & start the service
# ---------------------------------------------------------------------------
echo "Reloading systemd daemon..."
run_as_root systemctl daemon-reload

echo "Enabling service to start on boot..."
run_as_root systemctl enable "$APP_NAME"

echo "Starting service..."
run_as_root systemctl start "$APP_NAME"

echo ""
echo "Installation complete!"
echo ""
echo "  systemctl status  $APP_NAME   — check status"
echo "  systemctl start   $APP_NAME   — start the agent"
echo "  systemctl stop    $APP_NAME   — stop the agent"
echo "  systemctl disable $APP_NAME   — disable auto-start"

