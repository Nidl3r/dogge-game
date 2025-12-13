@echo off
REM Schnauzer Desktop Pet Launcher
REM Uses virtual environment if available, falls back to system Python

REM Check if venv exists and use it
if exist "%~dp0venv\Scripts\pythonw.exe" (
    start "" "%~dp0venv\Scripts\pythonw.exe" launcher_gui.py
) else if exist "%~dp0venv\Scripts\python.exe" (
    "%~dp0venv\Scripts\python.exe" launcher_gui.py
) else (
    REM Fall back to system Python
    where pythonw >nul 2>&1
    if %errorlevel% equ 0 (
        start "" pythonw launcher_gui.py
    ) else (
        python launcher_gui.py
    )
)
