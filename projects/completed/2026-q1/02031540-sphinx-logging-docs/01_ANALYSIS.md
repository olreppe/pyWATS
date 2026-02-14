# Analysis: Sphinx Logging Documentation

---

## Current State

### Existing Documentation

✅ **Conceptual Guide** - `docs/guides/logging.md` (700+ lines)
- Best practices
- Examples and patterns
- Troubleshooting
- Performance considerations
- Migration guide

✅ **Working Example** - `examples/converters/logging_example_converter.py` (290 lines)
- Full converter with ConversionLog
- Demonstrates all methods
- Runnable test code

❌ **API Reference** - Missing
- No `docs/api/logging.rst`
- Core logging not in Sphinx docs

❌ **Client Reference** - Missing
- No `docs/client/` directory
- Client logging not documented in Sphinx

### Source Code Structure

**Core Logging** (`src/pywats/core/logging.py`):
- `configure_logging()` - Main configuration function
- `FileRotatingHandler` - File handler with rotation
- `LoggingContext` - Context manager for scoped metadata
- `StructuredFormatter` - JSON formatter (existing)
- `CorrelationFilter` - Correlation ID filter (existing)

**Client Logging** (`src/pywats_client/core/logging.py`):
- `setup_client_logging()` - Client-specific setup
- `get_client_log_path()` - Path to pywats.log
- `get_conversion_log_dir()` - Conversion logs directory
- `cleanup_old_conversion_logs()` - Cleanup utility

**Conversion Logging** (`src/pywats_client/converters/conversion_log.py`):
- `ConversionLog` - Main logging class
- `ConversionLogEntry` - Log entry dataclass
- Methods: `step()`, `warning()`, `error()`, `finalize()`

### Docstring Quality

**Core Logging:**
```python
def configure_logging(
    level: str = "INFO",
    format: Literal["text", "json"] = "text",
    file_path: Optional[Path] = None,
    # ... parameters
) -> None:
    """
    Configure unified logging for pyWATS.
    
    [Has comprehensive docstring]
    """
```
✅ Good docstrings - ready for Sphinx

**Client Logging:**
```python
def setup_client_logging(
    instance_id: str = "default",
    log_level: str = "INFO",
    # ... parameters
) -> Path:
    """
    Configure unified logging for pyWATS client.
    
    [Has comprehensive docstring with examples]
    """
```
✅ Good docstrings - ready for Sphinx

**ConversionLog:**
```python
class ConversionLog:
    """
    Per-conversion detailed logging.
    
    [Has comprehensive class docstring with usage examples]
    """
```
✅ Good docstrings - ready for Sphinx

---

## Type Safety Assessment

### Current Issues

**❌ Example in logging.md guide:**
```python
# From docs/guides/logging.md line ~120
from pywats.core.logging import configure_logging
import logging

configure_logging(level="INFO", format="json")
logger = logging.getLogger(__name__)
logger.info("Application started", extra={"version": "1.0.0"})
```

**Problem:** No type hints, logger not typed

**✅ Should be:**
```python
from pywats.core.logging import configure_logging
import logging
from logging import Logger

configure_logging(level="INFO", format="json")
logger: Logger = logging.getLogger(__name__)
logger.info("Application started", extra={"version": "1.0.0"})
```

**❌ Example in logging_example_converter.py:**
```python
# Line ~285
args = ConverterArguments(
    api_client=Mock(),  # ← Mock returns Any
    file_info=Mock(name=test_file.name, extension=".csv", size=len(test_content)),
    # ...
)
```

**Problem:** Mock() returns Any, fields not properly typed

**✅ Should be:**
```python
from unittest.mock import Mock, MagicMock
from pywats_client.converters.models import FileInfo

# Create typed mock
api_mock = MagicMock(spec=WATS)

file_info = FileInfo(
    name=test_file.name,
    extension=".csv",
    size=len(test_content),
    # ... other required fields
)

args = ConverterArguments(
    api_client=api_mock,
    file_info=file_info,
    # ...
)
```

---

## Sphinx Structure Analysis

### Current Sphinx Setup

**`docs/api/` exists:**
```
docs/api/
├── conf.py
├── index.rst
├── analytics.rst
├── asset.rst
├── process.rst
├── product.rst
├── production.rst
├── report.rst
├── rootcause.rst
├── scim.rst
└── software.rst
```

**Missing:**
- `logging.rst` (API reference)

**`docs/client/` does NOT exist:**
- Need to create entire structure

### Required Changes

1. **Create `docs/api/logging.rst`**
   - Document pywats.core.logging module
   - Include all public functions/classes

2. **Create `docs/client/` directory**
   - New section for client documentation
   - Separate from API docs

3. **Create `docs/client/index.rst`**
   - TOC for client docs
   - Initially just logging

4. **Create `docs/client/logging.rst`**
   - Document pywats_client.core.logging
   - Document ConversionLog

5. **Update `docs/api/index.rst`**
   - Add logging to TOC

6. **Update main `docs/index.rst`** (if exists)
   - Add client section

---

## Cross-Reference Requirements

### API → Client
```rst
# In docs/api/logging.rst
For client-side logging setup, see :doc:`../client/logging`.
```

### Client → API
```rst
# In docs/client/logging.rst
This uses the core logging API. See :doc:`../api/logging` for API details.
```

### Both → Guide
```rst
For best practices and examples, see :doc:`../guides/logging`.
```

### Guide → Both
```markdown
# In docs/guides/logging.md
- [API Reference](../api/logging.rst)
- [Client Reference](../client/logging.rst)
```

---

## Type Safety Validation Plan

### Step 1: Extract Examples
```bash
# Extract code from RST files
python scripts/extract_rst_code.py docs/api/logging.rst > api_examples.py
python scripts/extract_rst_code.py docs/client/logging.rst > client_examples.py
```

### Step 2: Type Check
```bash
mypy api_examples.py --strict
mypy client_examples.py --strict
```

### Step 3: Verify Imports
```python
# Check all imports resolve
python -c "from pywats.core.logging import configure_logging"
python -c "from pywats_client.core.logging import setup_client_logging"
```

### Step 4: Verify Function Signatures
```bash
# Compare examples against source
grep -A 20 "def configure_logging" src/pywats/core/logging.py
grep -A 20 "def setup_client_logging" src/pywats_client/core/logging.py
```

---

## Risks & Mitigations

### Risk 1: Type-Unsafe Examples
**Mitigation:** 
- Follow `.docs_instructions.md` strictly
- Validate all examples before committing
- Use mypy on extracted code

### Risk 2: Outdated Function Signatures
**Mitigation:**
- Verify against source code before writing
- Use `:autofunction:` directive for auto-sync
- Regular validation checks

### Risk 3: Broken Cross-Links
**Mitigation:**
- Test all `:doc:`, `:class:`, `:func:` references
- Run Sphinx build with warnings as errors
- Check HTML output manually

### Risk 4: Inconsistent Patterns
**Mitigation:**
- Use template from `.docs_instructions.md`
- Review existing domain API docs for style
- Maintain consistency across all examples

---

## Dependencies

**Required:**
- Source code with good docstrings ✅
- Sphinx configuration ✅
- `.docs_instructions.md` ✅
- Conceptual guide ✅

**Tools:**
- Sphinx (installed)
- mypy (for validation)
- Python 3.14 (for running examples)

---

## Estimated Effort

**docs/api/logging.rst:** 2-3 hours
- Extract from docstrings: 30 min
- Format RST properly: 1 hour
- Add type-safe examples: 1 hour
- Validate and test: 30 min

**docs/client/** (new structure): 3-4 hours
- Create directory structure: 15 min
- Create index.rst: 30 min
- Create logging.rst: 2 hours
- Add type-safe examples: 1 hour
- Validate and test: 45 min

**Integration & Validation:** 1-2 hours
- Update main index files: 30 min
- Build and fix warnings: 30 min
- Verify all links: 30 min
- Final validation: 30 min

**Total:** 6-9 hours (1-1.5 days)

---

## Success Metrics

- [ ] Sphinx build: 0 warnings
- [ ] Type checking: 0 errors
- [ ] All cross-links work
- [ ] HTML renders correctly
- [ ] All function signatures verified
- [ ] All examples validated
