# Migration Guide

This document contains detailed migration instructions for breaking changes in PyWATS.
For a summary of all changes, see [CHANGELOG.md](CHANGELOG.md).

## Table of Contents

- [v0.5.1 - Exception Module Consolidation](#v051---exception-module-consolidation)
- [v0.1.0b40 - Async-First Client Architecture](#v010b40---async-first-client-architecture)
- [v0.1.0b40 - File I/O Separation](#v010b40---file-io-separation)
- [v0.1.0b40 - Deprecated UUR Classes Removed](#v010b40---deprecated-uur-classes-removed)
- [v0.1.0b38 - CompOp Import Location](#v010b38---compop-import-location)
- [v0.1.0b38 - Converter Models Import](#v010b38---converter-models-import)
- [v0.1.0b38 - Configuration Moved to Client](#v010b38---configuration-moved-to-client)
- [v0.1.0b34 - Report Query API](#v010b34---report-query-api)
- [v0.1.0b32 - Unified API Pattern](#v010b32---unified-api-pattern)

---

## v0.5.1 - Exception Module Consolidation

**⚠️ Deprecation Notice:** The `pywats.exceptions` module is deprecated and will be removed in v0.6.0.

All exception classes have been moved to `pywats.core.exceptions` with enhanced functionality.

### What Changed

- **Old location** (deprecated): `from pywats.exceptions import`
- **New location** (recommended): `from pywats.core.exceptions import`

The old module still works in v0.5.1 through v0.5.x (shows deprecation warning), but will be completely removed in v0.6.0.

### Migration Steps

**Step 1: Update Import Statements**

```python
# Before (deprecated - still works but shows warning):
from pywats.exceptions import (
    PyWATSError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
)

# After (recommended):
from pywats.core.exceptions import (
    PyWATSError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
)
```

**Step 2: Update Exception Handling** (No changes needed)

Your exception handling code works exactly the same:

```python
# This code works unchanged
try:
    product = api.product.get("PN-001")
except NotFoundError as e:
    print(f"Product not found: {e}")
except PyWATSError as e:
    print(f"API error: {e}")
```

**Step 3: Use New Exception Features** (Optional)

The new exception module provides enhanced features:

```python
from pywats.core.exceptions import ErrorMode

# ErrorMode.STRICT (default) - raises on empty/ambiguous responses
api = pyWATS(error_mode=ErrorMode.STRICT)

# ErrorMode.LENIENT - returns None for 404 and empty responses
api = pyWATS(error_mode=ErrorMode.LENIENT)
```

### Automated Migration

Update all import statements in your codebase:

```bash
# Find all files using old import
find . -name "*.py" -exec grep -l "from pywats.exceptions import" {} \;

# Update with sed (Linux/macOS)
find . -name "*.py" -exec sed -i 's/from pywats\.exceptions import/from pywats.core.exceptions import/g' {} \;

# Update with PowerShell (Windows)
Get-ChildItem -Recurse -Filter *.py | ForEach-Object {
    (Get-Content $_.FullName) -replace 'from pywats\.exceptions import', 'from pywats.core.exceptions import' | Set-Content $_.FullName
}
```

### Why This Change?

1. **Better organization**: Exceptions now in `pywats.core` alongside other core utilities
2. **Enhanced features**: New `ErrorMode` for flexible error handling
3. **Cleaner codebase**: Eliminates duplicate exception definitions
4. **Consistency**: All core modules now under `pywats.core`

### Timeline

- **v0.5.1**: Deprecation warning added, old module still works
- **v0.5.2 - v0.5.x**: Migration period (both modules work)
- **v0.6.0**: Old module completely removed (imports will fail)

---

## v0.1.0b40 - Async-First Client Architecture

The client service now uses an **async-first architecture** for better performance and concurrency.

### ClientService → AsyncClientService

```python
# Before
from pywats_client.service import ClientService
service = ClientService(instance_id="default")
service.start()  # Blocking call

# After
from pywats_client.service import AsyncClientService
import asyncio

service = AsyncClientService()
asyncio.run(service.run())  # Async entry point
```

### PendingWatcher → AsyncPendingQueue

The pending queue now supports concurrent uploads (5 simultaneous by default).

```python
# Before: Sequential uploads with locks
# PendingWatcher processed one report at a time

# After: Concurrent uploads with semaphore
from pywats_client.service import AsyncPendingQueue

queue = AsyncPendingQueue(
    api=async_wats,
    reports_dir=reports_path,
    max_concurrent=5  # 5 concurrent uploads
)
await queue.run()
```

### ConverterPool → AsyncConverterPool

The converter pool now supports concurrent conversions (10 simultaneous by default).

```python
# Before: ThreadPoolExecutor with fixed workers
# ConverterPool used threads for each conversion

# After: asyncio.Semaphore for bounded concurrency
from pywats_client.service import AsyncConverterPool

pool = AsyncConverterPool(
    config=client_config,
    api=async_wats,
    max_concurrent=10  # 10 concurrent conversions
)
await pool.run()
```

### GUI Pages: AsyncAPIRunner (Composition)

GUI pages now use `AsyncAPIRunner` for non-blocking API calls via dependency injection.

```python
# Before: Blocking API calls froze the UI
def _fetch_data(self, query: str):
    result = self.api.some_domain.query(query)
    self._display_result(result)

# After: Non-blocking calls with callbacks using composition
class MyPage(BasePage):
    def __init__(self, config, main_window=None, parent=None):
        super().__init__(config, parent, async_api_runner=getattr(main_window, 'async_api_runner', None))
    
    def _fetch_data(self, query: str):
        if self.async_api:
            self.async_api.run(
                self,
                api_call=lambda api: api.some_domain.query(query),
                on_success=self._on_success,
                on_error=self._on_error
            )
```

> **Note:** Example domain pages are available in `pywats_client.gui.pages.unused/` for reference.

### New Dependencies

The async architecture requires new dependencies:

```bash
# In requirements.txt / pyproject.toml:
aiofiles>=23.0.0  # Async file I/O
qasync>=0.27.0    # Qt + asyncio integration (for GUI)
```

---

## v0.1.0b40 - File I/O Separation

The `pywats` API layer is now **memory-only**. All file operations moved to `pywats_client`.

### Attachment.from_file() → AttachmentIO.from_file()

```python
# Before
from pywats.domains.report import Attachment
attachment = Attachment.from_file("screenshot.png")

# After
from pywats_client.io import AttachmentIO
attachment = AttachmentIO.from_file("screenshot.png")
```

### Step.attach_file() → AttachmentIO + add_attachment()

```python
# Before
step.attach_file("data.bin")

# After
from pywats_client.io import AttachmentIO
attachment = AttachmentIO.from_file("data.bin")
step.add_attachment(attachment)
```

### UURReport.attach_file() → attach_bytes()

```python
# Before
report.attach_file("path/to/file.pdf")

# After
from pywats_client.io import AttachmentIO
attachment = AttachmentIO.from_file("path/to/file.pdf")
report.attach_bytes(attachment.content, attachment.filename, attachment.mime_type)
```

### SimpleQueue → AsyncClientService

```python
# Before
from pywats.queue import SimpleQueue
queue = SimpleQueue(data_path="./queue")
queue.add(report)

# After (v1.4+)
# Use AsyncClientService for async file-based queuing
from pywats_client.service import AsyncClientService
import asyncio

async def main():
    service = AsyncClientService()
    await service.run()  # Service handles queue automatically

asyncio.run(main())

# Or for sync usage, the queue directory is still available:
# Reports placed in {queue_dir}/pending/*.json are auto-uploaded
```

---

## v0.1.0b40 - Deprecated UUR Classes Removed

All deprecated UUR legacy classes have been removed entirely.

### UURAttachment → Attachment

```python
# Before
from pywats.domains.report.report_models.uur import UURAttachment
attachment = UURAttachment(...)

# After
from pywats.domains.report import Attachment
attachment = Attachment.from_bytes(content, "file.pdf", "application/pdf")
```

### Failure → UURFailure

```python
# Before
from pywats.domains.report.report_models.uur import Failure
failure = Failure(...)

# After
from pywats.domains.report.report_models import UURFailure
# UURFailure is accessed via UURSubUnit.failures
```

### UURPartInfo → UURSubUnit

```python
# Before
from pywats.domains.report.report_models.uur import UURPartInfo

# After
from pywats.domains.report.report_models import UURSubUnit
# UURSubUnit provides the same functionality with clearer naming
```

### FailCode/FailCodes → ProcessService

```python
# Before
from pywats.domains.report.report_models.uur import FailCode, FailCodes

# After
# Use ProcessService.get_fail_codes() for fail code lookups
fail_codes = api.process.get_fail_codes()
```

### MiscUURInfo → Report.misc_infos

```python
# Before
from pywats.domains.report.report_models.uur import MiscUURInfo

# After
# Access misc info through Report.misc_infos property
```

---

## v0.1.0b38 - CompOp Import Location

```python
# Before
from pywats.domains.report.report_models.uut.steps.comp_operator import CompOp

# After (preferred)
from pywats import CompOp

# Or
from pywats.shared.enums import CompOp
```

---

## v0.1.0b38 - Converter Models Import

```python
# Before (scattered imports)
from pywats_client.converters.base import ConversionStatus, PostProcessAction

# After (canonical location)
from pywats_client.converters.models import ConversionStatus, PostProcessAction, FileInfo, ConverterResult
```

---

## v0.1.0b38 - Configuration Moved to Client

File-based configuration moved from `pywats` to `pywats_client`.

```python
# Before
from pywats.core.config import APIConfigManager, get_api_config_manager

# After
from pywats_client.core import ConfigManager
from pywats.core.config import get_default_settings  # For pure API defaults

# Pure API usage (no file I/O)
from pywats import pyWATS
from pywats.core.config import get_default_settings
settings = get_default_settings()
api = pyWATS(base_url="...", token="...", settings=settings)

# With client file config
from pywats_client.core import ConfigManager
settings = ConfigManager().load()
api = pyWATS(base_url="...", token="...", settings=settings)
```

---

## v0.1.0b34 - Report Query API

Report queries now use OData filter syntax instead of WATSFilter.

```python
# Before (WATSFilter - no longer works for report queries)
from pywats.domains.report import WATSFilter
filter_data = WATSFilter(serialNumber="W12345")
headers = api.report.query_uut_headers(filter_data)

# After (OData filter)
headers = api.report.query_uut_headers(odata_filter="serialNumber eq 'W12345'")

# Or using helper method
headers = api.report.get_headers_by_serial("W12345")

# More OData examples
headers = api.report.query_uut_headers(odata_filter="partNumber eq 'WIDGET-001'")
headers = api.report.query_uut_headers(odata_filter="result eq 'Failed'")
headers = api.report.query_uut_headers(odata_filter="partNumber eq 'WIDGET-001' and result eq 'Failed'")
```

**Note**: WATSFilter is still used for Analytics API endpoints.

---

## v0.1.0b32 - Unified API Pattern

Removed separate `api.*_internal` accessors. All methods now on main domain accessor.

```python
# Before
api.product_internal.get_box_build()
api.asset_internal.upload_file()
api.analytics_internal.get_unit_flow()
api.production_internal.get_unit_phases()
api.process_internal.get_fail_codes()

# After
api.product.get_box_build_template()
api.asset.upload_blob()
api.analytics.get_unit_flow()
api.production.get_all_unit_phases()
api.process.get_fail_codes()
```

Internal methods are marked with `⚠️ INTERNAL API` warnings in docstrings.
