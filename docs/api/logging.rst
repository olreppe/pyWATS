Logging
=======

.. module:: pywats.core.logging
   :synopsis: Unified logging infrastructure with correlation IDs and structured formats

The pyWATS logging module provides a unified, production-ready logging infrastructure
with support for correlation tracking, structured JSON output, file rotation, and
contextual logging.

Key Features
------------

* **Correlation IDs**: Automatic request correlation across distributed systems
* **Structured Logging**: JSON output with metadata for log aggregation
* **File Rotation**: Automatic log rotation based on size
* **Context Management**: Thread-safe logging context with scope control
* **Flexible Configuration**: Text or JSON formats with customizable handlers

Quick Start
-----------

.. code-block:: python

   from pywats.core.logging import configure_logging, get_logger

   # Configure logging once at application startup
   configure_logging(level="INFO", format="text")

   # Get logger for your module
   logger = get_logger(__name__)

   # Log messages with automatic correlation IDs
   logger.info("Application started")
   logger.error("Error occurred", exc_info=True)

Configuration
-------------

.. autofunction:: configure_logging

**Example: Text Format with Console Output**

.. code-block:: python

   from pywats.core.logging import configure_logging

   # Human-readable logs for development
   configure_logging(
       level="DEBUG",
       format="text",
       enable_correlation_ids=True
   )

**Example: JSON Format with File Rotation**

.. code-block:: python

   from pathlib import Path
   from pywats.core.logging import configure_logging

   # Structured logs for production (10MB files, 5 backups)
   configure_logging(
       level="INFO",
       format="json",
       file_path=Path("/var/log/pywats/app.log"),
       rotate_size_mb=10,
       rotate_backups=5
   )

**Example: Custom Handlers**

.. code-block:: python

   import logging
   from pywats.core.logging import configure_logging, StructuredFormatter

   # Send structured logs to external service
   handler = logging.handlers.SysLogHandler(address=('logs.example.com', 514))
   handler.setFormatter(StructuredFormatter())

   configure_logging(
       level="INFO",
       handlers=[handler]
   )

Logger Creation
---------------

.. autofunction:: get_logger

**Example: Module-Level Logger**

.. code-block:: python

   from pywats.core.logging import get_logger

   # Create logger for your module
   logger = get_logger(__name__)

   # Use throughout module
   class MyService:
       def process(self) -> None:
           logger.info("Processing started")
           # ... processing logic ...
           logger.info("Processing completed")

**Example: Controlling Library Logging**

.. code-block:: python

   import logging

   # Reduce verbosity of pyWATS logs
   logging.getLogger('pywats').setLevel(logging.WARNING)

   # Your application logs remain at INFO
   from pywats.core.logging import get_logger
   logger = get_logger(__name__)
   logger.info("This still logs")  # ✅ Visible

Contextual Logging
------------------

Add structured context to all log messages within a scope:

.. autofunction:: set_logging_context
.. autofunction:: clear_logging_context
.. autofunction:: get_logging_context

**Example: Request Context**

.. code-block:: python

   from pywats.core.logging import set_logging_context, clear_logging_context, get_logger

   logger = get_logger(__name__)

   # Add request context
   set_logging_context(request_id="req-12345", user_id="alice")

   logger.info("Processing request")
   # JSON output includes: {"request_id": "req-12345", "user_id": "alice", "message": "Processing request"}

   # Clear when done
   clear_logging_context()

**Example: Scoped Context with Context Manager**

.. autoclass:: LoggingContext
   :members:

.. code-block:: python

   from pywats.core.logging import LoggingContext, get_logger

   logger = get_logger(__name__)

   with LoggingContext(operation="data_import", batch_id="batch-789"):
       logger.info("Starting import")  # Includes operation and batch_id
       # ... import logic ...
       logger.info("Import completed")  # Still includes context

   logger.info("Outside context")  # No operation or batch_id

File Rotation
-------------

.. autoclass:: FileRotatingHandler
   :members:

**Example: Custom Rotation Settings**

.. code-block:: python

   from pathlib import Path
   from pywats.core.logging import FileRotatingHandler, StructuredFormatter

   # Rotate every 50MB, keep 10 backups
   handler = FileRotatingHandler(
       file_path=Path("/var/log/pywats/debug.log"),
       max_bytes=50 * 1024 * 1024,  # 50MB
       backup_count=10
   )
   handler.setFormatter(StructuredFormatter())
   handler.setLevel("DEBUG")

Structured Formatting
---------------------

.. autoclass:: StructuredFormatter
   :members:

**Example: JSON Output with Metadata**

.. code-block:: python

   import logging
   from pywats.core.logging import StructuredFormatter

   handler = logging.StreamHandler()
   handler.setFormatter(StructuredFormatter())

   logger = logging.getLogger(__name__)
   logger.addHandler(handler)

   logger.info("User logged in", extra={"user_id": "alice", "ip": "192.168.1.1"})
   # Output: {"timestamp": "2026-02-03T14:45:00Z", "level": "INFO", "user_id": "alice", ...}

Correlation Tracking
--------------------

.. autoclass:: CorrelationFilter
   :members:

**Example: Distributed Tracing**

.. code-block:: python

   import logging
   from pywats.core.logging import CorrelationFilter

   # Add correlation IDs to all log records
   logger = logging.getLogger(__name__)
   correlation_filter = CorrelationFilter()
   logger.addFilter(correlation_filter)

   # Each log message gets unique correlation ID
   logger.info("Request received")  # correlation_id: abc-123-def
   logger.info("Processing")        # correlation_id: abc-123-def (same request)

Integration Patterns
--------------------

Production Deployment
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pathlib import Path
   from pywats.core.logging import configure_logging

   # Production configuration
   configure_logging(
       level="INFO",
       format="json",
       file_path=Path("/var/log/pywats/production.log"),
       rotate_size_mb=100,
       rotate_backups=30,
       enable_correlation_ids=True,
       enable_context=True
   )

Development with Debug Logging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pywats.core.logging import configure_logging

   # Development configuration
   configure_logging(
       level="DEBUG",
       format="text",
       enable_correlation_ids=False  # Simpler output for debugging
   )

Web Application with Request Tracing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pywats.core.logging import LoggingContext, get_logger

   logger = get_logger(__name__)

   def handle_request(request):
       with LoggingContext(
           request_id=request.id,
           user=request.user.username,
           path=request.path
       ):
           logger.info("Request received")
           # ... process request ...
           logger.info("Request completed")

See Also
--------

* :doc:`../guides/observability` - Observability patterns and best practices
* :doc:`client/logging` - Client-side logging and conversion logs
* :doc:`../guides/production` - Production deployment guide

API Reference
-------------

Complete API documentation for all logging components.

Functions
^^^^^^^^^

.. autofunction:: configure_logging
.. autofunction:: get_logger
.. autofunction:: set_logging_context
.. autofunction:: clear_logging_context
.. autofunction:: get_logging_context

Classes
^^^^^^^

.. autoclass:: LoggingContext
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: FileRotatingHandler
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: StructuredFormatter
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: CorrelationFilter
   :members:
   :undoc-members:
   :show-inheritance:

Constants
^^^^^^^^^

.. data:: DEFAULT_FORMAT
   :type: str
   
   Default text format with correlation ID:
   ``"[%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s"``

.. data:: DEFAULT_FORMAT_DETAILED
   :type: str
   
   Detailed text format with timestamp and correlation ID:
   ``"%(asctime)s [%(levelname)s] [%(correlation_id)s] %(name)s: %(message)s"``
