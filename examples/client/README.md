# pyWATS Client Examples

This directory contains comprehensive examples demonstrating best practices for using the pyWATS client library.

## Quick Start

If you're new to pyWATS, start here:
1. **[Getting Started](../getting_started/)** - Basic setup and first API calls
2. **[Configuration](configuration.py)** - How to configure the client for different environments
3. **[Error Handling](error_handling.py)** - Robust error handling patterns

## Examples Overview

### Core Client Operations

#### [Attachment I/O](attachment_io.py)
**Topics:** File uploads, downloads, metadata management, bulk operations

Learn how to:
- Load attachments from files with automatic MIME type detection
- Save attachments to disk with atomic write operations
- Handle file size limits and validation
- Process multiple attachments in batch
- Delete source files after reading
- Handle file access and format errors

**Key Functions:**
- `AttachmentIO.from_file()` - Load attachments
- `AttachmentIO.save()` - Save to disk
- `AttachmentIO.save_multiple()` - Bulk operations
- `load_attachment()` / `save_attachment()` - Convenience functions

---

#### [Error Handling](error_handling.py)
**Topics:** Exception handling, retry strategies, graceful degradation, error logging

Learn how to:
- Handle specific exception types appropriately
- Implement retry strategies with exponential backoff
- Use error modes (STRICT vs LENIENT) effectively
- Handle client-specific errors (file, queue, converter errors)
- Implement graceful degradation patterns
- Log errors with troubleshooting hints

**Key Patterns:**
- `retry_with_exponential_backoff()` - Automatic retry logic
- `comprehensive_error_handler()` - Production-ready error handling
- Error mode selection for different use cases

---

#### [Configuration](configuration.py)
**Topics:** Environment configs, authentication, connection settings, performance tuning

Learn how to:
- Configure clients for different environments (dev, staging, prod)
- Manage authentication securely with environment variables
- Set timeouts and retry parameters
- Configure proxy settings
- Tune performance settings
- Enable debug logging
- Load configuration from files

**Key Concepts:**
- Environment-specific configurations
- Secure credential management
- Performance vs reliability trade-offs
- Logging configuration

---

#### [Batch Operations](batch_operations.py)
**Topics:** Bulk processing, parallel execution, progress tracking, optimization

Learn how to:
- Process multiple items efficiently
- Use parallel processing with ThreadPoolExecutor
- Track progress for long-running operations
- Handle errors in batch processing with retries
- Use chunking for very large datasets
- Optimize updates by skipping unchanged items
- Manage rate limits

**Key Techniques:**
- `bulk_create_parallel()` - Parallel batch processing
- `batch_with_progress_tracking()` - Progress monitoring
- `batch_with_error_handling()` - Robust batch operations
- `batch_with_chunking()` - Process large datasets
- `batch_update_optimization()` - Skip unnecessary updates

---

## Running the Examples

### Prerequisites
```bash
# Install pyWATS
pip install pywats

# Set environment variables
export PYWATS_API_URL="https://your-api.example.com"
export PYWATS_API_TOKEN="your-api-token"
```

### Run Individual Examples
```bash
# Attachment I/O examples
python examples/client/attachment_io.py

# Error handling patterns
python examples/client/error_handling.py

# Configuration examples
python examples/client/configuration.py

# Batch operations
python examples/client/batch_operations.py
```

### Modify for Your Use Case
Each example is self-contained and can be modified to fit your specific needs. Replace the simulated API calls with actual pyWATS client operations.

---

## Best Practices Summary

### Error Handling
✅ **DO:**
- Use STRICT mode in production for fail-fast behavior
- Use LENIENT mode in scripts for exploratory work
- Implement retry logic for transient errors (ServerError, ConnectionError, TimeoutError)
- Log errors with context for debugging

❌ **DON'T:**
- Retry authentication or validation errors
- Ignore exceptions without logging
- Use bare `except:` clauses
- Hard-code credentials

### Performance
✅ **DO:**
- Use parallel processing for I/O-bound operations
- Implement progress tracking for long-running jobs
- Use chunking for very large datasets
- Skip unnecessary updates by checking current state
- Monitor rate limits and add delays if needed

❌ **DON'T:**
- Process large batches sequentially
- Ignore rate limits
- Keep large datasets in memory unnecessarily

### Configuration
✅ **DO:**
- Use environment variables for credentials
- Configure different settings for dev/staging/prod
- Set appropriate timeouts for your use case
- Enable debug logging during development
- Document configuration requirements

❌ **DON'T:**
- Hard-code credentials in source code
- Use production credentials in development
- Commit credentials to version control
- Use overly long timeouts globally

### File Operations
✅ **DO:**
- Check file size limits before loading
- Handle file access errors gracefully
- Use atomic write operations (provided by AttachmentIO)
- Clean up temporary files
- Validate file formats

❌ **DON'T:**
- Load files without size checks
- Ignore file access errors
- Leave temporary files after use
- Assume all files are valid

---

## Additional Resources

- **[API Documentation](../../docs/)** - Full API reference
- **[Getting Started Guide](../../docs/guides/quickstart.md)** - Quick start tutorial
- **[Troubleshooting Guide](../../docs/guides/troubleshooting.md)** - Common issues and solutions
- **[Performance Guide](../../docs/guides/performance.md)** - Performance optimization tips

---

## Contributing

Found an issue or have a suggestion for a new example? Please open an issue or submit a pull request!

### Example Template

When creating new examples, follow this structure:

```python
"""
Example: [Brief description]

This example demonstrates:
- Topic 1
- Topic 2
- Topic 3

Prerequisites:
- Requirement 1
- Requirement 2
"""

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_function():
    """Brief description of what this demonstrates."""
    logger.info("=== Example Name ===")
    
    # Implementation with comments
    # ...


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Example Title")
    print("="*60)
    
    example_function()
    
    print("\n" + "="*60)
    print("Example completed!")
    print("="*60 + "\n")
```

---

**Last Updated:** 2026-02-02
