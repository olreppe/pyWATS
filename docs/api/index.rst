pyWATS API Reference
====================

Welcome to the pyWATS API reference documentation. This documentation is auto-generated from the source code docstrings.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   api/index
   domains/index
   models/index
   logging
   client
   changelog

Quick Links
-----------

* :doc:`getting-started` - Installation and basic usage
* :doc:`api/index` - Main pyWATS class reference
* :doc:`domains/index` - Domain service reference (Product, Asset, Report, etc.)
* :doc:`models/index` - Data model reference
* :doc:`logging` - API logging infrastructure
* :doc:`client` - Client services (GUI, conversions)

Installation
------------

.. code-block:: bash

   pip install pywats-api

Basic Usage
-----------

.. code-block:: python

   from pywats import pyWATS

   # Initialize
   api = pyWATS(
       base_url="https://your-wats-server.com",
       token="your_base64_token"
   )

   # Access domains
   products = api.product.get_products()
   product = api.product.get_product("WIDGET-001")

   # Query reports
   from pywats import WATSFilter
   filter = WATSFilter(part_number="WIDGET-001", period_count=30)
   headers = api.report.query_uut_headers(filter)

Additional Resources
====================

**Object Model Diagrams** (Comprehensive class diagrams with all members)

* `Report Object Models Overview <REPORT_OBJECT_MODELS.md>`_ - Complete guide to report structures
* `UUTReport Object Model <UUT_OBJECT_MODEL.md>`_ - Unit Under Test report class diagram
* `UURReport Object Model <UUR_OBJECT_MODEL.md>`_ - Unit Under Repair report class diagram

**Class References** (Auto-generated from source code)

* `Complete API Class Reference <class_reference/pywats_api_complete.md>`_ - All pyWATS API classes in one file
* `Class Reference Index <class_reference/README.md>`_ - Browse by component/domain

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
