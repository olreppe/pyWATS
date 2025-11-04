"""
Process models for WATS operations.

This module defines the Process class hierarchy for TestOperations, RepairOperations,
and WIP Operations.
"""

from typing import Dict, Any, Union, Optional, List
from enum import Enum
from pydantic import BaseModel, Field


class ProcessState(Enum):
    """Process state enumeration."""
    INACTIVE = 0
    ACTIVE = 1
    DISABLED = 2


class ProcessType(Enum):
    """Process type enumeration."""
    TEST = "test"
    REPAIR = "repair" 
    WIP = "wip"


class Process(BaseModel):
    """
    Base process class representing any WATS process.
    
    A Process can be a TestOperation, RepairOperation, or WIP Operation.
    """
    name: str = Field(..., description="Process name")
    code: int = Field(..., description="Unique process code")
    description: str = Field(default="", description="Process description")
    is_test_operation: bool = Field(alias="isTestOperation", default=False)
    is_repair_operation: bool = Field(alias="isRepairOperation", default=False)
    is_wip_operation: bool = Field(alias="isWipOperation", default=False)
    process_index: int = Field(alias="processIndex", default=0)
    state: int = Field(default=1, description="Process state (0=Inactive, 1=Active, 2=Disabled)")
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
    
    @property
    def process_state(self) -> ProcessState:
        """Get process state as enum."""
        return ProcessState(self.state)
    
    @property
    def process_types(self) -> List[ProcessType]:
        """Get list of process types this process belongs to."""
        types = []
        if self.is_test_operation:
            types.append(ProcessType.TEST)
        if self.is_repair_operation:
            types.append(ProcessType.REPAIR)
        if self.is_wip_operation:
            types.append(ProcessType.WIP)
        return types
    
    @property
    def is_active(self) -> bool:
        """Check if process is active."""
        return self.process_state == ProcessState.ACTIVE
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'Process':
        """Create Process from API response data."""
        return cls(**data)
    
    def __str__(self) -> str:
        types = ", ".join([t.value for t in self.process_types])
        return f"{self.name} (code: {self.code}, types: {types})"
    
    def __repr__(self) -> str:
        return f"Process(name='{self.name}', code={self.code}, types={self.process_types})"


class TestOperation(Process):
    """Test operation process."""
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.is_test_operation:
            raise ValueError("TestOperation must have is_test_operation=True")


class RepairOperation(Process):
    """Repair operation process."""
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.is_repair_operation:
            raise ValueError("RepairOperation must have is_repair_operation=True")


class WIPOperation(Process):
    """Work In Progress operation process."""
    
    def __init__(self, **data):
        super().__init__(**data)
        if not self.is_wip_operation:
            raise ValueError("WIPOperation must have is_wip_operation=True")


# Union type for all process types
ProcessUnion = Union[TestOperation, RepairOperation, WIPOperation, Process]
