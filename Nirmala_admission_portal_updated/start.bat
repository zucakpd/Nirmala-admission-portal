@echo off
REM Nirmala Admission Portal - Quick Start Script for Windows

echo ========================================
echo   NIRMALA ADMISSION PORTAL
echo   Quick Start Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

echo √ Python found
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo   Starting the server...
echo ========================================
echo.
echo The portal will be available at:
echo   http://localhost:5000
echo.
echo Default Login Credentials:
echo   Username: admin
echo   Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
pause
