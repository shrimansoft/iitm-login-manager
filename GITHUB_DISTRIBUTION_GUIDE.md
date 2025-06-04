# GitHub Distribution Guide for IITM Login Manager

This guide explains how to publish the IITM Login Manager to GitHub and set up a public APT repository so anyone can install it using `sudo apt install iitm-login-manager`.

## Table of Contents
1. [Publishing to GitHub](#publishing-to-github)
2. [Setting Up GitHub Pages APT Repository](#setting-up-github-pages-apt-repository)
3. [Automated Package Building with GitHub Actions](#automated-package-building-with-github-actions)
4. [Distribution Instructions for Users](#distribution-instructions-for-users)

## Publishing to GitHub

### Step 1: Create a GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon and select "New repository"
3. Name the repository: `iitm-login-manager`
4. Add description: "Ubuntu system tray application for IITM login automation with secure credential management"
5. Make it **Public**
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### Step 2: Add Remote and Push

```bash
cd /home/diro_1/Documents/shriman/1_projects/test_website/iitm-login-manager

# Add your GitHub repository as remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/iitm-login-manager.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Setting Up GitHub Pages APT Repository

### Step 3: Create APT Repository Structure

Create a new branch for the APT repository:

```bash
# Create and switch to apt-repo branch
git checkout --orphan apt-repo
git rm -rf .
```

### Step 4: Set Up Repository Files

Create the APT repository structure:

```bash
mkdir -p dists/stable/main/binary-amd64
mkdir -p pool/main
```

Copy your .deb package to the pool:
```bash
cp ../iitm-login-manager_1.0.0-1_all.deb pool/main/
```

### Step 5: Create Repository Metadata

Create `generate-repo.sh`:
```bash
#!/bin/bash
set -e

# Build package if it doesn't exist
if [ ! -f "pool/main/iitm-login-manager_1.0.0-1_all.deb" ]; then
    echo "Building package..."
    cd ..
    ./build-package.sh
    cd apt-repo
    cp ../iitm-login-manager_1.0.0-1_all.deb pool/main/
fi

# Generate Packages file
cd dists/stable/main/binary-amd64
dpkg-scanpackages ../../../../pool/main /dev/null | gzip -9c > Packages.gz
dpkg-scanpackages ../../../../pool/main /dev/null > Packages

# Generate Release file
cd ..
cat > Release << EOF
Suite: stable
Codename: stable
Components: main
Architectures: amd64 all
Date: $(date -Ru)
EOF

# Calculate checksums
echo "MD5Sum:" >> Release
for file in main/binary-amd64/Packages main/binary-amd64/Packages.gz; do
    if [ -f "$file" ]; then
        echo " $(md5sum "$file" | cut -d' ' -f1) $(stat --printf="%s" "$file") $file" >> Release
    fi
done

echo "SHA1:" >> Release
for file in main/binary-amd64/Packages main/binary-amd64/Packages.gz; do
    if [ -f "$file" ]; then
        echo " $(sha1sum "$file" | cut -d' ' -f1) $(stat --printf="%s" "$file") $file" >> Release
    fi
done

echo "SHA256:" >> Release
for file in main/binary-amd64/Packages main/binary-amd64/Packages.gz; do
    if [ -f "$file" ]; then
        echo " $(sha256sum "$file" | cut -d' ' -f1) $(stat --printf="%s" "$file") $file" >> Release
    fi
done

echo "APT repository generated successfully!"
```

Make it executable:
```bash
chmod +x generate-repo.sh
```

### Step 6: Enable GitHub Pages

1. Push the apt-repo branch:
```bash
git add .
git commit -m "Initial APT repository setup"
git push origin apt-repo
```

2. Go to your GitHub repository → Settings → Pages
3. Select "Deploy from a branch"
4. Choose "apt-repo" branch and "/ (root)" folder
5. Save

Your APT repository will be available at: `https://YOUR_USERNAME.github.io/iitm-login-manager/`

## Automated Package Building with GitHub Actions

### Step 7: Set Up GitHub Actions

Switch back to main branch and create workflow:

```bash
git checkout main
mkdir -p .github/workflows
```

Create `.github/workflows/build-and-deploy.yml`:

```yaml
name: Build and Deploy APT Package

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y debhelper dh-python python3-setuptools
        pip install -r requirements.txt
    
    - name: Build package
      run: |
        chmod +x build-package.sh
        ./build-package.sh
    
    - name: Upload package artifact
      uses: actions/upload-artifact@v3
      with:
        name: deb-package
        path: "*.deb"
    
    - name: Deploy to APT repository
      if: github.ref == 'refs/heads/main'
      run: |
        # Configure git
        git config --global user.name 'GitHub Actions'
        git config --global user.email 'actions@github.com'
        
        # Clone apt-repo branch
        git clone --single-branch --branch apt-repo https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}.git apt-repo
        
        # Copy new package
        cp *.deb apt-repo/pool/main/
        
        # Update repository
        cd apt-repo
        chmod +x generate-repo.sh
        ./generate-repo.sh
        
        # Commit and push
        git add .
        git commit -m "Update package: $(date)"
        git push
```

### Step 8: Create Installation Script

Create `install-from-github.sh`:

```bash
#!/bin/bash
set -e

# IITM Login Manager - GitHub Installation Script
echo "Installing IITM Login Manager from GitHub..."

# Add repository key (if you set up GPG signing)
# wget -qO - https://YOUR_USERNAME.github.io/iitm-login-manager/key.gpg | sudo apt-key add -

# Add repository
echo "deb [trusted=yes] https://YOUR_USERNAME.github.io/iitm-login-manager/ stable main" | sudo tee /etc/apt/sources.list.d/iitm-login-manager.list

# Update package list
sudo apt update

# Install package
sudo apt install -y iitm-login-manager

echo "Installation complete!"
echo "Run 'iitm-login-manager --help' for usage instructions"
echo "To start the system tray application, run: iitm-login-tray"
```

Make it executable:
```bash
chmod +x install-from-github.sh
```

## Distribution Instructions for Users

### Quick Installation (Recommended)

Users can install with a single command:

```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh | sudo bash
```

### Manual Installation

1. Add the APT repository:
```bash
echo "deb [trusted=yes] https://YOUR_USERNAME.github.io/iitm-login-manager/ stable main" | sudo tee /etc/apt/sources.list.d/iitm-login-manager.list
sudo apt update
```

2. Install the package:
```bash
sudo apt install iitm-login-manager
```

### Direct .deb Download

Users can also download and install the .deb file directly:

```bash
wget https://YOUR_USERNAME.github.io/iitm-login-manager/pool/main/iitm-login-manager_1.0.0-1_all.deb
sudo dpkg -i iitm-login-manager_1.0.0-1_all.deb
sudo apt-get install -f  # Fix any dependency issues
```

## Security Considerations

### GPG Signing (Optional but Recommended)

For production use, sign your packages and repository:

1. Generate GPG key:
```bash
gpg --full-generate-key
```

2. Export public key:
```bash
gpg --armor --export YOUR_EMAIL > key.gpg
```

3. Add to repository and update installation instructions

### Repository Security

- Use HTTPS URLs
- Consider using GitHub's built-in security features
- Regularly update dependencies

## Maintenance

### Updating the Package

1. Make changes to your code
2. Update version in `debian/changelog`
3. Commit and push to main branch
4. GitHub Actions will automatically build and deploy

### Manual Updates

```bash
# Build new package
./build-package.sh

# Switch to apt-repo branch
git checkout apt-repo

# Copy new package
cp ../iitm-login-manager_*.deb pool/main/

# Update repository
./generate-repo.sh

# Commit and push
git add .
git commit -m "Update to version X.X.X"
git push
```

## Example Repository URLs

Replace `YOUR_USERNAME` with your actual GitHub username:

- Repository: `https://github.com/YOUR_USERNAME/iitm-login-manager`
- APT Repository: `https://YOUR_USERNAME.github.io/iitm-login-manager/`
- Installation Script: `https://raw.githubusercontent.com/YOUR_USERNAME/iitm-login-manager/main/install-from-github.sh`

## Support

After publishing, users can:
- Report issues on GitHub
- Contribute via pull requests
- Star the repository to show support

Your IITM Login Manager will be installable via APT just like any official Ubuntu package!
