"""
UURSubUnit - v3 Implementation

Extended sub-unit for UUR reports with repair-specific fields.
Inherits from SubUnit base class for proper type compatibility.
"""
from __future__ import annotations

from typing import Optional, List

from ..common_types import Field
from ..sub_unit import SubUnit
from .uur_failure import UURFailure


class UURSubUnit(SubUnit):
    """
    Extended sub-unit for UUR (repair) reports.
    
    Extends SubUnit with repair-specific fields:
    - idx: Unit index (0 = main unit)
    - parent_idx: Parent unit index for hierarchy
    - failures: List of failures found on this unit
    - replaced_idx: Index of unit this replaced
    
    C# Name: SubUnit (in UUR context)
    """
    
    # Note: pn, sn, rev inherited from SubUnit
    # Override sn to make it optional for main unit
    sn: str = Field(  # type: ignore[assignment]
        default="",
        max_length=100,
        description="Serial number (can be empty for main unit)."
    )
    
    part_type: Optional[str] = Field(
        default="Unknown",
        max_length=50,
        validation_alias="partType",
        serialization_alias="partType",
        description="Type of unit."
    )
    
    # ========================================================================
    # Repair-Specific Fields
    # ========================================================================
    
    idx: int = Field(
        default=0,
        description="Unit index. Index 0 is the main unit being repaired."
    )
    
    parent_idx: Optional[int] = Field(
        default=None,
        validation_alias="parentIdx",
        serialization_alias="parentIdx",
        description="Index of parent unit (for sub-assembly hierarchy)."
    )
    
    position: Optional[int] = Field(
        default=None,
        description="Position of unit within parent."
    )
    
    replaced_idx: Optional[int] = Field(
        default=None,
        validation_alias="replacedIdx",
        serialization_alias="replacedIdx",
        description="Index of unit this unit replaced (for component swaps)."
    )
    
    # ========================================================================
    # Failures
    # ========================================================================
    
    failures: Optional[List[UURFailure]] = Field(
        default=None,
        description="List of failures found on this unit."
    )
    
    # ========================================================================
    # Factory Methods
    # ========================================================================
    
    @classmethod
    def create_main_unit(
        cls,
        pn: str,
        sn: str,
        rev: str = ""
    ) -> "UURSubUnit":
        """
        Create the main unit (idx=0) for a UUR report.
        
        Args:
            pn: Part number
            sn: Serial number
            rev: Revision
            
        Returns:
            UURSubUnit configured as main unit.
        """
        return cls(
            pn=pn,
            sn=sn,
            rev=rev,
            idx=0,
            part_type="Main"
        )
    
    # ========================================================================
    # Failure Management
    # ========================================================================
    
    def add_failure(
        self,
        category: str,
        code: str,
        *,
        comment: Optional[str] = None,
        com_ref: Optional[str] = None,
        func_block: Optional[str] = None,
        ref_step_id: Optional[int] = None,
        ref_step_name: Optional[str] = None,
        art_number: Optional[str] = None,
        art_rev: Optional[str] = None,
        art_vendor: Optional[str] = None,
        art_description: Optional[str] = None,
    ) -> UURFailure:
        """
        Add a failure to this sub-unit.
        
        Args:
            category: Failure category
            code: Failure code
            comment: Optional comment
            com_ref: Component reference (e.g., 'C12')
            func_block: Functional block
            ref_step_id: ID of UUT step that found this
            ref_step_name: Name of UUT step that found this
            art_number: Article/part number of failed component
            art_rev: Component revision
            art_vendor: Component vendor
            art_description: Component description
            
        Returns:
            The created UURFailure.
        """
        failure = UURFailure(
            category=category,
            code=code,
            comment=comment,
            com_ref=com_ref,
            func_block=func_block,
            ref_step_id=ref_step_id,
            ref_step_name=ref_step_name,
            art_number=art_number,
            art_rev=art_rev,
            art_vendor=art_vendor,
            art_description=art_description,
        )
        
        if self.failures is None:
            self.failures = []
        self.failures.append(failure)
        
        return failure
    
    def get_failures(self) -> List[UURFailure]:
        """Get all failures (empty list if none)."""
        return self.failures or []
    
    def has_failures(self) -> bool:
        """Check if this unit has any failures."""
        return bool(self.failures)
