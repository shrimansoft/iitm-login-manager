#!/usr/bin/env python3
"""
Test script for IITM Login Manager scheduling functionality
"""

import schedule
import time
import datetime
from iitm_login_manager.automator import IITMNetAccessAutomator

def test_login():
    """Test function that will be scheduled"""
    print(f"[{datetime.datetime.now()}] Scheduled login test executed!")
    automator = IITMNetAccessAutomator()
    return True

def test_scheduling():
    """Test the scheduling functionality"""
    print("Testing IITM Login Manager scheduling...")
    
    # Schedule a test run every minute (for quick testing)
    schedule.every(1).minutes.do(test_login)
    
    print("Scheduled job every 1 minute for testing purposes")
    print("Press Ctrl+C to stop the test")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping scheduler test...")

if __name__ == "__main__":
    test_scheduling()
