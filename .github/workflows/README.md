# 🚀 GitHub Actions - Automated Builds

This directory contains GitHub Actions workflows for automatically building your PDF Processor application for multiple platforms.

## 📋 Available Workflows

### 1. **build-macos-app.yml** - macOS Only
- Builds the macOS app on every push/PR
- Creates `PDF_Processor` executable
- Perfect for macOS-focused development

### 2. **build-windows-exe.yml** - Windows Only
- Builds the Windows executable on every push/PR
- Creates `PDF_Processor.exe` executable
- Perfect for Windows-focused development

### 3. **build-cross-platform.yml** - Both Platforms
- Builds for both Windows and macOS simultaneously
- Creates GitHub releases automatically
- Best for production deployments

## 🎯 How to Use

### Option 1: Automatic Builds (Recommended)
1. **Push your code** to the `main` or `master` branch
2. **GitHub Actions** will automatically start building
3. **Download artifacts** from the Actions tab
4. **For releases**: Automatic releases are created on main branch pushes

### Option 2: Manual Builds
1. Go to **Actions** tab in your GitHub repository
2. Select the desired workflow
3. Click **"Run workflow"**
4. Choose the branch and run

## 📦 Build Artifacts

### What You'll Get:
- ✅ **Windows**: `PDF_Processor.exe` (~50-70 MB)
- ✅ **macOS**: `PDF_Processor` (~50-70 MB)
- ✅ **Archives**: ZIP/TAR files for distribution
- ✅ **Release Assets**: Automatically uploaded to GitHub Releases

### Download Locations:
1. **Actions Tab** → Select workflow run → **Artifacts** section
2. **Releases Tab** → Download from latest release (for main branch)
3. **Direct Download** from workflow summary

## ⚙️ Workflow Features

### 🔧 Automated Setup:
- ✅ Python 3.11 environment
- ✅ PyInstaller installation
- ✅ Dependency management
- ✅ Build validation

### 📁 Asset Bundling:
- ✅ All font files (16 fonts)
- ✅ All images (logos, signatures)
- ✅ Document templates
- ✅ Python runtime

### 🧪 Quality Assurance:
- ✅ Pre-build validation
- ✅ Build verification
- ✅ File size reporting
- ✅ Error handling

### 📊 Build Reports:
- ✅ Build summaries
- ✅ File information
- ✅ Asset counts
- ✅ Usage instructions

## 🚀 Getting Started

### Step 1: Enable GitHub Actions
1. Push this code to your GitHub repository
2. Go to **Settings** → **Actions** → **General**
3. Set **"Allow all actions and reusable workflows"**

### Step 2: First Build
1. Make a commit and push to `main` branch
2. Go to **Actions** tab
3. Watch the build progress
4. Download artifacts when complete

### Step 3: Manual Trigger (Optional)
1. Go to **Actions** tab
2. Select **"Build Cross-Platform Executables"**
3. Click **"Run workflow"**
4. Select branch and run

## 📋 Workflow Triggers

### Automatic Triggers:
- ✅ Push to `main` or `master` branch
- ✅ Pull requests to `main` or `master`
- ✅ Manual workflow dispatch

### Build Matrix:
- **Windows**: `windows-latest` (Windows Server 2022)
- **macOS**: `macos-latest` (macOS 12)

## 🔍 Monitoring Builds

### Real-time Monitoring:
1. **Actions Tab** → Click on running workflow
2. **View logs** for each step
3. **Download artifacts** when complete
4. **Check build summaries** for details

### Build Status:
- 🟢 **Success**: Green checkmark
- 🔴 **Failed**: Red X with error details
- 🟡 **Running**: Yellow circle
- ⚪ **Queued**: Gray circle

## 🐛 Troubleshooting

### Common Issues:

#### Build Fails:
```
❌ Check the build logs for specific errors
❌ Ensure all required files are committed
❌ Verify requirements.txt is up to date
❌ Check for Python version compatibility
```

#### Missing Artifacts:
```
❌ Wait for build to complete (5-10 minutes)
❌ Check if build succeeded (green checkmark)
❌ Look in the "Artifacts" section of the workflow run
❌ Try re-running the workflow
```

#### Large File Sizes:
```
ℹ️ Expected: 50-70 MB (includes Python runtime)
ℹ️ GitHub has 2GB limit per artifact
ℹ️ Consider splitting large builds if needed
```

## 📈 Advanced Configuration

### Customizing Workflows:

#### Change Python Version:
```yaml
- uses: actions/setup-python@v4
  with:
    python-version: '3.10'  # or '3.9', '3.8'
```

#### Add Build Steps:
```yaml
- name: Custom build step
  run: |
    echo "Custom build logic here"
```

#### Modify Triggers:
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly builds
```

## 🎯 Best Practices

### ✅ Do's:
- Keep workflows in `.github/workflows/` directory
- Use descriptive names for workflows
- Include error handling in scripts
- Test workflows on feature branches first
- Use manual dispatch for testing

### ❌ Don'ts:
- Don't commit large files (>100MB)
- Don't use secrets in workflow files
- Don't hardcode sensitive information
- Don't create too many concurrent builds

## 📞 Support

### Getting Help:
1. **Check workflow logs** for detailed error messages
2. **Review build summaries** for status information
3. **Test locally first** using the build scripts
4. **Check GitHub Actions documentation**

### Useful Links:
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.org/)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

**Happy Building! 🚀**

*Automatically build and distribute your PDF Processor app with GitHub Actions!* 🎉
