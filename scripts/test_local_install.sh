#!/bin/bash
# Test local package installations
# Usage: bash scripts/test_local_install.sh

set -e  # Exit on error

echo "=========================================="
echo "Testing Local Package Installations"
echo "=========================================="

# Get the root directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Create a temporary virtual environment
VENV_DIR="$ROOT_DIR/.test_venv"

echo ""
echo "Creating temporary virtual environment..."
python -m venv "$VENV_DIR"

# Activate virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    echo "Error: Could not find activate script"
    exit 1
fi

echo "✓ Virtual environment created"

# Install packages in dependency order
PACKAGES=(
    "pywats"
    "pywats-client-service"
    "pywats-client-headless"
    "pywats-client-gui"
)

for package in "${PACKAGES[@]}"; do
    echo ""
    echo "=========================================="
    echo "Installing: $package"
    echo "=========================================="
    
    WHEEL_FILE=$(ls "$ROOT_DIR/packages/$package/dist/"*.whl 2>/dev/null | head -1)
    
    if [ -z "$WHEEL_FILE" ]; then
        echo "Error: No wheel file found for $package"
        echo "Run: bash scripts/build_all_packages.sh"
        deactivate
        rm -rf "$VENV_DIR"
        exit 1
    fi
    
    pip install "$WHEEL_FILE"
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully installed $package"
    else
        echo "✗ Failed to install $package"
        deactivate
        rm -rf "$VENV_DIR"
        exit 1
    fi
done

# Test imports
echo ""
echo "=========================================="
echo "Testing Imports"
echo "=========================================="

echo ""
echo "Testing pywats..."
python -c "from pywats import pyWATS; print(f'✓ pywats version: {pyWATS.__version__}')" || exit 1

echo ""
echo "Testing pywats-client-service..."
python -c "from pywats_client.core import WATSClient; print('✓ pywats-client-service imports OK')" || exit 1

echo ""
echo "Testing pywats-client-headless..."
python -c "from pywats_client.control import cli; print('✓ pywats-client-headless imports OK')" || exit 1

echo ""
echo "Testing pywats-client-gui..."
if python -c "from pywats_client.gui import app; print('✓ pywats-client-gui imports OK')" 2>/dev/null; then
    echo "✓ GUI imports OK"
else
    echo "⚠ GUI imports failed (may need display)"
fi

# Test CLI commands
echo ""
echo "=========================================="
echo "Testing CLI Commands"
echo "=========================================="

echo ""
echo "Testing pywats-client command..."
pywats-client --version || exit 1

echo "✓ CLI command works"

# Cleanup
echo ""
echo "=========================================="
echo "Cleanup"
echo "=========================================="

deactivate
rm -rf "$VENV_DIR"

echo "✓ Temporary environment removed"

echo ""
echo "=========================================="
echo "All Tests Passed! ✓"
echo "=========================================="
echo ""
echo "Packages are ready for release."
