@echo off
echo ========================================
echo PDF Processor - Windows Executable Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if PyInstaller is installed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo ✓ PyInstaller ready
echo.

REM Install required packages
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install required packages
    echo Make sure requirements.txt exists and is valid
    pause
    exit /b 1
)

echo ✓ Dependencies installed
echo.

REM Fix pathlib compatibility issue with PyInstaller
echo Checking for pathlib compatibility issues...
pip show pathlib >nul 2>&1
if not errorlevel 1 (
    echo Found incompatible pathlib package. Removing it...
    pip uninstall pathlib -y
    if errorlevel 1 (
        echo WARNING: Could not uninstall pathlib automatically
        echo Please run: pip uninstall pathlib
        echo Then re-run this build script
        pause
        exit /b 1
    )
    echo ✓ pathlib compatibility issue resolved
) else (
    echo ✓ No pathlib compatibility issues found
)
echo.

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del /q "*.spec"

echo ✓ Cleaned previous builds
echo.

REM Create the executable with PyInstaller
echo Building PDF Processor executable...
echo This may take several minutes...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "PDF_Processor" ^
    --icon "document_generator_icon.icns" ^
    --add-data "fonts;fonts" ^
    --add-data "images;images" ^
    --add-data "docs;docs" ^
    --hidden-import "PIL._tkinter_finder" ^
    --hidden-import "tkinter" ^
    --hidden-import "tkinter.ttk" ^
    --hidden-import "tkinter.filedialog" ^
    --hidden-import "reportlab.pdfgen.canvas" ^
    --hidden-import "reportlab.lib.pagesizes" ^
    --hidden-import "reportlab.pdfbase.pdfmetrics" ^
    --hidden-import "reportlab.pdfbase.ttfonts" ^
    --hidden-import "reportlab.lib.utils" ^
    --hidden-import "fitz" ^
    --hidden-import "PyPDF2" ^
    --hidden-import "concurrent.futures" ^
    --collect-all "reportlab" ^
    --collect-all "fitz" ^
    pdf_processor.py

if errorlevel 1 (
    echo.
    echo ❌ BUILD FAILED!
    echo Check the error messages above for details.
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ BUILD SUCCESSFUL!
echo ========================================
echo.
echo Your executable is ready:
echo Location: dist\PDF_Processor.exe
echo.
echo You can now:
echo 1. Run the executable directly from dist\PDF_Processor.exe
echo 2. Copy the executable to any Windows computer (no Python required!)
echo 3. Create a desktop shortcut for easy access
echo.
echo Note: The first run may be slower as Windows scans the new executable.
echo.

REM Ask if user wants to run the executable
set /p choice="Do you want to run the executable now? (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo Starting PDF Processor...
    start "" "dist\PDF_Processor.exe"
)

echo.
echo Build completed successfully!
pause
