#!/usr/bin/env python3
"""
IITM Login Manager - GTK System Tray Application
"""

import gi

# Try to import GTK components with fallbacks
try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GObject, GLib
    GTK_AVAILABLE = True
except (ImportError, ValueError) as e:
    print(f"Warning: GTK not available: {e}")
    GTK_AVAILABLE = False
    # Create dummy classes for when GTK is not available
    class Gtk:
        class Dialog: pass
        class VBox: pass
        class HBox: pass
        class Label: pass
        class Entry: pass
        class Frame: pass
        class CheckButton: pass
        class RadioButton: pass
        class MenuItem: pass
        class Menu: pass
        class SeparatorMenuItem: pass
        class AboutDialog: pass
        class ResponseType:
            OK = 1
            CANCEL = 0
        STOCK_OK = "OK"
        STOCK_CANCEL = "Cancel"
        @staticmethod
        def main(): pass
        @staticmethod
        def main_quit(): pass
    
    class GLib:
        @staticmethod
        def idle_add(func): pass
        @staticmethod
        def timeout_add(interval, func): pass
    
    class GObject: pass

try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3
    APPINDICATOR_AVAILABLE = True
except (ImportError, ValueError) as e:
    print(f"Warning: AppIndicator3 not available: {e}")
    APPINDICATOR_AVAILABLE = False
    # Create dummy AppIndicator3
    class AppIndicator3:
        class Indicator:
            @staticmethod
            def new(*args): return AppIndicator3.Indicator()
            def set_status(self, *args): pass
            def set_icon(self, *args): pass
            def set_menu(self, *args): pass
        class IndicatorCategory:
            APPLICATION_STATUS = 1
        class IndicatorStatus:
            ACTIVE = 1

try:
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
    NOTIFY_AVAILABLE = True
except (ImportError, ValueError) as e:
    print(f"Warning: Notify not available: {e}")
    NOTIFY_AVAILABLE = False
    # Create dummy Notify
    class Notify:
        @staticmethod
        def init(*args): pass
        @staticmethod
        def uninit(): pass
        class Notification:
            @staticmethod
            def new(*args): return Notify.Notification()
            def set_urgency(self, *args): pass
            def show(self): pass
        class Urgency:
            CRITICAL = 1

import os
import sys
import json
import threading
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# Import required packages with error handling
try:
    import schedule
except ImportError:
    print("Warning: schedule package not available. Install with: pip install schedule")
    schedule = None

try:
    import keyring
except ImportError:
    print("Warning: keyring package not available. Install with: pip install keyring")
    keyring = None

from .automator import IITMNetAccessAutomator, LoginStatus

class SettingsDialog(Gtk.Dialog):
    def __init__(self, parent, current_username="", current_schedule="daily"):
        super().__init__(title="IITM Login Settings", parent=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        self.set_default_size(400, 300)
        self.set_border_width(10)
        
        # Main container
        vbox = Gtk.VBox(spacing=10)
        self.get_content_area().add(vbox)
        
        # Title
        title_label = Gtk.Label()
        title_label.set_markup("<b>IITM Login Manager Settings</b>")
        vbox.pack_start(title_label, False, False, 0)
        
        # Username section
        username_frame = Gtk.Frame(label="Credentials")
        username_frame.set_border_width(5)
        username_vbox = Gtk.VBox(spacing=5)
        username_frame.add(username_vbox)
        
        # Username
        username_hbox = Gtk.HBox(spacing=10)
        username_label = Gtk.Label("Username (LDAP ID):")
        username_label.set_size_request(150, -1)
        username_label.set_alignment(0, 0.5)
        self.username_entry = Gtk.Entry()
        self.username_entry.set_text(current_username)
        self.username_entry.set_placeholder_text("e.g., me24d900")
        username_hbox.pack_start(username_label, False, False, 0)
        username_hbox.pack_start(self.username_entry, True, True, 0)
        username_vbox.pack_start(username_hbox, False, False, 0)
        
        # Password
        password_hbox = Gtk.HBox(spacing=10)
        password_label = Gtk.Label("Password:")
        password_label.set_size_request(150, -1)
        password_label.set_alignment(0, 0.5)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)  # Hide password
        self.password_entry.set_placeholder_text("Enter your IITM password")
        password_hbox.pack_start(password_label, False, False, 0)
        password_hbox.pack_start(self.password_entry, True, True, 0)
        username_vbox.pack_start(password_hbox, False, False, 0)
        
        # Load existing password if available
        try:
            existing_password = keyring.get_password("iitm-login-manager", current_username)
            if existing_password:
                self.password_entry.set_text(existing_password)
        except:
            pass
        
        vbox.pack_start(username_frame, False, False, 0)
        
        # Schedule section
        schedule_frame = Gtk.Frame(label="Auto-Login Schedule")
        schedule_frame.set_border_width(5)
        schedule_vbox = Gtk.VBox(spacing=5)
        schedule_frame.add(schedule_vbox)
        
        # Schedule options
        self.schedule_radio_daily = Gtk.RadioButton.new_with_label_from_widget(None, "Once daily (8:00 AM)")
        self.schedule_radio_twice = Gtk.RadioButton.new_with_label_from_widget(self.schedule_radio_daily, "Twice daily (8:00 AM & 8:00 PM)")
        self.schedule_radio_manual = Gtk.RadioButton.new_with_label_from_widget(self.schedule_radio_daily, "Manual only")
        
        # Set current selection
        if current_schedule == "twice":
            self.schedule_radio_twice.set_active(True)
        elif current_schedule == "manual":
            self.schedule_radio_manual.set_active(True)
        else:
            self.schedule_radio_daily.set_active(True)
        
        schedule_vbox.pack_start(self.schedule_radio_daily, False, False, 0)
        schedule_vbox.pack_start(self.schedule_radio_twice, False, False, 0)
        schedule_vbox.pack_start(self.schedule_radio_manual, False, False, 0)
        
        vbox.pack_start(schedule_frame, False, False, 0)
        
        # Auto-start option
        autostart_frame = Gtk.Frame(label="Startup")
        autostart_frame.set_border_width(5)
        autostart_vbox = Gtk.VBox(spacing=5)
        autostart_frame.add(autostart_vbox)
        
        self.autostart_check = Gtk.CheckButton("Start with system")
        autostart_vbox.pack_start(self.autostart_check, False, False, 0)
        
        # Check if autostart is currently enabled
        autostart_file = os.path.expanduser("~/.config/autostart/iitm-login-manager.desktop")
        self.autostart_check.set_active(os.path.exists(autostart_file))
        
        vbox.pack_start(autostart_frame, False, False, 0)
        
        # Show all widgets
        self.show_all()
    
    def get_username(self):
        return self.username_entry.get_text().strip()
    
    def get_password(self):
        return self.password_entry.get_text()
    
    def get_schedule(self):
        if self.schedule_radio_twice.get_active():
            return "twice"
        elif self.schedule_radio_manual.get_active():
            return "manual"
        else:
            return "daily"
    
    def get_autostart(self):
        return self.autostart_check.get_active()

class IITMTrayApp:
    def __init__(self):
        # Initialize notifications
        Notify.init("IITM Login Manager")
        
        # Load configuration
        self.config_file = os.path.expanduser("~/.config/iitm-login-manager/config.json")
        self.config = self.load_config()
        
        # Initialize automator
        self.automator = IITMNetAccessAutomator(
            username=self.config.get('username'),
            password=self.get_password_from_keyring(),
            callback=self.on_status_change
        )
        
        # Status tracking
        self.current_status = LoginStatus.UNKNOWN
        self.last_status_message = ""
        
        # Create indicator
        self.indicator = AppIndicator3.Indicator.new(
            "iitm-login-manager",
            self.get_icon_path("offline"),
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        
        # Create menu
        self.create_menu()
        
        # Start scheduler
        self.setup_scheduler()
        self.start_scheduler_thread()
        
        # Initial status check
        GLib.timeout_add(2000, self.check_initial_status)
    
    def get_icon_path(self, status):
        """Get icon path based on status"""
        icons = {
            "online": "network-wireless",
            "offline": "network-offline", 
            "connecting": "network-wireless-acquiring",
            "error": "network-error"
        }
        return icons.get(status, "network-offline")
    
    def load_config(self):
        """Load configuration from file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
        
        # Return default config
        return {
            'username': '',
            'schedule': 'daily',
            'last_login': None,
            'autostart': False
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get_password_from_keyring(self):
        """Get password from system keyring"""
        username = self.config.get('username')
        if username:
            try:
                return keyring.get_password("iitm-login-manager", username)
            except Exception as e:
                print(f"Error getting password from keyring: {e}")
        return None
    
    def save_password_to_keyring(self, username, password):
        """Save password to system keyring"""
        try:
            keyring.set_password("iitm-login-manager", username, password)
            return True
        except Exception as e:
            print(f"Error saving password to keyring: {e}")
            return False
    
    def create_menu(self):
        """Create the system tray menu"""
        menu = Gtk.Menu()
        
        # Status item
        self.status_item = Gtk.MenuItem("Status: Unknown")
        self.status_item.set_sensitive(False)
        menu.append(self.status_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Login now
        login_item = Gtk.MenuItem("Login Now")
        login_item.connect("activate", self.on_login_now)
        menu.append(login_item)
        
        # Check status
        check_item = Gtk.MenuItem("Check Internet Status")
        check_item.connect("activate", self.on_check_status)
        menu.append(check_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Settings
        settings_item = Gtk.MenuItem("Settings...")
        settings_item.connect("activate", self.on_settings)
        menu.append(settings_item)
        
        # About
        about_item = Gtk.MenuItem("About")
        about_item.connect("activate", self.on_about)
        menu.append(about_item)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit
        quit_item = Gtk.MenuItem("Quit")
        quit_item.connect("activate", self.on_quit)
        menu.append(quit_item)
        
        menu.show_all()
        self.indicator.set_menu(menu)
    
    def on_status_change(self, status, message):
        """Handle status change from automator"""
        self.current_status = status
        self.last_status_message = message
        
        # Update UI in main thread
        GLib.idle_add(self.update_ui_status)
        
        # Show notification for important status changes
        if status == LoginStatus.SUCCESS:
            self.show_notification("Login Successful", "Internet access has been activated!")
        elif status == LoginStatus.FAILED:
            self.show_notification("Login Failed", f"Could not login: {message}", urgent=True)
        elif status == LoginStatus.AUTH_ERROR:
            self.show_notification("Authentication Error", "Please check your credentials", urgent=True)
    
    def update_ui_status(self):
        """Update UI elements based on current status"""
        status_text = {
            LoginStatus.SUCCESS: "Online",
            LoginStatus.FAILED: "Login Failed", 
            LoginStatus.IN_PROGRESS: "Connecting...",
            LoginStatus.NETWORK_ERROR: "Network Error",
            LoginStatus.AUTH_ERROR: "Auth Error",
            LoginStatus.UNKNOWN: "Unknown"
        }
        
        icon_status = {
            LoginStatus.SUCCESS: "online",
            LoginStatus.FAILED: "error",
            LoginStatus.IN_PROGRESS: "connecting", 
            LoginStatus.NETWORK_ERROR: "error",
            LoginStatus.AUTH_ERROR: "error",
            LoginStatus.UNKNOWN: "offline"
        }
        
        # Update status text
        status_msg = status_text.get(self.current_status, "Unknown")
        if self.last_status_message:
            status_msg += f" - {self.last_status_message}"
        
        self.status_item.set_label(f"Status: {status_msg}")
        
        # Update icon
        icon = icon_status.get(self.current_status, "offline")
        self.indicator.set_icon(self.get_icon_path(icon))
        
        return False  # Don't repeat this timeout
    
    def show_notification(self, title, message, urgent=False):
        """Show desktop notification"""
        try:
            notification = Notify.Notification.new(title, message, "dialog-information")
            if urgent:
                notification.set_urgency(Notify.Urgency.CRITICAL)
            notification.show()
        except Exception as e:
            print(f"Error showing notification: {e}")
    
    def on_login_now(self, widget):
        """Handle manual login request"""
        if not self.automator.username or not self.automator.password:
            self.show_notification("No Credentials", "Please configure username and password in Settings", urgent=True)
            return
        
        self.show_notification("Login Started", "Attempting to login...")
        self.automator.automate_login_async()
    
    def on_check_status(self, widget):
        """Check current internet status"""
        def check_in_thread():
            has_internet = self.automator.check_internet_access()
            status_msg = "Internet access is working!" if has_internet else "No internet access detected"
            GLib.idle_add(lambda: self.show_notification("Internet Status", status_msg))
        
        thread = threading.Thread(target=check_in_thread)
        thread.daemon = True
        thread.start()
    
    def on_settings(self, widget):
        """Show settings dialog"""
        dialog = SettingsDialog(
            None, 
            current_username=self.config.get('username', ''),
            current_schedule=self.config.get('schedule', 'daily')
        )
        
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Save settings
            new_username = dialog.get_username()
            new_password = dialog.get_password()
            new_schedule = dialog.get_schedule()
            new_autostart = dialog.get_autostart()
            
            # Update config
            self.config['username'] = new_username
            self.config['schedule'] = new_schedule
            self.config['autostart'] = new_autostart
            
            # Save password to keyring
            if new_username and new_password:
                self.save_password_to_keyring(new_username, new_password)
            
            # Update automator
            self.automator.set_credentials(new_username, new_password)
            
            # Save config
            self.save_config()
            
            # Update scheduler
            self.setup_scheduler()
            
            # Handle autostart
            self.setup_autostart(new_autostart)
            
            self.show_notification("Settings Saved", "Configuration has been updated")
        
        dialog.destroy()
    
    def setup_autostart(self, enable):
        """Setup/remove autostart desktop file"""
        autostart_dir = os.path.expanduser("~/.config/autostart")
        autostart_file = os.path.join(autostart_dir, "iitm-login-manager.desktop")
        
        if enable:
            # Create autostart directory
            os.makedirs(autostart_dir, exist_ok=True)
            
            # Create desktop file
            desktop_content = f"""[Desktop Entry]
Type=Application
Name=IITM Login Manager
Comment=Automated IITM network login
Exec={sys.executable} -m iitm_login_manager.tray
Icon=network-wireless
Terminal=false
NoDisplay=true
StartupNotify=false
X-GNOME-Autostart-enabled=true
"""
            try:
                with open(autostart_file, 'w') as f:
                    f.write(desktop_content)
                os.chmod(autostart_file, 0o755)
            except Exception as e:
                print(f"Error creating autostart file: {e}")
        else:
            # Remove autostart file
            try:
                if os.path.exists(autostart_file):
                    os.remove(autostart_file)
            except Exception as e:
                print(f"Error removing autostart file: {e}")
    
    def on_about(self, widget):
        """Show about dialog"""
        dialog = Gtk.AboutDialog()
        dialog.set_program_name("IITM Login Manager")
        dialog.set_version("1.0.0")
        dialog.set_comments("Automated login system for IIT Madras network access")
        dialog.set_website("https://github.com/your-repo/iitm-login-manager")
        dialog.set_authors(["IITM Student"])
        dialog.set_license_type(Gtk.License.MIT_X11)
        
        dialog.run()
        dialog.destroy()
    
    def on_quit(self, widget):
        """Quit the application"""
        Notify.uninit()
        Gtk.main_quit()
    
    def setup_scheduler(self):
        """Setup scheduled login tasks"""
        schedule.clear()
        
        schedule_type = self.config.get('schedule', 'daily')
        
        if schedule_type == 'daily':
            schedule.every().day.at("08:00").do(self.scheduled_login)
        elif schedule_type == 'twice':
            schedule.every().day.at("08:00").do(self.scheduled_login)
            schedule.every().day.at("20:00").do(self.scheduled_login)
        # 'manual' - no scheduled tasks
    
    def scheduled_login(self):
        """Perform scheduled login"""
        if self.automator.username and self.automator.password:
            print(f"Performing scheduled login at {datetime.now()}")
            self.automator.automate_login_async()
        else:
            print("Scheduled login skipped - no credentials configured")
    
    def start_scheduler_thread(self):
        """Start the scheduler in a background thread"""
        def scheduler_loop():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=scheduler_loop)
        scheduler_thread.daemon = True
        scheduler_thread.start()
    
    def check_initial_status(self):
        """Check initial internet status"""
        def check_in_thread():
            has_internet = self.automator.check_internet_access()
            if has_internet:
                GLib.idle_add(lambda: self.on_status_change(LoginStatus.SUCCESS, "Already connected"))
            else:
                GLib.idle_add(lambda: self.on_status_change(LoginStatus.UNKNOWN, "Not connected"))
        
        thread = threading.Thread(target=check_in_thread)
        thread.daemon = True
        thread.start()
        
        return False  # Don't repeat this timeout
    
    def run(self):
        """Start the GTK main loop"""
        try:
            Gtk.main()
        except KeyboardInterrupt:
            self.on_quit(None)

def main():
    """Main entry point"""
    app = IITMTrayApp()
    app.run()

if __name__ == "__main__":
    main()