"""
TDM Models Module

Consolidated data models for Test Data Management including:
- WSJF (WATS Standard JSON Format) report models
- Analytics and statistics models  
- TDM-specific data structures

This module unifies the previously distributed model definitions to provide
a single source of truth for TDM-related data models.
"""

# WSJF Report models with complete step hierarchy (formerly from rest_api.models.wsjf_reports)
from .wsjf_reports import (
    # Base WSJF models
    WSJFReport, UUTReport, UURReport, ReportInfo, UUTInfo, UURInfo,
    MiscInfo, SequenceCallInfo, Failure, SubUnit, SubRepair, ReportStatus,
    
    # Complete step hierarchy models
    SequenceCall, Step, NumericLimitStep, PassFailStep, StringValueStep,
    
    # Measurement models
    Measurement, NumericMeasurement, MultiNumericMeasurement, 
    BooleanMeasurement, StringMeasurement,
    
    # Enums
    StepStatusType, CompOperatorType, StepTypeEnum,
    
    # Legacy compatibility
    LegacySequenceCall
)

# Analytics models (original TDM models)
from .analytics import (
    TrendData, MeasurementData, YieldData, StatisticsFilter, AnalyticsResult,
    TopFailedData, YieldTrendData, ProcessCapabilityData, TopFailedStep,
    AggregatedMeasurement, StepStatus, AlertLevels, LastResultData, TrendDataPoint
)

__all__ = [
    # Base WSJF Report Models
    "WSJFReport", "UUTReport", "UURReport", "ReportInfo", "UUTInfo", "UURInfo",
    "MiscInfo", "SequenceCallInfo", "Failure", "SubUnit", "SubRepair", "ReportStatus",
    
    # Complete Step Hierarchy Models
    "SequenceCall", "Step", "NumericLimitStep", "PassFailStep", "StringValueStep",
    
    # Measurement Models
    "Measurement", "NumericMeasurement", "MultiNumericMeasurement", 
    "BooleanMeasurement", "StringMeasurement",
    
    # Enums
    "StepStatusType", "CompOperatorType", "StepTypeEnum",
    
    # Legacy Compatibility
    "LegacySequenceCall",
    
    # Analytics Models  
    "TrendData", "MeasurementData", "YieldData", "StatisticsFilter", "AnalyticsResult",
    "TopFailedData", "YieldTrendData", "ProcessCapabilityData", "TopFailedStep",
    "AggregatedMeasurement", "StepStatus", "AlertLevels", "LastResultData", "TrendDataPoint"
]