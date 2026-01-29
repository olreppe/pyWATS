"""
UURReport v2 - Composition-based UUR (Unit Under Repair) report

Key differences from v1:
- Uses composition (ReportCommon) instead of inheritance (Report)
- Clean type signature (no field overrides)
- Dual process code architecture preserved
- 100% JSON compatible with v1

Design notes:
- UUR has dual process codes: repair_process_code + test_operation_code
- Failures stored on sub_units (idx=0 is main unit)
- Imports UURInfo and UURSubUnit from v1
"""

from __future__ import annotations

from typing import Literal, TYPE_CHECKING
from uuid import UUID
from pydantic import BaseModel, Field, model_validator

# Import ReportCommon (composition)
from .report_common import ReportCommon

# Import from v1 (stable models)
from ..report_models.uur.uur_info import UURInfo
from ..report_models.uur.uur_sub_unit import UURSubUnit
from ..report_models.attachment import Attachment

# Import base class
from ..report_models.wats_base import WATSBase

if TYPE_CHECKING:
    from .uut_report import UUTReport


class UURReport(WATSBase):
    """
    UUR (Unit Under Repair) Report - Composition-based v2
    
    UUR reports document repair/rework activities on units that have failed testing.
    
    Key features:
    - Links to original UUT report via `uur_info.ref_uut`
    - **Dual process codes**: 
      - repair_process_code (type of repair, e.g., 500=Repair)
      - test_operation_code (original test operation that failed)
    - Failures stored on sub_units (idx=0 is main unit)
    - Supports sub-unit replacement tracking
    
    Architecture:
    - common: ReportCommon (all shared fields via composition)
    - type: Literal["R"] (UUR type identifier)
    - uur_info: UURInfo (UUR-specific metadata, dual process codes)
    - sub_units: list[UURSubUnit] (units being repaired, idx=0 is main)
    
    Example usage:
    
    Factory pattern (recommended):
        uur = UURReport.create_from_uut(
            uut_report,
            repair_process_code=500,
            operator="John Doe"
        )
        
    Constructor pattern:
        uur = UURReport(
            common=ReportCommon(
                pn="ABC123",
                sn="SN-001",
                rev="A",
                process_code=500,  # Repair process code
                station_name="RepairStation",
                location="RepairLab",
                purpose="Repair"
            ),
            uur_info=UURInfo(
                test_operation_code=100,  # Original test that failed
                operator="John Doe"
            )
        )
    
    Adding failures:
        main = uur.get_main_unit()
        main.add_failure(category="Component", code="CAPACITOR_FAIL")
    """
    
    # =========================================================================
    # Core Fields
    # =========================================================================
    
    common: ReportCommon = Field(
        default_factory=ReportCommon,
        description="Shared fields for all report types (composition pattern)"
    )
    
    type: Literal["R"] = Field(
        default="R",
        description="Report type: 'R' = Repair Report (UUR)"
    )
    
    uur_info: UURInfo = Field(
        default_factory=UURInfo,
        validation_alias="uur",
        serialization_alias="uur",
        description="UUR-specific metadata (dual process codes, operator, comment)"
    )
    
    # Sub-units with failures (idx=0 is main unit)
    sub_units: list[UURSubUnit] = Field(
        default_factory=list,
        validation_alias="subUnits",
        serialization_alias="subUnits",
        description="List of sub-units being repaired (idx=0 is main unit)"
    )
    
    # Attachments (report-level)
    attachments: list[Attachment] = Field(
        default_factory=list,
        validation_alias="binaryData",
        serialization_alias="binaryData",
        description="Report-level attachments (photos, documents, etc.)"
    )
    
    @model_validator(mode='after')
    def ensure_main_unit(self) -> 'UURReport':
        """
        Ensure main unit (idx=0) exists.
        
        If no sub_units exist or none have idx=0, creates a main unit
        matching the report's part number, serial number, and revision.
        """
        if not self.sub_units or not any(su.idx == 0 for su in self.sub_units):
            main = UURSubUnit.create_main_unit(
                pn=self.common.pn,
                sn=self.common.sn,
                rev=self.common.rev
            )
            self.sub_units.insert(0, main)
        return self
    
    # =========================================================================
    # Sub-Unit Access Methods
    # =========================================================================
    
    def get_main_unit(self) -> UURSubUnit:
        """
        Get the main unit (idx=0).
        
        Returns:
            UURSubUnit: The main unit being repaired
        """
        for su in self.sub_units:
            if su.idx == 0:
                return su
        # Shouldn't happen due to ensure_main_unit validator
        raise ValueError("Main unit (idx=0) not found")
    
    def add_sub_unit(self, pn: str, sn: str, rev: str = "A") -> UURSubUnit:
        """
        Add a sub-unit to the repair report.
        
        Sub-units are assigned sequential indices starting from 1
        (idx=0 is reserved for the main unit).
        
        Args:
            pn: Part number of the sub-unit
            sn: Serial number of the sub-unit
            rev: Revision of the sub-unit
            
        Returns:
            UURSubUnit: The created sub-unit
            
        Example:
            sub = uur.add_sub_unit("PCB-123", "PCB-SN-001", "1.0")
            sub.add_failure(category="Solder", code="COLD_JOINT")
        """
        # Find next available index
        max_idx = max((su.idx for su in self.sub_units), default=0)
        next_idx = max_idx + 1
        
        su = UURSubUnit(
            idx=next_idx,
            pn=pn,
            sn=sn,
            rev=rev
        )
        self.sub_units.append(su)
        return su
    
    # =========================================================================
    # Factory Methods
    # =========================================================================
    
    @classmethod
    def create(
        cls,
        pn: str,
        sn: str,
        rev: str,
        repair_process_code: int,
        test_operation_code: int,
        station_name: str,
        location: str,
        purpose: str,
        operator: str = "Unknown",  # Required by UURInfo
        comment: str | None = None,
        **kwargs
    ) -> 'UURReport':
        """
        Factory method for creating UURReport with unpacked fields.
        
        Args:
            pn: Part number
            sn: Serial number
            rev: Revision
            repair_process_code: Repair operation code (e.g., 500=Repair)
            test_operation_code: Original test operation that failed
            station_name: Station/machine name
            location: Location
            purpose: Purpose
            operator: Operator name (defaults to "Unknown")
            comment: Repair comment (optional)
            **kwargs: Additional fields for ReportCommon
            
        Returns:
            UURReport: New UUR report instance
        """
        common = ReportCommon(
            pn=pn,
            sn=sn,
            rev=rev,
            process_code=repair_process_code,  # Top-level is repair code
            station_name=station_name,
            location=location,
            purpose=purpose,
            **kwargs
        )
        
        uur_info = UURInfo(
            test_operation_code=test_operation_code,  # Original test code
            operator=operator,  # Required field
            comment=comment
        )
        
        return cls(common=common, uur_info=uur_info)
    
    @classmethod
    def create_from_uut(
        cls,
        uut_report: 'UUTReport',
        repair_process_code: int = 500,
        operator: str = "Unknown",  # Required by UURInfo
        comment: str | None = None,
        station_name: str | None = None,
        location: str | None = None,
        purpose: str | None = None
    ) -> 'UURReport':
        """
        Factory method to create UURReport from a failed UUTReport.
        
        This is the typical workflow: a UUT fails testing, then a UUR
        is created to document the repair work.
        
        Args:
            uut_report: Original UUT report that failed
            repair_process_code: Repair operation code (default: 500=Repair)
            operator: Repair operator name
            comment: Repair comment
            station_name: Override station name (uses UUT's if not provided)
            location: Override location (uses UUT's if not provided)
            purpose: Override purpose (uses UUT's if not provided)
            
        Returns:
            UURReport: New UUR report linked to the UUT
            
        Example:
            uut = # ... UUT report that failed
            uur = UURReport.create_from_uut(
                uut,
                repair_process_code=500,
                operator="Jane Doe",
                comment="Replace failed capacitor"
            )
        """
        # Copy identity from UUT
        common = ReportCommon(
            id=uut_report.common.id,  # Link via same ID
            pn=uut_report.common.pn,
            sn=uut_report.common.sn,
            rev=uut_report.common.rev,
            process_code=repair_process_code,  # Different process code!
            station_name=station_name or uut_report.common.station_name,
            location=location or uut_report.common.location,
            purpose=purpose or uut_report.common.purpose
        )
        
        uur_info = UURInfo(
            ref_uut=uut_report.common.id,  # Reference to UUT
            test_operation_code=uut_report.common.process_code,  # Original test code
            operator=operator,
            comment=comment
        )
        
        return cls(common=common, uur_info=uur_info)
    
    # =========================================================================
    # Serialization Customization
    # =========================================================================
    
    def model_dump(self, **kwargs):
        """
        Override serialization to flatten common fields to top level.
        
        Ensures JSON output matches v1 structure.
        """
        data = super().model_dump(**kwargs)
        
        # Flatten common fields to top level
        if 'common' in data:
            common_data = data.pop('common')
            data = {**common_data, **data}
        
        return data
    
    def model_dump_json(self, **kwargs):
        """Override JSON serialization to flatten common fields."""
        import json
        from pydantic.json import pydantic_encoder
        
        data = self.model_dump(**kwargs)
        return json.dumps(data, default=pydantic_encoder)
    
    @classmethod
    def model_validate(cls, obj, **kwargs):
        """
        Override deserialization to handle both flattened and nested formats.
        """
        if isinstance(obj, dict):
            if 'common' in obj:
                return super().model_validate(obj, **kwargs)
            
            # Extract common fields from flattened format
            common_field_names = {
                'id', 'pn', 'sn', 'rev', 'process_code', 'processCode',
                'result', 'station_name', 'machineName', 'location', 'purpose',
                'start', 'start_utc', 'startUTC',
                'misc_infos', 'miscInfos', 'assets', 'asset_stats', 'assetStats',
                'binary_data', 'binaryData', 'additional_data', 'additionalData',
                'origin', 'product_name', 'productName', 'process_name', 'processName'
            }
            
            common_fields = {k: v for k, v in obj.items() if k in common_field_names}
            uur_fields = {k: v for k, v in obj.items() if k not in common_field_names}
            
            nested_obj = {
                'common': common_fields,
                **uur_fields
            }
            
            return super().model_validate(nested_obj, **kwargs)
        
        return super().model_validate(obj, **kwargs)
    
    @classmethod
    def model_validate_json(cls, json_data, **kwargs):
        """Override JSON deserialization to handle flattened format."""
        import json
        
        obj = json.loads(json_data) if isinstance(json_data, (str, bytes)) else json_data
        return cls.model_validate(obj, **kwargs)
