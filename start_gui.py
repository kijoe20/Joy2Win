#!/usr/bin/env python3
"""
Joy-Con 2 Windows - GUI Launcher
Simple launcher script for the Joy-Con GUI application
"""

import sys
import os

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import bleak
    except ImportError:
        missing_deps.append("bleak")
        
    try:
        import pyvjoy
    except ImportError:
        missing_deps.append("pyvjoy")
        
    try:
        import pynput
    except ImportError:
        missing_deps.append("pynput")
        
    if missing_deps:
        print("❌ Missing dependencies:")
        for dep in missing_deps:
            print(f"   - {dep}")
        print("\nPlease install them using:")
        print(f"   pip install {' '.join(missing_deps)}")
        print("\nAlso make sure vJoy is installed from:")
        print("   https://sourceforge.net/projects/vjoystick/")
        return False
        
    return True

def main():
    print("🎮 Joy-Con 2 Windows - Starting GUI...")
    
    # Check OS (for testing purposes, we'll allow Linux but show a warning)
    if os.name != 'nt':
        print("⚠️  Warning: This application is designed for Windows.")
        print("   GUI can be viewed for demonstration, but Joy-Con connection")
        print("   requires Windows with vJoy driver installed.")
        print("")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return
        
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return
        
    # Import and run the GUI
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print("Make sure all files are in the same directory.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()