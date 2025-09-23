@echo off
REM pyWATS Development Environment Setup Script
REM This script sets up the development environment for pyWATS

echo [SETUP] Setting up pyWATS development environment...
echo =====================================

REM Check if virtual environment exists
if not exist "venv\" (
    echo [CREATE] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created!
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo [INSTALL] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [SUCCESS] Dependencies installed!

REM Test the installation
echo [TEST] Testing installation...
python -c "import sys; sys.path.insert(0, 'src'); from pyWATS.connection import create_connection; print('[SUCCESS] pyWATS is ready!')"

if errorlevel 1 (
    echo [ERROR] Installation test failed
    pause
    exit /b 1
)

echo.
echo [COMPLETE] Setup complete!
echo =====================================
echo To activate the environment, run: venv\Scripts\activate.bat
echo To run the example: python main.py
echo To run tests: pytest
echo.
pause