"""
SequenceCall - v3 Implementation

Container step that holds child steps. Core of the test hierarchy.

Fixes:
- Factory methods with proper parent=self typing
- StepList with proper Generic parameter
- Caller field typed correctly
- Uses sequence object (serializes to seqCall) like V1 for WATS API compatibility
"""
from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Literal,
    Union,
    overload,
)

from ..step import Step
from .step_list import StepList
from .numeric_step import NumericStep, MultiNumericStep, NumericMeasurement
from .boolean_step import PassFailStep, MultiBooleanStep
from .string_step import StringValueStep, MultiStringStep
from .generic_step import GenericStep, FlowType
from .action_step import ActionStep
from .chart_step import ChartStep
from .unknown_step import UnknownStep
from ...common_types import (
    Field,
    StepStatus,
    StepGroup,
    CompOp,
    SequenceCallInfo,
)


# Type alias for all step types
# NOTE: UnknownStep MUST be last - Pydantic tries unions in order,
# and UnknownStep can match any step_type string value
StepType = Union[
    "SequenceCall",
    NumericStep,
    MultiNumericStep,
    PassFailStep,
    MultiBooleanStep,
    StringValueStep,
    MultiStringStep,
    GenericStep,
    ActionStep,
    ChartStep,
    UnknownStep,  # Fallback for unrecognized step types
]


class SequenceCall(Step):
    """
    Sequence call step - container for child steps.
    
    SequenceCall represents a call to a subsequence and contains the
    steps executed within that subsequence. This is the primary container
    for building test hierarchies.
    
    C# Name: SequenceCall
    
    Factory Methods:
        - add_numeric_step(): Add a NumericStep
        - add_boolean_step(): Add a PassFailStep
        - add_string_step(): Add a StringValueStep
        - add_sequence_call(): Add a nested SequenceCall
        - add_action_step(): Add an ActionStep
        - add_generic_step(): Add a GenericStep
        - add_chart_step(): Add a ChartStep
    
    Example:
        root = SequenceCall(name="MainSequence")
        root.add_numeric_step(name="Voltage", value=5.0, comp_op=CompOp.GELE, low_limit=4.5, high_limit=5.5)
        sub = root.add_sequence_call("SubTests")
        sub.add_boolean_step(name="LED Check", value=True)
    """
    
    # Step type discriminator - accepts both "SequenceCall" and "WATS_SeqCall" for compatibility
    step_type: Literal["SequenceCall", "WATS_SeqCall"] = Field(
        default="SequenceCall",
        validation_alias="stepType",
        serialization_alias="stepType",
    )
    
    # ========================================================================
    # Sequence-Specific Fields
    # ========================================================================
    
    # Sequence call info - contains path, name, version (serializes to seqCall)
    sequence: SequenceCallInfo = Field(
        default_factory=SequenceCallInfo,
        validation_alias="seqCall",
        serialization_alias="seqCall",
        description="Sequence file information."
    )
    
    # Caller sequence name (TestStand)
    caller: Optional[str] = Field(
        default=None,
        description="Name of the calling sequence."
    )
    
    # Module name
    module: Optional[str] = Field(
        default=None,
        description="Module or library name."
    )
    
    # ========================================================================
    # Child Steps
    # ========================================================================
    
    # List of child steps - this is the key container
    steps: StepList[StepType] = Field(
        default_factory=StepList,
        description="Child steps within this sequence."
    )
    
    def __init__(self, **data) -> None:
        """Initialize SequenceCall and set parent on StepList."""
        super().__init__(**data)
        # Ensure StepList has this as parent and inject parent into all child steps
        if isinstance(self.steps, StepList):
            self.steps.parent = self
        # Also set parent on each individual step (for cases where StepList.parent wasn't 
        # set during deserialization)
        for step in self.steps:
            step.parent = self

    # ========================================================================
    # Factory Methods - Create and Add Steps
    # ========================================================================
    
    def add_step(self, step: StepType) -> StepType:
        """
        Add an existing step to this sequence.
        
        Args:
            step: The step to add
            
        Returns:
            The added step (same instance, with parent set)
        """
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_numeric_step(
        self,
        *,
        name: str,
        value: float | str,
        unit: str = "NA",
        comp_op: CompOp = CompOp.LOG,
        low_limit: float | str | None = None,
        high_limit: float | str | None = None,
        status: StepStatus | str | None = None,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
        fail_parent_on_failure: bool = True,
    ) -> NumericStep:
        """
        Add a numeric limit test step.
        
        Args:
            name: Step name
            value: Measured value
            unit: Unit of measurement (default "NA")
            comp_op: Comparison operator (default LOG = log only)
            low_limit: Low limit value
            high_limit: High limit value
            status: Step status (None = auto-calculate in Active mode)
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            fail_parent_on_failure: Propagate failure to parent
            
        Returns:
            The created NumericStep.
        """
        from pywats.domains.report.import_mode import is_active_mode
        
        # Determine status
        explicit_status_provided = status is not None
        
        if status is None:
            final_status = StepStatus.Passed
        elif isinstance(status, str):
            final_status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
        else:
            final_status = status
        
        step = NumericStep.create(
            name=name,
            value=value,
            unit=unit,
            comp_op=comp_op,
            low_limit=low_limit,
            high_limit=high_limit,
            status=final_status,
        )
        step.id = id
        step.group = group
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.fail_parent_on_failure = fail_parent_on_failure
        step.parent = self
        self.steps.append(step)
        
        # In Active mode, auto-calculate status if not explicitly provided
        if is_active_mode() and not explicit_status_provided:
            if step.measurement is not None:
                calculated_status = step.measurement.calculate_status()
                if calculated_status == "F":
                    step.status = StepStatus.Failed
                    if step.measurement:
                        step.measurement.status = StepStatus.Failed
                    # Propagate failure to parent
                    if fail_parent_on_failure:
                        self.propagate_failure()
        
        return step
    
    def add_multi_numeric_step(
        self,
        *,
        name: str,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> MultiNumericStep:
        """
        Add a multi-numeric limit test step.
        
        Args:
            name: Step name
            status: Step status
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created MultiNumericStep (add measurements via add_measurement).
        """
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
            
        step = MultiNumericStep(
            name=name,
            status=status,
            group=group,
        )
        step.id = id
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_boolean_step(
        self,
        *,
        name: str,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> PassFailStep:
        """
        Add a boolean/pass-fail test step.
        
        Args:
            name: Step name
            status: Step status ("P", "F", or StepStatus)
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created PassFailStep.
        """
        # Convert string status to bool value
        if isinstance(status, str):
            value = status == "P"
            status_enum = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
        else:
            value = status == StepStatus.Passed
            status_enum = status
        
        step = PassFailStep.create(
            name=name,
            value=value,
            status=status_enum,
        )
        step.id = id
        step.group = group
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    # Alias for clarity
    add_pass_fail_step = add_boolean_step
    
    def add_string_step(
        self,
        *,
        name: str,
        value: str,
        unit: str = "NA",
        comp_op: CompOp = CompOp.LOG,
        limit: str | None = None,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> StringValueStep:
        """
        Add a string value test step.
        
        Args:
            name: Step name
            value: Measured string
            unit: Unit (default "NA")
            comp_op: Comparison operator
            limit: Expected string
            status: Step status
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created StringValueStep.
        """
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
            
        step = StringValueStep.create(
            name=name,
            value=value,
            comp_op=comp_op,
            limit=limit,
            status=status,
        )
        step.id = id
        step.group = group
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_multi_string_step(
        self,
        *,
        name: str,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> MultiStringStep:
        """
        Add a multi-string test step.
        
        Args:
            name: Step name
            status: Step status
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created MultiStringStep.
        """
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
            
        step = MultiStringStep(
            name=name,
            status=status,
            group=group,
        )
        step.id = id
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_multi_boolean_step(
        self,
        *,
        name: str,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> MultiBooleanStep:
        """
        Add a multi-boolean test step.
        
        Args:
            name: Step name
            status: Step status
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created MultiBooleanStep.
        """
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
            
        step = MultiBooleanStep(
            name=name,
            status=status,
            group=group,
        )
        step.id = id
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_sequence_call(
        self,
        name: str,
        *,
        caller: str | None = None,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
        file_name: str = "TestSequence.seq",
        path: str = "C:/SequenceCall.seq",
        version: str = "1.0.0",
    ) -> "SequenceCall":
        """
        Add a nested sequence call.
        
        Args:
            name: Sequence name
            caller: Caller sequence name
            status: Step status
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            file_name: Sequence file name
            path: Sequence file path
            version: Sequence version
            
        Returns:
            The created SequenceCall (add child steps via its factory methods).
        """
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
            
        step = SequenceCall(
            name=name,
            caller=caller,
            status=status,
            group=group,
            sequence=SequenceCallInfo(
                file_name=file_name,
                path=path,
                version=version,
            ),
        )
        step.id = id
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_action_step(
        self,
        name: str,
        *,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> ActionStep:
        """
        Add an action step.
        
        Args:
            name: Step name
            status: Step status
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created ActionStep.
        """
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
            
        step = ActionStep(
            name=name,
            status=status,
            group=group,
        )
        step.id = id
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_generic_step(
        self,
        *,
        step_type: FlowType | str,
        name: str,
        status: StepStatus | str = StepStatus.Passed,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> GenericStep:
        """
        Add a generic step.
        
        Args:
            step_type: Type of generic step (FlowType enum or string)
            name: Step name
            status: Step status
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created GenericStep.
        """
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
        
        # Convert FlowType enum to string
        step_type_str = step_type.value if isinstance(step_type, FlowType) else step_type
            
        step = GenericStep(
            name=name,
            step_type=step_type_str,  # type: ignore[arg-type]  # FlowType values are valid GenericStep types
            report_text=report_text,
            status=status,
            group=group,
        )
        step.id = id
        step.error_code = error_code
        step.error_message = error_message
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    def add_chart_step(
        self,
        name: str,
        *,
        chart_type: str = "LineChart",
        status: StepStatus | str = StepStatus.Passed,
        label: str = "Chart",
        x_label: str = "X",
        x_unit: str | None = None,
        y_label: str = "Y",
        y_unit: str | None = None,
        series: list | None = None,
        id: int | str | None = None,
        group: str = "M",
        error_code: int | str | None = None,
        error_message: str | None = None,
        report_text: str | None = None,
        start: str | None = None,
        tot_time: float | str | None = None,
    ) -> ChartStep:
        """
        Add a chart step.
        
        Args:
            name: Step name
            chart_type: Type of chart (LineChart, Histogram, etc.)
            status: Step status
            label: Chart title/label
            x_label: X-axis label
            x_unit: X-axis unit
            y_label: Y-axis label
            y_unit: Y-axis unit
            series: List of chart series
            id: Step ID
            group: Step group (S/M/C)
            error_code: Error code on failure
            error_message: Error message on failure
            report_text: Report text
            start: Start time
            tot_time: Total execution time
            
        Returns:
            The created ChartStep.
        """
        from ...chart import Chart
        
        if isinstance(status, str):
            status = StepStatus(status) if status in ("P", "F", "D", "E", "T", "S") else StepStatus.Passed
            
        step = ChartStep(
            name=name,
            status=status,
            group=group,
        )
        step.chart = Chart(
            chart_type=chart_type,  # type: ignore[arg-type]
            label=label,
            x_label=x_label,
            x_unit=x_unit or "",
            y_label=y_label,
            y_unit=y_unit or "",
            series=series or [],
        )
        step.id = id
        step.error_code = error_code
        step.error_message = error_message
        step.report_text = report_text
        step.start = start
        step.tot_time = tot_time
        step.parent = self
        self.steps.append(step)
        return step
    
    # ========================================================================
    # Validation
    # ========================================================================
    
    def validate_step(
        self,
        trigger_children: bool = False,
        errors: Optional[List[str]] = None
    ) -> bool:
        """
        Validate this sequence and optionally all child steps.
        
        Args:
            trigger_children: If True, recursively validate child steps
            errors: List to append error messages to
            
        Returns:
            True if all validations pass.
        """
        if errors is None:
            errors = []
            
        all_passed = True
        
        if trigger_children:
            for step in self.steps:
                if not step.validate_step(trigger_children=True, errors=errors):
                    all_passed = False
                    
        if not all_passed:
            self.status = StepStatus.Failed
            
        return all_passed
    
    # ========================================================================
    # Traversal and Search
    # ========================================================================
    
    def find_step(self, name: str, recursive: bool = True) -> Optional[Step]:
        """
        Find a step by name.
        
        Args:
            name: Step name to find
            recursive: If True, search child sequences too
            
        Returns:
            The first matching step, or None.
        """
        for step in self.steps:
            if step.name == name:
                return step
            if recursive and isinstance(step, SequenceCall):
                found = step.find_step(name, recursive=True)
                if found:
                    return found
        return None
    
    def find_all_steps(
        self, 
        name: str | None = None,
        step_type: type | None = None,
        recursive: bool = True
    ) -> List[Step]:
        """
        Find all steps matching criteria.
        
        Args:
            name: Step name to match (optional)
            step_type: Step type to match (optional)
            recursive: If True, search child sequences too
            
        Returns:
            List of matching steps.
        """
        results: List[Step] = []
        
        for step in self.steps:
            matches = True
            
            if name is not None and step.name != name:
                matches = False
            if step_type is not None and not isinstance(step, step_type):
                matches = False
                
            if matches:
                results.append(step)
                
            if recursive and isinstance(step, SequenceCall):
                results.extend(step.find_all_steps(name, step_type, recursive=True))
                
        return results
    
    def get_failed_steps(self, recursive: bool = True) -> List[Step]:
        """
        Get all failed steps.
        
        Args:
            recursive: If True, include failed steps from child sequences
            
        Returns:
            List of failed steps.
        """
        results: List[Step] = []
        
        for step in self.steps:
            if step.status == StepStatus.Failed:
                results.append(step)
                
            if recursive and isinstance(step, SequenceCall):
                results.extend(step.get_failed_steps(recursive=True))
                
        return results
    
    def count_steps(self, recursive: bool = True) -> int:
        """
        Count steps in this sequence.
        
        Args:
            recursive: If True, count steps in child sequences too
            
        Returns:
            Total step count.
        """
        count = len(self.steps)
        
        if recursive:
            for step in self.steps:
                if isinstance(step, SequenceCall):
                    count += step.count_steps(recursive=True)
                    
        return count
    
    def assign_parent(self) -> "SequenceCall":
        """
        Ensure all steps have the correct parent after model creation.
        
        This is typically called automatically during model validation,
        but can be called manually if needed.
        
        Returns:
            Self (for method chaining)
        """
        # Set parent reference for all child steps
        for step in self.steps:
            if hasattr(step, "parent"):
                step.parent = self
                # If step is a SequenceCall, recursively assign its children
                if isinstance(step, SequenceCall):
                    step.assign_parent()
        return self
    
    def print_hierarchy(self, indent: int = 0) -> None:
        """
        Recursively print the hierarchy of SequenceCall and its steps.
        
        Useful for debugging test structure.
        
        Args:
            indent: Current indentation level (internal use)
        """
        prefix = " " * (indent * 4)
        parent_name = getattr(self.parent, "name", "None") if hasattr(self, "parent") else "None"
        
        print(f"{prefix}- {self.__class__.__name__}: {self.name} (Parent: {parent_name}, Type: {self.step_type})")
        
        for step in self.steps:
            step_parent_name = getattr(step.parent, "name", "None") if hasattr(step, "parent") else "None"
            
            if isinstance(step, SequenceCall):
                step.print_hierarchy(indent + 1)
            else:
                step_type = getattr(step, "step_type", step.__class__.__name__)
                print(f"{prefix}    - {step.__class__.__name__}: {step.name} (Parent: {step_parent_name}, Type: {step_type})")
