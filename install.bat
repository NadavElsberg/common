@echo off
REM clone_and_install_common.bat
REM Usage: clone_and_install_common.bat [target_dir] [python_exe] [mode]
REM  - target_dir: where to clone (default: %USERPROFILE%\common)
REM  - python_exe: optional full path to python.exe (default: first python in PATH or 'py -3')
REM  - mode: "system" to install into given python, or omit to create a venv and install there

SETLOCAL ENABLEDELAYEDEXPANSION

SET "REPO_URL=https://github.com/NadavElsbreg/common.git"
SET "TARGET=%~1"
IF "%TARGET%"=="" SET "TARGET=%USERPROFILE%\common"

SET "PYTHON_EXE=%~2"
SET "MODE=%~3"

echo Target directory: "%TARGET%"
echo Install mode: %MODE%

REM Check for git
where git >nul 2>nul
IF ERRORLEVEL 1 (
  echo ERROR: 'git' not found in PATH. Install Git and re-run.
  exit /b 1
)

REM Resolve python if not provided
IF "%PYTHON_EXE%"=="" (
  for /f "delims=" %%P in ('where python 2^>nul') do (
    if not defined PYTHON_EXE set "PYTHON_EXE=%%P"
  )
  if not defined PYTHON_EXE (
    REM Fallback to 'py -3' launcher
    where py >nul 2>nul
    IF ERRORLEVEL 0 (
      set "PYTHON_EXE=py -3"
    ) ELSE (
      echo ERROR: No python found in PATH and no 'py' launcher. Please install Python.
      exit /b 1
    )
  )
)

echo Using Python: %PYTHON_EXE%

REM Clone or update
IF EXIST "%TARGET%\.git" (
  echo Directory exists and looks like a git repo, pulling latest...
  git -C "%TARGET%" pull || (
    echo Pull failed. You can remove "%TARGET%" and re-run to clone fresh.
    exit /b 1
  )
) ELSE (
  echo Cloning repository...
  git clone "%REPO_URL%" "%TARGET%" || (
    echo Git clone failed.
    exit /b 1
  )
)

REM If mode == system, use provided python to install editable directly
IF /I "%MODE%"=="system" (
  echo Installing package in editable mode into system python...
  %PYTHON_EXE% -m pip install --upgrade pip setuptools wheel
  %PYTHON_EXE% -m pip install -e "%TARGET%" || (
    echo Pip install failed.
    exit /b 1
  )
  echo Done. Package installed into %PYTHON_EXE%.
  exit /b 0
)

REM Default: create venv inside target and install there
echo Creating venv in "%TARGET%\venv" ...
%PYTHON_EXE% -m venv "%TARGET%\venv" || (
  echo Failed to create venv with %PYTHON_EXE%
  exit /b 1
)

SET "VENV_PY=%TARGET%\venv\Scripts\python.exe"
IF NOT EXIST "%VENV_PY%" (
  echo ERROR: venv python not found at "%VENV_PY%".
  exit /b 1
)

echo Upgrading pip in venv...
"%VENV_PY%" -m pip install --upgrade pip setuptools wheel

echo Installing package in editable mode into venv...
"%VENV_PY%" -m pip install -e "%TARGET%" || (
  echo Pip install failed inside venv.
  exit /b 1
)

echo SUCCESS: Repository cloned to "%TARGET%" and installed (editable) in "%TARGET%\venv".
echo To use it, activate the venv:
echo    "%TARGET%\venv\Scripts\activate.bat"
ENDLOCAL
exit /b 0