import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import asyncio
import threading
import sys
import os
from pathlib import Path
import configparser
from config import Config
import queue
import time
import logging
import io

class JoyConGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Joy-Con 2 Windows Compatibility")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # State variables
        self.is_running = False
        self.config_obj = None
        self.main_task = None
        self.log_queue = queue.Queue()
        self.log_handler = None
        
        # Create menu
        self.create_menu()
        
        # Create the UI
        self.create_widgets()
        self.load_config()
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
        
        # Start log monitoring
        self.check_log_queue()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎮 Joy-Con 2 Windows", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configuration Section
        config_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)
        
        # Controller Type
        ttk.Label(config_frame, text="Controller Type:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.controller_var = tk.StringVar()
        controller_combo = ttk.Combobox(config_frame, textvariable=self.controller_var, 
                                      values=["Both Joy-Cons (0)", "Left Joy-Con (1)", "Right Joy-Con (2)"],
                                      state="readonly", width=25)
        controller_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Orientation
        ttk.Label(config_frame, text="Orientation:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.orientation_var = tk.StringVar()
        orientation_combo = ttk.Combobox(config_frame, textvariable=self.orientation_var,
                                       values=["Vertical (0)", "Horizontal (1)"],
                                       state="readonly", width=25)
        orientation_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # LED Player
        ttk.Label(config_frame, text="Player LED:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.led_var = tk.StringVar()
        led_entry = ttk.Entry(config_frame, textvariable=self.led_var, width=25)
        led_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        ttk.Label(config_frame, text="(4-bit binary: 0000-1111)", font=("Arial", 8)).grid(row=2, column=2, sticky=tk.W, padx=(5, 0))
        
        # DSU Server
        self.dsu_var = tk.BooleanVar()
        dsu_check = ttk.Checkbutton(config_frame, text="Enable DSU Server (Motion Controls)", variable=self.dsu_var)
        dsu_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Mouse Mode
        ttk.Label(config_frame, text="Mouse Mode:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.mouse_var = tk.StringVar()
        mouse_combo = ttk.Combobox(config_frame, textvariable=self.mouse_var,
                                 values=["Disabled (0)", "Automatic (1)", "Always (2)"],
                                 state="readonly", width=25)
        mouse_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        
        # Auto Connect (future feature)
        self.auto_connect_var = tk.BooleanVar()
        auto_check = ttk.Checkbutton(config_frame, text="Auto Connect (Not implemented yet)", 
                                   variable=self.auto_connect_var, state="disabled")
        auto_check.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Save Config Button
        self.save_btn = ttk.Button(button_frame, text="💾 Save Configuration", command=self.save_config)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # Start/Stop Button
        self.start_btn = ttk.Button(button_frame, text="🚀 Start Joy-Con Connection", 
                                   command=self.toggle_connection, style="Accent.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="Connection Status", padding="10")
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(1, weight=1)
        
        # Status Label
        self.status_label = ttk.Label(status_frame, text="🔴 Disconnected", font=("Arial", 12, "bold"), foreground="red")
        self.status_label.grid(row=0, column=0, pady=(0, 10))
        
        # Log Display
        self.log_text = scrolledtext.ScrolledText(status_frame, height=15, width=70)
        self.log_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Instructions
        instructions_frame = ttk.LabelFrame(main_frame, text="Quick Start Guide", padding="10")
        instructions_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        instructions_text = """📋 Quick Setup:
1. Configure your Joy-Con settings above
2. Make sure vJoy is installed and configured (24+ buttons, Controller #1)
3. Click 'Save Configuration' to save your settings
4. Click 'Start Joy-Con Connection' to begin
5. When prompted, press the sync button on your Joy-Con(s)
6. Enjoy gaming with your Joy-Con on Windows!

💡 Tips:
• Use "Both Joy-Cons" for full controller experience
• "Vertical" orientation works best for most games
• Enable DSU server for motion controls in compatible games
• LED pattern "0001" = Player 1 (rightmost LED on)

⚠️ Requirements:
• Windows OS with administrator privileges
• vJoy driver installed and configured
• Bluetooth adapter for wireless connection"""
        
        instructions_label = ttk.Label(instructions_frame, text=instructions_text, justify=tk.LEFT, font=("Arial", 9))
        instructions_label.pack(anchor=tk.W)
        
        # Footer with links
        footer_frame = ttk.Frame(main_frame)
        footer_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        footer_text = "Made by Octokling • vJoy Download: sourceforge.net/projects/vjoystick"
        footer_label = ttk.Label(footer_frame, text=footer_text, font=("Arial", 8), foreground="gray")
        footer_label.pack()
        
        # Configure grid weights for resizing
        main_frame.rowconfigure(3, weight=1)
        
    def create_menu(self):
        """Create the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Configuration...", command=self.load_config_file)
        file_menu.add_command(label="Save Configuration", command=self.save_config, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Clear Log", command=self.clear_log)
        tools_menu.add_command(label="Test vJoy Installation", command=self.test_vjoy)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="vJoy Setup Guide", command=self.show_vjoy_guide)
        
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-s>', lambda e: self.save_config())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: self.toggle_connection())
        self.root.bind('<F1>', lambda e: self.show_about())
        
    def load_config_file(self):
        """Load configuration from a file dialog"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("INI files", "*.ini"), ("All files", "*.*")]
        )
        if filename:
            # TODO: Implement loading from custom file
            self.log_message(f"Loading configuration from {filename}")
            
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("Log cleared")
        
    def test_vjoy(self):
        """Test if vJoy is properly installed"""
        try:
            import pyvjoy
            # Try to create a vJoy device
            j = pyvjoy.VJoyDevice(1)
            if j:
                messagebox.showinfo("vJoy Test", "✅ vJoy is properly installed and accessible!")
                self.log_message("✅ vJoy test successful")
            else:
                messagebox.showerror("vJoy Test", "❌ vJoy device #1 is not available. Please check vJoy configuration.")
                self.log_message("❌ vJoy device #1 not available")
        except ImportError:
            messagebox.showerror("vJoy Test", "❌ pyvjoy module not found. Please install it with 'pip install pyvjoy'")
            self.log_message("❌ pyvjoy module not found")
        except Exception as e:
            messagebox.showerror("vJoy Test", f"❌ vJoy test failed: {e}")
            self.log_message(f"❌ vJoy test failed: {e}")
            
    def show_about(self):
        """Show about dialog"""
        about_text = """🎮 Joy-Con 2 Windows Compatibility Tool

Version: 1.0 with GUI
Author: Octokling

This tool allows you to connect Nintendo Switch 2 Joy-Con 
controllers to your Windows PC using Bluetooth and vJoy.

Features:
• Easy-to-use graphical interface
• Support for single or dual Joy-Con setups
• Motion controls via DSU server
• Customizable LED indicators
• Real-time connection monitoring

Requirements:
• Windows OS
• vJoy driver
• Bluetooth adapter
• Python dependencies: bleak, pyvjoy, pynput

For support and updates, visit the project repository."""
        
        messagebox.showinfo("About Joy-Con 2 Windows", about_text)
        
    def show_vjoy_guide(self):
        """Show vJoy setup guide"""
        guide_text = """📋 vJoy Setup Guide

1. Download vJoy from:
   https://sourceforge.net/projects/vjoystick/

2. Install vJoy with default settings

3. Open "Configure vJoy" from Start Menu

4. Configure Device #1:
   • Check "Enable vJoy"
   • Set "Number of Buttons" to 24 or higher
   • Configure axes as needed (X, Y, Z, RX, RY, RZ)
   • Click "Apply"

5. Restart your computer

6. Test the configuration using this tool's 
   "Test vJoy Installation" option

Common Issues:
• Run as Administrator if connection fails
• Ensure no other controller software is running
• Check Windows Device Manager for vJoy devices"""
        
        messagebox.showinfo("vJoy Setup Guide", guide_text)
        
    def load_config(self):
        """Load configuration from config.ini or use defaults"""
        try:
            self.config_obj = Config()
            config = self.config_obj.getConfig()
            
            # Set controller type
            controller_map = {0: "Both Joy-Cons (0)", 1: "Left Joy-Con (1)", 2: "Right Joy-Con (2)"}
            self.controller_var.set(controller_map.get(config['controller'], "Both Joy-Cons (0)"))
            
            # Set orientation
            orientation_map = {0: "Vertical (0)", 1: "Horizontal (1)"}
            self.orientation_var.set(orientation_map.get(config['orientation'], "Vertical (0)"))
            
            # Set LED player
            self.led_var.set(str(config['led_player']))
            
            # Set DSU
            self.dsu_var.set(config['enable_dsu'])
            
            # Set mouse mode
            mouse_map = {0: "Disabled (0)", 1: "Automatic (1)", 2: "Always (2)"}
            self.mouse_var.set(mouse_map.get(config['mouse_mode'], "Disabled (0)"))
            
            # Set auto connect
            self.auto_connect_var.set(config['auto_connect'])
            
            self.log_message("✅ Configuration loaded successfully")
            
        except Exception as e:
            self.log_message(f"⚠️ Error loading configuration: {e}")
            self.log_message("Using default values")
            
    def save_config(self):
        """Save current configuration to config.ini"""
        try:
            # Parse values from UI
            controller_value = int(self.controller_var.get().split('(')[1].split(')')[0])
            orientation_value = int(self.orientation_var.get().split('(')[1].split(')')[0])
            led_value = self.led_var.get().strip()
            dsu_value = 1 if self.dsu_var.get() else 0
            mouse_value = int(self.mouse_var.get().split('(')[1].split(')')[0])
            auto_connect_value = 1 if self.auto_connect_var.get() else 0
            
            # Validate LED value
            if len(led_value) != 4 or not all(c in '01' for c in led_value):
                messagebox.showerror("Invalid LED Value", 
                                   "LED player must be exactly 4 binary digits (0000-1111)")
                return
                
            # Create config content
            config_content = f"""[Controller]
# Controller usage type (0 = Left and Right Joycon, 1 = Left Joycon, 2 = Right Joycon)
# 0 = Both Joy-Cons
# 1 = Left Joy-Con
# 2 = Right Joy-Con
controller = {controller_value}

# Controller grip
# Adds buttons depending on the controller grip
# 0 = vertical, 1 = horizontal (Only single Joy-Con)
orientation = {orientation_value}

# Player LED indicator
# 0000 to 1111 in binary symbolizes four led lights
# 0 = Disabled, 1 = Enabled
led_player = {led_value}

# DSU Server (For motion controls)
# Not fully fonctional yet
# 0 = Disabled, 1 = Enabled
enable_dsu = {dsu_value}

# Automatically save computer mac address
# No need anymore to press the sync button on the Joy-Con, it connects automatically on startup
# 0 = Disabled, 1 = Enabled
# NOT IMPLEMENTED YET
auto_connect = {auto_connect_value}

# Emulate mouse with Joy-Con
# 0 = Disabled, 1 = Automatic (Switch between mouse and controller mode), 2 = Always (Mouse only (Not working on both Joy-Cons because is useless))
mouse_mode = {mouse_value}
"""
            
            # Write to config.ini
            with open('config.ini', 'w') as f:
                f.write(config_content)
                
            self.log_message("✅ Configuration saved to config.ini")
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except Exception as e:
            error_msg = f"❌ Error saving configuration: {e}"
            self.log_message(error_msg)
            messagebox.showerror("Error", error_msg)
            
    def toggle_connection(self):
        """Start or stop the Joy-Con connection"""
        if not self.is_running:
            self.start_connection()
        else:
            self.stop_connection()
            
    def start_connection(self):
        """Start the Joy-Con connection in a separate thread"""
        # Check if config.ini exists
        if not os.path.exists('config.ini'):
            response = messagebox.askyesno("No Configuration", 
                                         "config.ini not found. Save current configuration first?")
            if response:
                self.save_config()
            else:
                return
                
        self.is_running = True
        self.start_btn.config(text="🛑 Stop Connection")
        self.status_label.config(text="🟡 Connecting...", foreground="orange")
        self.log_message("🚀 Starting Joy-Con connection...")
        
        # Update window title
        self.root.title("🎮 Joy-Con 2 Windows - Connecting...")
        
        # Start the main function in a separate thread
        self.connection_thread = threading.Thread(target=self.run_main_async, daemon=True)
        self.connection_thread.start()
        
    def stop_connection(self):
        """Stop the Joy-Con connection"""
        self.is_running = False
        self.start_btn.config(text="🚀 Start Joy-Con Connection")
        self.status_label.config(text="🔴 Disconnected", foreground="red")
        self.log_message("🛑 Stopping Joy-Con connection...")
        
        # Update window title
        self.root.title("🎮 Joy-Con 2 Windows Compatibility")
        
        # Cancel the main task if it exists
        if self.main_task and not self.main_task.done():
            self.main_task.cancel()
            
    def run_main_async(self):
        """Run the main Joy-Con function asynchronously"""
        try:
            # Setup logging to capture messages
            self.setup_logging()
            
            # Import and run the main function
            from main_gui import main as main_joycon
            
            # Create new event loop for this thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the main function
            self.main_task = loop.create_task(main_joycon())
            loop.run_until_complete(self.main_task)
            
        except asyncio.CancelledError:
            self.log_message("Connection cancelled by user")
        except Exception as e:
            error_msg = f"❌ Connection error: {e}"
            self.log_message(error_msg)
        finally:
            # Cleanup logging
            self.cleanup_logging()
            
            if self.is_running:
                self.is_running = False
                # Update UI in main thread
                self.root.after(0, lambda: self.start_btn.config(text="🚀 Start Joy-Con Connection"))
                self.root.after(0, lambda: self.status_label.config(text="🔴 Disconnected"))
                
    def log_message(self, message):
        """Add a message to the log queue (thread-safe)"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_queue.put(f"[{timestamp}] {message}")
        
    def check_log_queue(self):
        """Check for new log messages and update the UI"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_log_queue)
        
    def setup_logging(self):
        """Setup logging to capture messages from the Joy-Con module"""
        class QueueHandler(logging.Handler):
            def __init__(self, log_queue, gui_instance):
                super().__init__()
                self.log_queue = log_queue
                self.gui = gui_instance
                
            def emit(self, record):
                msg = self.format(record)
                self.log_queue.put(f"[{time.strftime('%H:%M:%S')}] {msg}")
                
                # Update status based on log messages
                if "Connection established successfully" in msg:
                    self.gui.root.after(0, lambda: self.gui.status_label.config(text="🟢 Connected", foreground="green"))
                    self.gui.root.after(0, lambda: self.gui.root.title("🎮 Joy-Con 2 Windows - Connected"))
        
        # Create and configure the handler
        self.log_handler = QueueHandler(self.log_queue, self)
        self.log_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Add handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.INFO)
        
    def cleanup_logging(self):
        """Remove the logging handler"""
        if self.log_handler:
            root_logger = logging.getLogger()
            root_logger.removeHandler(self.log_handler)
            self.log_handler = None

def main():
    # Check if running on Windows (allow testing on other OS)
    if os.name != 'nt':
        print("⚠️  Warning: This application is designed for Windows.")
        print("   Running in demo mode for testing purposes.")
        # Don't return - allow GUI to start for demonstration
        
    root = tk.Tk()
    app = JoyConGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()