@echo off
setlocal enabledelayedexpansion

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH
    exit /b 1
)

echo Creating Python virtual environment...
python -m venv .venv
if %ERRORLEVEL% neq 0 (
    echo Failed to create virtual environment
    exit /b 1
)
echo.

echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %ERRORLEVEL% neq 0 (
    echo Failed to activate virtual environment
    exit /b 1
)
echo.

echo Creating initial requirements.txt...
echo # Python dependencies > requirements.txt
echo # Add your dependencies here >> requirements.txt
echo.

echo Done! Virtual environment is ready.
echo To activate the environment: .venv\Scripts\activate
echo To deactivate: deactivate

endlocal
