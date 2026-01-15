Domain Services
===============

pyWATS is organized into domain-specific services, each handling a different aspect of the WATS system.

.. toctree::
   :maxdepth: 2

   product
   asset
   production
   report
   analytics
   rootcause
   software
   scim
   process

Overview
--------

Each domain service is accessed as a property on the main :class:`~pywats.pywats.pyWATS` class:

.. code-block:: python

   from pywats import pyWATS

   api = pyWATS(base_url="...", token="...")

   # Access domain services
   api.product     # Product management
   api.asset       # Asset management
   api.production  # Production/unit management
   api.report      # Report queries and submission
   api.analytics   # Yield statistics and analysis
   api.rootcause   # Ticketing system
   api.software    # Software distribution
   api.scim        # User provisioning (SCIM)
   api.process     # Process/operation types

Service Pattern
---------------

All domain services follow a consistent pattern:

- **get_* methods** - Retrieve single or multiple items
- **create_* methods** - Create new items
- **update_* methods** - Update existing items  
- **delete_* methods** - Remove items
- **query_* methods** - Search with filters
