# Python library import
import asyncio
from netscud.device_selector import ConnectDevice

# from netscud.inventory import Inventory

__all__ = ("ConnectDevice",)

# Version
__version__ = "1.0.0"

# Supported devices
__supported_devices__ = [
    "alcatel_aos",
    "cisco_ios",
    "cisco_s300",
]
