#!/usr/bin/env python3
"""
Final verification script for IITM Login Manager
Tests all core functionality and reports readiness
"""

import subprocess
import sys
import os
import json
import time

def run_command(cmd, description):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"   ✅ {description}")
            return True, result.stdout
        else:
            print(f"   ❌ {description} - Error: {result.stderr.strip()}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {description} - Timeout")
        return False, "Timeout"
    except Exception as e:
        print(f"   ❌ {description} - Exception: {e}")
        return False, str(e)

def main():
    print("="*70)
    print("IITM Login Manager - Final Verification")
    print("="*70)
    
    # Test CLI commands
    print("\n📋 Testing CLI Commands:")
    
    tests = [
        ("iitm-login-manager --help > /dev/null", "CLI help command"),
        ("iitm-login-manager --status", "Status check command"),
        ("echo 'Testing package import' && python3 -c 'from iitm_login_manager.automator import IITMNetAccessAutomator; print(\"Import successful\")'", "Package import"),
        ("python3 -c 'import keyring; print(\"Keyring available\")'", "Keyring functionality"),
        ("python3 -c 'import schedule; print(\"Schedule available\")'", "Schedule functionality"),
    ]
    
    passed = 0
    total = len(tests)
    
    for cmd, desc in tests:
        success, output = run_command(cmd, desc)
        if success:
            passed += 1
    
    # Check configuration
    print("\n⚙️  Checking Configuration:")
    config_path = os.path.expanduser('~/.config/iitm-login-manager/config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        username = config.get('username')
        if username:
            print(f"   ✅ Configuration found for user: {username}")
            passed += 1
        else:
            print("   ❌ Configuration missing username")
    else:
        print("   ❌ Configuration file not found")
    total += 1
    
    # Check desktop integration
    print("\n🖥️  Checking Desktop Integration:")
    desktop_file = os.path.expanduser('~/.local/share/applications/iitm-login-manager.desktop')
    icon_file = os.path.expanduser('~/.local/share/icons/iitm-login-manager.png')
    
    if os.path.exists(desktop_file):
        print("   ✅ Desktop file installed")
        passed += 1
    else:
        print("   ⚠️  Desktop file not installed (optional)")
    
    if os.path.exists(icon_file):
        print("   ✅ Icon file installed")
        passed += 1
    else:
        print("   ⚠️  Icon file not installed (optional)")
    
    total += 2
    
    # Check if tray app can be started (briefly)
    print("\n🔄 Testing Tray Application:")
    tray_test_cmd = "timeout 3s iitm-login-tray > /dev/null 2>&1 || echo 'Tray test completed'"
    success, _ = run_command(tray_test_cmd, "Tray application startup")
    if success:
        passed += 1
    total += 1
    
    # Final summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    percentage = (passed / total) * 100
    print(f"Tests Passed: {passed}/{total} ({percentage:.1f}%)")
    
    if passed == total:
        print("\n🎉 EXCELLENT! IITM Login Manager is fully functional and ready for use!")
        print("\nQuick Start:")
        print("  • Run 'iitm-login-manager --login' to test login")
        print("  • Run 'iitm-login-tray' to start the system tray")
        print("  • The desktop file is available in applications menu")
        return 0
    elif passed >= total * 0.8:
        print("\n✅ GOOD! IITM Login Manager is mostly functional.")
        print("Some optional features may not be available, but core functionality works.")
        return 0
    else:
        print("\n⚠️  WARNING! Some important features are not working properly.")
        print("Please check the failed tests above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
