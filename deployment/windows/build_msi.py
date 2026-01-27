"""
MSI Installer Build Script for pyWATS Client

This script creates a Windows MSI installer from the frozen application.
Requires WiX Toolset v4+ to be installed.

Usage:
    python build_msi.py

Prerequisites:
    1. Run build_frozen.py first to create the frozen application
    2. Install WiX Toolset: dotnet tool install --global wix
    3. (Optional) Code signing certificate for production builds
"""

import os
import sys
import subprocess
import shutil
import uuid
from pathlib import Path
from datetime import datetime

# =============================================================================
# Configuration
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
PRODUCT_NAME = "pyWATS Client"
MANUFACTURER = "Virinco AS"
DESCRIPTION = "WATS Test Data Management Client"

# GUIDs - IMPORTANT: Keep these consistent across versions for upgrades
# Generate new ones only for completely new products
UPGRADE_CODE = "E7F2D8A1-4B5C-6D7E-8F9A-0B1C2D3E4F5A"  # Never change this
PRODUCT_CODE = str(uuid.uuid4()).upper()  # New for each version

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
BUILD_DIR = PROJECT_ROOT / "build"
DIST_DIR = PROJECT_ROOT / "dist"
FROZEN_DIR = BUILD_DIR / f"exe.win-amd64-{sys.version_info.major}.{sys.version_info.minor}"

# =============================================================================
# WiX Source Generation
# =============================================================================

def generate_wix_source():
    """Generate WiX source file from frozen application."""
    
    if not FROZEN_DIR.exists():
        print(f"❌ Frozen application not found: {FROZEN_DIR}")
        print("   Run 'python build_frozen.py' first")
        sys.exit(1)
    
    # Collect all files from frozen directory
    files = []
    components = []
    
    for i, path in enumerate(FROZEN_DIR.rglob("*")):
        if path.is_file():
            rel_path = path.relative_to(FROZEN_DIR)
            file_id = f"File_{i}"
            comp_id = f"Component_{i}"
            
            # Determine target directory
            if len(rel_path.parts) > 1:
                dir_path = "\\".join(rel_path.parts[:-1])
            else:
                dir_path = ""
            
            files.append({
                "id": file_id,
                "comp_id": comp_id,
                "source": str(path),
                "name": rel_path.name,
                "dir": dir_path,
            })
    
    # Generate WiX XML
    wix_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://wixtoolset.org/schemas/v4/wxs">
    
    <!-- Product Definition -->
    <Package 
        Name="{PRODUCT_NAME}"
        Version="{VERSION}"
        Manufacturer="{MANUFACTURER}"
        UpgradeCode="{UPGRADE_CODE}"
        Compressed="yes"
        InstallerVersion="500">
        
        <SummaryInformation Description="{DESCRIPTION}" />
        
        <!-- Upgrade handling -->
        <MajorUpgrade 
            DowngradeErrorMessage="A newer version of [ProductName] is already installed."
            Schedule="afterInstallInitialize" />
        
        <!-- Embedded cabinet -->
        <MediaTemplate EmbedCab="yes" CompressionLevel="high" />
        
        <!-- Install scope (per-machine) -->
        <Property Id="ALLUSERS" Value="1" />
        
        <!-- Custom properties -->
        <Property Id="INSTALL_SERVICE" Value="1" />
        <Property Id="START_SERVICE" Value="0" />
        
        <!-- Features -->
        <Feature Id="MainFeature" Title="{PRODUCT_NAME}" Level="1">
            <ComponentGroupRef Id="ProductComponents" />
            <ComponentRef Id="ProgramMenuShortcut" />
            <ComponentRef Id="DesktopShortcut" />
        </Feature>
        
        <Feature Id="ServiceFeature" Title="Windows Service" Level="1">
            <ComponentRef Id="ServiceComponent" />
            <Condition Level="0"><![CDATA[INSTALL_SERVICE = "0"]]></Condition>
        </Feature>
        
        <!-- Directory structure -->
        <StandardDirectory Id="ProgramFiles64Folder">
            <Directory Id="INSTALLDIR" Name="pyWATS">
                <Directory Id="LibDir" Name="lib" />
                <Directory Id="ResourcesDir" Name="resources" />
            </Directory>
        </StandardDirectory>
        
        <StandardDirectory Id="CommonAppDataFolder">
            <Directory Id="AppDataDir" Name="pyWATS">
                <Directory Id="LogsDir" Name="logs" />
                <Directory Id="QueueDir" Name="queue" />
            </Directory>
        </StandardDirectory>
        
        <StandardDirectory Id="ProgramMenuFolder">
            <Directory Id="ProgramMenuDir" Name="pyWATS" />
        </StandardDirectory>
        
        <StandardDirectory Id="DesktopFolder" />
        
        <!-- Components -->
        <ComponentGroup Id="ProductComponents" Directory="INSTALLDIR">
'''
    
    # Add file components
    for f in files:
        wix_xml += f'''            <Component Id="{f['comp_id']}" Guid="*">
                <File Id="{f['id']}" Source="{f['source']}" Name="{f['name']}" KeyPath="yes" />
            </Component>
'''
    
    wix_xml += f'''        </ComponentGroup>
        
        <!-- Program Menu Shortcut -->
        <Component Id="ProgramMenuShortcut" Directory="ProgramMenuDir" Guid="*">
            <Shortcut Id="StartMenuShortcut"
                      Name="{PRODUCT_NAME}"
                      Target="[INSTALLDIR]pywats-client-gui.exe"
                      WorkingDirectory="INSTALLDIR"
                      Icon="ProductIcon" />
            <RemoveFolder Id="RemoveProgramMenuDir" On="uninstall" />
            <RegistryValue Root="HKCU" Key="Software\\Virinco\\pyWATS" Name="MenuShortcut" Type="integer" Value="1" KeyPath="yes" />
        </Component>
        
        <!-- Desktop Shortcut -->
        <Component Id="DesktopShortcut" Directory="DesktopFolder" Guid="*">
            <Shortcut Id="DesktopShortcut"
                      Name="{PRODUCT_NAME}"
                      Target="[INSTALLDIR]pywats-client-gui.exe"
                      WorkingDirectory="INSTALLDIR"
                      Icon="ProductIcon" />
            <RegistryValue Root="HKCU" Key="Software\\Virinco\\pyWATS" Name="DesktopShortcut" Type="integer" Value="1" KeyPath="yes" />
        </Component>
        
        <!-- Windows Service -->
        <Component Id="ServiceComponent" Directory="INSTALLDIR" Guid="*">
            <File Id="ServiceExe" Source="{FROZEN_DIR / 'pywats-service.exe'}" Name="pywats-service.exe" KeyPath="yes" />
            <ServiceInstall
                Id="ServiceInstall"
                Name="pyWATSClient"
                DisplayName="pyWATS Client Service"
                Description="Monitors test results and uploads to WATS server"
                Type="ownProcess"
                Start="auto"
                ErrorControl="normal"
                Account="LocalSystem">
                <ServiceConfig DelayedAutoStart="yes" OnInstall="yes" OnReinstall="yes" />
            </ServiceInstall>
            <ServiceControl
                Id="ServiceControl"
                Name="pyWATSClient"
                Start="install"
                Stop="both"
                Remove="uninstall"
                Wait="yes" />
        </Component>
        
        <!-- Icon -->
        <Icon Id="ProductIcon" SourceFile="{SCRIPT_DIR / 'pywats.ico' if (SCRIPT_DIR / 'pywats.ico').exists() else FROZEN_DIR / 'pywats-client-gui.exe'}" />
        
        <!-- Custom Actions -->
        <CustomAction Id="StartService" Execute="deferred" Impersonate="no" Return="ignore"
                      Directory="INSTALLDIR" ExeCommand="[SystemFolder]sc.exe start pyWATSClient" />
        
        <InstallExecuteSequence>
            <Custom Action="StartService" After="StartServices">
                <![CDATA[START_SERVICE = "1" AND NOT REMOVE]]>
            </Custom>
        </InstallExecuteSequence>
        
    </Package>
</Wix>
'''
    
    return wix_xml

# =============================================================================
# Build Process
# =============================================================================

def build_msi():
    """Build the MSI installer."""
    
    print(f"🔨 Building MSI installer for pyWATS Client v{VERSION}")
    print(f"   Source: {FROZEN_DIR}")
    
    # Create dist directory
    DIST_DIR.mkdir(exist_ok=True)
    
    # Generate WiX source
    print("📝 Generating WiX source...")
    wix_source = generate_wix_source()
    wix_file = SCRIPT_DIR / "pywats.wxs"
    wix_file.write_text(wix_source, encoding="utf-8")
    print(f"   Written: {wix_file}")
    
    # Check for WiX
    wix_path = shutil.which("wix")
    if not wix_path:
        print("❌ WiX Toolset not found!")
        print("   Install with: dotnet tool install --global wix")
        print(f"\n📄 WiX source file created: {wix_file}")
        print("   You can build manually with: wix build pywats.wxs -o dist/pywats-client.msi")
        return False
    
    # Build MSI
    print("📦 Building MSI...")
    msi_name = f"pywats-client-{VERSION}.msi"
    msi_path = DIST_DIR / msi_name
    
    result = subprocess.run(
        ["wix", "build", str(wix_file), "-o", str(msi_path)],
        capture_output=True,
        text=True,
    )
    
    if result.returncode != 0:
        print(f"❌ WiX build failed:")
        print(result.stderr)
        return False
    
    print(f"✅ MSI created: {msi_path}")
    print(f"   Size: {msi_path.stat().st_size / 1024 / 1024:.1f} MB")
    
    # Sign if certificate available
    signtool = shutil.which("signtool")
    if signtool and os.environ.get("CODE_SIGN_CERT"):
        print("🔐 Signing MSI...")
        subprocess.run([
            "signtool", "sign",
            "/tr", "http://timestamp.digicert.com",
            "/td", "sha256",
            "/fd", "sha256",
            "/a",
            str(msi_path)
        ])
    
    return True

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    success = build_msi()
    sys.exit(0 if success else 1)
