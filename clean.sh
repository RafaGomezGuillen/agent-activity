#!/bin/bash
set -e

# Helper function to ask for confirmation
confirm_action() {
  local prompt_msg="$1"
  read -p "$prompt_msg (y/N): " response
  case "$response" in
    [yY][eE][sS]|[yY]) 
        return 0
        ;;
    *)
        return 1
        ;;
  esac
}

echo "Removing Agent build artifacts and temporary files..."
rm -rf "./agent/build"
rm -rf "./agent/dist"
rm -rf "./agent/logs"
rm -rf "./agent/data"

echo "Removing Backend build artifacts and temporary files..."
rm -rf "./backend/logs"
rm -rf "./backend/uploads"
rm -rf "./backend/database.db"

echo "Removing Frontend build artifacts and temporary files..."
rm -rf "./frontend/build"
rm -rf "./frontend/node_modules"
rm -rf "./frontend/dist"
rm -rf "./frontend/package-lock.json"

# Optional: Virtual Environments
if confirm_action "Do you want to remove the Python virtual environments (venv)?"; then
  echo "Removing venvs..."
  rm -rf "./agent/venv"
  rm -rf "./backend/venv"
else
  echo "Skipping venv removal."
fi

# Remove __pycache__ directories
echo "Removing __pycache__ directories..."
find "." -type d -name "__pycache__" -exec rm -rf {} +

echo "Cleaning completed successfully."