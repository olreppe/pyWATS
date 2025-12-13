#!/bin/bash
# Release packages to PyPI (production)
# Usage: bash scripts/release_to_pypi.sh

set -e  # Exit on error

echo "=========================================="
echo "RELEASING TO PYPI (PRODUCTION)"
echo "=========================================="
echo ""
echo "⚠️  WARNING: This will upload to production PyPI!"
echo ""
read -p "Have you tested on TestPyPI? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborting. Please test on TestPyPI first."
    exit 1
fi

echo ""
read -p "Are you sure you want to release to PyPI? (yes/no): " confirm2

if [ "$confirm2" != "yes" ]; then
    echo "Aborting."
    exit 1
fi

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
    
    if [ ! -d "$DIST_DIR" ]; then
        echo "Error: Dist directory not found for $package"
        echo "Run: bash scripts/build_all_packages.sh"
        exit 1
    fi
    
    if [ -z "$(ls -A $DIST_DIR 2>/dev/null)" ]; then
        echo "Error: No dist files found for $package"
        echo "Run: bash scripts/build_all_packages.sh"
        exit 1
    fi
    
    cd "$DIST_DIR"
    
    # Check package before upload
    echo "Checking package..."
    twine check *
    
    if [ $? -ne 0 ]; then
        echo "✗ Package check failed for $package"
        exit 1
    fi
    
    # Upload to PyPI
    twine upload *
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully uploaded $package to PyPI"
    else
        echo "✗ Failed to upload $package"
        exit 1
    fi
    
    # Small delay to avoid rate limiting
    sleep 2
done

echo ""
echo "=========================================="
echo "Release Complete! 🎉"
echo "=========================================="
echo ""
echo "Packages released:"
for package in "${PACKAGES[@]}"; do
    echo "  ✓ $package"
done
echo ""
echo "PyPI URLs:"
echo "  https://pypi.org/project/pywats/"
echo "  https://pypi.org/project/pywats-client-service/"
echo "  https://pypi.org/project/pywats-client-headless/"
echo "  https://pypi.org/project/pywats-client-gui/"
echo ""
echo "Next steps:"
echo "1. Tag the release in git: git tag -a v2.0.0 -m 'Release 2.0.0'"
echo "2. Push the tag: git push origin v2.0.0"
echo "3. Create GitHub release"
echo "4. Test installation: pip install pywats"
echo "5. Update documentation"
