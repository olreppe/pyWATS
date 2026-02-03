Client Logging
==============

.. module:: pywats_client.core.logging
   :synopsis: Client-side logging configuration for GUI applications

.. module:: pywats_client.converters.conversion_log
   :synopsis: Conversion log management for file transformation tracking

The client logging module provides logging infrastructure specifically designed
for GUI applications, desktop tools, and file conversion operations. This is
separate from the API-layer logging in ``pywats.core.logging``.

Key Features
------------

* **Separate Log Files**: Client logs don't mix with API request logs
* **Conversion Tracking**: Audit trail for file format conversions
* **Automatic Cleanup**: Retention policies for old log files
* **Platform-Aware Paths**: Log locations follow OS conventions
* **Offline Operations**: Works without WATS server connection

Quick Start
-----------

**Client Application Logging:**

.. code-block:: python

   from pywats_client.core.logging import setup_client_logging

   # Configure logging for your client application
   setup_client_logging(level="INFO", app_name="MyWATSTool")

**Conversion Tracking:**

.. code-block:: python

   from pywats_client.converters.conversion_log import ConversionLog, ConversionLogEntry
   from pathlib import Path
   from datetime import datetime, timezone

   log = ConversionLog()
   entry = ConversionLogEntry(
       timestamp=datetime.now(timezone.utc),
       converter="TERADYNE",
       status="SUCCESS",
       input_file=Path("data.txt"),
       output_file=Path("report.xml")
   )
   log.add_entry(entry)
   log.save(Path("conversions.json"))

Client Logging Configuration
-----------------------------

.. autofunction:: pywats_client.core.logging.setup_client_logging

**Example: Desktop Application Logging**

.. code-block:: python

   from pywats_client.core.logging import setup_client_logging, get_client_log_path
   import logging

   # Configure client logging
   setup_client_logging(level="DEBUG", app_name="WATSConverter")

   # Get logger
   logger = logging.getLogger(__name__)

   # Logs go to platform-specific location
   logger.info("Application started")

   # Check log file location
   log_path = get_client_log_path("WATSConverter")
   print(f"Logs saved to: {log_path}")

**Example: Production Client Configuration**

.. code-block:: python

   from pywats_client.core.logging import setup_client_logging

   # Production settings with rotation
   setup_client_logging(
       level="INFO",
       app_name="WATSDesktopTool",
       max_bytes=50 * 1024 * 1024,  # 50MB
       backup_count=10
   )

Log File Locations
------------------

.. autofunction:: pywats_client.core.logging.get_client_log_path

**Platform-Specific Paths:**

.. code-block:: python

   from pywats_client.core.logging import get_client_log_path

   # Windows: C:\Users\<user>\AppData\Local\MyApp\Logs\client.log
   # Linux: ~/.local/share/MyApp/logs/client.log
   # macOS: ~/Library/Logs/MyApp/client.log

   path = get_client_log_path("MyApp")

Conversion Log Management
--------------------------

.. autofunction:: pywats_client.core.logging.get_conversion_log_dir

**Example: Conversion Log Directory**

.. code-block:: python

   from pywats_client.core.logging import get_conversion_log_dir

   # Get conversion log directory
   conv_dir = get_conversion_log_dir()
   print(f"Conversion logs: {conv_dir}")

   # Save conversion log
   log_file = conv_dir / "conversions_2026-02-03.json"

Conversion Log API
------------------

.. autoclass:: pywats_client.converters.conversion_log.ConversionLogEntry
   :members:
   :undoc-members:

**Example: Creating Log Entries**

.. code-block:: python

   from pywats_client.converters.conversion_log import ConversionLogEntry
   from pathlib import Path
   from datetime import datetime, timezone

   # Success entry
   success_entry = ConversionLogEntry(
       timestamp=datetime.now(timezone.utc),
       converter="TERADYNE",
       status="SUCCESS",
       input_file=Path("/data/input.txt"),
       output_file=Path("/output/report.xml"),
       error_message=None
   )

   # Error entry
   error_entry = ConversionLogEntry(
       timestamp=datetime.now(timezone.utc),
       converter="GENRAD",
       status="ERROR",
       input_file=Path("/data/corrupt.dat"),
       output_file=None,
       error_message="Invalid file format: missing header"
   )

.. autoclass:: pywats_client.converters.conversion_log.ConversionLog
   :members:
   :undoc-members:
   :show-inheritance:

**Example: Managing Conversion Logs**

.. code-block:: python

   from pywats_client.converters.conversion_log import ConversionLog, ConversionLogEntry
   from pathlib import Path
   from datetime import datetime, timezone

   # Create log
   log = ConversionLog()

   # Add multiple entries
   log.add_entry(ConversionLogEntry(
       timestamp=datetime.now(timezone.utc),
       converter="TERADYNE",
       status="SUCCESS",
       input_file=Path("test1.txt"),
       output_file=Path("test1.xml")
   ))

   log.add_entry(ConversionLogEntry(
       timestamp=datetime.now(timezone.utc),
       converter="TERADYNE",
       status="SUCCESS",
       input_file=Path("test2.txt"),
       output_file=Path("test2.xml")
   ))

   # Save to file
   log.save(Path("conversions.json"))

   # Load existing log
   loaded_log = ConversionLog.load(Path("conversions.json"))

   # Get statistics
   stats = loaded_log.get_statistics()
   print(f"Total: {stats['total_entries']}")
   print(f"Success: {stats['success_count']}")
   print(f"Errors: {stats['error_count']}")
   print(f"Success Rate: {stats['success_rate']:.1%}")

**Example: Filtering Conversion Logs**

.. code-block:: python

   from pywats_client.converters.conversion_log import ConversionLog
   from pathlib import Path
   from datetime import datetime, timezone, timedelta

   log = ConversionLog.load(Path("conversions.json"))

   # Filter by converter
   teradyne_entries = log.filter_by_converter("TERADYNE")

   # Filter by status
   errors = log.filter_by_status("ERROR")

   # Filter by date range
   yesterday = datetime.now(timezone.utc) - timedelta(days=1)
   recent_entries = log.filter_by_date_range(start_date=yesterday)

   # Get error messages
   for entry in errors:
       print(f"Error in {entry.input_file}: {entry.error_message}")

Integration Patterns
--------------------

Desktop Application with Conversion Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pywats_client.core.logging import setup_client_logging, get_conversion_log_dir
   from pywats_client.converters.conversion_log import ConversionLog
   from pathlib import Path
   import logging

   # Setup client logging
   setup_client_logging(level="INFO", app_name="WATSConverter")
   logger = logging.getLogger(__name__)

   # Initialize conversion log
   conv_log_path = get_conversion_log_dir() / "conversions.json"
   conversion_log = ConversionLog.load(conv_log_path) if conv_log_path.exists() else ConversionLog()

   # Application logic
   logger.info("Starting conversion batch")
   # ... perform conversions, add entries to conversion_log ...
   conversion_log.save(conv_log_path)
   logger.info("Conversion batch completed")

Batch Conversion with Error Handling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pywats_client.converters.conversion_log import ConversionLog, ConversionLogEntry
   from pathlib import Path
   from datetime import datetime, timezone
   import logging

   logger = logging.getLogger(__name__)
   log = ConversionLog()

   for input_file in Path("input").glob("*.txt"):
       try:
           # Attempt conversion
           output_file = Path("output") / f"{input_file.stem}.xml"
           convert_file(input_file, output_file)

           # Log success
           log.add_entry(ConversionLogEntry(
               timestamp=datetime.now(timezone.utc),
               converter="TERADYNE",
               status="SUCCESS",
               input_file=input_file,
               output_file=output_file
           ))
       except Exception as e:
           # Log error
           logger.error(f"Conversion failed: {input_file}", exc_info=True)
           log.add_entry(ConversionLogEntry(
               timestamp=datetime.now(timezone.utc),
               converter="TERADYNE",
               status="ERROR",
               input_file=input_file,
               output_file=None,
               error_message=str(e)
           ))

   # Save log and print stats
   log.save(Path("batch_conversion.json"))
   stats = log.get_statistics()
   logger.info(f"Batch complete: {stats['success_count']}/{stats['total_entries']} succeeded")

See Also
--------

* :doc:`../logging` - API-layer logging for server communication
* :ref:`Observability Guide <observability>` - Observability patterns (coming soon)

API Reference
-------------

Complete API documentation for client logging components.

Core Logging Functions
^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: pywats_client.core.logging.setup_client_logging
.. autofunction:: pywats_client.core.logging.get_client_log_path
.. autofunction:: pywats_client.core.logging.get_conversion_log_dir

Conversion Log Classes
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats_client.converters.conversion_log.ConversionLogEntry
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats_client.converters.conversion_log.ConversionLog
   :members:
   :undoc-members:
   :show-inheritance:
