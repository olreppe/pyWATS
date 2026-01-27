# Windows MSI Installer

This folder contains the infrastructure for building Windows MSI installers for pyWATS Client.

## Overview

The Windows installer bundles:
- Python 3.11 runtime (embedded)
- pyWATS API library
- pyWATS Client application
- All dependencies

## Build Requirements

### Development Machine
- Windows 10/11 or Windows Server 2019+
- Python 3.11+ (for running build scripts)
- Visual Studio Build Tools 2019+ (for cx_Freeze)

### Build Tools
```powershell
# Install build dependencies
pip install cx_Freeze pyinstaller-versionfile

# Install WiX Toolset v4 (for MSI creation)
dotnet tool install --global wix
```

## Build Process

### 1. Freeze Python Application
```powershell
# Build frozen application
python build_frozen.py
```

This creates `build/frozen/` with:
- `pywats-client.exe` - Main executable
- `lib/` - Python libraries
- `python311.dll` - Python runtime

### 2. Create MSI Installer
```powershell
# Build MSI from frozen app
python build_msi.py
```

This creates `dist/pywats-client-{version}.msi`

## Installation

### Interactive Install
```powershell
msiexec /i pywats-client-1.0.0.msi
```

### Silent Install (GPO/SCCM)
```powershell
# Silent install with default options
msiexec /i pywats-client-1.0.0.msi /qn

# Silent install with custom options
msiexec /i pywats-client-1.0.0.msi /qn INSTALLDIR="D:\pyWATS" INSTALL_SERVICE=1

# Silent install with logging
msiexec /i pywats-client-1.0.0.msi /qn /l*v install.log
```

### Install Options

| Property | Default | Description |
|----------|---------|-------------|
| `INSTALLDIR` | `C:\Program Files\pyWATS` | Installation directory |
| `INSTALL_SERVICE` | `1` | Install Windows Service (0 to skip) |
| `START_SERVICE` | `0` | Start service after install |
| `CONFIG_URL` | (none) | Pre-configure WATS server URL |

## Uninstall

### Interactive
```powershell
# Via Control Panel > Programs > Uninstall
```

### Silent
```powershell
# By product code
msiexec /x {product-guid} /qn

# By MSI file
msiexec /x pywats-client-1.0.0.msi /qn
```

## Upgrade

The MSI supports in-place upgrades:
```powershell
# Upgrade preserves configuration
msiexec /i pywats-client-1.1.0.msi /qn
```

## Directory Structure

After installation:
```
C:\Program Files\pyWATS\
├── pywats-client.exe      # Main executable
├── python311.dll          # Python runtime
├── lib\                   # Python libraries
├── resources\             # Icons, images
└── uninstall.exe          # Uninstaller

C:\ProgramData\pyWATS\
├── config.json            # Configuration (preserved on upgrade)
├── logs\                  # Log files
└── queue\                 # Offline queue data
```

## Code Signing

For production releases, sign with Authenticode:
```powershell
# Sign the MSI
signtool sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a pywats-client-1.0.0.msi
```

## Troubleshooting

### MSI Install Fails
1. Check install log: `msiexec /i ... /l*v install.log`
2. Verify no previous version installed
3. Run as Administrator

### Service Won't Start
1. Check Event Viewer > Application
2. Verify config.json is valid
3. Test manually: `pywats-client.exe --diagnose`

## CI/CD

See `.github/workflows/build-installers.yml` for automated builds.
