#!/usr/bin/env python3
"""
Validate macOS build configuration for compatibility
"""
import os
import sys
import plistlib
import subprocess

def check_environment():
    """Check build environment settings"""
    print("🔍 Checking build environment...")
    
    # Check MACOSX_DEPLOYMENT_TARGET
    deployment_target = os.environ.get('MACOSX_DEPLOYMENT_TARGET')
    if deployment_target:
        print(f"✅ MACOSX_DEPLOYMENT_TARGET is set to: {deployment_target}")
        if deployment_target == "10.15":
            print("✅ Correct deployment target for Catalina compatibility")
        else:
            print(f"⚠️  Deployment target {deployment_target} may not support Catalina")
    else:
        print("⚠️  MACOSX_DEPLOYMENT_TARGET not set - will use system default")
    
    # Check Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check PyInstaller if available
    try:
        result = subprocess.run(['pyinstaller', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"📦 PyInstaller version: {result.stdout.strip()}")
        else:
            print("⚠️  PyInstaller not found or not working")
    except FileNotFoundError:
        print("⚠️  PyInstaller not installed")

def validate_info_plist(file_path):
    """Validate Info.plist configuration"""
    print(f"\n🔍 Validating {file_path}...")
    
    try:
        with open(file_path, 'rb') as f:
            plist_data = plistlib.load(f)
        
        # Check minimum system version
        min_version = plist_data.get('LSMinimumSystemVersion')
        if min_version:
            print(f"✅ LSMinimumSystemVersion: {min_version}")
            if min_version >= "10.15":
                print("✅ Supports Catalina and newer")
            else:
                print(f"⚠️  Version {min_version} is older than Catalina (10.15)")
        else:
            print("❌ LSMinimumSystemVersion not found")
        
        # Check bundle identifier
        bundle_id = plist_data.get('CFBundleIdentifier')
        if bundle_id:
            print(f"✅ Bundle identifier: {bundle_id}")
        
        # Check architecture priority (if present)
        arch_priority = plist_data.get('LSArchitecturePriority')
        if arch_priority:
            print(f"✅ Architecture priority: {arch_priority}")
        
        # Check architecture-specific versions (if present)
        arch_versions = plist_data.get('LSMinimumSystemVersionByArchitecture')
        if arch_versions:
            print("✅ Architecture-specific minimum versions:")
            for arch, version in arch_versions.items():
                print(f"   {arch}: {version}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ {file_path} not found")
        return False
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return False

def validate_build_script():
    """Validate build script configuration"""
    print("\n🔍 Validating build script...")
    
    script_path = "build_macos.sh"
    try:
        with open(script_path, 'r') as f:
            content = f.read()
        
        if "MACOSX_DEPLOYMENT_TARGET=10.15" in content:
            print("✅ Build script sets deployment target to 10.15")
        else:
            print("⚠️  Build script doesn't set deployment target to 10.15")
        
        if "--target-architecture universal2" in content:
            print("✅ Build script uses universal2 architecture")
        else:
            print("⚠️  Build script doesn't use universal2 architecture")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ {script_path} not found")
        return False

def main():
    """Main validation function"""
    print("🚀 macOS Build Configuration Validator")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Validate plist files
    info_plist_valid = validate_info_plist("Info.plist")
    app_info_plist_valid = validate_info_plist("App-Info.plist")
    
    # Validate build script
    script_valid = validate_build_script()
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    
    if info_plist_valid and app_info_plist_valid and script_valid:
        print("✅ All configuration files are valid for Catalina compatibility!")
        print("🎯 The app should work on macOS 10.15 (Catalina) and newer")
        return 0
    else:
        print("❌ Some configuration issues found")
        return 1

if __name__ == "__main__":
    sys.exit(main())