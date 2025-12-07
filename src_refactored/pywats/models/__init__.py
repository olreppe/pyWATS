# pyWATS Models
# Models organized by module

from .product import Product, ProductRevision, ProductView, ProductState
from .asset import Asset, AssetType, AssetLog, AssetState, AssetLogType
from .production import (
    Unit, UnitChange, ProductionBatch, SerialNumberType,
    UnitVerification, UnitVerificationGrade, SerialNumberIdentifier
)

# Query/filter models (for REST API queries)
from .report_query import (
    ReportHeader, WATSFilter, Attachment as QueryAttachment, YieldData,
    ProcessInfo, LevelInfo, ProductGroup, DateGrouping
)

# UUT/UUR Report models (WSJF format - full report structure)
from .report import (
    # Base classes
    WATSBase, Report, ReportStatus,
    ReportInfo, MiscInfo, AdditionalData, BinaryData,
    Asset as ReportAsset, AssetStats, Chart, ChartSeries, ChartType,
    SubUnit, Attachment as ReportAttachment, DeserializationContext,
    # UUT Report
    UUTReport, UUTInfo, Step, StepStatus,
    # UUR Report
    UURReport, UURInfo, SubRepair
)

from .common import Setting, ChangeType

__all__ = [
    # Product models
    "Product",
    "ProductRevision",
    "ProductView",
    "ProductState",
    # Asset models (from asset module)
    "Asset",
    "AssetType",
    "AssetLog",
    "AssetState",
    "AssetLogType",
    # Production models
    "Unit",
    "UnitChange",
    "ProductionBatch",
    "SerialNumberType",
    "SerialNumberIdentifier",
    "UnitVerification",
    "UnitVerificationGrade",
    # Query/filter models
    "ReportHeader",
    "WATSFilter",
    "QueryAttachment",
    "YieldData",
    "ProcessInfo",
    "LevelInfo",
    "ProductGroup",
    "DateGrouping",
    # UUT/UUR Report models (WSJF format)
    "WATSBase",
    "Report",
    "ReportStatus",
    "ReportInfo",
    "MiscInfo",
    "AdditionalData",
    "BinaryData",
    "ReportAsset",
    "AssetStats",
    "Chart",
    "ChartSeries",
    "ChartType",
    "SubUnit",
    "ReportAttachment",
    "DeserializationContext",
    "UUTReport",
    "UUTInfo",
    "Step",
    "StepStatus",
    "UURReport",
    "UURInfo",
    "SubRepair",
    # Common models
    "Setting",
    "ChangeType",
]
