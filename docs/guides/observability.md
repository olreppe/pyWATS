# PyWATS Observability Guide

**Complete guide to monitoring, metrics, and observability in pyWATS**

Last Updated: February 2, 2026

---

## Table of Contents

1. [Overview](#overview)
2. [Metrics Collection](#metrics-collection)
3. [Health Endpoints](#health-endpoints)
4. [Prometheus Integration](#prometheus-integration)
5. [Grafana Dashboards](#grafana-dashboards)
6. [HTTP Cache Metrics](#http-cache-metrics)
7. [Queue Metrics](#queue-metrics)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)

---

## Overview

PyWATS provides comprehensive observability features for production monitoring:

- **Prometheus Metrics**: Counter, gauge, histogram, and summary metrics
- **Health Endpoints**: HTTP endpoints for container orchestration
- **Cache Statistics**: HTTP response cache performance metrics
- **Queue Metrics**: Converter queue depth and processing stats
- **Customizable**: Enable/disable metrics, configure ports, add custom metrics

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Application Layer                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
│  │ AsyncWATS    │  │ Converters   │  │ Queues    │ │
│  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ │
│         │                  │                 │       │
│         ▼                  ▼                 ▼       │
│  ┌─────────────────────────────────────────────┐   │
│  │         MetricsCollector                     │   │
│  │  (Prometheus client library)                 │   │
│  └─────────────────────┬───────────────────────┘   │
│                        │                             │
└────────────────────────┼─────────────────────────────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ HealthServer │
                  │ /metrics     │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ Prometheus   │
                  │ (scraper)    │
                  └──────────────┘
```

---

## Metrics Collection

### Enable Metrics

**Via Configuration File** (`config.json`):

```json
{
  "enable_metrics": true,
  "metrics_port": 9090
}
```

**Via Python API**:

```python
from pywats import AsyncWATS

# Metrics automatically enabled with default config
async with AsyncWATS(base_url="...", token="...") as api:
    # Metrics tracked automatically
    products = await api.product.get_products()
```

**Via Client Service**:

```python
from pywats_client.service import AsyncClientService

service = AsyncClientService(instance_id="default")
# Metrics enabled if config.enable_metrics=True
await service.run()
```

### Available Metrics

#### HTTP Request Metrics

```python
# Counter: Total HTTP requests
http_requests_total{method="GET", endpoint="/api/Product", status="200"}

# Histogram: Request duration
http_request_duration_seconds{method="GET", endpoint="/api/Product"}

# Gauge: Active requests
http_requests_active{method="GET", endpoint="/api/Product"}
```

#### Cache Metrics

```python
# Gauge: Cache size
cache_size_bytes{cache_name="http_response"}

# Counter: Cache hits
cache_hits_total{cache_name="http_response"}

# Counter: Cache misses
cache_misses_total{cache_name="http_response"}

# Counter: Cache evictions
cache_evictions_total{cache_name="http_response"}

# Gauge: Cache hit rate (0.0-1.0)
cache_hit_rate{cache_name="http_response"}
```

#### Queue Metrics

```python
# Gauge: Queue depth
queue_depth{queue_name="converter_queue"}

# Counter: Items processed
queue_items_processed_total{queue_name="converter_queue"}

# Histogram: Processing time
queue_processing_duration_seconds{queue_name="converter_queue"}

# Gauge: Active workers
queue_active_workers{queue_name="converter_queue"}
```

#### Converter Metrics

```python
# Counter: Conversions completed
conversions_total{converter="CSVConverter", status="success"}

# Histogram: Conversion duration
conversion_duration_seconds{converter="CSVConverter"}

# Counter: Conversion errors
conversion_errors_total{converter="CSVConverter", error_type="validation"}
```

### Custom Metrics

Add your own metrics using the MetricsCollector:

```python
from pywats.core.metrics import MetricsCollector

collector = MetricsCollector(instance_id="my_app", enabled=True)

# Counter
my_counter = collector.counter(
    "my_operations_total",
    "Total operations performed",
    labels=["operation_type"]
)
my_counter.labels(operation_type="upload").inc()

# Gauge
my_gauge = collector.gauge(
    "my_active_connections",
    "Number of active connections"
)
my_gauge.set(42)

# Histogram
my_histogram = collector.histogram(
    "my_processing_time_seconds",
    "Processing time in seconds",
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0]
)
my_histogram.observe(2.5)
```

---

## Health Endpoints

PyWATS provides health check endpoints for container orchestration (Docker, Kubernetes):

### Available Endpoints

#### GET /health
Basic health check (always available):

```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-02T19:30:00Z"
}
```

#### GET /health/ready
Readiness probe (service is ready to accept traffic):

```bash
curl http://localhost:8080/health/ready
```

Response:
```json
{
  "status": "ready",
  "api_status": "online",
  "timestamp": "2026-02-02T19:30:00Z"
}
```

#### GET /health/live
Liveness probe (service is alive, may not be ready):

```bash
curl http://localhost:8080/health/live
```

Response:
```json
{
  "status": "alive",
  "uptime_seconds": 3600,
  "timestamp": "2026-02-02T19:30:00Z"
}
```

#### GET /metrics
Prometheus metrics endpoint:

```bash
curl http://localhost:8080/metrics
```

**With MetricsCollector** (Prometheus text format):
```
# HELP http_requests_total Total HTTP requests
# TYPE http_requests_total counter
http_requests_total{method="GET",endpoint="/api/Product",status="200"} 1523.0

# HELP cache_hit_rate Cache hit rate
# TYPE cache_hit_rate gauge
cache_hit_rate{cache_name="http_response"} 0.87
```

**Without MetricsCollector** (JSON fallback):
```json
{
  "cache": {
    "enabled": true,
    "size": 234,
    "max_size": 1000,
    "hit_rate": 0.87,
    "total_requests": 1523,
    "hits": 1325,
    "misses": 198,
    "evictions": 12
  },
  "queue": {
    "size": 5,
    "active_workers": 3,
    "total_processed": 4521
  }
}
```

### Kubernetes Configuration

**Deployment YAML**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pywats-client
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: pywats-client
        image: pywats-client:latest
        ports:
        - containerPort: 8080
          name: health
        env:
        - name: PYWATS_HEALTH_PORT
          value: "8080"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

---

## Prometheus Integration

### Setup Prometheus

**1. Install Prometheus**:

```bash
# Docker
docker run -d -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Docker Compose
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

**2. Configure Scraping** (`prometheus.yml`):

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'pywats-client'
    static_configs:
      - targets: ['localhost:8080']
        labels:
          instance: 'default'
          environment: 'production'
    
    metrics_path: '/metrics'
    scrape_interval: 10s
```

**3. Verify Metrics**:

Visit http://localhost:9090 and query:

```promql
# HTTP request rate
rate(http_requests_total[5m])

# Cache hit rate
cache_hit_rate

# Queue depth
queue_depth
```

### Common Queries

**HTTP Performance**:

```promql
# Request rate by endpoint
sum(rate(http_requests_total[5m])) by (endpoint)

# 95th percentile latency
histogram_quantile(0.95, http_request_duration_seconds_bucket)

# Error rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
```

**Cache Performance**:

```promql
# Overall hit rate
cache_hit_rate{cache_name="http_response"}

# Cache size utilization
cache_size_bytes / 1000  # If max_size=1000

# Eviction rate
rate(cache_evictions_total[5m])
```

**Queue Health**:

```promql
# Queue backlog
queue_depth{queue_name="converter_queue"}

# Processing throughput
rate(queue_items_processed_total[5m])

# Worker utilization
queue_active_workers / 5  # If max_workers=5
```

---

## Grafana Dashboards

### Setup Grafana

**1. Install Grafana**:

```bash
# Docker
docker run -d -p 3000:3000 grafana/grafana

# Docker Compose
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

**2. Add Prometheus Data Source**:

1. Navigate to http://localhost:3000
2. Login (admin/admin)
3. Configuration → Data Sources → Add data source
4. Select Prometheus
5. URL: `http://prometheus:9090` (Docker) or `http://localhost:9090` (local)
6. Save & Test

### Dashboard Examples

#### HTTP Performance Dashboard

**Panels**:

1. **Request Rate** (Graph):
   ```promql
   sum(rate(http_requests_total[5m])) by (endpoint)
   ```

2. **Response Time (p95)** (Graph):
   ```promql
   histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
   ```

3. **Error Rate** (Gauge):
   ```promql
   sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))
   ```

4. **Active Requests** (Stat):
   ```promql
   sum(http_requests_active)
   ```

#### Cache Performance Dashboard

**Panels**:

1. **Hit Rate** (Gauge):
   ```promql
   cache_hit_rate{cache_name="http_response"}
   ```

2. **Cache Size** (Graph):
   ```promql
   cache_size_bytes{cache_name="http_response"}
   ```

3. **Hits vs Misses** (Graph):
   ```promql
   rate(cache_hits_total[5m])
   rate(cache_misses_total[5m])
   ```

4. **Eviction Rate** (Graph):
   ```promql
   rate(cache_evictions_total[5m])
   ```

#### Queue Metrics Dashboard

**Panels**:

1. **Queue Depth** (Graph):
   ```promql
   queue_depth{queue_name="converter_queue"}
   ```

2. **Processing Rate** (Graph):
   ```promql
   rate(queue_items_processed_total[5m])
   ```

3. **Worker Utilization** (Gauge):
   ```promql
   queue_active_workers / 5 * 100
   ```

4. **Processing Time (p95)** (Graph):
   ```promql
   histogram_quantile(0.95, rate(queue_processing_duration_seconds_bucket[5m]))
   ```

### Import Dashboard JSON

Save this as `pywats-dashboard.json`:

```json
{
  "dashboard": {
    "title": "PyWATS Observability",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total[5m])) by (endpoint)"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Cache Hit Rate",
        "targets": [
          {
            "expr": "cache_hit_rate{cache_name=\"http_response\"}"
          }
        ],
        "type": "gauge"
      }
    ]
  }
}
```

Import via Grafana UI: Dashboards → Import → Upload JSON file

---

## HTTP Cache Metrics

### Monitoring Cache Performance

**Key Metrics**:

- **Hit Rate**: Percentage of requests served from cache (0.0-1.0)
- **Size**: Number of cached entries
- **Evictions**: Number of entries removed due to TTL or size limit
- **Requests/Hits/Misses**: Counters for cache operations

**Access via /metrics endpoint**:

```bash
curl http://localhost:8080/metrics | grep cache
```

**Example Output**:

```
cache_hit_rate{cache_name="http_response"} 0.87
cache_size_bytes{cache_name="http_response"} 234.0
cache_evictions_total{cache_name="http_response"} 12.0
cache_hits_total{cache_name="http_response"} 1325.0
cache_misses_total{cache_name="http_response"} 198.0
```

### Tuning Cache Configuration

**Optimal Settings**:

```python
# High hit rate workload (repeated requests)
api = AsyncWATS(
    base_url="...",
    token="...",
    enable_cache=True,
    cache_ttl=600,  # 10 minutes
    cache_max_size=2000
)

# Memory-constrained environment
api = AsyncWATS(
    base_url="...",
    token="...",
    enable_cache=True,
    cache_ttl=300,  # 5 minutes
    cache_max_size=500
)

# Disable caching
api = AsyncWATS(
    base_url="...",
    token="...",
    enable_cache=False
)
```

**Monitor and Adjust**:

1. Check hit rate: `cache_hit_rate` should be > 0.7 (70%)
2. Check evictions: High eviction rate → increase `cache_max_size`
3. Check memory: Large cache size → reduce `cache_max_size` or `cache_ttl`

---

## Queue Metrics

### Monitoring Converter Queues

**Key Metrics**:

- **Queue Depth**: Number of pending items (should stay low)
- **Active Workers**: Number of workers processing items
- **Total Processed**: Cumulative items processed
- **Processing Time**: Time to process each item

**Access via /metrics endpoint**:

```bash
curl http://localhost:8080/metrics | grep queue
```

**Example Output**:

```json
{
  "queue": {
    "size": 5,
    "active_workers": 3,
    "total_processed": 4521
  }
}
```

### Queue Health Alerts

**Prometheus Alerting Rules**:

```yaml
groups:
  - name: pywats_queues
    rules:
      - alert: QueueBacklog
        expr: queue_depth > 100
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Queue backlog detected"
          description: "Queue {{ $labels.queue_name }} has {{ $value }} items pending"
      
      - alert: NoActiveWorkers
        expr: queue_active_workers == 0 and queue_depth > 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "No active workers processing queue"
          description: "Queue {{ $labels.queue_name }} has items but no workers"
```

---

## Configuration

### ClientConfig Settings

**File**: `config.json`

```json
{
  "enable_cache": true,
  "cache_ttl_seconds": 300.0,
  "cache_max_size": 1000,
  "enable_metrics": true,
  "metrics_port": 9090
}
```

**Field Descriptions**:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enable_cache` | bool | true | Enable HTTP response caching |
| `cache_ttl_seconds` | float | 300.0 | Cache TTL in seconds (5 minutes) |
| `cache_max_size` | int | 1000 | Maximum cache entries |
| `enable_metrics` | bool | true | Enable Prometheus metrics |
| `metrics_port` | int | 9090 | Prometheus metrics port |

### Environment Variables

Override config via environment variables:

```bash
export PYWATS_HEALTH_PORT=8080
export PYWATS_ENABLE_CACHE=true
export PYWATS_CACHE_TTL=600
```

---

## Troubleshooting

### Metrics Not Appearing

**Issue**: `/metrics` endpoint returns empty or minimal data

**Solutions**:

1. **Check config**: Verify `enable_metrics=true` in config.json
2. **Check service**: Ensure AsyncClientService is running
3. **Check imports**: Verify prometheus_client is installed:
   ```bash
   pip install prometheus-client
   ```
4. **Check logs**: Look for "Metrics collection enabled" in service logs

### Cache Not Working

**Issue**: Cache hit rate is 0% or cache metrics missing

**Solutions**:

1. **Check config**: Verify `enable_cache=true`
2. **Check requests**: Only GET requests are cached
3. **Check TTL**: Items may be expiring too quickly (increase `cache_ttl_seconds`)
4. **Check size**: Cache may be full (increase `cache_max_size`)
5. **Clear cache**: Force refresh with `api._http_client.clear_cache()`

### Health Endpoint Not Responding

**Issue**: Cannot reach http://localhost:8080/health

**Solutions**:

1. **Check port**: Verify PYWATS_HEALTH_PORT environment variable
2. **Check firewall**: Ensure port 8080 is open
3. **Check service**: Ensure AsyncClientService is running
4. **Check logs**: Look for "Health server started on port" message

### High Memory Usage

**Issue**: Memory consumption increasing over time

**Solutions**:

1. **Reduce cache size**: Lower `cache_max_size` in config
2. **Reduce TTL**: Lower `cache_ttl_seconds` to expire entries faster
3. **Disable cache**: Set `enable_cache=false` if not needed
4. **Monitor metrics**: Check `cache_size_bytes` in Prometheus

---

## Best Practices

### Production Deployment

1. **Enable Metrics**: Always enable metrics in production
2. **Configure Alerts**: Set up Prometheus alerts for queue depth, error rates
3. **Monitor Cache**: Track cache hit rate and adjust TTL/size as needed
4. **Health Checks**: Use liveness/readiness probes in Kubernetes
5. **Resource Limits**: Set memory/CPU limits based on cache size

### Development

1. **Disable Cache**: Set `enable_cache=false` for testing latest data
2. **Verbose Logging**: Enable debug logs to see cache hits/misses
3. **Local Prometheus**: Run Prometheus locally to test metrics
4. **Manual Cache Control**: Use `clear_cache()` and `invalidate_cache()` for testing

### Security

1. **Metrics Port**: Do not expose metrics port to public internet
2. **Authentication**: Use network policies or reverse proxy for metrics endpoint
3. **Sensitive Data**: Ensure cached responses don't contain credentials
4. **Rate Limiting**: Consider rate limiting on /metrics endpoint

---

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Python Prometheus Client](https://github.com/prometheus/client_python)
- [PyWATS Architecture Guide](./architecture.md)
- [PyWATS Performance Guide](./performance.md)
- [Kubernetes Health Checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

---

**Questions or Issues?**

- GitHub Issues: [pyWATS Issues](https://github.com/olreppe/pyWATS/issues)
- Documentation: [PyWATS Docs](../README.md)
