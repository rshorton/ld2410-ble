import asyncio
import logging

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

#from pathlib import Path
#import sys
#path_root = Path(__file__).parents[1]
#print("path: ", path_root)
#sys.path.append(str(path_root))
#print(sys.path)
#from src.ld2410_ble.ld2410_ble import LD2410BLE, LD2410BLEState

from ld2410_ble.ld2410_ble import LD2410BLE, LD2410BLEState

_LOGGER = logging.getLogger(__name__)

# Set the address of your device here.  To determine the address,
# set LIST_ALL_DISCOVERED_BLE_DEVICES=True
# and then look for a device with 'HLK-LD2410' in the listing.
ADDRESS = "1c:b9:65:02:01:94"
RUN_FOREVER = True
LIST_ALL_DISCOVERED_BLE_DEVICES = True

async def run() -> None:
    scanner = BleakScanner()
    future: asyncio.Future[BLEDevice] = asyncio.Future()

    def on_detected(device: BLEDevice, adv: AdvertisementData) -> None:
        if future.done():
            return
        if LIST_ALL_DISCOVERED_BLE_DEVICES:
            _LOGGER.info("Detected: %s, address: %s" % (device, device.address.lower()))
        if device.address.lower() == ADDRESS.lower():
            _LOGGER.info("Found device: %s", device.address)
            future.set_result(device)

    scanner.register_detection_callback(on_detected)
    await scanner.start()

    def on_state_changed(state: LD2410BLEState) -> None:
        #_LOGGER.info("State changed: %s", state)
        if state.is_moving:
           _LOGGER.info("                                   moving (%0.2f m)" % (state.moving_target_distance/100.0))
        if state.is_static:           
           _LOGGER.info("                 static (%0.2f m)" % (state.static_target_distance/100.0))
        if not state.is_moving and not state.is_static:
           _LOGGER.info("no detection")

    device = await future
    ld2410b = LD2410BLE(device)
    await ld2410b.initialise()

    _LOGGER.info("initial config:")
    _LOGGER.info("motion energy config: %s" % str(ld2410b.config_motion_energy_gates))
    _LOGGER.info("static energy config: %s" % str(ld2410b.config_static_energy_gates))

    # Set the configuration...
    await ld2410b.config_gate_sensitivity(0, 75, 50)    # gate, moving sensitivity, static sensitivity
    await ld2410b.config_gate_sensitivity(1, 75, 50)
    await ld2410b.config_gate_sensitivity(2, 50, 50)
    await ld2410b.config_gate_sensitivity(3, 30, 64)
    await ld2410b.config_gate_sensitivity(4, 15, 64)
    await ld2410b.config_gate_sensitivity(5, 15, 64)
    await ld2410b.config_gate_sensitivity(6, 15, 20)
    await ld2410b.config_gate_sensitivity(7, 15, 20)
    await ld2410b.config_gate_sensitivity(8, 15, 20)
    
    await ld2410b.config_max_gate_and_unmanned_timeout(4, 4, 5) # max moving gate, max static gate, unmanned timeout

    await ld2410b.read_config()

    _LOGGER.info("after configuring:")
    _LOGGER.info("motion energy config: %s" % str(ld2410b.config_motion_energy_gates))
    _LOGGER.info("static energy config: %s" % str(ld2410b.config_static_energy_gates))
    _LOGGER.info("max motion gate: %s" % str(ld2410b.config_max_motion_gates))
    _LOGGER.info("max static gate: %s" % str(ld2410b.config_max_static_gates))
    _LOGGER.info("unmanned timeout: %s sec" % str(ld2410b.config_unmanned_timeout))

    cancel_callback = ld2410b.register_callback(on_state_changed)
    await ld2410b.initialise()

    if RUN_FOREVER:
        while True:    
            await asyncio.sleep(10)
    else:
        await asyncio.sleep(10)        
    cancel_callback()
    await scanner.stop()


logging.basicConfig(level=logging.INFO)
logging.getLogger("ld2410_ble").setLevel(logging.INFO)
asyncio.run(run())
