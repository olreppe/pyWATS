"""
pyWATS - Python API for WATS (Web-based Automatic Test System)

A clean, object-oriented Python library for interacting with the WATS server.

Usage:
    from pywats import pyWATS
    
    api = pyWATS(base_url="https://your-wats-server.com", token="your-token")
    
    # Access modules
    products = api.product.get_products()
    product = api.product.get_product("PART-001")
    
    # Use query models
    from pywats.models import WATSFilter
    filter = WATSFilter(part_number="PART-001")
    headers = api.report.query_uut_headers(filter)
    
    # Use report models (WSJF format)
    from pywats.models import UUTReport, UURReport
    report = UUTReport(pn="PART-001", sn="SN-12345", rev="A", ...)
"""

from .pywats import pyWATS
from .exceptions import (
    PyWATSError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ServerError,
    ConnectionError
)

# Import commonly used models for convenience
from .models import (
    # Product models
    Product,
    ProductRevision,
    ProductView,
    ProductState,
    # Asset models (from asset module)
    Asset,
    AssetType,
    AssetLog,
    AssetState,
    # Production models
    Unit,
    UnitChange,
    ProductionBatch,
    SerialNumberType,
    UnitVerification,
    UnitVerificationGrade,
    # RootCause (Ticketing) models
    Ticket,
    TicketStatus,
    TicketPriority,
    TicketView,
    TicketUpdate,
    TicketUpdateType,
    TicketAttachment,
    # Query/filter models
    ReportHeader,
    WATSFilter,
    YieldData,
    ProcessInfo,
    LevelInfo,
    ProductGroup,
    DateGrouping,
    # Common models
    Setting,
)

# UUT/UUR Report models (import separately to avoid name conflicts)
# from pywats.models import UUTReport, UURReport, Step, etc.

__version__ = "2.0.0"
__all__ = [
    # Main class
    "pyWATS",
    # Exceptions
    "PyWATSError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "ServerError",
    "ConnectionError",
    # Product models
    "Product",
    "ProductRevision",
    "ProductView",
    "ProductState",
    # Asset models
    "Asset",
    "AssetType",
    "AssetLog",
    "AssetState",
    # Production models
    "Unit",
    "UnitChange",
    "ProductionBatch",
    "SerialNumberType",
    "UnitVerification",
    "UnitVerificationGrade",
    # RootCause (Ticketing) models
    "Ticket",
    "TicketStatus",
    "TicketPriority",
    "TicketView",
    "TicketUpdate",
    "TicketUpdateType",
    "TicketAttachment",
    # Query/filter models
    "ReportHeader",
    "WATSFilter",
    "YieldData",
    "ProcessInfo",
    "LevelInfo",
    "ProductGroup",
    "DateGrouping",
    # Common models
    "Setting",
]
