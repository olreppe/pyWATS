# Quick launcher for pyWATS Client (Development)
# Run from project root: .\scripts\run_dev.ps1

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$VenvPython = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $VenvPython)) {
    Write-Host "Virtual environment not found. Run dev_install.ps1 first." -ForegroundColor Red
    exit 1
}

& $VenvPython -m pywats_client
