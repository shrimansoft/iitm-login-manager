#!/bin/bash
# IITM Login Manager Installation Script

set -e

echo "===========================================" 
echo "IITM Login Manager Installation Script"
echo "==========================================="

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root. Run as regular user."
   exit 1
fi

# Detect distribution
if command -v apt &> /dev/null; then
    DISTRO="debian"
elif command -v dnf &> /dev/null; then
    DISTRO="fedora"
elif command -v pacman &> /dev/null; then
    DISTRO="arch"
else
    echo "Warning: Could not detect package manager. You may need to install dependencies manually."
    DISTRO="unknown"
fi

echo "Detected distribution type: $DISTRO"

# Install system dependencies
echo ""
echo "Installing system dependencies..."

case $DISTRO in
    "debian")
        echo "Installing dependencies with apt..."
        sudo apt update
        sudo apt install -y python3-pip python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 gir1.2-notify-0.7 python3-setuptools python3-wheel
        ;;
    "fedora")
        echo "Installing dependencies with dnf..."
        sudo dnf install -y python3-pip python3-gobject gtk3-devel libappindicator-gtk3-devel libnotify-devel python3-setuptools python3-wheel
        ;;
    "arch")
        echo "Installing dependencies with pacman..."
        sudo pacman -S --needed python-pip python-gobject gtk3 libappindicator-gtk3 libnotify python-setuptools python-wheel
        ;;
    *)
        echo "Please install the following packages manually:"
        echo "- Python 3 with pip"
        echo "- GTK 3 development files"
        echo "- GObjectIntrospection bindings for Python"
        echo "- AppIndicator3 library"
        echo "- libnotify"
        ;;
esac

# Install Python package
echo ""
echo "Installing IITM Login Manager Python package..."

# Install in user mode to avoid permission issues
pip3 install --user .

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "Warning: ~/.local/bin is not in your PATH."
    echo "Add the following line to your ~/.bashrc or ~/.profile:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Or run the following command now:"
    echo "echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
fi

# Setup initial configuration
echo ""
echo "Setup complete! Now setting up your credentials..."
echo ""

# Run setup if the user agrees
read -p "Would you like to configure your IITM credentials now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ~/.local/bin/iitm-login-manager --setup
fi

echo ""
echo "============================================"
echo "Installation completed successfully!"
echo "============================================"
echo ""
echo "Usage:"
echo "  Start system tray app:   iitm-login-tray"
echo "  Manual login:            iitm-login-manager --login"
echo "  Check status:            iitm-login-manager --status"
echo "  Configure settings:      iitm-login-manager --setup"
echo ""
echo "To start the tray app automatically:"
echo "1. Run: iitm-login-tray"
echo "2. Right-click the tray icon → Settings"
echo "3. Check 'Start with system'"
echo ""
echo "Enjoy automated IITM network login!"
