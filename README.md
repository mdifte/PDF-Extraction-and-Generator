# PDF Processor

## Overview

The **PDF Processor** is a Python-based application customized for **Mike Wilen Real Estate**, **270 Hennepin Ave #1111, Minneapolis, MN 55401**, that extracts data from PDF files and generates formatted PDF documents. It provides a GUI interface for selecting and processing multiple PDFs in batch mode.


## Features

- Extracts structured data from PDFs using `PyMuPDF` (`fitz`).
- Generates formatted PDF documents using `ReportLab` and `PyPDF2`.
- Merges generated PDFs with an existing template.
- Provides a GUI for user-friendly interaction using `Tkinter`.
- Logs processing steps and errors for troubleshooting.
- **DYNAMICS**: E.g One input file of 50 pages produces one output file of 100 pages

## Requirements

Ensure you have **Python 3.8+** installed. Then, install dependencies:

```bash
pip install -r requirements.txt
```
## Project Structure
```graphql
.
├── data_extractor.py         # Extracts data from PDF files
├── document_generator.py     # Generates formatted PDF documents
├── pdf_processor.py          # Main application with GUI and batch processing
├── requirements.txt          # Dependencies
├── fonts/                    # Required font files
├── images/                   # Signature and logo images
├── docs/                     # Additional PDF templates
```

## How to Run
Run the application using:
```bash
python pdf_processor.py
```
## Convert to macOS App using PyInstaller
To convert this Python project into a standalone macOS app, follow these steps:

### 1. Install PyInstaller
Ensure `pyinstaller` is installed:
```bash
pip install pyinstaller
```
### 2. Create the macOS App
Run the following command in the terminal:
```bash
./build_macos.sh
```

**What you'll get:**
- `dist/PDF Processor.app` - A proper macOS application bundle (not just a single file)
- This is a complete macOS app that users can double-click to run
- Includes all fonts, images, and documents bundled inside

**Explanation of Flags:**
- `--onedir` : Creates a directory bundle (macOS .app format) instead of a single file
- `--windowed` : Hides the terminal window when running the app
- `--name "PDF Processor"` : Sets the application name with spaces (macOS style)
- `--icon=icon.icns` : (Optional) Use a custom app icon. Place the `.icns` file in the project directory

### 3. Edit the .spec File
After running PyInstaller for the first time, it generates a `.spec` file.\
Modify the `.spec` file to ensure all dependencies and data files (like fonts, images, and docs) are included.

Edit `pdf_processor.spec` to include dependencies:
Open `pdf_processor.spec` and modify the `datas` section:
```python
a = Analysis(
    ['pdf_processor.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('fonts/', 'fonts/'),
        ('images/', 'images/'),
        ('docs/', 'docs/')
    ],
    hiddenimports=['reportlab', 'PyPDF2', 'fitz'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
)
```
After modifying the `.spec` file, rebuild the application with:
```bash
pyinstaller pdf_processor.spec
```

## 4. Run the App
After running the command, the compiled app will be located inside the `dist/` directory.

To run the app:
```bash
# For macOS .app bundle:
open "dist/PDF Processor.app"

# Or simply double-click the PDF Processor.app file in Finder
```

## 5. Create a .dmg Installer (Optional)
To distribute the app, you may want to package it into a `.dmg` file:
```bash
hdiutil create -volname "PDF Processor" -srcfolder "dist/PDF Processor.app" -ov -format UDZO PDF_Processor.dmg
```

## Automated Builds with GitHub Actions

This project includes GitHub Actions workflows for automated cross-platform builds:

### Available Workflows

1. **macOS App Build** (`.github/workflows/build-macos-app.yml`)
   - Builds a macOS `.app` bundle (proper application format)
   - Creates a `.dmg` installer
   - Uploads artifacts for download

2. **Windows Executable Build** (`.github/workflows/build-windows-exe.yml`)
   - Builds a Windows `.exe` executable
   - Includes all dependencies
   - Uploads artifacts for download

3. **Cross-Platform Build** (`.github/workflows/build-cross-platform.yml`)
   - Builds for both macOS and Windows
   - Creates releases with all artifacts
   - Automatically creates GitHub releases

### How to Use GitHub Actions

1. **Push to GitHub**: Commit and push your code to a GitHub repository
2. **Trigger Workflows**: Go to the "Actions" tab in your repository
3. **Download Artifacts**: After successful builds, download the executables from the "Artifacts" section
4. **Automatic Releases**: The cross-platform workflow will create releases with all built executables

### Local Testing

Before pushing to GitHub, test your build setup locally:

```bash
python test_github_actions.py
```

This script will:
- Validate your build configuration
- Test dependency installation
- Check GitHub Actions files
- Simulate the build process

### CI/CD Compatibility

The build scripts automatically detect when running in GitHub Actions and skip interactive prompts:

- **Windows**: Detects `CI` environment variable and skips `pause` commands
- **macOS**: Detects `CI=true` and skips user input prompts
- **Local builds**: Interactive prompts remain for user convenience

### Workflow Triggers

- **Manual**: Click "Run workflow" in the Actions tab
- **Push to main/master**: Automatic on push to default branch
- **Pull Request**: Automatic on PR creation
- **Release**: Automatic on release creation

### Requirements for GitHub Actions

- Repository must be public or have GitHub Actions enabled for private repos
- Python 3.8+ available on GitHub runners
- All dependencies listed in `requirements.txt`
- Font and image files in correct directories

## Troubleshooting
- If fonts are missing, ensure they are in the fonts folder.
- If images are not found, check the images directory path.
- If dependencies are missing, reinstall them:
```bash
pip install -r requirements.txt
```
- If the `.app` crashes on another Mac, run the following before building:
```bash
pyinstaller --clean pdf_processor.spec
```
- **GitHub Actions fails with timeout**: The build scripts now automatically detect CI environments and skip interactive prompts. If you still encounter issues, ensure the `CI` environment variable is properly set.

## Author
Developed by **Gideon Ayanwoye**\
Email: ayanwoyegideon@gmail.com

##
#### Enjoy using the PDF Processor! 🚀
