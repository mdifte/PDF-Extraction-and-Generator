# macOS Compatibility Configuration

This document explains the macOS compatibility configuration for the PDF Processor application.

## Problem Solved

The original issue was that the macOS application required macOS 11.0 or newer, which prevented it from running on macOS Catalina (10.15). This has been resolved by implementing proper deployment target configuration.

## Current Compatibility

- **Minimum macOS version**: 10.15 (Catalina)
- **Architecture support**: Universal binary (Intel + Apple Silicon)
- **Tested on**: macOS 10.15+ (Catalina and newer)

## Technical Implementation

### 1. Deployment Target Configuration

The build process now sets `MACOSX_DEPLOYMENT_TARGET=10.15` to ensure compatibility with Catalina:

```bash
export MACOSX_DEPLOYMENT_TARGET=10.15
```

This is set in:
- `build_macos.sh` (local builds)
- GitHub Actions workflows (automated builds)

### 2. PyInstaller Configuration

The build uses PyInstaller with universal binary support:

```bash
pyinstaller --target-architecture universal2 ...
```

This creates a universal binary that works on both Intel and Apple Silicon Macs.

### 3. Info.plist Configuration

Two Info.plist files are configured:

#### Base Info.plist
```xml
<key>LSMinimumSystemVersion</key>
<string>10.15</string>
```

#### App-Info.plist (Enhanced)
```xml
<key>LSMinimumSystemVersion</key>
<string>10.15</string>

<key>LSArchitecturePriority</key>
<array>
    <string>arm64</string>
    <string>x86_64</string>
</array>

<key>LSMinimumSystemVersionByArchitecture</key>
<dict>
    <key>arm64</key>
    <string>11.0</string>
    <key>x86_64</key>
    <string>10.15</string>
</dict>
```

This configuration:
- Sets overall minimum to 10.15 (Catalina)
- Allows Apple Silicon Macs (arm64) to require 11.0 (Big Sur) since that's when Apple Silicon was introduced
- Allows Intel Macs (x86_64) to run on 10.15 (Catalina)

## Validation

Run the validation script to check configuration:

```bash
python3 validate_macos_compatibility.py
```

This script validates:
- Environment variables
- Info.plist configurations  
- Build script settings
- Architecture support

## Build Process

1. Set deployment target environment variable
2. Build with universal2 architecture
3. Copy enhanced Info.plist to app bundle
4. Validate compatibility configuration

## Testing Compatibility

### On macOS Catalina (10.15):
- Intel Macs: ✅ Supported
- Apple Silicon: N/A (Apple Silicon requires 11.0+)

### On macOS Big Sur (11.0) and newer:
- Intel Macs: ✅ Supported
- Apple Silicon: ✅ Supported

## Notes

- The universal binary allows a single app to work on both Intel and Apple Silicon Macs
- The enhanced Info.plist ensures proper version checking per architecture
- GitHub Actions automatically validates the configuration before building
- The deployment target setting affects how the Python interpreter and dependencies are compiled