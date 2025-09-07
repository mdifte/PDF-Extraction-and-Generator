# PDF Processor - Executable Builder

This directory contains scripts to build standalone executables for the PDF Processor application.

## 🚀 Quick Start

### For Windows Users:
1. **Double-click** `build_windows.bat`
2. Wait for the build to complete
3. Find your executable in `dist/PDF_Processor.exe`

### For macOS Users:
1. **Double-click** `build_macos.sh` (or run in Terminal)
2. Wait for the build to complete  
3. Find your app in `dist/PDF_Processor`

## 📋 What the Scripts Do

### Automatic Setup:
- ✅ Check Python installation
- ✅ Install PyInstaller if needed
- ✅ Install all required dependencies
- ✅ Clean previous builds
- ✅ Bundle all fonts, images, and docs
- ✅ Create standalone executable

### Included Files:
- **Fonts**: All TTF files for proper text rendering
- **Images**: Logo and signature files
- **Docs**: Second page template PDF
- **Dependencies**: All Python libraries bundled

## 🎯 Build Output

### Windows:
- **File**: `dist/PDF_Processor.exe`
- **Size**: ~50-70 MB
- **Requirements**: None (fully standalone)

### macOS:
- **File**: `dist/PDF_Processor`
- **Size**: ~50-70 MB  
- **Requirements**: None (fully standalone)

## 📁 Directory Structure After Build

```
dist/
├── PDF_Processor.exe (Windows)
├── PDF_Processor (macOS)
build/ (temporary build files)
*.spec (PyInstaller spec file)
```

## 🔧 Manual Build (Advanced)

If you prefer to run PyInstaller manually:

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name "PDF_Processor" \
  --add-data "fonts;fonts" \
  --add-data "images;images" \
  --add-data "docs;docs" \
  pdf_processor.py
```

## 🚨 Troubleshooting

### Build Fails:
1. Ensure Python 3.7+ is installed
2. Check internet connection for dependency downloads
3. Run as administrator (Windows) if permission errors
4. Clear build cache: delete `build/` and `dist/` folders

### Executable Won't Run:
1. Check antivirus software (may quarantine new executables)
2. Ensure all asset files are in the same directory
3. Check system compatibility (64-bit recommended)

### Missing Dependencies:
1. Update requirements.txt if you've added new packages
2. Re-run the build script
3. Check console output for missing modules

## 📦 Distribution

### For End Users:
- **Windows**: Distribute `PDF_Processor.exe` 
- **macOS**: Distribute `PDF_Processor` (or create .app bundle)
- **No Python required** on target machines
- **No installation needed** - just run the executable

### File Size Optimization:
- The executable includes the Python interpreter (~40MB)
- All dependencies and assets are bundled
- First run may be slower due to extraction

## 🔒 Security Notes

- Some antivirus software may flag PyInstaller executables
- This is a false positive common with packaged Python apps
- Consider code signing for production distribution
- Test on clean systems before distribution

## 📝 Version Info

- **Python**: 3.7+
- **PyInstaller**: Latest
- **Platform**: Windows 10+, macOS 10.14+
- **Architecture**: 64-bit recommended

## 🆘 Support

If you encounter issues:
1. Check the console output during build
2. Verify all files are present in the source directory
3. Ensure Python and pip are properly installed
4. Try rebuilding after clearing build cache

---

**Happy Building! 🎉**
