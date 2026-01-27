"""
py2app Setup Script for pyWATS Client

Creates a macOS .app bundle from the Python application.

Usage:
    python setup_app.py py2app

Requirements:
    pip install py2app
"""

import sys
import os
from pathlib import Path
from setuptools import setup

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

# =============================================================================
# Version Information
# =============================================================================

def get_version():
    """Get version from pyproject.toml"""
    try:
        import tomllib
        with open(Path(__file__).parent.parent.parent / "pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    except Exception:
        return "0.0.0"

VERSION = get_version()
APP_NAME = "pyWATS Client"
BUNDLE_ID = "com.virinco.pywats-client"

# =============================================================================
# Application Configuration
# =============================================================================

# Main script
APP = [str(Path(__file__).parent.parent.parent / "src" / "pywats_client" / "__main__.py")]

# Data files to include
DATA_FILES = [
    # Resources
    ('resources', [
        str(p) for p in (Path(__file__).parent.parent.parent / "src" / "pywats_client" / "gui" / "resources").glob("*")
        if p.is_file()
    ]),
]

# py2app options
OPTIONS = {
    'argv_emulation': False,  # Don't use argv emulation (deprecated)
    'iconfile': str(Path(__file__).parent / 'pywats.icns') if (Path(__file__).parent / 'pywats.icns').exists() else None,
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleIdentifier': BUNDLE_ID,
        'CFBundleVersion': VERSION,
        'CFBundleShortVersionString': VERSION,
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'LSMinimumSystemVersion': '12.0',
        'NSHighResolutionCapable': True,
        'NSHumanReadableCopyright': 'Copyright © 2024-2026 Virinco AS',
        'NSPrincipalClass': 'NSApplication',
        # Required for network access
        'NSAppTransportSecurity': {
            'NSAllowsArbitraryLoads': False,
            'NSAllowsArbitraryLoadsForMedia': False,
            'NSAllowsArbitraryLoadsInWebContent': False,
        },
        # URL scheme registration (optional)
        'CFBundleURLTypes': [
            {
                'CFBundleURLName': BUNDLE_ID,
                'CFBundleURLSchemes': ['pywats'],
            }
        ],
        # Document types (optional)
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'WATS Report',
                'CFBundleTypeExtensions': ['json', 'xml'],
                'CFBundleTypeRole': 'Viewer',
            }
        ],
    },
    'packages': [
        'pywats',
        'pywats_client',
        'httpx',
        'pydantic',
        'watchdog',
        'aiofiles',
        'certifi',
        'PySide6',  # Qt for GUI
    ],
    'excludes': [
        'tkinter',
        'unittest',
        'test',
        'distutils',
        'setuptools',
        'pip',
    ],
    'includes': [
        'ssl',
        'certifi',
        'asyncio',
    ],
    # Optimize for size
    'optimize': 2,
    'compressed': True,
    # Include Qt plugins
    'qt_plugins': [
        'platforms/libqcocoa.dylib',
        'styles/libqmacstyle.dylib',
    ] if sys.platform == 'darwin' else [],
}

# =============================================================================
# Setup
# =============================================================================

setup(
    name=APP_NAME,
    version=VERSION,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

print(f"\n✅ Build complete: {APP_NAME} v{VERSION}")
print(f"   Output: dist/{APP_NAME}.app")
