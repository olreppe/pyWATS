Production Domain
================

The Production domain manages the entire lifecycle of manufacturing units in WATS. It enables you to:

- Create and track production units with serial numbers
- Manage unit phases throughout the production workflow
- Handle box build assembly operations (attaching/detaching child units)
- Allocate and manage serial numbers from pools
- Verify unit status and testing progression
- Track unit history and changes
- Manage production batches

**Use Cases:**
- Manufacturing execution and unit tracking
- Serial number allocation and management
- Box build assembly (parent/child relationships)
- Unit phase management (Under Production → Finalized → Shipped)
- Production verification and quality gates
- Batch tracking and traceability
- Assembly validation against box build templates

**Domain Health:** A (54/60) - Excellent, production-ready

---

Quick Start
-----------

Create and Track a Production Unit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a unit and track it through production:

.. code-block:: python

   from pywats import pyWATS, UnitPhaseFlag
   from pywats.domains.production import Unit
   
   api = pyWATS(base_url="https://wats.example.com", token="token")
   
   # Create a new production unit
   new_unit = Unit(
       serial_number="SN-2024-001234",
       part_number="WIDGET-001",
       revision="A",
       unit_phase_id=UnitPhaseFlag.UNDER_PRODUCTION
   )
   
   created = await api.production.create_units([new_unit])
   print(f"Created unit: {created[0].serial_number}")
   
   # Get unit information
   unit = await api.production.get_unit("SN-2024-001234", "WIDGET-001")
   print(f"Unit phase: {unit.unit_phase}")
   print(f"Status: {unit.unit_phase_id}")

Allocate Serial Numbers
^^^^^^^^^^^^^^^^^^^^^^^^

Allocate serial numbers from a configured pool:

.. code-block:: python

   # Allocate 100 serial numbers
   serial_numbers = await api.production.allocate_serial_numbers(
       type_name="MAIN_BOARD_SN",
       count=100,
       reference_pn="WIDGET-001",
       station_name="SMT-LINE-01"
   )
   
   print(f"Allocated {len(serial_numbers)} serial numbers:")
   for sn in serial_numbers[:5]:
       print(f"  {sn}")

Box Build Assembly
^^^^^^^^^^^^^^^^^^

Attach child units to parent assemblies:

.. code-block:: python

   # Add a PCBA as child to a main assembly
   success = await api.production.add_child_to_assembly(
       parent_serial="MAIN-ASSY-001",
       parent_part="MAIN-MODULE",
       child_serial="PCBA-001",
       child_part="PCBA-BOARD"
   )
   
   if success:
       print("Child unit attached successfully")
   
   # Verify assembly against box build template
   verification = await api.production.verify_assembly(
       serial_number="MAIN-ASSY-001",
       part_number="MAIN-MODULE",
       revision="A"
   )
   
   print(f"Assembly verification: {verification}")

Async Usage for Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For concurrent operations and better performance:

.. code-block:: python

   import asyncio
   from pywats import AsyncWATS, UnitPhaseFlag
   
   async def manage_production_batch():
       async with AsyncWATS(base_url="...", token="...") as api:
           # Create multiple units concurrently
           serials = [f"BATCH-2024-{i:04d}" for i in range(100)]
           
           units = [
               Unit(
                   serial_number=sn,
                   part_number="WIDGET-001",
                   revision="A",
                   unit_phase_id=UnitPhaseFlag.UNDER_PRODUCTION
               )
               for sn in serials
           ]
           
           # Create all units in one call
           created = await api.production.create_units(units)
           print(f"Created {len(created)} units")
           
           # Set phases concurrently
           await asyncio.gather(*[
               api.production.set_unit_phase(
                   sn, "WIDGET-001", UnitPhaseFlag.FINALIZED
               )
               for sn in serials[:10]
           ])
   
   asyncio.run(manage_production_batch())

---

Core Concepts
-------------

Type-Safe Enums
^^^^^^^^^^^^^^^

The Production domain provides type-safe enums for unit phases and serial number identifiers:

.. code-block:: python

   from pywats import UnitPhaseFlag, SerialNumberIdentifier
   
   # Unit phase flags - lifecycle states
   UnitPhaseFlag.UNKNOWN              # 1
   UnitPhaseFlag.UNDER_PRODUCTION     # 2
   UnitPhaseFlag.PRODUCTION_REPAIR    # 4
   UnitPhaseFlag.SERVICE_REPAIR       # 8
   UnitPhaseFlag.FINALIZED            # 16
   UnitPhaseFlag.SCRAPPED             # 32
   UnitPhaseFlag.EXTENDED_TEST        # 64
   UnitPhaseFlag.CUSTOMIZATION        # 128
   UnitPhaseFlag.REPAIRED             # 256
   UnitPhaseFlag.MISSING              # 512
   UnitPhaseFlag.IN_STORAGE           # 1024
   UnitPhaseFlag.SHIPPED              # 2048
   
   # Serial number identifier types
   SerialNumberIdentifier.SERIAL_NUMBER  # 0 - Standard S/N
   SerialNumberIdentifier.MAC_ADDRESS    # 1 - MAC address
   SerialNumberIdentifier.IMEI           # 2 - IMEI number

Unit Model
^^^^^^^^^^

The ``Unit`` model represents a production unit:

.. code-block:: python

   from pywats.domains.production import Unit
   
   unit = Unit(
       serial_number="SN-001",           # Unique identifier
       part_number="WIDGET-001",          # Product part number
       revision="A",                      # Product revision
       parent_serial_number="ASSY-100",   # Parent (if child unit)
       batch_number="BATCH-2024-Q1",      # Production batch
       unit_phase_id=16,                  # Current phase (Finalized)
       unit_phase="Finalized",            # Phase name (read-only)
       process_code=1001,                 # Current process
       current_location="FINAL_TEST",     # Physical location
       sub_units=[],                      # Child units (if assembly)
   )

Unit Phases
^^^^^^^^^^^

Units move through predefined phases during their lifecycle:

.. code-block:: python

   # Get all available phases
   phases = await api.production.get_phases()
   for phase in phases:
       print(f"{phase.name} (ID={phase.phase_id})")
   
   # Set unit phase by ID
   await api.production.set_unit_phase(
       "SN-001", "WIDGET-001", 16  # Finalized
   )
   
   # Set phase by enum (recommended)
   await api.production.set_unit_phase(
       "SN-001", "WIDGET-001", UnitPhaseFlag.FINALIZED
   )
   
   # Set phase by name
   await api.production.set_unit_phase(
       "SN-001", "WIDGET-001", "Finalized"
   )

Box Build Assembly
^^^^^^^^^^^^^^^^^^

Units can have parent-child relationships for assemblies:

.. code-block:: python

   # Get unit with assembly structure
   unit = await api.production.get_unit("MAIN-ASSY-001", "MAIN-MODULE")
   
   # Access child units
   for child in unit.sub_units:
       print(f"Child: {child.serial_number} ({child.part_number})")
   
   # Parent reference
   if unit.parent_serial_number:
       print(f"Parent: {unit.parent_serial_number}")

---

Common Use Cases
----------------

Production Unit Lifecycle
^^^^^^^^^^^^^^^^^^^^^^^^^

Track a unit from creation through production:

.. code-block:: python

   from pywats import pyWATS, UnitPhaseFlag
   from pywats.domains.production import Unit
   
   api = pyWATS(base_url="...", token="...")
   
   # 1. Create unit
   unit = Unit(
       serial_number="SN-2024-NEW-001",
       part_number="WIDGET-001",
       revision="A",
       unit_phase_id=UnitPhaseFlag.UNDER_PRODUCTION
   )
   
   created = await api.production.create_units([unit])
   print(f"✓ Created: {created[0].serial_number}")
   
   # 2. Move through production phases
   phases = [
       ("ICT", UnitPhaseFlag.UNDER_PRODUCTION),
       ("FCT", UnitPhaseFlag.UNDER_PRODUCTION),
       ("FINAL_TEST", UnitPhaseFlag.UNDER_PRODUCTION),
       ("QC", UnitPhaseFlag.FINALIZED),
   ]
   
   for process_name, phase in phases:
       await api.production.set_unit_phase(
           "SN-2024-NEW-001", "WIDGET-001", phase
       )
       print(f"✓ Completed: {process_name}")
   
   # 3. Verify unit status
   grade = await api.production.get_unit_grade(
       "SN-2024-NEW-001", "WIDGET-001"
   )
   
   if grade.all_processes_passed_last_run:
       print("✓ All tests passed!")

Serial Number Management
^^^^^^^^^^^^^^^^^^^^^^^^

Manage serial numbers throughout production:

.. code-block:: python

   # Configure serial number type
   types = await api.production.get_serial_number_types()
   for sn_type in types:
       print(f"{sn_type.name}: {sn_type.format}")
   
   # Allocate serial numbers
   serials = await api.production.allocate_serial_numbers(
       type_name="MAIN_BOARD_SN",
       count=50,
       reference_pn="WIDGET-001",
       station_name="SMT-01"
   )
   
   print(f"Allocated {len(serials)} serial numbers")
   
   # Find serial numbers in range
   range_serials = await api.production.find_serial_numbers_in_range(
       type_name="MAIN_BOARD_SN",
       from_serial="MB-001000",
       to_serial="MB-001100"
   )
   
   # Find by reference
   ref_serials = await api.production.find_serial_numbers_by_reference(
       type_name="MAIN_BOARD_SN",
       reference_serial="PARENT-001",
       reference_part="WIDGET-001"
   )

Box Build Assembly Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete assembly workflow with validation:

.. code-block:: python

   # 1. Create parent assembly
   parent = Unit(
       serial_number="MAIN-ASSY-001",
       part_number="MAIN-MODULE",
       revision="A",
       unit_phase_id=UnitPhaseFlag.UNDER_PRODUCTION
   )
   await api.production.create_units([parent])
   
   # 2. Create child units (PCBAs, cables, etc.)
   children = [
       ("PCBA-001", "PCBA-BOARD"),
       ("PSU-001", "POWER-SUPPLY"),
       ("CABLE-001", "DATA-CABLE"),
   ]
   
   child_units = [
       Unit(
           serial_number=sn,
           part_number=pn,
           revision="A",
           unit_phase_id=UnitPhaseFlag.FINALIZED  # Children should be finalized
       )
       for sn, pn in children
   ]
   await api.production.create_units(child_units)
   
   # 3. Attach children to parent
   for child_sn, child_pn in children:
       success = await api.production.add_child_to_assembly(
           parent_serial="MAIN-ASSY-001",
           parent_part="MAIN-MODULE",
           child_serial=child_sn,
           child_part=child_pn
       )
       print(f"✓ Attached {child_sn}")
   
   # 4. Verify assembly against box build template
   verification = await api.production.verify_assembly(
       serial_number="MAIN-ASSY-001",
       part_number="MAIN-MODULE",
       revision="A"
   )
   
   if verification:
       print("✓ Assembly verified against template")
   
   # 5. Finalize assembly
   await api.production.set_unit_phase(
       "MAIN-ASSY-001", "MAIN-MODULE", UnitPhaseFlag.FINALIZED
   )

Batch Production Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^

Track production batches:

.. code-block:: python

   from pywats.domains.production import ProductionBatch
   
   # Create a production batch
   batch = ProductionBatch(
       batch_number="BATCH-2024-Q1-001",
       batch_size=1000
   )
   
   created_batch = await api.production.create_batch(batch)
   print(f"Created batch: {created_batch.batch_number}")
   
   # Create units with batch reference
   batch_units = [
       Unit(
           serial_number=f"BATCH-{i:04d}",
           part_number="WIDGET-001",
           revision="A",
           batch_number="BATCH-2024-Q1-001",
           unit_phase_id=UnitPhaseFlag.UNDER_PRODUCTION
       )
       for i in range(100)
   ]
   
   await api.production.create_units(batch_units)
   
   # Query batches
   batches = await api.production.get_batches(
       part_number="WIDGET-001"
   )
   
   for batch in batches:
       print(f"Batch {batch.batch_number}: {batch.batch_size} units")

Unit Verification
^^^^^^^^^^^^^^^^^

Verify unit status and test progression:

.. code-block:: python

   # Simple pass/fail check
   is_passing = await api.production.is_unit_passing(
       serial_number="SN-001",
       part_number="WIDGET-001"
   )
   
   if is_passing:
       print("✓ Unit is passing all tests")
   else:
       print("✗ Unit has failures")
   
   # Detailed verification grade
   grade = await api.production.get_unit_grade(
       serial_number="SN-001",
       part_number="WIDGET-001",
       revision="A"
   )
   
   print(f"Status: {grade.status}")
   print(f"Grade: {grade.grade}")
   print(f"First run pass: {grade.all_processes_passed_first_run}")
   print(f"Correct order: {grade.all_processes_executed_in_correct_order}")
   print(f"No repairs: {grade.no_repairs}")
   
   # Process-by-process verification
   for result in grade.results:
       print(f"Process {result.process_name}:")
       print(f"  Status: {result.status}")
       print(f"  Total tests: {result.total_count}")
       print(f"  Failures: {result.non_passed_count}")
       print(f"  Repairs: {result.repair_count}")

---

Advanced Features
-----------------

Unit History Tracking
^^^^^^^^^^^^^^^^^^^^^

Track all changes to a unit:

.. code-block:: python

   # Get unit change history
   history = await api.production.get_unit_history(
       serial_number="SN-001",
       part_number="WIDGET-001"
   )
   
   print(f"Unit change history ({len(history)} records):")
   for change in history:
       if change.new_unit_phase_id:
           print(f"Phase changed to: {change.new_unit_phase_id}")
       if change.new_part_number:
           print(f"Part number changed to: {change.new_part_number}")
       if change.new_parent_serial_number:
           print(f"Parent changed to: {change.new_parent_serial_number}")

Complex Assembly Operations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Advanced assembly management:

.. code-block:: python

   # Remove all children from assembly (disassembly)
   success = await api.production.remove_all_children_from_assembly(
       parent_serial="MAIN-ASSY-001",
       parent_part="MAIN-MODULE"
   )
   
   if success:
       print("✓ Assembly disassembled")
   
   # Remove specific child
   await api.production.remove_child_from_assembly(
       parent_serial="MAIN-ASSY-001",
       parent_part="MAIN-MODULE",
       child_serial="PCBA-001",
       child_part="PCBA-BOARD"
   )
   
   # Replace a child component
   async def replace_component(parent, child_old, child_new):
       # Remove old
       await api.production.remove_child_from_assembly(
           parent_serial=parent[0],
           parent_part=parent[1],
           child_serial=child_old[0],
           child_part=child_old[1]
       )
       # Add new
       await api.production.add_child_to_assembly(
           parent_serial=parent[0],
           parent_part=parent[1],
           child_serial=child_new[0],
           child_part=child_new[1]
       )
   
   await replace_component(
       ("MAIN-ASSY-001", "MAIN-MODULE"),
       ("PCBA-OLD", "PCBA-BOARD"),
       ("PCBA-NEW", "PCBA-BOARD")
   )

Serial Number Import/Export
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bulk serial number operations:

.. code-block:: python

   # Import serial numbers from CSV
   with open("serial_numbers.csv", "rb") as f:
       csv_content = f.read()
   
   success = await api.production.import_serial_numbers(
       file_content=csv_content,
       content_type="text/csv"
   )
   
   if success:
       print("✓ Serial numbers imported")
   
   # Export serial numbers to CSV
   csv_data = await api.production.export_serial_numbers(
       type_name="MAIN_BOARD_SN",
       state="Available",
       format="csv"
   )
   
   if csv_data:
       with open("exported_sns.csv", "wb") as f:
           f.write(csv_data)
       print("✓ Serial numbers exported")

Phase Management with Caching
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Efficiently work with unit phases:

.. code-block:: python

   # Load phases once (cached internally)
   phases = await api.production.get_phases()
   
   # Get specific phase
   finalized = await api.production.get_phase(phase_id=16)
   print(f"Phase: {finalized.name}")
   
   # Lookup by name
   under_prod = await api.production.get_phase(name="Under production")
   
   # Lookup by code
   shipped = await api.production.get_phase(code="Shipped")
   
   # Convert phase identifier to ID
   phase_id = await api.production.get_phase_id("Finalized")  # Returns 16
   phase_id = await api.production.get_phase_id(UnitPhaseFlag.FINALIZED)  # Returns 16
   
   # Force refresh from server
   phases = await api.production.get_phases(force_refresh=True)

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.production.async_service.AsyncProductionService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. autoclass:: pywats.domains.production.async_repository.AsyncProductionRepository
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

Unit Models
^^^^^^^^^^^

.. autoclass:: pywats.domains.production.models.Unit
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.production.models.UnitChange
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.production.models.UnitPhase
   :members:
   :undoc-members:
   :show-inheritance:

Verification Models
^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.production.models.UnitVerification
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.production.models.UnitVerificationGrade
   :members:
   :undoc-members:
   :show-inheritance:

Serial Number Models
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.production.models.SerialNumberType
   :members:
   :undoc-members:
   :show-inheritance:

Batch Models
^^^^^^^^^^^^

.. autoclass:: pywats.domains.production.models.ProductionBatch
   :members:
   :undoc-members:
   :show-inheritance:

Enums
-----

.. automodule:: pywats.domains.production.enums
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Use Type-Safe Enums for Phases**
   Always use ``UnitPhaseFlag`` enum instead of magic numbers for better IDE support, type safety, and code readability.

   .. code-block:: python

      # Good - Type-safe with autocomplete
      await api.production.set_unit_phase(
          "SN-001", "WIDGET-001", UnitPhaseFlag.FINALIZED
      )
      
      # Avoid - Magic numbers
      await api.production.set_unit_phase("SN-001", "WIDGET-001", 16)

2. **Validate Child Units Before Assembly**
   Ensure child units are in "Finalized" phase before attaching to parent assemblies. This prevents incomplete components from being assembled.

   .. code-block:: python

      # Verify child is finalized
      child = await api.production.get_unit(child_sn, child_pn)
      if child.unit_phase_id != UnitPhaseFlag.FINALIZED:
          await api.production.set_unit_phase(
              child_sn, child_pn, UnitPhaseFlag.FINALIZED
          )
      
      # Then attach
      await api.production.add_child_to_assembly(parent_sn, parent_pn, child_sn, child_pn)

3. **Use Batch Operations for Bulk Unit Creation**
   When creating multiple units, use ``create_units()`` instead of multiple individual calls for better performance.

   .. code-block:: python

      # Good - Single bulk operation
      units = [Unit(serial_number=f"SN-{i:04d}", ...) for i in range(100)]
      await api.production.create_units(units)
      
      # Avoid - Multiple individual calls
      for i in range(100):
          await api.production.create_units([Unit(...)])

4. **Cache Phase Information**
   Phase lists are static configuration. Use the built-in caching to avoid repeated API calls.

   .. code-block:: python

      # Phases are cached after first call
      phases = await api.production.get_phases()  # Fetches from server
      phases = await api.production.get_phases()  # Uses cache
      
      # Force refresh only when needed
      phases = await api.production.get_phases(force_refresh=True)

5. **Verify Assembly Against Templates**
   Always verify assemblies against box build templates to ensure all required components are present.

   .. code-block:: python

      # After assembly, verify against template
      verification = await api.production.verify_assembly(
          serial_number=parent_sn,
          part_number=parent_pn,
          revision=revision
      )
      
      if not verification:
          print("Warning: Assembly verification failed")

6. **Track Unit History for Traceability**
   Use unit history to maintain full traceability for quality and compliance requirements.

   .. code-block:: python

      # Get complete unit history
      history = await api.production.get_unit_history(sn, pn)
      
      # Log critical changes
      for change in history:
          if change.new_unit_phase_id:
              log_audit_trail(f"Phase change: {change.new_unit_phase_id}")

7. **Handle Serial Number Allocation Carefully**
   Serial numbers are precious resources. Only allocate what you need and implement proper error handling.

   .. code-block:: python

      try:
          serials = await api.production.allocate_serial_numbers(
              type_name="MAIN_BOARD_SN",
              count=needed_count,
              reference_pn=part_number,
              station_name=station_id
          )
      except Exception as e:
          logger.error(f"Serial allocation failed: {e}")
          # Implement fallback or retry logic

---

Related Documentation
---------------------

- :doc:`../domains/product` - Product domain (defines box build templates)
- :doc:`../domains/report` - Report domain (test results for units)
- :doc:`../domains/analytics` - Analytics domain (production metrics)
- :doc:`../getting-started` - Installation and setup

---

Domain Health
-------------

**Score:** 54/60 (A) - Excellent, production-ready

See :doc:`../../domain_health/production` for detailed domain health assessment.

**Strengths:**
- Perfect Service→Repository→HttpClient architecture
- 100% ErrorHandler coverage
- Comprehensive unit lifecycle management
- Excellent box build assembly support
- Type-safe enums for better DX
- Strong serial number management

**Key Features:**
- 25+ service methods covering all production scenarios
- Full unit lifecycle support (creation through shipping)
- Robust assembly operations with validation
- Flexible serial number allocation and tracking
- Comprehensive verification and grading
- Production batch management

**Recent Improvements (Jan 2026):**
- Added ``Raises:`` sections to all 25+ service methods
- Enhanced model documentation with examples
- Improved test coverage for assembly operations
- Added comprehensive phase management with caching
