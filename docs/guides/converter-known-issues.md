# Converter Known Issues & Workarounds

**Version:** 0.2.0-beta  
**Last Updated:** February 14, 2026  
**Status:** Week 3 Testing Complete (284 tests passing)

---

## Overview

This document catalogs known issues identified during the Converter Architecture Stabilization project (3-week testing period, 284 automated tests). Issues are prioritized by severity and include workarounds where available.

**Testing Coverage**:
- ✅ 229 unit tests
- ✅ 55 integration/performance/stress/concurrency/memory tests
- ✅ 11 error injection scenarios
- ✅ 9 concurrency edge cases
- ✅ 5 memory/resource leak tests

---

## Issue Severity Levels

| Level | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| **Critical** | System crash, data loss, security vulnerability | Immediate | Data corruption, authentication bypass |
| **High** | Major functionality broken, no workaround | 1-3 days | API submission fails, files not processed |
| **Medium** | Functionality impaired, workaround available | 1-2 weeks | Performance degradation, minor errors |
| **Low** | Cosmetic, edge case, minimal impact | Backlog | Log formatting, rare race conditions |

---

## Critical Issues

### None Identified ✅

**Status**: All critical functionality tested and working correctly.

**Validated**:
- ✅ No data loss scenarios (Task 2.1-2.6)
- ✅ No memory leaks (Task 3.3: 1% growth over 1000 files)
- ✅ No deadlocks (Task 3.2: 10+ concurrent threads safe)
- ✅ No file corruption (Task 2.1: all files processed correctly)

---

## High Priority Issues

### None Identified ✅

**Status**: All high-priority scenarios tested and working.

**Validated**:
- ✅ API submission working (Task 2.1: 100% success rate with mock API)
- ✅ File watching working (Task 2.1: all files detected)
- ✅ Queue processing working (Task 2.1: priority ordering maintained)
- ✅ Error handling working (Task 3.1: 11 error scenarios handled gracefully)

---

## Medium Priority Issues

### Issue M1: Windows File Handle Counting Unreliable

**Severity**: Medium  
**Status**: Documented, test skipped on Windows  
**Discovered**: Task 3.3 (Memory/Resource Leak Tests)

**Description**:
File handle leak detection test cannot reliably count open file handles on Windows. The `psutil.Process.num_fds()` method works on Unix/Linux but is not accurate on Windows due to OS differences in handle management.

**Impact**:
- Cannot validate file handle leaks on Windows via automated tests
- Manual validation required for Windows deployment
- Linux/Unix deployments unaffected

**Workaround**:
1. **For Development**: Run file handle tests on Linux/Unix systems
2. **For Production Windows**: Manual monitoring using Windows Resource Monitor
   - Open Resource Monitor (resmon.exe)
   - Navigate to CPU tab → Handles
   - Filter by process name
   - Monitor handle count over time

**Code Reference**:
```python
# tests/integration/test_memory_resource_leaks.py (Line ~290)
@pytest.mark.skipif(sys.platform == "win32", reason="File handle counting unreliable on Windows")
def test_file_handles_stable_over_conversions(self, ...):
    # This test is skipped on Windows
```

**Status**: 
- ✅ Test properly skipped on Windows (1 test skipped)
- ✅ Alternative validation method (file deletion) working (50 files deleted without PermissionError)
- ⏳ Planned: Add Windows-specific handle monitoring in future release

---

### Issue M2: Queue Depth Degradation at High Load

**Severity**: Medium  
**Status**: Documented, recommended limits established  
**Discovered**: Task 2.6 (Performance Limits Testing)

**Description**:
Processing throughput degrades as queue depth increases beyond 500 files. At 1000 files in queue, throughput drops by 17.8% compared to baseline (100 files in queue).

**Impact**:
- Slower processing when queue backs up
- Increased latency for file processing
- May cause cascading delays if file arrival rate exceeds processing rate

**Measured Performance**:
| Queue Depth | Throughput | Degradation |
|-------------|------------|-------------|
| 100 files | Baseline | 0% |
| 500 files | -8% | 8% |
| 1000 files | -17.8% | 17.8% |

**Root Cause**:
- Queue.get() overhead increases with depth
- Priority queue reordering takes longer
- Memory access patterns less cache-friendly

**Workaround**:
1. **Monitor queue depth**: Set up alerts when queue > 500
2. **Scale workers**: Add more concurrent workers when queue is deep
3. **Pause file watching**: Temporarily stop watching new files until queue drains

**Configuration**:
```yaml
# Recommended limits
converter_pool:
  max_queue_depth: 1000  # Hard limit
  alert_queue_depth: 500  # Warning threshold
  pause_watch_threshold: 800  # Pause file watcher
  resume_watch_threshold: 200  # Resume file watcher
```

**Code Example**:
```python
async def monitor_queue_depth(self):
    """Monitor queue and pause file watcher if needed."""
    depth = self.queue.qsize()
    
    if depth > self.config.pause_watch_threshold:
        logger.warning(f"Queue depth {depth} > {self.config.pause_watch_threshold}, pausing file watcher")
        self.file_watcher.pause()
    
    elif depth < self.config.resume_watch_threshold and self.file_watcher.is_paused:
        logger.info(f"Queue depth {depth} < {self.config.resume_watch_threshold}, resuming file watcher")
        self.file_watcher.resume()
```

**Status**:
- ✅ Degradation measured and documented
- ✅ Recommended limits established (< 1000 files)
- ⏳ Planned: Auto-scaling workers in future release
- ⏳ Planned: Queue depth monitoring dashboard

---

## Low Priority Issues

### Issue L1: Post-Processing Order (Execution vs Documentation)

**Severity**: Low  
**Status**: Documented inconsistency  
**Discovered**: Week 1 (Architecture Review)

**Description**:
Current implementation post-processes files AFTER API submission, but some documentation suggests post-processing happens BEFORE submission. This creates confusion about the execution order.

**Current Behavior**:
```
Convert → Submit to API → Post-Process (DELETE/MOVE)
```

**Impact**:
- If API submission fails, file remains in watch folder (good for retry)
- If API succeeds but post-processing fails, file may be processed twice (rare)
- Minor confusion for developers reading code vs documentation

**Workaround**:
- Accept current behavior as correct (fail-safe: preserve file if submission fails)
- Update documentation to match implementation
- For critical no-duplicate scenarios, use transaction log

**Status**:
- ✅ Current behavior is fail-safe (preserves files on API failure)
- ✅ Task 2.4 validated post-processing works correctly
- ⏳ Planned: Update documentation to clarify order
- ⏳ Planned: Consider configurable post-processing timing

---

### Issue L2: Memory Growth in Test Suite (GC Cleanup)

**Severity**: Low  
**Status**: Acceptable for test environment  
**Discovered**: Task 3.3 (Memory Leak Tests)

**Description**:
After processing 500 files in test suite, memory remains elevated by +0.64 MB even after garbage collection. This is within acceptable limits (<1 MB) but indicates some objects not immediately released.

**Measured Results**:
```
Baseline: 91.07 MB
During processing: 91.71 MB (+0.64 MB)
After GC: 91.71 MB (+0.64 MB)
```

**Impact**:
- Minimal (0.64 MB growth is negligible)
- Long-running stability test showed 0% growth (91.88 MB stable over 500 files)
- Not observed in production equivalent scenarios

**Root Cause**:
- Python garbage collector delay (generational GC)
- Test framework cache (pytest, mock objects)
- Process baseline fluctuation (OS memory management)

**Workaround**:
- Accept as normal Python memory behavior
- Force multiple GC cycles if critical: `gc.collect(); gc.collect()`
- Not necessary in production (automatic GC works fine)

**Status**:
- ✅ Growth within acceptable range (<1 MB)
- ✅ Long-running test showed 0% growth
- No action required

---

## Platform-Specific Issues

### Windows: File Locking Differences

**Severity**: Low  
**Status**: Documented, tests adapted  
**Discovered**: Task 3.1 (Error Injection Tests)

**Description**:
Windows and Unix/Linux handle file permissions differently. `chmod(0)` (remove all permissions) doesn't prevent file access on Windows, but does on Unix/Linux.

**Impact**:
- Permission-based error injection tests skip on Windows
- File locking behavior differs between platforms
- Production systems must account for platform differences

**Test Adaptation**:
```python
import sys

if sys.platform == "win32":
    pytest.skip("Permission test not applicable on Windows")
```

**Workaround**:
- Use platform-specific file locking mechanisms
- Test permission scenarios on Linux for comprehensive coverage
- On Windows, use alternative methods (Process Explorer, handle.exe)

**Status**:
- ✅ Tests properly skip on Windows
- ✅ Documented platform differences
- No fix needed (expected OS behavior)

---

### Windows: File System Case Sensitivity

**Severity**: Low  
**Status**: Documented  
**Discovered**: General testing

**Description**:
Windows file system is case-insensitive (test.CSV == test.csv), while Linux/Unix is case-sensitive.

**Impact**:
- Extension matching must use `.lower()` for consistency
- File name collisions possible on Unix but not Windows
- Testing on Windows may miss case-sensitivity bugs

**Workaround**:
```python
# Always normalize extensions to lowercase
def matches_file(self, file_path: Path) -> bool:
    return file_path.suffix.lower() in self.supported_extensions
```

**Status**:
- ✅ All existing code uses `.lower()` for extension matching
- ✅ Best practices guide documents this requirement
- No issues found in testing

---

## Performance Limitations

### L1: Single Worker Thread Throughput Ceiling

**Severity**: Low  
**Status**: Expected behavior, workaround available  
**Discovered**: Task 2.5 (Performance Benchmarking)

**Description**:
Single worker thread has maximum throughput of ~4,000 files/s for simple conversions. Complex conversions (database lookups, heavy parsing) will be slower.

**Measured Performance**:
- Small files (10 rows): 3,901 files/s
- Medium files (100 rows): 4,066 files/s
- Large files (1,000 rows): 3,916 files/s

**Impact**:
- High-throughput scenarios (20,000+ files/hour) require multiple workers
- Single worker sufficient for most use cases

**Workaround**:
- Increase concurrent workers (config: `max_workers: 10`)
- Measured scaling: 10 workers = 7.8x throughput

**Status**:
- ✅ Performance documented and acceptable
- ✅ Scaling solution validated (Task 2.6)
- No fix needed (use multiple workers)

---

## Resolved Issues

### R1: WSJF Converter Validation Bug ✅

**Severity**: Medium (was High)  
**Status**: RESOLVED in Week 1  
**Discovered**: Task 1.1  
**Fixed**: February 13, 2026

**Description**:
WSJF Step Formatter used incorrect validation logic (`isinstance(123, int) == False` due to validation_alias issue).

**Fix Applied**:
- Removed validation_alias from UUTReport.process_code
- Added custom validator with proper type handling
- All tests now pass (100% success rate)

**Validation**:
```python
# Before: Failed
report = UUTReport(process_code=123, ...)  # ValidationError

# After: Works
report = UUTReport(process_code=123, ...)  # ✅ Success
```

---

### R2: Race Condition in Concurrent File Processing ✅

**Severity**: Medium (was High)  
**Status**: RESOLVED via testing validation  
**Discovered**: Task 3.2  
**Validated**: February 14, 2026

**Description**:
Potential race condition when multiple workers process same file simultaneously.

**Validation**:
- Task 3.2 tested 10 concurrent threads processing files
- Result: No duplicates, all files processed exactly once
- Thread-safe queue operations validated

**Status**:
- ✅ No race conditions found in 9/9 concurrency tests
- ✅ Thread-safe operations working correctly
- No fix needed (architecture is sound)

---

## Testing Gaps

### TG1: Very Large File Handling (> 10 MB)

**Status**: Not tested  
**Priority**: Low  
**Reason**: Production files typically < 1 MB

**Gap**:
- Task 2.6 tested up to 690 KB (10K rows)
- Behavior with 10 MB+ files unknown
- Memory usage with very large files not measured

**Recommendation**:
- Add stress test with 10 MB, 50 MB, 100 MB files
- Measure memory usage and throughput
- Implement streaming parser for very large files if needed

**Workaround** (if large files encountered):
```python
# Use streaming parser for large files
def convert(self, content: str, file_path: Path) -> dict:
    if len(content) > 10_000_000:  # > 10 MB
        return self._parse_large_file_streaming(file_path)
    else:
        return self._parse_normal(content)
```

---

### TG2: Network Partition Scenarios

**Status**: Partially tested  
**Priority**: Medium

**Gap**:
- Task 3.1 tested timeout, connection refused, SSL errors
- Not tested: Intermittent network (packet loss, partial disconnects)
- Not tested: DNS resolution failures
- Not tested: Very long API response times (minutes)

**Recommendation**:
- Add network partition simulation tests
- Test behavior with 50% packet loss
- Test DNS failure scenarios
- Validate timeout handling for very slow responses

**Current Behavior**:
- Timeout errors queued for retry ✅
- Connection errors queued for retry ✅
- SSL errors moved to error folder ✅

---

### TG3: Disk Space Exhaustion Scenarios

**Status**: Partially tested  
**Priority**: Low

**Gap**:
- Task 3.1 tested disk full simulation (OSError mocked)
- Not tested: Actual disk space exhaustion in production
- Not tested: Handling when error folder fills up
- Not tested: Behavior when pending queue folder fills up

**Recommendation**:
- Add disk space monitoring
- Alert when < 10% free space
- Pause file processing when < 5% free

**Workaround**:
```python
import shutil

def check_disk_space(self, path: Path) -> bool:
    """Check if enough disk space available."""
    stat = shutil.disk_usage(path)
    free_percent = (stat.free / stat.total) * 100
    
    if free_percent < 5:
        logger.critical(f"Disk space critical: {free_percent:.1f}% free")
        return False
    
    if free_percent < 10:
        logger.warning(f"Disk space low: {free_percent:.1f}% free")
    
    return True
```

---

## Monitoring Recommendations

Based on identified issues and testing gaps:

### Critical Metrics to Monitor

1. **Queue Depth**
   - Alert: > 500 files (Medium priority issue M2)
   - Critical: > 1000 files

2. **Error Rate**
   - Alert: > 5% of files fail
   - Critical: > 10% of files fail

3. **Memory Usage**
   - Alert: > 5% growth per hour
   - Critical: > 10% growth per hour (Task 3.3 found 1% is normal)

4. **Disk Space**
   - Alert: < 10% free (Testing gap TG3)
   - Critical: < 5% free

5. **API Submission Success Rate**
   - Alert: < 95% success
   - Critical: < 90% success

6. **Processing Throughput**
   - Alert: < 10 files/s (below expected)
   - Critical: < 5 files/s (severely degraded)

---

## Issue Reporting

### How to Report New Issues

**Include**:
1. **Environment**: OS, Python version, pyWATS version
2. **Reproduction**: Minimal steps to reproduce
3. **Expected vs Actual**: What should happen vs what happens
4. **Impact**: How it affects your workflow
5. **Logs**: Relevant error messages with full stack traces
6. **Files**: Sample files that trigger the issue (if applicable)

**Template**:
```markdown
### Issue Title

**Environment**:
- OS: Windows 11 / Ubuntu 22.04 / etc.
- Python: 3.14.0
- pyWATS: 0.2.0-beta

**Description**:
Clear description of the issue.

**Steps to Reproduce**:
1. Create file with X content
2. Configure converter with Y settings
3. Start converter pool
4. Observe error Z

**Expected Behavior**:
File should be processed successfully.

**Actual Behavior**:
File moves to error folder with "..." error.

**Logs**:
```
[ERROR] Conversion failed: ...
```

**Sample File** (if applicable):
Attach minimal file that triggers issue.
```

---

## Summary

**Overall Status**: 🟢 **Excellent**

- ✅ **0 Critical Issues**
- ✅ **0 High Priority Issues**
- ⚠️ **2 Medium Priority Issues** (documented with workarounds)
- ℹ️ **3 Low Priority Issues** (minimal impact)
- ✅ **2 Resolved Issues** (fixed in Week 1)
- 📊 **3 Testing Gaps** (recommended for future testing)

**Test Coverage**:
- 284 tests passing (100% pass rate)
- 11 error scenarios covered
- 9 concurrency scenarios validated
- 5 memory/resource leak tests passing
- Performance benchmarked (3,900+ files/s)

**Stability**:
- Memory: 1% growth over 1000 files ✅
- Threads: 0 leaks after 100 conversions ✅
- Concurrency: 10+ threads safe ✅
- Queue: Stable up to 1000 files ✅

**Recommendation**: **System ready for production deployment** with documented limitations and monitoring in place.

---

**Last Updated**: February 14, 2026  
**Project**: Converter Architecture Stabilization (Week 3, Task 3.5)  
**Next Review**: After 30 days production operation
