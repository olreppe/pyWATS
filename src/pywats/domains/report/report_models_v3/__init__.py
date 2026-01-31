"""
Report Models v3 - Type-Safe Implementation

This package provides a type-safe implementation of WATS report models
that maintains the elegant architecture of v1 while fixing all mypy errors.

Key Features:
- Full Pydantic v2 support with proper ConfigDict
- Generic types for SubUnit specialization
- Proper Optional annotations
- SingleMeasurementMixin to eliminate code duplication
- StepList with proper parent injection
- C# naming aliases for API compatibility
- Zero mypy errors in standard mode

Usage:
    from pywats.domains.report.report_models_v3 import (
        UUTReport,
        SequenceCall,
        NumericStep,
        PassFailStep,
        CompOp,
        StepStatus,
    )
    
    # Create report
    report = UUTReport(pn="WIDGET-001", sn="SN123456", operation="Test")
    
    # Add test steps
    root = report.create_root("MainSequence")
    root.add_numeric_step("Voltage", value=5.0, comp=CompOp.GELE, limit_l=4.5, limit_h=5.5)
    root.add_pass_fail_step("LED Check", value=True)
"""
from __future__ import annotations

# Common types and enums
from .common_types import (
    WATSBase,
    Field,
    StepStatus,
    ReportStatus,
    ReportResult,  # Alias for backwards compatibility
    StepGroup,
    ReportType,
    ChartType,
    CompOp,
    FlowType,
)

# Base classes
from .wats_base import WATSBase
from .report_info import ReportInfo
from .sub_unit import SubUnit
from .report import Report
from .asset import Asset, AssetStats
from .chart import Chart, ChartSeries
from .binary_data import (
    BinaryData,
    Attachment,
    AdditionalData,
    AdditionalDataProperty,
    AdditionalDataArray,
    AdditionalDataArrayIndex,
    LoopInfo,
)
from .misc_info import MiscInfo, UURMiscInfo

# UUT classes
from .uut import (
    Step,
    UUTInfo,
    UUTReport,
    UUTSubUnit,
    StepList,
    StepType,
    SequenceCall,
    NumericStep,
    MultiNumericStep,
    PassFailStep,
    BooleanStep,
    StringValueStep,
    StringStep,
    GenericStep,
    ActionStep,
    ChartStep,
    NumericMeasurement,
    BooleanMeasurement,
    StringMeasurement,
)

# UUT step types
from .uut.steps.callexe_step import CallExeStep, CallExeStepInfo
from .uut.steps.message_popup_step import MessagePopUpStep, MessagePopupInfo
from .uut.steps.unknown_step import UnknownStep

# UUR classes
from .uur import (
    UURFailure,
    UURSubUnit,
    UURInfo,
    UURReport,
)

__all__ = [
    # Common Types
    "WATSBase",
    "Field",
    "StepStatus",
    "ReportStatus",
    "ReportResult",  # Alias for backwards compatibility
    "StepGroup",
    "ReportType",
    "ChartType",
    "CompOp",
    "FlowType",
    
    # Base Classes
    "ReportInfo",
    "SubUnit",
    "Report",
    "Asset",
    "AssetStats",
    "Chart",
    "ChartSeries",
    "BinaryData",
    "Attachment",
    "AdditionalData",
    "AdditionalDataProperty",
    "AdditionalDataArray",
    "AdditionalDataArrayIndex",
    "LoopInfo",
    "MiscInfo",
    "UURMiscInfo",
    
    # UUT Classes
    "Step",
    "UUTInfo",
    "UUTReport",
    "UUTSubUnit",
    "StepList",
    "StepType",
    "SequenceCall",
    "NumericStep",
    "MultiNumericStep",
    "PassFailStep",
    "BooleanStep",
    "StringValueStep",
    "StringStep",
    "GenericStep",
    "ActionStep",
    "ChartStep",
    "CallExeStep",
    "CallExeStepInfo",
    "MessagePopUpStep",
    "MessagePopupInfo",
    "UnknownStep",
    "NumericMeasurement",
    "BooleanMeasurement",
    "StringMeasurement",
    
    # UUR Classes
    "UURFailure",
    "UURSubUnit",
    "UURInfo",
    "UURReport",
]
