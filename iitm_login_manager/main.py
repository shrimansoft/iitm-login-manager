#!/usr/bin/env python3
"""
IITM Login Manager - Main CLI Interface
"""

import argparse
import sys
import os
from datetime import datetime
from .automator import IITMNetAccessAutomator, LoginStatus
import keyring
import json

def load_config():
    """Load configuration from file"""
    config_file = os.path.expanduser("~/.config/iitm-login-manager/config.json")
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load config: {e}")
    return {}

def get_credentials():
    """Get credentials from config and keyring"""
    config = load_config()
    username = config.get('username')
    
    if username:
        try:
            password = keyring.get_password("iitm-login-manager", username)
            if password:
                return username, password
        except Exception as e:
            print(f"Warning: Could not get password from keyring: {e}")
    
    return None, None

def setup_credentials():
    """Interactive setup of credentials"""
    print("Setting up IITM Login Manager credentials...")
    
    username = input("Enter your IITM username (LDAP ID): ").strip()
    if not username:
        print("Error: Username cannot be empty")
        return False
    
    import getpass
    password = getpass.getpass("Enter your password: ")
    if not password:
        print("Error: Password cannot be empty")
        return False
    
    # Save to keyring
    try:
        keyring.set_password("iitm-login-manager", username, password)
        print("✅ Password saved securely to system keyring")
    except Exception as e:
        print(f"Warning: Could not save password to keyring: {e}")
        return False
    
    # Save username to config
    config_file = os.path.expanduser("~/.config/iitm-login-manager/config.json")
    config = load_config()
    config['username'] = username
    
    try:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration saved")
    except Exception as e:
        print(f"Warning: Could not save config: {e}")
    
    return True

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="IITM Login Manager - Automated network login for IIT Madras",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  iitm-login-manager --login          # Perform login now
  iitm-login-manager --status         # Check internet status
  iitm-login-manager --setup          # Setup credentials
  iitm-login-manager --tray           # Start system tray app
        """
    )
    
    parser.add_argument('--login', action='store_true', 
                       help='Perform login now')
    parser.add_argument('--status', action='store_true',
                       help='Check current internet status')
    parser.add_argument('--setup', action='store_true',
                       help='Setup credentials interactively')
    parser.add_argument('--tray', action='store_true',
                       help='Start system tray application')
    parser.add_argument('--username', type=str,
                       help='Username for login (if not using saved credentials)')
    parser.add_argument('--password', type=str,
                       help='Password for login (if not using saved credentials)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # If no arguments, show help
    if not any([args.login, args.status, args.setup, args.tray]):
        parser.print_help()
        return 1
    
    # Setup credentials
    if args.setup:
        if setup_credentials():
            print("✅ Setup completed successfully!")
            return 0
        else:
            print("❌ Setup failed")
            return 1
    
    # Start tray application
    if args.tray:
        try:
            # Check if GTK is available
            import gi
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            
            from .tray import main as tray_main
            tray_main()
            return 0
        except ImportError as e:
            print(f"Error: Could not start tray application: {e}")
            print("GTK and related dependencies are required for the tray application.")
            print("Install them with:")
            print("  Ubuntu/Debian: sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 gir1.2-notify-0.7")
            print("  Fedora: sudo dnf install python3-gobject gtk3-devel libappindicator-gtk3-devel libnotify-devel")
            print("  Arch: sudo pacman -S python-gobject gtk3 libappindicator-gtk3 libnotify")
            return 1
        except Exception as e:
            print(f"Error starting tray application: {e}")
            return 1
        except KeyboardInterrupt:
            print("\nExiting...")
            return 0
    
    # Get credentials
    if args.username and args.password:
        username, password = args.username, args.password
    else:
        username, password = get_credentials()
        
        if not username or not password:
            print("❌ No credentials found. Run with --setup to configure credentials")
            return 1
    
    # Create automator
    def status_callback(status, message):
        if args.verbose:
            print(f"Status: {status} - {message}")
    
    automator = IITMNetAccessAutomator(username, password, callback=status_callback)
    
    # Check status
    if args.status:
        print("Checking internet status...")
        has_internet = automator.check_internet_access()
        
        if has_internet:
            print("✅ Internet access is working!")
            return 0
        else:
            print("❌ No internet access detected")
            return 1
    
    # Perform login
    if args.login:
        print(f"Starting login process for user: {username}")
        success = automator.automate_login()
        
        if success:
            print("✅ Login completed successfully!")
            return 0
        else:
            print("❌ Login failed")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
