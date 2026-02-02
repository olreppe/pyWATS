"""
Example: Robust error handling in pyWATS

This example demonstrates:
- Handling different exception types
- Retry strategies with exponential backoff
- Graceful degradation patterns
- Error logging best practices
- Using error modes (STRICT vs LENIENT)

Prerequisites:
- pyWATS installed and configured
- Valid API credentials (or mock for demonstration)
"""

from pywats.core.exceptions import (
    PyWATSError,
    NotFoundError,
    AuthenticationError,
    ValidationError,
    ServerError,
    ConnectionError,
    TimeoutError,
    ErrorMode
)
from pywats_client.exceptions import (
    ClientError,
    ConverterError,
    FileFormatError,
    FileAccessError,
    QueueError,
    ConfigurationError
)
import logging
import time
from typing import Callable, TypeVar, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_with_exponential_backoff(
    func: Callable[[], T],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retriable_exceptions: tuple = (ServerError, ConnectionError, TimeoutError)
) -> T:
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay between retries
        retriable_exceptions: Tuple of exceptions that should trigger retry
        
    Returns:
        Result of the function call
        
    Raises:
        The last exception if all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            return func()
            
        except retriable_exceptions as e:
            if attempt == max_retries - 1:
                logger.error(f"Max retries ({max_retries}) exceeded: {e}")
                raise
            
            # Calculate delay with exponential backoff
            delay = min(base_delay * (2 ** attempt), max_delay)
            
            logger.warning(
                f"Attempt {attempt + 1}/{max_retries} failed: {e}. "
                f"Retrying in {delay:.1f}s..."
            )
            time.sleep(delay)


def handle_specific_errors_example():
    """Demonstrate handling specific error types appropriately."""
    logger.info("\n=== Handling Specific Error Types ===")
    
    # Simulated function calls - replace with real API calls
    def simulate_api_call(error_type: str = None):
        """Simulate different error scenarios."""
        if error_type == "not_found":
            raise NotFoundError("Asset", "ASSET-123", "GET /asset/ASSET-123")
        elif error_type == "auth":
            raise AuthenticationError("Invalid API token")
        elif error_type == "validation":
            raise ValidationError("Invalid field: name", field_errors={"name": "Required"})
        elif error_type == "server":
            raise ServerError("Internal server error", status_code=500)
        return {"id": "ASSET-123", "name": "Test Asset"}
    
    # Example 1: Handle NotFoundError gracefully
    try:
        result = simulate_api_call("not_found")
    except NotFoundError as e:
        logger.warning(f"Resource not found: {e}")
        logger.info("Creating new resource instead...")
        # Fallback: Create new resource
        result = {"id": "ASSET-NEW", "name": "New Asset"}
        logger.info(f"Created: {result}")
    
    # Example 2: Authentication errors should not be retried
    try:
        result = simulate_api_call("auth")
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        logger.info(f"Troubleshooting: {e.troubleshooting_hint}")
        # Don't retry - user needs to fix credentials
        raise
    
    # Example 3: Validation errors with field details
    try:
        result = simulate_api_call("validation")
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        if hasattr(e, 'field_errors') and e.field_errors:
            logger.error("Field errors:")
            for field, error in e.field_errors.items():
                logger.error(f"  - {field}: {error}")
        # Fix validation issues and retry
        raise


def retry_strategy_example():
    """Demonstrate retry strategies."""
    logger.info("\n=== Retry Strategies ===")
    
    attempt_count = [0]  # Mutable to track across closures
    
    def flaky_operation():
        """Simulates an operation that fails a few times then succeeds."""
        attempt_count[0] += 1
        logger.info(f"Executing operation (attempt {attempt_count[0]})...")
        
        if attempt_count[0] < 3:
            raise ServerError(f"Temporary server error (attempt {attempt_count[0]})")
        
        return {"status": "success", "data": "Important data"}
    
    # Use retry decorator
    try:
        result = retry_with_exponential_backoff(
            flaky_operation,
            max_retries=5,
            base_delay=0.5  # Faster for demo
        )
        logger.info(f"Operation succeeded: {result}")
    except ServerError as e:
        logger.error(f"Operation failed after retries: {e}")


def error_mode_example():
    """Demonstrate STRICT vs LENIENT error modes."""
    logger.info("\n=== Error Modes: STRICT vs LENIENT ===")
    
    def simulate_empty_response(mode: ErrorMode):
        """Simulate an empty response based on error mode."""
        # In STRICT mode, empty responses raise EmptyResponseError
        # In LENIENT mode, empty responses return None
        
        if mode == ErrorMode.STRICT:
            logger.info("STRICT mode: Empty responses raise errors")
            from pywats.core.exceptions import EmptyResponseError
            raise EmptyResponseError("GET /asset/missing")
        else:
            logger.info("LENIENT mode: Empty responses return None")
            return None
    
    # STRICT mode (production)
    logger.info("\nProduction mode (STRICT):")
    try:
        result = simulate_empty_response(ErrorMode.STRICT)
    except PyWATSError as e:
        logger.warning(f"Error raised in STRICT mode: {e}")
    
    # LENIENT mode (scripts, exploration)
    logger.info("\nScript mode (LENIENT):")
    result = simulate_empty_response(ErrorMode.LENIENT)
    if result is None:
        logger.info("Received None in LENIENT mode - handle gracefully")


def client_error_handling():
    """Handle client-specific errors."""
    logger.info("\n=== Client Error Handling ===")
    
    # File format errors
    try:
        # Simulate invalid file format
        raise FileFormatError(
            "Invalid CSV format",
            filepath="bad_data.csv"
        )
    except FileFormatError as e:
        logger.error(f"File format error: {e}")
        logger.info(f"Hint: {e.troubleshooting_hint}")
    
    # File access errors
    try:
        # Simulate file access problem
        raise FileAccessError(
            "Permission denied",
            filepath="/restricted/file.txt"
        )
    except FileAccessError as e:
        logger.error(f"File access error: {e}")
        logger.info(f"Hint: {e.troubleshooting_hint}")
    
    # Queue errors
    try:
        # Simulate queue full
        from pywats_client.exceptions import QueueFullError
        raise QueueFullError(
            "Converter queue is full (max: 1000 items)"
        )
    except QueueError as e:
        logger.error(f"Queue error: {e}")
        logger.info("Waiting for queue to process...")
        # Could implement backpressure here


def graceful_degradation_example():
    """Demonstrate graceful degradation patterns."""
    logger.info("\n=== Graceful Degradation ===")
    
    def get_asset_with_fallback(asset_id: str):
        """Get asset with multiple fallback strategies."""
        
        # Try primary source
        try:
            logger.info(f"Trying to fetch asset {asset_id} from API...")
            # Simulate API call that might fail
            raise ConnectionError("API temporarily unavailable")
            
        except ConnectionError as e:
            logger.warning(f"Primary source failed: {e}")
            
            # Fallback 1: Try cache
            try:
                logger.info("Trying cache...")
                # Simulate cache lookup
                cached_data = None  # Would check cache here
                if cached_data:
                    logger.info("Retrieved from cache")
                    return cached_data
                raise NotFoundError("Asset", asset_id, "cache")
                
            except NotFoundError:
                logger.warning("Cache miss")
                
                # Fallback 2: Return default/placeholder
                logger.info("Using default placeholder")
                return {
                    "id": asset_id,
                    "name": "Unknown (offline)",
                    "status": "unavailable",
                    "_cached": False,
                    "_offline": True
                }
    
    result = get_asset_with_fallback("ASSET-123")
    logger.info(f"Result: {result}")


def comprehensive_error_handler(operation_name: str, func: Callable[[], T]) -> Optional[T]:
    """
    Comprehensive error handler for pyWATS operations.
    
    This function demonstrates a production-ready error handling pattern
    that handles all major error types appropriately.
    """
    logger.info(f"\n=== Executing: {operation_name} ===")
    
    try:
        # Try the operation
        result = func()
        logger.info(f"✓ {operation_name} succeeded")
        return result
        
    except AuthenticationError as e:
        # Authentication errors - don't retry
        logger.error(f"✗ Authentication error: {e}")
        logger.error("  → Fix your credentials and try again")
        raise
        
    except ValidationError as e:
        # Validation errors - don't retry
        logger.error(f"✗ Validation error: {e}")
        if hasattr(e, 'field_errors'):
            for field, error in e.field_errors.items():
                logger.error(f"  → {field}: {error}")
        raise
        
    except NotFoundError as e:
        # Not found - might be expected
        logger.warning(f"⚠ Resource not found: {e}")
        return None
        
    except (ServerError, ConnectionError, TimeoutError) as e:
        # Retriable errors - use exponential backoff
        logger.warning(f"⚠ Retriable error: {e}")
        return retry_with_exponential_backoff(func)
        
    except ClientError as e:
        # Client-specific errors
        logger.error(f"✗ Client error: {e}")
        logger.info(f"  → Hint: {e.troubleshooting_hint}")
        raise
        
    except PyWATSError as e:
        # Other pyWATS errors
        logger.error(f"✗ pyWATS error: {e}")
        raise
        
    except Exception as e:
        # Unexpected errors
        logger.error(f"✗ Unexpected error: {type(e).__name__}: {e}")
        raise


if __name__ == "__main__":
    print("\n" + "="*60)
    print("pyWATS Error Handling Examples")
    print("="*60)
    
    # Run all examples
    try:
        handle_specific_errors_example()
    except:
        pass  # Expected to raise
    
    retry_strategy_example()
    error_mode_example()
    client_error_handling()
    graceful_degradation_example()
    
    # Demonstrate comprehensive handler
    def sample_operation():
        return {"status": "ok"}
    
    comprehensive_error_handler("Sample Operation", sample_operation)
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")
