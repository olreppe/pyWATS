"""
UURFailure - v3 Implementation

Failure record for UUR reports.
"""
from __future__ import annotations

from typing import Optional

from ..common_types import WATSBase, Field


class UURFailure(WATSBase):
    """
    Failure record for UUR sub-units.
    
    Represents a failure found during repair analysis.
    
    C# Name: Failure
    """
    
    # ========================================================================
    # Core Failure Information
    # ========================================================================
    
    category: str = Field(
        default="Unknown",
        description="Failure category."
    )
    
    code: str = Field(
        default="Unknown",
        description="Failure code."
    )
    
    comment: Optional[str] = Field(
        default=None,
        description="Failure comment/description."
    )
    
    # ========================================================================
    # Component Reference
    # ========================================================================
    
    com_ref: Optional[str] = Field(
        default=None,
        validation_alias="comRef",
        serialization_alias="comRef",
        description="Component reference (e.g., 'C12', 'R5')."
    )
    
    func_block: Optional[str] = Field(
        default=None,
        validation_alias="funcBlock",
        serialization_alias="funcBlock",
        description="Functional block reference."
    )
    
    # ========================================================================
    # UUT Reference (links failure to original test step)
    # ========================================================================
    
    ref_step_id: Optional[int] = Field(
        default=None,
        validation_alias="refStepId",
        serialization_alias="refStepId",
        description="ID of step from referenced UUT that found this failure."
    )
    
    ref_step_name: Optional[str] = Field(
        default=None,
        validation_alias="refStepName",
        serialization_alias="refStepName",
        exclude=True,  # Server doesn't accept this field
        description="Name of step from referenced UUT that found this failure (client-side only)."
    )
    
    # ========================================================================
    # Article/Component Details
    # ========================================================================
    
    art_number: Optional[str] = Field(
        default=None,
        validation_alias="artNumber",
        serialization_alias="artNumber",
        description="Article/part number of failed component."
    )
    
    art_rev: Optional[str] = Field(
        default=None,
        validation_alias="artRev",
        serialization_alias="artRev",
        description="Revision of failed component."
    )
    
    art_vendor: Optional[str] = Field(
        default=None,
        validation_alias="artVendor",
        serialization_alias="artVendor",
        description="Vendor of failed component."
    )
    
    art_description: Optional[str] = Field(
        default=None,
        validation_alias="artDescription",
        serialization_alias="artDescription",
        description="Description of failed component."
    )
