#!/bin/bash
set -e

# IITM Login Manager - GitHub Installation Script
# This script installs IITM Login Manager from the GitHub APT repository

echo "🔧 IITM Login Manager - GitHub Installation"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository configuration
REPO_URL="https://shrimansoft.github.io/iitm-login-manager/"
PACKAGE_NAME="iitm-login-manager"
LIST_FILE="/etc/apt/sources.list.d/iitm-login-manager.list"

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

# Function to check if repository is already added
check_repository() {
    if [ -f "$LIST_FILE" ]; then
        echo -e "${YELLOW}⚠️  Repository already configured${NC}"
        return 0
    else
        return 1
    fi
}

# Function to add repository
add_repository() {
    echo -e "${BLUE}📦 Adding IITM Login Manager repository...${NC}"
    
    # Create repository entry
    echo "deb [trusted=yes] $REPO_URL stable main" | sudo tee "$LIST_FILE" > /dev/null
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Repository added successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to add repository${NC}"
        return 1
    fi
}

# Function to update package list
update_package_list() {
    echo -e "${BLUE}🔄 Updating package list...${NC}"
    
    sudo apt update > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Package list updated${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to update package list${NC}"
        echo "You may need to check your internet connection or repository configuration."
        return 1
    fi
}

# Function to install package
install_package() {
    echo -e "${BLUE}📦 Installing $PACKAGE_NAME...${NC}"
    
    sudo apt install -y $PACKAGE_NAME
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $PACKAGE_NAME installed successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to install $PACKAGE_NAME${NC}"
        return 1
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
    
    # Check if repository is already added
    if check_repository; then
        echo -e "${BLUE}Repository already configured, proceeding with installation...${NC}"
    else
        # Add repository
        if ! add_repository; then
            exit 1
        fi
    fi
    
    # Update package list
    if ! update_package_list; then
        exit 1
    fi
    
    # Install package
    if ! install_package; then
        exit 1
    fi
    
    # Verify installation
    if ! verify_installation; then
        echo -e "${YELLOW}⚠️  Installation completed but verification failed${NC}"
        echo "The package was installed but some components may not be working correctly."
    fi
    
    echo -e "\n${GREEN}🎉 Installation completed successfully!${NC}"
    show_usage
}

# Handle Ctrl+C
trap 'echo -e "\n${RED}❌ Installation cancelled by user${NC}"; exit 1' INT

# Run main function
main

