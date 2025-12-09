"""Production domain enums."""
from enum import IntEnum


class SerialNumberIdentifier(IntEnum):
    """Serial number identifier type."""
    SERIAL_NUMBER = 0
    MAC_ADDRESS = 1
    IMEI = 2
