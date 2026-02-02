Process Domain
==============

The Process domain manages manufacturing operation types and configurations in WATS. It enables you to:

- Manage test operations (ICT, FCT, End-of-Line test, etc.)
- Configure repair operations with fail codes and categories
- Track Work-In-Progress (WIP) operations
- Query operation metadata and routing information
- Validate process codes and operation types
- Access fail code hierarchies for repair tracking

**Use Cases:**
- Manufacturing routing and workflow configuration
- Test station setup and process selection
- Repair workstation configuration with fail codes
- WIP tracking and inventory management
- Process validation for test result submission
- Fail code lookup for repair logging

**Domain Health:** A (57/60) - Excellent, production-ready

---

Quick Start
-----------

Get All Processes
^^^^^^^^^^^^^^^^^

Retrieve all configured operations (cached for performance):

.. code-block:: python

   from pywats import pyWATS
   
   api = pyWATS(base_url="https://wats.example.com", token="token")
   
   # Get all processes (uses TTL cache - fast!)
   processes = api.process.get_processes()
   
   for process in processes:
       print(f"{process.code}: {process.name}")
       print(f"  Test: {process.is_test_operation}")
       print(f"  Repair: {process.is_repair_operation}")
       print(f"  WIP: {process.is_wip_operation}")

Filter by Operation Type
^^^^^^^^^^^^^^^^^^^^^^^^

Get only specific operation types:

.. code-block:: python

   # Get all test operations
   test_ops = api.process.get_test_operations()
   for op in test_ops:
       print(f"Test: {op.code} - {op.name}")
   
   # Get all repair operations
   repair_ops = api.process.get_repair_operations()
   for op in repair_ops:
       print(f"Repair: {op.code} - {op.name}")
   
   # Get all WIP operations
   wip_ops = api.process.get_wip_operations()
   for op in wip_ops:
       print(f"WIP: {op.code} - {op.name}")

Lookup Specific Process
^^^^^^^^^^^^^^^^^^^^^^^

Find a process by code or name:

.. code-block:: python

   # By code (int)
   process = api.process.get_process(100)
   if process:
       print(f"Found: {process.name}")
   
   # By name (str) - case insensitive
   process = api.process.get_process("End of line test")
   if process:
       print(f"Code: {process.code}")
   
   # Type-specific lookup
   test_op = api.process.get_test_operation(100)
   repair_op = api.process.get_repair_operation(500)

---

Core Concepts
-------------

Operation Types
^^^^^^^^^^^^^^^

WATS defines three operation types that control how units are processed:

.. code-block:: python

   from pywats import ProcessInfo
   
   # Test operations - for testing units
   # is_test_operation = True
   # Examples: ICT, FCT, End-of-Line, Burn-in
   
   # Repair operations - for repair/rework
   # is_repair_operation = True  
   # Examples: Repair, RMA repair, Field repair
   
   # WIP operations - for inventory tracking
   # is_wip_operation = True
   # Examples: WIP receiving, WIP storage

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.process.async_service.AsyncProcessService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. note::
   The repository layer is for advanced use cases. Most users should use the service layer above.

.. autoclass:: pywats.domains.process.async_repository.AsyncProcessRepository
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

ProcessInfo
^^^^^^^^^^^

.. autoclass:: pywats.domains.process.models.ProcessInfo
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Leverage TTL Caching**
   Process lists change infrequently. The default 5-minute cache provides excellent performance.

2. **Use Async for Concurrent Queries**
   When querying multiple operation types, use ``AsyncWATS`` and ``asyncio.gather()`` for parallel execution.

3. **Validate Before Submission**
   Always validate process codes before submitting test results or repair logs.

4. **Cache Repair Configurations**
   Repair configurations with fail codes are complex and change rarely. Load them once during startup.

5. **Use Type-Specific Lookups**
   Use ``get_test_operation()``, ``get_repair_operation()``, and ``get_wip_operation()`` for type safety.

---

Related Documentation
---------------------

- :doc:`../domains/production` - Production domain for submitting test results
- :doc:`../domains/report` - Report domain for querying test results
- :doc:`../getting-started` - Installation and setup

---

Domain Health
-------------

**Score:** 57/60 (A) - Excellent, production-ready

**Strengths:**
- Perfect Service→Repository→HttpClient architecture
- Comprehensive TTL caching with statistics
- Type-safe models with validation
- Excellent documentation with examples
