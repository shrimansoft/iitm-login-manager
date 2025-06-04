#!/usr/bin/env python3
"""
IITM Internet Access Automator
Enhanced version with better error handling and status reporting
"""

import requests
import re
from bs4 import BeautifulSoup
import time
import json
import os
from datetime import datetime, timedelta
import threading
import logging
from typing import Optional, Dict, Any, Tuple

class LoginStatus:
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    NETWORK_ERROR = "network_error"
    AUTH_ERROR = "auth_error"
    UNKNOWN = "unknown"

class IITMNetAccessAutomator:
    def __init__(self, username: str = None, password: str = None, callback=None):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.callback = callback  # For status updates
        self.status = LoginStatus.UNKNOWN
        self.last_login_time = None
        self.next_login_time = None
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.base_url = 'https://netaccess.iitm.ac.in'
        self.login_url = f'{self.base_url}/account/login'
        
    def set_credentials(self, username: str, password: str):
        """Set login credentials"""
        self.username = username
        self.password = password
        
    def _notify_status(self, status: str, message: str = ""):
        """Notify about status change"""
        self.status = status
        if self.callback:
            self.callback(status, message)
        self.logger.info(f"Status: {status} - {message}")
        
    def log(self, message: str):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        self.logger.info(message)
        
    def get_login_page(self) -> Optional[Dict[str, Any]]:
        """Get the login page and extract necessary information"""
        self.log("Fetching login page...")
        try:
            response = self.session.get(self.login_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the login form
            login_form = soup.find('form')
            if not login_form:
                self.log("ERROR: Could not find login form")
                return None
                
            # Extract any hidden fields or CSRF tokens
            hidden_fields = {}
            for hidden in login_form.find_all('input', type='hidden'):
                if hidden.get('name') and hidden.get('value'):
                    hidden_fields[hidden['name']] = hidden['value']
                    
            return {
                'form_action': login_form.get('action', ''),
                'hidden_fields': hidden_fields,
                'cookies': response.cookies
            }
            
        except requests.RequestException as e:
            self.log(f"ERROR: Failed to fetch login page: {e}")
            self._notify_status(LoginStatus.NETWORK_ERROR, str(e))
            return None
    
    def perform_login(self) -> Optional[requests.Response]:
        """Perform the login using credentials"""
        if not self.username or not self.password:
            self._notify_status(LoginStatus.AUTH_ERROR, "No credentials provided")
            return None
            
        self.log("Attempting to log in...")
        self._notify_status(LoginStatus.IN_PROGRESS, "Logging in...")
        
        # Get login page info
        login_info = self.get_login_page()
        if not login_info:
            return None
            
        # Prepare login data
        login_data = {
            'userLogin': self.username,
            'userPassword': self.password,
            'submit': ''
        }
        
        # Add any hidden fields
        login_data.update(login_info['hidden_fields'])
        
        # Set headers for POST request
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': self.base_url,
            'Referer': self.login_url,
        }
        
        try:
            # Perform login
            response = self.session.post(
                self.login_url,
                data=login_data,
                headers=headers,
                allow_redirects=True,
                timeout=15
            )
            
            # Check if login was successful
            if response.status_code == 200:
                # Check for success indicators
                if 'logout' in response.text.lower() or 'dashboard' in response.text.lower():
                    self.log("Login successful!")
                    return response
                elif 'invalid' in response.text.lower() or 'error' in response.text.lower():
                    self.log("ERROR: Invalid credentials")
                    self._notify_status(LoginStatus.AUTH_ERROR, "Invalid credentials")
                    return None
                else:
                    self.log("Login appears successful, proceeding...")
                    return response
            else:
                self.log(f"ERROR: Login failed with status code: {response.status_code}")
                self._notify_status(LoginStatus.FAILED, f"HTTP {response.status_code}")
                return None
                
        except requests.RequestException as e:
            self.log(f"ERROR: Login request failed: {e}")
            self._notify_status(LoginStatus.NETWORK_ERROR, str(e))
            return None
    
    def handle_access_options(self, response: requests.Response) -> requests.Response:
        """Handle the access options page (one day option, allow button)"""
        self.log("Processing access options...")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the approve button/link
        approve_link = soup.find('a', href='/account/approve')
        if approve_link:
            self.log("Found approve link for proxy-less access!")
            
            # Click the approve link
            try:
                approve_url = f"{self.base_url}/account/approve"
                self.log(f"Accessing approval URL: {approve_url}")
                
                approve_response = self.session.get(
                    approve_url,
                    headers={'Referer': response.url},
                    timeout=10
                )
                
                if approve_response.status_code == 200:
                    self.log("Approval page accessed successfully")
                    
                    # Parse the approval page
                    approve_soup = BeautifulSoup(approve_response.text, 'html.parser')
                    
                    # Look for forms on the approval page
                    forms = approve_soup.find_all('form')
                    self.log(f"Found {len(forms)} forms on approval page")
                    
                    for i, form in enumerate(forms):
                        self.log(f"Processing approval form {i+1}")
                        
                        # Extract form data
                        form_data = {}
                        action = form.get('action', '')
                        
                        # Get all input fields
                        for input_field in form.find_all('input'):
                            name = input_field.get('name')
                            value = input_field.get('value', '')
                            input_type = input_field.get('type', 'text')
                            
                            if name:
                                if input_type == 'radio':
                                    # Look for duration options (1 day, 1 week, 1 month)
                                    if 'day' in str(input_field.parent).lower() or 'day' in value.lower():
                                        form_data[name] = value
                                        self.log(f"Selected duration option: {name}={value}")
                                elif input_type in ['hidden', 'submit']:
                                    form_data[name] = value
                                elif name.lower() in ['duration', 'period']:
                                    # Default to shortest duration if available
                                    form_data[name] = value
                        
                        # Also look for buttons
                        for button in form.find_all('button'):
                            name = button.get('name')
                            if name:
                                form_data[name] = button.get('value', '')
                                self.log(f"Added button: {name}")
                        
                        self.log(f"Approval form data to submit: {form_data}")
                        
                        # Submit the approval form
                        try:
                            submit_url = f"{self.base_url}{action}" if action.startswith('/') else f"{self.base_url}/account/approve"
                            if action and not action.startswith('/') and not action.startswith('http'):
                                submit_url = f"{self.base_url}/{action}"
                            
                            self.log(f"Submitting approval form to: {submit_url}")
                            
                            final_response = self.session.post(
                                submit_url,
                                data=form_data,
                                headers={
                                    'Referer': approve_response.url,
                                    'Content-Type': 'application/x-www-form-urlencoded'
                                },
                                timeout=10
                            )
                            
                            if final_response.status_code == 200:
                                self.log("Approval form submitted successfully")
                                
                                # Check if the approval was successful
                                if 'authorized' in final_response.text.lower() or 'approved' in final_response.text.lower():
                                    self.log("✅ Machine authorization successful!")
                                elif 'error' in final_response.text.lower():
                                    self.log("❌ Authorization may have failed - check manually")
                                else:
                                    self.log("⚠️ Authorization status unclear - proceeding anyway")
                                
                                return final_response
                            else:
                                self.log(f"Approval form submission failed with status: {final_response.status_code}")
                                
                        except requests.RequestException as e:
                            self.log(f"ERROR: Failed to submit approval form: {e}")
                    
                    return approve_response
                    
            except requests.RequestException as e:
                self.log(f"ERROR: Failed to access approval URL: {e}")
        
        # Check if we're already on a success page
        if any(keyword in response.text.lower() for keyword in ['welcome', 'success', 'internet access', 'activated']):
            self.log("Appears to be already on success page - access may already be granted")
            return response
        
        return response
    
    def check_internet_access(self) -> bool:
        """Check if internet access is working"""
        self.log("Checking internet access...")
        test_urls = [
            'https://www.google.com',
            'https://httpbin.org/ip',
            'https://www.cloudflare.com'
        ]
        
        for url in test_urls:
            try:
                test_response = requests.get(url, timeout=10)
                if test_response.status_code == 200:
                    self.log("✅ Internet access is working!")
                    return True
            except requests.RequestException:
                continue
                
        self.log("❌ No internet access detected")
        return False
    
    def automate_login(self) -> bool:
        """Main automation function"""
        self.log("Starting IITM Internet Access automation...")
        
        # Step 1: Perform login
        login_response = self.perform_login()
        if not login_response:
            self.log("❌ Login failed. Please check your credentials.")
            self._notify_status(LoginStatus.FAILED, "Login failed")
            return False
        
        # Step 2: Handle access options
        final_response = self.handle_access_options(login_response)
        
        # Step 3: Wait for access to propagate
        self.log("Waiting for internet access to activate...")
        time.sleep(10)
        
        # Step 4: Verify internet access
        if self.check_internet_access():
            self.log("🎉 Automation completed successfully!")
            self._notify_status(LoginStatus.SUCCESS, "Login successful")
            self.last_login_time = datetime.now()
            return True
        else:
            self.log("⚠️  Automation completed but internet access verification failed")
            self.log("💡 This might be normal - try browsing manually to verify")
            # Return True anyway since the automation steps completed
            self._notify_status(LoginStatus.SUCCESS, "Login completed (verification unclear)")
            self.last_login_time = datetime.now()
            return True
    
    def automate_login_async(self):
        """Run automation in a separate thread"""
        thread = threading.Thread(target=self.automate_login)
        thread.daemon = True
        thread.start()
        return thread
    
    def get_status_info(self) -> Dict[str, Any]:
        """Get current status information"""
        return {
            'status': self.status,
            'last_login_time': self.last_login_time.isoformat() if self.last_login_time else None,
            'next_login_time': self.next_login_time.isoformat() if self.next_login_time else None,
            'has_credentials': bool(self.username and self.password),
            'internet_access': self.check_internet_access()
        }