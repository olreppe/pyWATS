# Exception Handling Best Practices

**Version:** 1.0  
**Last Updated:** February 8, 2026  
**Applies To:** pyWATS v0.5.1+

---

## Quick Reference

### ✅ DO

- **Use specific exception types** - Catch `ValidationError`, not generic `Exception`
- **Re-raise after logging** - Log the error, then `raise` to propagate it
- **Include troubleshooting hints** - Help users understand what went wrong and how to fix it
- **Use logger.exception()** - Automatically includes stack trace in logs
- **Add context to exceptions** - Include relevant details (file path, operation type, etc.)
- **Test exception scenarios** - Use `pytest.raises()` to verify error handling
- **Document exceptions in docstrings** - List what exceptions can be raised

### ❌ DON'T

- **Catch generic `Exception`** without re-raising - Swallows all errors including unexpected ones
- **Swallow exceptions silently** - Always log or re-raise
- **Log without `exc_info`** - Missing stack trace makes debugging impossible
- **Catch `KeyboardInterrupt` or `SystemExit`** - Let these propagate to allow clean shutdown
- **Use bare `except:`** - Catches everything including syntax errors
- **Create new exception hierarchies** - Use existing pyWATS exceptions
- **Log and re-raise without adding value** - Either transform the exception or just re-raise

---

## 1. When to Catch vs Bubble

### Decision Tree

```
┌─────────────────────────────────┐
│   Exception Occurred            │
└────────────┬────────────────────┘
             │
             ▼
    ┌────────────────────┐
    │ Can you recover?   │
    └────┬───────────┬───┘
         │           │
        YES          NO
         │           │
         ▼           ▼
    ┌─────────┐  ┌──────────────┐
    │ CATCH   │  │ Can you add  │
    │ HANDLE  │  │ value?       │
    └─────────┘  └──┬───────┬───┘
                    │       │
                   YES      NO
                    │       │
                    ▼       ▼
              ┌──────────┐ ┌────────┐
              │ CATCH    │ │ BUBBLE │
              │ TRANSFORM│ │ (raise)│
              │ RE-RAISE │ └────────┘
              └──────────┘
```

### Catch and Handle (Recover)

**When to use:** You can recover from the error and continue execution.

**Example: Graceful Degradation**
```python
def get_product_with_fallback(product_id: str) -> Product:
    """Get product from cache, fallback to API if cache miss."""
    try:
        return cache.get_product(product_id)
    except CacheError as e:
        logger.warning(f"Cache miss for product {product_id}: {e}")
        # Recover by fetching from API
        return api.get_product(product_id)
```

**Example: Retry Logic**
```python
def send_with_retry(data: dict, max_retries: int = 3) -> bool:
    """Send data with automatic retry on transient errors."""
    for attempt in range(max_retries):
        try:
            api.send_report(data)
            return True
        except TimeoutError as e:
            if attempt < max_retries - 1:
                logger.warning(f"Timeout on attempt {attempt + 1}, retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.error(f"Failed after {max_retries} attempts", exc_info=True)
                raise
```

### Catch, Transform, and Re-raise

**When to use:** You want to add context or convert to a more appropriate exception type.

**Example: Add Business Context**
```python
def convert_file(file_path: Path) -> Report:
    """Convert file to WATS report."""
    try:
        data = parser.parse_csv(file_path)
        return create_report(data)
    except FileNotFoundError as e:
        raise ConverterError(
            f"File not found: {file_path}",
            converter_name="CSVConverter",
            file_path=str(file_path)
        ) from e
    except ParseError as e:
        raise ConverterError(
            f"Invalid CSV format in {file_path.name}",
            converter_name="CSVConverter",
            file_path=str(file_path)
        ) from e
```

### Log and Re-raise

**When to use:** You can't handle the error but want to record that it happened at this layer.

**Example: Layer Boundary Logging**
```python
def process_unit(unit_id: str) -> ProcessedUnit:
    """Process a unit through the test sequence."""
    try:
        unit = fetch_unit(unit_id)
        results = run_tests(unit)
        return finalize_results(results)
    except Exception as e:
        logger.exception(f"Failed to process unit {unit_id}")
        raise  # Re-raise the original exception
```

### Bubble (Don't Catch)

**When to use:** You can't add value, and a higher layer should decide what to do.

**Example: Let Caller Decide**
```python
def parse_serial_number(value: str) -> str:
    """Parse and validate serial number."""
    if not value:
        raise ValidationError("Serial number is required")
    
    if not re.match(r'^[A-Z0-9]{6,12}$', value):
        raise ValidationError(
            f"Invalid serial number format: {value}",
            details={"expected_format": "6-12 alphanumeric characters"}
        )
    
    return value.upper()
    # No try/except - let caller handle ValidationError
```

---

## 2. Exception Patterns

### Pattern 1: Log and Re-raise (Most Common)

**Use when:** Logging for debugging, but can't handle the error.

```python
def api_operation(data: dict) -> dict:
    """Perform API operation with logging."""
    try:
        response = api_client.post("/endpoint", json=data)
        return response.json()
    except ConnectionError as e:
        logger.exception("API connection failed", exc_info=True)
        raise  # Re-raise original exception
```

**Key points:**
- Use `logger.exception()` or `logger.error(..., exc_info=True)`
- Always re-raise with `raise` (no argument)
- Don't create new exception - preserve original stack trace

### Pattern 2: Catch, Transform, Re-raise

**Use when:** Converting low-level exceptions to domain exceptions.

```python
def store_configuration(config: dict) -> None:
    """Save configuration to disk."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except OSError as e:
        raise ConfigurationError(
            f"Failed to save configuration to {CONFIG_FILE}",
            details={"error": str(e), "path": str(CONFIG_FILE)}
        ) from e  # ← Use 'from e' to preserve chain
```

**Key points:**
- Use `raise NewException(...) from e` to preserve exception chain
- Add business context in new exception
- Include troubleshooting hints
- Log at appropriate level before raising

### Pattern 3: Graceful Degradation

**Use when:** Failure is acceptable with reduced functionality.

```python
def get_report_with_analytics(report_id: int) -> Report:
    """Get report with optional analytics data."""
    report = api.get_report(report_id)
    
    try:
        analytics = analytics_service.get_metrics(report_id)
        report.analytics = analytics
    except (ConnectionError, TimeoutError) as e:
        logger.warning(f"Analytics unavailable for report {report_id}: {e}")
        report.analytics = None  # Degrade gracefully
    
    return report
```

**Key points:**
- Log the degradation at WARNING level
- Document degraded behavior in docstring
- Test both success and degraded paths

### Pattern 4: Resource Cleanup

**Use when:** Must clean up resources regardless of success/failure.

```python
def process_with_cleanup(file_path: Path) -> Result:
    """Process file with guaranteed cleanup."""
    temp_dir = None
    try:
        temp_dir = create_temp_directory()
        data = extract_to_temp(file_path, temp_dir)
        result = process_data(data)
        return result
    except Exception as e:
        logger.exception(f"Processing failed for {file_path}")
        raise
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)
```

**Key points:**
- Use `try...finally` for cleanup
- Cleanup runs even if exception occurs
- Consider context managers (`with`) when possible

### Pattern 5: Context Manager (Preferred for Resources)

**Use when:** Managing resources (files, connections, locks).

```python
from contextlib import contextmanager

@contextmanager
def conversion_log_context(operation_name: str):
    """Context manager for conversion logging."""
    log = ConversionLog.create_for_file(operation_name)
    try:
        yield log
        log.finalize(success=True)
    except Exception as e:
        log.error("Conversion failed", exception=e, raise_after_log=False)
        log.finalize(success=False, error=str(e))
        raise  # Re-raise after logging

# Usage
with conversion_log_context("test_data.csv") as log:
    log.step("Reading file")
    data = read_file()
    log.step("Processing")
    result = process(data)
```

**Key points:**
- Automatically handles cleanup
- Guarantees finalization
- More Pythonic than try/finally

---

## 3. Layer-Specific Guidelines

### API Layer (pyWATS Core)

**Responsibilities:**
- Raise specific domain exceptions
- Don't catch exceptions unless adding value
- Let exceptions bubble to client

**Example:**
```python
from pywats.core.exceptions import NotFoundError, ValidationError

def get_product(product_id: str) -> Product:
    """Get product by ID.
    
    Raises:
        ValidationError: If product_id is invalid
        NotFoundError: If product does not exist
    """
    if not product_id:
        raise ValidationError("Product ID is required")
    
    endpoint = f"/api/products/{product_id}"
    response = self._request("GET", endpoint)
    
    if response.status_code == 404:
        raise NotFoundError(f"Product not found: {product_id}")
    
    return Product.from_dict(response.json())
    # No catch - let HTTP errors bubble
```

### Client Layer (pyWATS Client)

**Responsibilities:**
- Transform API exceptions to client exceptions
- Add business context
- Log for debugging

**Example:**
```python
from pywats_client.exceptions import ConverterError

def convert_csv_file(file_path: Path) -> Report:
    """Convert CSV file to WATS report.
    
    Raises:
        ConverterError: If conversion fails
    """
    try:
        with open(file_path, 'r') as f:
            data = csv.DictReader(f)
            report = transform_to_report(data)
        
        return report
    
    except FileNotFoundError as e:
        logger.error(f"File not found: {file_path}", exc_info=True)
        raise ConverterError(
            f"CSV file not found: {file_path}",
            converter_name="CSVConverter",
            file_path=str(file_path)
        ) from e
    
    except (csv.Error, ValueError) as e:
        logger.error(f"CSV parse error in {file_path}", exc_info=True)
        raise ConverterError(
            f"Invalid CSV format in {file_path.name}",
            converter_name="CSVConverter",
            file_path=str(file_path)
        ) from e
```

### GUI Layer (pyWATS UI)

**Responsibilities:**
- Catch ALL exceptions (terminal layer)
- Display user-friendly messages
- Log for support/debugging
- Use ErrorHandlingMixin

**Example:**
```python
from pywats_ui.framework.error_mixin import ErrorHandlingMixin

class ProductPage(BasePage, ErrorHandlingMixin):
    """Product management page."""
    
    def _on_load_button_click(self):
        """Handle load button click."""
        product_id = self.product_id_input.text()
        
        try:
            product = api.get_product(product_id)
            self.display_product(product)
            self.show_success(f"Loaded product: {product.name}")
        
        except ValidationError as e:
            # Specific error - custom handling
            self.handle_error(e, "loading product")
            self.product_id_input.setFocus()
        
        except NotFoundError as e:
            # Specific error - custom handling
            self.handle_error(e, "loading product")
        
        except Exception as e:
            # Catch-all for unexpected errors
            logger.exception(f"Unexpected error loading product {product_id}")
            self.handle_error(e, "loading product")
```

### Converter Layer

**Responsibilities:**
- Log to ConversionLog
- Re-raise exceptions (as of v0.5.1)
- Provide detailed error context

**Example:**
```python
def convert_with_logging(file_path: Path) -> Report:
    """Convert file with detailed logging."""
    log = ConversionLog.create_for_file(file_path.name)
    
    try:
        log.step("Reading file", metadata={"size": file_path.stat().st_size})
        data = read_file(file_path)
        
        log.step("Parsing data", metadata={"rows": len(data)})
        parsed = parse_data(data)
        
        log.step("Creating report")
        report = create_report(parsed)
        
        log.finalize(success=True, report_id=report.id)
        return report
    
    except FileNotFoundError as e:
        log.error("File not found", exception=e)  # Logs AND re-raises (v0.5.1+)
        log.finalize(success=False, error=str(e))
    
    except ParseError as e:
        log.error("Parse error", exception=e)  # Logs AND re-raises (v0.5.1+)
        log.finalize(success=False, error=str(e))
```

---

## 4. Common Scenarios

### Scenario 1: File Operations

```python
def save_report_to_file(report: Report, file_path: Path) -> None:
    """Save report to file.
    
    Raises:
        FileAccessError: If file cannot be written
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        
        logger.info(f"Report saved to {file_path}")
    
    except (OSError, IOError) as e:
        logger.error(f"Failed to save report to {file_path}", exc_info=True)
        raise FileAccessError(
            f"Cannot write to file: {file_path}",
            file_path=str(file_path),
            operation="write"
        ) from e
```

### Scenario 2: Network Operations

```python
def fetch_with_retry(url: str, max_retries: int = 3) -> dict:
    """Fetch data with automatic retry.
    
    Raises:
        ConnectionError: If all retries fail
        TimeoutError: If request times out
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        
        except requests.Timeout as e:
            if attempt == max_retries - 1:
                logger.error(f"Request timeout after {max_retries} attempts", exc_info=True)
                raise TimeoutError(f"Request timed out: {url}") from e
            logger.warning(f"Timeout on attempt {attempt + 1}, retrying...")
            time.sleep(2 ** attempt)
        
        except requests.ConnectionError as e:
            if attempt == max_retries - 1:
                logger.error(f"Connection failed after {max_retries} attempts", exc_info=True)
                raise ConnectionError(f"Cannot connect to: {url}") from e
            logger.warning(f"Connection failed on attempt {attempt + 1}, retrying...")
            time.sleep(2 ** attempt)
```

### Scenario 3: Validation

```python
def validate_unit_data(data: dict) -> None:
    """Validate unit test data.
    
    Raises:
        ValidationError: If data is invalid
    """
    errors = []
    
    if not data.get('serial_number'):
        errors.append("Serial number is required")
    
    if not data.get('process'):
        errors.append("Process name is required")
    
    if 'test_results' not in data:
        errors.append("Test results are required")
    elif not isinstance(data['test_results'], list):
        errors.append("Test results must be a list")
    
    if errors:
        raise ValidationError(
            "Unit data validation failed",
            details={"errors": errors, "data_keys": list(data.keys())}
        )
```

### Scenario 4: Database/Queue Operations

```python
def queue_operation_with_fallback(operation: dict) -> str:
    """Queue operation with disk fallback.
    
    Raises:
        QueueCriticalError: If both queue and fallback fail
    """
    operation_id = generate_id()
    
    try:
        queue.enqueue(operation_id, operation)
        logger.info(f"Operation queued: {operation_id}")
        return operation_id
    
    except QueueFullError as e:
        logger.warning(f"Queue full, using fallback storage", exc_info=True)
        
        try:
            fallback_storage.save(operation_id, operation)
            logger.info(f"Operation saved to fallback: {operation_id}")
            return operation_id
        
        except IOError as fallback_error:
            # Double failure - CRITICAL
            logger.critical(
                "CRITICAL: Both queue and fallback failed",
                exc_info=True,
                extra={
                    "operation_id": operation_id,
                    "queue_error": str(e),
                    "fallback_error": str(fallback_error)
                }
            )
            raise QueueCriticalError(
                "Failed to queue operation. Both queue and fallback storage failed.",
                primary_error=str(e),
                fallback_error=str(fallback_error),
                operation_id=operation_id
            ) from fallback_error
```

---

## 5. Anti-Patterns (DON'T DO THIS)

### ❌ Anti-Pattern 1: Bare Except

```python
# DON'T
def process_data(data):
    try:
        return transform(data)
    except:  # ← Catches EVERYTHING including KeyboardInterrupt!
        return None

# DO
def process_data(data):
    try:
        return transform(data)
    except (ValueError, TypeError) as e:  # ← Specific exceptions
        logger.error(f"Invalid data format", exc_info=True)
        raise
```

### ❌ Anti-Pattern 2: Swallowing Exceptions

```python
# DON'T
def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except Exception:
        pass  # ← Silent failure!

# DO
def load_config():
    try:
        with open('config.json') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Config file not found, using defaults")
        return get_default_config()
    except json.JSONDecodeError as e:
        logger.error(f"Invalid config file", exc_info=True)
        raise ConfigurationError("Invalid configuration file format") from e
```

### ❌ Anti-Pattern 3: Logging Without exc_info

```python
# DON'T
def process():
    try:
        do_something()
    except Exception as e:
        logger.error(f"Error: {e}")  # ← No stack trace!
        raise

# DO
def process():
    try:
        do_something()
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)  # ← Stack trace included
        # OR
        logger.exception(f"Error: {e}")  # ← Equivalent, preferred
        raise
```

### ❌ Anti-Pattern 4: Catching Too Broadly

```python
# DON'T
def save_data(data):
    try:
        validate(data)
        transform(data)
        persist(data)
    except Exception as e:  # ← Which step failed?
        logger.error(f"Save failed: {e}")
        raise

# DO
def save_data(data):
    try:
        validate(data)
    except ValidationError as e:
        logger.error("Validation failed", exc_info=True)
        raise
    
    try:
        transformed = transform(data)
    except TransformError as e:
        logger.error("Transformation failed", exc_info=True)
        raise
    
    try:
        persist(transformed)
    except PersistenceError as e:
        logger.error("Persistence failed", exc_info=True)
        raise
```

### ❌ Anti-Pattern 5: Losing Exception Chain

```python
# DON'T
def load_file(path):
    try:
        return parse(path)
    except IOError as e:
        raise ValueError(f"Bad file")  # ← Original error lost!

# DO
def load_file(path):
    try:
        return parse(path)
    except IOError as e:
        raise ValueError(f"Bad file: {path}") from e  # ← Chain preserved
```

### ❌ Anti-Pattern 6: Multiple Catches Without Adding Value

```python
# DON'T
def api_call():
    try:
        return api.get_data()
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise ConnectionError(f"Connection error: {e}")  # ← Pointless

# DO
def api_call():
    # Just let it bubble if you can't add value
    return api.get_data()
    
# OR add actual value
def api_call_with_context(user_id):
    try:
        return api.get_data()
    except ConnectionError as e:
        logger.error(f"Connection error for user {user_id}", exc_info=True)
        raise ConnectionError(
            f"Failed to fetch data for user {user_id}",
            details={"user_id": user_id}
        ) from e
```

---

## 6. Testing Exception Handling

### Basic Exception Test

```python
def test_validation_raises_error():
    """Test that invalid data raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validate_serial_number("")
    
    assert "required" in str(exc_info.value).lower()
```

### Testing Exception Details

```python
def test_converter_error_includes_context():
    """Test that ConverterError includes file path."""
    with pytest.raises(ConverterError) as exc_info:
        convert_file(Path("/nonexistent/file.csv"))
    
    error = exc_info.value
    assert error.converter_name == "CSVConverter"
    assert "/nonexistent/file.csv" in error.file_path
```

### Testing Exception Chain

```python
def test_exception_chain_preserved():
    """Test that exception chain is preserved."""
    with pytest.raises(ConfigurationError) as exc_info:
        load_invalid_config()
    
    # Check original exception is in chain
    assert exc_info.value.__cause__ is not None
    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)
```

### Testing Logging

```python
def test_exception_logged(caplog):
    """Test that exception is logged with stack trace."""
    with pytest.raises(ProcessingError):
        process_bad_data({"invalid": "data"})
    
    # Verify logging
    assert "Processing failed" in caplog.text
    assert "Traceback" in caplog.text  # Stack trace present
```

---

## 7. Migration Guide (v0.5.0 → v0.5.1)

### ConversionLog Changes

**Before (v0.5.0):**
```python
log = ConversionLog.create_for_file("data.csv")
try:
    data = parse_file()
except ParseError as e:
    log.error("Parse failed", exception=e)  # Logged only
    # Exception NOT re-raised - silent failure!
```

**After (v0.5.1):**
```python
log = ConversionLog.create_for_file("data.csv")
try:
    data = parse_file()
except ParseError as e:
    log.error("Parse failed", exception=e)  # Logs AND re-raises!
    # Exception propagates - caller is notified

# For backward compatibility (if needed):
log.error("Parse failed", exception=e, raise_after_log=False)
```

---

## 8. Helpful Debugging Tips

### Enable Detailed Logging

```python
import logging

# Set to DEBUG for development
logging.basicConfig(level=logging.DEBUG)

# Or configure specific logger
logger = logging.getLogger('pywats.converters')
logger.setLevel(logging.DEBUG)
```

### Use Post-Mortem Debugging

```python
import pdb

def process_with_debug():
    try:
        do_something_risky()
    except Exception:
        pdb.post_mortem()  # Drop into debugger at exception
        raise
```

### Add Breakpoints

```python
def complex_operation():
    data = fetch_data()
    breakpoint()  # Python 3.7+ - drops into debugger
    result = process(data)
    return result
```

---

## 9. Summary Checklist

When writing exception handling code, ask yourself:

- [ ] **Specific?** - Am I catching specific exceptions, not bare `Exception`?
- [ ] **Logged?** - Am I logging with `exc_info=True` or `logger.exception()`?
- [ ] **Chain?** - Am I preserving the exception chain with `from e`?
- [ ] **Context?** - Am I adding useful context (file path, operation, etc.)?
- [ ] **Documented?** - Are exceptions listed in the docstring?
- [ ] **Tested?** - Do I have tests using `pytest.raises()`?
- [ ] **Re-raised?** - If I can't handle it, am I re-raising?
- [ ] **User-friendly?** - If this reaches GUI, is the message helpful?

---

## Related Documentation

- [Error Propagation Guide](error-propagation.md) - How errors flow through layers
- [Logging Guide](logging.md) - Structured logging best practices
- [Developer Checklist](developer-checklist.md) - Complete development checklist
- [API Reference: Exceptions](../api/exceptions.rst) - Exception class reference

---

**Questions or Issues?**  
Open an issue on GitHub or ask in the pyWATS developer channel.
