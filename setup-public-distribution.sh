#!/bin/bash

# 🚀 IITM Login Manager - Public Distribution Setup Script
# This script helps you set up public distribution for your IITM Login Manager

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "🚀 IITM Login Manager - Public Distribution Setup"
echo "================================================="
echo -e "${NC}"

# Check if we're in the right directory
if [ ! -f "setup.py" ] || [ ! -d "iitm_login_manager" ]; then
    echo -e "${RED}❌ This script must be run from the iitm-login-manager project directory${NC}"
    exit 1
fi

# Function to prompt for GitHub username
get_github_username() {
    echo -e "${YELLOW}📝 GitHub Repository Setup${NC}"
    echo "Before proceeding, you need to:"
    echo "1. Create a GitHub account (if you don't have one)"
    echo "2. Create a new public repository named 'iitm-login-manager'"
    echo
    
    read -p "Enter your GitHub username: " GITHUB_USERNAME
    
    if [ -z "$GITHUB_USERNAME" ]; then
        echo -e "${RED}❌ GitHub username is required${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ GitHub username: $GITHUB_USERNAME${NC}"
}

# Function to update configuration files
update_config_files() {
    echo -e "${BLUE}🔧 Updating configuration files...${NC}"
    
    # Files to update
    FILES=(
        "README.md"
        "install-from-github.sh" 
        "GITHUB_DISTRIBUTION_GUIDE.md"
        "PUBLIC_DISTRIBUTION_SETUP.md"
    )
    
    for file in "${FILES[@]}"; do
        if [ -f "$file" ]; then
            sed -i "s/YOUR_USERNAME/$GITHUB_USERNAME/g" "$file"
            echo -e "${GREEN}✓ Updated $file${NC}"
        else
            echo -e "${YELLOW}⚠️  File $file not found, skipping${NC}"
        fi
    done
}

# Function to setup git remote
setup_git_remote() {
    echo -e "${BLUE}🔗 Setting up Git remote...${NC}"
    
    # Check if remote already exists
    if git remote get-url origin &>/dev/null; then
        echo -e "${YELLOW}⚠️  Git remote 'origin' already exists${NC}"
        read -p "Do you want to update it? (y/N): " update_remote
        if [[ $update_remote =~ ^[Yy]$ ]]; then
            git remote set-url origin "https://github.com/$GITHUB_USERNAME/iitm-login-manager.git"
            echo -e "${GREEN}✓ Updated Git remote${NC}"
        fi
    else
        git remote add origin "https://github.com/$GITHUB_USERNAME/iitm-login-manager.git"
        echo -e "${GREEN}✓ Added Git remote${NC}"
    fi
}

# Function to commit and push changes
commit_and_push() {
    echo -e "${BLUE}📤 Committing and pushing changes...${NC}"
    
    # Check if there are changes to commit
    if ! git diff --quiet || ! git diff --cached --quiet; then
        git add .
        git commit -m "Configure for public distribution with GitHub username: $GITHUB_USERNAME"
        echo -e "${GREEN}✓ Changes committed${NC}"
    else
        echo -e "${YELLOW}⚠️  No changes to commit${NC}"
    fi
    
    # Push to GitHub
    echo "Pushing to GitHub repository..."
    git branch -M main
    
    if git push -u origin main; then
        echo -e "${GREEN}✓ Successfully pushed to GitHub${NC}"
    else
        echo -e "${RED}❌ Failed to push to GitHub${NC}"
        echo "Please check:"
        echo "1. Your GitHub repository exists and is accessible"
        echo "2. You have proper authentication set up (token/SSH key)"
        echo "3. Repository URL is correct"
        exit 1
    fi
}

# Function to provide next steps
show_next_steps() {
    echo -e "\n${GREEN}🎉 Repository setup complete!${NC}"
    echo -e "${PURPLE}Next steps:${NC}"
    echo
    echo "1. 🌐 Enable GitHub Pages:"
    echo "   - Go to: https://github.com/$GITHUB_USERNAME/iitm-login-manager/settings/pages"
    echo "   - Source: 'Deploy from a branch'"
    echo "   - Branch: 'apt-repo' (will be created by GitHub Actions)"
    echo "   - Folder: '/ (root)'"
    echo
    echo "2. ⏳ Wait for GitHub Actions to complete (2-5 minutes):"
    echo "   - Check: https://github.com/$GITHUB_USERNAME/iitm-login-manager/actions"
    echo
    echo "3. 🧪 Test the installation:"
    echo "   curl -fsSL https://raw.githubusercontent.com/$GITHUB_USERNAME/iitm-login-manager/main/install-from-github.sh | sudo bash"
    echo
    echo "4. 📊 Monitor your APT repository:"
    echo "   - URL: https://$GITHUB_USERNAME.github.io/iitm-login-manager/"
    echo
    echo "5. 📢 Share with the community:"
    echo "   - Reddit: r/IITMadras, r/linux, r/Ubuntu"
    echo "   - Student groups and forums"
    echo
    echo -e "${BLUE}🎯 Your software will be installable using:${NC}"
    echo -e "${GREEN}sudo apt install iitm-login-manager${NC}"
    echo
    echo "For detailed instructions, see: PUBLIC_DISTRIBUTION_SETUP.md"
}

# Function to validate prerequisites
check_prerequisites() {
    echo -e "${BLUE}🔍 Checking prerequisites...${NC}"
    
    # Check if git is configured
    if ! git config --get user.name &>/dev/null || ! git config --get user.email &>/dev/null; then
        echo -e "${RED}❌ Git is not configured${NC}"
        echo "Please configure git first:"
        echo "git config --global user.name 'Your Name'"
        echo "git config --global user.email 'your.email@example.com'"
        exit 1
    fi
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir &>/dev/null; then
        echo -e "${RED}❌ Not in a git repository${NC}"
        exit 1
    fi
    
    # Check if package builds successfully
    echo "🔨 Testing package build..."
    if ./build-package.sh &>/dev/null; then
        echo -e "${GREEN}✓ Package builds successfully${NC}"
        # Clean up build artifacts
        rm -f *.deb *.build *.buildinfo *.changes
    else
        echo -e "${RED}❌ Package build failed${NC}"
        echo "Please fix build issues before proceeding"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All prerequisites satisfied${NC}"
}

# Main execution
main() {
    echo -e "${BLUE}Starting public distribution setup...${NC}\n"
    
    # Check prerequisites
    check_prerequisites
    echo
    
    # Get GitHub username
    get_github_username
    echo
    
    # Update configuration files
    update_config_files
    echo
    
    # Setup git remote
    setup_git_remote
    echo
    
    # Commit and push
    commit_and_push
    echo
    
    # Show next steps
    show_next_steps
}

# Handle Ctrl+C
trap 'echo -e "\n${RED}❌ Setup cancelled by user${NC}"; exit 1' INT

# Run main function
main

echo -e "\n${GREEN}🎊 Setup completed! Your IITM Login Manager is ready for public distribution!${NC}"
