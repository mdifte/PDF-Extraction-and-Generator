# PDF Processor - Code Signing Setup Guide

## 🔐 Code Signing and Notarization Setup

To enable code signing and notarization for macOS builds, you need to configure the following secrets in your GitHub repository:

### Required Secrets

1. **DEVELOPER_ID_APPLICATION**
   - Your Apple Developer ID Application certificate identifier
   - Format: `Developer ID Application: Your Name (TEAMID)`
   - Example: `Developer ID Application: John Doe (ABC123DEF4)`

2. **AC_NOTARY_PROFILE**
   - The name of your notarytool keychain profile
   - This is created when you run `xcrun notarytool store-credentials`

### Setup Instructions

#### 1. Obtain Apple Developer Certificate
- Go to [Apple Developer Portal](https://developer.apple.com/account/)
- Create a Developer ID Application certificate
- Download and install the certificate on your Mac

#### 2. Set up Notary Tool Credentials
Run the following command on your Mac (replace with your actual values):

```bash
xcrun notarytool store-credentials "AC_NOTARY_PROFILE" \
  --apple-id "your-apple-id@example.com" \
  --team-id "YOUR_TEAM_ID" \
  --password "your-app-specific-password"
```

#### 3. Configure GitHub Secrets
In your GitHub repository:
1. Go to Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `DEVELOPER_ID_APPLICATION`: Your Developer ID Application string
   - `AC_NOTARY_PROFILE`: The profile name you used above

#### 4. Test the Setup
Push a commit to trigger the workflow. The build will automatically:
- Code sign the application
- Submit for notarization
- Staple the notarization ticket

### Troubleshooting

- **Code signing fails**: Verify your Developer ID certificate is valid and installed
- **Notarization fails**: Check your App Store Connect credentials and team ID
- **Gatekeeper blocks app**: Ensure notarization is successful and stapled

### Alternative: Manual Code Signing

If you prefer to sign locally, you can modify the build script:

```bash
# After building the app
codesign --force --deep --options runtime --sign "Developer ID Application: Your Name (TEAMID)" "dist/PDF Processor.app"
xcrun notarytool submit "dist/PDF Processor.app" --keychain-profile "AC_NOTARY_PROFILE" --wait
xcrun stapler staple "dist/PDF Processor.app"
```

### Security Notes

- Never commit certificates or private keys to your repository
- Use GitHub secrets for all sensitive information
- Regularly rotate your App Store Connect credentials
- Keep your Developer ID certificates up to date
