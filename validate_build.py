#!/usr/bin/env python3
"""
Pre-build validation script for PDF Processor
Checks if all required files and folders are present before building executable
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists and report status"""
    if os.path.exists(filepath):
        print(f"[OK] {description}: {filepath}")
        return True
    else:
        print(f"[MISSING] {description}: {filepath}")
        return False

def check_directory(dirpath, description, min_files=0):
    """Check if a directory exists and has minimum number of files"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        file_count = len([f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, f))])
        if file_count >= min_files:
            print(f"[OK] {description}: {dirpath} ({file_count} files)")
            return True
        else:
            print(f"[WARNING] {description}: {dirpath} (only {file_count} files, expected {min_files}+)")
            return False
    else:
        print(f"[MISSING] {description}: {dirpath}")
        return False

def check_pathlib_compatibility():
    """Check for pathlib compatibility issues"""
    try:
        import pathlib
        # Check if it's the old backport version by looking at the file location
        import inspect
        pathlib_path = inspect.getfile(pathlib)
        if 'site-packages' in pathlib_path and 'pathlib' in pathlib_path:
            print("WARNING: Old pathlib package detected")
            print("   This may cause PyInstaller compatibility issues")
            print("   The build script will attempt to fix this automatically")
            return False
    except ImportError:
        pass
    
    print("[OK] Pathlib compatibility: OK")
    return True

def main():
    print("=" * 50)
    print("PDF Processor - Pre-Build Validation")
    print("=" * 50)
    print()
    
    current_dir = Path.cwd()
    print(f"Checking directory: {current_dir}")
    print()
    
    all_good = True
    
    # Check main Python files
    print("Main Application Files:")
    all_good &= check_file("pdf_processor.py", "Main GUI application")
    all_good &= check_file("document_generator_updated.py", "Document generator")
    all_good &= check_file("data_extractor.py", "Data extractor")
    print()
    
    # Check build scripts
    print("Build Scripts:")
    all_good &= check_file("build_windows.bat", "Windows build script")
    all_good &= check_file("build_macos.sh", "macOS build script")
    print()
    
    # Check configuration files
    print("Configuration Files:")
    all_good &= check_file("requirements.txt", "Python dependencies")
    print()
    
    # Check resource directories
    print("Resource Directories:")
    all_good &= check_directory("fonts", "Font files", min_files=5)
    all_good &= check_directory("images", "Image files", min_files=1)
    all_good &= check_directory("docs", "Document templates", min_files=1)
    print()
    
    # Check specific critical files
    print("Critical Assets:")
    all_good &= check_file("fonts/Aptos.ttf", "Aptos font")
    all_good &= check_file("fonts/Montserrat-BlackItalic.ttf", "Montserrat Bold Italic font")
    all_good &= check_file("fonts/Montserrat-Medium.ttf", "Montserrat Medium font")
    all_good &= check_file("images/Picture1.png", "Main logo")
    all_good &= check_file("docs/Page 2 REVISED NEW.pdf", "Second page template")
    print()
    
    # Check pathlib compatibility
    print("Compatibility Checks:")
    check_pathlib_compatibility()
    print()
    
    # Check optional files
    print("Optional Files:")
    check_file("document_generator_icon.icns", "Application icon")
    check_file("BUILD_README.md", "Build documentation")
    print()
    
    # Final assessment
    print("=" * 50)
    if all_good:
        print("VALIDATION PASSED!")
        print("All required files are present.")
        print("You can proceed with building the executable.")
        print()
        print("Next steps:")
        print("• Windows: Run build_windows.bat")
        print("• macOS: Run build_macos.sh")
    else:
        print("VALIDATION FAILED!")
        print("Some required files are missing.")
        print("Please ensure all files are in place before building.")
        print()
        print("Missing files must be provided for successful build.")
    
    print("=" * 50)
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
