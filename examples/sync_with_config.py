"""
Example: Using sync wrapper with timeout and retry configuration.

This example demonstrates how to configure the synchronous pyWATS API
with custom timeout, retry, and correlation settings.
"""
from pywats import pyWATS
from pywats.core.config import SyncConfig, RetryConfig
import logging

# Enable logging to see correlation IDs and retry behavior
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(correlation_id)s] %(message)s'
)


def example_simple_timeout():
    """Example 1: Simple timeout configuration."""
    print("\n=== Example 1: Simple Timeout ===")
    
    # Configure 45 second timeout
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        timeout=45.0
    )
    
    try:
        product = api.product.get_product("ABC123")
        print(f"Got product: {product.part_number}")
    except TimeoutError:
        print("Request timed out after 45s")


def example_with_retry():
    """Example 2: Enable retry for network resilience."""
    print("\n=== Example 2: With Retry ===")
    
    # Configure retry behavior
    retry = RetryConfig(
        max_retries=3,        # Retry up to 3 times
        backoff=2.0,          # Exponential backoff (2s, 4s, 8s)
    )
    
    config = SyncConfig(
        timeout=30.0,
        retry_enabled=True,
        retry=retry
    )
    
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        sync_config=config
    )
    
    try:
        # This will retry automatically on connection errors
        product = api.product.get_product("ABC123")
        print(f"Got product: {product.part_number}")
    except ConnectionError:
        print("Connection failed after all retries")
    except TimeoutError:
        print("Request timed out")


def example_full_configuration():
    """Example 3: Full production configuration."""
    print("\n=== Example 3: Full Configuration ===")
    
    # Production-ready configuration
    config = SyncConfig(
        timeout=60.0,               # 1 minute timeout
        retry_enabled=True,         # Enable retry
        retry=RetryConfig(
            max_retries=5,          # More aggressive retry
            backoff=1.5,            # Faster backoff
            retry_on_errors=(
                ConnectionError,
                TimeoutError,
                # Add other transient errors as needed
            )
        ),
        correlation_id_enabled=True  # Track requests (default)
    )
    
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        sync_config=config
    )
    
    # Use normally - timeout/retry happen automatically
    try:
        # Example: Get product and its units
        product = api.product.get_product("WIDGET-001")
        print(f"Product: {product.part_number}")
        
        units = api.production.get_units(product_id=product.id, limit=10)
        print(f"Found {len(units)} units")
        
        # Query reports
        from pywats.domains.report.models import WATSFilter
        filter_spec = WATSFilter(
            part_number="WIDGET-001",
            period_count=7
        )
        headers = api.report.query_uut_headers(filter=filter_spec, limit=100)
        print(f"Found {len(headers)} reports in last 7 days")
        
    except TimeoutError as e:
        print(f"Operation timed out: {e}")
    except ConnectionError as e:
        print(f"Connection failed after retries: {e}")
    except Exception as e:
        print(f"Error: {e}")


def example_no_timeout():
    """Example 4: Disable timeout for long-running operations."""
    print("\n=== Example 4: No Timeout ===")
    
    config = SyncConfig(
        timeout=None,  # No timeout - run indefinitely
        retry_enabled=False
    )
    
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        sync_config=config
    )
    
    # Useful for:
    # - Large data exports
    # - Complex analytics queries
    # - Operations that may take variable time
    
    try:
        # This will run until complete, no matter how long
        from pywats.domains.report.models import WATSFilter
        filter_spec = WATSFilter(period_count=365)  # Full year
        
        print("Fetching full year of data (no timeout)...")
        headers = api.report.query_uut_headers(filter=filter_spec, limit=10000)
        print(f"Retrieved {len(headers)} reports")
    except Exception as e:
        print(f"Error: {e}")


def example_disable_correlation():
    """Example 5: Disable correlation IDs."""
    print("\n=== Example 5: Disable Correlation ===")
    
    config = SyncConfig(
        timeout=30.0,
        correlation_id_enabled=False  # Disable correlation IDs
    )
    
    api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        sync_config=config
    )
    
    # Logs won't show correlation IDs
    # Useful when you have your own request tracking
    product = api.product.get_product("ABC123")
    print(f"Got product: {product.part_number}")


def example_different_configs_per_instance():
    """Example 6: Different configs for different purposes."""
    print("\n=== Example 6: Different Configs ===")
    
    # Fast, no-retry API for quick queries
    fast_config = SyncConfig(
        timeout=5.0,           # Very short timeout
        retry_enabled=False    # No retry - fail fast
    )
    
    fast_api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        sync_config=fast_config
    )
    
    # Resilient API for critical operations
    resilient_config = SyncConfig(
        timeout=120.0,         # Long timeout
        retry_enabled=True,
        retry=RetryConfig(max_retries=10, backoff=2.0)
    )
    
    resilient_api = pyWATS(
        base_url="https://your-server.com",
        token="your-token",
        sync_config=resilient_config
    )
    
    # Use the right one for each task
    try:
        # Quick check - use fast API
        product_exists = fast_api.product.get_product("ABC123") is not None
        print(f"Product exists: {product_exists}")
    except TimeoutError:
        print("Quick check timed out")
    
    try:
        # Critical report submission - use resilient API
        # (report submission example would go here)
        print("Using resilient API for critical operations")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("pyWATS Sync Configuration Examples")
    print("=" * 60)
    
    # Note: These examples will fail without valid credentials
    # Replace with your actual WATS server URL and token
    
    print("\nNote: Update base_url and token with your credentials")
    print("Examples demonstrate configuration patterns, not live calls")
    
    # Uncomment to run examples:
    # example_simple_timeout()
    # example_with_retry()
    # example_full_configuration()
    # example_no_timeout()
    # example_disable_correlation()
    # example_different_configs_per_instance()


if __name__ == "__main__":
    main()
