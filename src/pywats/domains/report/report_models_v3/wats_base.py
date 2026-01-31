"""
WATS Base Model - v3 Implementation

Base class for all WATS report models with proper type annotations.
Fixes:
- Explicit typing for validation context access
- No type: ignore needed for context operations
"""
from __future__ import annotations

from typing import Any, Optional, Dict, ClassVar
from pydantic import BaseModel, ConfigDict, ValidationInfo, model_validator


class DeserializationContext:
    """Context for injecting default values during deserialization."""
    
    def __init__(self, defaults: Optional[Dict[str, Any]] = None) -> None:
        self.defaults: Dict[str, Any] = defaults or {}


class WATSBase(BaseModel):
    """
    Base class for all WATS Report Models.
    
    Provides:
    - Consistent model configuration across all models
    - Default value injection during deserialization
    - Proper handling of aliases, enums, and special float values
    """
    
    model_config = ConfigDict(
        populate_by_name=True,           # Allow both field name and alias
        arbitrary_types_allowed=True,     # Support custom types like StepList
        use_enum_values=True,            # Serialize enums as their values
        validate_default=True,           # Validate default values
        str_strip_whitespace=True,       # Strip whitespace from strings
        extra='ignore',                  # Ignore extra fields during parsing
        ser_json_inf_nan='strings',      # Serialize inf/nan as strings
    )
    
    @model_validator(mode="before")
    @classmethod
    def inject_defaults(cls, data: Any, info: ValidationInfo) -> Any:
        """
        Inject default values from deserialization context.
        
        Context can provide defaults like:
            {"UUTInfo.operator": "DefaultUser"}
        
        This allows setting defaults based on environment/configuration
        without hardcoding them in the model.
        """
        # Early return if data is not a dict (e.g., already a model instance)
        if not isinstance(data, dict):
            return data
            
        # Check if context is provided and has defaults
        context = info.context if info else None
        if context is None:
            return data
            
        # Support both DeserializationContext and plain dict
        defaults: Dict[str, Any] = {}
        if isinstance(context, DeserializationContext):
            defaults = context.defaults
        elif isinstance(context, dict) and 'defaults' in context:
            defaults = context.get('defaults', {})
        elif isinstance(context, dict):
            defaults = context
            
        if not defaults:
            return data
            
        # Apply defaults
        for key, value in defaults.items():
            if "." in key:
                # Scoped default: "UUTInfo.operator" only applies to UUTInfo class
                type_name, prop_name = key.split(".", 1)
                if type_name != cls.__name__:
                    continue
                    
                # Get the field's validation alias if it exists
                field_info = cls.model_fields.get(prop_name)
                alias = (
                    field_info.validation_alias
                    if field_info and field_info.validation_alias
                    else prop_name
                )
                
                # Only set if current value is None or empty
                if data.get(alias) in (None, ""):
                    data[alias] = value
            else:
                # Global default - applies to any class with that field
                if data.get(key) in (None, ""):
                    data[key] = value
                    
        return data
