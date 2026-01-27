# Standalone Executables (PyInstaller)

This folder contains PyInstaller configurations for creating standalone executables
that don't require Python to be installed on the target system.

## Overview

PyInstaller bundles the Python interpreter, all dependencies, and the application
into a single executable or folder that can be distributed independently.

## Supported Platforms

| Platform | Output | Size (approx) |
|----------|--------|---------------|
| Windows | `.exe` (single file or folder) | ~80-150 MB |
| Linux | ELF binary / AppImage | ~80-120 MB |
| macOS | `.app` bundle | ~100-150 MB |

## Build Requirements

### All Platforms
```bash
pip install pyinstaller pyinstaller-versionfile
```

### Linux (for AppImage)
```bash
# Install appimagetool
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
```

### Windows
- Visual C++ Redistributable (auto-included)
- UPX (optional, for compression): https://upx.github.io/

## Build Commands

### Quick Build (all platforms)
```bash
# Build for current platform
python build_standalone.py

# Build specific variant
python build_standalone.py --gui        # GUI client
python build_standalone.py --headless   # Headless client
python build_standalone.py --onefile    # Single executable
python build_standalone.py --onedir     # Folder distribution
```

### Manual PyInstaller Commands

#### Windows GUI Client
```bash
pyinstaller --name "pyWATS Client" \
    --windowed \
    --icon deployment/standalone/pywats.ico \
    --add-data "src/pywats_client/gui/resources;resources" \
    --hidden-import pywats \
    --hidden-import pywats_client \
    src/pywats_client/__main__.py
```

#### Linux Headless
```bash
pyinstaller --name pywats-client \
    --onefile \
    --hidden-import pywats \
    --hidden-import pywats_client \
    src/pywats_client/__main__.py
```

#### macOS App Bundle
```bash
pyinstaller --name "pyWATS Client" \
    --windowed \
    --osx-bundle-identifier com.virinco.pywats-client \
    --icon deployment/standalone/pywats.icns \
    --add-data "src/pywats_client/gui/resources:resources" \
    --hidden-import pywats \
    --hidden-import pywats_client \
    src/pywats_client/__main__.py
```

## Output Structure

### One-File Mode (`--onefile`)
```
dist/
└── pywats-client.exe    # Single executable (~80-150 MB)
```

Pros:
- Single file to distribute
- Easy to copy/deploy

Cons:
- Slower startup (extracts to temp on each run)
- Larger antivirus surface area

### One-Dir Mode (`--onedir`, default)
```
dist/
└── pyWATS Client/
    ├── pyWATS Client.exe    # Main executable
    ├── python311.dll        # Python runtime
    ├── _internal/           # Dependencies
    │   ├── pywats/
    │   ├── httpx/
    │   └── ...
    └── resources/           # App resources
```

Pros:
- Faster startup
- Easier debugging
- Lower antivirus false positives

Cons:
- Multiple files to distribute (use ZIP/installer)

## Linux AppImage

AppImage is the recommended distribution format for Linux:

```bash
# Build AppImage
python build_standalone.py --appimage

# Output: dist/pyWATS_Client-x86_64.AppImage
```

Users can run it directly:
```bash
chmod +x pyWATS_Client-x86_64.AppImage
./pyWATS_Client-x86_64.AppImage
```

## Troubleshooting

### Missing Modules
If PyInstaller misses a module:
1. Add to `--hidden-import` in spec file
2. Or add to `hiddenimports` list in build script

### Import Errors
Check that all dynamic imports are handled:
```python
# In your code, use try/except for optional imports
try:
    import PySide6
    HAS_GUI = True
except ImportError:
    HAS_GUI = False
```

### Large File Size
To reduce size:
1. Use `--exclude-module` for unused packages
2. Enable UPX compression: `--upx-dir /path/to/upx`
3. Strip debug symbols (Linux/macOS)

### Antivirus False Positives
Common with PyInstaller executables:
1. Sign the executable (Windows/macOS)
2. Submit to antivirus vendors for whitelisting
3. Use one-dir mode instead of one-file

## CI/CD Integration

See `.github/workflows/build-installers.yml` for automated builds.

Artifacts are uploaded to GitHub Releases for each version.
