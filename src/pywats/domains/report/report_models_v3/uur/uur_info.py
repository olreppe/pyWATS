"""
UURInfo - v3 Implementation

UUR-specific info with dual process code architecture.
Links repair report to original failed UUT report.
"""
from __future__ import annotations

from typing import Optional
from datetime import datetime
from uuid import UUID

from ..report_info import ReportInfo
from ..common_types import Field


class UURInfo(ReportInfo):
    """
    UUR-specific information.
    
    Key feature: Dual process code architecture
    - repair_process_code: What kind of repair this is
    - test_operation_code: Original test that was being performed
    
    C# Name: UUR_type
    """
    
    # ========================================================================
    # Dual Process Codes (Key Feature)
    # ========================================================================
    
    repair_process_code: Optional[int] = Field(
        default=None,
        validation_alias="repairProcessCode",
        serialization_alias="repairProcessCode",
        description="Repair process code - what kind of repair operation."
    )
    
    repair_process_name: Optional[str] = Field(
        default=None,
        validation_alias="repairProcessName",
        serialization_alias="repairProcessName",
        description="Repair process name."
    )
    
    test_operation_code: Optional[int] = Field(
        default=None,
        validation_alias="testOperationCode",
        serialization_alias="testOperationCode",
        description="Original test operation code that was being performed."
    )
    
    test_operation_name: Optional[str] = Field(
        default=None,
        validation_alias="testOperationName",
        serialization_alias="testOperationName",
        description="Original test operation name."
    )
    
    test_operation_guid: Optional[UUID] = Field(
        default=None,
        validation_alias="testOperationGuid",
        serialization_alias="testOperationGuid",
        description="Original test operation GUID."
    )
    
    # ========================================================================
    # API-Required Process Code (in uur object)
    # ========================================================================
    
    process_code: Optional[int] = Field(
        default=None,
        validation_alias="processCode",
        serialization_alias="processCode",
        description="Process code (required by API in uur object)."
    )
    
    process_code_format: Optional[str] = Field(
        default=None,
        validation_alias="processCodeFormat",
        serialization_alias="processCodeFormat",
        description="Process code format string."
    )
    
    process_name: Optional[str] = Field(
        default=None,
        validation_alias="processName",
        serialization_alias="processName",
        description="Process name."
    )
    
    # ========================================================================
    # UUT Reference (Links Repair to Failed Test)
    # ========================================================================
    
    ref_uut: Optional[UUID] = Field(
        default=None,
        validation_alias="refUUT",
        serialization_alias="refUUT",
        description="GUID of the UUT report being repaired."
    )
    
    # ========================================================================
    # Timing
    # ========================================================================
    
    confirm_date: Optional[datetime] = Field(
        default=None,
        validation_alias="confirmDate",
        serialization_alias="confirmDate",
        description="Date/time UUR was confirmed (UTC)."
    )
    
    finalize_date: Optional[datetime] = Field(
        default=None,
        validation_alias="finalizeDate",
        serialization_alias="finalizeDate",
        description="Date/time UUR was finalized (UTC)."
    )
    
    # ========================================================================
    # Status
    # ========================================================================
    
    active: bool = Field(
        default=True,
        description="Whether this UUR is active."
    )
    
    parent: Optional[UUID] = Field(
        default=None,
        description="Parent UUR GUID (for hierarchical repairs)."
    )
    
    # ========================================================================
    # Methods (V1 Compatibility)
    # ========================================================================
    
    def get_repair_process_info(self) -> dict:
        """
        Get repair process information.
        
        Returns:
            Dictionary with repair process details
        """
        return {
            'code': self.repair_process_code,
            'name': self.repair_process_name,
            'type': 'repair'
        }
    
    def get_test_operation_info(self) -> dict:
        """
        Get test operation information.
        
        Returns:
            Dictionary with test operation details
        """
        return {
            'code': self.test_operation_code,
            'name': self.test_operation_name,
            'guid': str(self.test_operation_guid) if self.test_operation_guid else None,
            'type': 'test'
        }
    
    def set_dual_process_codes(
        self,
        repair_code: int,
        repair_name: str,
        test_code: int,
        test_name: str,
        test_guid: Optional[UUID] = None
    ) -> None:
        """
        Set both repair and test process codes.
        
        Args:
            repair_code: Code for the repair operation
            repair_name: Name for the repair operation
            test_code: Code for the original test operation
            test_name: Name for the original test operation
            test_guid: GUID for the original test operation
        """
        # Set repair process
        self.repair_process_code = repair_code
        self.repair_process_name = repair_name
        
        # Set test operation
        self.test_operation_code = test_code
        self.test_operation_name = test_name
        self.test_operation_guid = test_guid
        
        # Update process_code for API compatibility
        self.process_code = test_code
        self.process_name = test_name
    
    def sync_process_codes(self) -> "UURInfo":
        """
        Sync test_operation_code/name with process_code/name.
        
        The API expects processCode/processName in the uur object to contain
        the test operation that was running. We store this as test_operation_*
        but serialize as process*.
        
        Returns:
            Self (for method chaining)
        """
        # If test_operation_code is set but process_code isn't, copy it
        if self.test_operation_code is not None and self.process_code is None:
            self.process_code = self.test_operation_code
        # If process_code is set but test_operation_code isn't, copy it
        elif self.process_code is not None and self.test_operation_code is None:
            self.test_operation_code = self.process_code
        
        # Same for names
        if self.test_operation_name is not None and self.process_name is None:
            self.process_name = self.test_operation_name
        elif self.process_name is not None and self.test_operation_name is None:
            self.test_operation_name = self.process_name
        
        return self
    
    def validate_dual_process_codes(self) -> tuple[bool, str]:
        """
        Validate that both process codes are properly set.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        if self.repair_process_code is None:
            errors.append("Repair process code is required")
        
        if self.test_operation_code is None:
            errors.append("Test operation code is required")
        
        if not self.repair_process_name:
            errors.append("Repair process name is required")
        
        if not self.test_operation_name:
            errors.append("Test operation name is required")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, ""
    
    def to_uur_type_dict(self) -> dict:
        """
        Convert to WRML UUR_type representation.
        
        Returns:
            Dictionary representing UUR_type structure
        """
        result: dict = {
            'process': {
                'code': self.test_operation_code,
                'code_specified': self.test_operation_code is not None,
                'name': self.test_operation_name
            },
            'active': self.active,
            'active_specified': True,
            'referenced_uut': str(self.ref_uut) if self.ref_uut else None
        }
        
        if self.test_operation_guid:
            result['process']['guid'] = str(self.test_operation_guid)
        
        if self.confirm_date:
            result['confirm_date'] = self.confirm_date.isoformat()
            result['confirm_date_specified'] = True
        
        if self.finalize_date:
            result['finalize_date'] = self.finalize_date.isoformat()
            result['finalize_date_specified'] = True
        
        if self.exec_time is not None:
            result['execution_time'] = self.exec_time
            result['execution_time_specified'] = True
        
        return result
    
    def to_dict(self) -> dict:
        """
        Enhanced dictionary representation with dual process codes.
        
        Returns:
            Dictionary with all UURInfo fields
        """
        return {
            # Dual process architecture
            'repair_process_code': self.repair_process_code,
            'repair_process_name': self.repair_process_name,
            'test_operation_code': self.test_operation_code,
            'test_operation_name': self.test_operation_name,
            'test_operation_guid': str(self.test_operation_guid) if self.test_operation_guid else None,
            
            # UUR-specific properties
            'referenced_uut_guid': str(self.ref_uut) if self.ref_uut else None,
            'confirm_date': self.confirm_date.isoformat() if self.confirm_date else None,
            'finalize_date': self.finalize_date.isoformat() if self.finalize_date else None,
            'active': self.active,
            
            # API-required fields
            'process_code': self.process_code,
            'process_name': self.process_name,
            'process_code_format': self.process_code_format
        }

