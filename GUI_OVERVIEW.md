# 🎮 Joy-Con 2 Windows - GUI Overview

## What's New

The Joy-Con 2 Windows project now includes a **modern, user-friendly graphical interface** that makes connecting and configuring your Nintendo Switch 2 Joy-Con controllers much easier than ever before!

## 🚀 Quick Start

### For New Users (Easiest Method)
1. **Double-click** `Start Joy-Con GUI.bat` in Windows Explorer
2. The application will automatically check dependencies and launch

### Alternative Methods
```bash
# Method 1: Using the launcher
python start_gui.py

# Method 2: Direct GUI launch
python gui.py
```

## 🎯 Key Features

### Easy Configuration
- **Visual dropdown menus** for controller type selection
- **Intuitive checkboxes** for features like DSU server and mouse mode
- **Real-time validation** of settings with helpful error messages
- **Automatic configuration saving** to `config.ini`

### Connection Management
- **One-click start/stop** connection controls
- **Real-time status display** with color-coded indicators:
  - 🔴 Disconnected (Red)
  - 🟡 Connecting... (Orange)
  - 🟢 Connected (Green)
- **Live log display** showing connection progress and debug information

### Built-in Tools
- **vJoy Test Function** - Check if vJoy is properly installed
- **Configuration Validation** - Ensures all settings are correct
- **Help System** - Built-in guides and documentation
- **Keyboard Shortcuts** for power users

## 📋 GUI Layout

### 1. Configuration Section
- **Controller Type**: Choose between Both Joy-Cons, Left only, or Right only
- **Orientation**: Vertical (recommended) or Horizontal for single Joy-Con
- **Player LED**: 4-bit binary pattern for LED indicators (e.g., "0001" = Player 1)
- **DSU Server**: Enable motion controls for compatible games
- **Mouse Mode**: Control mouse with Joy-Con (experimental)

### 2. Control Buttons
- **💾 Save Configuration**: Save current settings to config.ini
- **🚀 Start Joy-Con Connection**: Begin the connection process
- **🛑 Stop Connection**: Stop and disconnect controllers

### 3. Status Display
- **Connection Status**: Visual indicator of current state
- **Live Log**: Real-time messages and debug information
- **Scroll functionality**: Review past messages and errors

### 4. Quick Start Guide
- **Step-by-step instructions** visible in the interface
- **Tips and recommendations** for optimal setup
- **System requirements** clearly listed

## ⌨️ Keyboard Shortcuts

- **Ctrl+S**: Save Configuration
- **Ctrl+Q**: Exit Application
- **F5**: Start/Stop Connection
- **F1**: Show About Dialog

## 📖 Menu System

### File Menu
- **Load Configuration...**: Load settings from a custom file
- **Save Configuration**: Save current settings
- **Exit**: Close the application

### Tools Menu
- **Clear Log**: Clear the log display
- **Test vJoy Installation**: Verify vJoy is working correctly

### Help Menu
- **About**: Information about the application
- **vJoy Setup Guide**: Detailed installation instructions

## 🔧 Configuration Options Explained

### Controller Types
- **Both Joy-Cons (0)**: Use left and right Joy-Cons together as one controller
- **Left Joy-Con (1)**: Use only the left Joy-Con
- **Right Joy-Con (2)**: Use only the right Joy-Con

### Orientation
- **Vertical (0)**: Joy-Con held upright (recommended for most games)
- **Horizontal (1)**: Joy-Con held sideways (single Joy-Con only)

### Player LED Pattern
- Binary pattern controlling the 4 LEDs on the Joy-Con
- Examples:
  - `0001` = Player 1 (rightmost LED)
  - `0010` = Player 2 (second LED)
  - `0100` = Player 3 (third LED)
  - `1000` = Player 4 (leftmost LED)
  - `1111` = All LEDs on

### DSU Server
- Enables motion control support via DSU protocol
- Required for games that use gyroscope/accelerometer
- Still experimental - may not work with all games

### Mouse Mode
- **Disabled (0)**: Normal controller mode only
- **Automatic (1)**: Switch between controller and mouse mode
- **Always (2)**: Mouse-only mode (not recommended for dual Joy-Con)

## 🛠️ Troubleshooting

### Common Issues

#### "vJoy Test Failed"
1. Download vJoy from: https://sourceforge.net/projects/vjoystick/
2. Install with default settings
3. Open "Configure vJoy" from Start Menu
4. Enable Device #1 with 24+ buttons
5. Restart computer

#### "Connection Failed"
1. Check Bluetooth is enabled
2. Press sync button on Joy-Con when prompted
3. Ensure no other controller software is running
4. Run as Administrator if needed

#### "Python Dependencies Missing"
```bash
pip install bleak pyvjoy pynput
```

## 📁 File Structure

```
Joy2Win/
├── gui.py                  # Main GUI application
├── main_gui.py            # Modified core logic for GUI
├── start_gui.py           # GUI launcher with dependency checking
├── Start Joy-Con GUI.bat  # Windows batch launcher
├── main.py                # Original command-line interface
├── config.py              # Configuration management
├── config-example.ini     # Example configuration file
├── controller_command.py  # Joy-Con command interface
├── dsu_server.py          # DSU server for motion controls
├── control_type/          # Controller type implementations
├── controllers/           # Individual controller classes
└── README.md              # Main documentation
```

## 🎮 Usage Tips

1. **First Time Setup**:
   - Use the GUI to configure settings
   - Test vJoy installation using Tools menu
   - Save configuration before connecting

2. **Daily Use**:
   - Double-click the batch file to start
   - Press sync button when prompted
   - Monitor the log for any issues

3. **Advanced Users**:
   - Use keyboard shortcuts for faster operation
   - Customize config.ini directly if needed
   - Use command-line interface for automation

## 💡 Pro Tips

- **Vertical orientation** works best for most games
- **Player 1 LED** pattern is "0001"
- **Enable DSU** only if you need motion controls
- **Test vJoy** before first use to avoid issues
- **Keep the log visible** to monitor connection status

## 🔄 Migration from CLI

If you were using the command-line version:
1. Your existing `config.ini` will be automatically loaded
2. All settings transfer seamlessly
3. The GUI provides the same functionality with better usability
4. Command-line version still available as `main.py`

## 🆘 Support

If you encounter issues:
1. Check the log display in the GUI for error messages
2. Use the built-in vJoy test function
3. Refer to the vJoy Setup Guide in the Help menu
4. Ensure all dependencies are installed correctly

The GUI makes Joy-Con setup accessible to everyone while maintaining all the advanced features that power users need!