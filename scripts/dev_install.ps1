# pyWATS Development Installation Script
# =======================================
# This script installs pyWATS in development/editable mode.
# Settings are preserved in %APPDATA%\WATS\pyWATS-Client between updates.
#
# Usage:
#   .\scripts\dev_install.ps1           - Install/update in dev mode
#   .\scripts\dev_install.ps1 -Reinstall - Force reinstall
#

param(
    [switch]$Reinstall = $false
)

$ErrorActionPreference = "Stop"

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "=======================================" -ForegroundColor Cyan
Write-Host " pyWATS Development Installation" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the project directory
if (-not (Test-Path (Join-Path $ProjectRoot "pyproject.toml"))) {
    Write-Host "Error: pyproject.toml not found. Run this script from the pyWATS project directory." -ForegroundColor Red
    exit 1
}

# Check for virtual environment
$VenvPath = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $VenvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
. $ActivateScript

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
& $VenvPython -m pip install --upgrade pip --quiet

# Install/reinstall in editable mode
if ($Reinstall) {
    Write-Host "Uninstalling existing installation..." -ForegroundColor Yellow
    & $VenvPython -m pip uninstall pywats pywats-client -y 2>$null
}

Write-Host "Installing pyWATS in editable mode..." -ForegroundColor Yellow
& $VenvPython -m pip install -e $ProjectRoot --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Installation failed" -ForegroundColor Red
    exit 1
}

# Install additional dev dependencies if needed
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& $VenvPython -m pip install PySide6 httpx pydantic --quiet

# Create desktop shortcut for the GUI
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "pyWATS Client (Dev).lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -Command `"& '$VenvPython' -m pywats_client`""
$Shortcut.WorkingDirectory = $ProjectRoot
$Shortcut.Description = "pyWATS Client (Development Version)"
$Shortcut.Save()

Write-Host ""
Write-Host "=======================================" -ForegroundColor Green
Write-Host " Installation Complete!" -ForegroundColor Green
Write-Host "=======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Settings location:" -ForegroundColor Cyan
Write-Host "  $env:APPDATA\WATS\pyWATS-Client\" -ForegroundColor White
Write-Host ""
Write-Host "To run the GUI:" -ForegroundColor Cyan
Write-Host "  - Use the desktop shortcut: 'pyWATS Client (Dev)'" -ForegroundColor White
Write-Host "  - Or run: python -m pywats_client" -ForegroundColor White
Write-Host ""
Write-Host "To update after code changes:" -ForegroundColor Cyan
Write-Host "  - Code changes are automatically reflected (editable install)" -ForegroundColor White
Write-Host "  - For dependency changes, run: .\scripts\dev_install.ps1" -ForegroundColor White
Write-Host ""
