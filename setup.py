#!/usr/bin/env python3
"""
Setup script for IITM Login Manager
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "IITM Login Manager - Automated login system for IIT Madras network access"

setup(
    name="iitm-login-manager",
    version="1.0.0",
    author="shriman keshri",
    author_email="shrimansoft@gmail.com",
    description="Automated login system for IIT Madras network access with GTK system tray",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "PyGObject>=3.40.0",
        "schedule>=1.1.0",
        "cryptography>=3.4.0",
        "keyring>=23.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "iitm-login-manager=iitm_login_manager.main:main",
            "iitm-login-tray=iitm_login_manager.tray:main",
        ],
    },
    data_files=[
        ("share/applications", ["data/iitm-login-manager.desktop"]),
        ("share/pixmaps", ["data/iitm-login-manager.png"]),
        ("share/icons/hicolor/48x48/apps", ["data/iitm-login-manager.png"]),
        ("etc/systemd/user", ["data/iitm-login-manager.service"]),
    ],
    include_package_data=True,
    zip_safe=False,
)