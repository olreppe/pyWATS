"""Manual Inspection domain module.

Provides test sequence definition management, relation tracking,
sequence operations, and per-unit inspection details via the WATS
internal ``/api/internal/ManualInspection/`` API.
"""
from .models import (
    DefinitionStatus,
    RepairOnFailed,
    TestSequenceDefinition,
    TestSequenceProcessRelation,
    TestSequenceSiteRelation,
    TestSequenceRelation,
    TestSequenceInstance,
    RelationConflict,
    MiSequence,
)

# Async implementations (primary API)
from .async_repository import AsyncManualInspectionRepository
from .async_service import AsyncManualInspectionService

__all__ = [
    # Enums
    "DefinitionStatus",
    "RepairOnFailed",
    # Models
    "TestSequenceDefinition",
    "TestSequenceProcessRelation",
    "TestSequenceSiteRelation",
    "TestSequenceRelation",
    "TestSequenceInstance",
    "RelationConflict",
    "MiSequence",
    # Async implementations
    "AsyncManualInspectionRepository",
    "AsyncManualInspectionService",
]
