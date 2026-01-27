"""
cx_Freeze Build Script for pyWATS Client

This script creates a frozen Python application that can be distributed
without requiring Python to be installed on the target system.

Usage:
    python build_frozen.py [--gui] [--headless] [--all]

Options:
    --gui       Build GUI client (requires PySide6)
    --headless  Build headless client (server/embedded)
    --all       Build both variants (default)
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from cx_Freeze import setup, Executable

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
COMPANY_NAME = "Virinco AS"
PRODUCT_NAME = "pyWATS Client"
DESCRIPTION = "WATS Test Data Management Client"
COPYRIGHT = "Copyright © 2024-2026 Virinco AS"

# =============================================================================
# Build Options
# =============================================================================

# Packages to include
PACKAGES = [
    "pywats",
    "pywats_client",
    "httpx",
    "pydantic",
    "watchdog",
    "aiofiles",
    "asyncio",
    "ssl",
    "certifi",
    "httpcore",
    "anyio",
    "sniffio",
    "h11",
    "h2",
    "hpack",
    "hyperframe",
    "idna",
    "attrs",
    "dateutil",
    "json",
    "logging",
]

# Packages to exclude (reduce size)
EXCLUDES = [
    "tkinter",
    "unittest",
    "test",
    "tests",
    "distutils",
    "setuptools",
    "pip",
    "wheel",
    "pkg_resources",
    "numpy",
    "pandas",
    "matplotlib",
    "scipy",
    "PIL",
    "cv2",
]

# Additional files to include
INCLUDE_FILES = [
    # Resources
    (Path(__file__).parent.parent.parent / "src" / "pywats_client" / "gui" / "resources", "resources"),
    # License
    (Path(__file__).parent.parent.parent / "LICENSE", "LICENSE.txt"),
    # README
    (Path(__file__).parent.parent.parent / "README.md", "README.md"),
]

# =============================================================================
# Build Configuration
# =============================================================================

build_options = {
    "packages": PACKAGES,
    "excludes": EXCLUDES,
    "include_files": INCLUDE_FILES,
    "include_msvcr": True,  # Include Visual C++ runtime
    "optimize": 2,
    "silent": False,
}

# =============================================================================
# Executables
# =============================================================================

# Base for GUI apps (no console window)
GUI_BASE = "Win32GUI" if sys.platform == "win32" else None

# Base for console/service apps
CONSOLE_BASE = None

executables = []

# Check command line args
args = sys.argv[1:] if len(sys.argv) > 1 else ["--all"]

if "--gui" in args or "--all" in args:
    executables.append(
        Executable(
            script=str(Path(__file__).parent.parent.parent / "src" / "pywats_client" / "__main__.py"),
            base=GUI_BASE,
            target_name="pywats-client-gui.exe",
            icon=str(Path(__file__).parent / "pywats.ico") if (Path(__file__).parent / "pywats.ico").exists() else None,
            copyright=COPYRIGHT,
            shortcut_name="pyWATS Client",
            shortcut_dir="DesktopFolder",
        )
    )

if "--headless" in args or "--all" in args:
    executables.append(
        Executable(
            script=str(Path(__file__).parent.parent.parent / "src" / "pywats_client" / "__main__.py"),
            base=CONSOLE_BASE,
            target_name="pywats-client.exe",
            icon=str(Path(__file__).parent / "pywats.ico") if (Path(__file__).parent / "pywats.ico").exists() else None,
            copyright=COPYRIGHT,
        )
    )

# Service executable (always console-based)
executables.append(
    Executable(
        script=str(Path(__file__).parent.parent.parent / "src" / "pywats_client" / "service" / "windows_service.py"),
        base=CONSOLE_BASE,
        target_name="pywats-service.exe",
        icon=str(Path(__file__).parent / "pywats.ico") if (Path(__file__).parent / "pywats.ico").exists() else None,
        copyright=COPYRIGHT,
    )
)

# =============================================================================
# Setup
# =============================================================================

setup(
    name=PRODUCT_NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=COMPANY_NAME,
    options={"build_exe": build_options},
    executables=executables,
)

print(f"\n✅ Build complete: pyWATS Client v{VERSION}")
print(f"   Output: build/exe.win-amd64-{sys.version_info.major}.{sys.version_info.minor}/")
