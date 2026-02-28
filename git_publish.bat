@echo off
:: Change directory to where the script is located
cd /d "%~dp0"

:: 1. Stage all changes
git add .

:: 2. Ask for a commit message
set /p commit_msg="Enter your commit message (or press Enter for 'Updates'): "

:: 3. Set a default if the user just hits Enter
if "%commit_msg%"=="" set commit_msg=Updates

:: 4. Commit and Push
git commit -m "%commit_msg%"
git push origin main

echo.
echo ------------------------------------------
echo Success! Changes are on their way to GitHub.
pause