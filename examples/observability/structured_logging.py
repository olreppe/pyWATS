"""
Example: Structured Logging with pyWATS

Demonstrates JSON structured logging, correlation IDs, and logging context.

Structured logging provides:
1. Machine-readable JSON output for log aggregation systems
2. Automatic correlation IDs for request tracing
3. Context management for session/environment metadata
4. Traditional text logging for development
"""

import time
from pywats import (
    enable_debug_logging,
    set_logging_context,
    clear_logging_context,
    get_logging_context,
)
from pywats.core.logging import get_logger


def example_text_logging():
    """Example 1: Traditional text logging with correlation IDs."""
    print("\n=== Example 1: Traditional Text Logging ===\n")
    
    # Enable text logging (default)
    enable_debug_logging(use_correlation_ids=True)
    
    logger = get_logger("pywats.examples.logging")
    
    logger.debug("Debug message - detailed information")
    logger.info("Info message - general information")
    logger.warning("Warning message - something unusual")
    logger.error("Error message - something failed")
    
    print("\nNote: Correlation IDs shown as [--------] when not in pyWATS context")


def example_json_logging():
    """Example 2: JSON structured logging for log aggregation."""
    print("\n=== Example 2: JSON Structured Logging ===\n")
    
    # Enable JSON logging
    enable_debug_logging(use_json=True)
    
    logger = get_logger("pywats.examples.logging")
    
    # Basic log message
    logger.info("Application started")
    
    # Log with extra structured fields
    logger.info("Report submitted", extra={
        "report_id": 12345,
        "serial_number": "ABC-789",
        "station": "ICT-01",
        "duration_ms": 123.45
    })
    
    # Log with nested data
    logger.info("Query executed", extra={
        "query_type": "product_search",
        "filters": {"part_number": "PART-001", "status": "active"},
        "result_count": 42,
        "execution_time_ms": 56.78
    })
    
    print("\nNote: JSON output is ideal for ELK, Splunk, or CloudWatch")


def example_logging_context():
    """Example 3: Using logging context for session metadata."""
    print("\n=== Example 3: Logging Context ===\n")
    
    enable_debug_logging(use_json=True)
    
    logger = get_logger("pywats.examples.logging")
    
    # Set global context that applies to all logs
    set_logging_context(
        environment="production",
        version="0.3.0",
        station="FCT-02"
    )
    
    logger.info("Session started")
    logger.info("Processing batch", extra={"batch_id": "BATCH-001"})
    
    # Context appears in all log entries
    current_context = get_logging_context()
    print(f"\nCurrent context: {current_context}")
    
    # Clear context when session ends
    clear_logging_context()
    logger.info("Session ended")


def example_error_logging():
    """Example 4: Logging exceptions with structured data."""
    print("\n=== Example 4: Exception Logging ===\n")
    
    enable_debug_logging(use_json=True)
    
    logger = get_logger("pywats.examples.logging")
    
    try:
        # Simulate an error
        result = 1 / 0
    except ZeroDivisionError as e:
        logger.error("Mathematical error occurred", extra={
            "error_type": "division_by_zero",
            "operation": "calculate_yield",
            "inputs": {"numerator": 1, "denominator": 0}
        }, exc_info=True)
    
    print("\nNote: Exception traceback is included in JSON 'exception' field")


def example_performance_logging():
    """Example 5: Performance monitoring with structured logs."""
    print("\n=== Example 5: Performance Monitoring ===\n")
    
    enable_debug_logging(use_json=True)
    
    logger = get_logger("pywats.examples.logging")
    
    # Simulate operation timing
    start_time = time.time()
    
    # Simulate work
    time.sleep(0.1)
    
    duration_ms = (time.time() - start_time) * 1000
    
    logger.info("Operation completed", extra={
        "operation": "fetch_reports",
        "duration_ms": round(duration_ms, 2),
        "records_processed": 1500,
        "cache_hit_rate": 0.85,
        "avg_response_time_ms": 12.34
    })
    
    print("\nNote: Structured metrics enable performance dashboards")


def example_multi_service_logging():
    """Example 6: Logging across multiple services/modules."""
    print("\n=== Example 6: Multi-Service Logging ===\n")
    
    enable_debug_logging(use_json=True)
    
    # Different loggers for different modules
    report_logger = get_logger("pywats.domains.report")
    product_logger = get_logger("pywats.domains.product")
    cache_logger = get_logger("pywats.core.cache")
    
    # Set common context
    set_logging_context(request_id="req-12345", user_id="user789")
    
    # Each service logs with its own logger
    report_logger.info("Querying reports", extra={"filter": "pn=PART-001"})
    cache_logger.debug("Cache miss", extra={"key": "product:PART-001"})
    product_logger.info("Fetching product", extra={"product_id": "PART-001"})
    cache_logger.debug("Cache updated", extra={"key": "product:PART-001"})
    report_logger.info("Query completed", extra={"result_count": 25})
    
    clear_logging_context()
    
    print("\nNote: request_id appears in all logs for distributed tracing")


def example_custom_levels():
    """Example 7: Using different log levels."""
    print("\n=== Example 7: Log Levels ===\n")
    
    import logging
    
    # Set different levels for different scenarios
    
    # Development: Show everything
    print("Development mode (DEBUG level):")
    enable_debug_logging(level=logging.DEBUG)
    logger = get_logger("pywats.examples")
    logger.debug("Detailed debug info")
    logger.info("General info")
    
    # Production: Only warnings and errors
    print("\nProduction mode (WARNING level):")
    enable_debug_logging(level=logging.WARNING)
    logger = get_logger("pywats.examples")
    logger.debug("This won't appear")
    logger.info("This won't appear either")
    logger.warning("This appears")
    logger.error("This also appears")


def example_real_world_scenario():
    """Example 8: Real-world scenario - Report submission with full logging."""
    print("\n=== Example 8: Real-World Scenario ===\n")
    
    enable_debug_logging(use_json=True)
    
    logger = get_logger("pywats.examples.report_submission")
    
    # Set session context
    set_logging_context(
        environment="production",
        station="ICT-03",
        operator="john.doe",
        shift="morning"
    )
    
    # Simulate report submission workflow
    logger.info("Report submission started", extra={
        "part_number": "BOARD-Rev2",
        "serial_number": "SN-2024-0123",
        "process_type": "ICT"  # 'process' is a reserved LogRecord field, use 'process_type'
    })
    
    # Validation
    logger.debug("Validating report data", extra={
        "validators": ["schema", "business_rules", "constraints"],
        "validation_time_ms": 5.2
    })
    
    # Submission
    logger.info("Submitting to WATS server", extra={
        "server": "wats-prod-01.company.com",
        "retry_attempt": 1
    })
    
    # Success
    logger.info("Report submitted successfully", extra={
        "report_id": 987654,
        "total_duration_ms": 234.56,
        "server_response_time_ms": 189.23
    })
    
    clear_logging_context()
    
    print("\nNote: Complete audit trail with timing, context, and metadata")


if __name__ == "__main__":
    print("=" * 70)
    print("pyWATS Structured Logging Examples")
    print("=" * 70)
    
    example_text_logging()
    example_json_logging()
    example_logging_context()
    example_error_logging()
    example_performance_logging()
    example_multi_service_logging()
    example_custom_levels()
    example_real_world_scenario()
    
    print("\n" + "=" * 70)
    print("Examples complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. Use enable_debug_logging(use_json=True) for production")
    print("2. Add extra={...} to logger calls for structured fields")
    print("3. Use set_logging_context() for session/environment metadata")
    print("4. All logs include correlation IDs for request tracing")
    print("5. JSON output integrates with ELK, Splunk, CloudWatch, etc.")
