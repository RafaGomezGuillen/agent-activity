@echo off
setlocal EnableDelayedExpansion

REM ===============================
REM Resolve script directory
REM ===============================
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM ===============================
REM Project root (two levels up)
REM ===============================
cd /d "%SCRIPT_DIR%\..\.."
set "PROJECT_ROOT=%cd%"

REM ===============================
REM Get APP_NAME via Python (-c!)
REM ===============================
for /f "usebackq delims=" %%A in (`
    python -c "import sys, os; sys.path.insert(0, r'%PROJECT_ROOT%'); from config.settings import APP_NAME; print(APP_NAME)"
`) do set "APP_NAME=%%A"

echo Uninstalling %APP_NAME%...

REM ===============================
REM Kill running process (ignore errors)
REM ===============================
echo Stopping running processes...
taskkill /F /IM "%APP_NAME%.exe" >nul 2>&1

REM ===============================
REM Remove build artifacts
REM ===============================
echo Removing build artifacts...
if exist "%PROJECT_ROOT%\build\windows" rmdir /s /q "%PROJECT_ROOT%\build\windows"
if exist "%PROJECT_ROOT%\dist\windows"  rmdir /s /q "%PROJECT_ROOT%\dist\windows"

REM ===============================
REM Remove %APPDATA%\APP_NAME
REM ===============================
echo Removing app data...
powershell -NoProfile -Command ^
  "$p = Join-Path $env:APPDATA '%APP_NAME%'; if (Test-Path $p) { Remove-Item -LiteralPath $p -Recurse -Force }" ^
  >nul 2>&1

echo Uninstallation completed successfully!
endlocal
