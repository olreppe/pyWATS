"""Backward compatibility shim - use pywats.domains.analytics instead.

DEPRECATED: This module is deprecated. Import from pywats.domains.analytics instead.

Example:
    # Old (deprecated)
    from pywats.domains.app import AppService
    
    # New (preferred)
    from pywats.domains.analytics import AnalyticsService
"""
import warnings

# Re-export everything from analytics for backward compatibility
from ..analytics import (
    YieldDataType,
    ProcessType,
    YieldData,
    ProcessInfo,
    LevelInfo,
    ProductGroup,
    StepAnalysisRow,
    # New typed models
    TopFailedStep,
    RepairStatistics,
    RepairHistoryRecord,
    MeasurementData,
    AggregatedMeasurement,
    OeeAnalysisResult,
    # Repository & Service
    AnalyticsRepository,
    AnalyticsService,
    # Backward compatibility aliases
    AppRepository,
    AppService,
)

__all__ = [
    # Enums
    "YieldDataType",
    "ProcessType",
    # Models
    "YieldData",
    "ProcessInfo",
    "LevelInfo",
    "ProductGroup",
    "StepAnalysisRow",
    # New typed models
    "TopFailedStep",
    "RepairStatistics",
    "RepairHistoryRecord",
    "MeasurementData",
    "AggregatedMeasurement",
    "OeeAnalysisResult",
    # Repository & Service (new names)
    "AnalyticsRepository",
    "AnalyticsService",
    # Deprecated aliases
    "AppRepository",
    "AppService",
]

