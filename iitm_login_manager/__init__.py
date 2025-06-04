"""
IITM Login Manager
Automated login system for IIT Madras network access with optional GTK system tray
"""

__version__ = "1.0.0"
__author__ = "IITM Student"
__email__ = "your.email@example.com"

from .automator import IITMNetAccessAutomator, LoginStatus

# Try to import tray app, but don't fail if GTK is not available
try:
    from .tray import IITMTrayApp
    __all__ = ['IITMNetAccessAutomator', 'LoginStatus', 'IITMTrayApp']
except ImportError:
    __all__ = ['IITMNetAccessAutomator', 'LoginStatus']