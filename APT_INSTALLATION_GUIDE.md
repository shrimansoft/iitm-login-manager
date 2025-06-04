# IITM Login Manager - APT Installation Guide

## 📦 APT Package Installation

This guide explains how to install IITM Login Manager using the `apt` package manager, making it available system-wide just like any other Ubuntu package.

## 🔧 Prerequisites

- Ubuntu 20.04+ or Debian 11+ (or compatible distributions)
- `sudo` access for installation
- Internet connection for dependency resolution

## 🚀 Quick Installation

### Option 1: Install from Local Repository (Recommended)

1. **Download and Build the Package:**
   ```bash
   git clone <repository-url>
   cd iitm-login-manager
   ./build-package.sh
   ```

2. **Install via APT:**
   ```bash
   sudo apt update
   sudo apt install iitm-login-manager
   ```

   ✅ **Installation Complete!** The package is now available system-wide.

### Option 2: Manual Package Installation

1. **Build the Package:**
   ```bash
   git clone <repository-url>
   cd iitm-login-manager
   sudo apt install debhelper dh-python python3-setuptools python3-all devscripts
   debuild -us -uc -b
   ```

2. **Install the Generated Package:**
   ```bash
   sudo dpkg -i ../iitm-login-manager_1.0.0-1_all.deb
   sudo apt-get install -f  # Fix any dependency issues
   ```

## 📋 What Gets Installed

When you install via APT, the following components are automatically set up:

### **System Binaries:**
- `/usr/bin/iitm-login-manager` - Command-line interface
- `/usr/bin/iitm-login-tray` - GTK system tray application

### **Python Package:**
- `/usr/lib/python3/dist-packages/iitm_login_manager/` - Core modules
- All Python dependencies automatically resolved

### **Desktop Integration:**
- `/usr/share/applications/iitm-login-manager.desktop` - Application menu entry
- `/usr/share/pixmaps/iitm-login-manager.png` - Application icon
- Automatic registration with desktop environment

### **Documentation:**
- `/usr/share/doc/iitm-login-manager/` - Documentation and examples
- `/usr/share/doc/iitm-login-manager/examples/` - Configuration examples

## 🎯 Post-Installation Setup

### 1. **Initial Configuration:**
```bash
# Set up your IITM credentials (one-time setup)
iitm-login-manager --setup
```

### 2. **Test Installation:**
```bash
# Check if everything is working
iitm-login-manager --status
```

### 3. **Start System Tray:**
```bash
# Launch the GUI application
iitm-login-tray
```

## 🔄 Usage After Installation

### **Command Line Interface:**
```bash
# Perform manual login
iitm-login-manager --login

# Check internet status
iitm-login-manager --status

# View all options
iitm-login-manager --help
```

### **Graphical Interface:**
- **Application Menu:** Look for "IITM Login Manager" in your applications
- **Command:** Run `iitm-login-tray` from terminal
- **System Tray:** The application will appear in your system tray

### **Automatic Startup:**
The application can be configured to start automatically at login through:
- Desktop environment's startup applications
- System tray integration
- User systemd services

## 🔧 Advanced Configuration

### **Systemd User Service (Optional):**
```bash
# Copy the service file to user directory
mkdir -p ~/.config/systemd/user
cp /usr/share/doc/iitm-login-manager/examples/iitm-login-manager.service ~/.config/systemd/user/

# Enable and start the service
systemctl --user enable iitm-login-manager.service
systemctl --user start iitm-login-manager.service
```

### **Desktop Autostart:**
```bash
# Copy desktop file to autostart
mkdir -p ~/.config/autostart
cp /usr/share/applications/iitm-login-manager.desktop ~/.config/autostart/
```

## 🗑️ Removal

### **Uninstall the Package:**
```bash
sudo apt remove iitm-login-manager
```

### **Remove Configuration (Optional):**
```bash
# Remove user configuration
rm -rf ~/.config/iitm-login-manager

# Remove from autostart
rm -f ~/.config/autostart/iitm-login-manager.desktop

# Remove user systemd service
systemctl --user disable iitm-login-manager.service
rm -f ~/.config/systemd/user/iitm-login-manager.service
```

### **Remove Repository (If Added):**
```bash
sudo rm /etc/apt/sources.list.d/iitm-login-manager.list
sudo apt update
```

## 🔍 Troubleshooting

### **Package Not Found:**
```bash
sudo apt update
apt-cache policy iitm-login-manager
```

### **Dependency Issues:**
```bash
sudo apt install -f
sudo apt install --reinstall iitm-login-manager
```

### **GTK/Tray Issues:**
```bash
# Install additional GTK dependencies
sudo apt install gir1.2-appindicator3-0.1 gir1.2-notify-0.7
```

## 📊 Package Information

### **Package Details:**
- **Name:** `iitm-login-manager`
- **Version:** `1.0.0-1`
- **Section:** `net` (Network utilities)
- **Architecture:** `all` (Architecture independent)
- **Maintainer:** Shriman <shrimansoft@gmail.com>

### **Dependencies:**
- `python3` (>= 3.8)
- `python3-requests` - HTTP client library
- `python3-schedule` - Job scheduling
- `python3-keyring` - Secure credential storage
- `python3-gi` - GTK bindings
- `python3-bs4` - HTML parsing
- `gir1.2-gtk-3.0` - GTK 3 library
- `gir1.2-appindicator3-0.1` - System tray support
- `gir1.2-notify-0.7` - Desktop notifications

## 🎉 Benefits of APT Installation

1. **✅ System Integration:** Proper system-wide installation
2. **✅ Dependency Management:** Automatic dependency resolution
3. **✅ Easy Updates:** Update with `apt upgrade`
4. **✅ Clean Removal:** Complete uninstallation support
5. **✅ Security:** Package verification and integrity checks
6. **✅ Standard Location:** Files installed in standard Linux paths
7. **✅ Desktop Integration:** Automatic menu registration
8. **✅ Multi-User Support:** Available to all system users

The APT installation method provides the most robust and Linux-standard way to install and manage IITM Login Manager on your system!
