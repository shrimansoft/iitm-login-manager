# 🚀 Public Distribution Setup Guide

This guide will help you publish your IITM Login Manager to make it installable by anyone using `sudo apt install iitm-login-manager`.

## 📋 Prerequisites

- GitHub account
- Git installed and configured
- Your package built and tested locally

## 🔧 Step-by-Step Setup

### Step 1: Create GitHub Repository

1. **Go to GitHub** and create a new public repository:
   - Repository name: `iitm-login-manager`
   - Description: "Ubuntu system tray application for IITM login automation with secure credential management"
   - Make it **Public**
   - Don't initialize with README (we already have one)

2. **Note your GitHub username** - you'll need to replace `YOUR_USERNAME` in the configuration files

### Step 2: Update Configuration Files

Replace `YOUR_USERNAME` with your actual GitHub username in these files:

**Files to update:**
- `README.md`
- `install-from-github.sh`
- `GITHUB_DISTRIBUTION_GUIDE.md`

**Quick replacement command:**
```bash
cd /home/diro_1/Documents/shriman/1_projects/test_website/iitm-login-manager

# Replace YOUR_USERNAME with your actual GitHub username
GITHUB_USERNAME="your-actual-username"  # ⚠️ CHANGE THIS

find . -type f \( -name "*.md" -o -name "*.sh" \) -exec sed -i "s/YOUR_USERNAME/$GITHUB_USERNAME/g" {} \;
```

### Step 3: Push to GitHub

```bash
cd /home/diro_1/Documents/shriman/1_projects/test_website/iitm-login-manager

# Add your GitHub repository as remote (replace with your username)
git remote add origin https://github.com/YOUR_USERNAME/iitm-login-manager.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Enable GitHub Pages for APT Repository

1. **Go to your repository settings**: `https://github.com/YOUR_USERNAME/iitm-login-manager/settings`

2. **Navigate to Pages section**

3. **Configure Pages**:
   - Source: "Deploy from a branch"
   - Branch: `apt-repo` (will be created automatically by GitHub Actions)
   - Folder: `/ (root)`

4. **Save the settings**

### Step 5: Test the Automated Build

The GitHub Actions workflow will automatically:
- Build the package on every push to `main`
- Create the APT repository on the `apt-repo` branch
- Deploy to GitHub Pages

**Wait for the first build** (check the Actions tab in your repository)

### Step 6: Verify Public Installation

Once GitHub Actions completes (usually 2-5 minutes), test the public installation:

```bash
# Test the one-liner installation
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh | sudo bash
```

## 🌐 Public URLs

After setup, your project will have these public URLs:

- **Repository**: `https://github.com/YOUR_USERNAME/iitm-login-manager`
- **APT Repository**: `https://YOUR_USERNAME.github.io/iitm-login-manager/`
- **Installation Script**: `https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh`
- **Direct Package Download**: `https://YOUR_USERNAME.github.io/iitm-login-manager/pool/main/iitm-login-manager_1.0.0-1_all.deb`

## 📦 User Installation Methods

Users can install your software in three ways:

### Method 1: One-liner (Recommended)
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh | sudo bash
```

### Method 2: Manual APT Setup
```bash
echo "deb [trusted=yes] https://YOUR_USERNAME.github.io/iitm-login-manager/ stable main" | sudo tee /etc/apt/sources.list.d/iitm-login-manager.list
sudo apt update
sudo apt install iitm-login-manager
```

### Method 3: Direct .deb Download
```bash
wget https://YOUR_USERNAME.github.io/iitm-login-manager/pool/main/iitm-login-manager_1.0.0-1_all.deb
sudo dpkg -i iitm-login-manager_1.0.0-1_all.deb
sudo apt-get install -f
```

## 🔄 Maintenance and Updates

### Updating the Package

1. **Make changes** to your code
2. **Update version** in `debian/changelog`
3. **Commit and push** to main branch
4. **GitHub Actions** will automatically build and deploy

### Manual Package Update

If you need to manually update the package:

```bash
# Build new package
./build-package.sh

# The GitHub Actions will handle deployment automatically
# Or manually update the apt-repo branch if needed
```

## 📊 Monitoring

### Check Build Status
- Visit: `https://github.com/YOUR_USERNAME/iitm-login-manager/actions`
- Look for green checkmarks ✅ or red X's ❌

### Verify APT Repository
- Visit: `https://YOUR_USERNAME.github.io/iitm-login-manager/`
- Should show a nice webpage with installation instructions

### Test Installation
Regularly test the installation process:
```bash
# Test in a clean Ubuntu VM or container
docker run -it ubuntu:22.04 bash
apt update
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh | bash
```

## 🎯 Share with the Community

### Documentation for Users

Add these instructions to your repository's main README:

```markdown
## Quick Installation

Install IITM Login Manager with a single command:

\`\`\`bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh | sudo bash
\`\`\`

## Usage

After installation:
- **CLI**: `iitm-login-manager --help`
- **GUI**: `iitm-login-tray` or find it in Applications → Internet
- **Setup**: `iitm-login-manager setup` (first time only)
```

### Share the Project

- **Reddit**: r/IITMadras, r/linux, r/Ubuntu
- **Discord/Telegram**: IITM student groups
- **GitHub**: Add topics like `iitm`, `ubuntu`, `system-tray`, `automation`
- **Word of mouth**: Tell fellow students and faculty

## 🔐 Security Best Practices

### For Production Use

1. **GPG Sign Packages** (Optional but recommended):
   ```bash
   # Generate GPG key
   gpg --full-generate-key
   
   # Export public key
   gpg --armor --export your@email.com > key.gpg
   
   # Add to repository and update workflow
   ```

2. **Use Semantic Versioning**: Update versions properly in `debian/changelog`

3. **Test Before Release**: Always test packages before pushing to main

## 🚨 Troubleshooting

### Build Failures
- Check GitHub Actions logs
- Verify all dependencies are listed in `debian/control`
- Test build locally with `./build-package.sh`

### Installation Issues
- Test the installation script on clean Ubuntu systems
- Verify APT repository metadata is generated correctly
- Check GitHub Pages deployment status

### Permission Issues
- Ensure GitHub repository is public
- Verify GitHub Pages is enabled
- Check Actions permissions in repository settings

## ✅ Success Checklist

- [ ] GitHub repository created and configured
- [ ] All `YOUR_USERNAME` placeholders replaced
- [ ] Code pushed to GitHub
- [ ] GitHub Actions workflow running successfully
- [ ] GitHub Pages enabled and working
- [ ] APT repository accessible at `https://YOUR_USERNAME.github.io/iitm-login-manager/`
- [ ] Installation script tested and working
- [ ] Package installs correctly via `apt install`
- [ ] Application functions properly after installation

## 🎉 Congratulations!

Your IITM Login Manager is now publicly available! Anyone can install it using:

```bash
sudo apt install iitm-login-manager
```

Just like any other Ubuntu software package! 🎊

## 📞 Support

If you encounter issues during setup:

1. Check the [GitHub Actions logs](https://github.com/YOUR_USERNAME/iitm-login-manager/actions)
2. Verify the [APT repository](https://YOUR_USERNAME.github.io/iitm-login-manager/) is accessible
3. Test the [installation script](https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh)
4. Create an issue in the repository for help

Your software is now ready for the world! 🌍
