@echo off
setlocal

REM Windows native build script
set SCRIPT_DIR=%~dp0
for %%I in ("%SCRIPT_DIR%..\..") do set PROJECT_ROOT=%%~fI

for /f "usebackq delims=" %%A in (`python -c "import os,sys; sys.path.insert(0, r'%PROJECT_ROOT%'); from config.settings import APP_NAME; print(APP_NAME)"`) do set APP_NAME=%%A

echo Building %APP_NAME% for Windows...
echo Project root: %PROJECT_ROOT%

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

if exist "%PROJECT_ROOT%\dist\windows\%APP_NAME%.exe" (
  echo Build completed successfully!
  echo Executable location: %PROJECT_ROOT%\dist\windows\%APP_NAME%.exe
) else (
  echo Build finished but .exe was not generated.
  exit /b 1
)

endlocal
