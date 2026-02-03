Client Services
===============

.. module:: pywats_client
   :synopsis: Client-side services for GUI applications and file conversion

The ``pywats_client`` package provides services for building GUI applications,
managing file conversions, and handling client-side logging infrastructure.

This documentation covers client-specific services that are separate from the
main API layer (``pywats``).

.. toctree::
   :maxdepth: 2
   :caption: Client Services:

   logging

Overview
--------

Client services are designed for:

* **GUI Applications**: Desktop tools that interact with WATS servers
* **File Conversion**: Converting test data files between formats
* **Client-Side Logging**: Separate log management for client applications

Key Differences from API Layer
-------------------------------

+-------------------+----------------------------------+----------------------------------+
| Aspect            | API Layer (``pywats``)           | Client Layer (``pywats_client``) |
+===================+==================================+==================================+
| **Purpose**       | HTTP API communication           | GUI/conversion services          |
+-------------------+----------------------------------+----------------------------------+
| **Logging**       | Server request logging           | Client operations & conversions  |
+-------------------+----------------------------------+----------------------------------+
| **Users**         | Python scripts, automation       | Desktop applications, tools      |
+-------------------+----------------------------------+----------------------------------+
| **Deployment**    | Servers, containers, CI/CD       | User workstations                |
+-------------------+----------------------------------+----------------------------------+

Client Service Categories
--------------------------

Logging Services
^^^^^^^^^^^^^^^^

See :doc:`logging` for detailed documentation on:

* Client application logging configuration
* Conversion log management
* Log file location strategies
* Cleanup and retention policies

Quick Start: Client Logging
----------------------------

.. code-block:: python

   from pywats_client.core.logging import setup_client_logging, get_client_log_path

   # Configure client logging (separate from API logging)
   setup_client_logging(level="INFO", app_name="MyWATSTool")

   # Get log file location
   log_path = get_client_log_path("MyWATSTool")
   print(f"Logs: {log_path}")

Quick Start: Conversion Logs
-----------------------------

.. code-block:: python

   from pywats_client.converters.conversion_log import ConversionLog, ConversionLogEntry
   from pathlib import Path
   from datetime import datetime, timezone

   # Create conversion log
   log = ConversionLog()

   # Log conversion event
   entry = ConversionLogEntry(
       timestamp=datetime.now(timezone.utc),
       converter="TERADYNE",
       status="SUCCESS",
       input_file=Path("data.txt"),
       output_file=Path("report.xml")
   )
   log.add_entry(entry)

   # Save log
   log.save(Path("conversions.json"))

See Also
--------

* :doc:`../api/logging` - API-layer logging for server requests
* :doc:`../guides/observability` - Observability patterns and best practices

Architecture Notes
------------------

The client layer is intentionally separated from the API layer to:

1. **Isolate Concerns**: Client logs don't mix with API request logs
2. **Support Offline Tools**: Conversion tools work without WATS server connection
3. **Enable Desktop Apps**: GUI applications have different logging needs than scripts
4. **Manage File Operations**: Conversion logs track file transformations independently

This separation ensures that:

* API scripts remain simple and focused on HTTP communication
* Desktop tools can manage their own logging independently
* Conversion operations are auditable even when offline
* Log analysis can distinguish client operations from server requests
