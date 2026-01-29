"""
ReportCommon - Shared fields for UUT and UUR reports (composition pattern)

This replaces the inheritance-based Report base class with a composition model.

Key improvements:
- No Optional[list] anti-pattern (lists are always lists, may be empty)
- Clean type signatures (mypy friendly)
- Validators preserved from v1 (PN/SN validation, time sync)
- 100% JSON compatible with v1

Design notes:
- Does NOT include 'type' field (moved to concrete classes to avoid override)
- Does NOT include 'info' field (UUTInfo vs UURInfo - concrete class responsibility)
- Collections use list[T] (never None) with default_factory
- Parent injection handled by StepList, not here
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, field_validator, model_validator

# Import from v1 (stable models)
from ..report_models.wats_base import WATSBase
from ..report_models.misc_info import MiscInfo
from ..report_models.asset import Asset, AssetStats
from ..report_models.sub_unit import SubUnit
from ..report_models.binary_data import BinaryData
from ..report_models.additional_data import AdditionalData

# Import validators from core
from ....core.validation import validate_serial_number, validate_part_number


class ReportCommon(WATSBase):
    """
    Shared fields for all report types (composition pattern).
    
    This model contains all common fields between UUTReport and UURReport.
    Concrete report classes will compose this model rather than inheriting.
    
    Serial Number and Part Number Validation:
        The sn (serial number) and pn (part number) fields are validated
        for problematic characters that can cause issues with WATS searches.
        
        Problematic characters: * % ? [] [^] ! / \\
        
        To bypass validation (when you intentionally need these characters):
        - Use the allow_problematic_characters() context manager
        - Prefix the value with 'SUPPRESS:' (e.g., 'SUPPRESS:SN*001')
        
        See: pywats.core.validation for details
    """
    
    # =========================================================================
    # Identity Fields
    # =========================================================================
    
    id: UUID = Field(
        default_factory=uuid4, 
        description="A UUID identifying the report. Submitting a report with an existing id will overwrite the existing report."
    )
    
    pn: str = Field(
        ..., 
        max_length=100, 
        min_length=1,
        description="The part number of the unit tested or repaired."
    )
    
    sn: str = Field(
        ..., 
        max_length=100, 
        min_length=1, 
        description="The serial number of the unit tested or repaired."
    )
    
    rev: str = Field(
        ..., 
        max_length=100, 
        min_length=1, 
        description="The revision of the unit (part number) tested or repaired."
    )
    
    # Validate serial number for problematic characters
    @field_validator('sn', mode='after')
    @classmethod
    def validate_sn(cls, v: str) -> str:
        """Validate serial number for problematic characters."""
        return validate_serial_number(v)
    
    # Validate part number for problematic characters
    @field_validator('pn', mode='after')
    @classmethod
    def validate_pn(cls, v: str) -> str:
        """Validate part number for problematic characters."""
        return validate_part_number(v)
    
    process_code: int = Field(
        ..., 
        validation_alias="processCode", 
        serialization_alias="processCode"
    )
    
    # =========================================================================
    # Result
    # =========================================================================
    
    result: str = Field(
        default="P", 
        max_length=1, 
        min_length=1, 
        pattern='^[PFDET]$',
        description="P=Passed, F=Failed, E=Error, D=Done, T=Terminated"
    )
    
    # =========================================================================
    # Station Info
    # =========================================================================
    
    station_name: str = Field(
        ..., 
        max_length=100, 
        min_length=1, 
        validation_alias="machineName", 
        serialization_alias="machineName"
    )
    
    location: str = Field(
        ..., 
        max_length=100, 
        min_length=1
    )
    
    purpose: str = Field(
        ..., 
        max_length=100, 
        min_length=1
    )
    
    # =========================================================================
    # Timing Fields
    # =========================================================================
    
    start: datetime | None = Field(
        default=None,
        examples=["2019-12-12T12:26:16.977+01:00"],
        description="Local start time with timezone offset. Server uses this as the authoritative time."
    )
    
    start_utc: datetime | None = Field(
        default=None, 
        examples=['2019-09-12T12:26:16.977Z'], 
        validation_alias="startUTC", 
        serialization_alias="startUTC",
        exclude=True,  # Exclude from serialization (sending to server)
        description="UTC equivalent of start time. Automatically computed and kept in sync. Not sent to server."
    )
   
    @model_validator(mode='after')
    def sync_start_times(self) -> 'ReportCommon':
        """
        Synchronize start and start_utc times.
        
        Rules:
        1. If only start is set: Ensure it's timezone-aware and compute start_utc
        2. If only start_utc is set: Compute start as local time
        3. If both are set: Keep them as-is (user takes responsibility)
        4. If neither is set: Use current time as default
        
        The server uses only the 'start' field (local time with offset).
        The start_utc is automatically computed for convenience and returned by the API.
        """
        # Case 1: Both times are set - keep as-is
        if self.start and self.start_utc:
            # Just ensure they're timezone-aware
            if self.start.tzinfo is None:
                self.start = self.start.astimezone()
            if self.start_utc.tzinfo is None:
                self.start_utc = self.start_utc.replace(tzinfo=timezone.utc)
        
        # Case 2: Only start is set (most common)
        elif self.start:
            # Ensure start is timezone-aware
            if self.start.tzinfo is None:
                self.start = self.start.astimezone()
            # Compute start_utc
            self.start_utc = self.start.astimezone(timezone.utc)
        
        # Case 3: Only start_utc is set (less common)
        elif self.start_utc:
            # Ensure start_utc is timezone-aware (assume UTC if naive)
            if self.start_utc.tzinfo is None:
                self.start_utc = self.start_utc.replace(tzinfo=timezone.utc)
            # Compute start as local time
            self.start = self.start_utc.astimezone()
        
        # Case 4: Neither is set - use current time
        else:
            self.start = datetime.now().astimezone()
            self.start_utc = self.start.astimezone(timezone.utc)
        
        return self
    
    # =========================================================================
    # Collections - Clean list pattern (NO Optional[list] anti-pattern!)
    # =========================================================================
    
    # Miscellaneous information
    misc_infos: list[MiscInfo] = Field(
        default_factory=list, 
        validation_alias="miscInfos",
        serialization_alias="miscInfos",
        description="List of miscellaneous key-value information"
    )
    
    # SubUnits
    sub_units: list[SubUnit] = Field(
        default_factory=list, 
        validation_alias="subUnits",
        serialization_alias="subUnits",
        description="List of sub-units/components"
    )
    
    # Assets
    assets: list[Asset] = Field(
        default_factory=list,
        description="List of assets used during test/repair"
    )
    
    asset_stats: list[AssetStats] | None = Field(
        default=None, 
        exclude=True, 
        validation_alias="assetStats", 
        serialization_alias="assetStats",
        description="Asset statistics (output only, not sent to server)"
    )
    
    # Binary data (not widely used)
    binary_data: list[BinaryData] = Field(
        default_factory=list, 
        validation_alias="binaryData", 
        serialization_alias="binaryData",
        description="Binary attachments"
    )
    
    # Additional data (not widely used)
    additional_data: list[AdditionalData | None] = Field(
        default_factory=list, 
        validation_alias="additionalData", 
        serialization_alias="additionalData",
        description="Additional custom data"
    )
    
    # =========================================================================
    # Output-only Fields (returned by API, not sent)
    # =========================================================================
    
    origin: str | None = Field(
        default=None, 
        max_length=100,
        exclude=True,
        description="Origin of the report (output only)"
    )
    
    product_name: str | None = Field(
        default=None, 
        max_length=100,
        exclude=True, 
        validation_alias="productName", 
        serialization_alias="productName",
        description="Product name (output only)"
    )
    
    process_name: str | None = Field(
        default=None, 
        max_length=100,
        exclude=True, 
        validation_alias="processName", 
        serialization_alias="processName",
        description="Process name (output only)"
    )
    
    # =========================================================================
    # Helper Methods (preserved from v1)
    # =========================================================================
    
    def add_misc_info(self, description: str, value: Any) -> MiscInfo:
        """
        Add miscellaneous information to the report.
        
        Args:
            description: Key/description for the info
            value: Value (will be converted to string)
            
        Returns:
            The created MiscInfo object
        """
        str_val = str(value)
        mi = MiscInfo(description=description, string_value=str_val)
        self.misc_infos.append(mi)
        return mi

    def add_sub_unit(self, part_type: str, sn: str, pn: str, rev: str) -> SubUnit:
        """
        Add a sub-unit/component to the report.
        
        Args:
            part_type: Type of the part
            sn: Serial number of the sub-unit
            pn: Part number of the sub-unit
            rev: Revision of the sub-unit
            
        Returns:
            The created SubUnit object
        """
        su = SubUnit(part_type=part_type, sn=sn, pn=pn, rev=rev)
        self.sub_units.append(su)
        return su

    def add_asset(self, sn: str, usage_count: int) -> Asset:
        """
        Add an asset (tool/equipment) used during test/repair.
        
        Args:
            sn: Serial number of the asset
            usage_count: Number of times the asset was used
            
        Returns:
            The created Asset object
        """
        asset = Asset(sn=sn, usage_count=usage_count)
        self.assets.append(asset)
        return asset
