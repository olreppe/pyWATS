"""
TYPE SAFETY AUDIT REPORT - pyWATS
==================================
Generated: January 25, 2026
Scope: src/pywats/ and src/pywats_client/ (excluding tests)

This report documents type safety issues found in the codebase:
1. Functions with missing/incomplete return type hints
2. Functions returning raw dict instead of Pydantic models
3. Functions returning Any (overly permissive)
4. Duplicate models and enums that should be shared
5. String constants that should be enums
6. Inconsistent serialization patterns
"""

# =============================================================================
# SECTION 1: MISSING RETURN TYPE HINTS
# =============================================================================

MISSING_RETURN_TYPES = {
    # -------------------------------------------------------------------------
    # pywats/core/ - Core Infrastructure
    # -------------------------------------------------------------------------
    "pywats/core/async_client.py": [
        ("_emit_trace", "~120", "def _emit_trace(self, trace: dict[str, Any])", "-> None"),
        ("_record_trace", "~130", "def _record_trace(self, ...)", "-> None"),
    ],
    
    "pywats/core/client.py": [
        ("__init__", "~70", "def __init__(self, base_url, token, ...)", "-> None"),
        ("_parse_response", "~94", "def _parse_response(self, response)", "-> Any (TypeVar preferred)"),
    ],
    
    "pywats/core/exceptions.py": [
        ("__init__ (PyWATSError)", "~11", "def __init__(self, message, ...)", "-> None"),
        ("__str__", "~16", "def __str__(self)", "-> str"),
        ("__init__ (NotFoundError)", "~30", "def __init__(self, resource_type, ...)", "-> None"),
        ("__init__ (ValidationError)", "~40", "def __init__(self, message, ...)", "-> None"),
        ("__init__ (ServerError)", "~54", "def __init__(self, status_code, ...)", "-> None"),
        ("__init__ (ErrorHandler)", "~260", "def __init__(self, mode)", "-> None"),
    ],
    
    "pywats/core/station.py": [
        ("__init__ (StationRegistry)", "~243", "def __init__(self)", "-> None"),
    ],
    
    "pywats/core/throttle.py": [
        ("throttle", "~137", "@contextmanager", "-> ContextManager[None]"),
    ],
    
    "pywats/core/cache.py": [
        ("cached", "~59", "decorator function", "Use ParamSpec and TypeVar"),
        ("wrapper (inner)", "~75", "def wrapper(*args, **kwargs)", "Use TypeVar R"),
    ],
    
    "pywats/core/batch.py": [
        ("_async_batch_execute", "~403", "async def", "-> List[Result]"),
        ("_sync_batch_execute", "~404", "def", "-> List[Result]"),
    ],
    
    # -------------------------------------------------------------------------
    # pywats/pywats.py - Main API Class
    # -------------------------------------------------------------------------
    "pywats/pywats.py": [
        ("close", "~591", "def close(self)", "-> None"),
        ("version", "~697", "@property", "-> str (returns analytics.get_version())"),
    ],
    
    # -------------------------------------------------------------------------
    # pywats/queue/ - Queue Module
    # -------------------------------------------------------------------------
    "pywats/queue/simple_queue.py": [
        ("start_auto_process", "~314", "def start_auto_process(self, interval_seconds)", "-> None"),
        ("_auto_process_loop (inner)", "~329", "async def", "-> None"),
        ("stop_auto_process", "~342", "def stop_auto_process(self)", "-> None"),
        ("pause_auto_process", "~349", "def pause_auto_process(self)", "-> None"),
        ("resume_auto_process", "~357", "def resume_auto_process(self)", "-> None"),
    ],
    
    "pywats/queue/memory_queue.py": [
        ("set_hooks", "~350", "def set_hooks(self, hooks)", "-> None"),
    ],
    
    # -------------------------------------------------------------------------
    # pywats/domains/ - All Domain __init__ Methods
    # -------------------------------------------------------------------------
    "pywats/domains/__init__.py (pattern)": [
        # All domain service and repository __init__ methods lack -> None
        ("AsyncProductRepository.__init__", "~26", "def __init__(...)", "-> None"),
        ("AsyncProductService.__init__", "~26", "def __init__(...)", "-> None"),
        ("AsyncAssetRepository.__init__", "~27", "def __init__(...)", "-> None"),
        ("AsyncAssetService.__init__", "~24", "def __init__(...)", "-> None"),
        ("AsyncReportRepository.__init__", "~28", "def __init__(...)", "-> None"),
        ("AsyncReportService.__init__", "~44", "def __init__(...)", "-> None"),
        ("ReportService.__init__", "~51", "def __init__(...)", "-> None"),
        ("AsyncProductionRepository.__init__", "~29", "def __init__(...)", "-> None"),
        ("AsyncProductionService.__init__", "~31", "def __init__(...)", "-> None"),
        ("AsyncAnalyticsRepository.__init__", "~28", "def __init__(...)", "-> None"),
        # ... (20+ more __init__ methods across all domains)
    ],
    
    # -------------------------------------------------------------------------
    # pywats_client/gui/ - GUI Pages and Dialogs (HIGH VOLUME)
    # -------------------------------------------------------------------------
    "pywats_client/gui/pages/*.py": [
        # Pattern: Almost ALL GUI methods lack return type hints
        # Examples from asset.py:
        ("_setup_ui", "various", "def _setup_ui(self)", "-> None"),
        ("_connect_signals", "various", "def _connect_signals(self)", "-> None"),
        ("_load_data", "various", "def _load_data(self)", "-> None"),
        ("_on_selection_changed", "various", "def _on_selection_changed(self)", "-> None"),
        ("_format_date", "various", "def _format_date(self, dt)", "-> str"),
        ("_create_toolbar", "various", "def _create_toolbar(self)", "-> QToolBar"),
        ("_create_table", "various", "def _create_table(self)", "-> QTableWidget"),
        # ... (100+ methods across all GUI pages)
    ],
    
    "pywats_client/gui/settings_dialog.py": [
        ("_setup_navigation", "~200", "def _setup_navigation(self)", "-> None"),
        ("_setup_panels", "~250", "def _setup_panels(self)", "-> None"),
        ("_load_all_settings", "~1276", "def _load_all_settings(self)", "-> None"),
        ("_save_settings", "~1320", "def _save_settings(self)", "-> None"),
        # ... (20+ methods)
    ],
    
    "pywats_client/gui/dashboard.py": [
        ("_setup_ui", "~50", "def _setup_ui(self)", "-> None"),
        ("_update_stats", "~150", "def _update_stats(self)", "-> None"),
        ("_refresh_data", "~200", "def _refresh_data(self)", "-> None"),
        # ... (15+ methods)
    ],
    
    # -------------------------------------------------------------------------
    # pywats_client/service/ - Service Module (HIGH VOLUME)
    # -------------------------------------------------------------------------
    "pywats_client/service/converter_pool.py": [
        ("__init__", "~50", "def __init__(self, config)", "-> None"),
        ("start", "~100", "def start(self)", "-> None"),
        ("stop", "~150", "def stop(self)", "-> None"),
        ("_process_file", "~200", "def _process_file(self, path)", "-> ConversionResult"),
        ("_worker_loop", "~250", "def _worker_loop(self)", "-> None"),
        # ... (20+ methods)
    ],
    
    "pywats_client/service/pending_watcher.py": [
        ("__init__", "~30", "def __init__(self)", "-> None"),
        ("start", "~60", "def start(self)", "-> None"),
        ("stop", "~90", "def stop(self)", "-> None"),
        ("_watch_loop", "~120", "def _watch_loop(self)", "-> None"),
        ("_process_pending", "~150", "def _process_pending(self)", "-> None"),
        # ... (15+ methods)
    ],
    
    "pywats_client/service/client_service.py": [
        ("__init__", "~40", "def __init__(self, config)", "-> None"),
        ("start", "~80", "def start(self)", "-> None"),
        ("stop", "~120", "def stop(self)", "-> None"),
        ("_init_components", "~160", "def _init_components(self)", "-> None"),
        # ... (15+ methods)
    ],
    
    # -------------------------------------------------------------------------
    # pywats_client/core/ - Core Client Module
    # -------------------------------------------------------------------------
    "pywats_client/core/event_bus.py": [
        ("subscribe", "~50", "def subscribe(self, event_type, handler)", "-> None"),
        ("publish", "~70", "def publish(self, event)", "-> None"),
        ("unsubscribe", "~90", "def unsubscribe(self, event_type, handler)", "-> None"),
    ],
    
    "pywats_client/core/async_runner.py": [
        ("submit", "~80", "def submit(self, coro)", "-> TaskInfo"),
        ("cancel", "~110", "def cancel(self, task_id)", "-> bool"),
    ],
}

# Total estimated: 200+ missing return type hints


# =============================================================================
# SECTION 2: FUNCTIONS RETURNING RAW DICT (Should be Pydantic Models)
# =============================================================================

DICT_RETURNS_SHOULD_BE_MODELS = {
    # -------------------------------------------------------------------------
    # HIGH PRIORITY - Public API Methods
    # -------------------------------------------------------------------------
    "HIGH_PRIORITY": [
        {
            "file": "pywats/pywats.py",
            "function": "version (property)",
            "line": "~697",
            "current": "-> dict",
            "suggested_model": "VersionInfo(BaseModel)",
            "fields": ["version: str", "build: str", "api_version: str"],
        },
        {
            "file": "pywats/domains/analytics/async_service.py",
            "function": "get_version",
            "line": "~834",
            "current": "-> Dict[str, Any]",
            "suggested_model": "VersionInfo or keep dict (external API response)",
        },
        {
            "file": "pywats/domains/report/async_service.py",
            "function": "process_queue",
            "line": "~699",
            "current": "-> dict",
            "suggested_model": "QueueProcessingResult(BaseModel)",
            "fields": ["success: int", "failed: int", "skipped: int", "errors: List[str]"],
        },
        {
            "file": "pywats/domains/report/service.py",
            "function": "process_queue",
            "line": "~294",
            "current": "-> dict",
            "suggested_model": "QueueProcessingResult (same as above)",
        },
        {
            "file": "pywats/queue/simple_queue.py",
            "function": "process_queue",
            "line": "~215",
            "current": "-> dict",
            "suggested_model": "QueueProcessingResult (same as above)",
        },
    ],
    
    # -------------------------------------------------------------------------
    # MEDIUM PRIORITY - Internal/Stats Methods
    # -------------------------------------------------------------------------
    "MEDIUM_PRIORITY": [
        {
            "file": "pywats/core/batch.py",
            "function": "stats (property on Batcher)",
            "line": "~232",
            "current": "-> dict",
            "suggested_model": "BatcherStats(BaseModel)",
            "fields": ["pending: int", "processing: int", "completed: int", "failed: int"],
        },
        {
            "file": "pywats/queue/simple_queue.py",
            "function": "get_stats",
            "line": "~533",
            "current": "-> dict",
            "suggested_model": "QueueStats(BaseModel)",
            "fields": ["pending: int", "processing: int", "completed: int", "failed: int", "total: int"],
        },
        {
            "file": "pywats/domains/process/async_service.py",
            "function": "cache_stats",
            "line": "~118",
            "current": "-> Dict[str, Any]",
            "suggested_model": "CacheStats(BaseModel)",
            "fields": ["hits: int", "misses: int", "size: int", "hit_rate: float"],
        },
    ],
    
    # -------------------------------------------------------------------------
    # ACCEPTABLE AS DICT - Serialization Methods
    # -------------------------------------------------------------------------
    "ACCEPTABLE_AS_DICT": [
        # These are intentionally dict for JSON serialization
        ("pywats/core/config.py", "to_dict (DomainSettings)", "~51", "Serialization method - OK"),
        ("pywats/core/config.py", "to_dict (APISettings)", "~185", "Serialization method - OK"),
        ("pywats/core/station.py", "to_dict (Station)", "~133", "Serialization method - OK"),
        ("pywats/core/station.py", "to_dict (StationConfig)", "~206", "Serialization method - OK"),
        ("pywats/core/retry.py", "to_dict (RetryConfig)", "~135", "Serialization method - OK"),
        
        # Discovery utilities - metadata dicts are acceptable
        ("pywats/shared/discovery.py", "discover_models", "~29", "Discovery metadata - OK"),
        ("pywats/shared/discovery.py", "get_domain_info", "~142", "Discovery metadata - OK"),
        ("pywats/shared/discovery.py", "get_service_methods", "~180", "Discovery metadata - OK"),
    ],
    
    # -------------------------------------------------------------------------
    # CONVERTERS - Consider Typed Models
    # -------------------------------------------------------------------------
    "CONVERTERS_CONSIDER_MODELS": [
        {
            "file": "pywats/queue/converters.py",
            "function": "convert_from_wsxf",
            "line": "~42",
            "current": "-> dict",
            "note": "Returns parsed report data - consider UUTReportData model",
        },
        {
            "file": "pywats/queue/converters.py",
            "function": "convert_from_wstf",
            "line": "~75",
            "current": "-> dict",
            "note": "Returns parsed report data - consider UUTReportData model",
        },
        {
            "file": "pywats/queue/converters.py",
            "function": "convert_to_wsjf",
            "line": "~105",
            "current": "-> dict",
            "note": "Returns WSJF format - consider WSJFReport model",
        },
    ],
}


# =============================================================================
# SECTION 3: FUNCTIONS RETURNING ANY (Overly Permissive)
# =============================================================================

ANY_RETURNS = {
    # -------------------------------------------------------------------------
    # Repository Internal Methods (Pattern Issue)
    # -------------------------------------------------------------------------
    "REPOSITORY_PATTERN_ISSUE": {
        "description": "All repository classes have internal methods returning Any",
        "affected_files": [
            "pywats/domains/production/async_repository.py",
            "pywats/domains/production/repository_internal.py",
            "pywats/domains/analytics/async_repository.py",
            "pywats/domains/product/async_repository.py",
            "pywats/domains/software/async_repository.py",
            "pywats/domains/asset/async_repository.py",
            "pywats/domains/process/async_repository.py",
            "pywats/domains/process/repository_internal.py",
        ],
        "methods": ["_internal_get", "_internal_post", "_internal_put", "_internal_delete"],
        "suggested_fix": "Use generic TypeVar: async def _internal_get(..., response_type: Type[T]) -> T",
    },
    
    # -------------------------------------------------------------------------
    # Dynamic Wrapper Methods (Acceptable)
    # -------------------------------------------------------------------------
    "DYNAMIC_WRAPPERS_ACCEPTABLE": [
        ("pywats/pywats.py", "SyncServiceWrapper.__getattr__", "~73", "Dynamic method wrapper - OK"),
        ("pywats/pywats.py", "sync_wrapper (inner)", "~79", "Dynamic method wrapper - OK"),
        ("pywats/pywats.py", "SyncProductServiceWrapper.__getattr__", "~103", "Dynamic method wrapper - OK"),
    ],
    
    # -------------------------------------------------------------------------
    # Core Utilities (Acceptable)
    # -------------------------------------------------------------------------
    "CORE_UTILITIES_ACCEPTABLE": [
        ("pywats/core/client.py", "Response.json property", "~126", "Generic JSON - OK"),
        ("pywats/core/async_client.py", "Response.json property", "~224", "Generic JSON - OK"),
        ("pywats/core/async_client.py", "_parse_response", "~269", "Consider TypeVar"),
        ("pywats/shared/result.py", "Success.value", "~96", "Generic success value - OK"),
        ("pywats/shared/result.py", "Failure.error", "~118", "Generic error - OK"),
    ],
    
    # -------------------------------------------------------------------------
    # GUI Pages - High Volume Issue
    # -------------------------------------------------------------------------
    "GUI_PAGES_ANY_RETURNS": [
        {
            "file": "pywats_client/gui/pages/asset.py",
            "methods": ["_get_selected_item", "_get_cell_value"],
            "note": "Should return Optional[Asset] and specific types",
        },
        {
            "file": "pywats_client/gui/pages/product.py",
            "methods": ["_get_selected_item", "_get_cell_value"],
            "note": "Should return Optional[Product] and specific types",
        },
        {
            "file": "pywats_client/gui/pages/rootcause.py",
            "methods": ["_get_selected_item", "_get_cell_value"],
            "note": "Should return Optional[Ticket] and specific types",
        },
        {
            "file": "pywats_client/gui/settings_dialog.py",
            "methods": ["_get_panel_value", "_get_setting"],
            "note": "Should use Union types or TypeVar",
        },
    ],
}


# =============================================================================
# SECTION 4: DUPLICATE MODELS AND ENUMS
# =============================================================================

DUPLICATE_ENUMS = {
    # -------------------------------------------------------------------------
    # HIGH PRIORITY - Should Consolidate
    # -------------------------------------------------------------------------
    "ConversionStatus_DUPLICATE": {
        "severity": "HIGH",
        "locations": [
            "pywats_client/converters/base.py",
            "pywats_client/service/converter_pool.py",
        ],
        "comparison": {
            "converters/base.py": ["SUCCESS", "FAILED", "SUSPENDED", "SKIPPED"],
            "converter_pool.py": ["SUCCESS", "FAILED", "SUSPENDED", "SKIPPED", "REJECTED"],
        },
        "recommendation": "Keep converter_pool.py version (has REJECTED), delete from base.py",
    },
    
    "PostConversionAction_TRIPLICATE": {
        "severity": "HIGH",
        "locations": [
            "pywats_client/core/config.py",
            "pywats_client/converters/base.py",
            "pywats_client/service/converter_pool.py (nested)",
        ],
        "values": ["DELETE", "MOVE", "ZIP", "KEEP", "ERROR (only in converter_pool)"],
        "recommendation": "Create shared enum in pywats_client/core/enums.py",
    },
    
    "ConversionResult_DUPLICATE_CLASS": {
        "severity": "HIGH",
        "locations": [
            "pywats_client/converters/base.py (class)",
            "pywats_client/service/converter_pool.py (dataclass)",
        ],
        "differences": {
            "base.py": "Plain class with status, message, report",
            "converter_pool.py": "Dataclass with status, message, reports (list), validation, timing",
        },
        "recommendation": "Keep converter_pool.py version (more complete), deprecate base.py version",
    },
    
    "ConversionRecord_DUPLICATE_DATACLASS": {
        "severity": "MEDIUM",
        "locations": [
            "pywats_client/converters/base.py",
            "pywats_client/service/converter_pool.py",
        ],
        "differences": {
            "base.py": "Basic fields, single report",
            "converter_pool.py": "Extended fields, multiple reports, validation",
        },
        "recommendation": "Keep converter_pool.py version, deprecate base.py version",
    },
    
    "QueueItemStatus_vs_QueueStatus": {
        "severity": "MEDIUM",
        "locations": [
            "pywats/queue/memory_queue.py (QueueItemStatus)",
            "pywats_client/service/pending_watcher.py (QueueStatus)",
        ],
        "comparison": {
            "QueueItemStatus": ["PENDING", "PROCESSING", "COMPLETED", "FAILED", "SUSPENDED"],
            "QueueStatus": ["PENDING", "SUBMITTING", "COMPLETED", "ERROR"],
        },
        "recommendation": "Consolidate to shared enum with all values",
    },
    
    "CompOperator_vs_CompOp": {
        "severity": "MEDIUM",
        "locations": [
            "pywats/shared/enums.py (CompOperator)",
            "pywats/domains/report/report_models/uut/enums.py (CompOp)",
        ],
        "comparison": {
            "CompOperator": ["EQ", "NE", "LT", "LE", "GT", "GE", "GELE", "GTLT", "GELT", "GTLE", "LOG", "CASESENSITIVE", "CASEINSENSITIVE"],
            "CompOp": ["EQ", "EQT", "NE", "LT", "LE", "GT", "GE", "GELE", "GTLT", "GELT", "GTLE", "CASESENSIT", "IGNORECASE", "LOG"],
        },
        "recommendation": "Merge into single enum in pywats/shared/enums.py with all values",
    },
    
    "BatchConfig_NAME_COLLISION": {
        "severity": "LOW",
        "locations": [
            "pywats/core/batch.py (request batching)",
            "pywats_client/service/converter_pool.py (thread pool)",
        ],
        "fields": {
            "core/batch.py": ["batch_size", "delay_seconds"],
            "converter_pool.py": ["max_workers", "queue_size", "timeout"],
        },
        "recommendation": "Rename to RequestBatchConfig and ThreadPoolConfig",
    },
    
    # -------------------------------------------------------------------------
    # Service/Connection State Enums - Overlapping
    # -------------------------------------------------------------------------
    "ServiceState_OVERLAPPING": {
        "severity": "LOW",
        "locations": [
            "pywats_client/service/client_service.py (ServiceState)",
            "pywats_client/core/connection_config.py (ConnectionState)",
            "pywats_client/service/pending_watcher.py (WatcherState)",
            "pywats_client/service/converter_pool.py (PoolState)",
        ],
        "common_values": ["STOPPED", "STARTING", "RUNNING", "STOPPING", "ERROR"],
        "recommendation": "Create shared BaseState enum in pywats_client/core/states.py",
    },
}


# =============================================================================
# SECTION 5: STRING CONSTANTS THAT SHOULD BE ENUMS
# =============================================================================

STRING_CONSTANTS_SHOULD_BE_ENUMS = {
    # -------------------------------------------------------------------------
    # Converter Type Strings
    # -------------------------------------------------------------------------
    "CONVERTER_TYPES": {
        "current_usage": [
            ('pywats_client/core/config.py', '"file"', 'converter_type field'),
            ('pywats_client/core/config.py', '"scheduled"', 'converter_type field'),
            ('pywats_client/core/config.py', '"api"', 'converter_type field'),
        ],
        "enum_exists": "pywats_client/converters/base.py: ConverterType",
        "recommendation": "Use ConverterType enum in ConverterConfig validation",
    },
    
    # -------------------------------------------------------------------------
    # Report Type Strings
    # -------------------------------------------------------------------------
    "REPORT_TYPES": {
        "current_usage": [
            ('converters/*.py', '"UUT"', 'Report type identifier'),
            ('converters/*.py', '"UUR"', 'Report type identifier'),
            ('pywats/domains/report/', '"uut"', 'lowercase in service'),
            ('pywats/domains/report/', '"U"', 'single letter in API'),
        ],
        "enum_exists": "pywats/shared/enums.py: ReportType (UUT='U', UUR='R')",
        "recommendation": "Use ReportType enum consistently, add string aliases",
    },
    
    # -------------------------------------------------------------------------
    # Folder Names
    # -------------------------------------------------------------------------
    "FOLDER_NAMES": {
        "current_usage": [
            ('pywats_client/service/pending_watcher.py', '"Done"', 'done_folder'),
            ('pywats_client/service/pending_watcher.py', '"Error"', 'error_folder'),
            ('pywats_client/service/pending_watcher.py', '"Pending"', 'pending_folder'),
            ('pywats_client/service/converter_pool.py', '"Done"', 'done_folder'),
            ('pywats_client/service/converter_pool.py', '"Error"', 'error_folder'),
        ],
        "enum_exists": None,
        "recommendation": "Create FolderNames constants class in pywats_client/core/constants.py",
    },
    
    # -------------------------------------------------------------------------
    # Status Strings (Multiple Representations)
    # -------------------------------------------------------------------------
    "TEST_STATUS_STRINGS": {
        "description": "Test/step status has multiple string representations",
        "representations": {
            "full_strings": ["Passed", "Failed", "Error", "Terminated", "Done", "Skipped"],
            "single_letters": ["P", "F", "E", "T", "D", "S"],
            "lowercase": ["passed", "failed", "error", "terminated", "done", "skipped"],
        },
        "enum_exists": [
            "pywats/shared/enums.py: StatusFilter (full strings)",
            "pywats/domains/report/report_models/uut/enums.py: StepStatus (single letters)",
            "pywats/domains/report/models.py: UUTStatus (single letters)",
        ],
        "recommendation": "Create unified TestStatus enum with properties for both formats",
    },
    
    # -------------------------------------------------------------------------
    # Log Level Strings
    # -------------------------------------------------------------------------
    "LOG_LEVELS": {
        "current_usage": [
            ('pywats_client/gui/settings_dialog.py', '["DEBUG", "INFO", "WARNING", "ERROR"]', 'dropdown'),
            ('pywats_client/gui/log_viewer.py', '["DEBUG", "INFO", "WARNING", "ERROR"]', 'filter'),
            ('pywats_client/core/config.py', '"INFO"', 'default log level'),
        ],
        "enum_exists": "Python's logging module has level constants",
        "recommendation": "Use logging.DEBUG, logging.INFO, etc. or create LogLevel enum",
    },
    
    # -------------------------------------------------------------------------
    # Error Mode Strings
    # -------------------------------------------------------------------------
    "ERROR_MODES": {
        "current_usage": [
            ('pywats/core/config.py', '"strict"', 'error_mode field'),
            ('pywats/core/config.py', '"lenient"', 'error_mode field'),
        ],
        "enum_exists": "pywats/core/exceptions.py: ErrorMode",
        "recommendation": "Use ErrorMode enum in APISettings.error_mode field type",
    },
}


# =============================================================================
# SECTION 6: INCONSISTENT SERIALIZATION PATTERNS
# =============================================================================

SERIALIZATION_INCONSISTENCIES = {
    # -------------------------------------------------------------------------
    # to_dict vs model_dump
    # -------------------------------------------------------------------------
    "TO_DICT_VS_MODEL_DUMP": {
        "description": "Mixed usage of custom to_dict() vs Pydantic's model_dump()",
        "custom_to_dict_locations": [
            "pywats/domains/report/report_models/uur/*.py - All UUR models",
            "pywats/core/config.py - APISettings, DomainSettings",
            "pywats/core/station.py - Station, StationConfig",
            "pywats/core/retry.py - RetryConfig",
        ],
        "pydantic_model_dump_locations": [
            "pywats/domains/*/models.py - Most API models",
            "pywats/shared/models.py - PyWATSModel base",
        ],
        "recommendation": "Standardize on Pydantic's model_dump() for all models",
    },
    
    # -------------------------------------------------------------------------
    # Alias Patterns (Mostly Consistent)
    # -------------------------------------------------------------------------
    "ALIAS_PATTERNS": {
        "status": "MOSTLY_CONSISTENT",
        "pattern_used": {
            "validation_alias": "AliasChoices('camelCase', 'snake_case')",
            "serialization_alias": "'camelCase'",
        },
        "exceptions": [
            "Some UUR models use manual camelCase conversion in to_dict()",
        ],
    },
    
    # -------------------------------------------------------------------------
    # from_dict vs model_validate
    # -------------------------------------------------------------------------
    "FROM_DICT_VS_MODEL_VALIDATE": {
        "description": "Mixed usage of custom from_dict() vs Pydantic's model_validate()",
        "custom_from_dict_locations": [
            "pywats/core/config.py - APISettings.from_dict()",
            "pywats/core/station.py - Station.from_dict()",
        ],
        "recommendation": "Use Pydantic's model_validate() with proper aliases",
    },
}


# =============================================================================
# SECTION 7: PROPOSED NEW SHARED MODULES
# =============================================================================

PROPOSED_SHARED_MODULES = {
    "pywats/shared/status.py": {
        "description": "Unified status enums with multiple representation formats",
        "proposed_content": '''
class TestStatus(str, Enum):
    """Unified test/step status with multiple serialization formats."""
    PASSED = "P"
    FAILED = "F"
    ERROR = "E"
    TERMINATED = "T"
    SKIPPED = "S"
    DONE = "D"
    
    @property
    def full_name(self) -> str:
        """Get full string representation (e.g., 'Passed')."""
        return {"P": "Passed", "F": "Failed", "E": "Error", 
                "T": "Terminated", "S": "Skipped", "D": "Done"}[self.value]
    
    @property
    def lowercase(self) -> str:
        """Get lowercase representation (e.g., 'passed')."""
        return self.full_name.lower()
''',
    },
    
    "pywats/shared/stats.py": {
        "description": "Common statistics models",
        "proposed_content": '''
class QueueStats(BaseModel):
    """Statistics for queue operations."""
    pending: int = 0
    processing: int = 0
    completed: int = 0
    failed: int = 0
    total: int = 0

class QueueProcessingResult(BaseModel):
    """Result of queue processing operation."""
    success: int = 0
    failed: int = 0
    skipped: int = 0
    errors: List[str] = Field(default_factory=list)

class CacheStats(BaseModel):
    """Statistics for cache operations."""
    hits: int = 0
    misses: int = 0
    size: int = 0
    hit_rate: float = 0.0
''',
    },
    
    "pywats_client/core/constants.py": {
        "description": "Shared constants for client operations",
        "proposed_content": '''
class FolderNames:
    """Standard folder names for queue/conversion operations."""
    DONE = "Done"
    ERROR = "Error"
    PENDING = "Pending"
    PROCESSING = "Processing"
    ARCHIVE = "Archive"

class FileExtensions:
    """Standard file extensions."""
    WSJF = ".wsjf"
    WSXF = ".wsxf"
    WSTF = ".wstf"
    JSON = ".json"
    XML = ".xml"
''',
    },
    
    "pywats_client/core/enums.py": {
        "description": "Consolidated client enums",
        "proposed_content": '''
class ConversionStatus(str, Enum):
    """Status of a conversion operation."""
    SUCCESS = "success"
    FAILED = "failed"
    SUSPENDED = "suspended"
    SKIPPED = "skipped"
    REJECTED = "rejected"

class PostConversionAction(str, Enum):
    """Action to take after conversion."""
    DELETE = "delete"
    MOVE = "move"
    ZIP = "zip"
    KEEP = "keep"

class ServiceState(str, Enum):
    """State of a service component."""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"
    PAUSED = "paused"
''',
    },
}


# =============================================================================
# SECTION 8: SUMMARY AND PRIORITIES
# =============================================================================

SUMMARY = {
    "total_issues": {
        "missing_return_types": "200+ methods",
        "dict_returns_should_be_models": "~45 instances",
        "any_returns": "~50 instances",
        "duplicate_enums": "8 duplicate/overlapping enums",
        "string_constants_needing_enums": "6 categories",
    },
    
    "priority_actions": {
        "HIGH": [
            "1. Fix pywats.version property return type (-> dict should be -> str)",
            "2. Consolidate ConversionStatus enum (delete from base.py)",
            "3. Consolidate PostConversionAction enum (create shared)",
            "4. Consolidate ConversionResult class (keep converter_pool.py version)",
            "5. Create QueueProcessingResult model (replace dict returns)",
        ],
        "MEDIUM": [
            "6. Add -> None to all __init__ methods (200+ methods)",
            "7. Merge CompOperator and CompOp enums",
            "8. Create shared stats models (QueueStats, CacheStats, BatcherStats)",
            "9. Use ConverterType enum in config validation",
            "10. Create FolderNames constants class",
        ],
        "LOW": [
            "11. Add return types to all GUI methods (~100 methods)",
            "12. Consolidate service state enums",
            "13. Use TypeVar for repository internal methods",
            "14. Standardize on model_dump() vs to_dict()",
            "15. Create unified TestStatus enum with format properties",
        ],
    },
    
    "files_with_most_issues": [
        ("pywats_client/service/converter_pool.py", "25+ issues"),
        ("pywats_client/service/pending_watcher.py", "20+ issues"),
        ("pywats_client/service/client_service.py", "20+ issues"),
        ("pywats_client/gui/settings_dialog.py", "20+ issues"),
        ("pywats_client/gui/pages/*.py", "100+ issues (combined)"),
        ("pywats/pywats.py", "15+ issues"),
        ("pywats/domains/*/async_repository.py", "15+ issues each"),
    ],
    
    "estimated_effort": {
        "high_priority_fixes": "2-4 hours",
        "medium_priority_fixes": "4-8 hours",
        "low_priority_fixes": "8-16 hours",
        "total": "14-28 hours",
    },
}


# =============================================================================
# MAIN - Print Summary
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("TYPE SAFETY AUDIT REPORT - pyWATS")
    print("=" * 80)
    print()
    print("SUMMARY OF ISSUES FOUND:")
    print("-" * 40)
    for category, count in SUMMARY["total_issues"].items():
        print(f"  {category}: {count}")
    print()
    print("HIGH PRIORITY ACTIONS:")
    print("-" * 40)
    for action in SUMMARY["priority_actions"]["HIGH"]:
        print(f"  {action}")
    print()
    print("FILES WITH MOST ISSUES:")
    print("-" * 40)
    for file, issues in SUMMARY["files_with_most_issues"]:
        print(f"  {file}: {issues}")
    print()
    print(f"ESTIMATED TOTAL EFFORT: {SUMMARY['estimated_effort']['total']}")
    print("=" * 80)
