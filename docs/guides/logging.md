# Logging Best Practices Guide

**pyWATS Logging Infrastructure**

This guide covers the unified logging infrastructure in pyWATS, including:
- Core logging framework (API)
- Client logging (services, CLI, GUI)
- Conversion logging (per-conversion tracking)
- Best practices and patterns

---

## Table of Contents

1. [Overview](#overview)
2. [Core Logging (API)](#core-logging-api)
3. [Client Logging](#client-logging)
4. [Conversion Logging](#conversion-logging)
5. [Best Practices](#best-practices)
6. [Performance Considerations](#performance-considerations)
7. [Troubleshooting](#troubleshooting)

---

## Overview

pyWATS uses a three-tier logging architecture:

```
┌─────────────────────────────────────────────────┐
│  Core Logging (pywats.core.logging)            │
│  - configure_logging()                          │
│  - Structured logging (JSON)                    │
│  - Correlation IDs                              │
│  - File rotation                                │
└─────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼─────────────┐
│  Client Logging  │    │  Conversion Logging  │
│  (pywats_client) │    │  (per-conversion)    │
│  - pywats.log    │    │  - {file}_{ts}.log   │
│  - Rotation      │    │  - JSON lines        │
│  - Instances     │    │  - Step tracking     │
└──────────────────┘    └──────────────────────┘
```

**Key Principles:**
- **Unified Configuration**: Single `configure_logging()` API
- **Separation of Concerns**: Different logs for different purposes
- **Structured Data**: JSON format for machine readability
- **Crash Safety**: Auto-flush for critical logs
- **Performance**: Minimal overhead (<5%)

---

## Core Logging (API)

### Quick Start

```python
from pywats.core.logging import configure_logging

# Simple configuration
configure_logging(level="INFO", format="text")

# Advanced configuration
configure_logging(
    level="DEBUG",
    format="json",
    file_path="logs/app.log",
    enable_rotation=True,
    rotate_size_mb=10,
    rotate_backups=5,
    enable_correlation_ids=True,
    enable_context=True
)
```

### Available Functions

#### `configure_logging()`

Unified logging configuration for all pyWATS components.

**Parameters:**
- `level` (str): Log level - "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
- `format` (Literal["text", "json"]): Output format
- `file_path` (Optional[Path]): Log file path (None = console only)
- `enable_rotation` (bool): Enable file rotation (default: True if file_path set)
- `rotate_size_mb` (int): Max file size in MB (default: 10)
- `rotate_backups` (int): Number of backup files (default: 5)
- `handlers` (Optional[List]): Custom handlers
- `enable_correlation_ids` (bool): Add correlation IDs to logs (default: False)
- `enable_context` (bool): Enable context variables (default: False)

**Example:**
```python
from pywats.core.logging import configure_logging
import logging

# Configure for production
configure_logging(
    level="INFO",
    format="json",
    file_path="logs/production.log",
    rotate_size_mb=50,  # 50MB per file
    rotate_backups=10,  # Keep 10 backup files
    enable_correlation_ids=True
)

# Use standard logging
logger = logging.getLogger(__name__)
logger.info("Application started", extra={"version": "1.0.0"})
```

#### `FileRotatingHandler`

Convenience wrapper for RotatingFileHandler with pyWATS defaults.

**Example:**
```python
from pywats.core.logging import FileRotatingHandler
import logging

handler = FileRotatingHandler(
    "logs/custom.log",
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=5
)

logger = logging.getLogger("custom")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

#### `LoggingContext`

Context manager for scoped logging metadata.

**Example:**
```python
from pywats.core.logging import LoggingContext
import logging

logger = logging.getLogger(__name__)

with LoggingContext(request_id="REQ-123", user="alice"):
    logger.info("Processing request")
    # Logs include {"request_id": "REQ-123", "user": "alice"}
    
    with LoggingContext(operation="validate"):
        logger.info("Validating data")
        # Logs include all parent context + {"operation": "validate"}
```

### Text vs JSON Format

**Text Format** (default):
```
2026-02-03 14:37:38,392 - myapp - INFO - Application started
```

**JSON Format** (structured):
```json
{
  "timestamp": "2026-02-03T14:37:38.392Z",
  "level": "INFO",
  "logger": "myapp",
  "message": "Application started",
  "version": "1.0.0"
}
```

**When to use JSON:**
- Production environments
- Log aggregation systems (ELK, Splunk)
- Machine parsing required
- Advanced filtering/querying

**When to use text:**
- Development
- Console output
- Human-readable logs
- Simple debugging

---

## Client Logging

### Quick Start

```python
from pywats_client.core.logging import setup_client_logging

# Setup client logging
log_path = setup_client_logging(
    instance_id="production_station",
    log_level="INFO",
    log_format="text",
    enable_console=True
)

# All logs now go to pywats.log with rotation
import logging
logger = logging.getLogger(__name__)
logger.info("Service started")
```

### Client Logging Functions

#### `setup_client_logging()`

Configure unified logging for client applications.

**Parameters:**
- `instance_id` (str): Client instance identifier (default: "default")
- `log_level` (str): Logging level (default: "INFO")
- `log_format` (Literal["text", "json"]): Output format (default: "text")
- `enable_console` (bool): Also log to console (default: True)
- `rotate_size_mb` (int): Max file size in MB (default: 10)
- `rotate_backups` (int): Number of backup files (default: 5)

**Returns:** Path to pywats.log file

**Log Location:**
- Windows: `C:\ProgramData\pyWATS\{instance_id}\pywats.log`
- Linux: `~/.pywats/{instance_id}/pywats.log`

**Example:**
```python
from pywats_client.core.logging import setup_client_logging

# Headless service (no console)
setup_client_logging(
    instance_id="test_station_1",
    log_level="DEBUG",
    enable_console=False
)

# GUI with JSON logging
setup_client_logging(
    instance_id="gui_instance",
    log_level="INFO",
    log_format="json",
    enable_console=True,
    rotate_size_mb=20,
    rotate_backups=10
)
```

#### `get_conversion_log_dir()`

Get the directory for conversion logs.

**Example:**
```python
from pywats_client.core.logging import get_conversion_log_dir

log_dir = get_conversion_log_dir("production")
# Returns: C:\ProgramData\pyWATS\production\logs\conversions
```

#### `cleanup_old_conversion_logs()`

Clean up old conversion log files.

**Example:**
```python
from pywats_client.core.logging import cleanup_old_conversion_logs

# Preview what would be deleted
count = cleanup_old_conversion_logs(max_age_days=30, dry_run=True)
print(f"Would delete {count} old logs")

# Actually delete
count = cleanup_old_conversion_logs(max_age_days=30)
print(f"Deleted {count} old conversion logs")
```

---

## Conversion Logging

### Overview

ConversionLog provides per-conversion detailed tracking with:
- JSON line format (one JSON object per line)
- Step-by-step tracking
- Warning and error capture
- Auto-flush for crash safety
- Unique timestamped files

**Log Location:**
`{install_dir}/logs/conversions/{filename}_{timestamp}.log`

### Quick Start

```python
from pywats_client.converters.conversion_log import ConversionLog

# Create log for conversion
log = ConversionLog.create_for_file("test_data.csv", instance_id="station_a")

# Log conversion steps
log.step("Reading file", metadata={"size_bytes": 1024})
log.step("Parsing CSV", metadata={"rows": 10})
log.warning("Missing column: temperature")
log.step("Creating report", metadata={"serial": "SN123"})

# Finalize (success)
log.finalize(success=True, report_id=456)

# Or finalize (failure)
# log.finalize(success=False, error="Parse error at line 5")
```

### ConversionLog API

#### `ConversionLog.create_for_file()`

Create a ConversionLog for a specific file.

**Parameters:**
- `file_name` (str): Name of file being converted
- `instance_id` (str): Client instance identifier (default: "default")

**Returns:** ConversionLog instance

**Example:**
```python
log = ConversionLog.create_for_file("production_data.csv", "station_1")
# Creates: {install_dir}/logs/conversions/production_data_20260203_143022.log
```

#### `log.step()`

Log a conversion step (INFO level).

**Parameters:**
- `step_name` (str): Name/description of the step
- `message` (str): Optional message (default: "Started")
- `metadata` (Optional[Dict]): Additional data

**Example:**
```python
log.step("Reading file", metadata={"path": "/data/test.csv", "size": 1024})
log.step("Parsing CSV", message="Found 25 rows", metadata={"rows": 25})
```

#### `log.warning()`

Log a warning (WARNING level).

**Parameters:**
- `message` (str): Warning message
- `step` (str): Step name where warning occurred (default: "Validation")
- `metadata` (Optional[Dict]): Additional data

**Example:**
```python
log.warning("Missing optional field: operator_notes")
log.warning("Serial format unusual", metadata={"serial": "ABC-123"})
```

#### `log.error()`

Log an error (ERROR level).

**Parameters:**
- `message` (str): Error message
- `step` (str): Step name where error occurred (default: "Conversion")
- `metadata` (Optional[Dict]): Additional data
- `exception` (Optional[Exception]): Exception object (extracts type/message)

**Example:**
```python
log.error("Failed to parse CSV", metadata={"line": 5})

try:
    data = parse_file()
except ValueError as e:
    log.error("Parse error", exception=e)
```

#### `log.finalize()`

Finalize the conversion log.

**Parameters:**
- `success` (bool): Whether conversion succeeded
- `report_id` (Optional[int]): WATS report ID if successful
- `error` (Optional[str]): Error message if failed
- `metadata` (Optional[Dict]): Additional data

**Example:**
```python
# Success
log.finalize(success=True, report_id=456, metadata={"rows_processed": 25})

# Failure
log.finalize(success=False, error="Invalid file format")
```

### Using ConversionLog in Converters

```python
from pathlib import Path
from pywats_client.converters.base import ConverterBase, ConverterArguments, ConverterResult

class MyConverter(ConverterBase):
    def convert_file(self, file_path: Path, args: ConverterArguments) -> ConverterResult:
        # Get ConversionLog if provided
        log = args.conversion_log
        
        try:
            # Log each major step
            if log:
                log.step("Reading file")
            
            with open(file_path, 'r') as f:
                data = f.read()
            
            if log:
                log.step("Parsing data", metadata={"size": len(data)})
            
            # ... conversion logic ...
            
            # Log warnings for non-critical issues
            if not some_optional_field:
                if log:
                    log.warning("Optional field missing: temperature")
            
            # Create report
            report = {...}
            
            if log:
                log.step("Report created", metadata={"serial": report["serialNumber"]})
            
            # Note: Caller will finalize log with success=True and report_id
            return ConverterResult.success_result(report=report)
        
        except Exception as e:
            # Log error with full context
            if log:
                log.error(f"Conversion failed: {str(e)}", exception=e)
            
            # Caller will finalize log with success=False
            return ConverterResult.failed_result(error=str(e))
```

### Context Manager Pattern

```python
from pywats_client.converters.conversion_log import ConversionLog

# Auto-finalize on exception
with ConversionLog.create_for_file("data.csv") as log:
    log.step("Processing")
    # If exception occurs, log is automatically finalized with error
    raise ValueError("Test error")

# Log is finalized: {"level": "ERROR", "step": "FAILED", "message": "..."}
```

---

## Best Practices

### 1. Choose the Right Log Level

```python
logger.debug("Detailed variable values: x=5, y=10")    # Development
logger.info("User logged in: alice")                   # Important events
logger.warning("API rate limit approaching")           # Issues to watch
logger.error("Failed to process order #123")           # Errors
logger.critical("Database connection lost!")           # System-level failures
```

### 2. Use Structured Logging

```python
# ❌ Bad: String formatting loses structure
logger.info(f"User {user_id} processed {count} items")

# ✅ Good: Use extra parameter for structured data
logger.info(
    "User processed items",
    extra={"user_id": user_id, "item_count": count}
)
```

### 3. Add Context for Debugging

```python
from pywats.core.logging import LoggingContext

with LoggingContext(order_id=order_id, customer=customer_name):
    logger.info("Processing order")
    process_payment()  # Logs include order_id and customer
    send_confirmation()  # Logs include order_id and customer
```

### 4. Log Exceptions Properly

```python
# ❌ Bad: Loses stack trace
try:
    risky_operation()
except Exception as e:
    logger.error(f"Error: {e}")

# ✅ Good: Includes full stack trace
try:
    risky_operation()
except Exception as e:
    logger.exception("Operation failed")  # or logger.error("...", exc_info=True)
```

### 5. Use ConversionLog for Converters

```python
# ✅ Always check if ConversionLog is available
log = args.conversion_log

if log:
    log.step("Reading file", metadata={"path": str(file_path)})

# ✅ Log each major step
# ✅ Log warnings for non-critical issues
# ✅ Log errors with full context
# ✅ Let caller finalize the log
```

### 6. Avoid Logging Sensitive Data

```python
# ❌ Bad: Logs password
logger.info(f"Login attempt: user={username}, pass={password}")

# ✅ Good: Logs only non-sensitive data
logger.info("Login attempt", extra={"username": username, "success": True})
```

### 7. Clean Up Old Logs

```python
from pywats_client.core.logging import cleanup_old_conversion_logs

# Schedule periodic cleanup (e.g., daily)
cleanup_old_conversion_logs(max_age_days=30)
```

---

## Performance Considerations

### Logging Overhead

pyWATS logging infrastructure is designed for minimal overhead (<5% in typical scenarios).

**Benchmarks:**
- Text logging: ~50-100 μs per call
- JSON logging: ~100-200 μs per call
- File rotation: ~1-2 ms per rotation
- ConversionLog (auto-flush): ~200-300 μs per entry

### Optimization Tips

1. **Use appropriate log levels**
   ```python
   # Production: INFO or WARNING
   configure_logging(level="INFO")
   
   # Development: DEBUG
   configure_logging(level="DEBUG")
   ```

2. **Disable debug logging in production**
   ```python
   # ❌ Slow: Evaluates even when not logging
   logger.debug(f"Data: {expensive_operation()}")
   
   # ✅ Fast: Only evaluates if DEBUG enabled
   if logger.isEnabledFor(logging.DEBUG):
       logger.debug(f"Data: {expensive_operation()}")
   ```

3. **Use lazy evaluation for expensive operations**
   ```python
   # ✅ Good: Extra dict is only created if logged
   logger.info("Processing", extra={"data": large_object})
   ```

4. **Batch operations when possible**
   ```python
   # ❌ Slow: Many small logs
   for item in items:
       logger.debug(f"Processing {item}")
   
   # ✅ Fast: Single log with summary
   logger.info(f"Processed {len(items)} items", extra={"count": len(items)})
   ```

---

## Troubleshooting

### Logs Not Appearing

```python
# Check log level
import logging
logger = logging.getLogger(__name__)
print(f"Logger level: {logger.level}")
print(f"Root level: {logging.root.level}")

# Check handlers
for handler in logger.handlers:
    print(f"Handler: {handler}, Level: {handler.level}")
```

### Log File Not Created

```python
from pywats_client.core.logging import get_client_log_path

# Check expected path
log_path = get_client_log_path("my_instance")
print(f"Expected log path: {log_path}")
print(f"Exists: {log_path.exists()}")
print(f"Parent exists: {log_path.parent.exists()}")
```

### Rotation Not Working

```python
from pywats.core.logging import configure_logging

# Ensure rotation is enabled
configure_logging(
    level="INFO",
    file_path="logs/app.log",
    enable_rotation=True,  # Must be True
    rotate_size_mb=10
)
```

### ConversionLog Files Missing

```python
from pywats_client.core.logging import get_conversion_log_dir

# Check conversion log directory
conv_dir = get_conversion_log_dir("my_instance")
print(f"Conversion log dir: {conv_dir}")
print(f"Exists: {conv_dir.exists()}")
print(f"Files: {list(conv_dir.glob('*.log'))}")
```

### JSON Format Not Working

```python
from pywats.core.logging import configure_logging

# Ensure format="json"
configure_logging(
    level="INFO",
    format="json",  # Must be "json"
    file_path="logs/app.log"
)

# Verify formatter
import logging
logger = logging.getLogger()
for handler in logger.handlers:
    print(f"Formatter type: {type(handler.formatter).__name__}")
    # Should be "StructuredFormatter" for JSON
```

---

## Migration Guide

### From basicConfig()

```python
# ❌ Old
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# ✅ New
from pywats.core.logging import configure_logging
configure_logging(level="INFO", format="text")
```

### From Custom File Handlers

```python
# ❌ Old
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("app.log", maxBytes=10*1024*1024, backupCount=5)
logger = logging.getLogger()
logger.addHandler(handler)

# ✅ New
from pywats.core.logging import configure_logging
configure_logging(
    level="INFO",
    file_path="app.log",
    rotate_size_mb=10,
    rotate_backups=5
)
```

### For Client Services

```python
# ❌ Old
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ✅ New
from pywats_client.core.logging import setup_client_logging
setup_client_logging(instance_id="my_service", log_level="INFO")
```

---

## Examples

See the [examples/](../../examples/) directory for complete examples:

- `examples/observability/logging_demo.py` - Core logging features
- `examples/converters/logging_example_converter.py` - ConversionLog usage
- `examples/client/sync_with_config.py` - Client logging

---

## Reference

### Module Locations

- Core: `pywats.core.logging`
- Client: `pywats_client.core.logging`
- Conversion: `pywats_client.converters.conversion_log`

### Related Documentation

- [Architecture Guide](architecture.md)
- [API Reference](../api/logging.rst)
- [MIGRATION.md](../../MIGRATION.md) - Breaking changes

---

**Last Updated:** February 3, 2026  
**Version:** pyWATS 0.3.0
