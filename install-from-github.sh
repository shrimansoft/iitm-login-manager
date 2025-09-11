#!/bin/bash
set -e

# IITM Login Manager - GitHub Installation Script
# This script installs IITM Login Manager by building from source

echo "🔧 IITM Login Manager - GitHub Installation"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Package configuration
PACKAGE_NAME="iitm-login-manager"
REPO_URL="https://github.com/shrimansoft/iitm-login-manager.git"
TEMP_DIR="/tmp/iitm-login-manager-install"

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}❌ This script should not be run as root. Please run without sudo.${NC}"
   echo "The script will prompt for sudo when needed."
   exit 1
fi

# Check if apt is available
if ! command -v apt &> /dev/null; then
    echo -e "${RED}❌ This script requires apt package manager (Ubuntu/Debian)${NC}"
    exit 1
fi

echo -e "${BLUE}📋 Checking system requirements...${NC}"

# Check Ubuntu/Debian version
if [ -f /etc/os-release ]; then
    . /etc/os-release
    echo -e "${GREEN}✓ Detected: $PRETTY_NAME${NC}"
else
    echo -e "${YELLOW}⚠️  Could not detect OS version${NC}"
fi

# Function to check if package is already installed
check_existing_installation() {
    if dpkg -l | grep -q "^ii.*$PACKAGE_NAME"; then
        echo -e "${YELLOW}⚠️  $PACKAGE_NAME is already installed${NC}"
        local current_version=$(dpkg -l | grep "$PACKAGE_NAME" | awk '{print $3}')
        echo -e "${BLUE}Current version: $current_version${NC}"
        
        echo -n "Do you want to reinstall? (y/N): "
        read -r response
        if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            return 1  # Continue with installation
        else
            echo -e "${GREEN}Installation skipped. Use existing installation.${NC}"
            return 0  # Skip installation
        fi
    else
        return 1  # Not installed, continue
    fi
}

# Function to install build dependencies
install_build_dependencies() {
    echo -e "${BLUE}📋 Installing build dependencies...${NC}"
    
    sudo apt update > /dev/null 2>&1
    
    # Install build tools and dependencies
    sudo apt install -y git python3 python3-pip python3-setuptools 
                        python3-gi python3-gi-cairo gir1.2-gtk-3.0 
                        gir1.2-appindicator3-0.1 gir1.2-notify-0.7 
                        python3-requests python3-keyring > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build dependencies installed${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to install build dependencies${NC}"
        return 1
    fi
}

# Function to setup temporary directory and clone repository
setup_source() {
    echo -e "${BLUE}📁 Setting up source code...${NC}"
    
    # Remove existing temp directory if it exists
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
    
    # Clone the repository
    git clone "$REPO_URL" "$TEMP_DIR" > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Source code downloaded${NC}"
        cd "$TEMP_DIR"
        return 0
    else
        echo -e "${RED}❌ Failed to download source code${NC}"
        return 1
    fi
}

# Function to install package using setup.py
install_package() {
    echo -e "${BLUE}📦 Installing $PACKAGE_NAME...${NC}"
    
    # Install using pip with --user flag to avoid permission issues
    python3 -m pip install --user . > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $PACKAGE_NAME installed successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to install $PACKAGE_NAME${NC}"
        return 1
    fi
}

# Function to create temporary directory
setup_temp_directory() {
    echo -e "${BLUE}� Setting up temporary directory...${NC}"
    
    # Remove existing temp directory if it exists
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
    
    mkdir -p "$TEMP_DIR"
    cd "$TEMP_DIR"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Temporary directory created: $TEMP_DIR${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to create temporary directory${NC}"
        return 1
    fi
}

# Function to download package
download_package() {
    echo -e "${BLUE}� Downloading $DEB_FILE...${NC}"
    
    # Check if wget is available, otherwise use curl
    if command -v wget &> /dev/null; then
        wget -q --show-progress "$DOWNLOAD_URL" -O "$DEB_FILE"
    elif command -v curl &> /dev/null; then
        curl -L --progress-bar "$DOWNLOAD_URL" -o "$DEB_FILE"
    else
        echo -e "${RED}❌ Neither wget nor curl is available${NC}"
        return 1
    fi
    
    if [ $? -eq 0 ] && [ -f "$DEB_FILE" ]; then
        echo -e "${GREEN}✓ Package downloaded successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to download package${NC}"
        echo "URL: $DOWNLOAD_URL"
        return 1
    fi
}

# Function to install dependencies
install_dependencies() {
    echo -e "${BLUE}📋 Installing dependencies...${NC}"
    
    sudo apt update > /dev/null 2>&1
    
    # Install required packages for GUI applications
    sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
                        gir1.2-appindicator3-0.1 gir1.2-notify-0.7 \
                        python3-requests python3-keyring > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Some dependencies may not have been installed${NC}"
        return 0  # Continue anyway
    fi
}

# Function to install package
install_package() {
    echo -e "${BLUE}📦 Installing $DEB_FILE...${NC}"
    
    # Install the .deb package
    sudo dpkg -i "$DEB_FILE"
    
    # Fix any dependency issues
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  Fixing dependencies...${NC}"
        sudo apt-get install -f -y > /dev/null 2>&1
        
        # Try installing again
        sudo dpkg -i "$DEB_FILE"
    fi
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $PACKAGE_NAME installed successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to install $PACKAGE_NAME${NC}"
        return 1
    fi
}

# Function to cleanup
cleanup() {
    echo -e "${BLUE}🧹 Cleaning up...${NC}"
    
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
        echo -e "${GREEN}✓ Temporary files cleaned up${NC}"
    fi
}

# Function to verify installation
verify_installation() {
    echo -e "${BLUE}🔍 Verifying installation...${NC}"
    
    if command -v iitm-login-manager &> /dev/null; then
        echo -e "${GREEN}✓ CLI tool available: iitm-login-manager${NC}"
    else
        echo -e "${RED}❌ CLI tool not found${NC}"
        return 1
    fi
    
    if command -v iitm-login-tray &> /dev/null; then
        echo -e "${GREEN}✓ Tray application available: iitm-login-tray${NC}"
    else
        echo -e "${RED}❌ Tray application not found${NC}"
        return 1
    fi
    
    if [ -f /usr/share/applications/iitm-login-manager.desktop ]; then
        echo -e "${GREEN}✓ Desktop integration available${NC}"
    else
        echo -e "${YELLOW}⚠️  Desktop file not found${NC}"
    fi
    
    return 0
}

# Function to show usage information
show_usage() {
    echo -e "\n${BLUE}🚀 Getting Started${NC}"
    echo "=================="
    echo
    echo "CLI Commands:"
    echo "  iitm-login-manager --help          Show help"
    echo "  iitm-login-manager setup          Setup credentials"
    echo "  iitm-login-manager login          Perform login"
    echo "  iitm-login-manager status         Check login status"
    echo
    echo "GUI Application:"
    echo "  iitm-login-tray                   Start system tray application"
    echo "  Applications → Internet → IITM Login Manager"
    echo
    echo "Configuration:"
    echo "  - Credentials are stored securely using system keyring"
    echo "  - Configuration file: ~/.config/iitm-login-manager/config.json"
    echo "  - Logs: ~/.local/share/iitm-login-manager/logs/"
    echo
    echo "For more information, visit: https://github.com/shrimansoft/iitm-login-manager"
}

# Main installation process
main() {
    echo -e "${BLUE}Starting installation process...${NC}\n"
    
    # Check if already installed
    if check_existing_installation; then
        echo -e "${BLUE}Proceeding with installation/upgrade...${NC}"
    fi
    
    # Setup temporary directory
    if ! setup_temp_directory; then
        exit 1
    fi
    
    # Download package
    if ! download_package; then
        cleanup
        exit 1
    fi
    
    # Install dependencies
    if ! install_dependencies; then
        echo -e "${YELLOW}⚠️  Continuing with package installation despite dependency issues${NC}"
    fi
    
    # Install package
    if ! install_package; then
        cleanup
        exit 1
    fi
    
    # Verify installation
    if ! verify_installation; then
        echo -e "${YELLOW}⚠️  Installation completed but verification failed${NC}"
        echo "The package was installed but some components may not be working correctly."
    fi
    
    # Cleanup
    cleanup
    
    echo -e "\n${GREEN}🎉 Installation completed successfully!${NC}"
    show_usage
}

# Handle Ctrl+C
trap 'echo -e "\n${RED}❌ Installation cancelled by user${NC}"; cleanup; exit 1' INT

# Run main function
main

