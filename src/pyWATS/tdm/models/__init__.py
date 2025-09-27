"""
TDM Models Module

Consolidated data models for Test Data Management including:
- WSJF (WATS Standard JSON Format) report models
- Analytics and statistics models  
- TDM-specific data structures

This module unifies the previously distributed model definitions to provide
a single source of truth for TDM-related data models.
"""

# WSJF Report models (formerly from rest_api.models.wsjf_reports)
from .wsjf_reports import (
    WSJFReport, UUTReport, UURReport, ReportInfo, UUTInfo, UURInfo,
    MiscInfo, SequenceCall, SequenceCallInfo, Failure, SubUnit, SubRepair,
    ReportStatus
)

# Analytics models (original TDM models)
from .analytics import (
    TrendData, MeasurementData, YieldData, StatisticsFilter, AnalyticsResult,
    TopFailedData, YieldTrendData, ProcessCapabilityData, TopFailedStep,
    AggregatedMeasurement, StepStatus, AlertLevels, LastResultData, TrendDataPoint
)

__all__ = [
    # WSJF Report Models
    "WSJFReport", "UUTReport", "UURReport", "ReportInfo", "UUTInfo", "UURInfo",
    "MiscInfo", "SequenceCall", "SequenceCallInfo", "Failure", "SubUnit", "SubRepair",
    "ReportStatus",
    
    # Analytics Models  
    "TrendData", "MeasurementData", "YieldData", "StatisticsFilter", "AnalyticsResult",
    "TopFailedData", "YieldTrendData", "ProcessCapabilityData", "TopFailedStep",
    "AggregatedMeasurement", "StepStatus", "AlertLevels", "LastResultData", "TrendDataPoint"
]