"""
UUTReport v2 - Composition-based UUT (Unit Under Test) report

Key differences from v1:
- Uses composition (ReportCommon) instead of inheritance (Report)
- Imports Step hierarchy from v1 (already perfect with discriminated union!)
- Clean type signature (no field overrides)
- 100% JSON compatible with v1

Design notes:
- Parent injection handled by StepList (from v1) - unchanged
- Step hierarchy imported from v1 - DO NOT COPY!
- Supports both constructor and factory patterns
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

# Import ReportCommon (composition)
from .report_common import ReportCommon

# Import from v1 (stable models - relative imports)
from ..report_models.uut.uut_info import UUTInfo
from ..report_models.uut.steps.sequence_call import SequenceCall

# Import base class
from ..report_models.wats_base import WATSBase


class UUTReport(WATSBase):
    """
    UUT (Unit Under Test) Report - Composition-based v2
    
    This replaces the inheritance-based v1 UUTReport with a composition pattern.
    
    Key fields:
    - common: ReportCommon (all shared fields)
    - type: Literal["T"] (UUT type identifier)
    - root: SequenceCall (test steps hierarchy)
    - info: UUTInfo (UUT-specific metadata)
    
    The Step hierarchy (SequenceCall, NumericStep, StringStep, etc.) is imported
    from v1 and works unchanged. Parent injection happens via StepList.append()
    when steps are added.
    
    Example usage:
    
    Constructor pattern:
        report = UUTReport(
            common=ReportCommon(
                pn="ABC123",
                sn="SN-001",
                rev="A",
                process_code=100,
                station_name="Station1",
                location="TestLab",
                purpose="Development"
            )
        )
        
    Or with unpacked fields (delegated to common):
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
    
    Adding steps:
        root = report.get_root_sequence_call()
        root.add_numeric_step(name="Voltage", value=3.3, unit="V")
    """
    
    # =========================================================================
    # Core Fields
    # =========================================================================
    
    common: ReportCommon = Field(
        default_factory=ReportCommon,
        description="Shared fields for all report types (composition pattern)"
    )
    
    type: Literal["T"] = Field(
        default="T",
        description="Report type: 'T' = Test Report (UUT)"
    )
    
    root: SequenceCall = Field(
        default_factory=SequenceCall,
        description="Root sequence call containing all test steps"
    )
    
    info: UUTInfo | None = Field(
        default=None,
        validation_alias="uut",
        serialization_alias="uut",
        description="UUT-specific metadata (serializes as 'uut' in JSON)"
    )
    
    # =========================================================================
    # Methods
    # =========================================================================
    
    def get_root_sequence_call(self) -> SequenceCall:
        """
        Get the root sequence call for adding test steps.
        
        This is the primary way to add test steps to a UUT report.
        The root sequence acts as the container for all test steps.
        
        Returns:
            SequenceCall: The root sequence where steps can be added
            
        Example:
            root = report.get_root_sequence_call()
            root.add_numeric_step(name="Voltage", value=3.3, unit="V")
            root.add_sequence_call(name="SubTest")
        """
        self.root.name = "MainSequence Callback"
        return self.root
    
    # =========================================================================
    # Factory Method for Convenience
    # =========================================================================
    
    @classmethod
    def create(
        cls,
        pn: str,
        sn: str,
        rev: str,
        process_code: int,
        station_name: str,
        location: str,
        purpose: str,
        **kwargs
    ) -> 'UUTReport':
        """
        Factory method for creating UUTReport with unpacked fields.
        
        This provides a convenient alternative to creating ReportCommon explicitly.
        All common fields are passed through to ReportCommon.
        
        Args:
            pn: Part number
            sn: Serial number
            rev: Revision
            process_code: Process code
            station_name: Station/machine name
            location: Location
            purpose: Purpose
            **kwargs: Additional fields for ReportCommon
            
        Returns:
            UUTReport: New UUT report instance
            
        Example:
            report = UUTReport.create(
                pn="ABC123",
                sn="SN-001",
                rev="A",
                process_code=100,
                station_name="Station1",
                location="TestLab",
                purpose="Development"
            )
        """
        common = ReportCommon(
            pn=pn,
            sn=sn,
            rev=rev,
            process_code=process_code,
            station_name=station_name,
            location=location,
            purpose=purpose,
            **kwargs
        )
        return cls(common=common)
    
    # =========================================================================
    # Serialization Customization
    # =========================================================================
    
    def model_dump(self, **kwargs):
        """
        Override serialization to flatten common fields to top level.
        
        This ensures JSON output matches v1 structure:
        {
            "id": "...",
            "type": "T",
            "pn": "...",
            "sn": "...",
            ...
            "root": {...},
            "uut": {...}
        }
        
        Instead of nested:
        {
            "common": {"pn": "...", ...},
            "type": "T",
            ...
        }
        """
        # Get base serialization
        data = super().model_dump(**kwargs)
        
        # Flatten common fields to top level
        if 'common' in data:
            common_data = data.pop('common')
            # Merge common fields into top level (common fields first, then specific)
            data = {**common_data, **data}
        
        return data
    
    def model_dump_json(self, **kwargs):
        """
        Override JSON serialization to flatten common fields.
        
        Uses model_dump() which handles flattening, then serializes to JSON.
        """
        import json
        from pydantic.json import pydantic_encoder
        
        data = self.model_dump(**kwargs)
        return json.dumps(data, default=pydantic_encoder)
    
    @classmethod
    def model_validate(cls, obj, **kwargs):
        """
        Override deserialization to handle both flattened and nested formats.
        
        Accepts both formats:
        1. Flattened (v1 compatible): {"pn": "...", "sn": "...", "type": "T", ...}
        2. Nested (v2 explicit): {"common": {"pn": "...", ...}, "type": "T", ...}
        """
        if isinstance(obj, dict):
            # If 'common' key exists, use as-is (already nested)
            if 'common' in obj:
                return super().model_validate(obj, **kwargs)
            
            # Otherwise, extract common fields from top level
            common_field_names = {
                'id', 'pn', 'sn', 'rev', 'process_code', 'processCode',
                'result', 'station_name', 'machineName', 'location', 'purpose',
                'start', 'start_utc', 'startUTC',
                'misc_infos', 'miscInfos', 'sub_units', 'subUnits',
                'assets', 'asset_stats', 'assetStats',
                'binary_data', 'binaryData', 'additional_data', 'additionalData',
                'origin', 'product_name', 'productName', 'process_name', 'processName'
            }
            
            # Separate common fields from UUT-specific fields
            common_fields = {k: v for k, v in obj.items() if k in common_field_names}
            uut_fields = {k: v for k, v in obj.items() if k not in common_field_names}
            
            # Create nested structure
            nested_obj = {
                'common': common_fields,
                **uut_fields
            }
            
            return super().model_validate(nested_obj, **kwargs)
        
        return super().model_validate(obj, **kwargs)
    
    @classmethod
    def model_validate_json(cls, json_data, **kwargs):
        """
        Override JSON deserialization to handle flattened format.
        """
        import json
        
        # Parse JSON to dict first
        obj = json.loads(json_data) if isinstance(json_data, (str, bytes)) else json_data
        
        # Use model_validate which handles flattening
        return cls.model_validate(obj, **kwargs)
