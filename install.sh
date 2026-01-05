#!/usr/bin/env bash
# install.sh - clone and install common (editable)
# Usage: ./install.sh [target_dir] [python_exe] [mode]
#  - target_dir: where to clone (default: $HOME/common)
#  - python_exe: optional python command (default: first 'python3' or 'python')
#  - mode: "system" to install into the given python, or omit to create a venv and install there

set -euo pipefail
IFS=$'\n\t'

REPO_URL="https://github.com/NadavElsbreg/common.git"
TARGET="${1:-$HOME/common}"
PYTHON_EXE="${2:-}"
MODE="${3:-}"

echo "Target directory: $TARGET"
echo "Install mode: $MODE"

command -v git >/dev/null 2>&1 || { echo "ERROR: git not found in PATH."; exit 1; }

# Resolve python if not provided
if [ -z "$PYTHON_EXE" ]; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_EXE=python3
  elif command -v python >/dev/null 2>&1; then
    PYTHON_EXE=python
  else
    echo "ERROR: No python found in PATH. Install Python 3.12+ and re-run."; exit 1
  fi
fi

echo "Using Python: $PYTHON_EXE"

# Verify python version >= 3.12
PY_VER=$($PYTHON_EXE -c "import sys; v=sys.version_info; print(f'{v[0]}.{v[1]}.{v[2]}')") || true
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 12 ]; }; then
  echo "ERROR: Python >= 3.12 required; detected $PY_VER"; exit 1
fi

echo "Python version: $PY_VER"

# Clone or update
if [ -d "$TARGET/.git" ]; then
  echo "Directory exists and looks like a git repo, pulling latest..."
  git -C "$TARGET" pull || { echo "Git pull failed"; exit 1; }
else
  echo "Cloning repository..."
  git clone "$REPO_URL" "$TARGET" || { echo "Git clone failed"; exit 1; }
fi

if [ "$MODE" = "system" ]; then
  echo "Installing package (editable) into specified Python..."
  "$PYTHON_EXE" -m pip install --upgrade pip setuptools wheel
  "$PYTHON_EXE" -m pip install -e "$TARGET" -v || { echo "Pip install failed"; exit 1; }
  echo "Inspecting installation:"
  "$PYTHON_EXE" -m pip show common || echo "pip show common returned nothing for this interpreter"
  exit 0
fi

# Default: create venv inside target and install there
VENV_DIR="$TARGET/venv"
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv in $VENV_DIR"
  "$PYTHON_EXE" -m venv "$VENV_DIR" || { echo "Failed to create venv"; exit 1; }
fi

VENV_PY="$VENV_DIR/bin/python"
if [ ! -x "$VENV_PY" ]; then
  echo "ERROR: venv python not found at $VENV_PY"; exit 1
fi

echo "Upgrading pip in venv..."
"$VENV_PY" -m pip install --upgrade pip setuptools wheel

echo "Installing package in editable mode into venv..."
"$VENV_PY" -m pip install -e "$TARGET" -v || { echo "Pip install failed inside venv"; exit 1; }

echo "Verifying installation inside venv:"
"$VENV_PY" -m pip show common || echo "pip show common returned nothing for the venv"
"$VENV_PY" -c "import common; import inspect; print('common at', getattr(common,'__file__', None))" || echo "Failed to import common from the venv"

echo "SUCCESS: Repository cloned to $TARGET and installed (editable) in $VENV_DIR"
echo "To use it, activate the venv: source $VENV_DIR/bin/activate"
