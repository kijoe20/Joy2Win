import asyncio, os
from bleak import BleakClient, BleakScanner
from config import Config
from controller_command import ControllerCommand, UUID_NOTIFY, UUID_CMD_RESPONSE
from dsu_server import main_dsu
import logging
import sys
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
# Check if the operating system is Windows
if (os.name != 'nt'):
    logger.error("This application is only supported on Windows.")
    sys.exit(1)
# Read the configuration from config.ini
config = Config().getConfig()
manufact = {
    "id": 0x0553,  # Nintendo Co., Ltd. (https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/)
    "data-prefix": bytes([0x01, 0x00, 0x03, 0x7e, 0x05])
  # Manufacturer data prefix for Joy-Con (I hope this prefix is correct, and it same for everyone)
}
clients = []  # List to hold connected clients
# Function to scan for controllers
async def scan_joycons():
    device_controller = None
    
    def callback(device, advertisement_data):
        nonlocal device_controller
        data = advertisement_data.manufacturer_data.get(manufact["id"])
        if not data:
            return
        if data.startswith(manufact["data-prefix"]):
            logger.info(f"Joy-Con found: {device.name} - {device.address}")
            device_controller = device
            
    logger.info("Scanning for available controllers...")
    scanner = BleakScanner(detection_callback=callback)
    await scanner.start()
    await asyncio.sleep(10)  # Scan for 10 seconds
    await scanner.stop()
    
    return device_controller

# Function to handle main game input loop
async def main_game_input(client, controllerName, orientation, config):
    controllerCommand = ControllerCommand()
    
    try:
        logger.info(f"Starting main game input loop for {controllerName} Joy-Con...")
        
        while client.is_connected:
            # Read sensor data
            try:
                response = await controllerCommand.send_command(client, "JOY2_GET_SENSOR_DATA")
                if response:
                    # Process the response data here
                    # This is where you would interpret the sensor data and send it to your DSU server
                    pass
            except Exception as e:
                logger.error(f"Error reading sensor data: {e}")
                break
            
            await asyncio.sleep(0.01)  # Small delay to prevent overwhelming the system
            
    except Exception as e:
        logger.error(f"Error in main game input loop: {e}")
    finally:
        logger.info(f"Main game input loop ended for {controllerName} Joy-Con")

# Function to initialize and connect to a controller
async def init_controller(controllerName, side, orientation, controller_type):
    device = await scan_joycons()
    
    if device:
        try:
            client = BleakClient(device.address)
            await client.connect()
            
            if client.is_connected:
                logger.info(f"Connected to {side} {controllerName}")
                clients.append(client)  # Add client to the list
                
                # Initialize controller commands
                await initSendControllerCmd(client, controllerName)
                
                # Start the main game input loop
                if side == "Left":
                    asyncio.create_task(main_game_input(client, "Left", orientation, config))
                else:
                    asyncio.create_task(main_game_input(client, "Right", orientation, config))
        else:
            logger.error("Failed to connect to controller.")
    else:
        logger.error("Controller not found.")

async def initSendControllerCmd(client, controllerName):
    controllerCommand = ControllerCommand()
    
    if(controllerName == "Joy-Con"):
        await controllerCommand.send_command(client, "JOY2_CONNECTED_VIBRATION")
        
        # Convert binary string (e.g., "0101") to hexadecimal string (e.g., "5")
        led_player = config['led_player']
        if len(led_player) != 4 or not all(c in '01' for c in led_player):
            logger.warning("LED player incorrectly set in config.ini, defaulting to 0001.")
            led_player = "0001"
        await controllerCommand.send_command(client, "JOY2_SET_PLAYER_LED", {"led_player": format(int(led_player, 2), 'x')})
        await controllerCommand.send_command(client, "JOY2_INIT_SENSOR_DATA")
        await controllerCommand.send_command(client, "JOY2_START_SENSOR_DATA")

async def main():
    try:
        orientation = config['orientation']
        if not (orientation == 0 or orientation == 1):
            logger.warning("Invalid orientation in config.ini. Please set 'orientation' to 0 (Vertical) or 1 (Horizontal).\nDefaulting to vertical.")
            orientation = 0  # Default to vertical if invalid
        
        if config['controller'] == 0:
            await init_controller("Joy-Con", "Left", orientation, 0)
            await init_controller("Joy-Con", "Right", orientation, 0)
        elif config['controller'] == 1:
            await init_controller("Joy-Con", "Left", orientation, 1)
        elif config['controller'] == 2:
            await init_controller("Joy-Con", "Right", orientation, 2)
        else:
            logger.warning("Invalid controller in config.ini. Please set 'controller' to 0, 1, or 2.\nDefaulting to both Joy-Cons.")
            await init_controller("Joy-Con", "Left", orientation, 0)
            await init_controller("Joy-Con", "Right", orientation, 0)
        
        if config['enable_dsu'] == True :
            main_dsu()
        
        logger.info("🟢 Connection established successfully! Your Joy-Con is now ready to use.")
        
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Interrupting...")
    finally:
        logger.info("Disconnecting controllers...")
        for client in clients:
            await client.disconnect()
        logger.info("All controllers disconnected.")

#Used to get the manufacturer data from joycons
#async def scan_all():
    #devices = await BleakScanner.discover()
    #for d in devices:
    #    md = d.metadata.get("manufacturer_data", {})
    #    if md:
    #        for manu_id, data_bytes in md.items():
    #            logger.info(f"Device: {d.name}, ID: {manu_id}, Data: {data_bytes.hex()}")

if __name__ == "__main__":
    asyncio.run(main())
