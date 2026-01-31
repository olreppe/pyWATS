"""
UURReport - v3 Implementation

Unit Under Repair report - documents repair/rework activities.
Simpler than UUTReport: no steps/sequences, failures on sub-units.
"""
from __future__ import annotations

from typing import Optional, List, Literal, Any
from uuid import UUID

from pydantic import model_validator

from ..report import Report
from ..common_types import Field
from ..binary_data import Attachment
from .uur_info import UURInfo
from .uur_sub_unit import UURSubUnit
from .uur_failure import UURFailure


class UURReport(Report[UURSubUnit]):
    """
    Unit Under Repair (UUR) report.
    
    Documents repair/rework activities on units that have failed testing.
    
    Key Features:
    - Links to original UUT report via uur_info.ref_uut
    - Dual process codes: repair (what repair type) and test (original test)
    - Failures stored on sub_units (idx=0 is main unit)
    - No test steps/sequences (unlike UUTReport)
    
    C# Name: UURReport
    
    Example:
        # Create repair report linked to failed UUT
        uur = UURReport(
            pn="WIDGET-001",
            sn="SN123456",
            operation="Repair"
        )
        
        # Link to failed UUT
        uur.uur_info.ref_uut = uut_report.id
        uur.uur_info.repair_process_code = 500
        
        # Add failure to main unit
        main = uur.get_main_unit()
        main.add_failure(category="Component", code="CAP_FAIL", com_ref="C12")
        
        # Submit
        await client.submit_report(uur)
    """
    
    # Report type discriminator: R = Repair
    type: Literal["R"] = Field(
        default="R",
        pattern='^[R]$',
        description="Report type: R = Repair/UUR."
    )
    
    # ========================================================================
    # UUR-Specific Info
    # ========================================================================
    
    uur_info: UURInfo = Field(
        default_factory=UURInfo,
        validation_alias="uur",
        serialization_alias="uur",
        description="UUR-specific information (process codes, UUT reference)."
    )
    
    # ========================================================================
    # Sub-Units with Failures
    # ========================================================================
    
    # Override sub_units to use UURSubUnit type
    sub_units: List[UURSubUnit] = Field(  # type: ignore[assignment]
        default_factory=list,
        validation_alias="subUnits",
        serialization_alias="subUnits",
        description="Sub-units with failures (idx=0 is main unit)."
    )
    
    # ========================================================================
    # Assets
    # ========================================================================
    
    asset_stats: Optional[List] = Field(
        default_factory=list,
        validation_alias="assetStats",
        serialization_alias="assetStats",
        description="Asset statistics."
    )
    
    # ========================================================================
    # Attachments
    # ========================================================================
    
    attachments: List[Attachment] = Field(
        default_factory=list,
        validation_alias="binaryData",
        serialization_alias="binaryData",
        description="Report-level attachments."
    )
    
    # ========================================================================
    # Validators
    # ========================================================================
    
    @model_validator(mode='after')
    def ensure_main_unit(self) -> "UURReport":
        """Ensure main unit (idx=0) exists."""
        if not self.sub_units or not any(su.idx == 0 for su in self.sub_units):
            main = UURSubUnit.create_main_unit(
                pn=self.pn,
                sn=self.sn,
                rev=self.rev or ""
            )
            self.sub_units.insert(0, main)
        return self
    
    # ========================================================================
    # Convenience Properties (delegate to uur_info)
    # ========================================================================
    
    @property
    def uut_guid(self) -> Optional[UUID]:
        """GUID of the referenced UUT report."""
        return self.uur_info.ref_uut if self.uur_info else None
    
    @uut_guid.setter
    def uut_guid(self, value: UUID) -> None:
        if self.uur_info:
            self.uur_info.ref_uut = value
    
    @property
    def operator(self) -> Optional[str]:
        """Operator who performed the repair."""
        return self.uur_info.operator if self.uur_info else None
    
    @operator.setter
    def operator(self, value: str) -> None:
        if self.uur_info:
            self.uur_info.operator = value
    
    @property
    def comment(self) -> Optional[str]:
        """Repair comment."""
        return self.uur_info.comment if self.uur_info else None
    
    @comment.setter
    def comment(self, value: str) -> None:
        if self.uur_info:
            self.uur_info.comment = value
    
    @property
    def execution_time(self) -> float:
        """Time spent on repair (seconds)."""
        return self.uur_info.exec_time if self.uur_info and self.uur_info.exec_time else 0.0
    
    @execution_time.setter
    def execution_time(self, value: float) -> None:
        if self.uur_info:
            self.uur_info.exec_time = value
    
    @property
    def repair_process_code(self) -> int:
        """Alias for process_code (repair operation code)."""
        return self.process_code
    
    @property
    def repair_operation_code(self) -> int:
        """Alias for process_code (repair operation code)."""
        return self.process_code
    
    @property
    def test_operation_code(self) -> Optional[int]:
        """Test operation code from uur_info."""
        return self.uur_info.test_operation_code if self.uur_info else None
    
    @property
    def all_failures(self) -> List[UURFailure]:
        """Get all failures from all sub-units."""
        result = []
        for su in self.sub_units:
            if su.failures:
                result.extend(su.failures)
        return result
    
    @property
    def failures(self) -> List[UURFailure]:
        """Alias for all_failures."""
        return self.all_failures
    
    def get_sub_unit(self, idx: int) -> Optional[UURSubUnit]:
        """Get sub-unit by index."""
        for su in self.sub_units:
            if su.idx == idx:
                return su
        return None
    
    def add_failure(
        self,
        category: str,
        code: str,
        comment: Optional[str] = None,
        component_ref: Optional[str] = None,
        ref_step_id: Optional[int] = None
    ) -> UURFailure:
        """Add failure to main unit."""
        main = self.get_main_unit()
        return main.add_failure(category, code, comment, component_ref, ref_step_id)
    
    def add_failure_to_main_unit(
        self,
        category: str,
        code: str,
        comment: Optional[str] = None,
        component_ref: Optional[str] = None
    ) -> UURFailure:
        """Add failure to main unit (alias for add_failure)."""
        return self.add_failure(category, code, comment, component_ref)
    
    def attach_bytes(
        self,
        name: str,
        content: bytes,
        mime_type: str = "application/octet-stream"
    ) -> Attachment:
        """Attach binary data to report."""
        attachment = Attachment(
            name=name,
            mime_type=mime_type,
            data=content
        )
        self.attachments.append(attachment)
        return attachment
    
    def get_summary(self) -> dict:
        """Get report summary."""
        return {
            'pn': self.pn,
            'sn': self.sn,
            'result': self.result,
            'repair_process_code': self.process_code,
            'test_operation_code': self.test_operation_code,
            'total_failures': len(self.all_failures),
            'sub_units': len(self.sub_units)
        }
    
    def validate_report(self) -> tuple[bool, str]:
        """Validate report structure and content."""
        errors = []
        
        # Check main unit exists
        try:
            _ = self.get_main_unit()
        except ValueError as e:
            errors.append(str(e))
            return False, "; ".join(errors)
        
        # Validate dual process codes
        if self.uur_info and self.process_code and self.uur_info.test_operation_code:
            if self.process_code == self.uur_info.test_operation_code:
                errors.append("repair process_code and test_operation_code should differ")
        
        if errors:
            return False, "; ".join(errors)
        return True, "OK"
    
    def copy_misc_from_uut(self, uut_report: Any) -> None:
        """Copy misc_infos from UUT report."""
        if hasattr(uut_report, 'misc_infos') and uut_report.misc_infos:
            self.misc_infos = list(uut_report.misc_infos)
    
    # ========================================================================
    # UUT Linking
    # ========================================================================
    
    def link_to_uut(self, uut_id: UUID) -> None:
        """
        Link this repair report to a failed UUT report.
        
        Args:
            uut_id: UUID of the failed UUT report.
        """
        self.uur_info.ref_uut = uut_id
    
    def set_repair_process(
        self,
        code: int,
        name: Optional[str] = None
    ) -> None:
        """
        Set the repair process code.
        
        Args:
            code: Repair process code
            name: Optional process name
        """
        self.uur_info.repair_process_code = code
        self.uur_info.process_code = code
        if name:
            self.uur_info.repair_process_name = name
            self.uur_info.process_name = name
    
    def set_test_operation(
        self,
        code: int,
        name: Optional[str] = None,
        guid: Optional[UUID] = None
    ) -> None:
        """
        Set the original test operation that failed.
        
        Args:
            code: Test operation code
            name: Optional operation name
            guid: Optional operation GUID
        """
        self.uur_info.test_operation_code = code
        if name:
            self.uur_info.test_operation_name = name
        if guid:
            self.uur_info.test_operation_guid = guid
    
    # ========================================================================
    # Main Unit Access
    # ========================================================================
    
    def get_main_unit(self) -> UURSubUnit:
        """
        Get the main unit (idx=0).
        
        Returns:
            UURSubUnit representing the main unit being repaired.
        """
        for su in self.sub_units:
            if su.idx == 0:
                return su
        
        # Should not happen due to validator, but create if missing
        main = UURSubUnit.create_main_unit(
            pn=self.pn,
            sn=self.sn,
            rev=self.rev or ""
        )
        self.sub_units.insert(0, main)
        return main
    
    # ========================================================================
    # Sub-Unit Management
    # ========================================================================
    
    def add_sub_unit(  # type: ignore[override]
        self,
        pn: str,
        sn: str,
        rev: Optional[str] = None,
        part_type: str = "Unknown",
        parent_idx: Optional[int] = None,
    ) -> UURSubUnit:
        """
        Add a sub-unit to the repair report.
        
        Args:
            pn: Part number
            sn: Serial number
            rev: Revision
            part_type: Type of unit
            parent_idx: Index of parent unit (optional)
            
        Returns:
            The created UURSubUnit.
        """
        # Find next available index
        max_idx = max((su.idx for su in self.sub_units), default=-1)
        
        sub_unit = UURSubUnit(
            pn=pn,
            sn=sn,
            rev=rev,
            part_type=part_type,
            idx=max_idx + 1,
            parent_idx=parent_idx,
        )
        self.sub_units.append(sub_unit)
        return sub_unit
    
    def get_sub_unit_by_idx(self, idx: int) -> Optional[UURSubUnit]:
        """Get a sub-unit by its index."""
        for su in self.sub_units:
            if su.idx == idx:
                return su
        return None
    
    # ========================================================================
    # Failure Helpers
    # ========================================================================
    
    def add_main_failure(
        self,
        category: str,
        code: str,
        **kwargs: Any
    ) -> UURFailure:
        """
        Add a failure to the main unit.
        
        Args:
            category: Failure category
            code: Failure code
            **kwargs: Additional failure fields
            
        Returns:
            The created UURFailure.
        """
        main = self.get_main_unit()
        return main.add_failure(category, code, **kwargs)
    
    def get_all_failures(self) -> List[UURFailure]:
        """Get all failures across all sub-units."""
        failures: List[UURFailure] = []
        for su in self.sub_units:
            failures.extend(su.get_failures())
        return failures
    
    def count_failures(self) -> int:
        """Count total failures across all sub-units."""
        return sum(len(su.get_failures()) for su in self.sub_units)
    
    # ========================================================================
    # Attachment Helpers
    # ========================================================================
    
    def add_attachment(self, attachment: Attachment) -> None:
        """Add an attachment to the report."""
        self.attachments.append(attachment)
    
    def add_attachment_from_file(
        self,
        file_path: str,
        content_type: Optional[str] = None,
        description: Optional[str] = None
    ) -> Attachment:
        """
        Add an attachment from a file.
        
        Args:
            file_path: Path to the file
            content_type: MIME type (auto-detected if not provided)
            description: Optional description
            
        Returns:
            The created Attachment.
        """
        attachment = Attachment.from_file(file_path, content_type, description)
        self.attachments.append(attachment)
        return attachment
