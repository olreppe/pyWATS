"""Report domain.

Provides services and repository for test reports (UUT/UUR).
The models are re-exported from the existing models package.
"""
# Re-export existing report models - these are complex and well-established
from ...models.report import (
    UUTReport,
    UURReport,
    Report,
    MiscInfo,
    Step,
    StepStatus,
)
from ...models.report.uut.steps.sequence_call import SequenceCall, StepList

# Import query-related models
from .enums import DateGrouping
from .models import WATSFilter, ReportHeader, Attachment

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
    "Step",
    "StepStatus",
    "MiscInfo",
    # Query Models
    "WATSFilter",
    "ReportHeader",
    "Attachment",
    # Enums
    "DateGrouping",
    # Service & Repository
    "ReportService",
    "ReportRepository",
]
