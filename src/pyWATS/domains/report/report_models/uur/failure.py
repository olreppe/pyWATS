"""
Enhanced Failure model for UUR reports.

Based on C# Failure class specification - represents failures with part index
association, step order linking, fail code GUID resolution, and attachment support.
"""

from typing import List, Optional, TYPE_CHECKING
from uuid import UUID

from pydantic import BaseModel, Field
from ..wats_base import WATSBase
from ..binary_data import BinaryData

if TYPE_CHECKING:
    from .uur_report import UURReport
    from .fail_code import FailCode
    from .uur_attachment import UURAttachment


class Failure(WATSBase):
    """
    This class represents a failure found and can be connected to a UUR report or UURPartInfo.
    
    Based on C# Failure class specification with full API compatibility.
    """

    def __init__(self, uur_report: 'UURReport', fail_code_guid: str, part_idx: int = 0,
                 component_reference: str = "", comment: str = "", 
                 failed_step_order_number: int = 0):
        """
        Initialize failure.
        
        Args:
            uur_report: Parent UUR report
            fail_code_guid: GUID of the fail code
            part_idx: Index of part this failure belongs to (0 = main unit)
            component_reference: Reference to failed component
            comment: Comment about the failure
            failed_step_order_number: UUT step order that revealed this failure
        """
        super().__init__()
        self._uur_report = uur_report
        self._fail_code_guid = fail_code_guid
        self._part_idx = part_idx
        self._component_reference = component_reference
        self._comment = comment
        self._failed_step_order_number = failed_step_order_number
        
        # Denormalized fail code metadata (populated when resolved)
        self._category = ""
        self._code = ""
        self._description = ""
        
        # Article/component information
        self._article_number = ""
        self._article_revision = ""
        self._article_description = ""
        self._article_vendor = ""
        self._function_block = ""
        
        # Failure-level attachments
        self._attachments: List['UURAttachment'] = []
    
    # Legacy fields (keeping for backward compatibility)
    art_number: Optional[str] = Field(default=None, validation_alias="artNumber", serialization_alias="artNumber")
    """The article number of the failed component."""
    
    art_rev: Optional[str] = Field(default=None, validation_alias="artRev", serialization_alias="artRev")
    """The article revision of the failed component."""
    
    art_vendor: Optional[str] = Field(default=None, validation_alias="artVendor", serialization_alias="artVendor")
    """The article vendor of the failed component."""
    
    art_description: Optional[str] = Field(default=None, validation_alias="artDescription", serialization_alias="artDescription")
    """The article description of the failed component."""
    
    category: str = Field(min_length=1)
    """The failure category."""
    
    code: str = Field(min_length=1)
    """The failure category code."""
    
    comment: Optional[str] = None
    """A comment about the failure."""
    
    com_ref: Optional[str] = Field(default=None, validation_alias="comRef", serialization_alias="comRef")
    """The component reference of the failed component."""
    
    func_block: Optional[str] = Field(default=None, validation_alias="funcBlock", serialization_alias="funcBlock")
    """The group of components the failed component belongs to."""
    
    ref_step_id: Optional[int] = Field(default=None, validation_alias="refStepId", serialization_alias="refStepId")
    """The id of the step from the reference UUT report that uncovered the failure."""
    
    ref_step_name: Optional[str] = Field(default=None, validation_alias="refStepName", serialization_alias="refStepName")
    """The name of the step from the reference UUT report that uncovered the failure (read-only)."""
    
    attachments: Optional[List[BinaryData]] = Field(default=None)
    """A list of attached files or documents in binary form."""
    
    # Enhanced properties based on C# API
    @property
    def component_reference(self) -> str:
        """Reference to failed component; e.g. R12"""
        return self._component_reference
    
    @component_reference.setter
    def component_reference(self, value: str):
        """Set component reference"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._component_reference = value
        
        # Also update legacy field for compatibility
        self.com_ref = value
    
    @property
    def fail_code(self) -> Optional['FailCode']:
        """A valid fail code"""
        # Note: UURReport.get_fail_code not available yet
        # TODO: Implement when UURReport.get_fail_code is available
        return None
    
    @fail_code.setter
    def fail_code(self, value: 'FailCode'):
        """Set fail code"""
        self._fail_code_guid = str(value.id)
        # Update denormalized metadata
        self._code = value.description
        self._description = value.description
    
    @property
    def failed_step_order_number(self) -> int:
        """It is possible to link the failure to the UUT test step. Put UUT step order in here."""
        return self._failed_step_order_number
    
    @failed_step_order_number.setter
    def failed_step_order_number(self, value: int):
        """Set failed step order number"""
        self._failed_step_order_number = value
        # Also update legacy field for compatibility
        self.ref_step_id = value
    
    @property
    def part_index(self) -> int:
        """Index of part this failure belongs to (internal)"""
        return self._part_idx
    
    @part_index.setter
    def part_index(self, value: int):
        """Set part index"""
        self._part_idx = value
    
    @property
    def compref_article_number(self) -> str:
        """Article number of a component"""
        return self._article_number
    
    @compref_article_number.setter
    def compref_article_number(self, value: str):
        """Set component article number"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._article_number = value
        
        # Also update legacy field for compatibility
        self.art_number = value
    
    @property
    def compref_article_revision(self) -> str:
        """Article revision of a component"""
        return self._article_revision
    
    @compref_article_revision.setter
    def compref_article_revision(self, value: str):
        """Set component article revision"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._article_revision = value
        
        # Also update legacy field for compatibility
        self.art_rev = value
    
    @property
    def compref_article_description(self) -> str:
        """Component reference article description"""
        return self._article_description
    
    @compref_article_description.setter
    def compref_article_description(self, value: str):
        """Set component article description"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._article_description = value
        
        # Also update legacy field for compatibility
        self.art_description = value
    
    @property
    def compref_article_vendor(self) -> str:
        """Component vendor"""
        return self._article_vendor
    
    @compref_article_vendor.setter
    def compref_article_vendor(self, value: str):
        """Set component vendor"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._article_vendor = value
        
        # Also update legacy field for compatibility
        self.art_vendor = value
    
    @property
    def compref_function_block(self) -> str:
        """Component functional block (area)"""
        return self._function_block
    
    @compref_function_block.setter
    def compref_function_block(self, value: str):
        """Set component functional block"""
        # Note: API validation not available yet
        # TODO: Add validation when UURReport.api is implemented
        self._function_block = value
        
        # Also update legacy field for compatibility
        self.func_block = value
    
    @property
    def uur_attachments(self) -> List['UURAttachment']:
        """Get files attached to this failure."""
        return self._attachments.copy()
    
    def attach_file(self, file_name: str, delete_after_attach: bool = False) -> 'UURAttachment':
        """
        Attaches a file to the failure.
        
        Args:
            file_name: Full path and name of file
            delete_after_attach: If true, the file is deleted after being attached
            
        Returns:
            UURAttachment object
        """
        from .uur_attachment import UURAttachment
        
        attachment = UURAttachment(
            self._uur_report,
            file_path=file_name,
            failure_idx=self._part_idx,  # Use part index as failure index
            delete_after_attach=delete_after_attach
        )
        self._attachments.append(attachment)
        return attachment
    
    def attach_byte_array(self, label: str, content: bytes, mime_type: str = "") -> 'UURAttachment':
        """
        Attaches a byte array to the failure.
        
        Args:
            label: Will be shown in WATS as a label to the attachment
            content: Byte array (binary data) to be attached
            mime_type: MIME type for the content
            
        Returns:
            UURAttachment object
        """
        from .uur_attachment import UURAttachment
        
        if not mime_type:
            mime_type = "application/octet-stream"
        
        attachment = UURAttachment(
            self._uur_report,
            label=label,
            content=content,
            mime_type=mime_type,
            failure_idx=self._part_idx  # Use part index as failure index
        )
        self._attachments.append(attachment)
        return attachment
    
    def set_fail_code_metadata(self, category: str, code: str, description: str = ""):
        """Set denormalized fail code metadata"""
        self._category = category
        self._code = code
        self._description = description
        
        # Also update legacy fields for compatibility
        self.category = category
        self.code = code
    
    def validate_failure(self) -> tuple[bool, str]:
        """
        Validate this failure.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        # Validate fail code GUID
        if not self._fail_code_guid:
            errors.append("Fail code GUID is required")
        else:
            try:
                UUID(self._fail_code_guid)
            except ValueError:
                errors.append("Fail code GUID is not a valid UUID")
        
        # Validate part index
        if self._part_idx < 0:
            errors.append("Part index cannot be negative")
        
        # Validate component reference if provided
        if self._component_reference and len(self._component_reference) > 50:
            errors.append("Component reference cannot exceed 50 characters")
        
        # Validate attachments
        for i, attachment in enumerate(self._attachments):
            if hasattr(attachment, 'validate_size'):
                is_valid, error = attachment.validate_size()
                if not is_valid:
                    errors.append(f"Attachment {i}: {error}")
        
        if errors:
            return False, "; ".join(errors)
        
        return True, ""
    
    def to_failures_type_dict(self) -> dict:
        """
        Convert to WRML Failures_type representation.
        
        Returns:
            Dictionary representing Failures_type structure
        """
        result = {
            'failcode': self._fail_code_guid,
            'part_idx': self._part_idx,
            'comp_ref': self._component_reference,
            'code': self._code,
            'category': self._category,
            'comment': [self._comment] if self._comment else [],  # C# uses List<string>
            'step_id': self._failed_step_order_number,
            'article_number': self._article_number,
            'article_revision': self._article_revision,
            'article_description': self._article_description,
            'article_vendor': self._article_vendor,
            'function_block': self._function_block
        }
        
        return result
    
    def to_dict(self) -> dict:
        """Convert to dictionary representation"""
        return {
            'fail_code_guid': self._fail_code_guid,
            'part_idx': self._part_idx,
            'component_reference': self._component_reference,
            'comment': self._comment,
            'failed_step_order_number': self._failed_step_order_number,
            'category': self._category,
            'code': self._code,
            'description': self._description,
            'article_number': self._article_number,
            'article_revision': self._article_revision,
            'article_description': self._article_description,
            'article_vendor': self._article_vendor,
            'function_block': self._function_block,
            'attachment_count': len(self._attachments)
        }
    
    def __str__(self) -> str:
        return f"Failure(part[{self._part_idx}], {self._component_reference}, {self._code})"
    
    def __repr__(self) -> str:
        return (f"Failure(fail_code_guid='{self._fail_code_guid}', part_idx={self._part_idx}, "
                f"component_reference='{self._component_reference}')")
