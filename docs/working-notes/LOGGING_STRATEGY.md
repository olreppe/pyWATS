# Logging and Console Output Strategy for PyWATS

**Date:** December 12, 2025  
**Updated:** January 2025  
**Topic:** Architectural recommendations for logging and console output

## Executive Summary

Based on your layered architecture (Facade → Service → Repository → HttpClient), here's the recommended approach:

**Console Output:** Core API feature (minimal, structured)  
**Logging:** Client application feature (comprehensive, configurable)

This follows the **Separation of Concerns** principle and allows library users to control their own logging strategies.

## ✅ Implementation Status (January 2025)

Enhanced INFO-level logging has been added to all service layer mutating operations:

### Logged Operations by Domain

| Domain | Operations | Log Format |
|--------|------------|------------|
| **Asset** | create, update, delete, state_change, calibration, maintenance, counter_reset, type_create, child_add, file_upload, log_message | `ASSET_*: identifier (key=value)` |
| **Product** | create, update, bulk_save, revision_create, revision_update, bom_update | `PRODUCT_*: part_number (key=value)` |
| **Production** | create_units, update_unit | `UNIT_*: serial_number (pn=part_number)` |
| **Report** | submit, submit_xml | `REPORT_SUBMITTED: id=guid (pn=..., sn=...)` |
| **RootCause** | create_ticket, update, comment, status_change, assign, archive | `TICKET_*: ticket_id (key=value)` |
| **Software** | create_package, update, delete, status_workflow, upload_zip | `PACKAGE_*: name (key=value)` |

### Log Message Format

All log messages follow a consistent format for easy filtering and parsing:

```
DOMAIN_ACTION: identifier (key=value, key=value)
```

Examples:
- `ASSET_CREATED: SN-123 (type_id=abc, name=Station1)`
- `UNIT_UPDATED: UNIT-456 (pn=PROD-001)`
- `REPORT_SUBMITTED: id=abc-123-def (pn=PROD-001, sn=UNIT-456)`
- `TICKET_STATUS_CHANGED: 550e8400-e29b-41d4-a716-446655440000 (status=SOLVED)`
- `PACKAGE_RELEASED: id=pkg-123 (status=RELEASED)`

### How to Use

```python
import logging

# Enable INFO level to see operation logs
logging.basicConfig(level=logging.INFO)

# Or filter to just pywats logs
logging.getLogger('pywats').setLevel(logging.INFO)

# Hook into specific domains
logging.getLogger('pywats.domains.asset.service').setLevel(logging.INFO)
logging.getLogger('pywats.domains.report.service').setLevel(logging.INFO)
```

---

## 🎯 Recommended Architecture

### Layer 1: Core API (PyWATS Library) - Minimal Output

**Philosophy:** Libraries should be quiet by default, let applications decide what to log.

```
┌─────────────────────────────────────────────┐
│  Core API (PyWATS)                          │
│  - Use Python's logging module             │
│  - Create named loggers                     │
│  - NEVER print() directly                   │
│  - Let applications configure handlers      │
└─────────────────────────────────────────────┘
```

**Implementation:**

```python
# src/pywats/core/client.py
import logging

logger = logging.getLogger("pywats.core.client")

class HttpClient:
    def get(self, endpoint: str, **kwargs):
        logger.debug(f"GET {endpoint}")
        response = httpx.get(...)
        logger.debug(f"Response: {response.status_code}")
        return response
```

**Key Points:**
- ✅ Use `logging.getLogger(__name__)` in every module
- ✅ Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- ❌ NEVER use `print()` in library code
- ❌ NEVER configure logging handlers in the library

### Layer 2: Client Application - Full Control

**Philosophy:** Applications configure logging to their needs.

```python
# pywats_client/app.py or user scripts
import logging
from pywats import pyWATS

# User configures logging as they want
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pywats.log'),
        logging.StreamHandler()  # Console output
    ]
)

# Or use their own logging configuration
api = pyWATS(...)
```

---

## 📋 Detailed Implementation Plan

### 1. Core API Logging Structure

```
pywats/
  __init__.py          → logger: "pywats"
  core/
    client.py          → logger: "pywats.core.client"
    exceptions.py      → logger: "pywats.core.exceptions"
  domains/
    product/
      service.py       → logger: "pywats.domains.product.service"
      repository.py    → logger: "pywats.domains.product.repository"
    report/
      service.py       → logger: "pywats.domains.report.service"
      repository.py    → logger: "pywats.domains.report.repository"
```

**Pattern for every module:**

```python
"""Module docstring"""
import logging

logger = logging.getLogger(__name__)

class MyClass:
    def my_method(self):
        logger.debug("Starting operation")
        try:
            result = self._do_something()
            logger.info("Operation successful")
            return result
        except Exception as e:
            logger.error(f"Operation failed: {e}", exc_info=True)
            raise
```

### 2. Logging Levels Guide

| Level | Use Case | Example |
|-------|----------|---------|
| **DEBUG** | Detailed diagnostic info | `logger.debug(f"Calling GET /api/Product/{part_number}")` |
| **INFO** | Confirmation of expected operations | `logger.info(f"Retrieved {len(products)} products")` |
| **WARNING** | Something unexpected but handled | `logger.warning("Empty response, returning None (LENIENT mode)")` |
| **ERROR** | Error occurred, operation failed | `logger.error(f"Failed to connect to {url}: {e}")` |
| **CRITICAL** | Serious error, program may crash | `logger.critical("Invalid configuration")` |

### 3. What to Log in Each Layer

#### HttpClient (core/client.py)

```python
class HttpClient:
    def __init__(self, base_url, token, timeout):
        logger.info(f"Initializing HttpClient: {base_url}")
        logger.debug(f"Timeout: {timeout}s, SSL verify: {self._verify_ssl}")
    
    def get(self, endpoint: str, **kwargs):
        logger.debug(f"GET {self._base_url}{endpoint}")
        logger.debug(f"Params: {kwargs.get('params', {})}")
        
        try:
            response = self._client.get(...)
            logger.debug(f"Response: {response.status_code} ({len(response.content)} bytes)")
            return Response(...)
        except httpx.TimeoutError as e:
            logger.error(f"Timeout on GET {endpoint}: {e}")
            raise TimeoutError(...)
        except httpx.ConnectError as e:
            logger.error(f"Connection failed to {endpoint}: {e}")
            raise ConnectionError(...)
```

#### Repository Layer

```python
class ProductRepository:
    def get_by_part_number(self, part_number: str):
        logger.debug(f"Fetching product: {part_number}")
        
        response = self._http_client.get(f"/api/Product/{part_number}")
        data = self._error_handler.handle_response(response, ...)
        
        if data is None:
            logger.warning(f"Product not found: {part_number}")
            return None
        
        product = Product.model_validate(data)
        logger.info(f"Retrieved product: {part_number} ({product.name})")
        return product
```

#### Service Layer

```python
class ProductService:
    def get_product(self, part_number: str):
        logger.debug(f"Service.get_product: {part_number}")
        product = self._repository.get_by_part_number(part_number)
        
        if product and self.is_active(product):
            logger.info(f"Active product found: {part_number}")
        elif product:
            logger.warning(f"Inactive product: {part_number} (state: {product.state})")
        
        return product
```

### 4. Error Logging

**In ErrorHandler (core/exceptions.py):**

```python
class ErrorHandler:
    def handle_response(self, response: Response, operation: str):
        if response.is_success:
            if not response.data:
                msg = f"Empty response for {operation}"
                logger.warning(msg)
                if self._mode == ErrorMode.STRICT:
                    logger.error("Raising EmptyResponseError (STRICT mode)")
                    raise EmptyResponseError(msg, operation)
                return None
            return response.data
        
        if response.is_not_found:
            msg = f"Resource not found: {operation}"
            logger.warning(msg)
            if self._mode == ErrorMode.STRICT:
                logger.error("Raising NotFoundError (STRICT mode)")
                raise NotFoundError(msg, operation)
            return None
        
        # Actual errors always log and raise
        logger.error(
            f"HTTP {response.status_code} error: {operation}",
            extra={
                "status_code": response.status_code,
                "error_message": response.error_message
            }
        )
        raise self._create_exception(response, operation)
```

---

## 🛠️ Implementation: Add to Core API

### Step 1: Create logging utilities

```python
# src/pywats/core/logging.py (NEW FILE)
"""
Logging utilities for pyWATS.

The library uses Python's standard logging module but never configures
handlers or output. This allows applications to control logging behavior.
"""
import logging
from typing import Optional


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for the given name.
    
    All pyWATS loggers are children of 'pywats' root logger,
    allowing users to control library logging with:
    
        logging.getLogger('pywats').setLevel(logging.WARNING)
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


def enable_debug_logging():
    """
    Convenience function to enable debug logging for pyWATS.
    
    This is a helper for quick debugging but applications should
    configure logging properly for production use.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger('pywats').setLevel(logging.DEBUG)


# Suppress warnings about unconfigured logging
# This prevents "No handlers found" warnings
logging.getLogger('pywats').addHandler(logging.NullHandler())
```

### Step 2: Update __init__.py

```python
# src/pywats/__init__.py
from .core.logging import enable_debug_logging

__all__ = [
    # ... existing exports ...
    "enable_debug_logging",  # Convenience for debugging
]
```

---

## 📱 Client Application Examples

### Example 1: Simple Console Output

```python
# User's script or client app
import logging
from pywats import pyWATS

# Enable INFO level for pyWATS
logging.basicConfig(level=logging.INFO)

api = pyWATS(base_url="...", token="...")
products = api.product.get_products()
# Will see: INFO - Retrieved 42 products
```

### Example 2: Debug Mode

```python
from pywats import pyWATS, enable_debug_logging

# Quick debug helper
enable_debug_logging()

api = pyWATS(base_url="...", token="...")
# Will see detailed debug output
```

### Example 3: Production Logging

```python
import logging.config
from pywats import pyWATS

# Professional logging configuration
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'pywats': {
            'level': 'INFO',
            'handlers': ['file', 'console'],
            'propagate': False,
        },
    },
})

api = pyWATS(...)
```

### Example 4: Rich Console Output (Client Feature)

```python
# pywats_client/services/logging_service.py
from rich.console import Console
from rich.logging import RichHandler
import logging

console = Console()

def setup_rich_logging():
    """Setup rich console output for the client."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(console=console, rich_tracebacks=True)]
    )

# In your GUI or CLI:
setup_rich_logging()
console.print("[bold green]pyWATS Client Started[/bold green]")
```

---

## ⚙️ Configuration Options in pyWATS Class

You could add optional verbose mode to the facade:

```python
# src/pywats/pywats.py
class pyWATS:
    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: int = 30,
        error_mode: ErrorMode = ErrorMode.STRICT,
        verbose: bool = False  # NEW
    ):
        """
        Initialize pyWATS API.
        
        Args:
            ...
            verbose: Enable INFO level logging for pyWATS (default: False)
                    Note: This is a convenience flag. For production use,
                    configure logging properly using Python's logging module.
        """
        if verbose:
            # Simple convenience - not recommended for production
            import logging
            logging.basicConfig(level=logging.INFO)
            logging.getLogger('pywats').setLevel(logging.INFO)
        
        # ... rest of init
```

**But this is optional - many libraries don't provide this.**

---

## 🎨 Client-Specific Features

### GUI Progress Indicators

```python
# pywats_client/services/report_service.py
class ClientReportService:
    def __init__(self, api: pyWATS, progress_callback=None):
        self._api = api
        self._progress = progress_callback or (lambda msg: None)
    
    def upload_batch_reports(self, reports: list):
        self._progress("Starting upload...")
        
        for i, report in enumerate(reports):
            logger.info(f"Uploading report {i+1}/{len(reports)}")
            self._progress(f"Uploading {i+1}/{len(reports)}")
            
            self._api.report.send_uut_report(report)
        
        self._progress("Upload complete!")
```

### CLI Output with Click

```python
# pywats_client/cli/commands.py
import click
from pywats import pyWATS

@click.command()
@click.option('--verbose', is_flag=True)
def list_products(verbose):
    """List all products."""
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    api = pyWATS(...)
    products = api.product.get_products()
    
    for p in products:
        click.echo(f"{p.part_number}: {p.name}")
```

---

## 📊 Comparison: Core vs Client

| Feature | Core API (PyWATS) | Client App |
|---------|-------------------|------------|
| **Console Output** | None (only logging) | Yes, formatted |
| **Progress Bars** | No | Yes (rich, tqdm, etc.) |
| **Logging Config** | Never | Always |
| **Colored Output** | No | Yes (rich, colorama) |
| **User Prompts** | Never | Yes |
| **Notifications** | No | Yes (toast, sound, etc.) |
| **GUI Updates** | No | Yes (PyQt signals, etc.) |

---

## 🎯 Best Practices Summary

### For Core API (PyWATS Library)

1. ✅ Use `logging.getLogger(__name__)` in every module
2. ✅ Log at appropriate levels (DEBUG for details, INFO for operations, ERROR for failures)
3. ✅ Add NullHandler to prevent "No handlers" warnings
4. ✅ Include context in log messages (IDs, names, counts)
5. ✅ Use `exc_info=True` when logging exceptions
6. ❌ NEVER use `print()`
7. ❌ NEVER configure logging handlers
8. ❌ NEVER write to stdout/stderr directly

### For Client Applications

1. ✅ Configure logging at application startup
2. ✅ Use appropriate handlers (file, console, rotating, etc.)
3. ✅ Add console output for user interaction
4. ✅ Use rich libraries for better UX (rich, tqdm, click)
5. ✅ Separate logging (diagnostics) from user output (feedback)

---

## 🚀 Migration Path

### Phase 1: Add Logging Infrastructure (1-2 hours)

1. Create `src/pywats/core/logging.py`
2. Add `get_logger()` and `enable_debug_logging()`
3. Update `src/pywats/__init__.py` exports

### Phase 2: Add Loggers to Core (2-3 hours)

1. Add `logger = logging.getLogger(__name__)` to each module
2. Start with HttpClient (most impactful)
3. Add to ErrorHandler
4. Add to Repositories
5. Add to Services (optional - less useful)

### Phase 3: Client Updates (1-2 hours)

1. Update `pywats_client` to configure logging
2. Add console output for user feedback
3. Separate logging from user messages

---

## 💡 Recommendation

**Start with Phase 1 and 2** - add logging to the core API. This provides value immediately:
- Users can debug issues by enabling logging
- You can troubleshoot problems more easily
- Professional libraries should have good logging

**Phase 3 is client-specific** - each application (GUI, CLI, scripts) can decide its own output strategy.

Would you like me to implement Phase 1 (logging infrastructure) now?
