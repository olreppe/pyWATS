"""Common models shared across modules
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import IntEnum


class ChangeType(IntEnum):
    """Change type for settings"""
    NONE = 0
    ADD = 1
    UPDATE = 2
    DELETE = 3
    # Additional values from API
    UNKNOWN_4 = 4
    UNKNOWN_5 = 5
    UNKNOWN_6 = 6


@dataclass
class Setting:
    """
    Key-value setting used for tags/custom data.
    Used in Products, ProductRevisions, Assets, and Units.
    """
    key: str
    value: str
    change: Optional[ChangeType] = None

    @classmethod
    def from_dict(cls, data: dict) -> "Setting":
        """Create Setting from API response dictionary"""
        return cls(
            key=data.get("key", ""),
            value=data.get("value", ""),
            change=ChangeType(data["change"]) if data.get("change") is not None else None
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        result: Dict[str, Any] = {
            "key": self.key,
            "value": self.value
        }
        if self.change is not None:
            result["change"] = self.change.value
        return result


@dataclass
class BaseModel:
    """Base class for all models with common functionality"""
    
    @classmethod
    def from_dict(cls, data: dict) -> "BaseModel":
        """Create model from API response dictionary - to be overridden"""
        raise NotImplementedError("Subclasses must implement from_dict")
    
    def to_dict(self) -> dict:
        """Convert model to dictionary for API requests - to be overridden"""
        raise NotImplementedError("Subclasses must implement to_dict")
