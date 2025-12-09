"""Asset enumerations."""
from enum import IntEnum


class AssetState(IntEnum):
    """Asset state enumeration."""
    UNKNOWN = 0
    OK = 1
    WARNING = 2
    ALERT = 3
    NEEDS_MAINTENANCE = 4
    NEEDS_CALIBRATION = 5
    DISABLED = 6


class AssetLogType(IntEnum):
    """Asset log entry type."""
    UNKNOWN = 0
    CREATED = 1
    CALIBRATION = 2
    MAINTENANCE = 3
    STATE_CHANGE = 4
    COUNT_RESET = 5
    COMMENT = 6
