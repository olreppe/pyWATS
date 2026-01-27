# Migration Guide

This document contains detailed migration instructions for breaking changes in PyWATS.
For a summary of all changes, see [CHANGELOG.md](CHANGELOG.md).

## Table of Contents

- [v0.1.0b40 - File I/O Separation](#v010b40---file-io-separation)
- [v0.1.0b40 - Deprecated UUR Classes Removed](#v010b40---deprecated-uur-classes-removed)
- [v0.1.0b38 - CompOp Import Location](#v010b38---compop-import-location)
- [v0.1.0b38 - Converter Models Import](#v010b38---converter-models-import)
- [v0.1.0b38 - Configuration Moved to Client](#v010b38---configuration-moved-to-client)
- [v0.1.0b34 - Report Query API](#v010b34---report-query-api)
- [v0.1.0b32 - Unified API Pattern](#v010b32---unified-api-pattern)

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

### SimpleQueue → ClientService

```python
# Before
from pywats.queue import SimpleQueue
queue = SimpleQueue(data_path="./queue")
queue.add(report)

# After
# Use pywats_client.ClientService for file-based queuing
from pywats_client import ClientService
service = ClientService(config)
service.queue.add(report)
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
