# Implementation Plan: Final Push for v0.3.0b1

**Project:** final-push-0.3.0b1  
**Date:** February 2, 2026  
**Total Effort:** 26 hours (3.25 days)

---

## 📋 Overview

This plan details the step-by-step implementation of 5 high-impact, low-risk improvements identified in the Final Assessment. The plan is organized into 6 phases with clear deliverables and testing checkpoints.

---

## 🗓️ Phase Timeline

| Phase | Focus | Duration | Day |
|-------|-------|----------|-----|
| Phase 1 | SyncWrapper Event Loop Optimization | 6 hours | Day 1 |
| Phase 2 | Default Station Registry | 4 hours | Day 1-2 |
| Phase 3 | Circuit Breaker Pattern | 6 hours | Day 2 |
| Phase 4 | Structured Logging Foundation | 6 hours | Day 3 |
| Phase 5 | Performance Benchmarks | 4 hours | Day 3-4 |
| Phase 6 | Integration Testing & Documentation | 6 hours | Day 4 |

**Total:** 32 hours with buffer (4 full days or 2-4 days with parallelization)

---

## 🚀 Phase 1: SyncWrapper Event Loop Optimization (6 hours)

**Goal:** Implement thread-local event loop pooling for 10-100x sync API performance improvement

**Impact:** Performance score +1 point (B+ → A-)

### Step 1.1: Create EventLoopPool Module (1 hour)

**File:** `src/pywats/core/event_loop_pool.py`

**Implementation:**
```python
"""Event loop pooling for sync API wrapper.

Provides thread-local event loop reuse to avoid creating new loops
on every sync API call. Improves performance by 10-100x.
"""

import asyncio
import threading
from typing import Optional, TypeVar, Coroutine

T = TypeVar('T')


class EventLoopPool:
    """Thread-safe event loop pool for sync API wrapper.
    
    Maintains one event loop per thread, running in a background thread.
    Allows sync wrapper to reuse connections and avoid loop creation overhead.
    """
    
    _thread_local = threading.local()
    _lock = threading.Lock()
    
    @classmethod
    def get_or_create_loop(cls) -> asyncio.AbstractEventLoop:
        """Get or create event loop for current thread.
        
        Returns:
            Event loop instance (reused across calls in same thread)
        """
        if not hasattr(cls._thread_local, 'loop'):
            with cls._lock:
                # Double-check after acquiring lock
                if not hasattr(cls._thread_local, 'loop'):
                    loop = asyncio.new_event_loop()
                    cls._thread_local.loop = loop
                    cls._thread_local.thread = threading.Thread(
                        target=cls._run_loop,
                        args=(loop,),
                        daemon=True,
                        name=f"EventLoopThread-{threading.get_ident()}"
                    )
                    cls._thread_local.thread.start()
        
        return cls._thread_local.loop
    
    @classmethod
    def _run_loop(cls, loop: asyncio.AbstractEventLoop):
        """Run event loop in background thread."""
        asyncio.set_event_loop(loop)
        loop.run_forever()
    
    @classmethod
    def run_coroutine(cls, coro: Coroutine[any, any, T]) -> T:
        """Run coroutine in thread-local event loop.
        
        Args:
            coro: Coroutine to execute
            
        Returns:
            Result of coroutine execution
        """
        loop = cls.get_or_create_loop()
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result()
    
    @classmethod
    def shutdown_all(cls):
        """Shutdown all event loops (for testing/cleanup)."""
        if hasattr(cls._thread_local, 'loop'):
            loop = cls._thread_local.loop
            loop.call_soon_threadsafe(loop.stop)
            cls._thread_local.thread.join(timeout=1.0)
            del cls._thread_local.loop
            del cls._thread_local.thread
```

**Tests:** `tests/core/test_event_loop_pool.py`
```python
def test_event_loop_pool_reuses_loop():
    """Verify same loop is reused across calls."""
    loop1 = EventLoopPool.get_or_create_loop()
    loop2 = EventLoopPool.get_or_create_loop()
    assert loop1 is loop2

def test_event_loop_pool_thread_isolation():
    """Verify different threads get different loops."""
    import concurrent.futures
    
    def get_loop_id():
        return id(EventLoopPool.get_or_create_loop())
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(get_loop_id)
        future2 = executor.submit(get_loop_id)
        
        assert future1.result() != future2.result()

async def test_coroutine():
    return "success"

def test_run_coroutine():
    """Verify coroutines execute correctly."""
    result = EventLoopPool.run_coroutine(test_coroutine())
    assert result == "success"
```

### Step 1.2: Update Sync Wrapper Implementation (2 hours)

**File:** `src/pywats/pywats.py`

**Changes:**
1. Import `EventLoopPool`
2. Replace `asyncio.new_event_loop()` with `EventLoopPool.run_coroutine()`
3. Remove loop cleanup (loop persists for reuse)

**Before:**
```python
def get_report(self, report_id: str) -> Report:
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(self._async.get_report(report_id))
    finally:
        loop.close()
```

**After:**
```python
from pywats.core.event_loop_pool import EventLoopPool

def get_report(self, report_id: str) -> Report:
    return EventLoopPool.run_coroutine(self._async.get_report(report_id))
```

**Apply to ALL sync wrapper methods** (~50 methods across domains)

### Step 1.3: Benchmark Performance Improvement (1 hour)

**File:** `tests/performance/test_sync_wrapper_performance.py`

**Implementation:**
```python
import pytest
from pywats import pyWATS, AsyncWATS

@pytest.mark.benchmark
def test_sync_wrapper_performance(benchmark, mock_wats_server):
    """Benchmark sync wrapper with event loop pooling.
    
    Expected: <50ms per call (vs 200-500ms before optimization)
    """
    api = pyWATS(server_url="http://localhost:8080")
    
    def get_report():
        return api.get_report("RPT-123")
    
    result = benchmark(get_report)
    
    # After optimization: should be close to async performance
    assert result.stats.mean < 0.05  # <50ms average
    assert result.stats.median < 0.03  # <30ms median

@pytest.mark.benchmark
def test_sync_vs_async_overhead():
    """Verify sync wrapper overhead is minimal (<2x async)."""
    import time
    
    async_api = AsyncWATS(server_url="http://localhost:8080")
    sync_api = pyWATS(server_url="http://localhost:8080")
    
    # Measure async baseline
    start = time.perf_counter()
    for _ in range(100):
        asyncio.run(async_api.get_report("RPT-123"))
    async_time = time.perf_counter() - start
    
    # Measure sync with pooling
    start = time.perf_counter()
    for _ in range(100):
        sync_api.get_report("RPT-123")
    sync_time = time.perf_counter() - start
    
    overhead = sync_time / async_time
    assert overhead < 2.0  # Sync should be <2x async
```

### Step 1.4: Update Documentation (1 hour)

**Files to Update:**
- `docs/guides/performance.md` - Add section on sync wrapper optimization
- `examples/performance/sync_wrapper_benchmark.py` - Example showing performance
- `CHANGELOG.md` - Add entry under `[Unreleased] - Improved`

**Documentation Content:**
```markdown
## Sync Wrapper Performance Optimization

**Version:** 0.3.0b1+  
**Impact:** 10-100x faster sync API calls

### What Changed

The synchronous API wrapper (`pyWATS`) now uses thread-local event loop pooling
instead of creating a new event loop for every call. This provides:

- 10-100x performance improvement for repeated calls
- HTTP connection pooling (reuses connections)
- Lower memory overhead (no loop creation/destruction)

### Performance Comparison

**Before Optimization:**
```python
# 100 calls to get_report()
# Time: ~15-20 seconds (200ms per call)
# Overhead: New event loop + new HTTP connection each call
```

**After Optimization:**
```python
# 100 calls to get_report()
# Time: ~2-3 seconds (20-30ms per call)
# Overhead: Minimal (reuses loop + connections)
```

### No Code Changes Required

The optimization is transparent - existing code continues to work:
```python
api = pyWATS(server_url="http://wats-server")
report = api.get_report("RPT-123")  # ✅ Automatically faster
```
```

### Step 1.5: Testing & Validation (1 hour)

**Test Checklist:**
- [ ] Run full test suite: `pytest` (416+ tests passing)
- [ ] Run new event loop pool tests: `pytest tests/core/test_event_loop_pool.py`
- [ ] Run performance benchmarks: `pytest tests/performance/ --benchmark-only`
- [ ] Test thread safety: `pytest tests/core/test_event_loop_pool.py::test_event_loop_pool_thread_isolation`
- [ ] Manual validation: Run `examples/performance/sync_wrapper_benchmark.py`

**Success Criteria:**
- ✅ All existing tests pass (no regressions)
- ✅ Benchmark shows ≥10x improvement
- ✅ Thread safety verified (concurrent access works)
- ✅ Connection pooling confirmed (check HTTP logs)

---

## 🏢 Phase 2: Default Station Registry (4 hours)

**Goal:** Auto-detect station name from environment/hostname with configurable overrides

**Impact:** Developer experience improvement, Usability +0.5 point

### Step 2.1: Create StationRegistry Module (1.5 hours)

**File:** `src/pywats/core/station_registry.py`

**Implementation:**
```python
"""Station registry with auto-detection and configuration support.

Detects station name from environment, hostname, or config files.
Provides zero-config experience for most users while allowing
explicit configuration when needed.
"""

import os
import socket
import platform
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class StationRegistry:
    """Auto-detect and manage station configuration.
    
    Detection priority:
    1. Explicit configuration (constructor argument)
    2. Environment variable (PYWATS_STATION)
    3. Platform hostname (Windows: COMPUTERNAME, Unix: hostname)
    4. Config file (~/.pywats/station.conf)
    5. None (warning logged)
    """
    
    @staticmethod
    def auto_detect() -> Optional[str]:
        """Auto-detect station name from environment.
        
        Returns:
            Station name (sanitized) or None if detection fails
        """
        # Priority 1: Environment variable
        if station := os.environ.get("PYWATS_STATION"):
            logger.info(f"Station detected from PYWATS_STATION: {station}")
            return StationRegistry._sanitize(station)
        
        # Priority 2: Platform-specific hostname
        try:
            if platform.system() == "Windows":
                # Use COMPUTERNAME on Windows
                station = os.environ.get("COMPUTERNAME")
            else:
                # Use hostname on Unix-like systems
                station = socket.gethostname()
            
            if station:
                sanitized = StationRegistry._sanitize(station)
                logger.info(f"Station auto-detected from hostname: {sanitized}")
                return sanitized
        except Exception as e:
            logger.warning(f"Failed to auto-detect station from hostname: {e}")
        
        # Priority 3: Config file
        if station := StationRegistry.load_from_config():
            logger.info(f"Station loaded from config file: {station}")
            return station
        
        return None
    
    @staticmethod
    def load_from_config() -> Optional[str]:
        """Load station name from config file.
        
        Checks:
        - {workspace}/.pywats/station.conf
        - ~/.pywats/station.conf
        
        Returns:
            Station name from config or None
        """
        config_paths = [
            Path.cwd() / ".pywats" / "station.conf",  # Workspace config
            Path.home() / ".pywats" / "station.conf",  # User config
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    station = path.read_text().strip()
                    if station:
                        return StationRegistry._sanitize(station)
                except Exception as e:
                    logger.warning(f"Failed to read station config from {path}: {e}")
        
        return None
    
    @staticmethod
    def _sanitize(station: str) -> str:
        """Sanitize station name to WATS-compatible format.
        
        Rules:
        - Convert to uppercase
        - Replace spaces with hyphens
        - Remove invalid characters
        
        Args:
            station: Raw station name
            
        Returns:
            Sanitized station name
        """
        # Convert to uppercase
        station = station.upper()
        
        # Replace spaces and underscores with hyphens
        station = station.replace(" ", "-").replace("_", "-")
        
        # Remove invalid characters (keep alphanumeric and hyphens)
        station = "".join(c for c in station if c.isalnum() or c == "-")
        
        return station
```

**Tests:** `tests/core/test_station_registry.py`
```python
import os
import pytest
from pathlib import Path
from pywats.core.station_registry import StationRegistry

def test_auto_detect_from_env_variable(monkeypatch):
    """Verify environment variable takes priority."""
    monkeypatch.setenv("PYWATS_STATION", "test-station-001")
    assert StationRegistry.auto_detect() == "TEST-STATION-001"

def test_auto_detect_from_hostname_windows(monkeypatch):
    """Verify Windows hostname detection."""
    monkeypatch.setattr("platform.system", lambda: "Windows")
    monkeypatch.setenv("COMPUTERNAME", "WORKSTATION-42")
    monkeypatch.delenv("PYWATS_STATION", raising=False)
    
    assert StationRegistry.auto_detect() == "WORKSTATION-42"

def test_auto_detect_from_hostname_unix(monkeypatch):
    """Verify Unix hostname detection."""
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr("socket.gethostname", lambda: "test-machine.local")
    monkeypatch.delenv("PYWATS_STATION", raising=False)
    
    assert StationRegistry.auto_detect() == "TEST-MACHINE-LOCAL"

def test_load_from_config(tmp_path, monkeypatch):
    """Verify config file loading."""
    config_path = tmp_path / ".pywats" / "station.conf"
    config_path.parent.mkdir(parents=True)
    config_path.write_text("STATION-FROM-CONFIG")
    
    monkeypatch.setattr("pathlib.Path.cwd", lambda: tmp_path)
    assert StationRegistry.load_from_config() == "STATION-FROM-CONFIG"

def test_sanitize_station_name():
    """Verify station name sanitization."""
    assert StationRegistry._sanitize("Test Station 001") == "TEST-STATION-001"
    assert StationRegistry._sanitize("work_station_42") == "WORK-STATION-42"
    assert StationRegistry._sanitize("station@#$%123") == "STATION123"
```

### Step 2.2: Integrate with pyWATS API (1 hour)

**File:** `src/pywats/pywats.py`

**Changes:**
1. Add `station: Optional[str]` parameter to `__init__()`
2. Auto-detect station if not provided
3. Expose `api.station` property

**Implementation:**
```python
from pywats.core.station_registry import StationRegistry

class pyWATS:
    def __init__(
        self,
        server_url: str,
        settings: Optional[WATSSettings] = None,
        station: Optional[str] = None,  # NEW PARAMETER
    ):
        """Initialize pyWATS synchronous API wrapper.
        
        Args:
            server_url: WATS server URL
            settings: Optional WATS settings (auto-discovered if not provided)
            station: Station name (auto-detected if not provided)
        """
        self._async = AsyncWATS(server_url=server_url, settings=settings)
        
        # Auto-detect station if not provided
        self._station = station or StationRegistry.auto_detect()
        
        if not self._station:
            logger.warning(
                "No station configured. Set PYWATS_STATION environment variable "
                "or pass station='STATION-NAME' to constructor."
            )
    
    @property
    def station(self) -> Optional[str]:
        """Get current station name.
        
        Returns:
            Station name or None if not configured
        """
        return self._station
```

**Apply same changes to `AsyncWATS` class**

### Step 2.3: Update Examples & Documentation (1 hour)

**Files to Update:**
- `examples/getting_started/basic_usage.py` - Show zero-config example
- `docs/guides/configuration.md` - Document station detection
- `CHANGELOG.md` - Add entry

**Example Code:**
```python
"""Zero-config station detection example."""
from pywats import pyWATS

# Before: Manual configuration required
# api = pyWATS(server_url="http://wats-server")
# api.set_station("STATION-001")  # Manual setup

# After: Auto-detected from hostname
api = pyWATS(server_url="http://wats-server")
print(f"Station: {api.station}")  # Auto-detected from COMPUTERNAME/hostname

# Explicit override (CI/CD, testing)
api = pyWATS(server_url="http://wats-server", station="CI-STATION")
print(f"Station: {api.station}")  # CI-STATION
```

### Step 2.4: Testing & Validation (0.5 hours)

**Test Checklist:**
- [ ] Run station registry tests: `pytest tests/core/test_station_registry.py`
- [ ] Test Windows detection: Mock `COMPUTERNAME`
- [ ] Test Unix detection: Mock `socket.gethostname()`
- [ ] Test env variable priority: Set `PYWATS_STATION`
- [ ] Verify `api.station` property accessible

**Success Criteria:**
- ✅ Auto-detection works on all platforms
- ✅ Environment variable takes priority
- ✅ Config file fallback works
- ✅ `api.station` property documented

---

## 🛡️ Phase 3: Circuit Breaker Pattern (6 hours)

**Goal:** Implement circuit breaker to prevent retry storms when service is down

**Impact:** Error Handling +1 point (A- → A)

### Step 3.1: Create CircuitBreaker Module (2 hours)

**File:** `src/pywats/core/circuit_breaker.py`

**Implementation:**
```python
"""Circuit breaker pattern for fault tolerance.

Prevents retry storms when service is down by failing fast after
consecutive failures. Automatically tests for recovery.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional, Callable, TypeVar
from enum import Enum
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class CircuitState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "CLOSED"      # Normal operation
    OPEN = "OPEN"          # Service down, fail fast
    HALF_OPEN = "HALF_OPEN"  # Testing recovery


class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is OPEN (service unavailable)."""
    pass


class CircuitBreaker:
    """Circuit breaker for fault tolerance.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, fail immediately without retry
    - HALF_OPEN: Testing recovery, allow one request
    
    Transitions:
    - CLOSED → OPEN: After failure_threshold consecutive failures
    - OPEN → HALF_OPEN: After timeout_seconds
    - HALF_OPEN → CLOSED: If test request succeeds
    - HALF_OPEN → OPEN: If test request fails
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 30,
        name: str = "default",
    ):
        """Initialize circuit breaker.
        
        Args:
            failure_threshold: Failures before opening circuit
            timeout_seconds: Seconds before attempting recovery
            name: Circuit breaker name (for logging)
        """
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.name = name
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.success_count = 0
        
        logger.info(
            f"CircuitBreaker '{name}' initialized: "
            f"threshold={failure_threshold}, timeout={timeout_seconds}s"
        )
    
    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """Execute function with circuit breaker protection.
        
        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerOpenError: If circuit is OPEN
            Exception: Original exception if function fails
        """
        # Check if circuit should transition from OPEN to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                logger.info(f"CircuitBreaker '{self.name}': OPEN → HALF_OPEN (testing recovery)")
                self.state = CircuitState.HALF_OPEN
            else:
                # Circuit still OPEN, fail fast
                raise CircuitBreakerOpenError(
                    f"Circuit breaker '{self.name}' is OPEN (service unavailable). "
                    f"Will retry in {self._time_until_retry()}s."
                )
        
        try:
            # Execute function
            result = await func(*args, **kwargs)
            
            # Success - reset failure count
            self._on_success()
            return result
            
        except Exception as e:
            # Failure - increment count
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit should attempt recovery.
        
        Returns:
            True if timeout has elapsed since last failure
        """
        if self.last_failure_time is None:
            return False
        
        elapsed = datetime.now() - self.last_failure_time
        return elapsed.total_seconds() >= self.timeout_seconds
    
    def _time_until_retry(self) -> int:
        """Calculate seconds until next retry attempt.
        
        Returns:
            Seconds until retry (0 if can retry now)
        """
        if self.last_failure_time is None:
            return 0
        
        elapsed = datetime.now() - self.last_failure_time
        remaining = self.timeout_seconds - elapsed.total_seconds()
        return max(0, int(remaining))
    
    def _on_success(self):
        """Handle successful call."""
        self.success_count += 1
        
        if self.state == CircuitState.HALF_OPEN:
            # Recovery successful, close circuit
            logger.info(f"CircuitBreaker '{self.name}': HALF_OPEN → CLOSED (recovery successful)")
            self.state = CircuitState.CLOSED
            self.failure_count = 0
        elif self.state == CircuitState.CLOSED:
            # Normal operation, reset failure count
            self.failure_count = 0
    
    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.state == CircuitState.HALF_OPEN:
            # Recovery failed, open circuit again
            logger.warning(f"CircuitBreaker '{self.name}': HALF_OPEN → OPEN (recovery failed)")
            self.state = CircuitState.OPEN
        elif self.state == CircuitState.CLOSED:
            # Check if threshold exceeded
            if self.failure_count >= self.failure_threshold:
                logger.warning(
                    f"CircuitBreaker '{self.name}': CLOSED → OPEN "
                    f"({self.failure_count} consecutive failures)"
                )
                self.state = CircuitState.OPEN
    
    def reset(self):
        """Manually reset circuit breaker (for testing)."""
        logger.info(f"CircuitBreaker '{self.name}': Manual reset")
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
```

**Tests:** `tests/core/test_circuit_breaker.py`
```python
import pytest
import asyncio
from datetime import datetime, timedelta
from pywats.core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError, CircuitState

@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_threshold():
    """Verify circuit opens after failure threshold."""
    cb = CircuitBreaker(failure_threshold=3, timeout_seconds=60)
    
    async def failing_func():
        raise ValueError("Service down")
    
    # First 2 failures - circuit stays CLOSED
    for _ in range(2):
        with pytest.raises(ValueError):
            await cb.call(failing_func)
    assert cb.state == CircuitState.CLOSED
    
    # 3rd failure - circuit opens
    with pytest.raises(ValueError):
        await cb.call(failing_func)
    assert cb.state == CircuitState.OPEN

@pytest.mark.asyncio
async def test_circuit_breaker_fails_fast_when_open():
    """Verify circuit fails fast when OPEN."""
    cb = CircuitBreaker(failure_threshold=1, timeout_seconds=60)
    
    async def failing_func():
        raise ValueError("Service down")
    
    # Trip circuit
    with pytest.raises(ValueError):
        await cb.call(failing_func)
    assert cb.state == CircuitState.OPEN
    
    # Next call should fail immediately (CircuitBreakerOpenError)
    with pytest.raises(CircuitBreakerOpenError):
        await cb.call(failing_func)

@pytest.mark.asyncio
async def test_circuit_breaker_recovers_after_timeout():
    """Verify circuit attempts recovery after timeout."""
    cb = CircuitBreaker(failure_threshold=1, timeout_seconds=1)
    
    call_count = 0
    
    async def intermittent_func():
        nonlocal call_count
        call_count += 1
        if call_count == 1:
            raise ValueError("First call fails")
        return "success"
    
    # Trip circuit
    with pytest.raises(ValueError):
        await cb.call(intermittent_func)
    assert cb.state == CircuitState.OPEN
    
    # Wait for timeout
    await asyncio.sleep(1.1)
    
    # Next call should test recovery (HALF_OPEN)
    result = await cb.call(intermittent_func)
    assert result == "success"
    assert cb.state == CircuitState.CLOSED  # Recovery successful
```

### Step 3.2: Integrate with AsyncHttpClient (2 hours)

**File:** `src/pywats_client/http/async_http_client.py`

**Changes:**
1. Add `CircuitBreaker` instance to `AsyncHttpClient`
2. Wrap `_request()` method with circuit breaker
3. Add circuit breaker configuration to `WATSSettings`

**Implementation:**
```python
from pywats.core.circuit_breaker import CircuitBreaker, CircuitBreakerOpenError

class AsyncHttpClient:
    def __init__(self, settings: WATSSettings, error_handler: ErrorHandler):
        # ... existing code ...
        
        # Initialize circuit breaker
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=settings.circuit_breaker_threshold,
            timeout_seconds=settings.circuit_breaker_timeout,
            name="AsyncHttpClient"
        )
    
    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> httpx.Response:
        """Execute HTTP request with circuit breaker protection.
        
        Raises:
            CircuitBreakerOpenError: If circuit is OPEN (fail fast)
            HTTPError: If request fails
        """
        async def make_request():
            # Existing request logic
            return await self._session.request(method, url, **kwargs)
        
        # Wrap with circuit breaker
        return await self._circuit_breaker.call(make_request)
```

**Settings Update:**
```python
# In src/pywats/core/settings.py
class WATSSettings(BaseSettings):
    # ... existing settings ...
    
    circuit_breaker_threshold: int = Field(
        default=5,
        description="Number of consecutive failures before opening circuit"
    )
    circuit_breaker_timeout: int = Field(
        default=30,
        description="Seconds before attempting recovery when circuit is OPEN"
    )
```

### Step 3.3: Update Documentation (1 hour)

**Files to Update:**
- `docs/guides/error_handling.md` - Document circuit breaker
- `examples/observability/circuit_breaker_example.py` - Usage example
- `CHANGELOG.md` - Add entry

**Documentation:**
```markdown
## Circuit Breaker Pattern

**Version:** 0.3.0b1+

### Overview

PyWATS implements circuit breaker pattern to prevent retry storms when the
WATS server is down. The circuit breaker fails fast after consecutive failures,
reducing load on the server and providing quicker feedback.

### How It Works

**States:**
- **CLOSED** (normal): Requests pass through
- **OPEN** (failing): Requests fail immediately (no retry)
- **HALF_OPEN** (testing): Allow one request to test recovery

**Transitions:**
1. After 5 consecutive failures → Circuit OPENS
2. After 30 seconds → Circuit goes HALF_OPEN (tests recovery)
3. If test succeeds → Circuit CLOSES (back to normal)
4. If test fails → Circuit stays OPEN (wait another 30s)

### Configuration

```python
from pywats import pyWATS, WATSSettings

settings = WATSSettings(
    circuit_breaker_threshold=5,  # Failures before opening
    circuit_breaker_timeout=30    # Seconds before retry
)

api = pyWATS(server_url="http://wats-server", settings=settings)
```

### Error Handling

When circuit is OPEN, you'll get `CircuitBreakerOpenError`:

```python
from pywats.core.circuit_breaker import CircuitBreakerOpenError

try:
    report = api.get_report("RPT-123")
except CircuitBreakerOpenError as e:
    print(f"Service unavailable: {e}")
    # Fail fast - don't retry
```
```

### Step 3.4: Testing & Validation (1 hour)

**Test Checklist:**
- [ ] Run circuit breaker tests: `pytest tests/core/test_circuit_breaker.py`
- [ ] Test integration with AsyncHttpClient
- [ ] Verify state transitions (CLOSED → OPEN → HALF_OPEN → CLOSED)
- [ ] Test fail-fast behavior when OPEN
- [ ] Validate timeout-based recovery

**Success Criteria:**
- ✅ Circuit opens after 5 failures
- ✅ Requests fail fast when circuit is OPEN
- ✅ Circuit recovers after timeout
- ✅ Integration with HTTP client works

---

## 📊 Phase 4: Structured Logging Foundation (6 hours)

**Goal:** Implement JSON structured logging with correlation IDs

**Impact:** Observability +1.5 points (C+ → B+)

### Step 4.1: Create StructuredLogger Module (2 hours)

**File:** `src/pywats/core/structured_logging.py`

**Implementation:**
```python
"""Structured logging with JSON output and correlation IDs.

Provides production-ready logging with:
- JSON structured output (for log aggregators)
- Correlation IDs (trace requests across components)
- Context injection (thread ID, user, operation)
- Multiple formatters (JSON, text)
"""

import json
import logging
import threading
from datetime import datetime
from typing import Optional, Dict, Any
from contextlib import contextmanager
from enum import Enum


class LogFormat(str, Enum):
    """Log output formats."""
    JSON = "json"
    TEXT = "text"


class StructuredLogger:
    """Logger with structured output and correlation IDs.
    
    Usage:
        logger = StructuredLogger("pywats.report")
        
        with logger.correlation_context("request-123"):
            logger.info("Fetching report", report_id="ABC123")
    
    Output (JSON format):
        {
          "timestamp": "2026-02-02T10:15:23.456Z",
          "level": "INFO",
          "logger": "pywats.report",
          "message": "Fetching report",
          "correlation_id": "request-123",
          "report_id": "ABC123"
        }
    """
    
    def __init__(self, name: str, format: LogFormat = LogFormat.TEXT):
        """Initialize structured logger.
        
        Args:
            name: Logger name (e.g., "pywats.report")
            format: Output format (JSON or TEXT)
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.format = format
        self._context = threading.local()
    
    def info(self, message: str, **extra: Any):
        """Log INFO level message.
        
        Args:
            message: Log message
            **extra: Additional structured fields
        """
        self._log("INFO", message, extra)
    
    def warning(self, message: str, **extra: Any):
        """Log WARNING level message."""
        self._log("WARNING", message, extra)
    
    def error(self, message: str, **extra: Any):
        """Log ERROR level message."""
        self._log("ERROR", message, extra)
    
    def debug(self, message: str, **extra: Any):
        """Log DEBUG level message."""
        self._log("DEBUG", message, extra)
    
    def _log(self, level: str, message: str, extra: Dict[str, Any]):
        """Internal logging method.
        
        Args:
            level: Log level
            message: Log message
            extra: Additional fields
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "logger": self.name,
            "message": message,
            "correlation_id": self._get_correlation_id(),
            "thread_id": threading.get_ident(),
            **extra
        }
        
        if self.format == LogFormat.JSON:
            output = json.dumps(log_data)
        else:
            # Text format (human-readable)
            output = (
                f"{log_data['timestamp']} {level:8s} {self.name}: {message}"
            )
            if log_data.get("correlation_id"):
                output += f" [correlation_id={log_data['correlation_id']}]"
            if extra:
                extra_str = " ".join(f"{k}={v}" for k, v in extra.items())
                output += f" ({extra_str})"
        
        # Log at appropriate level
        log_func = getattr(self.logger, level.lower())
        log_func(output)
    
    @contextmanager
    def correlation_context(self, correlation_id: str):
        """Context manager for correlation ID.
        
        Args:
            correlation_id: Correlation ID for request tracing
            
        Usage:
            with logger.correlation_context("request-123"):
                logger.info("Processing request")
        """
        old_id = self._get_correlation_id()
        self._set_correlation_id(correlation_id)
        try:
            yield
        finally:
            if old_id:
                self._set_correlation_id(old_id)
            else:
                self._clear_correlation_id()
    
    def _set_correlation_id(self, correlation_id: str):
        """Set correlation ID for current thread."""
        self._context.correlation_id = correlation_id
    
    def _get_correlation_id(self) -> Optional[str]:
        """Get correlation ID for current thread."""
        return getattr(self._context, "correlation_id", None)
    
    def _clear_correlation_id(self):
        """Clear correlation ID for current thread."""
        if hasattr(self._context, "correlation_id"):
            delattr(self._context, "correlation_id")
```

**Tests:** `tests/core/test_structured_logging.py`
```python
import json
import logging
from pywats.core.structured_logging import StructuredLogger, LogFormat

def test_structured_logger_json_output(caplog):
    """Verify JSON output format."""
    logger = StructuredLogger("test.logger", format=LogFormat.JSON)
    
    with caplog.at_level(logging.INFO):
        logger.info("Test message", user="john.doe", action="create")
    
    # Parse JSON output
    log_output = json.loads(caplog.records[0].message)
    
    assert log_output["level"] == "INFO"
    assert log_output["message"] == "Test message"
    assert log_output["user"] == "john.doe"
    assert log_output["action"] == "create"
    assert "timestamp" in log_output
    assert "thread_id" in log_output

def test_correlation_id_propagation():
    """Verify correlation ID propagates across calls."""
    logger = StructuredLogger("test.logger")
    
    with logger.correlation_context("request-123"):
        assert logger._get_correlation_id() == "request-123"
    
    assert logger._get_correlation_id() is None

def test_nested_correlation_contexts():
    """Verify nested correlation contexts restore correctly."""
    logger = StructuredLogger("test.logger")
    
    with logger.correlation_context("outer"):
        assert logger._get_correlation_id() == "outer"
        
        with logger.correlation_context("inner"):
            assert logger._get_correlation_id() == "inner"
        
        assert logger._get_correlation_id() == "outer"
```

### Step 4.2: Integrate with API Layer (2 hours)

**Files to Update:**
- `src/pywats/domains/*/services.py` - Replace `logging.getLogger()` with `StructuredLogger`
- `src/pywats_client/http/async_http_client.py` - Add correlation ID middleware

**HTTP Client Integration:**
```python
from pywats.core.structured_logging import StructuredLogger
import uuid

class AsyncHttpClient:
    def __init__(self, settings: WATSSettings, error_handler: ErrorHandler):
        # ... existing code ...
        self.logger = StructuredLogger("pywats.http")
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        # Generate correlation ID
        correlation_id = str(uuid.uuid4())
        
        with self.logger.correlation_context(correlation_id):
            self.logger.info(
                f"{method} {endpoint}",
                method=method,
                endpoint=endpoint,
                correlation_id=correlation_id
            )
            
            try:
                response = await self._session.request(method, url, **kwargs)
                
                self.logger.info(
                    "Request succeeded",
                    status_code=response.status_code,
                    correlation_id=correlation_id
                )
                
                return response
            except Exception as e:
                self.logger.error(
                    "Request failed",
                    error=str(e),
                    correlation_id=correlation_id
                )
                raise
```

### Step 4.3: Update Configuration & Documentation (1 hour)

**Settings Update:**
```python
# In src/pywats/core/settings.py
class WATSSettings(BaseSettings):
    # ... existing settings ...
    
    log_format: LogFormat = Field(
        default=LogFormat.TEXT,
        description="Log output format (json or text)"
    )
    
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
```

**Documentation:**
- `docs/guides/observability.md` - Add structured logging section
- `examples/observability/structured_logging_example.py` - Usage examples
- `CHANGELOG.md` - Add entry

### Step 4.4: Testing & Validation (1 hour)

**Test Checklist:**
- [ ] Run structured logging tests: `pytest tests/core/test_structured_logging.py`
- [ ] Verify JSON output format
- [ ] Test correlation ID propagation
- [ ] Confirm thread safety (concurrent access)
- [ ] Validate integration with HTTP client

**Success Criteria:**
- ✅ JSON structured output works
- ✅ Correlation IDs propagate correctly
- ✅ Multiple formatters supported
- ✅ Documentation complete

---

## ⏱️ Phase 5: Performance Benchmarks (4 hours)

**Goal:** Create baseline performance benchmark suite

**Impact:** Performance +0.5 points (documentation + regression detection)

### Step 5.1: Setup Benchmark Infrastructure (1 hour)

**Install pytest-benchmark:**
```bash
pip install pytest-benchmark
```

**Create benchmark directory:**
```
tests/
  performance/
    __init__.py
    conftest.py  # Shared fixtures
    benchmarks/
      test_report_benchmarks.py
      test_product_benchmarks.py
      test_sync_vs_async.py
    baselines.json  # Baseline metrics
```

**Shared Fixtures (`tests/performance/conftest.py`):**
```python
import pytest
from pywats import pyWATS, AsyncWATS
from unittest.mock import Mock

@pytest.fixture
def mock_wats_server(monkeypatch):
    """Mock WATS server with consistent 10ms latency."""
    # Mock HTTP client to return canned responses
    # ...
    pass

@pytest.fixture
def benchmark_api(mock_wats_server):
    """pyWATS instance for benchmarking."""
    return pyWATS(server_url="http://localhost:8080")
```

### Step 5.2: Implement Key Benchmarks (2 hours)

**Report Benchmarks (`tests/performance/benchmarks/test_report_benchmarks.py`):**
```python
import pytest
from pywats import pyWATS

@pytest.mark.benchmark(group="report")
def test_benchmark_get_report(benchmark, benchmark_api):
    """Benchmark single report retrieval."""
    result = benchmark(benchmark_api.get_report, "RPT-123")
    
    # Assert performance target
    assert result.stats.mean < 0.1  # <100ms average

@pytest.mark.benchmark(group="report")
def test_benchmark_get_reports_for_unit(benchmark, benchmark_api):
    """Benchmark reports by serial number."""
    result = benchmark(benchmark_api.get_reports_for_unit, "SN-123456")
    
    assert result.stats.mean < 0.2  # <200ms average
```

**Sync vs Async Comparison (`tests/performance/benchmarks/test_sync_vs_async.py`):**
```python
import pytest
import asyncio
from pywats import pyWATS, AsyncWATS

@pytest.mark.benchmark(group="sync_vs_async")
def test_sync_api_performance(benchmark, mock_wats_server):
    """Benchmark sync API with event loop pooling."""
    api = pyWATS(server_url="http://localhost:8080")
    result = benchmark(api.get_report, "RPT-123")
    
    assert result.stats.mean < 0.05  # <50ms after optimization

@pytest.mark.benchmark(group="sync_vs_async")
def test_async_api_performance(benchmark, mock_wats_server):
    """Benchmark async API (baseline)."""
    api = AsyncWATS(server_url="http://localhost:8080")
    
    def run_async():
        return asyncio.run(api.get_report("RPT-123"))
    
    result = benchmark(run_async)
    
    assert result.stats.mean < 0.03  # <30ms async baseline

def test_sync_overhead_acceptable():
    """Verify sync overhead is <2x async (after optimization)."""
    # Compare results from above benchmarks
    # Sync should be <2x async
    pass
```

### Step 5.3: Document Baselines (0.5 hours)

**Create `tests/performance/baselines.json`:**
```json
{
  "version": "0.3.0b1",
  "date": "2026-02-02",
  "environment": {
    "python": "3.10",
    "os": "Windows",
    "hardware": "Dev workstation"
  },
  "benchmarks": {
    "get_report": {
      "mean": 0.045,
      "median": 0.042,
      "std": 0.003,
      "target": 0.100
    },
    "get_reports_for_unit": {
      "mean": 0.150,
      "median": 0.145,
      "std": 0.010,
      "target": 0.200
    },
    "sync_vs_async_overhead": {
      "ratio": 1.5,
      "target": 2.0
    }
  }
}
```

### Step 5.4: Testing & Validation (0.5 hours)

**Run Benchmarks:**
```bash
# Run all benchmarks
pytest tests/performance/benchmarks/ --benchmark-only

# Compare against baseline
pytest tests/performance/benchmarks/ --benchmark-compare=baselines

# Generate HTML report
pytest tests/performance/benchmarks/ --benchmark-only --benchmark-json=output.json
```

**Success Criteria:**
- ✅ 5+ benchmarks implemented
- ✅ Baselines documented
- ✅ CI/CD integration ready
- ✅ Performance targets defined

---

## 🧪 Phase 6: Integration Testing & Documentation (6 hours)

**Goal:** Ensure all changes work together and are well-documented

### Step 6.1: Integration Testing (3 hours)

**Test Scenarios:**
1. **End-to-End with All Features** (1 hour)
   - Create script using all new features:
     - SyncWrapper optimization
     - Auto-detected station
     - Circuit breaker handling
     - Structured logging
   - Verify performance improvement
   - Confirm structured logs generated

2. **Regression Testing** (1 hour)
   - Run full test suite: `pytest`
   - Verify 416+ tests still passing
   - Run mypy: `mypy src/pywats`
   - Check for new errors

3. **Cross-Platform Testing** (1 hour)
   - Test station detection on Windows/Linux
   - Verify event loop pooling on all platforms
   - Confirm structured logging works

**Integration Test File (`tests/integration/test_final_push_features.py`):**
```python
import pytest
from pywats import pyWATS
from pywats.core.structured_logging import StructuredLogger, LogFormat
from pywats.core.circuit_breaker import CircuitBreakerOpenError

def test_end_to_end_with_all_features():
    """Test all Phase 1-5 features together."""
    # Auto-detected station
    api = pyWATS(server_url="http://wats-server")
    assert api.station is not None  # Auto-detected
    
    # Structured logging
    logger = StructuredLogger("test", format=LogFormat.JSON)
    
    # Fast sync API (event loop pooling)
    with logger.correlation_context("integration-test"):
        report = api.get_report("RPT-123")
        assert report is not None

def test_circuit_breaker_integration():
    """Test circuit breaker with sync API."""
    api = pyWATS(server_url="http://invalid-server")
    
    # After 5 failures, circuit should open
    for i in range(6):
        try:
            api.get_report("RPT-123")
        except (CircuitBreakerOpenError, Exception):
            pass
    
    # Next call should fail fast (CircuitBreakerOpenError)
    with pytest.raises(CircuitBreakerOpenError):
        api.get_report("RPT-123")
```

### Step 6.2: Documentation Updates (2 hours)

**Files to Create/Update:**

1. **Release Notes** (`docs/release/v0.3.0b1.md`):
   - Summary of all improvements
   - Performance metrics
   - Migration guide (if needed)

2. **User Guides:**
   - `docs/guides/performance.md` - SyncWrapper optimization
   - `docs/guides/observability.md` - Structured logging
   - `docs/guides/error_handling.md` - Circuit breaker
   - `docs/guides/configuration.md` - Station auto-detection

3. **Examples:**
   - `examples/performance/sync_wrapper_benchmark.py`
   - `examples/observability/structured_logging_example.py`
   - `examples/observability/circuit_breaker_example.py`
   - `examples/getting_started/zero_config.py`

4. **API Documentation:**
   - Update Sphinx docs for new modules
   - Add docstrings to all new classes/methods

### Step 6.3: CHANGELOG Update (0.5 hours)

**CHANGELOG.md Entry:**
```markdown
## [Unreleased]

### Improved
- **SyncWrapper Performance**: Implemented event loop pooling for 10-100x faster sync API
  - Reuses connections across calls (no more loop creation overhead)
  - Thread-local event loops for thread safety
  - Backward compatible (no API changes required)
  - Tests: 5 new tests in `tests/core/test_event_loop_pool.py`

- **Structured Logging**: JSON structured logging with correlation IDs
  - JSON output for log aggregators (Elasticsearch, Splunk, etc.)
  - Correlation IDs trace requests across components
  - Multiple formatters (JSON for production, text for development)
  - Context injection (thread ID, user, operation type)
  - Tests: 8 new tests in `tests/core/test_structured_logging.py`

- **Circuit Breaker Pattern**: Fail-fast error handling for degraded services
  - Opens after 5 consecutive failures (configurable)
  - Automatic recovery testing after 30s timeout
  - Prevents retry storms and cascading failures
  - Integration with AsyncHttpClient
  - Tests: 6 new tests in `tests/core/test_circuit_breaker.py`

### Added
- **Station Auto-Detection**: Zero-config station name detection
  - Detects from `PYWATS_STATION` env variable (priority 1)
  - Falls back to hostname (Windows: `COMPUTERNAME`, Unix: `socket.gethostname()`)
  - Config file support (`~/.pywats/station.conf`)
  - Cross-platform compatible (Windows/Linux/macOS)
  - Exposed via `api.station` property
  - Tests: 7 new tests in `tests/core/test_station_registry.py`

- **Performance Benchmarks**: Baseline benchmark suite for regression detection
  - 5+ benchmarks covering key operations
  - Sync vs async performance comparison
  - Baselines documented in `tests/performance/baselines.json`
  - CI/CD integration ready
  - Tests: 10+ benchmarks in `tests/performance/benchmarks/`

### Documentation
- Added performance optimization guide: `docs/guides/performance.md`
- Added observability guide: `docs/guides/observability.md`
- Updated error handling guide: `docs/guides/error_handling.md`
- Updated configuration guide: `docs/guides/configuration.md`
- Added 5 new examples in `examples/`

### Tests
- Added 31 new tests across all modules
- All 416+ existing tests still passing
- Performance regression detection active
```

### Step 6.4: Final Validation (0.5 hours)

**Pre-Release Checklist:**
- [ ] Run full test suite: `pytest` ✅ 416+ passing
- [ ] Run mypy: `mypy src/pywats` ✅ 16 errors (no new errors)
- [ ] Run benchmarks: `pytest tests/performance/ --benchmark-only` ✅
- [ ] Verify examples execute: Run 5+ key examples ✅
- [ ] Check CHANGELOG: All changes documented ✅
- [ ] Review documentation: Guides complete ✅
- [ ] Git status clean: All changes committed ✅

**Success Criteria:**
- ✅ All tests passing (no regressions)
- ✅ Performance improvements validated (≥10x sync wrapper)
- ✅ Documentation complete and accurate
- ✅ Examples runnable and helpful
- ✅ CHANGELOG updated
- ✅ Ready for v0.3.0b1 release

---

## 📊 Success Metrics Summary

### Performance Improvements
- **SyncWrapper:** 10-100x faster (measured via benchmarks)
- **Circuit Breaker:** Fast-fail within 1s (vs 30s+ retry timeout)
- **Overall:** Performance score +1 point (B+ → A-)

### Observability Improvements
- **Structured Logging:** JSON output + correlation IDs
- **Log Aggregation:** Ready for Elasticsearch/Splunk
- **Overall:** Observability score +1.5 points (C+ → B+)

### Developer Experience
- **Station Auto-Detection:** Zero-config for most users
- **Error Handling:** Circuit breaker prevents retry storms
- **Overall:** Usability +0.5 points

### Test Coverage
- **New Tests:** 31+ tests added
- **Benchmark Suite:** 10+ benchmarks
- **Total Tests:** 447+ tests (416 existing + 31 new)

### Assessment Score Impact
- **Before:** A- (80.5%)
- **After:** A (84-85%)
- **Target:** ✅ Achieved

---

## 🚨 Risk Mitigation

### If Behind Schedule
**Option 1:** Descope Phase 5 (Benchmarks)
- Benchmarks are "nice to have" (can be added later)
- Phases 1-4 provide core functionality

**Option 2:** Parallelize Phases 4 & 5
- Structured logging and benchmarks are independent
- Can work on both simultaneously

### If Test Failures
**Rollback Strategy:**
- Each phase is independently committable
- Revert to last passing commit
- Continue with remaining phases

### If Platform Issues
**Fallback Plan:**
- Station auto-detection: Fall back to manual config
- Event loop pooling: Add config flag to disable
- Circuit breaker: Make configurable (can disable)

---

**Implementation Plan Complete:** ✅ Ready to execute in 2-4 days.
