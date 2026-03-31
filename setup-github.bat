@echo off
REM GitHub Setup Script for Windows

echo =========================================
echo  GitHub Setup for Interviewer Agent
echo =========================================
echo.

REM Check if GitHub CLI is installed
where gh >nul 2>nul
if %errorlevel% neq 0 (
    echo GitHub CLI (gh) is not installed.
    echo.
    echo Please install GitHub CLI first:
    echo 1. Visit: https://cli.github.com/
    echo 2. Download and install
    echo 3. Restart this script
    echo.
    pause
    exit /b 1
)

echo Checking GitHub authentication...
gh auth status 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Not authenticated with GitHub.
    echo Starting authentication process...
    echo.
    gh auth login --hostname github.com
)

echo.
echo =========================================
echo  Creating GitHub Repository
echo =========================================
echo.

REM Ask for repository name
set /p REPO_NAME="Enter repository name (default: intervieweragent): "
if "%REPO_NAME%"=="" set REPO_NAME=intervieweragent

REM Ask for repository visibility
echo.
echo Repository visibility:
echo 1. public  (anyone can view, recommended for open source)
echo 2. private (only you can view)
echo.
set /p VISIBILITY="Choose (1=public, 2=private) [default: public]: "
if "%VISIBILITY%"=="2" (
    set VIS_ARG=--private
) else (
    set VIS_ARG=--public
)

echo.
echo Creating repository: %REPO_NAME% ...
gh repo create "%REPO_NAME%" %VIS_ARG% --source=. --remote=origin --push

if %errorlevel% equ 0 (
    echo.
    echo =========================================
    echo  Setup Complete!
    echo =========================================
    echo.
    echo Your repository is now live at:
    echo https://github.com/%USERNAME%/%REPO_NAME%
    echo.
    echo Next steps:
    echo 1. Visit the repository URL above
    echo 2. Add repository description and topics
    echo 3. Consider adding a LICENSE file
    echo.
) else (
    echo.
    echo Repository creation failed.
    echo It may already exist. Try connecting existing repo:
    echo.
    echo    git remote add origin https://github.com/%USERNAME%/%REPO_NAME%.git
    echo    git push -u origin main
    echo.
)

pause
