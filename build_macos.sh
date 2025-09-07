#!/bin/bash

echo "========================================"
echo "PDF Processor - macOS App Builder"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

print_status "Python 3 found"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not available"
    echo "Please install pip3"
    exit 1
fi

print_status "pip3 ready"

# Check if PyInstaller is installed
if ! pip3 show pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        print_error "Failed to install PyInstaller"
        exit 1
    fi
fi

print_status "PyInstaller ready"

# Install required packages
echo "Installing required packages..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Failed to install required packages"
        echo "Check requirements.txt for issues"
        exit 1
    fi
else
    print_warning "requirements.txt not found, installing basic packages..."
    pip3 install PyMuPDF reportlab PyPDF2 Pillow
fi

print_status "Dependencies installed"

# Fix pathlib compatibility issue with PyInstaller
echo "Checking for pathlib compatibility issues..."
if pip3 show pathlib &> /dev/null; then
    echo "Found incompatible pathlib package. Removing it..."
    pip3 uninstall pathlib -y
    if [ $? -ne 0 ]; then
        print_error "Could not uninstall pathlib automatically"
        echo "Please run: pip3 uninstall pathlib"
        echo "Then re-run this build script"
        exit 1
    fi
    print_status "pathlib compatibility issue resolved"
else
    print_status "No pathlib compatibility issues found"
fi
echo

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -f *.spec

print_status "Cleaned previous builds"

# Create the app bundle with PyInstaller
echo "Building PDF Processor app..."
echo "This may take several minutes..."
echo

python3 -m PyInstaller \
    --onedir \
    --windowed \
    --name "PDF Processor" \
    --icon "document_generator_icon.icns" \
    --add-data "fonts:fonts" \
    --add-data "images:images" \
    --add-data "docs:docs" \
    --hidden-import "PIL._tkinter_finder" \
    --hidden-import "tkinter" \
    --hidden-import "tkinter.ttk" \
    --hidden-import "tkinter.filedialog" \
    --hidden-import "reportlab.pdfgen.canvas" \
    --hidden-import "reportlab.lib.pagesizes" \
    --hidden-import "reportlab.pdfbase.pdfmetrics" \
    --hidden-import "reportlab.pdfbase.ttfonts" \
    --hidden-import "reportlab.lib.utils" \
    --hidden-import "fitz" \
    --hidden-import "PyPDF2" \
    --hidden-import "concurrent.futures" \
    --collect-all "reportlab" \
    --collect-all "fitz" \
    pdf_processor.py

if [ $? -ne 0 ]; then
    echo
    print_error "BUILD FAILED!"
    echo "Check the error messages above for details."
    exit 1
fi

echo
echo "========================================"
print_status "BUILD SUCCESSFUL!"
echo "========================================"
echo
echo "Your macOS app bundle is ready:"
echo "Location: dist/PDF Processor.app"
echo
echo "You can now:"
echo "1. Run the app by double-clicking: dist/PDF Processor.app"
echo "2. Copy the app to /Applications/ for system-wide access"
echo "3. Create an alias on your desktop"
echo
echo "To install system-wide (optional):"
echo "  cp -r 'dist/PDF Processor.app' /Applications/"
echo

# Check if running in CI environment
if [ "$CI" = "true" ]; then
    echo "Running in CI environment - skipping interactive prompts"
    echo
    print_status "Build completed successfully!"
    # Make the script executable for future runs
    chmod +x "$0"
    exit 0
fi

# Ask if user wants to run the app
read -p "Do you want to run the app now? (y/n): " choice
case "$choice" in 
    y|Y ) 
        echo
        echo "Starting PDF Processor..."
        open "dist/PDF Processor.app" &
        ;;
    * ) 
        echo "You can run it later by double-clicking: dist/PDF Processor.app"
        ;;
esac

echo
print_status "Build completed successfully!"

# Make the script executable for future runs
chmod +x "$0"
