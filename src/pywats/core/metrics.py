"""
Metrics collection for pyWATS using Prometheus client.

This module provides a centralized metrics collection system for monitoring
pyWATS performance, health, and usage patterns.

Installation:
    pip install pywats-api[observability]

Usage:
    from pywats.core.metrics import metrics, start_metrics_server
    
    # Start metrics server
    start_metrics_server(port=9090)
    
    # Metrics are collected automatically when using the pyWATS client
    # Access at http://localhost:9090/metrics

Features:
    - Request duration and count tracking
    - Error rate monitoring
    - System resource metrics (CPU, memory)
    - Queue and converter metrics
    - Prometheus-compatible format
"""

import functools
import logging
import time
from typing import Callable, Optional, TypeVar, Any
import threading

logger = logging.getLogger(__name__)

# Optional dependency - only import if prometheus_client is installed
try:
    from prometheus_client import (
        Counter,
        Gauge,
        Histogram,
        CollectorRegistry,
        generate_latest,
        CONTENT_TYPE_LATEST,
    )
    from prometheus_client import start_http_server
    
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    logger.debug("prometheus_client not installed - metrics disabled")

# Optional dependency for system metrics
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logger.debug("psutil not installed - system metrics disabled")

T = TypeVar('T')


class MetricsCollector:
    """
    Central metrics collection for pyWATS.
    
    Collects Prometheus-compatible metrics for:
    - HTTP request duration and counts
    - Error rates
    - System resources (if psutil available)
    - Queue statistics
    - Converter execution
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.enabled = PROMETHEUS_AVAILABLE
        
        if not self.enabled:
            logger.warning(
                "Metrics disabled - install with: pip install pywats-api[observability]"
            )
            return
        
        self.registry = CollectorRegistry()
        self._initialize_metrics()
        self._system_monitor_running = False
    
    def _initialize_metrics(self):
        """Initialize Prometheus metrics."""
        if not self.enabled:
            return
        
        # HTTP Request metrics
        self.http_requests_total = Counter(
            'pywats_http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status'],
            registry=self.registry
        )
        
        self.http_request_duration_seconds = Histogram(
            'pywats_http_request_duration_seconds',
            'HTTP request duration in seconds',
            ['method', 'endpoint'],
            registry=self.registry
        )
        
        # Error metrics
        self.errors_total = Counter(
            'pywats_errors_total',
            'Total errors by type',
            ['error_type', 'operation'],
            registry=self.registry
        )
        
        # System metrics (if psutil available)
        if PSUTIL_AVAILABLE:
            self.process_cpu_percent = Gauge(
                'pywats_process_cpu_percent',
                'Process CPU usage percent',
                registry=self.registry
            )
            
            self.process_memory_bytes = Gauge(
                'pywats_process_memory_bytes',
                'Process memory usage in bytes',
                registry=self.registry
            )
            
            self.process_threads = Gauge(
                'pywats_process_threads',
                'Number of process threads',
                registry=self.registry
            )
        
        # Queue metrics
        self.queue_depth = Gauge(
            'pywats_queue_depth',
            'Current queue depth',
            ['queue_name'],
            registry=self.registry
        )
        
        self.queue_processing_duration_seconds = Histogram(
            'pywats_queue_processing_duration_seconds',
            'Queue item processing duration',
            ['queue_name', 'item_type'],
            registry=self.registry
        )
        
        # Converter metrics
        self.converter_executions_total = Counter(
            'pywats_converter_executions_total',
            'Total converter executions',
            ['converter', 'status'],
            registry=self.registry
        )
        
        self.converter_duration_seconds = Histogram(
            'pywats_converter_duration_seconds',
            'Converter execution duration',
            ['converter'],
            registry=self.registry
        )
    
    def track_request(self, method: str, endpoint: str) -> Callable:
        """
        Decorator to track HTTP request metrics.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            
        Returns:
            Decorator function
            
        Example:
            @metrics.track_request('GET', '/asset')
            def get_asset(self, asset_id):
                ...
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            if not self.enabled:
                return func
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> T:
                start_time = time.time()
                status = 'success'
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    status = 'error'
                    # Track error
                    error_type = type(e).__name__
                    self.errors_total.labels(
                        error_type=error_type,
                        operation=func.__name__
                    ).inc()
                    raise
                finally:
                    duration = time.time() - start_time
                    self.http_requests_total.labels(
                        method=method,
                        endpoint=endpoint,
                        status=status
                    ).inc()
                    self.http_request_duration_seconds.labels(
                        method=method,
                        endpoint=endpoint
                    ).observe(duration)
            
            return wrapper
        return decorator
    
    def track_converter(self, converter_name: str) -> Callable:
        """
        Decorator to track converter execution metrics.
        
        Args:
            converter_name: Name of the converter
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable[..., T]) -> Callable[..., T]:
            if not self.enabled:
                return func
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs) -> T:
                start_time = time.time()
                status = 'success'
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception:
                    status = 'error'
                    raise
                finally:
                    duration = time.time() - start_time
                    self.converter_executions_total.labels(
                        converter=converter_name,
                        status=status
                    ).inc()
                    self.converter_duration_seconds.labels(
                        converter=converter_name
                    ).observe(duration)
            
            return wrapper
        return decorator
    
    def update_queue_depth(self, queue_name: str, depth: int):
        """
        Update queue depth metric.
        
        Args:
            queue_name: Name of the queue
            depth: Current queue depth
        """
        if self.enabled:
            self.queue_depth.labels(queue_name=queue_name).set(depth)
    
    def track_queue_processing(self, queue_name: str, item_type: str, duration: float):
        """
        Track queue item processing duration.
        
        Args:
            queue_name: Name of the queue
            item_type: Type of item processed
            duration: Processing duration in seconds
        """
        if self.enabled:
            self.queue_processing_duration_seconds.labels(
                queue_name=queue_name,
                item_type=item_type
            ).observe(duration)
    
    def start_system_monitoring(self, interval: float = 15.0):
        """
        Start background thread to collect system metrics.
        
        Args:
            interval: Update interval in seconds (default: 15)
        """
        if not self.enabled or not PSUTIL_AVAILABLE:
            logger.debug("System monitoring not available")
            return
        
        if self._system_monitor_running:
            logger.debug("System monitoring already running")
            return
        
        self._system_monitor_running = True
        
        def monitor_loop():
            """Background monitoring loop."""
            process = psutil.Process()
            
            while self._system_monitor_running:
                try:
                    # Update CPU usage
                    cpu_percent = process.cpu_percent(interval=1.0)
                    self.process_cpu_percent.set(cpu_percent)
                    
                    # Update memory usage
                    memory_info = process.memory_info()
                    self.process_memory_bytes.set(memory_info.rss)
                    
                    # Update thread count
                    thread_count = process.num_threads()
                    self.process_threads.set(thread_count)
                    
                    time.sleep(interval)
                except Exception as e:
                    logger.error(f"Error in system monitoring: {e}")
                    time.sleep(interval)
        
        thread = threading.Thread(target=monitor_loop, daemon=True, name="MetricsMonitor")
        thread.start()
        logger.info(f"Started system monitoring (interval: {interval}s)")
    
    def stop_system_monitoring(self):
        """Stop system monitoring thread."""
        self._system_monitor_running = False
        logger.info("Stopped system monitoring")
    
    def get_metrics(self) -> bytes:
        """
        Get current metrics in Prometheus format.
        
        Returns:
            Metrics in Prometheus text format
        """
        if not self.enabled:
            return b"# Metrics disabled\n"
        
        return generate_latest(self.registry)


# Global metrics instance
metrics = MetricsCollector()


def start_metrics_server(port: int = 9090, addr: str = '0.0.0.0') -> Optional[Any]:
    """
    Start HTTP server to expose metrics on /metrics endpoint.
    
    Args:
        port: Port to listen on (default: 9090)
        addr: Address to bind to (default: '0.0.0.0')
        
    Returns:
        Server object or None if metrics not available
        
    Example:
        >>> from pywats.core.metrics import start_metrics_server
        >>> server = start_metrics_server(port=9090)
        >>> # Metrics available at http://localhost:9090/metrics
    """
    if not PROMETHEUS_AVAILABLE:
        logger.warning(
            "Cannot start metrics server - install with: "
            "pip install pywats-api[observability]"
        )
        return None
    
    try:
        # Start Prometheus HTTP server
        start_http_server(port, addr=addr, registry=metrics.registry)
        logger.info(f"Metrics server started on {addr}:{port}")
        logger.info(f"Metrics available at http://{addr}:{port}/metrics")
        
        # Start system monitoring
        metrics.start_system_monitoring()
        
        return True  # Return something to indicate success
        
    except Exception as e:
        logger.error(f"Failed to start metrics server: {e}")
        return None


__all__ = [
    'metrics',
    'MetricsCollector',
    'start_metrics_server',
    'PROMETHEUS_AVAILABLE',
]
