:: 1. Define the paths (relative to the script location)
set RAW_DIR=gitignore\_raw_photos
set ARCHIVE_DIR=gitignore\archive
set POSTS_DIR=assets\images\posts

:: 2. Check if the folders exist, create them if they don't
if not exist "%ARCHIVE_DIR%" mkdir "%ARCHIVE_DIR%"
if not exist "%POSTS_DIR%" mkdir "%POSTS_DIR%"

:: 3. Check if there are any images to process
dir /b /a-d "%RAW_DIR%\*.jpg" "%RAW_DIR%\*.jpeg" "%RAW_DIR%\*.png" "%RAW_DIR%\*.JPG" "%RAW_DIR%\*.HEIC" >nul 2>&1
if %errorlevel% neq 0 (
    echo No new photos found in %RAW_DIR%. Skipping optimization.
    pause
    exit /b
)

echo Processing new photos...

:: 4. Convert, resize, and save to the posts folder
:: We use 'magick' for v7+ or 'mogrify' for older versions. 
magick mogrify -path "%POSTS_DIR%" -resize "1200x>" -quality 80 -format webp "%RAW_DIR%\*.*"

:: 5. Move the originals to the archive
echo Archiving originals...
move "%RAW_DIR%\*.jpg" "%ARCHIVE_DIR%\" >nul 2>&1
move "%RAW_DIR%\*.jpeg" "%ARCHIVE_DIR%\" >nul 2>&1
move "%RAW_DIR%\*.png" "%ARCHIVE_DIR%\" >nul 2>&1
move "%RAW_DIR%\*.JPG" "%ARCHIVE_DIR%\" >nul 2>&1
move "%RAW_DIR%\*.HEIC" "%ARCHIVE_DIR%\" >nul 2>&1

echo Done! Photos optimized in %POSTS_DIR% and archived in %ARCHIVE_DIR%.
pause