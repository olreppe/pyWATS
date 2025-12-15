# Converter Architecture Redesign

> **Implementation Status: Phase 1 Complete ✓**
> 
> The core converter architecture has been implemented:
> - [x] `models.py` - Core data models (ConverterSource, ValidationResult, ConverterResult, etc.)
> - [x] `file_converter.py` - FileConverter base class
> - [x] `folder_converter.py` - FolderConverter base class  
> - [x] `scheduled_converter.py` - ScheduledConverter base class
> - [x] `context.py` - ConverterContext class
> - [x] `core/config.py` - Updated ConverterConfig with new fields
> - [x] `example_csv_v2.py` - Example implementation using new architecture
> - [ ] ConverterProcessor - Integration with new classes (Phase 2)
> - [ ] ConverterManager - Integration with new classes (Phase 2)
> - [ ] GUI updates for new converter configuration (Phase 3)

## Executive Summary

This document proposes a comprehensive redesign of the pyWATS converter architecture to address limitations of the Windows/.NET WATS Client API while maintaining backward compatibility with file-based converters.

### Key Improvements

1. **Multiple Converter Types**: File, Folder, Scheduled (database/API polling)
2. **Validation & Confidence Scoring**: Converters rate their fit (0.0-1.0) and can preview detected fields
3. **Suspend/Resume with Backoff**: Files can be suspended and retried with configurable delays
4. **Folder-Based Conversions**: Support multi-file scenarios (log + config, session folders)
5. **AI-Ready Architecture**: Prepare for server-side AI-assisted conversion
6. **Improved Error Handling**: Retry logic, failure logging, max retry limits

---

## Current Architecture Analysis

### Windows/.NET WATS Client (Reference)

```
IReportConverter_v2 Interface:
├── Constructor(ConverterArguments dict)
├── ImportReport(apiref, filestream) → UUT/UUR Report
└── Arguments property (user-defined key-value pairs)

Client-Side Settings:
├── Assembly/Class path
├── Watch folder
├── Filter (regex, e.g., "*.txt")
└── PPA (Post-Process Action: Move, Zip, Delete)
```

### Current pyWATS Implementation

```
ConverterBase (abstract):
├── name, version, description (properties)
├── supported_extensions, supported_mime_types
├── validate_file(FileInfo) → (bool, reason)
├── convert_file(Path, ConverterArguments) → ConverterResult
└── on_success(), on_failure() (callbacks)

ConverterProcessor:
├── Process single files
├── Post-process actions
├── Retry logic for suspended conversions
└── Error folder management
```

### Identified Weaknesses

| Issue | Description | Impact |
|-------|-------------|--------|
| Single-file only | No support for folder-based conversions | Can't handle multi-file reports |
| No confidence scoring | Can't auto-select best converter | Manual converter assignment required |
| Limited retry | Suspend blocks processing | Other files wait unnecessarily |
| No scheduled converters | Can't poll databases/APIs | Missing use case |
| No preview/validation | Can't preview what will be converted | User confusion on matching |

---

## Proposed Architecture

### 1. Converter Type Hierarchy

```
                    ┌─────────────────────┐
                    │  ConverterProtocol  │  (Abstract interface)
                    │                     │
                    │  + name             │
                    │  + version          │
                    │  + description      │
                    │  + arguments_schema │
                    │  + validate()       │
                    │  + convert()        │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│  FileConverter   │ │ FolderConverter  │ │ScheduledConverter│
│                  │ │                  │ │                  │
│ Triggered by     │ │ Triggered by     │ │ Triggered by     │
│ file creation/   │ │ folder creation  │ │ timer/schedule   │
│ modification     │ │ or folder "ready"│ │                  │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

### 2. Core Models

#### ConverterSource (Input Abstraction)

```python
@dataclass
class ConverterSource:
    """
    Abstraction over what's being converted.
    Works for files, folders, and virtual sources (database records).
    """
    source_type: SourceType  # FILE, FOLDER, DATABASE, API
    path: Optional[Path] = None  # Primary file or folder
    files: List[Path] = field(default_factory=list)  # All related files
    metadata: Dict[str, Any] = field(default_factory=dict)  # Source-specific metadata
    
    # For database/API sources
    record_id: Optional[str] = None
    connection_string: Optional[str] = None
    
    @property
    def primary_name(self) -> str:
        """Name of the primary file/folder/record"""
        if self.path:
            return self.path.name
        return self.record_id or "unknown"
    
    @property
    def is_folder(self) -> bool:
        return self.source_type == SourceType.FOLDER
    
    @classmethod
    def from_file(cls, file_path: Path) -> "ConverterSource":
        """Create source from a single file"""
        return cls(
            source_type=SourceType.FILE,
            path=file_path,
            files=[file_path]
        )
    
    @classmethod
    def from_folder(cls, folder_path: Path, include_pattern: str = "*") -> "ConverterSource":
        """Create source from a folder with all matching files"""
        import fnmatch
        files = [f for f in folder_path.rglob("*") if f.is_file() and fnmatch.fnmatch(f.name, include_pattern)]
        return cls(
            source_type=SourceType.FOLDER,
            path=folder_path,
            files=files
        )
```

#### ValidationResult (Confidence Scoring)

```python
@dataclass
class ValidationResult:
    """
    Result of converter validation/preview.
    
    Converters rate how well they match the input and can
    preview what they detected (serial number, part number, etc.)
    """
    can_convert: bool  # Whether conversion is possible
    confidence: float  # 0.0 to 1.0 - how well this converter fits
    
    # Detected/preview information
    detected_part_number: Optional[str] = None
    detected_serial_number: Optional[str] = None
    detected_process: Optional[str] = None
    detected_start_time: Optional[datetime] = None
    detected_result: Optional[str] = None  # Passed/Failed
    
    # Validation details
    message: str = ""  # Human-readable explanation
    warnings: List[str] = field(default_factory=list)
    
    # For suspend/retry scenarios
    ready: bool = True  # False if dependencies are missing
    missing_dependencies: List[str] = field(default_factory=list)
    retry_after: Optional[timedelta] = None  # Suggested wait time
    
    @classmethod
    def perfect_match(cls, **detected) -> "ValidationResult":
        """Perfect confidence match"""
        return cls(can_convert=True, confidence=1.0, **detected)
    
    @classmethod
    def good_match(cls, confidence: float = 0.8, **detected) -> "ValidationResult":
        """Good confidence match"""
        return cls(can_convert=True, confidence=confidence, **detected)
    
    @classmethod
    def extension_match(cls, **detected) -> "ValidationResult":
        """Low confidence - only extension matched"""
        return cls(can_convert=True, confidence=0.3, 
                   message="Matched by extension only", **detected)
    
    @classmethod
    def no_match(cls, reason: str) -> "ValidationResult":
        """Cannot convert this source"""
        return cls(can_convert=False, confidence=0.0, message=reason)
    
    @classmethod
    def not_ready(cls, missing: List[str], retry_after: timedelta = None) -> "ValidationResult":
        """Can convert but dependencies missing"""
        return cls(
            can_convert=True,
            confidence=0.7,
            ready=False,
            missing_dependencies=missing,
            retry_after=retry_after,
            message=f"Waiting for: {', '.join(missing)}"
        )
```

#### ConverterResult (Enhanced)

```python
@dataclass
class ConverterResult:
    """
    Enhanced result of a conversion operation.
    """
    status: ConversionStatus
    report: Optional[Dict[str, Any]] = None
    reports: List[Dict[str, Any]] = field(default_factory=list)  # For multi-report conversions
    
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Suspend/retry information
    suspend_reason: Optional[str] = None
    retry_after: Optional[timedelta] = None  # How long to wait before retry
    retry_count: int = 0  # Current retry attempt
    
    # Post-processing
    post_action: PostProcessAction = PostProcessAction.MOVE
    
    # Statistics
    processing_time_ms: Optional[int] = None
    records_processed: int = 0
    
    @property
    def has_multiple_reports(self) -> bool:
        return len(self.reports) > 1 or (self.report and self.reports)
    
    def get_all_reports(self) -> List[Dict[str, Any]]:
        """Get all reports (single or multiple)"""
        if self.reports:
            return self.reports
        elif self.report:
            return [self.report]
        return []
```

### 3. Converter Base Classes

#### Abstract Protocol

```python
from abc import ABC, abstractmethod
from typing import Protocol

class ConverterProtocol(Protocol):
    """
    Protocol defining what all converters must implement.
    """
    
    @property
    def name(self) -> str: ...
    
    @property
    def version(self) -> str: ...
    
    @property  
    def converter_type(self) -> ConverterType: ...
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult: ...
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult: ...
```

#### FileConverter

```python
class FileConverter(ABC):
    """
    Base class for file-based converters.
    
    Triggered when a file is created or modified in the watch folder.
    This is the most common converter type.
    
    Example:
        class CSVConverter(FileConverter):
            @property
            def name(self) -> str:
                return "CSV Converter"
            
            @property
            def file_patterns(self) -> List[str]:
                return ["*.csv", "*.txt"]
            
            def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
                # Check if this is a valid CSV
                try:
                    with open(source.path) as f:
                        header = f.readline()
                    if "PartNumber" in header and "SerialNumber" in header:
                        return ValidationResult.perfect_match()
                    return ValidationResult.extension_match()
                except:
                    return ValidationResult.no_match("Cannot read file")
            
            def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
                # Actual conversion
                ...
    """
    
    def __init__(self) -> None:
        self.arguments: Dict[str, Any] = {}
        self._context: Optional[ConverterContext] = None
    
    @property
    def converter_type(self) -> ConverterType:
        return ConverterType.FILE
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name"""
        pass
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return ""
    
    @property
    def file_patterns(self) -> List[str]:
        """
        File patterns this converter handles.
        
        Uses glob patterns: "*.csv", "test_*.log", "report.xml"
        Return ["*"] to accept all files.
        """
        return ["*"]
    
    @property
    def arguments_schema(self) -> Dict[str, ArgumentDefinition]:
        """
        Define configurable arguments for this converter.
        
        Returns dictionary of argument_name -> ArgumentDefinition.
        These are exposed in the GUI for user configuration.
        
        Example:
            return {
                "delimiter": ArgumentDefinition(
                    type=str,
                    default=",",
                    description="CSV field delimiter"
                ),
                "skip_header": ArgumentDefinition(
                    type=bool,
                    default=True,
                    description="Skip first row as header"
                )
            }
        """
        return {}
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """
        Validate source and rate how well this converter fits.
        
        This is called BEFORE convert() to:
        1. Quickly filter files that don't qualify
        2. Rate how well this converter matches (for auto-selection)
        3. Preview detected fields (part number, serial, etc.)
        4. Check if dependencies are ready
        
        Default implementation checks file patterns only (low confidence).
        Override for content-based validation (high confidence).
        
        Args:
            source: The file/folder to potentially convert
            context: Converter context with API client, settings, etc.
        
        Returns:
            ValidationResult with confidence score and detected fields
        """
        import fnmatch
        
        # Check file pattern
        matches_pattern = False
        for pattern in self.file_patterns:
            if pattern == "*" or fnmatch.fnmatch(source.primary_name, pattern):
                matches_pattern = True
                break
        
        if not matches_pattern:
            return ValidationResult.no_match(
                f"File {source.primary_name} doesn't match patterns: {self.file_patterns}"
            )
        
        # Default: extension-only match (low confidence)
        return ValidationResult.extension_match()
    
    @abstractmethod
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """
        Convert the source file to a WATS report.
        
        Args:
            source: File to convert
            context: Converter context with API, settings, folders
        
        Returns:
            ConverterResult with status and report(s)
        """
        pass
```

#### FolderConverter

```python
class FolderConverter(ABC):
    """
    Base class for folder-based converters.
    
    Triggered when a folder is detected as "ready" for processing.
    Useful for multi-file scenarios:
    - Log file + configuration file
    - Test session folder with multiple data files
    - Batch of related reports
    
    Readiness can be determined by:
    - Presence of a marker file (e.g., "READY", ".complete")
    - Time-based (no new files for X seconds)
    - All expected files present
    - Custom logic in is_folder_ready()
    
    Example:
        class SessionFolderConverter(FolderConverter):
            @property
            def name(self) -> str:
                return "Test Session Converter"
            
            @property
            def folder_pattern(self) -> str:
                return "session_*"  # Only process folders matching this
            
            @property
            def readiness_marker(self) -> str:
                return ".complete"  # Look for this file
            
            def is_folder_ready(self, source: ConverterSource, context: ConverterContext) -> bool:
                # Custom readiness check
                required_files = ["data.json", "config.xml"]
                return all(
                    (source.path / f).exists() for f in required_files
                )
            
            def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
                data_file = source.path / "data.json"
                config_file = source.path / "config.xml"
                # Process both files...
    """
    
    @property
    def converter_type(self) -> ConverterType:
        return ConverterType.FOLDER
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def folder_pattern(self) -> str:
        """Glob pattern for folder names to process. Default: all folders."""
        return "*"
    
    @property
    def readiness_marker(self) -> Optional[str]:
        """
        Filename that indicates folder is ready.
        
        If set, folder is only processed when this file exists.
        E.g., ".complete", "READY.txt", "__done__"
        """
        return None
    
    @property
    def readiness_timeout_seconds(self) -> int:
        """
        Seconds of no file changes before folder is considered ready.
        
        Only used if readiness_marker is None.
        Set to 0 to disable timeout-based readiness.
        """
        return 30
    
    def is_folder_ready(self, source: ConverterSource, context: ConverterContext) -> bool:
        """
        Check if folder is ready for processing.
        
        Override for custom readiness logic.
        Default checks for readiness_marker file.
        """
        if self.readiness_marker:
            marker_path = source.path / self.readiness_marker
            return marker_path.exists()
        return True  # Assume ready if no marker defined
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """Validate the folder source"""
        import fnmatch
        
        if not source.is_folder:
            return ValidationResult.no_match("Not a folder")
        
        if not fnmatch.fnmatch(source.primary_name, self.folder_pattern):
            return ValidationResult.no_match(
                f"Folder {source.primary_name} doesn't match pattern: {self.folder_pattern}"
            )
        
        if not self.is_folder_ready(source, context):
            return ValidationResult.not_ready(
                missing=["Folder not ready"],
                retry_after=timedelta(seconds=self.readiness_timeout_seconds)
            )
        
        return ValidationResult.good_match(confidence=0.7)
    
    @abstractmethod
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        pass
```

#### ScheduledConverter

```python
class ScheduledConverter(ABC):
    """
    Base class for scheduled/polling converters.
    
    Runs at configurable intervals to check for and process records.
    Useful for:
    - Database polling (convert queued records)
    - API polling (fetch and convert from external systems)
    - Batch processing at scheduled times
    
    Unlike file/folder converters, scheduled converters:
    - Are not triggered by filesystem events
    - Run on a timer/schedule
    - May produce multiple reports per run
    - Should be idempotent (can run multiple times safely)
    
    Example:
        class DatabaseConverter(ScheduledConverter):
            @property
            def name(self) -> str:
                return "Database Queue Converter"
            
            @property
            def schedule_interval_seconds(self) -> int:
                return 300  # Run every 5 minutes
            
            async def run(self, context: ConverterContext) -> List[ConverterResult]:
                # Fetch pending records from database
                async with context.get_db_connection() as conn:
                    records = await conn.fetch("SELECT * FROM pending_reports WHERE processed = FALSE")
                
                results = []
                for record in records:
                    try:
                        report = self._convert_record(record)
                        results.append(ConverterResult.success_result(report=report))
                        await conn.execute("UPDATE pending_reports SET processed = TRUE WHERE id = $1", record['id'])
                    except Exception as e:
                        results.append(ConverterResult.failed_result(str(e)))
                
                return results
    """
    
    @property
    def converter_type(self) -> ConverterType:
        return ConverterType.SCHEDULED
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    def schedule_interval_seconds(self) -> int:
        """How often to run (in seconds). Default: 5 minutes."""
        return 300
    
    @property
    def schedule_cron(self) -> Optional[str]:
        """
        Cron expression for scheduling (alternative to interval).
        
        If set, takes precedence over schedule_interval_seconds.
        Format: "minute hour day month weekday"
        
        Examples:
            "0 * * * *"     - Every hour
            "*/15 * * * *"  - Every 15 minutes
            "0 0 * * *"     - Every midnight
            "0 6 * * 1"     - Every Monday at 6 AM
        """
        return None
    
    @property
    def run_on_startup(self) -> bool:
        """Whether to run immediately on startup."""
        return True
    
    @property
    def stop_when_empty(self) -> bool:
        """
        Whether to stop after processing all available records.
        
        If True, exits run() early when no more records exist.
        If False, always waits for full interval before next run.
        """
        return True
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        """Not used for scheduled converters"""
        return ValidationResult.perfect_match()
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        """Not used directly - use run() instead"""
        raise NotImplementedError("Scheduled converters use run() instead of convert()")
    
    @abstractmethod
    async def run(self, context: ConverterContext) -> List[ConverterResult]:
        """
        Execute the scheduled conversion.
        
        Called on schedule. Should:
        1. Check for pending records/sources
        2. Convert each one
        3. Return list of results
        
        Returns:
            List of ConverterResult objects (one per converted record)
        """
        pass
    
    async def should_run(self, context: ConverterContext) -> bool:
        """
        Check if the converter should run now.
        
        Override for custom conditions (e.g., check if database is available).
        Default: always returns True.
        """
        return True
```

### 4. Converter Context

```python
@dataclass
class ConverterContext:
    """
    Context passed to converters with all necessary references.
    
    Provides access to:
    - API client for server operations
    - Configuration and user settings
    - Folder paths
    - Logging
    - Optional database/external connections
    """
    api_client: Any  # WATSClient instance
    user_arguments: Dict[str, Any]  # User-configured arguments
    
    # Folder paths
    drop_folder: Path
    done_folder: Path
    error_folder: Path
    suspended_folder: Path
    
    # Metadata
    station_name: str = ""
    process: Optional[str] = None
    
    # Runtime info
    converter_name: str = ""
    conversion_id: str = ""  # Unique ID for this conversion
    
    # Optional connections (for scheduled converters)
    _connections: Dict[str, Any] = field(default_factory=dict)
    
    def get_argument(self, name: str, default: Any = None) -> Any:
        """Get a user-configured argument"""
        return self.user_arguments.get(name, default)
    
    def set_connection(self, name: str, connection: Any) -> None:
        """Store a database/API connection"""
        self._connections[name] = connection
    
    def get_connection(self, name: str) -> Optional[Any]:
        """Retrieve a stored connection"""
        return self._connections.get(name)
```

### 5. Converter Configuration

```python
class ConverterType(Enum):
    FILE = "file"
    FOLDER = "folder"
    SCHEDULED = "scheduled"


@dataclass
class ConverterConfig:
    """
    Configuration for a registered converter.
    """
    # Identity
    name: str  # Unique name for this configuration
    converter_type: ConverterType
    enabled: bool = True
    
    # Module/Class location
    module_path: str  # Python module path or file path
    class_name: str   # Converter class name
    
    # Watch settings (for FILE and FOLDER types)
    watch_folder: Optional[Path] = None
    file_patterns: List[str] = field(default_factory=lambda: ["*"])
    
    # Post-processing
    post_process_action: PostProcessAction = PostProcessAction.MOVE
    post_process_folder: Optional[Path] = None  # For MOVE action
    
    # User arguments (passed to converter)
    arguments: Dict[str, Any] = field(default_factory=dict)
    
    # Retry settings
    max_retries: int = 3
    retry_delay_seconds: int = 60
    retry_backoff_multiplier: float = 2.0  # Exponential backoff
    
    # Timeout
    conversion_timeout_seconds: int = 300  # 5 minutes default
    
    # Schedule settings (for SCHEDULED type only)
    schedule_interval_seconds: Optional[int] = None
    schedule_cron: Optional[str] = None
    
    # Priority (for auto-selection when multiple converters match)
    priority: int = 100  # Lower = higher priority
```

### 6. Converter Manager (Orchestration)

```python
class ConverterManager:
    """
    Manages converter lifecycle and orchestrates conversions.
    
    Responsibilities:
    - Load and register converters
    - Start/stop file system watchers
    - Route files to appropriate converters
    - Handle suspend/retry logic
    - Maintain conversion statistics
    - Integrate with scheduled converters
    """
    
    def __init__(
        self,
        api_client: Any,
        config: ClientConfig,
        auto_select: bool = True
    ):
        self.api_client = api_client
        self.config = config
        self.auto_select = auto_select
        
        # Registered converters
        self._file_converters: Dict[str, FileConverter] = {}
        self._folder_converters: Dict[str, FolderConverter] = {}
        self._scheduled_converters: Dict[str, ScheduledConverter] = {}
        
        # Configuration
        self._converter_configs: Dict[str, ConverterConfig] = {}
        
        # File system watchers
        self._watchers: Dict[str, Observer] = {}
        
        # Pending/suspended queue
        self._pending_queue: asyncio.Queue[PendingConversion] = asyncio.Queue()
        self._suspended: Dict[str, SuspendedConversion] = {}
        
        # Statistics
        self._stats = ConverterStats()
        
        # Scheduler for scheduled converters
        self._scheduler: Optional[asyncio.Task] = None
        
        # Failure log
        self._failure_log: List[FailureRecord] = []
    
    async def start(self) -> None:
        """Start all watchers and schedulers"""
        await self._start_file_watchers()
        await self._start_scheduler()
        await self._start_pending_processor()
    
    async def stop(self) -> None:
        """Stop all watchers and schedulers"""
        await self._stop_file_watchers()
        await self._stop_scheduler()
    
    def register_converter(
        self,
        converter: Union[FileConverter, FolderConverter, ScheduledConverter],
        config: ConverterConfig
    ) -> None:
        """Register a converter with its configuration"""
        if isinstance(converter, FileConverter):
            self._file_converters[config.name] = converter
        elif isinstance(converter, FolderConverter):
            self._folder_converters[config.name] = converter
        elif isinstance(converter, ScheduledConverter):
            self._scheduled_converters[config.name] = converter
        
        self._converter_configs[config.name] = config
    
    async def process_source(
        self,
        source: ConverterSource,
        converter_name: Optional[str] = None
    ) -> ConverterResult:
        """
        Process a source through the conversion pipeline.
        
        If converter_name is None and auto_select is True,
        selects the best matching converter based on validation scores.
        """
        # Find appropriate converter
        if converter_name:
            converter, config = self._get_converter(converter_name)
        else:
            converter, config = await self._auto_select_converter(source)
        
        if not converter:
            return ConverterResult.skipped_result("No matching converter found")
        
        # Create context
        context = self._create_context(config)
        
        # Validate
        validation = converter.validate(source, context)
        
        if not validation.can_convert:
            return ConverterResult.skipped_result(validation.message)
        
        if not validation.ready:
            return await self._handle_not_ready(source, converter, config, validation)
        
        # Convert
        try:
            result = await self._run_conversion(converter, source, context, config)
            
            if result.status == ConversionStatus.SUCCESS:
                await self._handle_success(source, result, config)
            elif result.status == ConversionStatus.SUSPENDED:
                await self._handle_suspended(source, result, config)
            elif result.status == ConversionStatus.FAILED:
                await self._handle_failure(source, result, config)
            
            return result
            
        except Exception as e:
            return await self._handle_exception(source, e, config)
    
    async def _auto_select_converter(
        self,
        source: ConverterSource
    ) -> Tuple[Optional[Union[FileConverter, FolderConverter]], Optional[ConverterConfig]]:
        """
        Auto-select the best converter for a source.
        
        Runs validation on all enabled converters and selects
        the one with highest confidence score.
        """
        best_converter = None
        best_config = None
        best_score = 0.0
        
        converters = (
            self._file_converters if not source.is_folder 
            else self._folder_converters
        )
        
        for name, converter in converters.items():
            config = self._converter_configs.get(name)
            if not config or not config.enabled:
                continue
            
            context = self._create_context(config)
            validation = converter.validate(source, context)
            
            if validation.can_convert and validation.confidence > best_score:
                best_score = validation.confidence
                best_converter = converter
                best_config = config
        
        return best_converter, best_config
```

### 7. Suspend/Retry Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     SUSPEND/RETRY WORKFLOW                       │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────────┐
    │ New File     │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Validate     │
    └──────┬───────┘
           │
           ├─── not ready ────────────────────┐
           │                                   │
           ▼                                   ▼
    ┌──────────────┐                  ┌────────────────────┐
    │ Convert      │                  │ Add to Pending     │
    └──────┬───────┘                  │ Queue              │
           │                          └─────────┬──────────┘
           │                                    │
    ┌──────┴──────────────────┐                │
    │                         │                │
    ▼                         ▼                │
┌────────┐             ┌───────────┐           │
│SUCCESS │             │ SUSPENDED │           │
└────┬───┘             └─────┬─────┘           │
     │                       │                 │
     ▼                       ▼                 │
┌─────────────┐       ┌─────────────────┐      │
│ Post-Process│       │ Move to         │      │
│ (Move/Zip)  │       │ Suspended Folder│      │
└─────────────┘       └────────┬────────┘      │
                               │               │
                               ▼               │
                      ┌─────────────────┐      │
                      │ Create Retry    │      │
                      │ Timer           │◄─────┘
                      └────────┬────────┘
                               │
                               │  After retry_delay
                               ▼
                      ┌─────────────────┐
                      │ Move back to    │
                      │ Drop Folder     │
                      └────────┬────────┘
                               │
                               │  (Triggers new conversion attempt)
                               ▼
                      ┌─────────────────┐
                      │ Increment       │
                      │ retry_count     │
                      └────────┬────────┘
                               │
                               ├─── retry_count < max_retries
                               │          │
                               │          └───► (Re-process)
                               │
                               └─── retry_count >= max_retries
                                          │
                                          ▼
                               ┌─────────────────┐
                               │ Move to Error   │
                               │ Folder          │
                               └─────────────────┘
```

### 8. GUI Integration

The ConvertersPage should be enhanced to show:

```
┌─────────────────────────────────────────────────────────────────┐
│ Converters                                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Registered Converters                                     │  │
│  ├──────────┬────────┬─────────┬────────────┬──────────────┤  │
│  │ Name     │ Type   │ Status  │ Watch Path │ Pattern      │  │
│  ├──────────┼────────┼─────────┼────────────┼──────────────┤  │
│  │ CSV      │ File   │ ✓ Active│ C:\Drop    │ *.csv        │  │
│  │ Session  │ Folder │ ✓ Active│ C:\Drop    │ session_*    │  │
│  │ DBQueue  │ Sched. │ ✓ Active│ -          │ @5min        │  │
│  └──────────┴────────┴─────────┴────────────┴──────────────┘  │
│                                                                 │
│  [+ Add Converter]  [Edit]  [Remove]  [Test]                   │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Converter Arguments                                       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ delimiter:     [ , ]                                      │  │
│  │ skip_header:   [✓]                                        │  │
│  │ encoding:      [ UTF-8      ▼ ]                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Activity Log (Live)                                       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ 14:32:15 | CSV      | test.csv       | ✓ Success        │  │
│  │ 14:31:45 | CSV      | data.csv       | ⏸ Suspended (1/3)│  │
│  │ 14:30:22 | Session  | session_001/   | ✓ Success        │  │
│  │ 14:28:00 | DBQueue  | (5 records)    | ✓ Success        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Statistics: 45 converted | 2 suspended | 1 failed            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Migration Path

### Phase 1: Enhance Existing (Backward Compatible)

1. Add `ValidationResult` class
2. Add optional `validate()` method to `ConverterBase` 
3. Add `ConverterSource` abstraction
4. Enhance `ConverterResult` with retry_after

### Phase 2: Add New Converter Types

1. Create `FolderConverter` base class
2. Create `ScheduledConverter` base class  
3. Add folder watching capability
4. Add scheduler integration

### Phase 3: Auto-Selection & Confidence

1. Implement confidence scoring in ConverterManager
2. Add auto-selection logic
3. Add preview/validation UI
4. Enhance ConvertersPage

### Phase 4: AI Integration Preparation

1. Add server-side validation endpoint
2. Implement minimal-context submission
3. Create AI converter proxy

---

## Example Implementations

### File Converter Example

```python
class StdFTestConverter(FileConverter):
    """Converts Stdf format files to WATS reports"""
    
    @property
    def name(self) -> str:
        return "STDF Converter"
    
    @property
    def file_patterns(self) -> List[str]:
        return ["*.stdf", "*.std"]
    
    @property
    def arguments_schema(self) -> Dict[str, ArgumentDefinition]:
        return {
            "default_station": ArgumentDefinition(
                type=str,
                default="ATE-01",
                description="Default station name if not in file"
            ),
            "include_parametric": ArgumentDefinition(
                type=bool,
                default=True,
                description="Include parametric test data"
            )
        }
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        try:
            # Read header to detect STDF signature
            with open(source.path, 'rb') as f:
                header = f.read(4)
            
            # Check STDF magic number
            if header[:3] == b'FAR':
                return ValidationResult.perfect_match(
                    detected_part_number=self._extract_part_number(source.path)
                )
            
            return ValidationResult.no_match("Not a valid STDF file")
        except Exception as e:
            return ValidationResult.no_match(str(e))
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        # Conversion logic...
        pass
```

### Folder Converter Example

```python
class TestSessionConverter(FolderConverter):
    """Converts test session folders with multiple data files"""
    
    @property
    def name(self) -> str:
        return "Test Session Converter"
    
    @property
    def folder_pattern(self) -> str:
        return "session_*"
    
    @property
    def readiness_marker(self) -> str:
        return "session.complete"
    
    def validate(self, source: ConverterSource, context: ConverterContext) -> ValidationResult:
        # Check for required files
        required = ["data.json", "config.xml", "results.csv"]
        missing = [f for f in required if not (source.path / f).exists()]
        
        if missing:
            return ValidationResult.not_ready(
                missing=missing,
                retry_after=timedelta(seconds=30)
            )
        
        # Parse config for preview
        config = self._parse_config(source.path / "config.xml")
        return ValidationResult.perfect_match(
            detected_part_number=config.get("partNumber"),
            detected_serial_number=config.get("serialNumber"),
            detected_process=config.get("process")
        )
    
    def convert(self, source: ConverterSource, context: ConverterContext) -> ConverterResult:
        # Process all files in folder
        data = json.load(open(source.path / "data.json"))
        results = csv.reader(open(source.path / "results.csv"))
        config = self._parse_config(source.path / "config.xml")
        
        # Create report
        report = self._build_report(data, results, config)
        
        return ConverterResult.success_result(report=report)
```

### Scheduled Converter Example

```python
class DatabaseQueueConverter(ScheduledConverter):
    """Polls database for pending test records"""
    
    @property
    def name(self) -> str:
        return "Database Queue Converter"
    
    @property
    def schedule_interval_seconds(self) -> int:
        return 60  # Check every minute
    
    @property
    def arguments_schema(self) -> Dict[str, ArgumentDefinition]:
        return {
            "connection_string": ArgumentDefinition(
                type=str,
                required=True,
                description="Database connection string"
            ),
            "batch_size": ArgumentDefinition(
                type=int,
                default=100,
                description="Max records per run"
            )
        }
    
    async def run(self, context: ConverterContext) -> List[ConverterResult]:
        conn_str = context.get_argument("connection_string")
        batch_size = context.get_argument("batch_size", 100)
        
        results = []
        
        async with asyncpg.create_pool(conn_str) as pool:
            async with pool.acquire() as conn:
                # Fetch pending records
                records = await conn.fetch(
                    """
                    SELECT * FROM pending_tests 
                    WHERE processed = FALSE 
                    ORDER BY created_at 
                    LIMIT $1
                    """,
                    batch_size
                )
                
                for record in records:
                    try:
                        report = self._convert_record(record)
                        results.append(ConverterResult.success_result(
                            report=report,
                            metadata={"record_id": record['id']}
                        ))
                        
                        # Mark as processed
                        await conn.execute(
                            "UPDATE pending_tests SET processed = TRUE WHERE id = $1",
                            record['id']
                        )
                    except Exception as e:
                        results.append(ConverterResult.failed_result(str(e)))
        
        return results
```

---

## Configuration Example

```yaml
# converters.yaml
converters:
  - name: "csv_converter"
    type: file
    enabled: true
    module: "converters.csv_converter"
    class: "CSVConverter"
    watch_folder: "C:/TestData/Drop"
    file_patterns:
      - "*.csv"
      - "*.txt"
    post_process_action: move
    post_process_folder: "C:/TestData/Done"
    max_retries: 3
    retry_delay_seconds: 60
    arguments:
      delimiter: ","
      skip_header: true
      encoding: "utf-8"

  - name: "session_converter"
    type: folder
    enabled: true
    module: "converters.session_converter"
    class: "SessionConverter"
    watch_folder: "C:/TestData/Sessions"
    folder_pattern: "session_*"
    readiness_marker: ".complete"
    post_process_action: zip
    arguments:
      include_logs: true

  - name: "db_queue"
    type: scheduled
    enabled: true
    module: "converters.db_converter"
    class: "DatabaseQueueConverter"
    schedule_interval_seconds: 300
    arguments:
      connection_string: "postgresql://..."
      batch_size: 50
```

---

## Next Steps

1. **Review this design** - Feedback on the proposed architecture
2. **Implement Phase 1** - Backward-compatible enhancements
3. **Create test converters** - Validate the design with real use cases
4. **Implement remaining phases** - Full feature set
5. **Documentation update** - Update CONVERTER_ARCHITECTURE.md

---

## Questions to Consider

1. **Auto-selection threshold**: Should we require minimum confidence (e.g., 0.5) or always pick best match?

2. **Multiple converter matches**: What if multiple converters have same confidence? Priority setting? User prompt?

3. **Folder readiness**: Is marker file + timeout sufficient, or do we need more sophisticated detection?

4. **Scheduled converter isolation**: Should they run in separate process/thread to not block file processing?

5. **AI integration**: Should validation include a "submit to AI" fallback for unknown formats?
