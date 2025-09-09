#!/bin/bash

echo "========================================"
echo "PDF Processor macOS App Builder (Universal)"
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

# Set deployment target for macOS Catalina compatibility
export MACOSX_DEPLOYMENT_TARGET="10.15"
echo "Setting deployment target: $MACOSX_DEPLOYMENT_TARGET"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script must be run on macOS to build universal binaries"
    exit 1
fi

print_status "Running on macOS $(sw_vers -productVersion)"

# Check system architecture
SYSTEM_ARCH=$(uname -m)
echo "System architecture: $SYSTEM_ARCH"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed or not in PATH"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

print_status "Python 3 found: $(python3 --version)"

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

print_status "PyInstaller ready: $(pyinstaller --version)"

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

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -f *.spec

print_status "Cleaned previous builds"

# Determine the correct icon file
ICON_FILE=""
if [ -f "document_generator_icon.icns" ]; then
    ICON_FILE="document_generator_icon.icns"
elif [ -f "images/app_icon.icns" ]; then
    ICON_FILE="images/app_icon.icns"
elif [ -f "app_icon.icns" ]; then
    ICON_FILE="app_icon.icns"
else
    print_warning "No .icns icon file found, building without icon"
fi

# Check if main Python file exists
MAIN_FILE=""
if [ -f "pdf_processor.py" ]; then
    MAIN_FILE="pdf_processor.py"
elif [ -f "main.py" ]; then
    MAIN_FILE="main.py"
else
    print_error "Main Python file not found (pdf_processor.py or main.py)"
    exit 1
fi

print_status "Main file: $MAIN_FILE"
if [ -n "$ICON_FILE" ]; then
    print_status "Icon file: $ICON_FILE"
fi

# Build the universal app bundle with PyInstaller
echo
echo "Building Universal PDF Processor app (Intel + Apple Silicon)..."
echo "This may take several minutes..."
echo "Target architecture: universal2"
echo "Deployment target: $MACOSX_DEPLOYMENT_TARGET"
echo

# Build command with universal2 target
BUILD_CMD="python3 -m PyInstaller \
    --onedir \
    --windowed \
    --name 'PDF Processor' \
    --target-arch universal2 \
    --osx-bundle-identifier 'com.pdfprocessor.app'"

# Add icon if available
if [ -n "$ICON_FILE" ]; then
    BUILD_CMD="$BUILD_CMD --icon '$ICON_FILE'"
fi

# Add data directories if they exist
if [ -d "fonts" ]; then
    BUILD_CMD="$BUILD_CMD --add-data 'fonts:fonts'"
    print_status "Including fonts directory"
fi

if [ -d "images" ]; then
    BUILD_CMD="$BUILD_CMD --add-data 'images:images'"
    print_status "Including images directory"
fi

if [ -d "docs" ]; then
    BUILD_CMD="$BUILD_CMD --add-data 'docs:docs'"
    print_status "Including docs directory"
fi

# Add hidden imports and collections
BUILD_CMD="$BUILD_CMD \
    --hidden-import 'PIL._tkinter_finder' \
    --hidden-import 'tkinter' \
    --hidden-import 'tkinter.ttk' \
    --hidden-import 'tkinter.filedialog' \
    --hidden-import 'tkinter.messagebox' \
    --hidden-import 'reportlab.pdfgen.canvas' \
    --hidden-import 'reportlab.lib.pagesizes' \
    --hidden-import 'reportlab.pdfbase.pdfmetrics' \
    --hidden-import 'reportlab.pdfbase.ttfonts' \
    --hidden-import 'reportlab.lib.utils' \
    --hidden-import 'fitz' \
    --hidden-import 'PyPDF2' \
    --hidden-import 'docx' \
    --hidden-import 'lxml' \
    --hidden-import 'lxml.etree' \
    --hidden-import 'lxml.html' \
    --hidden-import 'lxml._elementpath' \
    --hidden-import 'lxml.cssselect' \
    --hidden-import 'concurrent.futures' \
    --collect-all 'reportlab' \
    --collect-all 'fitz' \
    --collect-all 'docx' \
    --collect-all 'lxml' \
    $MAIN_FILE"

# Execute the build command
eval $BUILD_CMD

if [ $? -ne 0 ]; then
    echo
    print_error "BUILD FAILED!"
    echo "Check the error messages above for details."
    exit 1
fi

# Verify the build and check architecture
echo
echo "Verifying build..."
APP_PATH="dist/PDF Processor.app"
EXECUTABLE_PATH="$APP_PATH/Contents/MacOS/PDF Processor"

if [ -d "$APP_PATH" ]; then
    print_status "App bundle created successfully"
    
    # Check file size
    APP_SIZE=$(du -sh "$APP_PATH" | cut -f1)
    echo "App bundle size: $APP_SIZE"
    
    # Verify executable exists
    if [ -f "$EXECUTABLE_PATH" ]; then
        print_status "Executable found"
        
        # Check architecture
        echo
        echo "Architecture verification:"
        file "$EXECUTABLE_PATH"
        
        # Check if it's universal
        if lipo -info "$EXECUTABLE_PATH" 2>/dev/null | grep -q "are:"; then
            print_status "Universal binary created successfully!"
            lipo -info "$EXECUTABLE_PATH"
        else
            print_warning "Single architecture binary (this is normal on some systems)"
            lipo -info "$EXECUTABLE_PATH" 2>/dev/null || echo "Architecture: $(file "$EXECUTABLE_PATH" | cut -d: -f2)"
        fi
        
        # Check deployment target
        echo
        echo "Deployment target verification:"
        otool -l "$EXECUTABLE_PATH" | grep -A 3 LC_VERSION_MIN_MACOSX || echo "No deployment target info found"
        
    else
        print_error "Executable not found in app bundle"
        exit 1
    fi
else
    print_error "App bundle not created"
    exit 1
fi

echo
echo "========================================"
print_status "BUILD SUCCESSFUL!"
echo "========================================"
echo
echo "Your Universal macOS app bundle is ready:"
echo "Location: dist/PDF Processor.app"
echo "Target: macOS 10.15+ (Catalina and newer)"
echo "Architecture: Universal (Intel + Apple Silicon)"
echo
echo "You can now:"
echo "1. Run the app by double-clicking: dist/PDF Processor.app"
echo "2. Copy the app to /Applications/ for system-wide access"
echo "3. Create an alias on your desktop"
echo
echo "To install system-wide (optional):"
echo "  cp -r 'dist/PDF Processor.app' /Applications/"
echo
echo "To test compatibility:"
echo "  lipo -info 'dist/PDF Processor.app/Contents/MacOS/PDF Processor'"
echo

print_status "Universal build completed successfully!"

# Make the script executable for future runs
chmod +x "$0"