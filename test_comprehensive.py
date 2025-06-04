#!/usr/bin/env python3
"""
Comprehensive test suite for IITM Login Manager
"""

import os
import sys
import json
import keyring
import requests
from iitm_login_manager.automator import IITMNetAccessAutomator

def test_config_loading():
    """Test configuration loading"""
    print("🧪 Testing configuration loading...")
    
    config_path = os.path.expanduser('~/.config/iitm-login-manager/config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        username = config.get('username')
        if username:
            print(f"   ✅ Username loaded: {username}")
            return username
        else:
            print("   ❌ Username not found in config")
            return None
    else:
        print("   ❌ Config file not found")
        return None

def test_keyring_access(username):
    """Test keyring password retrieval"""
    print("🧪 Testing keyring access...")
    
    if username:
        password = keyring.get_password('iitm-login-manager', username)
        if password:
            print(f"   ✅ Password retrieved (length: {len(password)})")
            return password
        else:
            print("   ❌ Password not found in keyring")
            return None
    else:
        print("   ❌ No username provided")
        return None

def test_internet_connectivity():
    """Test internet connectivity"""
    print("🧪 Testing internet connectivity...")
    
    try:
        response = requests.get('https://httpbin.org/status/200', timeout=10)
        if response.status_code == 200:
            print("   ✅ Internet connectivity working")
            return True
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Internet connectivity failed: {e}")
        return False

def test_automator_initialization():
    """Test automator initialization"""
    print("🧪 Testing automator initialization...")
    
    try:
        automator = IITMNetAccessAutomator()
        print("   ✅ Automator initialized successfully")
        return automator
    except Exception as e:
        print(f"   ❌ Automator initialization failed: {e}")
        return None

def test_dependencies():
    """Test required dependencies"""
    print("🧪 Testing dependencies...")
    
    dependencies = {
        'requests': 'HTTP library',
        'schedule': 'Job scheduling',
        'keyring': 'Secure credential storage',
        'configparser': 'Configuration management',
        'json': 'JSON handling',
        'threading': 'Multi-threading support'
    }
    
    failed_deps = []
    for dep, desc in dependencies.items():
        try:
            __import__(dep)
            print(f"   ✅ {dep} ({desc})")
        except ImportError:
            print(f"   ❌ {dep} ({desc}) - MISSING")
            failed_deps.append(dep)
    
    return len(failed_deps) == 0

def main():
    """Run comprehensive tests"""
    print("="*60)
    print("IITM Login Manager - Comprehensive Test Suite")
    print("="*60)
    
    # Test results
    results = {}
    
    # Test dependencies
    results['dependencies'] = test_dependencies()
    
    # Test configuration
    username = test_config_loading()
    results['config'] = username is not None
    
    # Test keyring
    password = test_keyring_access(username) if username else None
    results['keyring'] = password is not None
    
    # Test internet
    results['internet'] = test_internet_connectivity()
    
    # Test automator
    automator = test_automator_initialization()
    results['automator'] = automator is not None
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.upper():>15}: {status}")
    
    print("-" * 60)
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! IITM Login Manager is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
