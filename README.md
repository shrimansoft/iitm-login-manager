# IITM Login Manager

A simple desktop app that automatically logs you into the IIT Madras internet network. No more manual login every time you connect to IITM WiFi!

## What does it do?

- 🔄 **Automatic Login**: Logs you into IITM network automatically
- 🕐 **Scheduled Login**: Can login once or twice daily at set times
- 🔔 **Notifications**: Shows you when login is successful or if there's a problem  
- 🖥️ **System Tray**: Lives quietly in your system tray with a simple icon
- 🔒 **Secure**: Your password is stored safely on your computer

## Easy Installation

Just copy and paste this command in your terminal:

```bash
curl -fsSL https://raw.githubusercontent.com/shrimansoft/iitm-login-manager/master/install-from-github.sh | bash
```

That's it! The app will be installed automatically. (The script will ask for your password when needed)

## How to Use

### Step 1: Set up your login details
After installation, open a terminal and type:
```bash
iitm-login-manager --setup
```
Enter your IITM username and password when asked.

You'll see a small network icon in your system tray (usually top-right corner of your screen).

### Step 3: Configure (optional)
Right-click on the tray icon and select "Settings" to:
- Choose when to auto-login (once daily, twice daily, or manual only)
- Enable auto-start with your computer


### Get More Help

- For detailed technical information, see [TECHNICAL_GUIDE.md](TECHNICAL_GUIDE.md)
- Report problems: [GitHub Issues](https://github.com/shrimansoft/iitm-login-manager/issues)

## License

Free to use under MIT License - see LICENSE file for details.