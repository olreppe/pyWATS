"""
PyInstaller Build Script for pyWATS Client Standalone Executables

Creates standalone executables for Windows, Linux, and macOS that don't
require Python to be pre-installed.

Usage:
    python build_standalone.py [options]

Options:
    --gui         Build GUI client (default)
    --headless    Build headless client (no GUI dependencies)
    --onefile     Single executable (slower startup)
    --onedir      Directory distribution (faster startup, default)
    --appimage    Build Linux AppImage (Linux only)
    --clean       Clean build directories before building
    --debug       Include debug information

Requirements:
    pip install pyinstaller pyinstaller-versionfile
"""

import sys
import os
import shutil
import subprocess
import argparse
from pathlib import Path

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
SRC_DIR = PROJECT_ROOT / "src"
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"

def get_version():
    """Get version from pyproject.toml"""
    try:
        import tomllib
        with open(PROJECT_ROOT / "pyproject.toml", "rb") as f:
            data = tomllib.load(f)
            return data["project"]["version"]
    except Exception:
        return "0.0.0"

VERSION = get_version()
APP_NAME = "pyWATS Client"
APP_NAME_HEADLESS = "pywats-client"

# =============================================================================
# PyInstaller Options
# =============================================================================

# Hidden imports that PyInstaller might miss
HIDDEN_IMPORTS = [
    "pywats",
    "pywats.client",
    "pywats.domains",
    "pywats.domains.report",
    "pywats.domains.asset",
    "pywats.domains.product",
    "pywats.domains.process",
    "pywats.domains.production",
    "pywats.domains.analytics",
    "pywats.domains.software",
    "pywats.domains.rootcause",
    "pywats_client",
    "pywats_client.core",
    "pywats_client.service",
    "httpx",
    "httpx._transports",
    "httpcore",
    "h11",
    "h2",
    "hpack",
    "hyperframe",
    "pydantic",
    "pydantic.v1",
    "watchdog",
    "watchdog.observers",
    "aiofiles",
    "certifi",
    "ssl",
    "asyncio",
    "json",
    "logging",
    "typing_extensions",
]

# GUI-specific imports
GUI_IMPORTS = [
    "PySide6",
    "PySide6.QtCore",
    "PySide6.QtGui",
    "PySide6.QtWidgets",
]

# Windows-specific imports
WINDOWS_IMPORTS = [
    "win32serviceutil",
    "win32service",
    "win32event",
    "servicemanager",
    "win32api",
    "win32con",
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
    "IPython",
    "jupyter",
]

# =============================================================================
# Build Functions
# =============================================================================

def clean():
    """Clean build directories."""
    print("🧹 Cleaning build directories...")
    for d in [BUILD_DIR, DIST_DIR]:
        if d.exists():
            shutil.rmtree(d)
    
    # Clean PyInstaller cache
    spec_files = list(PROJECT_ROOT.glob("*.spec"))
    for f in spec_files:
        f.unlink()


def build_pyinstaller(gui=True, onefile=False, debug=False):
    """Build with PyInstaller."""
    
    name = APP_NAME if gui else APP_NAME_HEADLESS
    print(f"🔨 Building {name} v{VERSION}")
    print(f"   Platform: {sys.platform}")
    print(f"   Mode: {'onefile' if onefile else 'onedir'}")
    print(f"   GUI: {gui}")
    
    # Base command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name", name,
        "--noconfirm",
    ]
    
    # One-file or one-dir
    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    
    # GUI vs console
    if gui and sys.platform in ("win32", "darwin"):
        cmd.append("--windowed")
    else:
        cmd.append("--console")
    
    # Icon
    if sys.platform == "win32":
        icon = SCRIPT_DIR / "pywats.ico"
        if icon.exists():
            cmd.extend(["--icon", str(icon)])
    elif sys.platform == "darwin":
        icon = SCRIPT_DIR / "pywats.icns"
        if icon.exists():
            cmd.extend(["--icon", str(icon)])
            cmd.extend(["--osx-bundle-identifier", "com.virinco.pywats-client"])
    
    # Hidden imports
    imports = HIDDEN_IMPORTS.copy()
    if gui:
        imports.extend(GUI_IMPORTS)
    if sys.platform == "win32":
        imports.extend(WINDOWS_IMPORTS)
    
    for imp in imports:
        cmd.extend(["--hidden-import", imp])
    
    # Excludes
    for exc in EXCLUDES:
        cmd.extend(["--exclude-module", exc])
    
    # Data files
    resources = SRC_DIR / "pywats_client" / "gui" / "resources"
    if resources.exists():
        sep = ";" if sys.platform == "win32" else ":"
        cmd.extend(["--add-data", f"{resources}{sep}resources"])
    
    # Debug
    if debug:
        cmd.append("--debug=all")
    
    # Entry point
    cmd.append(str(SRC_DIR / "pywats_client" / "__main__.py"))
    
    # Run PyInstaller
    print(f"   Command: {' '.join(cmd[:5])}...")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if result.returncode != 0:
        print(f"❌ Build failed with code {result.returncode}")
        return False
    
    # Verify output
    if onefile:
        if sys.platform == "win32":
            output = DIST_DIR / f"{name}.exe"
        else:
            output = DIST_DIR / name
    else:
        output = DIST_DIR / name
    
    if output.exists():
        if output.is_file():
            size = output.stat().st_size / 1024 / 1024
        else:
            size = sum(f.stat().st_size for f in output.rglob("*") if f.is_file()) / 1024 / 1024
        print(f"✅ Build complete: {output}")
        print(f"   Size: {size:.1f} MB")
        return True
    else:
        print(f"❌ Output not found: {output}")
        return False


def build_appimage():
    """Build Linux AppImage."""
    
    if sys.platform != "linux":
        print("❌ AppImage can only be built on Linux")
        return False
    
    print("📦 Building AppImage...")
    
    # First build onedir
    if not build_pyinstaller(gui=False, onefile=False):
        return False
    
    app_dir = DIST_DIR / f"{APP_NAME}.AppDir"
    
    # Create AppDir structure
    app_dir.mkdir(exist_ok=True)
    (app_dir / "usr" / "bin").mkdir(parents=True, exist_ok=True)
    (app_dir / "usr" / "share" / "applications").mkdir(parents=True, exist_ok=True)
    (app_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps").mkdir(parents=True, exist_ok=True)
    
    # Copy built application
    src_dir = DIST_DIR / APP_NAME_HEADLESS
    for item in src_dir.iterdir():
        dst = app_dir / "usr" / "bin" / item.name
        if item.is_dir():
            shutil.copytree(item, dst)
        else:
            shutil.copy2(item, dst)
    
    # Create AppRun script
    apprun = app_dir / "AppRun"
    apprun.write_text(f"""#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${{SELF%/*}}
export PATH="${{HERE}}/usr/bin:${{PATH}}"
export LD_LIBRARY_PATH="${{HERE}}/usr/lib:${{LD_LIBRARY_PATH}}"
exec "${{HERE}}/usr/bin/{APP_NAME_HEADLESS}" "$@"
""")
    apprun.chmod(0o755)
    
    # Create .desktop file
    desktop = app_dir / f"{APP_NAME_HEADLESS}.desktop"
    desktop.write_text(f"""[Desktop Entry]
Type=Application
Name={APP_NAME}
Exec={APP_NAME_HEADLESS}
Icon={APP_NAME_HEADLESS}
Categories=Utility;Development;
Comment=WATS Test Data Management Client
Terminal=false
""")
    shutil.copy2(desktop, app_dir / "usr" / "share" / "applications")
    
    # Copy icon
    icon_src = SCRIPT_DIR / "pywats.png"
    if icon_src.exists():
        shutil.copy2(icon_src, app_dir / f"{APP_NAME_HEADLESS}.png")
        shutil.copy2(icon_src, app_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps" / f"{APP_NAME_HEADLESS}.png")
    
    # Build AppImage
    appimage_name = f"pyWATS_Client-{VERSION}-x86_64.AppImage"
    result = subprocess.run(
        ["appimagetool", str(app_dir), str(DIST_DIR / appimage_name)],
        cwd=DIST_DIR
    )
    
    if result.returncode == 0:
        print(f"✅ AppImage created: {DIST_DIR / appimage_name}")
        return True
    else:
        print("❌ AppImage creation failed")
        return False


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Build pyWATS standalone executables")
    parser.add_argument("--gui", action="store_true", help="Build GUI client (default)")
    parser.add_argument("--headless", action="store_true", help="Build headless client")
    parser.add_argument("--onefile", action="store_true", help="Single executable")
    parser.add_argument("--onedir", action="store_true", help="Directory distribution (default)")
    parser.add_argument("--appimage", action="store_true", help="Build Linux AppImage")
    parser.add_argument("--clean", action="store_true", help="Clean before building")
    parser.add_argument("--debug", action="store_true", help="Include debug info")
    parser.add_argument("--all", action="store_true", help="Build all variants")
    
    args = parser.parse_args()
    
    # Defaults
    if not args.gui and not args.headless:
        args.gui = True
    if not args.onefile and not args.onedir:
        args.onedir = True
    
    # Clean
    if args.clean:
        clean()
    
    # Build
    success = True
    
    if args.all:
        # Build everything
        success &= build_pyinstaller(gui=True, onefile=False, debug=args.debug)
        success &= build_pyinstaller(gui=True, onefile=True, debug=args.debug)
        success &= build_pyinstaller(gui=False, onefile=False, debug=args.debug)
        success &= build_pyinstaller(gui=False, onefile=True, debug=args.debug)
        if sys.platform == "linux":
            success &= build_appimage()
    elif args.appimage:
        success = build_appimage()
    else:
        success = build_pyinstaller(
            gui=args.gui and not args.headless,
            onefile=args.onefile,
            debug=args.debug
        )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
