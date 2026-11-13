@echo off
REM ============================================================================
REM One-Click Helper to Push Project to GitHub
REM ============================================================================

echo ============================================================================
echo Pushing Customer Churn Prediction Project to GitHub (User: amokshagna)...
echo ============================================================================
echo.

set /p REPO_CHOICE="Do you want to push to existing repo 'BIA' or a new repo? (Enter 1 for 'BIA', 2 for new repo name) [Default: 1]: "
if "%REPO_CHOICE%"=="" set REPO_CHOICE=1

if "%REPO_CHOICE%"=="1" (
    set REMOTE_URL=https://github.com/amokshagna/BIA.git
    set TARGET_BRANCH=final-project
) else (
    set /p NEW_NAME="Enter your new GitHub repository name (e.g. BIAfinalproj): "
    set REMOTE_URL=https://github.com/amokshagna/%NEW_NAME%.git
    set TARGET_BRANCH=main
)

echo.
echo Target Remote: %REMOTE_URL%
echo Target Branch: %TARGET_BRANCH%
echo.

git remote remove origin >nul 2>&1
git remote add origin %REMOTE_URL%

echo Attempting push to %REMOTE_URL%...
echo (If prompted, enter your GitHub Username 'amokshagna' and a Personal Access Token as the password)
echo.

git push -u origin %TARGET_BRANCH%

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================================
    echo SUCCESS: Project pushed to GitHub successfully!
    echo ============================================================================
) else (
    echo.
    echo If authentication failed, please generate a Personal Access Token on GitHub:
    echo 1. Go to https://github.com/settings/tokens
    echo 2. Generate a new token with 'repo' scope
    echo 3. Use that token as your password when git asks.
)

pause
