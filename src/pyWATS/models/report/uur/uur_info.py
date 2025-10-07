"""
Enhanced UURInfo model for UUR reports.

Based on C# UURReport specification - handles dual process code architecture
(repair process vs test operation) and all missing properties.
"""

from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import Field

from ..report_info import ReportInfo


class UURInfo(ReportInfo):
    """
    UUR-specific information with dual process code architecture.
    
    Based on C# UUR_type specification with full API compatibility.
    """
    
    # Dual process codes (key architectural feature)
    repair_process_code: Optional[int] = Field(default=None, validation_alias="repairProcessCode", serialization_alias="repairProcessCode")
    """The repair process code (top-level WATSReport.Process) - what kind of repair operation this is"""
    
    repair_process_name: Optional[str] = Field(default=None, validation_alias="repairProcessName", serialization_alias="repairProcessName")
    """The repair process name"""
    
    test_operation_code: Optional[int] = Field(default=None, validation_alias="testOperationCode", serialization_alias="testOperationCode")
    """The test operation code (UUR_type.Process) - original test operation that was being performed"""
    
    test_operation_name: Optional[str] = Field(default=None, validation_alias="testOperationName", serialization_alias="testOperationName")
    """The test operation name"""
    
    test_operation_guid: Optional[UUID] = Field(default=None, validation_alias="testOperationGuid", serialization_alias="testOperationGuid")
    """The test operation GUID"""
    
    # Legacy fields (keeping for backward compatibility)
    processCode: Optional[int] = Field(default=None, validation_alias="processCode", serialization_alias="processCode")
    """Legacy field - maps to test_operation_code"""
    
    processCodeFormat: Optional[str] = Field(default=None, validation_alias="processCodeFormat", serialization_alias="processCodeFormat")
    """Legacy field - process code format"""
    
    processName: Optional[str] = Field(default=None, validation_alias="processName", serialization_alias="processName")
    """Legacy field - maps to test_operation_name"""
    
    # UUR-specific properties
    refUUT: Optional[UUID] = Field(default=None, validation_alias="refUUT", serialization_alias="refUUT")
    """Referenced UUT GUID - the GUID of the UUT report being repaired"""
    
    comment: Optional[str] = Field(default=None)
    """Comment on repair"""
    
    uur_operator: Optional[str] = Field(default=None, validation_alias="userLoginName", serialization_alias="userLoginName")
    """Name of the operator that performed the repair"""
    
    # Timing information
    confirmDate: Optional[datetime] = Field(default=None, validation_alias="confirmDate", serialization_alias="confirmDate")
    """UUR was confirmed date time (UTC) - not currently displayed in UUR report"""
    
    finalizeDate: Optional[datetime] = Field(default=None, validation_alias="finalizeDate", serialization_alias="finalizeDate")
    """UUR was finalized date time (UTC)"""
    
    executionTime: Optional[float] = Field(default=None, validation_alias="executionTime", serialization_alias="executionTime")
    """Time spent on UUR report (seconds)"""
    
    # Status flags
    active: bool = Field(default=True)
    """Whether this UUR is active"""
    
    # Hierarchy information (if needed)
    parent: Optional[UUID] = Field(default=None)
    """Parent UUR GUID (for hierarchical repairs)"""
    
    children: Optional[list[UUID]] = Field(default=None)
    """Child UUR GUIDs (for hierarchical repairs)"""
    
    def __init__(self, **data):
        """Initialize UURInfo with dual process code mapping"""
        super().__init__(**data)
        
        # Map legacy fields to new dual process architecture
        if self.processCode is not None and self.test_operation_code is None:
            self.test_operation_code = self.processCode
        
        if self.processName and not self.test_operation_name:
            self.test_operation_name = self.processName
    
    @property
    def referenced_uut_guid(self) -> Optional[UUID]:
        """Alias for refUUT (matches C# UUTGuid property)"""
        return self.refUUT
    
    @referenced_uut_guid.setter
    def referenced_uut_guid(self, value: Optional[UUID]):
        """Set referenced UUT GUID"""
        self.refUUT = value
    
    @property
    def user_login_name(self) -> Optional[str]:
        """Alias for uur_operator (matches C# property name)"""
        return self.uur_operator
    
    @user_login_name.setter
    def user_login_name(self, value: Optional[str]):
        """Set operator login name"""
        self.uur_operator = value
    
    @property
    def confirm_date(self) -> Optional[datetime]:
        """Alias for confirmDate (matches C# property name)"""
        return self.confirmDate
    
    @confirm_date.setter
    def confirm_date(self, value: Optional[datetime]):
        """Set confirm date"""
        self.confirmDate = value
    
    @property
    def finalize_date(self) -> Optional[datetime]:
        """Alias for finalizeDate (matches C# property name)"""
        return self.finalizeDate
    
    @finalize_date.setter
    def finalize_date(self, value: Optional[datetime]):
        """Set finalize date"""
        self.finalizeDate = value
    
    @property
    def execution_time(self) -> float:
        """Time spent on UUR report (seconds)"""
        return self.executionTime if self.executionTime is not None else 0.0
    
    @execution_time.setter
    def execution_time(self, value: float):
        """Set execution time"""
        self.executionTime = value
    
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
    
    def set_dual_process_codes(self, repair_code: int, repair_name: str,
                              test_code: int, test_name: str, test_guid: Optional[UUID] = None):
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
        
        # Update legacy fields for compatibility
        self.processCode = test_code
        self.processName = test_name
    
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
        result = {
            'process': {
                'code': self.test_operation_code,
                'code_specified': self.test_operation_code is not None,
                'name': self.test_operation_name
            },
            'user_login_name': self.uur_operator,
            'active': self.active,
            'active_specified': True,
            'comment': self.comment,
            'referenced_uut': str(self.refUUT) if self.refUUT else None
        }
        
        if self.test_operation_guid:
            result['process']['guid'] = str(self.test_operation_guid)
        
        if self.confirmDate:
            result['confirm_date'] = self.confirmDate.isoformat()
            result['confirm_date_specified'] = True
        
        if self.finalizeDate:
            result['finalize_date'] = self.finalizeDate.isoformat()
            result['finalize_date_specified'] = True
        
        if self.executionTime is not None:
            result['execution_time'] = self.executionTime
            result['execution_time_specified'] = True
        
        return result
    
    def to_dict(self) -> dict:
        """Enhanced dictionary representation with dual process codes"""
        # Build dictionary manually instead of calling super()
        base_dict = {}
        
        uur_dict = {
            # Dual process architecture
            'repair_process_code': self.repair_process_code,
            'repair_process_name': self.repair_process_name,
            'test_operation_code': self.test_operation_code,
            'test_operation_name': self.test_operation_name,
            'test_operation_guid': str(self.test_operation_guid) if self.test_operation_guid else None,
            
            # UUR-specific properties
            'referenced_uut_guid': str(self.refUUT) if self.refUUT else None,
            'comment': self.comment,
            'operator': self.uur_operator,
            'confirm_date': self.confirmDate.isoformat() if self.confirmDate else None,
            'finalize_date': self.finalizeDate.isoformat() if self.finalizeDate else None,
            'execution_time': self.executionTime,
            'active': self.active,
            
            # Legacy compatibility
            'process_code': self.processCode,
            'process_name': self.processName,
            'process_code_format': self.processCodeFormat
        }
        
        return {**base_dict, **uur_dict}
