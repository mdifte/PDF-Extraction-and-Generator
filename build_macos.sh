#!/bin/bash

echo "========================================"
echo "PDF Processor macOS App Builder"
echo "========================================"
echo

# Set macOS deployment target for broader compatibility
# This ensures the app will run on macOS Catalina (10.15) and newer
export MACOSX_DEPLOYMENT_TARGET=10.15
echo "🎯 Setting deployment target to macOS ${MACOSX_DEPLOYMENT_TARGET} (Catalina) for broader compatibility"

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

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -f *.spec

print_status "Cleaned previous builds"

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
echo "🔧 Build configuration:"
echo "   Deployment target: ${MACOSX_DEPLOYMENT_TARGET}"
echo "   Python version: $(python3 --version)"
echo "   PyInstaller version: $(python3 -m PyInstaller --version)"
echo

# Set macOS deployment target for Catalina compatibility
export MACOSX_DEPLOYMENT_TARGET=10.15
echo "Setting macOS deployment target to: $MACOSX_DEPLOYMENT_TARGET"

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
    --hidden-import "docx" \
    --hidden-import "lxml" \
    --hidden-import "lxml.etree" \
    --hidden-import "lxml.html" \
    --hidden-import "lxml._elementpath" \
    --hidden-import "lxml.cssselect" \
    --hidden-import "concurrent.futures" \
    --collect-all "reportlab" \
    --collect-all "fitz" \
    --collect-all "docx" \
    --collect-all "lxml" \
    --osx-bundle-identifier "com.pdfprocessor.app" \
    --target-architecture universal2 \
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

# Update Info.plist with proper compatibility settings
echo "🔧 Updating Info.plist for macOS compatibility..."
if [ -f "App-Info.plist" ] && [ -d "dist/PDF Processor.app/Contents" ]; then
    cp "App-Info.plist" "dist/PDF Processor.app/Contents/Info.plist"
    print_status "Info.plist updated with Catalina compatibility"
else
    print_warning "App-Info.plist not found or app bundle incomplete"
fi

# Set proper permissions for the executable
echo "Setting executable permissions..."
chmod 755 "dist/PDF Processor.app/Contents/MacOS/PDF Processor"
if [ $? -eq 0 ]; then
    print_status "Executable permissions set to 755"
else
    print_error "Failed to set executable permissions"
fi

# Create distribution archive with ditto to preserve permissions
echo "Creating distribution archive with ditto..."
ditto -c -k --sequesterRsrc --keepParent "dist/PDF Processor.app" "PDF-Processor-macOS-App.zip"
if [ $? -eq 0 ]; then
    print_status "Distribution archive created: PDF-Processor-macOS-App.zip"
    echo "Archive size: $(du -sh 'PDF-Processor-macOS-App.zip' | cut -f1)"
else
    print_error "Failed to create distribution archive"
fi

echo
echo "You can now:"
echo "1. Run the app by double-clicking: dist/PDF Processor.app"
echo "2. Copy the app to /Applications/ for system-wide access"
echo "3. Create an alias on your desktop"
echo "4. Distribute the zip file: PDF-Processor-macOS-App.zip"
echo
echo "📋 Compatibility Information:"
echo "   Minimum macOS version: 10.15 (Catalina)"
echo "   Architecture: Universal binary (Intel + Apple Silicon)"
echo "   Works on: Intel Macs and Apple Silicon Macs"
echo
echo "To install system-wide (optional):"
echo "  cp -r 'dist/PDF Processor.app' /Applications/"
echo

echo
print_status "Build completed successfully for GitHub Actions!"

# Make the script executable for future runs
chmod +x "$0"
