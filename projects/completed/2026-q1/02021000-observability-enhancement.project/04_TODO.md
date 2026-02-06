# Observability Enhancement - TODO

**Project:** Observability Enhancement  
**Status:** 🔄 Active  
**Last Updated:** 2026-02-02

---

## Sprint 1: Prometheus Metrics Foundation ✅ COMPLETE

### Core Metrics Module ✅
- ✅ Created `src/pywats/core/metrics.py` (396 lines)
  - ✅ MetricsCollector class
  - ✅ Counter, Gauge, Histogram wrappers
  - ✅ @track_request_metrics decorator
  - ✅ HTTP, system, queue, converter metrics

### Metrics Endpoint ✅
- ✅ Enhanced `src/pywats_client/service/health_server.py`
  - ✅ GET /metrics endpoint
  - ✅ Prometheus text format support
  - ✅ JSON fallback for cache/queue stats

### HTTP Client Instrumentation ✅
- ✅ Modified `src/pywats/core/client.py`
  - ✅ Added metrics_collector parameter
  - ✅ Track request duration, status codes, method, endpoint

---

## Sprint 2: Integration ✅ COMPLETE

- ✅ /metrics endpoint in health_server.py
- ✅ HTTP cache statistics exposed

---

## Sprint 3: Service Integration & Production (CURRENT)

### AsyncClientService Integration ✅ COMPLETE
- ✅ Create MetricsCollector in `async_client_service.py`
  - ✅ Add _metrics_collector instance variable
  - ✅ Initialize in _initialize_api if config.enable_metrics
  - ✅ Pass cache params to AsyncWATS when creating API client
  - ✅ Wire to health_server for /metrics endpoint

### Component Wiring ✅ COMPLETE
- ✅ Wire components to HealthServer in _start_health_server
  - ✅ Set health_server._metrics_collector (if enabled)
  - ✅ Set health_server._http_client (for cache stats)
  - ✅ Set health_server._converter_pool (for queue stats)
  - ✅ Added debug logging for each wired component

### Configuration ✅ COMPLETE
- ✅ Add metrics config to `config.py`
  - ✅ enable_metrics: bool = True
  - ✅ metrics_port: int = 9090
  - ✅ Also added cache config (enable_cache, cache_ttl_seconds, cache_max_size)

### Testing & Validation (Optional)
- [ ] Integration tests for /metrics endpoint
- [ ] Load testing (measure overhead)

### Documentation ✅ COMPLETE
- ✅ Create `docs/guides/observability.md`
  - ✅ Prometheus scraping setup with example prometheus.yml
  - ✅ Grafana dashboard examples (HTTP, cache, queue panels)
  - ✅ Kubernetes health check configuration
  - ✅ Common Prometheus queries (request rate, latency, cache hit rate)
  - ✅ Troubleshooting guide
  - ✅ Best practices for production deployment
  - ✅ 600+ lines comprehensive guide

---

## Sprint 2: Correlation IDs (DEFERRED)
- [ ] Update `pyproject.toml`
  - [ ] Add prometheus-client>=0.19.0
  - [ ] Add psutil>=5.9.0
  - [ ] Add as optional dependencies [observability]

### Testing (Sprint 1)
- [ ] Create `tests/core/test_metrics.py`
  - [ ] Test counter increments
  - [ ] Test histogram observations
  - [ ] Test gauge updates
  - [ ] Test decorator functionality
  - [ ] Test thread safety
- [ ] Create `tests/integration/test_metrics_endpoint.py`
  - [ ] Test /metrics endpoint returns data
  - [ ] Test Prometheus format compliance
  - [ ] Test concurrent requests
  - [ ] Test server start/stop

---

## Sprint 2: Enhanced Observability (Week 2)

### Queue Metrics
- [ ] Modify queue files in `src/pywats_client/queue/`
  - [ ] Add queue depth gauge
  - [ ] Track processing time histogram
  - [ ] Monitor worker status
  - [ ] Track error rates
  - [ ] Add queue-specific labels
  - [ ] Write tests

### Converter Metrics
- [ ] Modify converter files in `src/pywats_client/converters/`
  - [ ] Track execution counter
  - [ ] Monitor duration histogram
  - [ ] Track success/failure rates
  - [ ] Add converter-specific labels
  - [ ] Write tests

### Correlation ID Standardization
- [ ] Audit all modules for correlation ID usage
  - [ ] Check API client modules
  - [ ] Check service modules
  - [ ] Check event handlers
  - [ ] Ensure propagation through event bus
  - [ ] Add missing correlation IDs
  - [ ] Document patterns
  - [ ] Write tests

### Health Check Enhancement
- [ ] Modify `src/pywats_client/service/health_server.py`
  - [ ] Add dependency health checks
  - [ ] Include version information
  - [ ] Add startup timestamp
  - [ ] Track health check metrics
  - [ ] Write tests

### Documentation
- [ ] Create `docs/guides/observability.md`
  - [ ] Metrics overview
  - [ ] Accessing metrics endpoint
  - [ ] Understanding metrics
  - [ ] Prometheus integration guide
  - [ ] Grafana dashboard examples
- [ ] Create `docs/development/metrics.md`
  - [ ] Adding new metrics
  - [ ] Using decorators
  - [ ] Best practices
  - [ ] Performance considerations
- [ ] Update README.md
  - [ ] Add observability section
  - [ ] Link to guides

### Examples
- [ ] Create `examples/observability/` directory
- [ ] Create `examples/observability/prometheus_monitoring.py`
  - [ ] Basic metrics server example
  - [ ] Client usage with metrics
  - [ ] Prometheus scrape config example
- [ ] Create `examples/observability/custom_metrics.py`
  - [ ] Adding custom metrics
  - [ ] Using decorators
  - [ ] Advanced patterns
- [ ] Create `examples/observability/grafana_dashboard.json`
  - [ ] Sample dashboard
  - [ ] Key metrics visualization

### Testing (Sprint 2)
- [ ] Performance testing
  - [ ] Measure metrics collection overhead
  - [ ] Verify <1% performance impact
  - [ ] Test memory usage
  - [ ] Test concurrent metric updates
- [ ] Integration testing
  - [ ] Test full observability stack
  - [ ] Test Prometheus scraping
  - [ ] Test health check integration
  - [ ] End-to-end scenarios

### Docker/Kubernetes
- [ ] Update `deployment/docker/Dockerfile` (if needed)
  - [ ] Expose metrics port (9090)
  - [ ] Add environment variables for metrics config
- [ ] Create Kubernetes examples (if applicable)
  - [ ] ServiceMonitor for Prometheus Operator
  - [ ] Prometheus annotations
  - [ ] Health/readiness probe configuration

---

## Code Review & Validation

### Pre-merge Checklist
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Performance tests show <1% overhead
- [ ] No breaking changes
- [ ] Documentation complete
- [ ] Examples working
- [ ] Code review completed
- [ ] Security scan passed

### Validation Criteria
- [ ] `/metrics` endpoint returns Prometheus format
- [ ] All HTTP requests tracked with latency/status
- [ ] System resources monitored
- [ ] Queue depth and processing metrics available
- [ ] Correlation IDs used consistently
- [ ] Health checks enhanced
- [ ] Documentation accurate and complete

---

## Post-Implementation

### Follow-up Tasks
- [ ] Create Grafana dashboard templates
- [ ] Add alerting rule examples
- [ ] Create runbook for common issues
- [ ] Training documentation for ops team

### Future Enhancements (Out of Scope)
- [ ] OpenTelemetry distributed tracing
- [ ] Log aggregation integration
- [ ] APM integration (DataDog, New Relic)
- [ ] Custom exporters
- [ ] Advanced metrics (percentiles, histograms)

---

## Notes

### Important Considerations
1. All metrics features must be opt-in (backward compatible)
2. Performance overhead must stay <1%
3. Must work in both GUI and service modes
4. Must be Docker/Kubernetes compatible
5. Library-friendly design (no forced configuration)

### Resources
- Prometheus Python Client: https://github.com/prometheus/client_python
- psutil: https://psutil.readthedocs.io/
- OpenTelemetry (future): https://opentelemetry.io/

---

**Created:** 2026-02-02  
**Last Updated:** 2026-02-02  
**Review Frequency:** Daily during active development
