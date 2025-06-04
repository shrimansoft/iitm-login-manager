#!/usr/bin/env python3
"""
Simple test script for IITM Login Manager CLI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_cli():
    """Test the CLI functionality"""
    print("Testing IITM Login Manager CLI...")
    
    try:
        from iitm_login_manager.automator import IITMNetAccessAutomator, LoginStatus
        print("✅ Automator module loaded successfully")
        
        # Test automator creation
        automator = IITMNetAccessAutomator("test_user", "test_pass")
        print("✅ Automator instance created successfully")
        
        # Test status info
        status_info = automator.get_status_info()
        print(f"✅ Status info: {status_info}")
        
    except Exception as e:
        print(f"❌ Error testing automator: {e}")
        return False
    
    try:
        from iitm_login_manager.main import load_config, get_credentials
        print("✅ Main module functions loaded successfully")
        
        # Test config loading
        config = load_config()
        print(f"✅ Config loading works: {type(config)}")
        
    except Exception as e:
        print(f"❌ Error testing main module: {e}")
        return False
    
    print("✅ All CLI tests passed!")
    return True

if __name__ == "__main__":
    success = test_cli()
    sys.exit(0 if success else 1)
