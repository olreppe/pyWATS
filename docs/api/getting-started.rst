Getting Started
===============

This guide covers installation, configuration, and basic usage of pyWATS.

Installation
------------

Library Only
^^^^^^^^^^^^

For Python scripts and applications:

.. code-block:: bash

   pip install pywats-api

With GUI Client
^^^^^^^^^^^^^^^

For desktop applications with Qt-based GUI:

.. code-block:: bash

   pip install pywats-api[client]

Headless Client
^^^^^^^^^^^^^^^

For servers and embedded systems (no Qt/GUI):

.. code-block:: bash

   pip install pywats-api[client-headless]

API Initialization
------------------

Basic Setup
^^^^^^^^^^^

.. code-block:: python

   from pywats import pyWATS

   api = pyWATS(
       base_url="https://your-wats-server.com",
       token="your_base64_token"  # Base64 of "username:password"
   )

   # Test connection
   if api.test_connection():
       print(f"Connected! Version: {api.get_version()}")

Configuration Options
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pywats import pyWATS, RetryConfig
   from pywats.core.exceptions import ErrorMode

   api = pyWATS(
       base_url="https://your-wats-server.com",
       token="your_token",
       timeout=60,                          # Request timeout (seconds)
       error_mode=ErrorMode.STRICT,         # STRICT or LENIENT
       retry_enabled=True,                  # Auto-retry on transient failures
       retry_config=RetryConfig(            # Custom retry settings
           max_attempts=5,
           base_delay=2.0
       ),
   )

Error Handling
--------------

STRICT Mode (Default)
^^^^^^^^^^^^^^^^^^^^^

Raises exceptions for 404 and empty responses:

.. code-block:: python

   from pywats import NotFoundError

   try:
       product = api.product.get_product("NONEXISTENT")
   except NotFoundError:
       print("Product not found")

LENIENT Mode
^^^^^^^^^^^^

Returns None for 404 and empty responses:

.. code-block:: python

   from pywats.core.exceptions import ErrorMode

   api = pyWATS(..., error_mode=ErrorMode.LENIENT)
   
   product = api.product.get_product("NONEXISTENT")
   if product is None:
       print("Product not found")

Automatic Retry
---------------

The library automatically retries requests on transient failures:

- Connection errors
- Timeout errors  
- HTTP 429 (Too Many Requests)
- HTTP 500, 502, 503, 504 (Server errors)

Only idempotent methods (GET, PUT, DELETE) are retried. POST is never retried.

.. code-block:: python

   from pywats import RetryConfig

   # Custom retry configuration
   config = RetryConfig(
       max_attempts=5,
       base_delay=2.0,
       max_delay=60.0,
       jitter=True,
   )

   api = pyWATS(..., retry_config=config)

   # Check retry statistics
   print(api.retry_config.stats)

Next Steps
----------

- :doc:`api/index` - Full API reference
- :doc:`domains/index` - Domain services documentation
- :doc:`models/index` - Data models documentation
