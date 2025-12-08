@echo off
REM Quick launcher for pyWATS Client
REM Double-click this file to run the GUI

cd /d "%~dp0.."
call .venv\Scripts\activate.bat
python -m pywats_client
