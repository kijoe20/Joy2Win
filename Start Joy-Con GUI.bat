@echo off
title Joy-Con 2 Windows - GUI Launcher
echo.
echo 🎮 Joy-Con 2 Windows - Starting GUI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Python is not installed or not in PATH.
        echo Please install Python from https://python.org
        echo.
        pause
        exit /b 1
    ) else (
        echo Using python3...
        python3 start_gui.py
        goto end
    )
) else (
    python start_gui.py
)

:end

REM If we get here, the GUI has closed
echo.
echo GUI closed.
pause