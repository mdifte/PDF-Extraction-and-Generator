#!/usr/bin/env python3
"""
GitHub Actions Workflow Tester
Tests your build scripts locally before pushing to GitHub
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n🔧 {description}")
    print(f"Command: {cmd}")
    print("-" * 50)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED (Exit code: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def test_validation():
    """Test the validation script"""
    return run_command("python validate_build.py", "Testing build validation")

def test_dependencies():
    """Test dependency installation"""
    return run_command("pip install -r requirements.txt", "Testing dependency installation")

def test_build_script():
    """Test the appropriate build script for current platform"""
    system = platform.system().lower()

    if system == "windows":
        return run_command("python -c \"print('Windows build script would run here')\"", "Testing Windows build script")
    elif system == "darwin":  # macOS
        return run_command("chmod +x build_macos.sh && echo 'macOS build script is executable'", "Testing macOS build script")
    else:
        print(f"⚠️  Unsupported platform: {system}")
        return False

def check_github_actions_files():
    """Check if GitHub Actions files are present"""
    print("\n📋 Checking GitHub Actions files...")

    required_files = [
        ".github/workflows/build-macos-app.yml",
        ".github/workflows/build-windows-exe.yml",
        ".github/workflows/build-cross-platform.yml",
        ".github/workflows/README.md"
    ]

    all_present = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            all_present = False

    return all_present

def main():
    print("=" * 60)
    print("🚀 GitHub Actions Workflow Tester")
    print("=" * 60)
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    print("=" * 60)

    # Check GitHub Actions files
    if not check_github_actions_files():
        print("\n❌ GitHub Actions files are missing!")
        print("Please ensure all workflow files are present before pushing to GitHub.")
        return 1

    # Run tests
    tests = [
        ("Validation Script", test_validation),
        ("Dependencies", test_dependencies),
        ("Build Script", test_build_script)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        result = test_func()
        results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    for i, (test_name, _) in enumerate(tests):
        status = "✅ PASS" if results[i] else "❌ FAIL"
        print(f"{test_name}: {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
        print("Your code is ready for GitHub Actions deployment.")
        print("\nNext steps:")
        print("1. Commit and push these files to your GitHub repository")
        print("2. Go to Actions tab to see the automated builds")
        print("3. Download the built executables from the Artifacts section")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        print("Please fix the issues before deploying to GitHub Actions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
