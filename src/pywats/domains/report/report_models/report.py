"""
Report Base Class - v3 Implementation

Base class containing ALL common fields for UUT and UUR reports.
Proper inheritance: UUTReport(Report), UURReport(Report).
"""
from __future__ import annotations

from typing import Optional, List, TypeVar, Generic, TYPE_CHECKING, Any
from datetime import datetime, timezone

from .common_types import (
    WATSBase,
    Field,
    field_validator,
    model_validator,
    uuid4,
    UUID,
    ReportResult,
    validate_serial_number,
    validate_part_number,
)
from .report_info import ReportInfo
from .sub_unit import SubUnit
from .misc_info import MiscInfo
from .asset import Asset
from .binary_data import BinaryData, AdditionalData

# TypeVar for SubUnit specialization in subclasses
SubUnitT = TypeVar('SubUnitT', bound=SubUnit)


class Report(WATSBase, Generic[SubUnitT]):
    """
    Base class for all WATS reports.
    
    Contains ALL fields common to both UUT (test) and UUR (repair) reports.
    This ensures single source of truth and proper inheritance.
    
    Subclasses:
        - UUTReport: Test reports with root sequence call
        - UURReport: Repair reports with repair-specific fields
        
    Generic Parameter:
        SubUnitT: The SubUnit type - SubUnit for UUT, UURSubUnit for UUR
    """
    
    # ========================================================================
    # Core Identification Fields
    # ========================================================================
    
    # Unique report identifier (UUID)
    id: UUID = Field(
        default_factory=uuid4,
        description="Unique report identifier. Submitting with existing ID overwrites."
    )
    
    # Report type discriminator: T=Test/UUT, R=Repair/UUR
    type: str = Field(
        default="T",
        max_length=1,
        min_length=1,
        pattern='^[TR]$',
        description="Report type: 'T'=Test/UUT, 'R'=Repair/UUR."
    )
    
    # Part number - required
    pn: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Part number of the unit tested or repaired."
    )
    
    # Serial number - required
    sn: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Serial number of the unit tested or repaired."
    )
    
    # Revision - required
    rev: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Revision of the part number."
    )
    
    # ========================================================================
    # Field Validators
    # ========================================================================
    
    @field_validator('sn', mode='after')
    @classmethod
    def validate_sn(cls, v: str) -> str:
        """Validate serial number for problematic characters."""
        return validate_serial_number(v)
    
    @field_validator('pn', mode='after')
    @classmethod
    def validate_pn(cls, v: str) -> str:
        """Validate part number for problematic characters."""
        return validate_part_number(v)
    
    # ========================================================================
    # Process & Station Fields
    # ========================================================================
    
    # Process code - identifies the test/repair process
    process_code: int = Field(
        ...,
        validation_alias="processCode",
        serialization_alias="processCode",
        description="Process code identifying the test/repair process."
    )
    
    # Result of the report
    result: ReportResult = Field(
        default=ReportResult.Passed,
        description="Overall result: P=Passed, F=Failed, D=Done, E=Error, T=Terminated."
    )
    
    # Station/Machine name
    station_name: str = Field(
        ...,
        max_length=100,
        min_length=1,
        validation_alias="machineName",
        serialization_alias="machineName",
        description="Name of the test station/machine."
    )
    
    # Location
    location: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Physical location of the test station."
    )
    
    # Purpose (e.g., "Production", "Engineering", "RMA")
    purpose: str = Field(
        ...,
        max_length=100,
        min_length=1,
        description="Purpose of the test (e.g., 'Production', 'Engineering')."
    )
    
    # ========================================================================
    # Timing Fields
    # ========================================================================
    
    # Local start time with timezone
    start: Optional[datetime] = Field(
        default=None,
        examples=["2026-01-30T12:26:16.977+01:00"],
        description="Local start time with timezone offset."
    )
    
    # UTC start time (computed, not sent to server)
    start_utc: Optional[datetime] = Field(
        default=None,
        examples=["2026-01-30T11:26:16.977Z"],
        validation_alias="startUTC",
        serialization_alias="startUTC",
        exclude=True,  # Not sent to server
        description="UTC equivalent of start time (computed, not serialized)."
    )
    
    @model_validator(mode='after')
    def sync_start_times(self) -> "Report[SubUnitT]":
        """
        Synchronize start and start_utc times.
        
        The server uses 'start' (local time with offset) as authoritative.
        start_utc is computed for convenience.
        """
        if self.start and self.start_utc:
            # Both set - ensure timezone aware
            if self.start.tzinfo is None:
                object.__setattr__(self, 'start', self.start.astimezone())
            if self.start_utc.tzinfo is None:
                object.__setattr__(self, 'start_utc', 
                                   self.start_utc.replace(tzinfo=timezone.utc))
                
        elif self.start:
            # Only start set - compute UTC
            if self.start.tzinfo is None:
                object.__setattr__(self, 'start', self.start.astimezone())
            object.__setattr__(self, 'start_utc', 
                               self.start.astimezone(timezone.utc))
            
        elif self.start_utc:
            # Only UTC set - compute local
            if self.start_utc.tzinfo is None:
                object.__setattr__(self, 'start_utc', 
                                   self.start_utc.replace(tzinfo=timezone.utc))
            object.__setattr__(self, 'start', self.start_utc.astimezone())
            
        else:
            # Neither set - use current time
            now = datetime.now(timezone.utc)
            object.__setattr__(self, 'start', now.astimezone())
            object.__setattr__(self, 'start_utc', now)
            
        return self
    
    # ========================================================================
    # Report Info (subclasses override with specific type)
    # ========================================================================
    
    # Report-specific info - overridden in UUTReport and UURReport
    # Using Optional here; subclasses provide concrete type
    info: Optional[ReportInfo] = Field(
        default=None,
        description="Report-specific information (UUTInfo or UURInfo)."
    )
    
    # ========================================================================
    # Collections
    # ========================================================================
    
    # Sub-units / components
    sub_units: Optional[List[SubUnitT]] = Field(  # type: ignore[valid-type]
        default_factory=list,
        validation_alias="subUnits",
        serialization_alias="subUnits",
        description="List of sub-units/components."
    )
    
    # Miscellaneous information
    misc_infos: Optional[List[MiscInfo]] = Field(
        default=None,
        validation_alias="miscInfos",
        serialization_alias="miscInfos",
        description="Additional key-value information."
    )
    
    # Assets/equipment used
    assets: Optional[List[Asset]] = Field(
        default=None,
        description="Test equipment/assets used."
    )
    
    asset_stats: Optional[List] = Field(
        default=None,
        validation_alias="assetStats",
        serialization_alias="assetStats",
        description="Asset statistics."
    )
    
    # Binary data attachments
    binary_data: Optional[List[BinaryData]] = Field(
        default=None,
        validation_alias="binaryData",
        serialization_alias="binaryData",
        description="Binary data attachments."
    )
    
    # Additional data
    additional_data: Optional[List[AdditionalData]] = Field(
        default=None,
        validation_alias="additionalData",
        serialization_alias="additionalData",
        description="Additional structured data."
    )
    
    # ========================================================================
    # Output-Only Fields (not sent to server)
    # ========================================================================
    
    origin: Optional[str] = Field(
        default=None,
        max_length=100,
        exclude=True,
        description="Origin identifier (output only)."
    )
    
    product_name: Optional[str] = Field(
        default=None,
        max_length=100,
        exclude=True,
        validation_alias="productName",
        serialization_alias="productName",
        description="Product name (output only)."
    )
    
    process_name: Optional[str] = Field(
        default=None,
        max_length=100,
        exclude=True,
        validation_alias="processName",
        serialization_alias="processName",
        description="Process name (output only)."
    )
    
    process_code_format: Optional[str] = Field(
        default=None,
        max_length=100,
        exclude=True,
        validation_alias="processCodeFormat",
        serialization_alias="processCodeFormat",
        description="Process code format (output only)."
    )
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def add_misc_info(self, description: str, value: Any) -> MiscInfo:
        """
        Add miscellaneous information to the report.
        
        Args:
            description: The info key/description
            value: The value (will be converted to string)
            
        Returns:
            The created MiscInfo object
        """
        str_val = str(value)
        mi = MiscInfo(description=description, string_value=str_val)
        if self.misc_infos is None:
            self.misc_infos = []
        self.misc_infos.append(mi)
        return mi
    
    def add_asset(self, sn: str, usage_count: int) -> Asset:
        """
        Add an asset to the report.
        
        Args:
            sn: Asset serial number
            usage_count: Number of times used
            
        Returns:
            The created Asset object
        """
        asset = Asset(sn=sn, usage_count=usage_count)
        if self.assets is None:
            self.assets = []
        self.assets.append(asset)
        return asset
    
    def add_sub_unit(self, part_type: str, sn: str, pn: str, rev: str) -> SubUnitT:
        """
        Add a sub-unit to the report.
        
        Args:
            part_type: Type of the sub-unit
            sn: Serial number
            pn: Part number
            rev: Revision
            
        Returns:
            The created SubUnit object
        """
        su = SubUnit(part_type=part_type, sn=sn, pn=pn, rev=rev)  # type: ignore
        if self.sub_units is None:
            self.sub_units = []
        self.sub_units.append(su)  # type: ignore
        return su  # type: ignore
    
    def add_binary_data(
        self,
        data: bytes,
        name: str,
        content_type: str = "application/octet-stream"
    ) -> BinaryData:
        """
        Add binary data to the report.
        
        Args:
            data: The raw bytes
            name: Filename
            content_type: MIME type
            
        Returns:
            The created BinaryData object
        """
        if self.binary_data is None:
            self.binary_data = []
            
        bd = BinaryData.from_bytes(data, name, content_type)
        self.binary_data.append(bd)
        return bd
