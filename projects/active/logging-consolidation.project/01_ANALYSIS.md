# Analysis: Logging Infrastructure

**Date:** February 3, 2026  
**Type:** Infrastructure Audit & Design

---

## 🎯 Problem Statement

The pyWATS codebase has **dispersed, inconsistent, and duplicated logging implementations** across API, Client, GUI, and Converters:

1. **Multiple Configuration Points:** Logging configured in at least 5 different locations
2. **No Unified Framework:** Each component reinvents logging patterns
3. **Missing Features:** No per-conversion logs, incomplete exception tracking
4. **Inconsistent Structured Logging:** JSON logging only in API core
5. **No Client Persistence:** Client logs not properly persisted to installation directory
6. **Poor Exception Handling:** Converter exceptions don't bubble properly to GUI

**Current Pain Points:**
- Developers don't know which logging pattern to use
- Troubleshooting requires checking multiple log locations
- Converter errors hidden from users
- Inconsistent log formats across components
- Duplicate code for common logging tasks

---

## 📋 Current State Audit

### Logging Locations Discovered

#### 1. **API Core Logging** (`src/pywats/core/logging.py`)
**Status:** ✅ Well-designed, structured logging support  
**Features:**
- `StructuredFormatter` for JSON logging
- `CorrelationFilter` for request tracking
- `get_logger()` utility function
- Context variable support (`set_logging_context()`)
- Helper functions: `enable_debug_logging()`, `enable_json_logging()`

**Issues:**
- Limited to API package only
- Not used by client or converters
- No file persistence built-in

**Lines of Code:** ~285 lines

---

#### 2. **Client CLI Logging** (`src/pywats_client/cli.py`)
**Status:** ⚠️ Basic configuration, inconsistent  
**Pattern:**
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)
```

**Issues:**
- Uses `basicConfig` (overrides existing configuration)
- Simple format (no timestamps, no correlation IDs)
- No file output
- Conflicts with other logging setups

---

#### 3. **Client Service Logging** (`src/pywats_client/control/service.py`)
**Status:** ⚠️ Custom implementation, not reusable  
**Pattern:**
```python
def _setup_logging(self):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_path)
    logging.basicConfig(level=log_level, handlers=handlers, force=True)
```

**Issues:**
- Hardcoded in service class
- No rotation (files grow unbounded)
- Format string duplicated
- Not accessible to other components

**Current Behavior:**
- Logs to file only if `log_to_file=True`
- File path: `{reports_path.parent}/{log_file}`
- No structured logging support

---

#### 4. **Converter Logging** (`src/pywats_client/converters/base.py`)
**Status:** ❌ Missing - only basic logger instances  
**Pattern:**
```python
logger = logging.getLogger(__name__)  # In functions, not in class
```

**Issues:**
- No `ConversionLog` implementation
- No per-conversion tracking
- Converter errors not properly logged
- No detailed step logging

**Missing Features:**
- Conversion start/end timestamps
- Step-by-step progress tracking
- File-specific logs per conversion
- Error context preservation

---

#### 5. **Domain Services** (50+ files)
**Status:** ✅ Consistent pattern, but basic  
**Pattern:**
```python
import logging
logger = logging.getLogger(__name__)
```

**Issues:**
- Each file creates its own logger
- No centralized configuration
- No structured logging usage
- Inconsistent log levels

**Example Locations:**
- `src/pywats/domains/*/async_service.py`
- `src/pywats/domains/*/async_repository.py`
- `src/pywats_events/**/*.py`
- `src/pywats/queue/**/*.py`

---

#### 6. **Examples & Documentation**
**Status:** ❌ Inconsistent, sometimes wrong  
**Issues:**
- Mix of `logging.basicConfig()` and custom setup
- No structured logging examples
- Outdated patterns in older docs
- Missing best practices guide

---

### Duplication Analysis

**Duplicated Code:**
1. **Log Format Strings:** At least 3 different formats
   - `'%(levelname)s: %(message)s'` (CLI)
   - `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'` (Service)
   - Custom formats in examples

2. **Logger Creation:** `logging.getLogger(__name__)` repeated 50+ times

3. **Configuration Logic:** 3 different `basicConfig` calls

4. **File Handlers:** Duplicate file handler setup in multiple places

**Estimated Lines of Duplicate Code:** ~150+ lines

---

## 📊 Requirements Analysis

### Functional Requirements

**Must Have:**

1. **Unified Logging Framework**
   - Single module for configuration: `pywats.core.logging` (enhance existing)
   - Reusable across API, Client, GUI, Converters
   - Structured logging (JSON) support everywhere
   - Correlation ID tracking end-to-end

2. **Top-Level Client Log (`pywats.log`)**
   - Location: Client installation directory (configurable)
   - Rotating file handler (size: 10MB, backups: 5)
   - Time-based rotation option (daily/weekly)
   - All client service activity logged
   - Format: Structured JSON or traditional text (configurable)

3. **Per-Conversion Logging**
   - `ConversionLog` class in `ConverterBase`
   - Automatic creation per conversion
   - Detailed step tracking API:
     ```python
     log.step("Parsing CSV", details={"rows": 150})
     log.warning("Missing column: temperature")
     log.error("Validation failed", exc=exception)
     ```
   - File output: `{conversion_logs_dir}/{timestamp}_{filename}.log`
   - Optional: Keep last N logs, auto-cleanup old logs

4. **Exception Handling Pipeline**
   - Converter exceptions captured with full context
   - Logged to both `ConversionLog` and `pywats.log`
   - Bubbled to client service with stack trace
   - Forwarded to GUI with user-friendly message
   - Debug details available in logs

5. **Component Separation**
   - API logging: `pywats.core.logging` (existing + enhancements)
   - Client logging: `pywats_client.core.logging` (new, imports from API)
   - GUI logging: Uses client logging via clean interface
   - Converter logging: Integrated into `ConverterBase`

6. **Configuration API**
   ```python
   from pywats.core.logging import configure_logging
   
   configure_logging(
       level="INFO",
       format="json",  # or "text"
       file_path="pywats.log",
       rotate_size_mb=10,
       rotate_backups=5,
       enable_correlation_ids=True,
       enable_context=True
   )
   ```

**Should Have:**

7. **Performance Monitoring**
   - Log entry timing (debug mode)
   - Async logging for high-throughput scenarios
   - Buffer configuration (memory vs immediate flush)

8. **Filtering & Redaction**
   - Sensitive data redaction (passwords, tokens)
   - Component-specific log levels
   - Rate limiting for repeated messages

9. **Observability Integration**
   - Prometheus metrics for log events
   - OpenTelemetry span integration
   - Health check endpoint showing log status

**Nice to Have:**

10. **Log Viewer Integration**
    - Client log viewer (future GUI app)
    - Real-time log streaming
    - Search and filter capabilities

---

### Non-Functional Requirements

**Performance:**
- Logging overhead < 5% in production
- Async logging for I/O operations
- Minimal memory footprint (buffered writes)

**Reliability:**
- No log loss during crashes (flush buffers)
- Graceful degradation if disk full
- Auto-recovery from logging errors

**Maintainability:**
- Single source of truth for logging config
- Clear migration path from old patterns
- Comprehensive documentation

**Testability:**
- Mock logging in unit tests
- Capture logs for assertion
- No side effects in test suite

---

## 🏗️ Architecture Design

### Proposed Structure

```
src/
  pywats/
    core/
      logging.py                    # Enhanced unified framework (285 → 450 lines)
        - StructuredFormatter       # ✅ Existing
        - CorrelationFilter         # ✅ Existing
        - configure_logging()       # 🆕 New unified config
        - get_logger()              # ✅ Existing
        - FileRotatingHandler       # 🆕 Wrapper for rotation config
        - LoggingContext            # 🆕 Context manager for scoped logging
  
  pywats_client/
    core/
      logging.py                    # Client-specific logging (NEW, ~200 lines)
        - setup_client_logging()    # Configure pywats.log
        - get_log_path()            # Installation directory path
        - ClientLogHandler          # Custom handler for client needs
    
    converters/
      base.py                       # Enhanced with ConversionLog
        - ConversionLog             # 🆕 Per-conversion logging (~150 lines)
          - step(message, **context)
          - warning(message, **context)
          - error(message, exc=None)
          - finalize()
      
      models.py                     # Models for conversion logging
        - ConversionLogEntry        # 🆕 Log entry dataclass
        - ConversionLogConfig       # 🆕 Configuration

examples/
  observability/
    logging_patterns.py             # 🆕 Comprehensive logging examples
    conversion_logging.py           # 🆕 Converter logging demo
```

### Key Components

#### 1. Enhanced `pywats.core.logging` (Unified Framework)

**New Functions:**
```python
def configure_logging(
    level: Union[str, int] = "INFO",
    format: Literal["text", "json"] = "text",
    handlers: Optional[List[logging.Handler]] = None,
    file_path: Optional[Path] = None,
    rotate_size_mb: int = 10,
    rotate_backups: int = 5,
    enable_correlation_ids: bool = True,
    enable_context: bool = True
) -> None:
    """Configure logging for pyWATS applications."""
```

**New Classes:**
```python
class FileRotatingHandler(logging.handlers.RotatingFileHandler):
    """Enhanced rotating file handler with pyWATS defaults."""

class LoggingContext:
    """Context manager for scoped logging metadata."""
    def __init__(self, **context):
        self.context = context
    
    def __enter__(self):
        set_logging_context(self.context)
    
    def __exit__(self, *args):
        clear_logging_context()
```

---

#### 2. New `pywats_client.core.logging` (Client Integration)

```python
from pywats.core.logging import configure_logging, get_logger

def setup_client_logging(
    instance_id: str = "default",
    log_level: str = "INFO",
    enable_file_logging: bool = True,
    enable_console: bool = True
) -> Path:
    """
    Configure logging for client service.
    
    Creates top-level pywats.log in installation directory.
    Returns path to log file.
    """
    from .config import ClientConfig
    
    config = ClientConfig.load_for_instance(instance_id)
    log_dir = config.get_installation_dir() / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_path = log_dir / f"pywats_{instance_id}.log"
    
    handlers = []
    if enable_console:
        handlers.append(logging.StreamHandler(sys.stdout))
    if enable_file_logging:
        handlers.append(FileRotatingHandler(
            log_path,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ))
    
    configure_logging(
        level=log_level,
        handlers=handlers,
        enable_correlation_ids=True,
        enable_context=True
    )
    
    return log_path

def get_conversion_log_dir(instance_id: str = "default") -> Path:
    """Get directory for conversion logs."""
    from .config import ClientConfig
    config = ClientConfig.load_for_instance(instance_id)
    log_dir = config.get_installation_dir() / "logs" / "conversions"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir
```

---

#### 3. `ConversionLog` in `ConverterBase`

```python
@dataclass
class ConversionLogEntry:
    """Single log entry in a conversion."""
    timestamp: datetime
    level: str  # INFO, WARNING, ERROR
    message: str
    context: Dict[str, Any] = field(default_factory=dict)
    exception: Optional[Exception] = None

class ConversionLog:
    """
    Per-conversion logging with detailed step tracking.
    
    Automatically created by ConverterBase for each conversion.
    Logs are written to {conversion_logs_dir}/{timestamp}_{filename}.log
    
    Example:
        log = ConversionLog("file.csv", args.file_info)
        log.step("Starting conversion")
        log.step("Parsing CSV", rows=150)
        log.warning("Missing column: temperature")
        try:
            validate(data)
        except ValidationError as e:
            log.error("Validation failed", exc=e)
        log.finalize(success=False)
    """
    
    def __init__(
        self,
        conversion_id: str,
        file_info: FileInfo,
        log_dir: Path
    ):
        self.conversion_id = conversion_id
        self.file_info = file_info
        self.log_path = log_dir / f"{conversion_id}.log"
        self.entries: List[ConversionLogEntry] = []
        self.start_time = datetime.now(timezone.utc)
        self._file: Optional[TextIO] = None
        
        # Open log file
        self._open()
        self._write_header()
    
    def _open(self):
        """Open log file for writing."""
        self._file = open(self.log_path, 'w', encoding='utf-8')
    
    def _write_header(self):
        """Write conversion metadata header."""
        self._write({
            "event": "conversion_start",
            "conversion_id": self.conversion_id,
            "file": self.file_info.name,
            "size": self.file_info.size,
            "timestamp": self.start_time.isoformat()
        })
    
    def step(self, message: str, **context):
        """Log a conversion step (INFO level)."""
        entry = ConversionLogEntry(
            timestamp=datetime.now(timezone.utc),
            level="INFO",
            message=message,
            context=context
        )
        self.entries.append(entry)
        self._write_entry(entry)
    
    def warning(self, message: str, **context):
        """Log a warning."""
        entry = ConversionLogEntry(
            timestamp=datetime.now(timezone.utc),
            level="WARNING",
            message=message,
            context=context
        )
        self.entries.append(entry)
        self._write_entry(entry)
    
    def error(self, message: str, exc: Optional[Exception] = None, **context):
        """Log an error with optional exception."""
        entry = ConversionLogEntry(
            timestamp=datetime.now(timezone.utc),
            level="ERROR",
            message=message,
            context=context,
            exception=exc
        )
        self.entries.append(entry)
        self._write_entry(entry)
        
        if exc:
            # Write full traceback
            import traceback
            tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            self._write({"traceback": tb})
    
    def finalize(self, success: bool, reports_created: int = 0):
        """Finalize conversion logging."""
        duration = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        
        self._write({
            "event": "conversion_complete",
            "success": success,
            "duration_seconds": duration,
            "reports_created": reports_created,
            "total_entries": len(self.entries),
            "warnings": sum(1 for e in self.entries if e.level == "WARNING"),
            "errors": sum(1 for e in self.entries if e.level == "ERROR")
        })
        
        if self._file:
            self._file.close()
            self._file = None
    
    def _write_entry(self, entry: ConversionLogEntry):
        """Write single log entry to file."""
        data = {
            "timestamp": entry.timestamp.isoformat(),
            "level": entry.level,
            "message": entry.message
        }
        if entry.context:
            data.update(entry.context)
        self._write(data)
    
    def _write(self, data: Dict[str, Any]):
        """Write JSON line to log file."""
        if self._file:
            self._file.write(json.dumps(data) + '\n')
            self._file.flush()  # Ensure immediate write

# Integration into ConverterBase
class ConverterBase(ABC):
    # ... existing code ...
    
    def convert_file(
        self,
        file_path: Path,
        args: ConverterArguments
    ) -> ConverterResult:
        """
        Template method that wraps conversion with logging.
        Subclasses override convert_with_logging().
        """
        # Create conversion log
        conversion_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{args.file_info.name}"
        log_dir = get_conversion_log_dir()  # From pywats_client.core.logging
        
        conversion_log = ConversionLog(conversion_id, args.file_info, log_dir)
        
        try:
            conversion_log.step("Starting conversion")
            result = self.convert_with_logging(file_path, args, conversion_log)
            
            if result.status == ConversionStatus.SUCCESS:
                conversion_log.step("Conversion successful", 
                                  reports_created=len(result.reports))
                conversion_log.finalize(success=True, 
                                      reports_created=len(result.reports))
            else:
                conversion_log.finalize(success=False)
            
            return result
            
        except Exception as e:
            conversion_log.error("Conversion failed with exception", exc=e)
            conversion_log.finalize(success=False)
            
            # Re-raise to bubble to client
            raise
    
    @abstractmethod
    def convert_with_logging(
        self,
        file_path: Path,
        args: ConverterArguments,
        log: ConversionLog  # NEW parameter
    ) -> ConverterResult:
        """
        Convert file to WATS reports with detailed logging.
        
        Subclasses must implement this instead of convert_file.
        Use `log` parameter to track conversion steps.
        """
        pass
```

---

## 🔄 Exception Bubbling Flow

```
┌─────────────────────┐
│   Converter.py      │
│  (User Code)        │
└──────┬──────────────┘
       │ Exception raised
       │ ↓
┌──────▼──────────────┐
│  ConversionLog      │
│  - Capture exception│
│  - Log full trace   │
│  - Write to file    │
└──────┬──────────────┘
       │ Re-raise
       │ ↓
┌──────▼──────────────┐
│  ConverterBase      │
│  - Log to pywats.log│
│  - Add context      │
└──────┬──────────────┘
       │ Re-raise
       │ ↓
┌──────▼──────────────┐
│  Client Service     │
│  - Log error        │
│  - Update status    │
│  - Notify GUI       │
└──────┬──────────────┘
       │ Error event
       │ ↓
┌──────▼──────────────┐
│  GUI (if attached)  │
│  - Show user error  │
│  - Link to log file │
└─────────────────────┘
```

---

## 📊 Comparison: Current vs Proposed

| Aspect | Current | Proposed | Improvement |
|--------|---------|----------|-------------|
| **Unified Config** | ❌ Multiple places | ✅ Single module | Clear ownership |
| **Structured Logging** | ⚠️ API only | ✅ All components | Consistency |
| **Client Log File** | ⚠️ Basic, no rotation | ✅ Rotating, configurable | Production-ready |
| **Conversion Logs** | ❌ Missing | ✅ Per-conversion detail | Troubleshooting |
| **Exception Tracking** | ⚠️ Partial | ✅ End-to-end pipeline | Full visibility |
| **Code Duplication** | ❌ ~150 lines | ✅ Minimal | Maintainability |
| **Performance** | ✅ Good | ✅ Same or better | Optimized |
| **Documentation** | ⚠️ Scattered | ✅ Comprehensive | Developer experience |

---

## ⚠️ Risk Assessment

### HIGH Risk
- **Breaking Existing Code:** Changing logging patterns could break existing converters
  - *Mitigation:* Deprecation path, backward compatibility shims, gradual migration

### MEDIUM Risk
- **Performance Impact:** Structured logging and file I/O could add overhead
  - *Mitigation:* Async logging, benchmarking, optional features

- **Disk Space:** Conversion logs could accumulate
  - *Mitigation:* Auto-cleanup, configurable retention, size limits

### LOW Risk
- **Complexity:** More sophisticated logging framework
  - *Mitigation:* Clear documentation, examples, helper utilities

---

## 🎯 Recommendation

**Preferred Approach:** Enhance existing `pywats.core.logging` + add client-specific module

**Rationale:**
1. Builds on solid foundation (existing structured logging)
2. Minimal breaking changes
3. Clear component separation
4. Reusable across API, Client, GUI
5. Ready for GUI separation

**Implementation Priority:**
1. **Phase 1:** Enhance `pywats.core.logging` with unified config
2. **Phase 2:** Add `pywats_client.core.logging` with file persistence
3. **Phase 3:** Implement `ConversionLog` in `ConverterBase`
4. **Phase 4:** Migrate existing code, update examples
5. **Phase 5:** Documentation and testing

**Total Effort Estimate:** 2 weeks (40-60 hours)

---

*Analysis Complete: February 3, 2026*
