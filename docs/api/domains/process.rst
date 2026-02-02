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

Common Use Cases
----------------

Manufacturing Routing Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set up routing information for test stations:

.. code-block:: python

   from pywats import AsyncWATS
   
   async with AsyncWATS(base_url="...", token="...") as api:
       
       async def configure_test_station(station_name: str):
           """Configure available operations for a test station."""
           
           # Get all test operations
           test_ops = await api.process.get_test_operations()
           
           # Filter to station-specific operations
           # (Based on your routing logic)
           station_ops = [
               op for op in test_ops 
               if station_name in op.name or "End of Line" in op.name
           ]
           
           print(f"\n{station_name} - Available Operations:")
           for op in station_ops:
               print(f"  [{op.code}] {op.name}")
           
           return station_ops

Process Code Validation Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Validate process codes before report submission:

.. code-block:: python

   async def validate_and_submit_report(process_code: int, report_data: dict):
       """Validate process code before submitting test results."""
       
       # Verify process exists and is correct type
       process = await api.process.get_process(process_code)
       
       if not process:
           raise ValueError(f"Invalid process code: {process_code}")
       
       if not process.is_test_operation:
           raise ValueError(
               f"Process {process_code} is not a test operation. "
               f"Use repair workflow instead."
           )
       
       print(f"✓ Valid test operation: {process.name}")
       
       # Create and submit report with validated process
       report = api.report.create_uut_report(
           operation_type=process_code,
           **report_data
       )
       
       response = await api.report.submit_report(report)
       return response

Repair Workstation Setup
^^^^^^^^^^^^^^^^^^^^^^^^^

Configure repair stations with fail codes:

.. code-block:: python

   async def setup_repair_workstation():
       """Get repair operations and fail code hierarchies."""
       
       # Get all repair operations
       repair_ops = await api.process.get_repair_operations()
       
       for repair in repair_ops:
           print(f"\nRepair Operation: {repair.name} (Code: {repair.code})")
           
           # Note: Fail codes would typically be queried from
           # the repair configuration endpoint if available
           # This shows the basic operation structure
           
           if hasattr(repair, 'fail_categories'):
               for category in repair.fail_categories:
                   print(f"  Category: {category.name}")
                   for code in category.codes:
                       print(f"    - {code.name}")

Multi-Step Process Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Define and validate multi-step manufacturing workflow:

.. code-block:: python

   async def define_production_workflow(product_line: str):
       """Define complete production workflow with all operations."""
       
       # Define workflow steps for a product line
       workflow_steps = [
           ("PCB Test", 100),
           ("Assembly", 200),
           ("Functional Test", 300),
           ("End of Line Test", 400),
           ("Final Inspection", 500),
       ]
       
       # Validate all process codes exist
       validated_workflow = []
       
       for step_name, code in workflow_steps:
           process = await api.process.get_process(code)
           
           if not process:
               print(f"⚠ Warning: Process code {code} not found for {step_name}")
               continue
           
           validated_workflow.append({
               'step': step_name,
               'code': code,
               'name': process.name,
               'type': 'test' if process.is_test_operation else 'other'
           })
           
           print(f"✓ {step_name}: {process.name} (Code: {code})")
       
       return validated_workflow

Batch Process Queries
^^^^^^^^^^^^^^^^^^^^^^

Efficiently query multiple process types:

.. code-block:: python

   import asyncio
   
   async def get_all_operation_types():
       """Fetch all operation types concurrently for performance."""
       
       # Query all operation types in parallel
       test_ops, repair_ops, wip_ops = await asyncio.gather(
           api.process.get_test_operations(),
           api.process.get_repair_operations(),
           api.process.get_wip_operations()
       )
       
       # Generate operation summary
       print("\nOperation Summary:")
       print(f"  Test Operations: {len(test_ops)}")
       print(f"  Repair Operations: {len(repair_ops)}")
       print(f"  WIP Operations: {len(wip_ops)}")
       
       # Create lookup dictionary for fast access
       operation_lookup = {
           'test': {op.code: op for op in test_ops},
           'repair': {op.code: op for op in repair_ops},
           'wip': {op.code: op for op in wip_ops}
       }
       
       return operation_lookup

Process Compliance Checking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Verify process usage and compliance:

.. code-block:: python

   from datetime import datetime, timedelta
   from collections import Counter
   
   async def audit_process_usage():
       """Audit which processes are actively being used."""
       
       # Get all processes
       all_processes = await api.process.get_processes()
       
       # Query recent test reports
       recent_reports = await api.report.query_headers(
           odata_filter=f"start ge {datetime.now() - timedelta(days=30)}",
           top=1000
       )
       
       # Count process usage
       process_usage = Counter(r.process_code for r in recent_reports)
       
       # Identify unused processes
       all_codes = {p.code for p in all_processes}
       used_codes = set(process_usage.keys())
       unused_codes = all_codes - used_codes
       
       print("\nProcess Usage Analysis (Last 30 Days):")
       print(f"  Total Processes: {len(all_processes)}")
       print(f"  Actively Used: {len(used_codes)}")
       print(f"  Unused: {len(unused_codes)}")
       
       # Show most used processes
       print("\nTop 10 Most Used:")
       for code, count in process_usage.most_common(10):
           process = await api.process.get_process(code)
           name = process.name if process else "Unknown"
           print(f"  {code} ({name}): {count} reports")
       
       # List unused processes
       if unused_codes:
           print("\nUnused Processes:")
           for code in sorted(unused_codes)[:10]:
               process = await api.process.get_process(code)
               if process:
                   print(f"  {code}: {process.name}")

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
