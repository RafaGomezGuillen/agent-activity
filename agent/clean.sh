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
rm -rf "./build"
rm -rf "./dist"
rm -rf "./logs"
rm -rf "./data"

# Optional: Virtual Environments
if confirm_action "Do you want to remove the Python virtual environments (venv)?"; then
  echo "Removing venv..."
  rm -rf "./venv"
else
  echo "Skipping venv removal."
fi

# Remove __pycache__ directories
echo "Removing __pycache__ directories..."
find "." -type d -name "__pycache__" -exec rm -rf {} +

echo "Cleaning completed successfully."