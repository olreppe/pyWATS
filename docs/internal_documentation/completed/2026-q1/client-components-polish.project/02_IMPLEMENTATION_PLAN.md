# Client Components Polish - Implementation Plan

**Project:** Client Components Polish  
**Status:** In Progress  
**Timeline:** Sprint 1-2 (2 weeks)  
**Created:** 2026-02-02

---

## Overview

Polish client components from **54-72/80** to **75+/80** by:
1. Creating missing examples
2. Standardizing error handling
3. Enhancing documentation
4. Improving getting started experience

---

## Sprint 1: Examples & Error Handling (Week 1)

### 1.1 Complete Missing Examples

#### Attachment I/O Example
**File:** `examples/client/attachment_io.py` (new)

**Tasks:**
- [ ] File upload example
- [ ] File download example
- [ ] Large file handling
- [ ] Metadata management
- [ ] Error handling

**Implementation:**
```python
"""
Example: Working with file attachments in pyWATS

Demonstrates:
- Uploading files to assets/products
- Downloading attachments
- Managing attachment metadata
- Handling large files
"""

from pywats import Client
from pathlib import Path

def upload_attachment_example():
    """Upload a file to an asset."""
    client = Client()
    
    # Upload a file
    file_path = Path("document.pdf")
    attachment = client.asset.upload_attachment(
        asset_id="ASSET-123",
        file_path=file_path,
        description="Test document"
    )
    
    print(f"Uploaded: {attachment.filename} (ID: {attachment.id})")

def download_attachment_example():
    """Download an attachment."""
    client = Client()
    
    # Download to file
    client.asset.download_attachment(
        asset_id="ASSET-123",
        attachment_id="ATT-456",
        output_path="downloaded.pdf"
    )
    
    print("Downloaded successfully")

if __name__ == "__main__":
    upload_attachment_example()
    download_attachment_example()
```

#### Error Handling Example
**File:** `examples/client/error_handling.py` (new)

**Tasks:**
- [ ] Retry strategies
- [ ] Graceful degradation
- [ ] Error logging
- [ ] Recovery patterns

**Implementation:**
```python
"""
Example: Robust error handling in pyWATS

Demonstrates:
- Handling different exception types
- Retry strategies with exponential backoff
- Graceful degradation
- Error logging best practices
"""

from pywats import Client
from pywats.exceptions import (
    NotFoundError,
    AuthenticationError,
    ServerError,
    ValidationError
)
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_with_backoff(func, max_retries=3):
    """Retry function with exponential backoff."""
    for attempt in range(max_retries):
        try:
            return func()
        except ServerError as e:
            if attempt == max_retries - 1:
                logger.error(f"Max retries exceeded: {e}")
                raise
            
            wait_time = 2 ** attempt
            logger.warning(f"Retry {attempt+1}/{max_retries} after {wait_time}s: {e}")
            time.sleep(wait_time)

def handle_specific_errors():
    """Handle different error types appropriately."""
    client = Client()
    
    try:
        asset = client.asset.get("ASSET-123")
        
    except NotFoundError:
        logger.warning("Asset not found, creating new one")
        asset = client.asset.create(name="New Asset")
        
    except AuthenticationError:
        logger.error("Authentication failed - check credentials")
        raise
        
    except ValidationError as e:
        logger.error(f"Invalid request: {e}")
        # Fix validation issues and retry
        raise
        
    except ServerError as e:
        logger.error(f"Server error: {e}")
        # Use retry logic
        asset = retry_with_backoff(lambda: client.asset.get("ASSET-123"))
    
    return asset

if __name__ == "__main__":
    asset = handle_specific_errors()
    print(f"Successfully retrieved: {asset.name}")
```

#### Configuration Example
**File:** `examples/client/configuration.py` (new)

**Tasks:**
- [ ] Environment-specific configs
- [ ] Authentication patterns
- [ ] Connection settings
- [ ] Performance tuning

#### Batch Operations Example
**File:** `examples/client/batch_operations.py` (new)

**Tasks:**
- [ ] Bulk create/update
- [ ] Parallel processing
- [ ] Progress tracking
- [ ] Error handling for batch

#### Advanced Async Example
**File:** `examples/client/async_advanced.py` (new)

**Tasks:**
- [ ] Concurrent operations
- [ ] Error handling in async
- [ ] Context managers
- [ ] Best practices

### 1.2 Standardize Error Handling

**Files:** Client modules in `src/pywats_client/`

**Tasks:**
- [ ] Audit current error handling
- [ ] Define standard patterns
- [ ] Update inconsistent code
- [ ] Add error handling tests
- [ ] Document patterns

**Standard Pattern:**
```python
# Add to pywats_client/core/error_handler.py
class StandardErrorHandler:
    """Standardized error handling for client operations."""
    
    @staticmethod
    def with_retry(func, max_retries=3, backoff_factor=2):
        """Execute function with retry logic."""
        ...
    
    @staticmethod
    def handle_response(response):
        """Standardized response handling."""
        ...
```

---

## Sprint 2: Documentation & Polish (Week 2)

### 2.1 Enhance Docstrings

**Files:** All public APIs in `src/pywats/` and `src/pywats_client/`

**Tasks:**
- [ ] Add examples to all public methods
- [ ] Document parameters fully
- [ ] Document return types
- [ ] Document exceptions
- [ ] Add type hints

**Template:**
```python
def operation(param: str, optional: int = 0) -> Result:
    """
    Brief description.
    
    Longer description with context and use cases.
    
    Args:
        param: Description of required parameter
        optional: Description of optional parameter (default: 0)
        
    Returns:
        Result object with details
        
    Raises:
        ErrorType: When this error occurs
        
    Example:
        >>> client = Client()
        >>> result = client.operation("value")
        >>> print(result.status)
        success
        
    See Also:
        - related_operation(): Related functionality
    """
    ...
```

### 2.2 Create Usage Guides

#### Quick Start Guide
**File:** `docs/guides/quickstart.md` (enhance existing)

**Tasks:**
- [ ] Streamline installation
- [ ] Simplify authentication
- [ ] Add first success milestone
- [ ] Target <15 minutes
- [ ] Test with new users

**Structure:**
```markdown
# Quick Start (15 minutes)

## 1. Installation (2 minutes)
## 2. Authentication (3 minutes)
## 3. First API Call (5 minutes)
## 4. Common Operations (5 minutes)
## 5. Next Steps
```

#### Authentication Guide
**File:** `docs/guides/authentication.md` (new)

**Topics:**
- API key setup
- Token management
- Environment variables
- Security best practices

#### Error Handling Guide
**File:** `docs/guides/error_handling.md` (new)

**Topics:**
- Exception hierarchy
- Retry strategies
- Logging patterns
- Debugging tips

#### Troubleshooting Guide
**File:** `docs/guides/troubleshooting.md` (new)

**Topics:**
- Common errors
- Diagnostic commands
- Log analysis
- Getting help

### 2.3 Improve Example Comments

**Files:** All examples in `examples/`

**Tasks:**
- [ ] Add explanatory comments
- [ ] Document why, not just what
- [ ] Add output examples
- [ ] Cross-reference docs

**Pattern:**
```python
# Good: Explains why and provides context
# We use error mode LENIENT here because assets may not exist
# in development environments, and we want to continue processing
client = Client(error_mode=ErrorMode.LENIENT)

# Instead of just:
# Set error mode
client = Client(error_mode=ErrorMode.LENIENT)
```

### 2.4 Update README

**File:** `README.md`

**Tasks:**
- [ ] Add client examples section
- [ ] Highlight key features
- [ ] Link to guides
- [ ] Add troubleshooting quick links

---

## Testing Strategy

### Example Validation
**File:** `tests/examples/test_examples.py`

**Tasks:**
- [ ] Validate all examples run
- [ ] Check example output
- [ ] Ensure examples stay updated

```python
def test_examples_run():
    """Ensure all examples execute without errors."""
    import subprocess
    
    examples = [
        "examples/client/attachment_io.py",
        "examples/client/error_handling.py",
        # ...
    ]
    
    for example in examples:
        result = subprocess.run(["python", example], capture_output=True)
        assert result.returncode == 0, f"{example} failed"
```

### Documentation Tests
**File:** `tests/docs/test_docstrings.py`

**Tasks:**
- [ ] Verify all public APIs have docstrings
- [ ] Check docstring format
- [ ] Validate examples in docstrings

---

## Documentation

### File Organization
```
docs/
├── guides/
│   ├── quickstart.md (enhanced)
│   ├── authentication.md (new)
│   ├── error_handling.md (new)
│   ├── troubleshooting.md (new)
│   └── performance.md (existing)
└── api/
    └── (auto-generated from docstrings)

examples/
├── getting_started/ (existing)
├── client/
│   ├── attachment_io.py (new)
│   ├── error_handling.py (new)
│   ├── configuration.py (new)
│   ├── batch_operations.py (new)
│   └── async_advanced.py (new)
└── (domain-specific examples)
```

---

## Success Criteria

- [x] All client examples runnable and complete
- [x] Error handling follows standard patterns
- [x] 100% of public APIs have docstring examples
- [x] Getting started guide <15 minutes
- [x] Client examples score 70+/80
- [x] Troubleshooting guide complete
- [x] All examples validated in tests

---

## Rollout Plan

### Week 1: Examples & Error Handling
1. Create missing examples
2. Standardize error handling
3. Test examples
4. Initial validation

### Week 2: Documentation & Polish
1. Enhance docstrings
2. Create usage guides
3. Update README
4. Final testing and validation

---

**Estimated Effort:** 2 sprints (10-12 development days)  
**Risk Level:** Low (documentation and examples)  
**Priority:** P4 (Medium Impact, Low-Medium Effort)
