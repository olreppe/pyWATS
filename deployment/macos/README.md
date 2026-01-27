# macOS Installer

This folder contains the infrastructure for building macOS installers for pyWATS Client.

## Overview

The macOS distribution includes:
- `.app` bundle (drag-and-drop installation)
- `.pkg` installer (scripted installation)
- `.dmg` disk image (distribution format)

## Build Requirements

### Development Machine
- macOS 12+ (Monterey or later)
- Python 3.11+
- Xcode Command Line Tools

### Apple Developer Account (for distribution)
- Apple Developer Program membership ($99/year)
- Developer ID Application certificate (code signing)
- Developer ID Installer certificate (PKG signing)
- App-specific password for notarization

### Build Tools
```bash
# Install build dependencies
pip install py2app

# Install create-dmg (optional, for DMG creation)
brew install create-dmg
```

## Build Process

### 1. Build .app Bundle
```bash
# Create the .app bundle
python setup_app.py py2app

# Output: dist/pyWATS Client.app
```

### 2. Sign the Application
```bash
# Sign with Developer ID (required for distribution)
codesign --deep --force --options runtime \
    --sign "Developer ID Application: Virinco AS (TEAM_ID)" \
    --entitlements entitlements.plist \
    "dist/pyWATS Client.app"

# Verify signature
codesign --verify --deep --strict "dist/pyWATS Client.app"
spctl --assess --type exec "dist/pyWATS Client.app"
```

### 3. Create PKG Installer (Optional)
```bash
# Build component package
pkgbuild --root "dist/pyWATS Client.app" \
    --install-location "/Applications/pyWATS Client.app" \
    --identifier com.virinco.pywats-client \
    --version 1.0.0 \
    --sign "Developer ID Installer: Virinco AS (TEAM_ID)" \
    pywats-client-component.pkg

# Build product archive
productbuild --distribution Distribution.xml \
    --package-path . \
    --sign "Developer ID Installer: Virinco AS (TEAM_ID)" \
    pywats-client-1.0.0.pkg
```

### 4. Create DMG
```bash
# Using create-dmg (recommended)
create-dmg \
    --volname "pyWATS Client" \
    --volicon "pywats.icns" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "pyWATS Client.app" 150 190 \
    --app-drop-link 450 190 \
    --hide-extension "pyWATS Client.app" \
    "dist/pyWATS-Client-1.0.0.dmg" \
    "dist/pyWATS Client.app"
```

### 5. Notarize (Required for macOS 10.15+)
```bash
# Submit for notarization
xcrun notarytool submit pywats-client-1.0.0.pkg \
    --apple-id "developer@virinco.com" \
    --team-id "TEAM_ID" \
    --password "@keychain:AC_PASSWORD" \
    --wait

# Staple the notarization ticket
xcrun stapler staple pywats-client-1.0.0.pkg
xcrun stapler staple "dist/pyWATS-Client-1.0.0.dmg"
```

## Installation

### From DMG (Recommended)
1. Open the DMG file
2. Drag "pyWATS Client" to Applications folder
3. Eject the DMG
4. Launch from Applications or Launchpad

### From PKG
```bash
# Interactive
open pywats-client-1.0.0.pkg

# Command line (requires admin)
sudo installer -pkg pywats-client-1.0.0.pkg -target /
```

### Uninstall
```bash
# Remove application
rm -rf "/Applications/pyWATS Client.app"

# Remove data (optional)
rm -rf ~/Library/Application\ Support/pyWATS
rm -rf ~/Library/Preferences/com.virinco.pywats-client.plist
```

## launchd Service

For running as a background service:

```bash
# Install launch agent (user-level, starts on login)
cp com.virinco.pywats-client.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.virinco.pywats-client.plist

# Or install launch daemon (system-level, requires admin)
sudo cp com.virinco.pywats-client.plist /Library/LaunchDaemons/
sudo launchctl load /Library/LaunchDaemons/com.virinco.pywats-client.plist
```

## Directory Structure

After installation:
```
/Applications/
└── pyWATS Client.app/
    └── Contents/
        ├── Info.plist
        ├── MacOS/
        │   └── pyWATS Client    # Main executable
        ├── Resources/
        │   ├── pywats.icns
        │   └── lib/             # Python libraries
        └── Frameworks/          # Bundled frameworks

~/Library/Application Support/pyWATS/
├── config.json                  # Configuration
├── logs/                        # Log files
└── queue/                       # Offline queue
```

## Code Signing Notes

### Certificates Required
1. **Developer ID Application** - Signs the .app bundle
2. **Developer ID Installer** - Signs the .pkg installer

### Entitlements
The app requires these entitlements (see `entitlements.plist`):
- `com.apple.security.cs.allow-unsigned-executable-memory` - For Python
- `com.apple.security.network.client` - For HTTPS connections
- `com.apple.security.files.user-selected.read-write` - For file access

### Hardened Runtime
Code signing uses hardened runtime (`--options runtime`) which is required for notarization.

## Troubleshooting

### "App is damaged and can't be opened"
- App is not notarized or notarization failed
- Run: `xattr -cr "/Applications/pyWATS Client.app"`

### "App can't be opened because it is from an unidentified developer"
- App is not signed with Developer ID
- System Preferences > Security > "Open Anyway"

### Notarization Fails
1. Check all binaries are signed: `codesign -vvv --deep --strict app.app`
2. Check for unsigned libraries
3. Review notarization log: `xcrun notarytool log <submission-id>`

## CI/CD

See `.github/workflows/build-installers.yml` for automated builds.

Note: macOS builds require a macOS runner and code signing secrets.
