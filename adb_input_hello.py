import os
import time
from adb_shell.adb_device import AdbDevice
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.transport.usb_transport import UsbTransport

# Expand the path to the user's home directory
adb_key_path = os.path.expanduser('~/.android/adbkey')

# Load the ADB key
with open(adb_key_path, 'rb') as f:
    priv = f.read()
signer = PythonRSASigner.FromString(priv)

# Find the connected devices
devices = UsbTransport.find_adb_devices()

if len(devices) == 1:
    transport = devices[0]
    device = AdbDevice(transport, signer)
    device.connect()

    # Send the message "Hello" with a 5 ms break between each character
    message = "Hello"
    for char in message:
        device.shell(f'input text {char}')
        time.sleep(0.005)  # 5 ms break

    # Disconnect from the device
    device.disconnect()

else:
    print(f"Expected 1 device, found {len(devices)} devices.")