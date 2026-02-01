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
    UUR-specific information (serialized as 'uur' object).
    
    IMPORTANT: UUR reports have dual process codes:
    
    1. Report.process_code (top-level) = Repair operation code (500, 510, etc.)
       - What KIND of repair this is
       - Example: 500 = "Repair", 510 = "RMA Repair"
    
    2. UURInfo.process_code (uur object) = Test operation code (100, 50, etc.)
       - What TEST was being performed when the failure occurred
       - Example: 100 = "End of line test", 50 = "PCBA test"
    
    This dual architecture allows tracking:
    - What repair work was done (Report.process_code)
    - What test operation caused the failure (UURInfo.process_code)
    
    C# Name: UUR_type
    """
    
    # ========================================================================
    # Test Operation Reference (What test was running when failure occurred)
    # ========================================================================
    
    process_code: Optional[int] = Field(
        default=None,
        validation_alias="processCode",
        serialization_alias="processCode",
        description="Test operation code that was running when failure occurred. Required by API in uur object."
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
        description="Test operation name that was running."
    )
    
    # Deprecated aliases for clarity (use process_code/process_name instead)
    test_operation_code: Optional[int] = Field(
        default=None,
        validation_alias="testOperationCode",
        serialization_alias="testOperationCode",
        deprecated=True,
        description="DEPRECATED: Use process_code. Original test operation code."
    )
    
    test_operation_name: Optional[str] = Field(
        default=None,
        validation_alias="testOperationName",
        serialization_alias="testOperationName",
        deprecated=True,
        description="DEPRECATED: Use process_name. Original test operation name."
    )
    
    test_operation_guid: Optional[UUID] = Field(
        default=None,
        validation_alias="testOperationGuid",
        serialization_alias="testOperationGuid",
        description="Test operation GUID."
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
        
        NOTE: Repair process information is stored in the parent Report object's
        process_code and process_name fields, not in UURInfo.
        This method is deprecated - access Report.process_code directly.
        
        Returns:
            Dictionary with repair process details (DEPRECATED)
        """
        # Repair info is in the parent Report, not in UURInfo!
        # This method can't access it. Returning empty structure for backward compatibility.
        return {
            'code': None,
            'name': None,
            'type': 'repair',
            'deprecated': 'Use Report.process_code instead'
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
        Set test process code (the test that was running when failure occurred).
        
        NOTE: This method is deprecated. The repair_code/repair_name parameters
        are ignored - repair information belongs in the parent Report object,
        not in UURInfo.
        
        Args:
            repair_code: IGNORED (repair info is in Report.process_code)
            repair_name: IGNORED (repair info is in Report.process_name)
            test_code: Code for the test that was running
            test_name: Name for the test that was running
            test_guid: GUID for the test operation
        """
        # NOTE: repair_code and repair_name are IGNORED
        # Repair info must be set on the parent UURReport.process_code
        
        # Set test operation (what was running when failure occurred)
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
        Validate that test process code is properly set.
        
        NOTE: This method only validates UURInfo fields (test operation).
        Repair process validation must be done on the parent Report object.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        # Only validate test operation (what was running when failure occurred)
        # Repair operation validation belongs in Report
        if self.test_operation_code is None and self.process_code is None:
            errors.append("Test operation code is required (process_code or test_operation_code)")
        
        if not self.test_operation_name and not self.process_name:
            errors.append("Test operation name is required (process_name or test_operation_name)")
        
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
        Enhanced dictionary representation of UURInfo.
        
        NOTE: Repair process info is in parent Report, not in UURInfo.
        This only includes test operation information.
        
        Returns:
            Dictionary with all UURInfo fields
        """
        return {
            # Test operation (what was running when failure occurred)
            'test_operation_code': self.test_operation_code,
            'test_operation_name': self.test_operation_name,
            'test_operation_guid': str(self.test_operation_guid) if self.test_operation_guid else None,
            
            # UUR-specific properties
            'referenced_uut_guid': str(self.ref_uut) if self.ref_uut else None,
            'confirm_date': self.confirm_date.isoformat() if self.confirm_date else None,
            'finalize_date': self.finalize_date.isoformat() if self.finalize_date else None,
            'active': self.active,
            
            # API-required fields (aliases for test operation)
            'process_code': self.process_code,
            'process_name': self.process_name,
            'process_code_format': self.process_code_format
        }

