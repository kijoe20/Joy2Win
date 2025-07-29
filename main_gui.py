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
            if not device_controller:
                logger.info(f"Controller with address: {device.address} found.")
                device_controller = device

    scanner = BleakScanner(callback)
    await scanner.start()
    while True:
        if device_controller:
            break
        await asyncio.sleep(0.5)
    await scanner.stop()
    return device_controller

# Connect the controller and attribute to a notification handler
async def connect(device_controller):
    client = BleakClient(device_controller)
    try:
        await client.connect()
        if client.is_connected:
            return client
        else:
            logger.error("Failed to connect.")
            return None
    except Exception as e:
        logger.error(f"Connection error: {e}")
        return None

# Function to handle data
async def notification_handler(sender, data):
    logger.debug(f"Data from {sender}: {data.hex()}")

async def init_controller(controller_type, controller_mode, orientation, controller_config):
    device_controller = await scan_joycons()
    if device_controller:
        client = await connect(device_controller)
        if client:
            clients.append(client)  # Add client to the list
            await client.start_notify(UUID_NOTIFY, notification_handler)
            logger.info(f"{controller_type} {controller_mode} connected")
            await initSendControllerCmd(client, controller_type)
            from game_input import main_game_input  # Import here to avoid circular import
            if controller_config == 0:
                if controller_mode == "Left":
                    asyncio.create_task(main_game_input(client, "Left", orientation, config))
                else:
                    asyncio.create_task(main_game_input(client, "Right", orientation, config))
            else:
                if controller_config == 1:
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
        if(not config['orientation'] == 0 and not config['orientation'] == 1):
            logger.warning("Invalid orientation in config.ini. Please set 'orientation' to 0 (Vertical) or 1 (Horizontal).\nDefaulting to vertical.")
            config['orientation'] = 0  # Default to vertical if invalid
        
        if config['controller'] == 0:
            await init_controller("Joy-Con", "Left", config['orientation'], 0)
            await init_controller("Joy-Con", "Right", config['orientation'], 0)
        elif config['controller'] == 1:
            await init_controller("Joy-Con", "Left", config['orientation'], 1)
        elif config['controller'] == 2:
            await init_controller("Joy-Con", "Right", config['orientation'], 2)
        else:
            logger.warning("Invalid controller in config.ini. Please set 'controller' to 0, 1, or 2.\nDefaulting to both Joy-Cons.")
            await init_controller("Joy-Con", "Left", config['orientation'], 0)
            await init_controller("Joy-Con", "Right", config['orientation'], 0)
        
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
