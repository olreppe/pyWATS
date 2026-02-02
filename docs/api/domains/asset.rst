Asset Domain
================

The Asset domain provides comprehensive equipment, fixture, and tool management capabilities for manufacturing environments in WATS. It enables you to:

- Track equipment with calibration and maintenance scheduling
- Monitor asset usage counts and trigger preventive maintenance
- Manage hierarchical asset structures (parent-child relationships)
- Record calibration and maintenance activities with audit logs
- Set alarm thresholds for usage limits and due dates
- Track asset state and location throughout the facility

**Use Cases:**
- Equipment calibration management (ISO 17025 compliance)
- Preventive maintenance scheduling based on usage
- Fixture life tracking and replacement planning
- Test equipment inventory and location tracking
- Usage-based maintenance triggers
- Hierarchical asset management (stations with fixtures and probes)

**Domain Health:** A- (52/60) - Very Good, production-ready

---

Quick Start
-----------

Basic Asset Operations
^^^^^^^^^^^^^^^^^^^^^^^

Get and manage assets:

.. code-block:: python

   from pywats import pyWATS
   
   api = pyWATS(base_url="https://wats.example.com", token="token")
   
   # Get all assets
   assets = await api.asset.get_assets()
   print(f"Total assets: {len(assets)}")
   
   # Get specific asset by serial number
   asset = await api.asset.get_asset(serial_number="DMM-001")
   if asset:
       print(f"Asset: {asset.asset_name}")
       print(f"  Serial: {asset.serial_number}")
       print(f"  State: {asset.state}")
       print(f"  Location: {asset.location}")

Create and Update Assets
^^^^^^^^^^^^^^^^^^^^^^^^^

Create new equipment assets:

.. code-block:: python

   from pywats.domains.asset import Asset, AssetState
   from uuid import UUID
   from datetime import datetime, timedelta
   
   # Create a new test equipment asset
   new_asset = await api.asset.create_asset(
       serial_number="SCOPE-042",
       type_id=UUID("12345678-1234-1234-1234-123456789012"),
       asset_name="Oscilloscope - Lab A",
       description="Tektronix MSO64 Mixed Signal Oscilloscope",
       location="Lab A - Station 3",
       state=AssetState.IN_OPERATION,
       part_number="MSO64",
       revision="1.0",
       last_calibration_date=datetime.now(),
       next_calibration_date=datetime.now() + timedelta(days=365)
   )
   print(f"Created: {new_asset.asset_name}")

Calibration Tracking
^^^^^^^^^^^^^^^^^^^^

Record calibration events:

.. code-block:: python

   from datetime import datetime, timedelta
   
   # Record standard calibration (sets lastCalibrationDate to now)
   await api.asset.record_calibration(
       serial_number="DMM-001",
       comment="Annual calibration performed"
   )
   
   # Record external calibration with custom dates (WATS 25.3+)
   await api.asset.record_calibration_external(
       serial_number="DMM-001",
       from_date=datetime.now() - timedelta(days=2),
       to_date=datetime.now() + timedelta(days=365),
       comment="Calibrated by external ISO 17025 lab"
   )
   
   # Find assets due for calibration
   assets = await api.asset.get_assets()
   due_date = datetime.now() + timedelta(days=30)
   
   for asset in assets:
       if asset.next_calibration_date and asset.next_calibration_date <= due_date:
           print(f"⚠️  {asset.serial_number} - Due: {asset.next_calibration_date}")

Async Usage for Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For concurrent operations and better performance:

.. code-block:: python

   import asyncio
   from pywats import AsyncWATS
   
   async def manage_multiple_assets():
       async with AsyncWATS(base_url="...", token="...") as api:
           # Get multiple assets concurrently
           dmm, scope, fixture = await asyncio.gather(
               api.asset.get_asset(serial_number="DMM-001"),
               api.asset.get_asset(serial_number="SCOPE-042"),
               api.asset.get_asset(serial_number="FIXTURE-100")
           )
           
           # Process results
           for asset in [dmm, scope, fixture]:
               if asset:
                   print(f"{asset.serial_number}: {asset.state}")
   
   asyncio.run(manage_multiple_assets())

---

Core Concepts
-------------

Type-Safe Enums
^^^^^^^^^^^^^^^

The Asset domain provides type-safe enums for IDE autocomplete and compile-time validation:

.. code-block:: python

   from pywats.domains.asset import AssetState, AssetLogType, AssetAlarmState, IntervalMode
   
   # Asset operational states
   AssetState.UNKNOWN          # 0 - Unknown
   AssetState.IN_OPERATION     # 1 - Active and operational
   AssetState.OK               # 1 - Alias for IN_OPERATION
   AssetState.IN_TRANSIT       # 2 - Being moved
   AssetState.IN_MAINTENANCE   # 3 - Under maintenance
   AssetState.IN_CALIBRATION   # 4 - Being calibrated
   AssetState.IN_STORAGE       # 5 - Stored/not in use
   AssetState.SCRAPPED         # 6 - Decommissioned
   
   # Alarm states (from Status endpoint)
   AssetAlarmState.OK          # 0 - No issues
   AssetAlarmState.WARNING     # 1 - Warning threshold exceeded
   AssetAlarmState.ALARM       # 2 - Alarm threshold exceeded
   
   # Log entry types
   AssetLogType.MESSAGE        # 0 - User message
   AssetLogType.REGISTER       # 1 - Asset created
   AssetLogType.UPDATE         # 2 - Property updated
   AssetLogType.RESET_COUNT    # 3 - Count reset
   AssetLogType.CALIBRATION    # 4 - Calibrated
   AssetLogType.MAINTENANCE    # 5 - Maintenance performed
   AssetLogType.STATE_CHANGE   # 6 - State changed
   
   # Interval modes (WATS 25.3+)
   IntervalMode.NORMAL         # 0 - Standard interval-based
   IntervalMode.UNLIMITED      # -1 - No limit required
   IntervalMode.EXTERNAL       # -2 - Managed externally

Asset Model
^^^^^^^^^^^

The ``Asset`` model represents physical equipment:

.. code-block:: python

   from pywats.domains.asset import Asset, AssetState
   from uuid import UUID
   
   # Key asset attributes
   asset = Asset(
       serial_number="FIXTURE-001",          # Required: Unique identifier
       type_id=UUID("..."),                   # Required: Asset type
       asset_name="Test Fixture #1",          # Display name
       part_number="FIX-PCB-2000",            # Part number
       revision="B",                          # Revision
       state=AssetState.IN_OPERATION,         # Current state
       location="Line 3 - Station 5",         # Physical location
       description="PCB test fixture",        # Description
       
       # Calibration tracking
       last_calibration_date=datetime(...),
       next_calibration_date=datetime(...),
       
       # Maintenance tracking
       last_maintenance_date=datetime(...),
       next_maintenance_date=datetime(...),
       
       # Usage tracking
       total_count=5000,                      # Lifetime usage
       running_count=250,                     # Since last cal/maintenance
       
       # Hierarchy
       parent_asset_id="STATION-001",         # Parent asset ID
       asset_children=[],                     # Child assets
   )

AssetType Model
^^^^^^^^^^^^^^^

Asset types define templates with calibration/maintenance schedules and thresholds:

.. code-block:: python

   from pywats.domains.asset import AssetType
   
   # Create asset type with intervals and thresholds
   asset_type = await api.asset.create_asset_type(
       type_name="Digital Multimeter",
       calibration_interval=365.0,          # Days between calibrations
       maintenance_interval=180.0,          # Days between maintenance
       running_count_limit=10000,           # Max uses before maintenance
       total_count_limit=100000,            # Total lifetime limit
       warning_threshold=80.0,              # Warning at 80%
       alarm_threshold=90.0,                # Alarm at 90%
       icon="measurement_device"            # UI icon
   )

---

Common Use Cases
----------------

Equipment Calibration Dashboard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Track calibration status across all equipment:

.. code-block:: python

   from pywats import AsyncWATS
   from pywats.domains.asset import AssetState
   from datetime import datetime, timedelta
   
   async with AsyncWATS(base_url="...", token="...") as api:
       # Get all assets
       assets = await api.asset.get_assets()
       
       now = datetime.now()
       overdue = []
       due_soon = []  # Due within 30 days
       current = []
       
       for asset in assets:
           if not asset.next_calibration_date:
               continue
           
           days_until = (asset.next_calibration_date - now).days
           
           if days_until < 0:
               overdue.append((asset, abs(days_until)))
           elif days_until <= 30:
               due_soon.append((asset, days_until))
           else:
               current.append(asset)
       
       # Print report
       print("CALIBRATION STATUS REPORT")
       print("=" * 60)
       print(f"\n❌ OVERDUE ({len(overdue)}):")
       for asset, days in overdue:
           print(f"   {asset.serial_number}: {days} days overdue")
       
       print(f"\n⚠️  DUE WITHIN 30 DAYS ({len(due_soon)}):")
       for asset, days in due_soon:
           print(f"   {asset.serial_number}: {days} days remaining")
       
       print(f"\n✅ CURRENT: {len(current)} assets")

Usage-Based Maintenance Tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Track asset usage and schedule maintenance:

.. code-block:: python

   # Increment usage count when asset is used
   await api.asset.increment_count(
       serial_number="FIXTURE-001",
       amount=1
   )
   
   # Check if maintenance is needed
   asset = await api.asset.get_asset(serial_number="FIXTURE-001")
   if asset and asset.running_count:
       # Get asset type to check limits
       types = await api.asset.get_asset_types()
       asset_type = next((t for t in types if t.type_id == asset.type_id), None)
       
       if asset_type and asset_type.running_count_limit:
           pct_used = (asset.running_count / asset_type.running_count_limit) * 100
           
           if pct_used >= 90:
               print(f"🔴 CRITICAL: {asset.serial_number} at {pct_used:.0f}% usage")
           elif pct_used >= 75:
               print(f"🟡 WARNING: {asset.serial_number} at {pct_used:.0f}% usage")
   
   # Record maintenance and reset counter
   await api.asset.record_maintenance(
       serial_number="FIXTURE-001",
       comment="Replaced worn contacts"
   )
   await api.asset.reset_running_count(
       serial_number="FIXTURE-001",
       comment="Reset after maintenance"
   )

Hierarchical Asset Management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Manage parent-child asset relationships:

.. code-block:: python

   from uuid import UUID
   
   # Create parent asset (test station)
   station = await api.asset.create_asset(
       serial_number="STATION-001",
       type_id=UUID("..."),
       asset_name="ICT Station #1",
       location="Line 3"
   )
   
   # Create child assets (fixtures)
   fixture = await api.asset.create_asset(
       serial_number="FIXTURE-A",
       type_id=UUID("..."),
       asset_name="Top Fixture",
       parent_asset_id=station.asset_id,  # Link to parent
       location="Line 3 - Station 1"
   )
   
   # Get all child assets
   children = await api.asset.get_child_assets(
       parent_serial="STATION-001",
       level=1  # Direct children only
   )
   
   print(f"Station {station.serial_number} has {len(children)} fixtures:")
   for child in children:
       print(f"  - {child.serial_number}: {child.asset_name}")

State Management and Monitoring
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Track and update asset operational states:

.. code-block:: python

   from pywats.domains.asset import AssetState
   
   # Set asset to maintenance state
   await api.asset.set_asset_state(
       state=AssetState.IN_MAINTENANCE,
       serial_number="FIXTURE-001"
   )
   
   # Get current status (includes alarm state)
   status = await api.asset.get_status(serial_number="FIXTURE-001")
   if status:
       print(f"Status: {status}")
   
   # Return to operation
   await api.asset.set_asset_state(
       state=AssetState.IN_OPERATION,
       serial_number="FIXTURE-001"
   )
   
   # Query assets by state
   in_calibration = await api.asset.get_assets_by_alarm_state(
       state=AssetState.IN_CALIBRATION
   )
   print(f"{len(in_calibration)} assets currently in calibration")

Asset Audit Log
^^^^^^^^^^^^^^^

Track all asset changes and activities:

.. code-block:: python

   # Get log entries for an asset
   asset = await api.asset.get_asset(serial_number="DMM-001")
   
   if asset and asset.asset_id:
       # Filter logs for this asset
       logs = await api.asset.get_asset_log(
           filter_str=f"assetId eq '{asset.asset_id}'",
           orderby="date desc",
           top=10
       )
       
       print(f"Recent activity for {asset.serial_number}:")
       for log in logs:
           print(f"  {log.date}: {log.log_type} - {log.comment}")
   
   # Add custom log message
   if asset and asset.asset_id:
       await api.asset.add_log_message(
           asset_id=asset.asset_id,
           message="Equipment relocated to Lab B",
           user="operator"
       )

---

Advanced Features
-----------------

External Calibration/Maintenance (WATS 25.3+)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For assets calibrated or maintained by external systems:

.. code-block:: python

   from datetime import datetime, timedelta
   
   # Record external calibration with custom date range
   # Useful when calibration cert shows specific dates
   await api.asset.record_calibration_external(
       serial_number="DMM-001",
       from_date=datetime(2026, 1, 15),   # When performed
       to_date=datetime(2027, 1, 15),      # Next due date
       comment="External lab calibration - Cert #CAL-2026-0042"
   )
   
   # Record external maintenance
   await api.asset.record_maintenance_external(
       serial_number="FIXTURE-001",
       from_date=datetime.now() - timedelta(days=3),
       to_date=datetime.now() + timedelta(days=90),
       comment="Vendor preventive maintenance"
   )

Direct Counter Management (WATS 25.3+)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set exact counter values (requires 'Edit Total count' permission):

.. code-block:: python

   # Set running count to specific value
   # Useful after manual counter reset or migration
   await api.asset.set_running_count(
       value=0,
       serial_number="FIXTURE-001"
   )
   
   # Set total count (lifetime usage)
   # Useful when migrating from legacy systems
   await api.asset.set_total_count(
       value=50000,
       serial_number="FIXTURE-001"
   )

OData Filtering
^^^^^^^^^^^^^^^

Advanced queries using OData filter syntax:

.. code-block:: python

   # Get assets in specific location
   lab_a_assets = await api.asset.get_assets(
       filter_str="location eq 'Lab A'"
   )
   
   # Get assets by state
   in_maintenance = await api.asset.get_assets(
       filter_str="state eq 3"  # AssetState.IN_MAINTENANCE
   )
   
   # Complex filter: calibration due in next 30 days
   from datetime import datetime, timedelta
   due_date = (datetime.now() + timedelta(days=30)).isoformat()
   
   due_soon = await api.asset.get_assets(
       filter_str=f"nextCalibrationDate le {due_date}"
   )
   
   # Pagination for large datasets
   page_1 = await api.asset.get_assets(top=100, skip=0)
   page_2 = await api.asset.get_assets(top=100, skip=100)

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.asset.async_service.AsyncAssetService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. note::
   The repository layer is for advanced use cases. Most users should use the service layer above.

.. autoclass:: pywats.domains.asset.async_repository.AsyncAssetRepository
   :members:
   :undoc-members:
   :show-inheritance:

---

Models
------

Asset Model
^^^^^^^^^^^

.. autoclass:: pywats.domains.asset.models.Asset
   :members:
   :undoc-members:
   :show-inheritance:

AssetType Model
^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.asset.models.AssetType
   :members:
   :undoc-members:
   :show-inheritance:

AssetLog Model
^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.asset.models.AssetLog
   :members:
   :undoc-members:
   :show-inheritance:

---

Enums
-----

AssetState
^^^^^^^^^^

.. autoclass:: pywats.domains.asset.enums.AssetState
   :members:
   :undoc-members:
   :show-inheritance:

AssetAlarmState
^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.asset.enums.AssetAlarmState
   :members:
   :undoc-members:
   :show-inheritance:

AssetLogType
^^^^^^^^^^^^

.. autoclass:: pywats.domains.asset.enums.AssetLogType
   :members:
   :undoc-members:
   :show-inheritance:

IntervalMode
^^^^^^^^^^^^

.. autoclass:: pywats.domains.asset.enums.IntervalMode
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Use Serial Numbers for Lookups**
   Serial numbers are more user-friendly than GUIDs. Use ``get_asset(serial_number="...")`` instead of tracking asset IDs.

2. **Leverage Hierarchical Structures**
   Model your physical equipment hierarchy (Station → Fixture → Probe) using parent-child relationships for better organization and tracking.

3. **Set Appropriate Thresholds**
   Configure warning (75-80%) and alarm (90-95%) thresholds on asset types to get proactive notifications before equipment requires service.

4. **Use External Calibration Methods for Compliance**
   For ISO 17025 or similar compliance, use ``record_calibration_external()`` to precisely record calibration certificate dates.

5. **Track Usage Counts for Preventive Maintenance**
   Increment asset usage counts during testing to enable usage-based maintenance triggers (e.g., every 10,000 cycles).

6. **Maintain Audit Logs**
   Use ``add_log_message()`` to record important events (repairs, relocations, modifications) for complete asset history.

7. **Leverage Async for Bulk Operations**
   When working with many assets, use ``AsyncWATS`` and ``asyncio.gather()`` to query/update multiple assets concurrently for significant performance gains.

8. **Filter Early with OData**
   Use OData ``$filter`` syntax to retrieve only relevant assets server-side instead of filtering in Python, reducing data transfer and improving performance.

---

Related Documentation
---------------------

- :doc:`../domains/production` - Production tracking (uses assets in test processes)
- :doc:`../domains/process` - Process configuration (links assets to test operations)
- :doc:`../getting-started` - Installation and setup

---

Domain Health
-------------

**Score:** 52/60 (A-) - Very Good, production-ready

See :doc:`../../domain_health/asset` for detailed domain health assessment.

**Strengths:**
- Clean Service→Repository→HttpClient architecture
- 100% ErrorHandler coverage across all methods
- Comprehensive calibration and maintenance tracking
- Type-safe enums (AssetState, AssetLogType, etc.)
- Good documentation with code examples
- WATS 25.3 features fully integrated

**Recent Improvements (Jan 2026):**
- Added ``Raises:`` documentation to all methods
- Enhanced with 3 practical code examples
- Migrated to ErrorHandler for consistent error handling
- Updated examples for WATS 25.3 external cal/maintenance features
