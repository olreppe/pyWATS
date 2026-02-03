"""
Example: Client configuration patterns in pyWATS

This example demonstrates:
- Environment-specific configurations
- Authentication patterns
- Connection settings
- Performance tuning options
- Configuration file management

Prerequisites:
- pyWATS installed
"""

from pywats import Client
from pywats.core.config import DomainSettings
from pywats.core.exceptions import ErrorMode
from pywats_client.core.config import (
    ClientConfig,
    ConverterConfig,
    ProxyConfig,
    StationPreset
)
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def basic_configuration() -> None:
    """Basic client configuration."""
    logger.info("\n=== Basic Configuration ===")
    
    # Method 1: Direct instantiation
    client = Client(
        base_url="https://api.example.com",
        auth_token="your-api-token-here"
    )
    logger.info("Created client with basic config")
    
    # Method 2: From environment variables
    # Set these in your environment:
    # export PYWATS_API_URL="https://api.example.com"
    # export PYWATS_API_TOKEN="your-token"
    
    client = Client(
        base_url=os.getenv("PYWATS_API_URL", "https://default.example.com"),
        auth_token=os.getenv("PYWATS_API_TOKEN")
    )
    logger.info("Created client from environment variables")


def error_mode_configuration() -> None:
    """Configure error handling mode."""
    logger.info("\n=== Error Mode Configuration ===")
    
    # STRICT mode (production) - raises exceptions on errors
    strict_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        error_mode=ErrorMode.STRICT
    )
    logger.info("STRICT mode: Exceptions raised for empty responses")
    
    # LENIENT mode (scripts/exploration) - returns None on not found
    lenient_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        error_mode=ErrorMode.LENIENT
    )
    logger.info("LENIENT mode: Returns None for empty responses")


def timeout_configuration() -> None:
    """Configure request timeouts."""
    logger.info("\n=== Timeout Configuration ===")
    
    # Set custom timeouts (in seconds)
    client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        timeout=30  # 30 second timeout
    )
    logger.info("Configured 30-second timeout")
    
    # For operations with large data transfers
    slow_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        timeout=120  # 2 minute timeout
    )
    logger.info("Configured 2-minute timeout for slow operations")


def retry_configuration():
    """Configure retry behavior."""
    logger.info("\n=== Retry Configuration ===")
    
    # Configure retry parameters
    client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        max_retries=5,  # Retry up to 5 times
        retry_backoff=2.0  # Exponential backoff factor
    )
    logger.info("Configured 5 retries with 2.0 backoff factor")


def proxy_configuration():
    """Configure proxy settings."""
    logger.info("\n=== Proxy Configuration ===")
    
    # Configure HTTP proxy
    proxy_config = ProxyConfig(
        http_proxy="http://proxy.company.com:8080",
        https_proxy="https://proxy.company.com:8443",
        no_proxy="localhost,127.0.0.1"
    )
    
    logger.info(f"Proxy config: {proxy_config.to_dict()}")
    
    # Use with client (example - actual Client might not support this directly)
    # You would typically set these as environment variables:
    # os.environ['HTTP_PROXY'] = proxy_config.http_proxy
    # os.environ['HTTPS_PROXY'] = proxy_config.https_proxy


def converter_configuration():
    """Configure converter settings."""
    logger.info("\n=== Converter Configuration ===")
    
    # Configure converter behavior
    converter_config = ConverterConfig(
        max_queue_size=1000,
        worker_threads=4,
        batch_size=10,
        timeout_seconds=300
    )
    
    logger.info(f"Converter config:")
    logger.info(f"  Max queue size: {converter_config.max_queue_size}")
    logger.info(f"  Worker threads: {converter_config.worker_threads}")
    logger.info(f"  Batch size: {converter_config.batch_size}")


def domain_settings_configuration():
    """Configure domain-specific settings."""
    logger.info("\n=== Domain Settings ===")
    
    # Create domain settings with custom behavior
    settings = DomainSettings(
        cache_ttl=600,  # Cache for 10 minutes
        auto_submit=True,  # Auto-submit changes
        max_attachment_size_mb=50  # 50 MB limit
    )
    
    logger.info(f"Domain settings:")
    logger.info(f"  Cache TTL: {settings.cache_ttl}s")
    logger.info(f"  Auto-submit: {settings.auto_submit}")
    logger.info(f"  Max attachment: {settings.max_attachment_size_mb}MB")


def environment_specific_config():
    """Configure for different environments."""
    logger.info("\n=== Environment-Specific Configuration ===")
    
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        config = {
            "base_url": "https://api.prod.example.com",
            "error_mode": ErrorMode.STRICT,
            "timeout": 30,
            "max_retries": 3,
            "log_level": logging.WARNING
        }
        logger.info("Production configuration loaded")
        
    elif environment == "staging":
        config = {
            "base_url": "https://api.staging.example.com",
            "error_mode": ErrorMode.STRICT,
            "timeout": 60,
            "max_retries": 5,
            "log_level": logging.INFO
        }
        logger.info("Staging configuration loaded")
        
    else:  # development
        config = {
            "base_url": "https://api.dev.example.com",
            "error_mode": ErrorMode.LENIENT,
            "timeout": 120,
            "max_retries": 1,
            "log_level": logging.DEBUG
        }
        logger.info("Development configuration loaded")
    
    # Create client with environment config
    client = Client(
        base_url=config["base_url"],
        auth_token=os.getenv("PYWATS_API_TOKEN"),
        error_mode=config["error_mode"],
        timeout=config["timeout"]
    )
    
    logging.getLogger("pywats").setLevel(config["log_level"])
    
    logger.info(f"Client configured for {environment} environment")


def configuration_from_file():
    """Load configuration from a file."""
    logger.info("\n=== Configuration from File ===")
    
    # Example config file format (JSON, YAML, etc.)
    config_data = {
        "api": {
            "base_url": "https://api.example.com",
            "timeout": 30,
            "error_mode": "STRICT"
        },
        "converter": {
            "max_queue_size": 500,
            "worker_threads": 2
        }
    }
    
    # Parse config
    error_mode = ErrorMode.STRICT if config_data["api"]["error_mode"] == "STRICT" else ErrorMode.LENIENT
    
    client = Client(
        base_url=config_data["api"]["base_url"],
        auth_token=os.getenv("PYWATS_API_TOKEN"),
        timeout=config_data["api"]["timeout"],
        error_mode=error_mode
    )
    
    logger.info("Client created from config file")
    
    # Save configuration
    config_to_save = {
        "base_url": client._http.base_url if hasattr(client, '_http') else "unknown",
        "timeout": config_data["api"]["timeout"],
        "error_mode": error_mode.name
    }
    
    logger.info(f"Config to save: {config_to_save}")


def http_caching_configuration():
    """Configure HTTP response caching."""
    logger.info("\n=== HTTP Caching Configuration ===")
    
    # Enable caching for read-heavy workloads
    cached_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        enable_cache=True,  # Enable HTTP response caching
        cache_ttl=300,  # Cache responses for 5 minutes
        cache_max_size=1000  # Store up to 1000 cached responses
    )
    logger.info("HTTP caching enabled:")
    logger.info("  Cache TTL: 300 seconds (5 minutes)")
    logger.info("  Max cache size: 1000 entries")
    
    # Disable caching for real-time data
    realtime_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        enable_cache=False  # Disable caching for real-time data
    )
    logger.info("Caching disabled for real-time data")
    
    # Custom cache configuration for different workloads
    # Long TTL for rarely-changing data (products, processes)
    product_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        enable_cache=True,
        cache_ttl=3600,  # 1 hour for product data
        cache_max_size=500
    )
    logger.info("Product client: 1 hour cache TTL")
    
    # Short TTL for frequently-changing data (reports, metrics)
    report_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        enable_cache=True,
        cache_ttl=60,  # 1 minute for report data
        cache_max_size=2000
    )
    logger.info("Report client: 1 minute cache TTL")
    
    # Monitor cache statistics (if client supports it)
    # Example: cached_client.get_cache_stats()
    # Would return: {'hits': 150, 'misses': 50, 'size': 200, 'max_size': 1000}


def performance_tuning():
    """Configure for optimal performance."""
    logger.info("\n=== Performance Tuning ===")
    
    # High-performance configuration with caching
    high_perf_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        timeout=10,  # Short timeout
        max_retries=1,  # Minimal retries
        enable_cache=True,  # Enable caching
        cache_ttl=300,  # 5 minute cache
        cache_max_size=1000
    )
    logger.info("High-performance client configured with caching")
    
    # Reliability-focused configuration
    reliable_client = Client(
        base_url="https://api.example.com",
        auth_token="token",
        timeout=60,  # Longer timeout
        max_retries=5,  # More retries
        error_mode=ErrorMode.STRICT  # Fail fast on errors
    )
    logger.info("Reliability-focused client configured")


def logging_configuration():
    """Configure logging for pyWATS."""
    logger.info("\n=== Logging Configuration ===")
    
    # Enable debug logging for pyWATS
    from pywats.core.logging import enable_debug_logging
    
    enable_debug_logging()
    logger.info("Debug logging enabled for pyWATS")
    
    # Configure specific module logging
    pywats_logger = logging.getLogger('pywats')
    pywats_logger.setLevel(logging.DEBUG)
    
    # Configure HTTP client logging
    http_logger = logging.getLogger('pywats.http_client')
    http_logger.setLevel(logging.INFO)
    
    logger.info("Module-specific logging configured")


def secure_credential_management():
    """Demonstrate secure credential handling."""
    logger.info("\n=== Secure Credential Management ===")
    
    # Method 1: Environment variables (recommended)
    client = Client(
        base_url=os.getenv("PYWATS_API_URL"),
        auth_token=os.getenv("PYWATS_API_TOKEN")
    )
    logger.info("Credentials loaded from environment variables")
    
    # Method 2: Credentials file (with proper permissions)
    credentials_file = Path.home() / ".pywats" / "credentials"
    
    if credentials_file.exists():
        # Read credentials (file should be chmod 600)
        logger.info(f"Reading credentials from {credentials_file}")
        # Implementation would read and parse the file
    
    # NEVER: Hard-code credentials in source code
    # BAD: client = Client(auth_token="abc123secretkey")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("pyWATS Configuration Examples")
    print("="*60)
    
    # Run all examples
    basic_configuration()
    error_mode_configuration()
    timeout_configuration()
    retry_configuration()
    proxy_configuration()
    converter_configuration()
    domain_settings_configuration()
    environment_specific_config()
    configuration_from_file()
    http_caching_configuration()
    performance_tuning()
    logging_configuration()
    secure_credential_management()
    
    print("\n" + "="*60)
    print("Configuration examples completed!")
    print("="*60 + "\n")
    
    print("\nKey Takeaways:")
    print("1. Use environment variables for credentials")
    print("2. Choose error mode based on use case (STRICT for prod, LENIENT for scripts)")
    print("3. Tune timeouts and retries for your workload")
    print("4. Enable HTTP caching for read-heavy workloads (300-3600 second TTL)")
    print("5. Disable caching for real-time data (enable_cache=False)")
    print("6. Monitor cache statistics to optimize TTL and size")
    print("7. Enable debug logging during development")
    print("8. Keep credentials secure and never commit them to source control")
