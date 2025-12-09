"""
UURPartInfo model for UUR reports.

Based on C# UURPartInfo specification - represents sub-part information with proper
part hierarchy, indexing, and failure association.
"""

from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from .uur_report import UURReport
    from .failure import Failure
    from .fail_code import FailCode


class UURPartInfo(BaseModel):
    """
    Sub part information for UUR reports.
    
    Based on C# UURPartInfo class specification.
    Replaces the basic SubRepair with full C# API compatibility.
    """
    
    def __init__(self, uur_report: 'UURReport', part_index: int, part_number: str = "",
                 serial_number: str = "", part_revision_number: str = "", 
                 part_type: str = "", parent_idx: int = 0, replaced_idx: Optional[int] = None):
        """
        Initialize UUR part info.
        
        Args:
            uur_report: Parent UUR report
            part_index: Index of sub part (0 = main unit)
            part_number: Part number of sub part
            serial_number: Sub part's serial number
            part_revision_number: Sub part revision number
            part_type: Part type of sub part
            parent_idx: Parent index of sub part (0 for single-level hierarchy)
            replaced_idx: Index of part this replaces (if any)
        """
        super().__init__()
        self._uur_report = uur_report
        self._part_index = part_index
        self._part_number = part_number
        self._serial_number = serial_number
        self._part_revision_number = part_revision_number
        self._part_type = part_type
        self._parent_idx = parent_idx
        self._replaced_idx = replaced_idx
        self._failures: List['Failure'] = []
    
    @property
    def part_type(self) -> str:
        """Part type of sub part"""
        return self._part_type
    
    @part_type.setter
    def part_type(self, value: str):
        """Set part type"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._part_type = value
    
    @property
    def part_number(self) -> str:
        """Part number of sub part"""
        return self._part_number
    
    @part_number.setter
    def part_number(self, value: str):
        """Set part number"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._part_number = value
    
    @property
    def serial_number(self) -> str:
        """Sub part's serial number"""
        return self._serial_number
    
    @serial_number.setter
    def serial_number(self, value: str):
        """Set serial number"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._serial_number = value
    
    @property
    def part_revision_number(self) -> str:
        """Sub part revision number"""
        return self._part_revision_number
    
    @part_revision_number.setter
    def part_revision_number(self, value: str):
        """Set part revision number"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._part_revision_number = value
    
    @property
    def part_index(self) -> int:
        """Index of sub part, Index 0 has to have SN/PN as main unit"""
        return self._part_index
    
    @property
    def parent_idx(self) -> int:
        """Parent index of sub part"""
        return self._parent_idx
    
    @parent_idx.setter
    def parent_idx(self, value: int):
        """Set parent index"""
        self._parent_idx = value
    
    @property
    def replaced_idx(self) -> Optional[int]:
        """If given, this sub part replaces the part with this index"""
        return self._replaced_idx
    
    @replaced_idx.setter
    def replaced_idx(self, value: Optional[int]):
        """Set replaced index"""
        self._replaced_idx = value
    
    @property
    def failures(self) -> List['Failure']:
        """Returns an array of failures to a part"""
        return self._failures.copy()
    
    def add_failure(self, fail_code: 'FailCode', component_reference: str = "", 
                   comment: str = "", step_order_number: int = 0) -> 'Failure':
        """
        Adds a failure to the repaired unit.
        
        Args:
            fail_code: Valid fail code
            component_reference: Reference to component
            comment: Comment about the failure
            step_order_number: UUT step order number that revealed this failure
            
        Returns:
            Created Failure object
        """
        # Note: This method will be implemented when UURReport is complete
        # TODO: Implement when UURReport._add_failure_internal is available
        raise NotImplementedError("add_failure will be implemented with enhanced UURReport")
    
    def get_failures_by_component(self, component_reference: str) -> List['Failure']:
        """
        Get all failures for a specific component reference.
        
        Args:
            component_reference: Component reference to search for
            
        Returns:
            List of failures for the component
        """
        # Note: This method depends on enhanced Failure model
        # TODO: Implement when Failure.component_reference is available
        return []
    
    def get_failures_by_fail_code(self, fail_code_id: UUID) -> List['Failure']:
        """
        Get all failures for a specific fail code.
        
        Args:
            fail_code_id: Fail code GUID to search for
            
        Returns:
            List of failures with the specified fail code
        """
        # Note: This method depends on enhanced Failure model
        # TODO: Implement when Failure.fail_code is available
        return []
    
    def remove_failure(self, failure: 'Failure') -> bool:
        """
        Remove a failure from this part.
        
        Args:
            failure: Failure to remove
            
        Returns:
            True if failure was removed, False if not found
        """
        try:
            self._failures.remove(failure)
            return True
        except ValueError:
            return False
    
    def validate_part_info(self) -> tuple[bool, str]:
        """
        Validate this part info.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        # Validate main unit constraints
        if self._part_index == 0:
            if not self._part_number:
                errors.append("Main unit (index 0) must have a part number")
            if not self._serial_number:
                errors.append("Main unit (index 0) must have a serial number")
        
        # Validate parent index
        if self._parent_idx < 0:
            errors.append("Parent index cannot be negative")
        
        # Validate replaced index
        if self._replaced_idx is not None and self._replaced_idx < 0:
            errors.append("Replaced index cannot be negative")
        
        # Validate failures (when enhanced Failure model is available)
        # TODO: Implement when enhanced Failure model with validate method is available
        
        if errors:
            return False, "; ".join(errors)
        
        return True, ""
    
    def to_report_unit_hierarchy_dict(self) -> dict:
        """
        Convert to WRML ReportUnitHierarchy_type representation.
        
        Returns:
            Dictionary representing ReportUnitHierarchy_type structure
        """
        result = {
            'part_type': self._part_type,
            'pn': self._part_number,  # Part Number
            'sn': self._serial_number,  # Serial Number
            'rev': self._part_revision_number,  # Revision
            'idx': self._part_index,
            'idx_specified': True,
            'parent_idx': self._parent_idx,
            'parent_idx_specified': True
        }
        
        if self._replaced_idx is not None:
            result['replaced_idx'] = self._replaced_idx
            result['replaced_idx_specified'] = True
        
        return result
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation"""
        return {
            'part_index': self._part_index,
            'part_type': self._part_type,
            'part_number': self._part_number,
            'serial_number': self._serial_number,
            'part_revision_number': self._part_revision_number,
            'parent_idx': self._parent_idx,
            'replaced_idx': self._replaced_idx,
            'failure_count': len(self._failures)
        }
    
    def __str__(self) -> str:
        return f"UURPartInfo[{self._part_index}]({self._part_number}, {self._serial_number})"
    
    def __repr__(self) -> str:
        return (f"UURPartInfo(part_index={self._part_index}, "
                f"part_number='{self._part_number}', serial_number='{self._serial_number}', "
                f"failures={len(self._failures)})")