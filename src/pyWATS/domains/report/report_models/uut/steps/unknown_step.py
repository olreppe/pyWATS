# Unknown Step - Fallback for unsupported step types

from typing import Any, Dict, Optional
from pydantic import Field

# Imports
from ..step import Step


class UnknownStep(Step):
    """
    Fallback step type for unrecognized or unsupported step types.
    
    This class handles step types that are not explicitly supported by pyWATS,
    preventing parsing failures when encountering unknown stepType values.
    It stores all unrecognized fields in extra_data for inspection.
    """
    # Accept any step_type string value for unknown types
    step_type: str = Field(..., validation_alias="stepType", serialization_alias="stepType")
    
    # Store any extra fields that aren't part of the base Step model
    extra_data: Dict[str, Any] = Field(default_factory=dict, exclude=True)
    
    model_config = {
        "extra": "allow",  # Allow extra fields for forward compatibility
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
    }
    
    def __init__(self, **data):
        """Capture unknown fields in extra_data"""
        # Extract known Step fields and keep others as extra_data
        extra = {}
        for key in list(data.keys()):
            # Check if this is a known field in Step or UnknownStep
            if key not in Step.model_fields and key not in ['step_type', 'stepType', 'extra_data']:
                extra[key] = data[key]
        
        if extra:
            data['extra_data'] = extra
        
        super().__init__(**data)
    
    def validate_step(self, trigger_children=False, errors=None) -> bool:
        """Validation always passes for unknown steps"""
        if not super().validate_step(trigger_children=trigger_children, errors=errors):
            return False
        return True
