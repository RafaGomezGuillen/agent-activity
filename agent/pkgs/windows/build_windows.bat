@echo off
setlocal

REM Windows native build script
set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%..\..") do set PROJECT_ROOT=%%~fI
set APP_VERSION=%APP_VERSION%
if "%APP_VERSION%"=="" set APP_VERSION=1.0.0

for /f "usebackq delims=" %%A in (`python -c "import os,sys; sys.path.insert(0, r'%PROJECT_ROOT%'); from config.settings import APP_NAME; print(APP_NAME)"`) do set APP_NAME=%%A

echo Building %APP_NAME% for Windows...
echo Project root: %PROJECT_ROOT%
echo App version: %APP_VERSION%

echo Cleaning old build artifacts...
if exist "%PROJECT_ROOT%\build\windows" rmdir /S /Q "%PROJECT_ROOT%\build\windows"
if exist "%PROJECT_ROOT%\dist\windows" rmdir /S /Q "%PROJECT_ROOT%\dist\windows"
mkdir "%PROJECT_ROOT%\build\windows"
mkdir "%PROJECT_ROOT%\dist\windows"

echo Running PyInstaller...
pushd "%PROJECT_ROOT%"
python -m PyInstaller "%SCRIPT_DIR%build_windows.spec" --distpath "%PROJECT_ROOT%\dist\windows" --workpath "%PROJECT_ROOT%\build\windows" --noconfirm
if errorlevel 1 (
  echo Build failed!
  popd
  exit /b 1
)
popd

set BUILD_MODE=
set DIST_EXE=%PROJECT_ROOT%\dist\windows\%APP_NAME%.exe
set DIST_DIR=%PROJECT_ROOT%\dist\windows\%APP_NAME%

if exist "%DIST_EXE%" (
  set BUILD_MODE=onefile
  echo Build completed successfully!
  echo Executable location: %DIST_EXE%
) else if exist "%DIST_DIR%" (
  set BUILD_MODE=onedir
  echo Build completed successfully!
  echo App directory: %DIST_DIR%
) else (
  echo Build finished but no Windows artifact was generated.
  exit /b 1
)

endlocal
