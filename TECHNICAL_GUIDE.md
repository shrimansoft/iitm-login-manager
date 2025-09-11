# IITM Login Manager - Technical Guide

This guide contains detailed technical information for developers and advanced users.

## Advanced Installation Methods

### Manual APT Installation

1. Add the repository:
```bash
echo "deb [trusted=yes] https://shrimansoft.github.io/iitm-login-manager/ stable main" | sudo tee /etc/apt/sources.list.d/iitm-login-manager.list
sudo apt update
```

2. Install the package:
```bash
sudo apt install iitm-login-manager
```

### Direct Download

Download the .deb package directly from GitHub:

```bash
wget https://shrimansoft.github.io/iitm-login-manager/pool/main/iitm-login-manager_1.0.0-1_all.deb
sudo dpkg -i iitm-login-manager_1.0.0-1_all.deb
sudo apt-get install -f  # Fix any dependency issues
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/shrimansoft/iitm-login-manager.git
cd iitm-login-manager
```

2. Install dependencies:
```bash
sudo apt install debhelper dh-python python3-setuptools
pip install -r requirements.txt
```

3. Build and install:
```bash
./build-package.sh
sudo dpkg -i *.deb
```

## System Dependencies

The following system packages are required:

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 gir1.2-notify-0.7
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-gobject gtk3-devel libappindicator-gtk3-devel libnotify-devel
```

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk3 libappindicator-gtk3 libnotify
```

## Advanced Usage

### Command Line Interface

You can use the command line interface for automation:

```bash
# Perform login now
iitm-login-manager --login

# Check internet status
iitm-login-manager --status

# Setup credentials
iitm-login-manager --setup

# Start tray app
iitm-login-manager --tray

# Verbose output for debugging
iitm-login-manager --login --verbose
```

### Systemd Service Management

Enable and manage the systemd user service:

```bash
# Enable auto-start
systemctl --user enable iitm-login-manager.service

# Start the service
systemctl --user start iitm-login-manager.service

# Check service status
systemctl --user status iitm-login-manager.service

# View service logs
journalctl --user -u iitm-login-manager.service
```

## Troubleshooting

### Application doesn't start
- Make sure all GTK dependencies are installed
- Check if you're running a desktop environment with system tray support
- Try running from terminal to see error messages

### Login fails
- Verify your credentials using the command line: `iitm-login-manager --login --verbose`
- Check if you can access the IITM netaccess portal manually
- Ensure you're connected to IITM network

### No system tray icon
- Make sure your desktop environment supports system tray (most modern DEs do)
- Try installing `gnome-shell-extension-appindicator` on GNOME
- Check if the application is running: `pgrep -f iitm-login-tray`

### Permission errors
- Make sure you have write permissions to `~/.config/iitm-login-manager/`
- Check keyring permissions if password storage fails

## Development

### Running from source

```bash
cd iitm-login-manager
python -m iitm_login_manager.main --help
python -m iitm_login_manager.tray
```

### Building and installing

```bash
python setup.py sdist bdist_wheel
pip install dist/iitm-login-manager-1.0.0.tar.gz
```

## Security Implementation

- Passwords are stored securely using the system keyring (gnome-keyring, kwallet, etc.)
- No passwords are stored in plain text files
- All network communication uses HTTPS where possible
- Configuration files only contain non-sensitive information

## Contributing

1. Fork the repository on GitHub
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly on different desktop environments
5. Commit your changes (`git commit -am 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/iitm-login-manager.git
cd iitm-login-manager

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

## Technical Support

For technical issues and advanced troubleshooting:

1. Check the troubleshooting section above
2. Run with `--verbose` flag to see detailed output
3. Check system logs: `journalctl --user -u iitm-login-manager.service`
4. Review configuration files in `~/.config/iitm-login-manager/`
5. Create a detailed issue on the [GitHub repository](https://github.com/shrimansoft/iitm-login-manager/issues)

## Architecture

The application consists of:

- **Core Module** (`iitm_login_manager.main`): Handles login logic and credential management
- **Tray Application** (`iitm_login_manager.tray`): GTK-based system tray interface
- **Automator** (`iitm_login_manager.automator`): Scheduling and background tasks
- **Configuration**: Stored in `~/.config/iitm-login-manager/`
- **Credentials**: Securely stored in system keyring

## Changelog

### v1.0.0
- Initial release
- GTK system tray application
- Automated scheduling support
- Secure credential storage
- Desktop notifications
- Command line interface
- Systemd service integration
- Multi-desktop environment support
