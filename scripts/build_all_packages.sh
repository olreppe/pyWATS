#!/bin/bash
# Build all pyWATS packages
# Usage: bash scripts/build_all_packages.sh

set -e  # Exit on error

echo "=========================================="
echo "Building pyWATS Packages"
echo "=========================================="

# Get the root directory
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Clean previous builds
echo ""
echo "Cleaning previous builds..."
find packages -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
find packages -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
find packages -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Array of packages in dependency order
PACKAGES=(
    "pywats"
    "pywats-client-service"
    "pywats-client-headless"
    "pywats-client-gui"
)

# Build each package
for package in "${PACKAGES[@]}"; do
    echo ""
    echo "=========================================="
    echo "Building: $package"
    echo "=========================================="
    
    cd "$ROOT_DIR/packages/$package"
    
    # Create dist directory if it doesn't exist
    mkdir -p dist
    
    # Build the package
    python -m build
    
    if [ $? -eq 0 ]; then
        echo "✓ Successfully built $package"
        echo "  Output: packages/$package/dist/"
    else
        echo "✗ Failed to build $package"
        exit 1
    fi
done

echo ""
echo "=========================================="
echo "Build Summary"
echo "=========================================="
echo ""

# Show what was built
for package in "${PACKAGES[@]}"; do
    echo "$package:"
    DIST_DIR="$ROOT_DIR/packages/$package/dist"
    if [ -d "$DIST_DIR" ] && [ -n "$(ls -A "$DIST_DIR" 2>/dev/null)" ]; then
        ls -lh "$DIST_DIR" | grep -E '\.(whl|tar\.gz)$' || echo "  No package files found"
    else
        echo "  Dist directory empty or not found"
    fi
    echo ""
done

echo "=========================================="
echo "All packages built successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test installations locally"
echo "2. Upload to TestPyPI: bash scripts/upload_to_testpypi.sh"
echo "3. Upload to PyPI: bash scripts/release_to_pypi.sh"
