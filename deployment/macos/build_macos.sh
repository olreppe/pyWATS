#!/bin/bash
#
# Build script for macOS pyWATS Client distribution
#
# Usage:
#   ./build_macos.sh [--sign] [--notarize] [--dmg] [--pkg]
#
# Environment variables:
#   DEVELOPER_ID_APP    - "Developer ID Application: Name (TEAM_ID)"
#   DEVELOPER_ID_INST   - "Developer ID Installer: Name (TEAM_ID)"
#   APPLE_ID            - Apple ID email for notarization
#   TEAM_ID             - Apple Developer Team ID
#   AC_PASSWORD         - App-specific password (or @keychain:NAME)
#

set -e

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BUILD_DIR="$PROJECT_ROOT/build"
DIST_DIR="$PROJECT_ROOT/dist"

# Get version from pyproject.toml
VERSION=$(python3 -c "import tomllib; print(tomllib.load(open('$PROJECT_ROOT/pyproject.toml', 'rb'))['project']['version'])")

APP_NAME="pyWATS Client"
APP_BUNDLE="$DIST_DIR/$APP_NAME.app"
DMG_NAME="pyWATS-Client-$VERSION.dmg"
PKG_NAME="pywats-client-$VERSION.pkg"

# Signing identities (set via environment or defaults)
DEVELOPER_ID_APP="${DEVELOPER_ID_APP:-}"
DEVELOPER_ID_INST="${DEVELOPER_ID_INST:-}"

# Flags
DO_SIGN=false
DO_NOTARIZE=false
DO_DMG=false
DO_PKG=false

# =============================================================================
# Parse Arguments
# =============================================================================

while [[ $# -gt 0 ]]; do
    case $1 in
        --sign)
            DO_SIGN=true
            shift
            ;;
        --notarize)
            DO_NOTARIZE=true
            DO_SIGN=true  # Notarization requires signing
            shift
            ;;
        --dmg)
            DO_DMG=true
            shift
            ;;
        --pkg)
            DO_PKG=true
            shift
            ;;
        --all)
            DO_SIGN=true
            DO_NOTARIZE=true
            DO_DMG=true
            DO_PKG=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# =============================================================================
# Functions
# =============================================================================

log() {
    echo "==> $1"
}

error() {
    echo "ERROR: $1" >&2
    exit 1
}

check_requirements() {
    log "Checking requirements..."
    
    # Check for py2app
    python3 -c "import py2app" 2>/dev/null || error "py2app not installed. Run: pip install py2app"
    
    # Check for Xcode tools
    xcode-select -p >/dev/null 2>&1 || error "Xcode Command Line Tools not installed"
    
    if $DO_SIGN; then
        [[ -n "$DEVELOPER_ID_APP" ]] || error "DEVELOPER_ID_APP not set"
        # Verify certificate exists
        security find-identity -v -p codesigning | grep -q "$DEVELOPER_ID_APP" || \
            error "Certificate not found: $DEVELOPER_ID_APP"
    fi
    
    if $DO_NOTARIZE; then
        [[ -n "$APPLE_ID" ]] || error "APPLE_ID not set"
        [[ -n "$TEAM_ID" ]] || error "TEAM_ID not set"
        [[ -n "$AC_PASSWORD" ]] || error "AC_PASSWORD not set"
    fi
    
    if $DO_DMG; then
        command -v create-dmg >/dev/null 2>&1 || \
            log "Warning: create-dmg not found, using hdiutil instead"
    fi
}

build_app() {
    log "Building .app bundle..."
    
    cd "$SCRIPT_DIR"
    
    # Clean previous build
    rm -rf "$BUILD_DIR" "$DIST_DIR"
    
    # Run py2app
    python3 setup_app.py py2app
    
    [[ -d "$APP_BUNDLE" ]] || error "Build failed: $APP_BUNDLE not found"
    
    log "App bundle created: $APP_BUNDLE"
}

sign_app() {
    log "Signing application..."
    
    # Sign with hardened runtime (required for notarization)
    codesign --deep --force --options runtime \
        --sign "$DEVELOPER_ID_APP" \
        --entitlements "$SCRIPT_DIR/entitlements.plist" \
        "$APP_BUNDLE"
    
    # Verify
    codesign --verify --deep --strict "$APP_BUNDLE"
    spctl --assess --type exec "$APP_BUNDLE" || \
        log "Warning: Gatekeeper assessment failed (may need notarization)"
    
    log "Application signed successfully"
}

build_pkg() {
    log "Building PKG installer..."
    
    local COMPONENT_PKG="$DIST_DIR/pywats-component.pkg"
    
    # Build component package
    pkgbuild --root "$APP_BUNDLE" \
        --install-location "/Applications/$APP_NAME.app" \
        --identifier "com.virinco.pywats-client" \
        --version "$VERSION" \
        ${DEVELOPER_ID_INST:+--sign "$DEVELOPER_ID_INST"} \
        "$COMPONENT_PKG"
    
    # Build product archive with distribution
    if [[ -f "$SCRIPT_DIR/Distribution.xml" ]]; then
        productbuild --distribution "$SCRIPT_DIR/Distribution.xml" \
            --package-path "$DIST_DIR" \
            ${DEVELOPER_ID_INST:+--sign "$DEVELOPER_ID_INST"} \
            "$DIST_DIR/$PKG_NAME"
        rm "$COMPONENT_PKG"
    else
        mv "$COMPONENT_PKG" "$DIST_DIR/$PKG_NAME"
    fi
    
    log "PKG created: $DIST_DIR/$PKG_NAME"
}

build_dmg() {
    log "Building DMG..."
    
    local DMG_PATH="$DIST_DIR/$DMG_NAME"
    
    if command -v create-dmg >/dev/null 2>&1; then
        # Use create-dmg for nicer DMG
        create-dmg \
            --volname "$APP_NAME" \
            ${SCRIPT_DIR}/pywats.icns:+--volicon "$SCRIPT_DIR/pywats.icns"} \
            --window-pos 200 120 \
            --window-size 600 400 \
            --icon-size 100 \
            --icon "$APP_NAME.app" 150 190 \
            --app-drop-link 450 190 \
            --hide-extension "$APP_NAME.app" \
            "$DMG_PATH" \
            "$APP_BUNDLE"
    else
        # Fallback to hdiutil
        local TEMP_DMG="$DIST_DIR/temp.dmg"
        local MOUNT_DIR="/Volumes/$APP_NAME"
        
        # Create temporary DMG
        hdiutil create -srcfolder "$APP_BUNDLE" -volname "$APP_NAME" \
            -fs HFS+ -fsargs "-c c=64,a=16,e=16" -format UDRW "$TEMP_DMG"
        
        # Mount and customize (optional)
        # hdiutil attach "$TEMP_DMG"
        # ... customize layout ...
        # hdiutil detach "$MOUNT_DIR"
        
        # Convert to compressed read-only
        hdiutil convert "$TEMP_DMG" -format UDZO -imagekey zlib-level=9 -o "$DMG_PATH"
        rm "$TEMP_DMG"
    fi
    
    log "DMG created: $DMG_PATH"
}

notarize() {
    log "Submitting for notarization..."
    
    local TARGET="$DIST_DIR/$PKG_NAME"
    [[ -f "$TARGET" ]] || TARGET="$DIST_DIR/$DMG_NAME"
    [[ -f "$TARGET" ]] || TARGET="$APP_BUNDLE"
    
    # Submit for notarization
    xcrun notarytool submit "$TARGET" \
        --apple-id "$APPLE_ID" \
        --team-id "$TEAM_ID" \
        --password "$AC_PASSWORD" \
        --wait
    
    # Staple the ticket
    if [[ -f "$DIST_DIR/$PKG_NAME" ]]; then
        xcrun stapler staple "$DIST_DIR/$PKG_NAME"
    fi
    
    if [[ -f "$DIST_DIR/$DMG_NAME" ]]; then
        xcrun stapler staple "$DIST_DIR/$DMG_NAME"
    fi
    
    log "Notarization complete"
}

# =============================================================================
# Main
# =============================================================================

main() {
    log "Building pyWATS Client v$VERSION for macOS"
    
    check_requirements
    build_app
    
    $DO_SIGN && sign_app
    $DO_PKG && build_pkg
    $DO_DMG && build_dmg
    $DO_NOTARIZE && notarize
    
    log "Build complete!"
    log "Outputs:"
    ls -la "$DIST_DIR"
}

main
