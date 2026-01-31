"""
Step Base Class - v3 Implementation

Abstract base class for all test steps with proper type annotations.
Fixes:
- Parent type properly annotated for forward reference
- Failure propagation with type safety
- Step path traversal
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Optional,
    Union,
    List,
    ClassVar,
    Any,
    Annotated,
)
from abc import ABC, abstractmethod

from ..common_types import (
    WATSBase,
    Field,
    StepStatus,
    StepGroup,
)
from ..chart import Chart, ChartType
from ..binary_data import Attachment, AdditionalData, LoopInfo

# Forward reference for parent - avoids circular import
if TYPE_CHECKING:
    from .steps.sequence_call import SequenceCall


class Step(WATSBase, ABC):
    """
    Abstract base class for all WATS test steps.
    
    Provides common fields and functionality for all step types:
    - Step identification (name, type, status)
    - Parent/child relationship management
    - Failure propagation through hierarchy
    - Attachments and additional data
    
    Subclasses must implement:
    - validate_step(): Step-specific validation logic
    """
    
    # ========================================================================
    # Class Variables
    # ========================================================================
    
    MAX_NAME_LENGTH: ClassVar[int] = 100
    
    # ========================================================================
    # Parent Reference (Internal Use Only)
    # ========================================================================
    
    # Parent step - excluded from serialization
    # Using Any type to avoid forward reference issues with SequenceCall
    # At runtime, this will be a SequenceCall instance
    parent: Optional[Any] = Field(
        default=None, 
        exclude=True,
        description="Parent SequenceCall (internal use, not serialized)."
    )
    
    # Control whether failures propagate to parent
    fail_parent_on_failure: bool = Field(
        default=True,
        exclude=True,
        description="If True, failure status propagates to parent in Active mode."
    )
    
    # ========================================================================
    # Core Step Fields
    # ========================================================================
    
    # Step type discriminator - overridden by subclasses with specific Literal
    step_type: str = Field(
        default="NONE",
        validation_alias="stepType",
        serialization_alias="stepType",
        description="Step type identifier for polymorphic deserialization."
    )
    
    # Step name
    name: str = Field(
        default="StepName",
        max_length=100,
        min_length=1,
        description="Step name/title."
    )
    
    # Step group: Setup, Main, or Cleanup
    group: str = Field(
        default="M",
        max_length=1,
        min_length=1,
        pattern='^[SMC]$',
        description="Step group: S=Setup, M=Main, C=Cleanup."
    )
    
    # Step status
    status: StepStatus = Field(
        default=StepStatus.Passed,
        description="Step execution status."
    )
    
    # Optional step ID
    id: Optional[Union[int, str]] = Field(
        default=None,
        description="Optional step identifier."
    )
    
    # ========================================================================
    # Error Information
    # ========================================================================
    
    error_code: Optional[Union[int, str]] = Field(
        default=None,
        validation_alias="errorCode",
        serialization_alias="errorCode",
        description="Error code if step failed."
    )
    
    error_code_format: Optional[str] = Field(
        default=None,
        validation_alias="errorCodeFormat",
        serialization_alias="errorCodeFormat",
        description="Format string for error code display."
    )
    
    error_message: Optional[str] = Field(
        default=None,
        validation_alias="errorMessage",
        serialization_alias="errorMessage",
        description="Error message if step failed."
    )
    
    report_text: Optional[str] = Field(
        default=None,
        validation_alias="reportText",
        serialization_alias="reportText",
        description="Additional report text."
    )
    
    # ========================================================================
    # Timing Fields
    # ========================================================================
    
    start: Optional[str] = Field(
        default=None,
        description="Step start time."
    )
    
    tot_time: Optional[Union[float, str]] = Field(
        default=None,
        validation_alias="totTime",
        serialization_alias="totTime",
        description="Total execution time in seconds."
    )
    
    tot_time_format: Optional[str] = Field(
        default=None,
        validation_alias="totTimeFormat",
        serialization_alias="totTimeFormat",
        description="Format string for time display."
    )
    
    # TestStand GUID
    ts_guid: Optional[str] = Field(
        default=None,
        validation_alias="tsGuid",
        serialization_alias="tsGuid",
        description="TestStand step GUID."
    )
    
    # ========================================================================
    # Failure Flags (Read-Only from Server)
    # ========================================================================
    
    caused_seq_failure: Optional[bool] = Field(
        default=None,
        validation_alias="causedSeqFailure",
        serialization_alias="causedSeqFailure",
        description="Whether this step caused the sequence to fail."
    )
    
    caused_uut_failure: Optional[bool] = Field(
        default=None,
        validation_alias="causedUUTFailure",
        serialization_alias="causedUUTFailure",
        description="Whether this step caused the UUT to fail."
    )
    
    # ========================================================================
    # Additional Data
    # ========================================================================
    
    # Loop information for steps in loops
    loop: Optional[LoopInfo] = Field(
        default=None,
        description="Loop iteration information."
    )
    
    # Additional structured results
    additional_results: Optional[List[AdditionalData]] = Field(
        default=None,
        validation_alias="additionalResults",
        serialization_alias="additionalResults",
        description="Additional result data."
    )
    
    # Chart attached to step
    chart: Optional[Chart] = Field(
        default=None,
        description="Chart visualization data."
    )
    
    # File attachment
    attachment: Optional[Attachment] = Field(
        default=None,
        description="File attachment."
    )
    
    # ========================================================================
    # Failure Propagation (Active Mode)
    # ========================================================================
    
    def propagate_failure(self) -> None:
        """
        Propagate failure status up the step hierarchy.
        
        When called, sets this step's status to Failed and recursively
        propagates to parent steps if fail_parent_on_failure is True.
        
        This is called automatically in Active mode when a measurement
        fails and fail_parent_on_failure=True.
        """
        self.status = StepStatus.Failed
        
        if self.fail_parent_on_failure and self.parent is not None:
            self.parent.propagate_failure()
    
    # ========================================================================
    # Path Navigation
    # ========================================================================
    
    def get_step_path(self) -> str:
        """
        Get the full path to this step in the hierarchy.
        
        Returns a '/'-separated path like:
            "MainSequence Callback/SubSequence/TestStep"
        
        Returns:
            The full path from root to this step.
        """
        path: List[str] = []
        current_step: Optional[Step] = self
        
        while current_step is not None:
            path.append(current_step.name)
            current_step = current_step.parent
            
        return '/'.join(reversed(path))
    
    # ========================================================================
    # Chart and Attachment Helpers
    # ========================================================================
    
    def add_chart(
        self,
        chart_type: ChartType,
        chart_label: str,
        x_label: str,
        x_unit: str,
        y_label: str,
        y_unit: str
    ) -> Chart:
        """
        Add a chart to this step.
        
        Args:
            chart_type: Type of chart (LineChart, XYGraph, etc.)
            chart_label: Chart title
            x_label: X-axis label
            x_unit: X-axis unit
            y_label: Y-axis label
            y_unit: Y-axis unit
            
        Returns:
            The created Chart object for adding series data.
        """
        self.chart = Chart(
            chart_type=chart_type,
            label=chart_label,
            x_label=x_label,
            y_label=y_label,
            x_unit=x_unit,
            y_unit=y_unit
        )
        return self.chart
    
    def add_attachment(self, attachment: Attachment) -> None:
        """
        Add an attachment to this step.
        
        Args:
            attachment: The Attachment object to add.
        """
        self.attachment = attachment
    
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
            The created Attachment object.
        """
        self.attachment = Attachment.from_file(file_path, content_type, description)
        return self.attachment
    
    # ========================================================================
    # Validation (Abstract)
    # ========================================================================
    
    @abstractmethod
    def validate_step(
        self, 
        trigger_children: bool = False, 
        errors: Optional[List[str]] = None
    ) -> bool:
        """
        Validate this step.
        
        Subclasses must implement step-specific validation logic.
        
        Args:
            trigger_children: If True, also validate child steps (for SequenceCall)
            errors: List to append error messages to
            
        Returns:
            True if validation passes, False otherwise.
        """
        return True
