@echo off
REM ============================================================================
REM  SysGuard - One-Click Launcher for Windows
REM
REM  WHAT THIS DOES (the short version):
REM    Double-click this file and SysGuard just starts up. You do not need to
REM    know anything about Python or command lines. On its own this script:
REM      1. Checks that Python is installed, and if not, tells you where to
REM         get it (python.org) and stops.
REM      2. Creates a private "virtual environment" folder (.venv) the first
REM         time you run it, so SysGuard's files never touch the rest of your
REM         computer.
REM      3. Installs the libraries SysGuard needs, but SKIPS this step on
REM         later runs unless requirements.txt has actually changed. This
REM         keeps startup fast.
REM      4. Starts the live system monitor.
REM
REM  To close the monitor, press Ctrl+C in this black window.
REM ============================================================================

setlocal
cd /d "%~dp0"

set "VENV=%~dp0.venv"
set "REQS=%~dp0requirements.txt"
set "HASHFILE=%VENV%\requirements.hash"
set "PYEXE="

echo.
echo  ==============================================
echo    SysGuard - System Health Monitor
echo  ==============================================
echo.

REM --- Step 1: is Python installed? -----------------------------------------
echo [1/4] Checking for Python...

where py >nul 2>nul
if not errorlevel 1 set "PYEXE=py -3"

if not defined PYEXE (
    where python >nul 2>nul
    if not errorlevel 1 set "PYEXE=python"
)

if not defined PYEXE goto :nopython

%PYEXE% -c "import sys" >nul 2>nul
if errorlevel 1 goto :nopython

for /f "tokens=*" %%V in ('%PYEXE% -c "import sys;print(sys.version.split()[0])" 2^>nul') do set "PYVER=%%V"
echo       Python found ^(version %PYVER%^).
echo.

REM --- Step 2: create the virtual environment if needed ---------------------
echo [2/4] Preparing private environment folder...

if exist "%VENV%\Scripts\python.exe" (
    echo       Already set up - skipping.
) else (
    echo       Creating .venv folder, please wait...
    %PYEXE% -m venv "%VENV%"
    if errorlevel 1 goto :venvfail
    echo       Done.
)
echo.

REM --- Step 3: install libraries, but only when they are out of date ---------
echo [3/4] Checking required libraries...

set "REQHASH="
if exist "%REQS%" (
    for /f "tokens=* delims= " %%H in ('certutil -hashfile "%REQS%" MD5 ^| findstr /r /v ":"') do set "REQHASH=%%H"
)

REM NOTE: these three lines are deliberately NOT inside a ( ) block. Inside a
REM block, %VAR% is expanded when the block is parsed, before the "set /p" has
REM actually run, so the comparison would always read an empty value and
REM reinstall the libraries on every single launch.
set "OLDHASH="
if exist "%HASHFILE%" set /p OLDHASH=<"%HASHFILE%"

set "NEEDINSTALL=1"
if not "%REQHASH%"=="" if "%OLDHASH%"=="%REQHASH%" set "NEEDINSTALL=0"

if "%NEEDINSTALL%"=="1" (
    echo       Installing libraries for the first time or after an update...
    "%VENV%\Scripts\python.exe" -m pip install --upgrade pip --quiet
    "%VENV%\Scripts\python.exe" -m pip install -r "%REQS%"
    if errorlevel 1 goto :pipfail
    >"%HASHFILE%" echo %REQHASH%
    echo       Libraries installed.
) else (
    echo       Libraries already up to date - skipping ^(faster startup^).
)
echo.

REM --- Step 4: start the monitor --------------------------------------------
echo [4/4] Starting SysGuard...
echo.
echo  Press Ctrl+C in this window to stop the monitor.
echo.

"%VENV%\Scripts\python.exe" "%~dp0monitor.py"
if errorlevel 1 goto :runfail

echo.
echo  SysGuard stopped.
goto :done

REM --- error handlers -------------------------------------------------------
:nopython
echo.
echo  ==============================================================
echo   Python is not installed on this computer.
echo  ==============================================================
echo.
echo   SysGuard needs Python to run. It is free and takes about
echo   5 minutes to install:
echo.
echo       1. Go to https://www.python.org/downloads/
echo       2. Click the big yellow "Download Python" button
echo       3. Run the installer and IMPORTANTLY tick the box
echo          that says "Add python.exe to PATH"
echo       4. Install, then double-click this file again
echo.
pause
exit /b 1

:venvfail
echo.
echo   ERROR: Could not create the .venv folder.
echo   This is usually an antivirus or folder-permission problem.
echo.
pause
exit /b 1

:pipfail
echo.
echo   ERROR: Could not install the required libraries.
echo   Check your internet connection and try again.
echo.
pause
exit /b 1

:runfail
echo.
echo   ERROR: The monitor stopped unexpectedly.
echo   The message above should say why.
echo.
pause
exit /b 1

:done
endlocal
exit /b 0