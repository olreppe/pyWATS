# Implementation Plan: Sphinx Logging Documentation

---

## Phase 1: Setup & Preparation (30 min)

### Tasks

1. **Review `.docs_instructions.md`** (10 min)
   - Read and internalize type safety rules
   - Understand validation requirements
   - Note template patterns

2. **Inspect existing Sphinx structure** (10 min)
   - Check `docs/api/index.rst` format
   - Review existing domain docs (e.g., `report.rst`)
   - Identify RST patterns to follow

3. **Verify source code docstrings** (10 min)
   - Read `src/pywats/core/logging.py`
   - Read `src/pywats_client/core/logging.py`
   - Read `src/pywats_client/converters/conversion_log.py`
   - Note function signatures

**Deliverables:**
- Understanding of patterns to follow
- List of functions/classes to document

---

## Phase 2: API Documentation (2-3 hours)

### Task 1: Create `docs/api/logging.rst`

**Structure:**
```rst
Logging API
===========

Core logging utilities for pyWATS.

.. seealso::
   
   For client logging setup, see :doc:`../client/logging`.
   For best practices, see :doc:`../guides/logging`.

Module Overview
---------------

The :mod:`pywats.core.logging` module provides...

Functions
---------

.. autofunction:: pywats.core.logging.configure_logging

.. autofunction:: pywats.core.logging.enable_debug_logging

Classes
-------

.. autoclass:: pywats.core.logging.FileRotatingHandler
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.core.logging.LoggingContext
   :members:
   :undoc-members:

Examples
--------

Basic Configuration
~~~~~~~~~~~~~~~~~~~

[Type-safe example]

JSON Logging
~~~~~~~~~~~~

[Type-safe example]

Context Management
~~~~~~~~~~~~~~~~~~

[Type-safe example]
```

**Validation Steps:**
1. Extract examples to temp file
2. Add imports and run through mypy
3. Verify function signatures match source
4. Test that imports work

### Task 2: Update `docs/api/index.rst`

Add logging to TOC:
```rst
.. toctree::
   :maxdepth: 2
   
   logging
   analytics
   asset
   ...
```

**Deliverables:**
- `docs/api/logging.rst` (~150-200 lines)
- Updated `docs/api/index.rst`

---

## Phase 3: Client Documentation Structure (1 hour)

### Task 1: Create `docs/client/` directory

```bash
mkdir docs/client
```

### Task 2: Create `docs/client/index.rst`

```rst
pyWATS Client Documentation
===========================

Documentation for pyWATS client components.

.. toctree::
   :maxdepth: 2
   :caption: Client Components
   
   logging

Overview
--------

The pyWATS client provides...

Components
----------

- **Logging**: Client-side logging setup and conversion tracking
- **Service**: Background service for file monitoring
- **Converters**: File format conversion framework
```

### Task 3: Create `docs/client/conf.py` (if needed)

May inherit from main conf.py or need separate config.

**Deliverables:**
- `docs/client/` directory
- `docs/client/index.rst`

---

## Phase 4: Client Logging Documentation (2-3 hours)

### Task 1: Create `docs/client/logging.rst`

**Structure:**
```rst
Client Logging
==============

Client-side logging setup and conversion tracking.

.. seealso::
   
   For core logging API, see :doc:`../api/logging`.
   For best practices, see :doc:`../guides/logging`.

Overview
--------

The client logging infrastructure provides:

- Top-level ``pywats.log`` in installation directory
- Per-conversion detailed logging
- Automatic log rotation
- JSON line format for audit trails

Client Logging Setup
--------------------

.. automodule:: pywats_client.core.logging
   :members:
   :undoc-members:

Functions
~~~~~~~~~

.. autofunction:: pywats_client.core.logging.setup_client_logging

.. autofunction:: pywats_client.core.logging.get_client_log_path

.. autofunction:: pywats_client.core.logging.get_conversion_log_dir

.. autofunction:: pywats_client.core.logging.cleanup_old_conversion_logs

Conversion Logging
------------------

.. automodule:: pywats_client.converters.conversion_log
   :members:
   :undoc-members:

Classes
~~~~~~~

.. autoclass:: pywats_client.converters.conversion_log.ConversionLog
   :members:
   :show-inheritance:

.. autoclass:: pywats_client.converters.conversion_log.ConversionLogEntry
   :members:
   :show-inheritance:

Examples
--------

Setup Client Logging
~~~~~~~~~~~~~~~~~~~~

[Type-safe example - headless service]

Setup with JSON Format
~~~~~~~~~~~~~~~~~~~~~~

[Type-safe example - structured logging]

Using ConversionLog
~~~~~~~~~~~~~~~~~~~

[Type-safe example - converter integration]

Full Converter Example
~~~~~~~~~~~~~~~~~~~~~~

[Type-safe example - complete workflow]
```

**Type-Safe Examples Required:**

1. **Setup Client Logging:**
```python
from pywats_client.core.logging import setup_client_logging
from pathlib import Path

log_path: Path = setup_client_logging(
    instance_id="production_station",
    log_level="INFO",
    log_format="text",
    enable_console=False
)
```

2. **ConversionLog Usage:**
```python
from pywats_client.converters.conversion_log import ConversionLog
from typing import Optional

log: ConversionLog = ConversionLog.create_for_file(
    "test_data.csv",
    instance_id="station_a"
)

log.step("Reading file", metadata={"size_bytes": 1024})
log.step("Parsing CSV", metadata={"rows": 10})
log.warning("Missing optional field: temperature")
log.finalize(success=True, report_id=456)
```

3. **Converter Integration:**
```python
from pathlib import Path
from typing import Optional
from pywats_client.converters.base import (
    ConverterBase,
    ConverterArguments,
    ConverterResult,
)
from pywats_client.converters.conversion_log import ConversionLog

class MyConverter(ConverterBase):
    def convert_file(
        self,
        file_path: Path,
        args: ConverterArguments
    ) -> ConverterResult:
        log: Optional[ConversionLog] = args.conversion_log
        
        if log:
            log.step("Reading file")
        
        # Conversion logic...
        
        return ConverterResult.success_result(report={...})
```

**Validation Steps:**
1. Extract ALL examples to files
2. Type check each with mypy --strict
3. Verify all imports resolve
4. Check ConversionLog methods exist
5. Verify ConverterArguments has conversion_log field

**Deliverables:**
- `docs/client/logging.rst` (~250-300 lines)
- All examples validated

---

## Phase 5: Integration & Cross-Linking (30 min)

### Task 1: Update Main Documentation Index

Check if `docs/index.rst` exists and add client section:

```rst
.. toctree::
   :maxdepth: 2
   :caption: Documentation
   
   api/index
   client/index
   guides/index
```

### Task 2: Add Cross-References

**In `docs/api/logging.rst`:**
```rst
.. seealso::
   
   :doc:`../client/logging`
      Client-side logging setup and ConversionLog
   
   :doc:`../guides/logging`
      Best practices and troubleshooting
```

**In `docs/client/logging.rst`:**
```rst
.. seealso::
   
   :doc:`../api/logging`
      Core logging API (configure_logging, etc.)
   
   :doc:`../guides/logging`
      Best practices and troubleshooting
```

**In `docs/guides/logging.md`:**
```markdown
## Reference

- [API Reference](../api/logging.rst) - Core logging functions
- [Client Reference](../client/logging.rst) - Client setup and ConversionLog
```

**Deliverables:**
- All cross-links added
- Bidirectional references work

---

## Phase 6: Build & Validation (1-2 hours)

### Task 1: Build Sphinx Docs

```bash
cd docs
python run_sphinx_build.py
# or
make html
```

**Check for:**
- ❌ Warnings
- ❌ Errors
- ❌ Broken links

### Task 2: Type Check Examples

```bash
# Extract code blocks
python scripts/extract_rst_code.py docs/api/logging.rst > /tmp/api_examples.py
python scripts/extract_rst_code.py docs/client/logging.rst > /tmp/client_examples.py

# Type check
mypy /tmp/api_examples.py --strict
mypy /tmp/client_examples.py --strict
```

**Target:** 0 errors

### Task 3: Verify Function Signatures

```bash
# Verify each example matches source
grep -A 10 "def configure_logging" src/pywats/core/logging.py
grep -A 10 "def setup_client_logging" src/pywats_client/core/logging.py
grep -A 10 "class ConversionLog" src/pywats_client/converters/conversion_log.py
```

### Task 4: Manual HTML Review

1. Open `docs/_build/html/api/logging.html`
2. Check formatting looks good
3. Click all cross-reference links
4. Verify examples render correctly

### Task 5: Final Checklist

- [ ] Sphinx build: 0 warnings
- [ ] Type checking: 0 errors  
- [ ] All links work
- [ ] HTML renders correctly
- [ ] All function signatures verified
- [ ] All imports tested
- [ ] Examples follow `.docs_instructions.md`
- [ ] No `dict`, `Any`, or untyped returns
- [ ] Enums used where appropriate
- [ ] All code validated

**Deliverables:**
- Clean Sphinx build
- Validated examples
- Working HTML output

---

## Phase 7: Documentation (1 hour)

### Task 1: Add Endpoint Risk Documentation

**Create Sphinx reference to `docs/INTERNAL_ENDPOINT_RISK.md`:**

In `docs/api/logging.rst` and `docs/client/logging.rst`, add warning box:

```rst
.. warning::
   
   **Internal Endpoint Dependency**
   
   This version connects to an internal endpoint that may change.
   See :doc:`../INTERNAL_ENDPOINT_RISK` for details and mitigation.
```

### Task 2: Update Project Status

Update `README.md` to mark complete.

### Task 3: Update CHANGELOG

Add entry in `CHANGELOG.md` following `.deployment_instructions.md`:

```markdown
### Improved
- **Sphinx Documentation**: Complete API and client reference for logging infrastructure
  - **API Reference** (docs/api/logging.rst): Core logging functions and classes
  - **Client Reference** (docs/client/logging.rst): Client setup and ConversionLog
  - **Endpoint Risk**: Documented internal dependency risk in docs/INTERNAL_ENDPOINT_RISK.md
  - All code examples type-safe and validated (verified with mypy --strict)
  - Cross-linked with conceptual guide
  - **Tests Coverage**: All examples validated against source signatures
```

**Deliverables:**
- Endpoint risk cross-references in docs
- Updated project docs
- CHANGELOG entry following deployment standards

---

## Timeline

**Day 1 (4-5 hours):**
- Phase 1: Setup (30 min)
- Phase 2: API docs (2-3 hours)
- Phase 3: Client structure (1 hour)

**Day 2 (4-5 hours):**
- Phase 4: Client logging docs (2-3 hours)
- Phase 5: Integration (30 min)
- Phase 6: Build & validation (1-2 hours)
- Phase 7: Documentation (30 min)

**Total:** 8-10 hours (1-1.5 days)

---

## Critical Success Factors

1. **Type Safety:** Follow `.docs_instructions.md` religiously
2. **Validation:** Every example must be type-checked
3. **Verification:** Compare all signatures against source
4. **Cross-Links:** Ensure all references work
5. **Quality:** Zero Sphinx warnings
