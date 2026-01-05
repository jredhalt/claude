@echo off
REM Skateskins Ad Generator - Start Script for Windows

echo ================================================
echo    Skateskins Video ^& Ad Generator
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Check if FFmpeg is installed
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo WARNING: FFmpeg is not installed
    echo Video generation will not work without FFmpeg
    echo Download from: https://ffmpeg.org/download.html
    echo.
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist "venv\.dependencies_installed" (
    echo Installing dependencies...
    pip install -r requirements.txt
    type nul > venv\.dependencies_installed
) else (
    echo Dependencies already installed
)

REM Create necessary directories
if not exist "uploads\broll" mkdir uploads\broll
if not exist "uploads\photos" mkdir uploads\photos
if not exist "uploads\inspiration" mkdir uploads\inspiration
if not exist "output\videos" mkdir output\videos
if not exist "output\static_ads" mkdir output\static_ads

echo.
echo ================================================
echo Starting Skateskins Ad Generator...
echo ================================================
echo.
echo Web Interface: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ================================================
echo.

REM Start the server
cd backend
python app.py
