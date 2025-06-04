# IITM Login Manager

A GTK-based system tray application for automated login to IIT Madras network access system. This tool provides a convenient way to manage your IITM network login with scheduled automation and desktop notifications.

## Features

- **System Tray Integration**: Shows login status with visual indicators in the system tray
- **Automated Scheduling**: Login automatically once or twice daily
- **Secure Credential Storage**: Passwords stored securely using system keyring
- **Desktop Notifications**: Get notified about login status and issues
- **Manual Login**: Trigger login manually when needed
- **Internet Status Checking**: Monitor your current internet connectivity
- **Auto-start Support**: Start automatically with your desktop session

## Installation

### APT Package Installation (Recommended)

Install using the standard Ubuntu package manager:

```bash
# Add repository and install
sudo apt update
sudo apt install iitm-login-manager
```

✅ **That's it!** The application is now installed system-wide and available in your applications menu.

### From Source

1. Clone or download this repository
2. Install the package using pip:

```bash
cd iitm-login-manager
pip install .
```

### Dependencies

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

## Usage

### Initial Setup

After installation, run the setup command to configure your credentials:

```bash
iitm-login-manager --setup
```

This will prompt you for your IITM username (LDAP ID) and password. The password will be stored securely in your system keyring.

### Starting the System Tray App

To start the system tray application:

```bash
iitm-login-tray
```

The app will appear in your system tray with a network icon that changes color based on connection status:
- **Blue**: Connected/Online
- **Gray**: Offline/Disconnected  
- **Yellow**: Connecting
- **Red**: Error

### Command Line Usage

You can also use the command line interface:

```bash
# Perform login now
iitm-login-manager --login

# Check internet status
iitm-login-manager --status

# Setup credentials
iitm-login-manager --setup

# Start tray app
iitm-login-manager --tray
```

### Configuration

Right-click on the system tray icon and select "Settings..." to configure:

- **Credentials**: Your IITM username and password
- **Schedule**: Choose between:
  - Once daily (8:00 AM)
  - Twice daily (8:00 AM & 8:00 PM)  
  - Manual only
- **Auto-start**: Start with desktop session

## Auto-start Setup

To make the application start automatically with your desktop session:

1. Right-click the tray icon → Settings
2. Check "Start with system"
3. Click OK

Alternatively, you can enable the systemd user service:

```bash
systemctl --user enable iitm-login-manager.service
systemctl --user start iitm-login-manager.service
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

## Security Notes

- Passwords are stored securely using the system keyring (gnome-keyring, kwallet, etc.)
- No passwords are stored in plain text files
- All network communication uses HTTPS where possible
- Configuration files only contain non-sensitive information

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly  
5. Submit a pull request

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run with `--verbose` flag to see detailed output
3. Check system logs: `journalctl --user -u iitm-login-manager.service`
4. Create an issue on the project repository

## Changelog

### v1.0.0
- Initial release
- GTK system tray application
- Automated scheduling support
- Secure credential storage
- Desktop notifications
- Command line interface