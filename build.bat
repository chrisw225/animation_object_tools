@echo off
echo Building Animation & Object Tools Extension...
echo.

REM Check if blender is available
blender --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Blender not found in PATH
    echo Please make sure Blender is installed and accessible from command line
    echo.
    echo You can also run manually:
    echo blender --command extension build
    pause
    exit /b 1
)

echo Found Blender, building extension...
echo.

REM Build the extension
blender --command extension build

if %errorlevel% equ 0 (
    echo.
    echo ✅ Extension built successfully!
    echo.
    echo 📤 Next steps:
    echo 1. Test the extension in Blender
    echo 2. Upload to https://extensions.blender.org/submit/
    echo 3. Wait for review and approval
) else (
    echo.
    echo ❌ Build failed!
    echo Check the error messages above.
)

pause 