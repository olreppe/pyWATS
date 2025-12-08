@echo off
REM Quick launcher for pyWATS Client (Development)
REM Double-click this file to run the client

cd /d "%~dp0.."
".venv\Scripts\python.exe" -m pywats_client
