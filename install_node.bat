@echo off
setlocal enabledelayedexpansion

echo Checking for Node.js installation...
where node >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Node.js is not installed. Installing via winget...
    winget install OpenJS.NodeJS
    if %ERRORLEVEL% neq 0 (
        echo Failed to install Node.js
        exit /b 1
    )
    echo Please restart your terminal after installation
    echo Then run: npm --version
    pause
    exit /b 0
)

echo Node.js is installed
node --version
npm --version

endlocal
