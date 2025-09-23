# pyWATS Development Environment Setup Script (PowerShell)
# This script sets up the development environment for pyWATS

Write-Host "[SETUP] Setting up pyWATS development environment..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "[CREATE] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "[SUCCESS] Virtual environment created!" -ForegroundColor Green
} else {
    Write-Host "[INFO] Virtual environment already exists" -ForegroundColor Cyan
}

# Install dependencies
Write-Host "[INSTALL] Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe -m pip install --upgrade pip
& .\venv\Scripts\python.exe -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[SUCCESS] Dependencies installed!" -ForegroundColor Green

# Test the installation
Write-Host "[TEST] Testing installation..." -ForegroundColor Yellow
& .\venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'src'); from pyWATS.connection import create_connection; print('[SUCCESS] pyWATS is ready!')"

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Installation test failed" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "[COMPLETE] Setup complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host "To activate the environment, run: .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "To run the example: .\venv\Scripts\python.exe main.py" -ForegroundColor Cyan
Write-Host "To run tests: .\venv\Scripts\python.exe -m pytest" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue"