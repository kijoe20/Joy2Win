# 🎮 Joy-Con 2 Windows Compatibility

This project allows you to connect your **Nintendo Switch 2 Joy-Con** controllers to a Windows PC using Bluetooth and vJoy, now featuring an **easy-to-use graphical interface**!

## 🖼️ Screenshot
![GUI Interface](screenshot-placeholder.png)
*The new GUI makes configuration and connection management simple and intuitive*

---

## 🚀 Installation

1. Clone this repository :
   ```bash
   git clone https://github.com/Logan-Gaillard/Joy2Win.git
   cd Joy2Win
   ```

2. Install Python dependencies:
    ```bash
    pip install bleak pyvjoy pynput
    ```

3. Install vJoy driver:
    - Download from: https://sourceforge.net/projects/vjoystick/
    - Install with default settings

4. Configure vJoy:
    - Open "Configure vJoy" from Start Menu
    - Select Device #1
    - Check "Enable vJoy"  
    - Set "Number of Buttons" to 24 or higher
    - Configure axes (X, Y, Z, RX, RY, RZ) as needed
    - Click "Apply"
    - Restart your computer

5. **Easy Start**: Double-click `Start Joy-Con GUI.bat` or run:
    ```bash
    python start_gui.py
    ```  

## 🕹️ Usage

### Option 1: GUI Interface (Recommended for beginners)

1. Launch the GUI application:
    ```bash
    python start_gui.py
    ```
    or
    ```bash
    python gui.py
    ```

2. Configure your settings in the GUI:
   - Select controller type (Both Joy-Cons, Left only, or Right only)
   - Choose orientation (Vertical or Horizontal)
   - Set LED player indicator
   - Enable/disable features like DSU server and mouse mode

3. Click "Save Configuration" to save your settings

4. Click "Start Joy-Con Connection" to begin

5. When prompted, press the sync button on your Joy-Con(s)

6. Enjoy gaming with your Joy-Con on Windows!

### Option 2: Command Line Interface

1. Copy the `config-exemple.ini` file, rename it to `config.ini`, and edit it according to your needs.

2. Run the script :
    ```bash
    python main.py
    ```

3. Follow the instructions displayed when the script starts.

Your Joy-Con 2 will be compatible with your Windows.

## ✨ Features

- **Easy-to-use GUI interface** with visual configuration options
- **Command-line interface** for advanced users
- Select usage type and Joy-Con orientation (single or paired, horizontal or vertical (only for single joycon))
- Player LED indicator support (By default, player 1)
- Vibration feedback when Joy-Con is successfully connected
- **Real-time connection status** and logging in GUI
- **Automatic configuration validation** and error checking
- **Live configuration editor** with instant feedback

## Repositories
- [pyvjoy](https://github.com/tidzo/pyvjoy)
- [switch2_controller_research](https://github.com/ndeadly/switch2_controller_research)

## Author
Made by **Octokling**

Helped by :  
- narr_the_reg
- ndeadly