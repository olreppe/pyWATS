# Synchronous vs Asynchronous API Usage

This guide explains the differences between pyWATS's synchronous and asynchronous APIs and when to use each.

## Overview

pyWATS provides both synchronous and asynchronous interfaces:

- **Synchronous API** (`pyWATS`): Easy-to-use, blocking operations. Best for scripts, interactive use, and simple automation.
- **Asynchronous API** (`AsyncWATS`): High-performance, non-blocking operations. Best for concurrent workflows and high-throughput applications.

## Synchronous API (pyWATS)

The synchronous API is the default and recommended choice for most users.

### Basic Usage

```python
from pywats import pyWATS

# Initialize
api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token"
)

# All operations block until complete
product = api.product.get_product("PART-001")
units = api.production.get_units(product_id=product.id)
```

### When to Use Synchronous API

- **Scripts and automation**: One-off tasks, data migrations
- **Interactive use**: Jupyter notebooks, REPL exploration
- **Simple workflows**: Sequential operations without concurrency needs
- **Rapid prototyping**: Quick development without async complexity

## Timeout Configuration

By default, all synchronous operations have a **30-second timeout**:

```python
# Default timeout
api = pyWATS(base_url="...", token="...")
result = api.product.get_product("ABC123")  # Times out after 30s
```

### Custom Timeout

Configure a custom timeout for all operations:

```python
# 60 second timeout
api = pyWATS(base_url="...", token="...", timeout=60.0)

# No timeout (run indefinitely)
api = pyWATS(base_url="...", token="...", timeout=None)
```

### Advanced Timeout with SyncConfig

For more control, use `SyncConfig`:

```python
from pywats import pyWATS
from pywats.core.config import SyncConfig

config = SyncConfig(
    timeout=45.0,               # 45 second timeout
    correlation_id_enabled=True  # Enable request tracking
)

api = pyWATS(base_url="...", token="...", sync_config=config)
```

## Retry Configuration

Enable automatic retry for transient failures (network issues, timeouts):

```python
from pywats import pyWATS
from pywats.core.config import SyncConfig, RetryConfig

# Configure retry behavior
retry = RetryConfig(
    max_retries=3,        # Retry up to 3 times
    backoff=2.0,          # Exponential backoff (2s, 4s, 8s)
    retry_on_errors=(ConnectionError, TimeoutError)  # Which errors to retry
)

config = SyncConfig(
    timeout=30.0,
    retry_enabled=True,
    retry=retry
)

api = pyWATS(base_url="...", token="...", sync_config=config)

# Now operations automatically retry on transient failures
try:
    product = api.product.get_product("ABC123")
except ConnectionError:
    print("Failed after retries")
```

### Retry Behavior

When retry is enabled:

1. **First attempt** fails with `ConnectionError` or `TimeoutError`
2. **Wait** 2 seconds (backoff^1)
3. **Second attempt** fails
4. **Wait** 4 seconds (backoff^2)
5. **Third attempt** fails
6. **Wait** 8 seconds (backoff^3)
7. **Final attempt** - if fails, raises exception

**Retried errors** (by default):
- `ConnectionError`: Network connectivity issues
- `TimeoutError`: Operation exceeded timeout

**Not retried**:
- `ValueError`: Invalid input
- `KeyError`: Missing data
- Other application errors

## Correlation IDs

Correlation IDs help track requests through logs for debugging:

```python
import logging
from pywats import pyWATS, enable_debug_logging

# Enable debug logging with correlation IDs
enable_debug_logging()

api = pyWATS(base_url="...", token="...")
api.product.get_product("ABC123")

# Logs show correlation IDs:
# [INFO] [a1b2c3d4] Getting product ABC123
# [INFO] [a1b2c3d4] Product retrieved successfully
```

Correlation IDs are **enabled by default**. To disable:

```python
from pywats.core.config import SyncConfig

config = SyncConfig(correlation_id_enabled=False)
api = pyWATS(base_url="...", token="...", sync_config=config)
```

## Complete Example

```python
from pywats import pyWATS
from pywats.core.config import SyncConfig, RetryConfig

# Production-ready configuration
config = SyncConfig(
    timeout=60.0,               # 1 minute timeout
    retry_enabled=True,         # Enable retry
    retry=RetryConfig(
        max_retries=3,
        backoff=2.0
    ),
    correlation_id_enabled=True  # Track requests
)

api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token",
    sync_config=config
)

# Operations now have:
# - 60 second timeout
# - Automatic retry on failures
# - Correlation IDs in logs

try:
    product = api.product.get_product("PART-001")
    print(f"Got product: {product.part_number}")
except TimeoutError:
    print("Request timed out after 60s")
except ConnectionError:
    print("Connection failed after 3 retries")
```

## Asynchronous API (AsyncWATS)

For high-performance applications that need concurrency:

```python
import asyncio
from pywats import AsyncWATS

async def main():
    async with AsyncWATS(base_url="...", token="...") as api:
        # Concurrent operations
        products_task = api.product.get_products()
        units_task = api.production.get_units()
        
        # Wait for both
        products, units = await asyncio.gather(products_task, units_task)

asyncio.run(main())
```

### When to Use Asynchronous API

- **High throughput**: Processing hundreds/thousands of requests
- **Concurrent workflows**: Multiple independent operations
- **Event-driven systems**: Webhooks, message queues
- **Integration with async frameworks**: FastAPI, aiohttp servers

## Performance Comparison

| Operation | Synchronous | Asynchronous |
|-----------|-------------|--------------|
| Single request | ~100ms | ~100ms (same) |
| 100 sequential requests | ~10s | ~10s (same) |
| 100 concurrent requests | ~10s | ~500ms (20x faster) |

**Verdict**: Use async for concurrent operations, sync for everything else.

## Migration Path

Starting with sync, migrating to async later:

```python
# Phase 1: Start with sync (easy development)
from pywats import pyWATS

api = pyWATS(base_url="...", token="...")
product = api.product.get_product("ABC123")

# Phase 2: Migrate to async when needed (high performance)
from pywats import AsyncWATS
import asyncio

async def main():
    async with AsyncWATS(base_url="...", token="...") as api:
        product = await api.product.get_product("ABC123")

asyncio.run(main())
```

## Best Practices

### Synchronous API

1. **Set appropriate timeouts**: Default 30s may be too short for complex queries
2. **Enable retry for production**: Network issues happen, retry handles them gracefully
3. **Use correlation IDs**: Essential for debugging production issues
4. **Keep it simple**: Don't overcomplicate unless you need async

### Asynchronous API

1. **Use context managers**: `async with AsyncWATS(...) as api`
2. **Batch concurrent operations**: `asyncio.gather()` for multiple requests
3. **Handle errors per task**: One failure shouldn't crash everything
4. **Set concurrency limits**: Don't overwhelm the server

## Troubleshooting

### TimeoutError

```python
# Problem: Operations timing out
api = pyWATS(base_url="...", token="...")  # Default 30s timeout

# Solution: Increase timeout
api = pyWATS(base_url="...", token="...", timeout=120.0)
```

### ConnectionError

```python
# Problem: Intermittent network issues
api = pyWATS(base_url="...", token="...")

# Solution: Enable retry
from pywats.core.config import SyncConfig, RetryConfig
config = SyncConfig(
    retry_enabled=True,
    retry=RetryConfig(max_retries=5, backoff=2.0)
)
api = pyWATS(base_url="...", token="...", sync_config=config)
```

### Cannot use pyWATS from within async context

```python
# Problem: Trying to use sync API in async function
async def my_function():
    api = pyWATS(...)  # ❌ RuntimeError!
    product = api.product.get_product("ABC123")

# Solution: Use AsyncWATS instead
async def my_function():
    async with AsyncWATS(...) as api:
        product = await api.product.get_product("ABC123")  # ✅
```

## See Also

- [Thread Safety Guide](thread-safety.md)
- [Integration Patterns](integration-patterns.md)
- [API Reference](../api/)
