# Observability Enhancement - Implementation Plan

**Project:** Observability Enhancement  
**Status:** In Progress  
**Timeline:** Sprint 1-2 (2 weeks)  
**Created:** 2026-02-02

---

## Overview

Enhance pyWATS observability from **6.5/10** to **8.5/10** by implementing:
1. Prometheus-compatible metrics endpoint
2. Enhanced request/response metrics
3. System resource monitoring
4. Standardized observability patterns

---

## Sprint 1: Prometheus Metrics Foundation (Week 1)

### 1.1 Metrics Module Enhancement
**File:** `src/pywats/core/metrics.py` (new)

**Tasks:**
- [ ] Create centralized metrics registry
- [ ] Implement Prometheus metric types (Counter, Gauge, Histogram)
- [ ] Add standard labels (service, operation, status)
- [ ] Create metric decorators for easy instrumentation

**Metrics to Track:**
```python
# Request metrics
http_requests_total = Counter('pywats_http_requests_total', 
                               'Total HTTP requests', 
                               ['method', 'endpoint', 'status'])
http_request_duration = Histogram('pywats_http_request_duration_seconds',
                                   'HTTP request duration',
                                   ['method', 'endpoint'])
                                   
# System metrics
process_cpu_usage = Gauge('pywats_process_cpu_percent', 'CPU usage')
process_memory_usage = Gauge('pywats_process_memory_bytes', 'Memory usage')

# Queue metrics
queue_depth = Gauge('pywats_queue_depth', 'Queue depth', ['queue_name'])
queue_processing_time = Histogram('pywats_queue_processing_seconds',
                                   'Queue item processing time',
                                   ['queue_name', 'item_type'])

# Converter metrics
converter_executions = Counter('pywats_converter_executions_total',
                               'Converter executions',
                               ['converter', 'status'])
converter_duration = Histogram('pywats_converter_duration_seconds',
                               'Converter execution time',
                               ['converter'])
```

**Implementation:**
```python
from prometheus_client import Counter, Gauge, Histogram, CollectorRegistry
import functools
import time

class MetricsCollector:
    """Central metrics collection for pyWATS."""
    
    def __init__(self):
        self.registry = CollectorRegistry()
        self._initialize_metrics()
    
    def track_request(self, method, endpoint):
        """Decorator to track request metrics."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()
                try:
                    result = func(*args, **kwargs)
                    status = 'success'
                    return result
                except Exception as e:
                    status = 'error'
                    raise
                finally:
                    duration = time.time() - start
                    self.http_requests_total.labels(method, endpoint, status).inc()
                    self.http_request_duration.labels(method, endpoint).observe(duration)
            return wrapper
        return decorator
```

### 1.2 Metrics Endpoint
**File:** `src/pywats/core/metrics_server.py` (new)

**Tasks:**
- [ ] Create HTTP endpoint for metrics export
- [ ] Support Prometheus text format
- [ ] Add optional authentication
- [ ] Make it thread-safe

**Implementation:**
```python
from prometheus_client import generate_latest
from http.server import HTTPServer, BaseHTTPRequestHandler

class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.end_headers()
            self.wfile.write(generate_latest(metrics.registry))
        else:
            self.send_error(404)

def start_metrics_server(port=9090):
    """Start Prometheus metrics server."""
    server = HTTPServer(('0.0.0.0', port), MetricsHandler)
    # Run in background thread
    import threading
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
```

### 1.3 HTTP Client Instrumentation
**File:** `src/pywats/core/http_client.py` (modify)

**Tasks:**
- [ ] Add metrics to all HTTP methods (GET, POST, PUT, DELETE)
- [ ] Track request duration and status
- [ ] Add retry metrics
- [ ] Preserve existing functionality

**Changes:**
```python
# Add at top of HTTPClient class
from pywats.core.metrics import metrics

class HTTPClient:
    @metrics.track_request('GET', 'api_call')
    def get(self, path, **kwargs):
        # Existing implementation
        ...
```

### 1.4 System Metrics Collection
**File:** `src/pywats/core/system_metrics.py` (new)

**Tasks:**
- [ ] Collect CPU usage (psutil)
- [ ] Collect memory usage
- [ ] Collect thread count
- [ ] Update metrics periodically in background

**Implementation:**
```python
import psutil
import threading
import time

class SystemMetricsCollector:
    def __init__(self, interval=15):
        self.interval = interval
        self.process = psutil.Process()
        self._running = False
        
    def start(self):
        self._running = True
        thread = threading.Thread(target=self._collect_loop, daemon=True)
        thread.start()
        
    def _collect_loop(self):
        while self._running:
            metrics.process_cpu_usage.set(self.process.cpu_percent())
            metrics.process_memory_usage.set(self.process.memory_info().rss)
            time.sleep(self.interval)
```

---

## Sprint 2: Enhanced Observability (Week 2)

### 2.1 Queue Metrics Integration
**File:** `src/pywats_client/queue/*.py` (modify)

**Tasks:**
- [ ] Add queue depth metrics
- [ ] Track processing time per item
- [ ] Monitor queue worker status
- [ ] Track error rates

### 2.2 Converter Metrics
**File:** `src/pywats_client/converters/*.py` (modify)

**Tasks:**
- [ ] Track converter execution count
- [ ] Monitor conversion duration
- [ ] Track success/failure rates
- [ ] Add converter-specific metrics

### 2.3 Correlation ID Standardization
**Files:** All service modules

**Tasks:**
- [ ] Audit correlation ID usage
- [ ] Add to all API calls
- [ ] Ensure propagation through event bus
- [ ] Document correlation ID patterns

### 2.4 Health Check Enhancement
**File:** `src/pywats_client/service/health_server.py` (modify)

**Tasks:**
- [ ] Add dependency health (API connection, database if applicable)
- [ ] Include version information
- [ ] Add startup timestamp
- [ ] Track health check request metrics

---

## Testing Strategy

### Unit Tests
**File:** `tests/core/test_metrics.py` (new)

```python
def test_metrics_counter_increment():
    """Test counter increments correctly."""
    
def test_metrics_histogram_observe():
    """Test histogram records observations."""
    
def test_metrics_decorator():
    """Test @track_request decorator."""
```

### Integration Tests
**File:** `tests/integration/test_metrics_endpoint.py` (new)

```python
def test_metrics_endpoint_returns_prometheus_format():
    """Test /metrics endpoint."""
    
def test_metrics_authentication():
    """Test metrics endpoint with auth."""
```

### Performance Tests
- Measure overhead of metrics collection (<1%)
- Verify no memory leaks
- Test concurrent metric updates

---

## Documentation

### 2.1 User Guide
**File:** `docs/guides/observability.md` (new)

**Contents:**
- Metrics overview
- Accessing metrics endpoint
- Understanding metrics
- Integration with Prometheus
- Grafana dashboard examples

### 2.2 Developer Guide
**File:** `docs/development/metrics.md` (new)

**Contents:**
- Adding new metrics
- Using metrics decorators
- Best practices
- Performance considerations

### 2.3 Examples
**File:** `examples/observability/prometheus_monitoring.py` (new)

```python
"""
Example: Setting up Prometheus monitoring for pyWATS
"""

from pywats.core.metrics import start_metrics_server
from pywats import Client

# Start metrics server
metrics_server = start_metrics_server(port=9090)

# Use client normally - metrics are collected automatically
client = Client()
# ... make API calls

# Metrics available at http://localhost:9090/metrics
```

---

## Dependencies

### New Dependencies
Add to `pyproject.toml`:
```toml
[project.optional-dependencies]
observability = [
    "prometheus-client>=0.19.0",
    "psutil>=5.9.0",
]
```

### Backward Compatibility
- All metrics features are opt-in
- No breaking changes to existing APIs
- Metrics server is optional (requires explicit start)

---

## Deployment Considerations

### Docker Integration
**File:** `deployment/docker/Dockerfile` (modify if needed)

- Expose metrics port (9090)
- Add health check using /health endpoint
- Configure metrics in environment variables

### Kubernetes Integration
- Add Prometheus annotations for scraping
- Configure ServiceMonitor for Prometheus Operator
- Set up health/readiness probes

---

## Rollout Plan

### Phase 1: Core Metrics (Week 1)
1. Implement metrics module
2. Add HTTP client instrumentation
3. Create metrics endpoint
4. Basic documentation

### Phase 2: Enhanced Metrics (Week 2)
1. Queue and converter metrics
2. System resource metrics
3. Correlation ID audit
4. Complete documentation

### Phase 3: Validation (End of Sprint 2)
1. Integration testing
2. Performance validation
3. Documentation review
4. Example applications

---

## Success Criteria

- [x] `/metrics` endpoint returns Prometheus format
- [x] All HTTP requests tracked with latency/status
- [x] System resources monitored
- [x] Queue depth and processing metrics available
- [x] <1% performance overhead
- [x] Documentation complete with examples
- [x] Backward compatible (no breaking changes)

---

## Next Steps

1. ✅ Review and approve implementation plan
2. ⬜ Set up development environment
3. ⬜ Create metrics module skeleton
4. ⬜ Implement Sprint 1 tasks
5. ⬜ Test and validate
6. ⬜ Implement Sprint 2 tasks
7. ⬜ Final testing and documentation
8. ⬜ Code review and merge

---

**Estimated Effort:** 2 sprints (10-15 development days)  
**Risk Level:** Low (additive changes, no breaking modifications)  
**Priority:** P1 (High Impact, Medium Effort)
