#!/bin/bash
# Build script for IITM Login Manager APT package

set -e

echo "=============================================="
echo "IITM Login Manager - APT Package Builder"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "setup.py" ] || [ ! -d "debian" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Install build dependencies
echo "Installing build dependencies..."
sudo apt update
sudo apt install -y debhelper dh-python python3-setuptools python3-all \
                    devscripts build-essential fakeroot lintian \
                    python3-requests python3-schedule python3-keyring \
                    python3-gi python3-bs4 gir1.2-gtk-3.0 \
                    gir1.2-appindicator3-0.1 gir1.2-notify-0.7

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf debian/.debhelper debian/files debian/debhelper-build-stamp
rm -rf debian/iitm-login-manager* debian/*.substvars
rm -f ../*.deb ../*.dsc ../*.tar.* ../*.buildinfo ../*.changes

# Build the package
echo "Building Debian package..."
debuild -us -uc -b

# Check if package was built successfully
if [ -f "../iitm-login-manager_1.0.0-1_all.deb" ]; then
    echo "✅ Package built successfully!"
    echo "Package location: ../iitm-login-manager_1.0.0-1_all.deb"
    
    # Create local repository directory
    echo "Setting up local APT repository..."
    sudo mkdir -p /opt/iitm-login-manager-repo
    sudo cp ../iitm-login-manager_1.0.0-1_all.deb /opt/iitm-login-manager-repo/
    
    # Create Packages file
    cd /opt/iitm-login-manager-repo
    sudo dpkg-scanpackages . /dev/null | sudo tee Packages > /dev/null
    sudo gzip -k Packages
    
    # Create Release file
    sudo tee Release > /dev/null <<EOF
Archive: stable
Component: main
Origin: IITM Login Manager Repository
Label: IITM Login Manager
Architecture: all
Description: Local repository for IITM Login Manager
EOF
    
    # Add repository to sources
    echo "Adding repository to APT sources..."
    echo "deb [trusted=yes] file:///opt/iitm-login-manager-repo ./" | sudo tee /etc/apt/sources.list.d/iitm-login-manager.list
    
    # Update package lists
    sudo apt update
    
    echo ""
    echo "🎉 SUCCESS! IITM Login Manager is now available via APT!"
    echo ""
    echo "To install, run:"
    echo "  sudo apt install iitm-login-manager"
    echo ""
    echo "To remove the repository later:"
    echo "  sudo rm /etc/apt/sources.list.d/iitm-login-manager.list"
    echo "  sudo apt update"
    
else
    echo "❌ Package build failed!"
    exit 1
fi
