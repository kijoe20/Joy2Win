#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import messagebox

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

def show_confirmation_dialog(title, message):
    """Show a confirmation dialog using tkinter"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    result = messagebox.askyesno(title, message)
    root.destroy()
    return result

def show_info_dialog(title, message):
    """Show an info dialog using tkinter"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo(title, message)
    root.destroy()

def main():
    print("🎮 Joy-Con 2 Windows - Starting GUI...")
    
    # Check OS (for testing purposes, we'll allow Linux but show a warning)
    if os.name != 'nt':
        print("⚠️  Warning: This application is designed for Windows.")
        print("   GUI can be viewed for demonstration, but Joy-Con connection")
        print("   requires Windows with vJoy driver installed.")
        print("")
        
        # Replace input() with GUI dialog
        if not show_confirmation_dialog(
            "Platform Warning", 
            "This application is designed for Windows.\n\n"
            "GUI can be viewed for demonstration, but Joy-Con connection "
            "requires Windows with vJoy driver installed.\n\n"
            "Continue anyway?"
        ):
            return
        
    # Check dependencies
    if not check_dependencies():
        show_info_dialog("Dependencies Missing", "Please install the missing dependencies and try again.")
        return
        
    # Import and run the GUI
    try:
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print("Make sure all files are in the same directory.")
        show_info_dialog("Import Error", f"Error importing GUI: {e}\n\nMake sure all files are in the same directory.")
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        show_info_dialog("Startup Error", f"Error starting GUI: {e}")

if __name__ == "__main__":
    main()
