@echo off
setlocal EnableDelayedExpansion

:: Set the project repository URL and branch
set REPO_URL=https://github.com/Auto-HQ-Test/AUTO_HQ_TEST_FINAL
set BRANCH=main
set INSTALL_DIR=%USERPROFILE%\auto_hqtest
set PYTHON_VERSION=3.11.0
set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe

:: Check Git 
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Git is not installed. Downloading Git...
    curl -L -o git-installer.exe https://github.com/git-for-windows/git/releases/download/v2.41.0.windows.1/Git-2.41.0-64-bit.exe
    start /wait git-installer.exe /VERYSILENT /NORESTART
    del git-installer.exe
)

:: Create and navigate to installation directory
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
cd /d "%INSTALL_DIR%"

:: Clone/Update repository
if exist .git (
    echo Updating repository...
    git pull origin %BRANCH%
) else (
    echo Cloning repository...
    git clone -b %BRANCH% %REPO_URL% .
)

:: Check Python Installation
python --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Downloading Python %PYTHON_VERSION%...
    curl -L -o %PYTHON_INSTALLER% https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe
    echo Installing Python...
    start /wait %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1
    del %PYTHON_INSTALLER%
    
    :: Refresh environment variables
    call refreshenv.cmd
    if %ERRORLEVEL% NEQ 0 (
        echo Please restart your computer to complete Python installation
        pause
        exit
    )
)

:: Create virtual environment if it doesn't exist
if not exist "autohqtest_venv" (
    echo Creating virtual environment...
    python -m venv autohqtest_venv
)

:: Activate virtual environment and install requirements
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

:: Move over to the installation directory then run the application
cd %INSTALL_DIR%
python gui_runner.py

:: Deactivate virtual environment before exit
call venv\Scripts\deactivate.bat

endlocal
pause