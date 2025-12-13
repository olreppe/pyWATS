#!/bin/bash
# Upload packages to TestPyPI for testing
# Usage: bash scripts/upload_to_testpypi.sh

set -e  # Exit on error

echo "=========================================="
echo "Uploading to TestPyPI"
echo "=========================================="

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "Error: twine is not installed"
    echo "Install with: pip install twine"
    exit 1
fi

# Get the root directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Array of packages in dependency order
PACKAGES=(
    "pywats"
    "pywats-client-service"
    "pywats-client-headless"
    "pywats-client-gui"
)

# Upload each package
for package in "${PACKAGES[@]}"; do
    echo ""
    echo "=========================================="
    echo "Uploading: $package"
    echo "=========================================="
    
    DIST_DIR="$ROOT_DIR/packages/$package/dist"
    
    if [ ! -d "$DIST_DIR" ] || [ -z "$(ls -A $DIST_DIR)" ]; then
        echo "Error: No dist files found for $package"
        echo "Run: bash scripts/build_all_packages.sh"
        exit 1
    fi
    
    cd "$DIST_DIR"
    
    # Upload to TestPyPI
    twine upload --repository testpypi *
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully uploaded $package to TestPyPI"
    else
        echo "✗ Failed to upload $package"
        exit 1
    fi
    
    # Small delay to avoid rate limiting
    sleep 2
done

echo ""
echo "=========================================="
echo "Upload Complete!"
echo "=========================================="
echo ""
echo "Test installation:"
echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats"
echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats-client-headless"
echo "  pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats-client-gui"
echo ""
echo "View packages:"
echo "  https://test.pypi.org/project/pywats/"
echo "  https://test.pypi.org/project/pywats-client-service/"
echo "  https://test.pypi.org/project/pywats-client-headless/"
echo "  https://test.pypi.org/project/pywats-client-gui/"
