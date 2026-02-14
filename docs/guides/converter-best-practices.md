# Converter Best Practices Guide

**Version:** 0.2.0-beta  
**Last Updated:** February 14, 2026  
**Audience:** Production system developers and administrators

---

## Overview

This guide consolidates best practices discovered during 3 weeks of testing the pyWATS converter architecture, including:
- 284 automated tests (229 unit + 55 integration)
- Performance benchmarking (3,900+ files/s throughput)
- Error injection testing (file system, network, module loading)
- Concurrency validation (10+ concurrent threads, 314 files/s)
- Memory leak detection (0-1% growth over 1000+ conversions)

---

## Converter Development Patterns

### 1. Always Validate Input

**❌ Bad**:
```python
def convert(self, content: str, file_path: Path) -> dict:
    data = json.loads(content)
    report = UUTReport(
        sn=data['serial'],  # Assumes field exists
        pn=data['part'],
        # ...
    )
```

**✅ Good**:
```python
def convert(self, content: str, file_path: Path) -> dict:
    # Validate not empty
    if not content or not content.strip():
        raise ValueError("File content is empty")
    
    # Parse with error handling
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    
    # Validate required fields
    required = ['serial', 'part', 'result']
    missing = [f for f in required if f not in data]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")
    
    # Create report with validated data
    report = UUTReport(sn=data['serial'], pn=data['part'])
```

**Why**: Validation prevents cryptic errors downstream and helps users fix their data files.

---

### 2. Use Resource-Safe File Handling

**❌ Bad**:
```python
def convert(self, content: str, file_path: Path) -> dict:
    f = open(file_path, 'r')
    extra_data = f.read()  # File handle not closed!
    # ... process
```

**✅ Good**:
```python
def convert(self, content: str, file_path: Path) -> dict:
    # Option 1: Context manager
    with open(file_path, 'r') as f:
        extra_data = f.read()
    
    # Option 2: Path methods (auto-cleanup)
    extra_data = file_path.read_text()
    
    # ... process
```

**Why**: **Task 3.3 validated** that file handle leaks can accumulate. Proper cleanup prevents:
- PermissionError when trying to delete files
- Running out of file descriptors under high load

---

### 3. Thread-Safe Shared State

**❌ Bad**:
```python
class MyConverter(ConverterBase):
    def __init__(self):
        super().__init__()
        self.conversion_count = 0  # Shared state without lock
    
    def convert(self, content: str, file_path: Path) -> dict:
        self.conversion_count += 1  # Race condition!
        # ...
```

**✅ Good**:
```python
import threading

class MyConverter(ConverterBase):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.conversion_count = 0
    
    def convert(self, content: str, file_path: Path) -> dict:
        with self.lock:
            self.conversion_count += 1
            count = self.conversion_count
        
        # Do work outside lock to avoid blocking
        # ...
```

**Why**: **Task 3.2 validated** that concurrent converters can process 10+ files simultaneously. Without locks:
- Counters become inaccurate
- Shared data structures (lists, dicts) can corrupt
- Race conditions cause unpredictable behavior

---

### 4. Efficient Parsing

**❌ Bad** (O(n²) complexity):
```python
def convert(self, content: str, file_path: Path) -> dict:
    lines = content.split('\n')
    
    # Repeatedly iterate over all lines
    sn = None
    for line in lines:
        if line.startswith('SERIAL:'):
            sn = line.split(':')[1]
    
    pn = None
    for line in lines:  # Iterate again!
        if line.startswith('PART:'):
            pn = line.split(':')[1]
```

**✅ Good** (O(n) complexity):
```python
def convert(self, content: str, file_path: Path) -> dict:
    lines = content.split('\n')
    
    # Single pass to extract all fields
    data = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip()
    
    sn = data.get('SERIAL')
    pn = data.get('PART')
```

**Why**: **Task 2.5 benchmarked** 3,900+ files/s throughput. Efficient parsing:
- Reduces CPU usage (15-25% vs 40-60%)
- Improves throughput
- Handles large files better

---

### 5. Proper Error Messages

**❌ Bad**:
```python
raise ValueError("Invalid")
raise ValueError("Error in file")
raise ValueError("Bad data")
```

**✅ Good**:
```python
raise ValueError(f"Missing required field 'SERIAL' in {file_path.name}")
raise ValueError(f"Invalid date format in START_TIME: expected YYYY-MM-DD, got '{raw_date}'")
raise ValueError(f"Unknown test result '{result}': must be one of PASS, FAIL, ERROR, TERMINATED")
```

**Why**: **Task 3.1 tested** 11 error scenarios. Clear error messages help:
- Users fix their data files quickly
- Operators debug production issues
- Log analysis identify patterns

---

### 6. Progressive Parsing for Large Files

**❌ Bad** (loads entire file):
```python
def convert(self, content: str, file_path: Path) -> dict:
    # Load entire XML into memory
    tree = ET.parse(content)
    root = tree.getroot()
    
    # Even if we only need header...
    sn = root.find('.//Header/Serial').text
```

**✅ Good** (lazy evaluation):
```python
def convert(self, content: str, file_path: Path) -> dict:
    # For very large files, use incremental parsing
    if len(content) > 1_000_000:  # > 1 MB
        return self._parse_large_file(file_path)
    else:
        return self._parse_normal(content)

def _parse_large_file(self, file_path: Path) -> dict:
    # Use streaming parser
    for event, elem in ET.iterparse(file_path, events=('start', 'end')):
        if event == 'end' and elem.tag == 'Header':
            sn = elem.find('Serial').text
            break  # Stop early, don't parse rest
```

**Why**: **Task 2.6 tested** files up to 690KB (10K rows). Large file optimization:
- Reduces memory usage
- Improves responsiveness
- Prevents timeouts

---

## Testing Recommendations

### 1. Test File Generators

**✅ Use test file generators** instead of real files:

```python
from tests.fixtures.test_file_generators import TestFileGenerator

def test_csv_conversion():
    # Generate test CSV with controlled parameters
    test_file = TestFileGenerator.generate_csv_file(
        output_path=tmp_path / "test.csv",
        rows=50,
        columns=['PartNumber', 'SerialNumber', 'Result']
    )
    
    converter = CSVConverter()
    content = test_file.read_text()
    result = converter.convert(content, test_file)
    
    assert result['sn'] is not None
```

**Benefits**:
- **Control**: Exact field values, row counts, formats
- **Speed**: Generate 1000+ files in <4 seconds
- **Corruption**: Test malformed files easily
- **Repeatability**: Same files every test run

---

### 2. Mock Converters for Integration Tests

**✅ Create lightweight mock converters**:

```python
class MockSlowConverter(ConverterBase):
    """Simulates slow converter for performance testing."""
    
    def __init__(self, delay_ms: int = 100):
        super().__init__()
        self.delay_ms = delay_ms
        self.conversion_count = 0
    
    def convert(self, content: str, file_path: Path) -> dict:
        time.sleep(self.delay_ms / 1000.0)
        self.conversion_count += 1
        
        return UUTReport(
            sn=f"SN-{self.conversion_count}",
            pn="MOCK-PART",
            # ... minimal report
        ).model_dump()
```

**Benefits**:
- **Fast**: No complex parsing logic
- **Controllable**: Adjust delay, failure rate
- **Measurable**: Track conversion counts
- **Predictable**: Same behavior every run

---

### 3. Test Error Scenarios

**✅ Test what happens when things fail**:

```python
def test_locked_file_handling(converter, tmp_path):
    """Test converter handles locked files gracefully."""
    from tests.fixtures.test_file_generators import LockedFile
    
    test_file = tmp_path / "locked.csv"
    test_file.write_text("test data")
    
    with LockedFile(test_file):
        # File is locked by another process
        with pytest.raises(PermissionError):
            content = test_file.read_text()

def test_disk_full_handling(converter, tmp_path, monkeypatch):
    """Test converter handles disk full errors."""
    def mock_write_text(*args, **kwargs):
        raise OSError("No space left on device")
    
    monkeypatch.setattr(Path, 'write_text', mock_write_text)
    
    # Converter should handle gracefully
    # (implementation depends on your error handling)
```

**Why**: **Task 3.1 validated** 11 error scenarios:
- Locked files
- Disk full
- Network timeouts
- SSL errors
- Malformed data

---

### 4. Concurrency Testing

**✅ Test thread safety with concurrent operations**:

```python
import threading

def test_concurrent_conversions(converter):
    """Test converter handles concurrent calls safely."""
    
    def convert_file(file_num):
        content = f"SERIAL:SN-{file_num}\nPART:TEST\nRESULT:PASS"
        converter.convert(content, Path(f"test_{file_num}.txt"))
    
    # Spawn 10 concurrent threads
    threads = []
    for i in range(10):
        t = threading.Thread(target=convert_file, args=(i,))
        threads.append(t)
        t.start()
    
    # Wait for all to complete
    for t in threads:
        t.join()
    
    # Verify no race conditions
    assert converter.conversion_count == 10  # All counted
```

**Why**: **Task 3.2 validated** 10+ concurrent threads with:
- No race conditions
- No deadlocks
- No duplicate processing

---

### 5. Memory Leak Testing

**✅ Test long-running stability**:

```python
import gc
import psutil
import os

def test_no_memory_leaks(converter):
    """Test converter doesn't leak memory over many conversions."""
    process = psutil.Process(os.getpid())
    
    # Baseline memory
    gc.collect()
    baseline_mb = process.memory_info().rss / 1024 / 1024
    
    # Process 1000 files
    for i in range(1000):
        content = f"SERIAL:SN-{i}\nPART:TEST\nRESULT:PASS"
        converter.convert(content, Path(f"test_{i}.txt"))
    
    # Final memory
    gc.collect()
    final_mb = process.memory_info().rss / 1024 / 1024
    
    # Verify minimal growth
    growth_percent = ((final_mb - baseline_mb) / baseline_mb) * 100
    assert growth_percent < 5, f"Memory grew {growth_percent:.1f}%"
```

**Why**: **Task 3.3 validated** 1000+ file conversions with:
- 1.0% memory growth (well under 10% threshold)
- 0% growth in long-running stability test
- All file handles closed properly

---

## Performance Tips

### 1. Benchmark Your Converter

**Measure throughput**:

```python
import time

def benchmark_converter(converter, file_count=1000):
    """Measure converter throughput."""
    test_content = "SERIAL:SN-001\nPART:TEST\nRESULT:PASS"
    
    start = time.perf_counter()
    
    for i in range(file_count):
        converter.convert(test_content, Path(f"test_{i}.txt"))
    
    elapsed = time.perf_counter() - start
    throughput = file_count / elapsed
    
    print(f"Throughput: {throughput:.0f} files/s")
    print(f"Avg time: {elapsed/file_count*1000:.2f} ms/file")
    
    return throughput
```

**Target performance** (from Task 2.5):
- Small files (10 rows): 3,900+ files/s
- Medium files (100 rows): 4,000+ files/s
- Large files (1000 rows): 3,900+ files/s

---

### 2. Optimize Hot Paths

**Profile to find bottlenecks**:

```python
import cProfile
import pstats

def profile_converter(converter):
    """Profile converter performance."""
    profiler = cProfile.Profile()
    
    test_content = "..." # Your test content
    
    profiler.enable()
    for i in range(100):
        converter.convert(test_content, Path(f"test_{i}.txt"))
    profiler.disable()
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 slowest functions
```

**Common bottlenecks**:
- Regex compilation (cache patterns at class level)
- Repeated parsing (parse once, reuse)
- String concatenation in loops (use list + join)
- Unnecessary object creation (reuse where possible)

---

### 3. Queue Depth Management

**Monitor and limit queue depth**:

```python
# In your application
def monitor_queue(converter_pool):
    """Monitor queue depth and alert if too deep."""
    current_depth = converter_pool.queue.qsize()
    
    if current_depth > 500:
        logger.warning(f"Queue depth high: {current_depth}")
    
    if current_depth > 1000:
        logger.error(f"Queue depth critical: {current_depth}")
        # Maybe pause file watcher until queue drains
```

**Why**: **Task 2.6 found** queue performance degrades:
- 100 files: Baseline performance
- 500 files: 8% degradation
- 1000 files: 17.8% degradation

---

### 4. Concurrent Worker Scaling

**Scale workers based on load**:

```yaml
# converters.yaml
converter_pool:
  max_workers: 10  # Concurrent converters
  worker_scaling:
    min_workers: 2
    max_workers: 20
    scale_up_threshold: 100  # Add worker when queue > 100
    scale_down_threshold: 10  # Remove worker when queue < 10
```

**Why**: **Task 2.6 found** linear scaling up to 10 workers:
- 1 worker: Baseline
- 5 workers: 4.2x throughput
- 10 workers: 7.8x throughput

---

## Error Handling Guidelines

### 1. Use Specific Exception Types

**❌ Generic exceptions**:
```python
raise Exception("File is invalid")
raise Exception("Network error")
```

**✅ Specific exceptions**:
```python
raise ValueError("Missing required field: SERIAL")  # Data validation
raise FileNotFoundError(f"Source file not found: {file_path}")  # File I/O
raise ConnectionError("API submission failed: connection refused")  # Network
```

**Benefits**:
- Caller can handle specific errors differently
- Logs are more actionable
- Debugging is easier

---

### 2. Graceful Degradation

**Handle errors without crashing**:

```python
async def process_file(self, file_path: Path):
    """Process file with graceful error handling."""
    try:
        # Attempt conversion
        content = file_path.read_text()
        result = self.converter.convert(content, file_path)
        
        # Attempt submission
        await self.api_client.submit(result)
        
        # Success: delete/move file
        self.post_process(file_path, PostProcessAction.DELETE)
        
    except ValueError as e:
        # Conversion error: move to error folder
        logger.error(f"Conversion failed: {e}")
        self.move_to_error(file_path, str(e))
        
    except ConnectionError as e:
        # Network error: queue for retry
        logger.warning(f"Submission failed: {e}")
        self.save_queued_file(result, file_path)
        
    except Exception as e:
        # Unexpected error: log and move to error
        logger.exception(f"Unexpected error processing {file_path}")
        self.move_to_error(file_path, f"Unexpected: {e}")
```

**Why**: **Task 3.1 validated** graceful handling of:
- File system errors → Move to error folder
- Network errors → Queue for retry
- Converter errors → Log and skip
- Queue corruption → Skip corrupted files

---

### 3. Retry Strategies

**Implement smart retries**:

```python
import asyncio

async def submit_with_retry(self, report: dict, max_retries=3):
    """Submit report with exponential backoff."""
    for attempt in range(max_retries):
        try:
            report_id = await self.api_client.submit(report)
            return report_id
        
        except asyncio.TimeoutError:
            if attempt < max_retries - 1:
                delay = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                logger.warning(f"Timeout, retrying in {delay}s (attempt {attempt+1}/{max_retries})")
                await asyncio.sleep(delay)
            else:
                logger.error("Max retries exceeded, queuing for later")
                raise
        
        except ConnectionError:
            # Don't retry connection errors (API likely down)
            logger.error("Connection error, queuing for later")
            raise
```

**Best practices**:
- **Exponential backoff**: Avoid overwhelming recovering services
- **Max retries**: Prevent infinite retry loops
- **Selective retry**: Only retry transient errors (timeout, rate limit)
- **Don't retry**: Permanent errors (404, 400, authentication)

---

### 4. Error Logging

**Log actionable information**:

```python
import logging
import traceback

logger = logging.getLogger(__name__)

try:
    result = converter.convert(content, file_path)
except Exception as e:
    logger.error(
        "Conversion failed",
        extra={
            'file': str(file_path),
            'converter': converter.name,
            'error_type': type(e).__name__,
            'error_message': str(e),
            'traceback': traceback.format_exc(),
        }
    )
```

**Include context**:
- File name/path
- Converter name
- Error type and message
- Stack trace for debugging

---

## Monitoring and Observability

### 1. Key Metrics to Track

```python
from prometheus_client import Counter, Histogram, Gauge

# Counters
files_processed = Counter('converter_files_processed_total', 'Total files processed')
files_failed = Counter('converter_files_failed_total', 'Total files failed')
api_submissions = Counter('converter_api_submissions_total', 'Total API submissions')

# Histograms
conversion_duration = Histogram('converter_conversion_duration_seconds', 'Conversion duration')
submission_duration = Histogram('converter_submission_duration_seconds', 'Submission duration')

# Gauges
queue_depth = Gauge('converter_queue_depth', 'Current queue depth')
active_workers = Gauge('converter_active_workers', 'Active worker count')
```

**Usage**:
```python
with conversion_duration.time():
    result = converter.convert(content, file_path)
files_processed.inc()

queue_depth.set(self.queue.qsize())
```

---

### 2. Health Checks

```python
async def health_check(self) -> dict:
    """Return system health status."""
    return {
        'status': 'healthy' if self.is_running else 'stopped',
        'queue_depth': self.queue.qsize(),
        'active_workers': len(self.workers),
        'files_processed_total': self.stats.files_processed,
        'files_failed_total': self.stats.files_failed,
        'api_connected': await self.api_client.ping(),
        'uptime_seconds': time.time() - self.start_time,
    }
```

**Expose via HTTP endpoint**:
```python
from aiohttp import web

async def health(request):
    status = await converter_pool.health_check()
    return web.json_response(status)

app = web.Application()
app.router.add_get('/health', health)
```

---

### 3. Alerting Thresholds

**Set up alerts for**:

| Metric | Warning | Critical |
|--------|---------|----------|
| Queue Depth | > 500 files | > 1000 files |
| Error Rate | > 5% | > 10% |
| API Failures | > 10% | > 25% |
| Memory Growth | > 5% per hour | > 10% per hour |
| Processing Rate | < 10 files/s | < 5 files/s |

---

## Production Checklist

Before deploying to production:

- [ ] **Code Quality**
  - [ ] All tests passing (unit + integration)
  - [ ] Code coverage > 80%
  - [ ] No linting errors
  - [ ] Error handling comprehensive

- [ ] **Performance**
  - [ ] Throughput tested (target: 20+ files/s)
  - [ ] Memory leak tested (< 5% growth per hour)
  - [ ] Queue depth limits configured
  - [ ] Worker scaling tested

- [ ] **Error Handling**
  - [ ] File system errors handled
  - [ ] Network errors handled with retry
  - [ ] Converter errors logged with context
  - [ ] Queue corruption handled

- [ ] **Monitoring**
  - [ ] Metrics collection configured
  - [ ] Health checks implemented
  - [ ] Alerts configured
  - [ ] Log aggregation set up

- [ ] **Documentation**
  - [ ] Converter behavior documented
  - [ ] Configuration examples provided
  - [ ] Troubleshooting guide created
  - [ ] Runbook for operators

- [ ] **Security**
  - [ ] File permissions locked down
  - [ ] API credentials secured
  - [ ] Input validation thorough
  - [ ] No sensitive data in logs

---

## Summary

**Key Takeaways**:

1. **Validate everything**: Input data, file formats, field values
2. **Handle resources properly**: Use context managers, close files
3. **Thread safety**: Lock shared state in concurrent converters
4. **Graceful errors**: Don't crash, log and continue
5. **Test thoroughly**: Unit, integration, performance, memory, concurrency
6. **Monitor actively**: Queue depth, error rate, throughput
7. **Optimize wisely**: Profile first, then optimize hot paths

**Validation**:
- ✅ 284 tests passing (100% pass rate)
- ✅ 3,900+ files/s throughput
- ✅ 1% memory growth over 1000 files
- ✅ 10+ concurrent workers tested
- ✅ 11 error scenarios validated

---

**Last Updated**: February 14, 2026  
**Project**: Converter Architecture Stabilization (Week 3, Tasks 3.4 + 3.6)
