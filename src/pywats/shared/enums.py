"""Shared enums used across pyWATS domains.

These enums provide type-safe values for common parameters across the API,
eliminating magic strings and enabling IDE autocomplete.

Usage:
    from pywats import StatusFilter, RunFilter, StepType
    
    filter = WATSFilter(status=StatusFilter.PASSED, run=RunFilter.FIRST)
"""
from enum import Enum, IntEnum
from typing import Any


class StatusFilter(str, Enum):
    """
    Status filter values for querying reports with flexible string conversion.
    
    Used for filtering reports by test outcome in WATSFilter and analytics queries.
    
    Accepts multiple input formats:
    - Member names: StatusFilter.PASSED (UPPERCASE recommended)
    - Full words: "Passed", "PASSED", "passed" (case-insensitive)
    - Short forms: "Pass", "Fail", etc.
    - Common aliases: "OK", "success", etc.
    
    Always serializes to WATS query format ("Passed", "Failed", etc.).
    
    Note: This is different from StepStatus/ReportStatus which use single-letter 
    codes ("P", "F") for WSJF submission. StatusFilter uses full words for queries.
    
    Examples:
        >>> StatusFilter("Passed")       # Full word
        >>> StatusFilter("PASSED")       # Case-insensitive
        >>> StatusFilter("pass")         # Short form
        >>> StatusFilter("OK")           # Alias
        >>> StatusFilter.PASSED.value    # Returns "Passed"
    """
    PASSED = "Passed"
    """Test passed successfully."""
    
    FAILED = "Failed"
    """Test failed with a failure condition."""
    
    ERROR = "Error"
    """Test encountered an error (not pass/fail)."""
    
    TERMINATED = "Terminated"
    """Test was terminated before completion."""
    
    DONE = "Done"
    """Test completed (neutral status, no pass/fail)."""
    
    SKIPPED = "Skipped"
    """Test was skipped."""
    
    @classmethod
    def _missing_(cls, value: Any) -> "StatusFilter":
        """
        Handle flexible string conversion.
        
        Tries:
        1. Case-insensitive match against enum values ("Passed", "Failed", etc.)
        2. Case-insensitive match against member names ("PASSED", "FAILED", etc.)
        3. Alias lookup ("OK" → "Passed", "fail" → "Failed", etc.)
        
        Raises:
            ValueError: If value cannot be converted to valid status filter
        """
        if not isinstance(value, str):
            raise ValueError(
                f"StatusFilter value must be string, got {type(value).__name__}"
            )
        
        # Try case-insensitive match against enum values
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        
        # Try case-insensitive match against member names (PASSED, FAILED, etc.)
        value_upper = value.upper()
        for member in cls:
            if member.name == value_upper:
                return member
        
        # Try alias lookup (case-insensitive)
        canonical = StatusFilter._STATUS_ALIASES.get(value.lower())
        if canonical:
            for member in cls:
                if member.value == canonical:
                    return member
        
        # No match found
        valid_options = ", ".join(m.name for m in cls)
        raise ValueError(
            f"Invalid status filter: '{value}'. "
            f"Valid options: {valid_options} "
            "(case-insensitive, also accepts single letters and aliases like 'OK')"
        )
    
    @property
    def full_name(self) -> str:
        """Get full word representation (same as value)."""
        return self.value
    
    @property
    def is_passing(self) -> bool:
        """True if status indicates a passing result."""
        return self in (StatusFilter.PASSED, StatusFilter.DONE)
    
    @property
    def is_failure(self) -> bool:
        """True if status indicates a failure."""
        return self in (StatusFilter.FAILED, StatusFilter.ERROR, StatusFilter.TERMINATED)

# Alias mappings for StatusFilter
StatusFilter._STATUS_ALIASES = {
    # Passed variations
    "pass": "Passed",
    "ok": "Passed",
    "success": "Passed",
    "successful": "Passed",
    "p": "Passed",
    
    # Failed variations
    "fail": "Failed",
    "failure": "Failed",
    "ng": "Failed",
    "f": "Failed",
    
    # Error variations
    "err": "Error",
    "e": "Error",
    
    # Terminated variations
    "term": "Terminated",
    "abort": "Terminated",
    "aborted": "Terminated",
    "t": "Terminated",
    
    # Done variations
    "complete": "Done",
    "completed": "Done",
    "d": "Done",
    
    # Skipped variations
    "skip": "Skipped",
    "s": "Skipped",
}


class RunFilter(IntEnum):
    """
    Run filter for step/measurement analysis.
    
    Specifies which run(s) to include when analyzing multi-run test data.
    
    Example:
        >>> filter = WATSFilter(run=RunFilter.FIRST)
        >>> filter = WATSFilter(run=RunFilter.ALL)
    """
    FIRST = 1
    """Only first run (first attempt)."""
    
    SECOND = 2
    """Only second run (first retest)."""
    
    THIRD = 3
    """Only third run (second retest)."""
    
    LAST = -1
    """Only last/final run for each unit."""
    
    ALL = -2
    """All runs (include retests)."""


class StepType(str, Enum):
    """
    Test step types in WATS.
    
    Used to categorize and filter steps by their function.
    These match the WATS backend step type values.
    
    Example:
        >>> # Filter for measurement steps only
        >>> [s for s in steps if s.step_type == StepType.NUMERIC_LIMIT]
    """
    # Sequence/Group steps
    SEQUENCE_CALL = "SequenceCall"
    """Call to another sequence/routine."""
    
    # Measurement steps
    NUMERIC_LIMIT = "NumericLimit"
    """Numeric measurement with limits (pass/fail based on value)."""
    
    STRING_VALUE = "StringValue"
    """String value measurement (match or comparison)."""
    
    PASS_FAIL = "PassFail"
    """Simple pass/fail step (boolean result)."""
    
    MULTIPLE_NUMERIC = "MultipleNumericLimit"
    """Multiple numeric measurements in one step."""
    
    # Action steps
    ACTION = "Action"
    """Action step (do something, no measurement)."""
    
    MESSAGE_POPUP = "MessagePopup"
    """Display a message to operator."""
    
    CALL_EXECUTABLE = "CallExecutable"
    """Call external executable/script."""
    
    # Flow control
    LABEL = "Label"
    """Label for goto/flow control."""
    
    GOTO = "Goto"
    """Goto/jump to label."""
    
    FLOW_CONTROL = "FlowControl"
    """Flow control step (if/else/loop)."""
    
    STATEMENT = "Statement"
    """Code statement/expression."""
    
    # Property steps
    PROPERTY_LOADER = "PropertyLoader"
    """Load property from storage."""
    
    # Generic
    GENERIC = "Generic"
    """Generic step type."""
    
    # Unknown/other
    UNKNOWN = "Unknown"
    """Unknown step type (for forward compatibility)."""


class CompOp(str, Enum):
    """
    Comparison operators for numeric limit steps.
    
    Defines how a measured value is compared against limits.
    Inherits from (str, Enum) for JSON serialization compatibility.
    
    Also available as CompOperator alias (alternative name).
    
    Example:
        >>> from pywats.shared.enums import CompOp
        >>> # Or use the alias:
        >>> from pywats.shared.enums import CompOperator
        >>> 
        >>> if step.comp_op == CompOp.GELE:
        ...     print("Value must be between limits (inclusive)")
    """
    # None limit compOp
    LOG = "LOG"
    """No limit - just log the value."""

    # Single limit compOp (lowLimit required, highLimit not supported)
    EQ = "EQ"
    """Equal to (==)."""
    
    EQT = "EQT"
    """Equal or Tolerant."""
    
    NE = "NE"
    """Not equal to (!=)."""
    
    LT = "LT"
    """Less than (<)."""
    
    LE = "LE"
    """Less than or equal (<=)."""
    
    GT = "GT"
    """Greater than (>)."""
    
    GE = "GE"
    """Greater than or equal (>=)."""
    
    CASESENSIT = "CASESENSIT"
    """Case-sensitive string comparison."""
    
    IGNORECASE = "IGNORECASE"
    """Case-insensitive string comparison."""

    # Dual limit compOp (both lowLimit and highLimit required)
    # Range comparisons (AND - value must be within range)
    GTLT = "GTLT"
    """Between exclusive (> low AND < high)."""
    
    GTLE = "GTLE"
    """Between (> low AND <= high)."""
    
    GELT = "GELT"
    """Between (>= low AND < high)."""
    
    GELE = "GELE"
    """Between inclusive (>= low AND <= high)."""

    # Outside range comparisons (OR - value must be outside range)
    LTGT = "LTGT"
    """Outside range (< low OR > high)."""
    
    LTGE = "LTGE"
    """Outside or equal (< low OR >= high)."""
    
    LEGT = "LEGT"
    """Outside or equal (<= low OR > high)."""
    
    LEGE = "LEGE"
    """Outside or equal (<= low OR >= high)."""

    @classmethod
    def _missing_(cls, value: object) -> "CompOp | None":
        """Handle case-insensitive enum lookup."""
        if isinstance(value, str):
            upper_value = value.upper()
            for member in cls:
                if member.value == upper_value:
                    return member
        return None

    def __str__(self) -> str:
        """Return the value for serialization."""
        return self.value

    def __repr__(self) -> str:
        """Return representation."""
        return f"CompOp.{self.name}"

    def get_limits_requirement(self) -> tuple[bool, bool]:
        """
        Returns a tuple indicating whether lowLimit and highLimit are required.
        
        Returns:
            (low_required, high_required) tuple
        """
        if self == CompOp.LOG:
            return (False, False)
        elif self in {
            CompOp.EQ, CompOp.EQT, CompOp.NE, CompOp.LT, CompOp.LE, 
            CompOp.GT, CompOp.GE, CompOp.CASESENSIT, CompOp.IGNORECASE
        }:
            return (True, False)
        else:
            return (True, True)

    def validate_limits(self, low_limit: float | None, high_limit: float | None) -> bool:
        """Validate that limits match requirements for this operator."""
        low_required, high_required = self.get_limits_requirement()
        
        if not low_required and not high_required:
            return True
        if low_required and low_limit is None:
            return False
        if high_required and high_limit is None:
            return False
        return True

    def evaluate(
        self, 
        value: float | int, 
        low_limit: float | int | None = None, 
        high_limit: float | int | None = None
    ) -> bool:
        """
        Evaluate whether a measurement value passes the comparison.
        
        Args:
            value: The measured value to evaluate
            low_limit: The low limit
            high_limit: The high limit (for dual-limit operators)
            
        Returns:
            True if the measurement passes, False if it fails
        """
        if self == CompOp.LOG:
            return True
        if self in {CompOp.CASESENSIT, CompOp.IGNORECASE, CompOp.EQT}:
            return True  # String comparisons not supported
        
        # Single-limit comparisons
        if self == CompOp.EQ:
            return value == low_limit if low_limit is not None else True
        elif self == CompOp.NE:
            return value != low_limit if low_limit is not None else True
        elif self == CompOp.GT:
            return value > low_limit if low_limit is not None else True
        elif self == CompOp.LT:
            return value < low_limit if low_limit is not None else True
        elif self == CompOp.GE:
            return value >= low_limit if low_limit is not None else True
        elif self == CompOp.LE:
            return value <= low_limit if low_limit is not None else True
        
        # Dual-limit AND comparisons
        if low_limit is None or high_limit is None:
            return True
        if self == CompOp.GTLT:
            return value > low_limit and value < high_limit
        elif self == CompOp.GELE:
            return value >= low_limit and value <= high_limit
        elif self == CompOp.GELT:
            return value >= low_limit and value < high_limit
        elif self == CompOp.GTLE:
            return value > low_limit and value <= high_limit
        
        # Dual-limit OR comparisons
        elif self == CompOp.LTGT:
            return value < low_limit or value > high_limit
        elif self == CompOp.LEGE:
            return value <= low_limit or value >= high_limit
        elif self == CompOp.LEGT:
            return value <= low_limit or value > high_limit
        elif self == CompOp.LTGE:
            return value < low_limit or value >= high_limit
        
        return True


class SortDirection(str, Enum):
    """
    Sort direction for dimension queries.
    
    Used with DimensionBuilder to specify ordering.
    
    Example:
        >>> builder = DimensionBuilder()
        >>> builder.add(KPI.UNIT_COUNT, SortDirection.DESC)
    """
    ASC = "asc"
    """Ascending order (smallest first)."""
    
    DESC = "desc"
    """Descending order (largest first)."""


class QueueItemStatus(str, Enum):
    """
    Unified status for queue items across all queue implementations.
    
    This is the single source of truth for queue item states, used by:
    - pywats.queue.MemoryQueue (in-memory API queue)
    - pywats_client.queue.PersistentQueue (file-backed client queue)
    - pywats_client.service.AsyncClientService (report submission)
    
    State transitions:
        PENDING → PROCESSING → COMPLETED (success)
                            → FAILED (error, may retry)
                            → SUSPENDED (paused, will retry)
    
    Example:
        >>> from pywats.shared import QueueItemStatus
        >>> item.status = QueueItemStatus.PROCESSING
    """
    PENDING = "pending"
    """Item is waiting to be processed."""
    
    PROCESSING = "processing"
    """Item is currently being processed."""
    
    COMPLETED = "completed"
    """Item was successfully processed."""
    
    FAILED = "failed"
    """Item processing failed (may be retried based on policy)."""
    
    SUSPENDED = "suspended"
    """Item is temporarily suspended (will retry after delay)."""
    
    @property
    def is_terminal(self) -> bool:
        """Check if this is a terminal state (no more transitions)."""
        return self in (QueueItemStatus.COMPLETED, QueueItemStatus.FAILED)
    
    @property
    def is_active(self) -> bool:
        """Check if item is active (pending or processing)."""
        return self in (QueueItemStatus.PENDING, QueueItemStatus.PROCESSING)
    
    @property
    def can_process(self) -> bool:
        """Check if item can be picked up for processing."""
        return self in (QueueItemStatus.PENDING, QueueItemStatus.SUSPENDED)
