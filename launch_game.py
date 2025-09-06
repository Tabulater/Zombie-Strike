#!/usr/bin/env python3
"""
Zombie Strike Game Launcher

This script provides a simple way to launch the Zombie Strike game.
It checks for required dependencies and provides helpful error messages.
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required to run this game.")
        print(f"Your Python version: {platform.python_version()}")
        print("Please download and install the latest Python version from https://www.python.org/downloads/")
        input("Press Enter to exit...")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import pygame
        return True
    except ImportError:
        print("Required package 'pygame' is not installed.")
        print("Installing dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.")
            input("Press Enter to exit...")
            return False

def main():
    """Main entry point for the launcher."""
    print("=== Zombie Strike Launcher ===")
    
    if not check_python_version():
        sys.exit(1)
        
    if not check_dependencies():
        sys.exit(1)
    
    # Launch the game
    try:
        print("Starting Zombie Strike...")
        import Tatipamula_Culminating
        sys.exit(0)
    except Exception as e:
        print(f"Error launching the game: {e}")
        print("Please make sure all game files are present and try again.")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
