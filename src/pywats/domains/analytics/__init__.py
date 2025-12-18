"""Analytics domain module.

Provides statistics, KPIs, yield analysis, and dashboard data services.
Note: Maps to the WATS /api/App/* endpoints (backend naming).
"""
from .enums import YieldDataType, ProcessType
from .models import YieldData, ProcessInfo, LevelInfo, ProductGroup, StepAnalysisRow
from .repository import AnalyticsRepository
from .service import AnalyticsService

# Backward compatibility aliases (deprecated)
AppRepository = AnalyticsRepository
AppService = AnalyticsService

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
    # Repository & Service
    "AnalyticsRepository",
    "AnalyticsService",
    # Deprecated aliases
    "AppRepository",
    "AppService",
]

