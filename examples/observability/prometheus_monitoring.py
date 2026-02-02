"""
Example: Prometheus Monitoring for pyWATS

This example demonstrates how to enable Prometheus metrics collection
for monitoring pyWATS performance and health.

Prerequisites:
- Install observability features: pip install pywats-api[observability]
- Optional: Install Prometheus for scraping metrics

Features Demonstrated:
- Starting the metrics server
- Automatic request tracking
- System resource monitoring
- Viewing metrics in Prometheus format
- Custom metrics tracking
"""

import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def basic_metrics_example():
    """Basic example of enabling metrics collection."""
    logger.info("\n=== Basic Metrics Example ===")
    
    try:
        from pywats.core.metrics import start_metrics_server, metrics
        
        # Start metrics server on port 9090
        server = start_metrics_server(port=9090)
        
        if server:
            logger.info("✓ Metrics server started successfully")
            logger.info("  → Metrics available at: http://localhost:9090/metrics")
            logger.info("  → System monitoring: Enabled (CPU, memory, threads)")
            logger.info("")
            logger.info("  Try it:")
            logger.info("    curl http://localhost:9090/metrics")
            logger.info("    # or visit in your browser")
        else:
            logger.warning("✗ Metrics server failed to start")
            logger.info("  Install with: pip install pywats-api[observability]")
            return
        
        # Simulate some activity
        logger.info("\nSimulating API activity...")
        for i in range(5):
            # Simulate HTTP request tracking
            simulate_api_request(i)
            time.sleep(1)
        
        # Get current metrics
        logger.info("\nCurrent metrics snapshot:")
        metrics_data = metrics.get_metrics()
        
        # Print first few lines
        lines = metrics_data.decode('utf-8').split('\n')
        for line in lines[:20]:
            if line and not line.startswith('#'):
                logger.info(f"  {line}")
        
        logger.info("\n✓ Metrics collection is working!")
        logger.info("  Keep this script running and visit:")
        logger.info("  http://localhost:9090/metrics")
        
        # Keep running for manual testing
        logger.info("\nPress Ctrl+C to stop...")
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            logger.info("\nStopping metrics server...")
            metrics.stop_system_monitoring()
        
    except ImportError:
        logger.error("prometheus_client not installed")
        logger.info("Install with: pip install pywats-api[observability]")


def simulate_api_request(request_num: int):
    """Simulate an API request for metrics demonstration."""
    from pywats.core.metrics import metrics
    
    # Track a simulated request
    start_time = time.time()
    
    # Simulate some work
    time.sleep(0.1)
    
    duration = time.time() - start_time
    
    # Record metrics manually (normally done by decorators)
    metrics.http_requests_total.labels(
        method='GET',
        endpoint='/asset',
        status='success'
    ).inc()
    
    metrics.http_request_duration_seconds.labels(
        method='GET',
        endpoint='/asset'
    ).observe(duration)
    
    logger.info(f"Request {request_num + 1}: GET /asset (duration: {duration:.3f}s)")


def custom_metrics_example():
    """Example of tracking custom application metrics."""
    logger.info("\n=== Custom Metrics Example ===")
    
    try:
        from pywats.core.metrics import metrics
        
        # Track queue depth
        logger.info("Setting queue depth metrics...")
        for i in range(5):
            depth = 10 - i * 2
            metrics.update_queue_depth('converter_queue', depth)
            logger.info(f"  Queue depth: {depth}")
            time.sleep(1)
        
        # Track converter execution
        logger.info("\nSimulating converter execution...")
        
        @metrics.track_converter('csv_converter')
        def process_csv():
            """Simulated converter function."""
            time.sleep(0.2)
            return "processed"
        
        for i in range(3):
            result = process_csv()
            logger.info(f"  Converter run {i + 1}: {result}")
        
        logger.info("\n✓ Custom metrics recorded!")
        
    except ImportError:
        logger.error("prometheus_client not installed")


def prometheus_integration_guide():
    """Show how to configure Prometheus to scrape pyWATS metrics."""
    logger.info("\n=== Prometheus Integration Guide ===")
    
    prometheus_config = """
# Add this to your prometheus.yml:

scrape_configs:
  - job_name: 'pywats'
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 15s
    
# Then start Prometheus:
#   prometheus --config.file=prometheus.yml

# View metrics at:
#   http://localhost:9090/graph
"""
    
    logger.info(prometheus_config)
    
    grafana_info = """
# Grafana Dashboard Ideas:

1. Request Rate Panel:
   - Metric: rate(pywats_http_requests_total[5m])
   - Group by: endpoint, status

2. Request Duration Panel:
   - Metric: histogram_quantile(0.95, pywats_http_request_duration_seconds)
   - Shows 95th percentile response time

3. Error Rate Panel:
   - Metric: rate(pywats_errors_total[5m])
   - Group by: error_type

4. System Resources Panel:
   - Metrics: pywats_process_cpu_percent, pywats_process_memory_bytes
   - Shows resource usage over time

5. Queue Depth Panel:
   - Metric: pywats_queue_depth
   - Shows queue backlog
"""
    
    logger.info(grafana_info)


def metrics_best_practices():
    """Display best practices for metrics usage."""
    logger.info("\n=== Metrics Best Practices ===")
    
    best_practices = """
1. Resource Usage:
   - Metrics add ~10-50MB memory overhead
   - CPU overhead is <1% for normal operations
   - Use sampling for very high-traffic scenarios

2. Cardinality:
   - Avoid high-cardinality labels (user IDs, timestamps)
   - Keep label values to a reasonable set (endpoints, status codes)
   - Use aggregation for detailed breakdowns

3. Retention:
   - Prometheus stores time-series data
   - Configure retention based on your needs
   - Use recording rules for frequently-queried aggregations

4. Security:
   - Metrics endpoint exposes internal system state
   - Use firewall rules or authentication if publicly exposed
   - Consider network segmentation for metrics

5. Monitoring:
   - Set up alerts for error rates
   - Monitor resource usage trends
   - Track performance degradation
   - Use dashboards for at-a-glance health

6. Integration:
   - Use decorators for automatic tracking
   - Enable metrics in production for observability
   - Disable in development if not needed
   - Export metrics to your monitoring system
"""
    
    logger.info(best_practices)


def main():
    """Run all observability examples."""
    print("\n" + "="*60)
    print("pyWATS Prometheus Monitoring Examples")
    print("="*60)
    
    # Show integration guide first
    prometheus_integration_guide()
    metrics_best_practices()
    
    # Run basic example (will keep running)
    basic_metrics_example()
    
    # Custom metrics (only if basic didn't block)
    custom_metrics_example()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
