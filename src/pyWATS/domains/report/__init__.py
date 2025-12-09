"""Report domain.

Provides services and repository for test reports (UUT/UUR).
The models are re-exported from the existing models package.
"""
# Re-export existing report models - these are complex and well-established
from ...models.report import (
    UUTReport,
    UURReport,
    Report,
    SequenceCall,
    StepList,
    MiscInfo,
)
from ...models.report.common_types import (
    ResultStatus,
    StepType,
    NumericLimitComparator,
    StringLimitComparator,
)
from ...models.report.constants import (
    LIMIT_COMPARATOR_MAP,
    STRING_LIMIT_COMPARATOR_MAP,
    RESULT_STATUS_MAP,
    STEP_TYPE_MAP,
)

# Import service and repository
from .service import ReportService
from .repository import ReportRepository

__all__ = [
    # Models
    "UUTReport",
    "UURReport",
    "Report",
    "SequenceCall",
    "StepList",
    "MiscInfo",
    # Enums
    "ResultStatus",
    "StepType",
    "NumericLimitComparator",
    "StringLimitComparator",
    # Constants
    "LIMIT_COMPARATOR_MAP",
    "STRING_LIMIT_COMPARATOR_MAP",
    "RESULT_STATUS_MAP",
    "STEP_TYPE_MAP",
    # Service & Repository
    "ReportService",
    "ReportRepository",
]
