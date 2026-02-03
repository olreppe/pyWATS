Analytics Domain
================

The Analytics domain provides comprehensive data analysis and visualization capabilities for manufacturing test results in WATS. It enables you to:

- Calculate yield metrics and First Pass Yield (FPY)
- Analyze measurement data with statistical metrics (Cpk, standard deviation, etc.)
- Visualize production flow through Unit Flow analysis
- Track process performance with OEE (Overall Equipment Effectiveness)
- Monitor real-time alarm and notification logs

**Use Cases:**
- Manufacturing performance dashboards
- Trend analysis and process optimization
- Quality control and Six Sigma initiatives
- Real-time monitoring and alerting
- Failure analysis and root cause investigation

**Domain Health:** A (54/60) - Excellent, production-ready

---

Quick Start
-----------

Basic Yield Calculation
^^^^^^^^^^^^^^^^^^^^^^^

Get yield statistics for a product over the last 7 days:

.. code-block:: python

   from pywats import pyWATS, WATSFilter, StatusFilter
   
   api = pyWATS(base_url="https://wats.example.com", token="token")
   
   # Create filter for last 7 days
   filter_obj = WATSFilter(
       part_number="WIDGET-001",
       status=StatusFilter.ALL,  # Type-safe enum
       days=7
   )
   
   # Get yield data
   yield_result = api.analytics.get_yield(filter_obj)
   
   print(f"Yield: {yield_result.yield_pct:.1f}%")
   print(f"Passed: {yield_result.passed}")
   print(f"Failed: {yield_result.failed}")
   print(f"Total: {yield_result.total}")

Measurement Analysis
^^^^^^^^^^^^^^^^^^^^

Analyze measurement data with statistical metrics:

.. code-block:: python

   from pywats import MeasurementPath
   
   # Get aggregated measurements for specific test steps
   path = MeasurementPath("Numeric Limit Tests/3.3V Rail")
   measurements = api.analytics.get_aggregated_measurements(
       filter_obj,
       measurement_paths=path
   )
   
   for meas in measurements:
       print(f"{meas.step_name}:")
       print(f"  Average: {meas.avg:.3f}")
       print(f"  Cpk: {meas.cpk:.2f}")
       print(f"  Std Dev: {meas.std_dev:.3f}")

Async Usage for Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For concurrent requests and better performance:

.. code-block:: python

   import asyncio
   from pywats import AsyncWATS, WATSFilter
   
   async def analyze_multiple_products():
       async with AsyncWATS(base_url="...", token="...") as api:
           # Create filters for different products
           widget_filter = WATSFilter(part_number="WIDGET-001", days=7)
           board_filter = WATSFilter(part_number="BOARD-PCB-2000", days=7)
           
           # Run queries concurrently - much faster!
           widget_yield, board_yield = await asyncio.gather(
               api.analytics.get_yield(widget_filter),
               api.analytics.get_yield(board_filter)
           )
           
           print(f"Widget yield: {widget_yield.yield_pct:.1f}%")
           print(f"Board yield: {board_yield.yield_pct:.1f}%")
   
   asyncio.run(analyze_multiple_products())

---

Core Concepts
-------------

Type-Safe Enums
^^^^^^^^^^^^^^^

The Analytics domain provides type-safe enums for IDE autocomplete and compile-time validation:

.. code-block:: python

   from pywats import StatusFilter, RunFilter, StepType, CompOperator
   
   # Status filter - filter by test result status
   StatusFilter.PASSED      # "P" - Passed tests only
   StatusFilter.FAILED      # "F" - Failed tests only
   StatusFilter.ERROR       # "E" - Error/terminated tests
   StatusFilter.TERMINATED  # "T" - Terminated tests
   StatusFilter.ABORTED     # "A" - Aborted tests
   StatusFilter.ALL         # "" - All tests
   
   # Run filter - filter by run type
   RunFilter.FIRST_RUN      # "F" - First run only
   RunFilter.RE_RUN         # "R" - Re-runs only
   RunFilter.ALL            # "" - All runs
   
   # Step types for filtering specific test steps
   StepType.NUMERIC_LIMIT_TEST
   StepType.STRING_VALUE_TEST
   StepType.PASS_FAIL_TEST
   StepType.MULTIPLE_NUMERIC_LIMIT_TEST

WATSFilter Object
^^^^^^^^^^^^^^^^^

The ``WATSFilter`` object is central to querying analytics data:

.. code-block:: python

   from pywats import WATSFilter, StatusFilter, RunFilter
   from datetime import datetime, timedelta
   
   # Time-based filtering
   filter1 = WATSFilter(
       part_number="WIDGET-001",
       days=7  # Last 7 days
   )
   
   filter2 = WATSFilter(
       part_number="WIDGET-001",
       start_date_time=datetime(2026, 1, 1),
       end_date_time=datetime(2026, 1, 31)
   )
   
   # Status and run filtering
   filter3 = WATSFilter(
       part_number="WIDGET-001",
       status=StatusFilter.FAILED,  # Only failed tests
       run_filter=RunFilter.FIRST_RUN,  # First runs only
       days=30
   )
   
   # Process-specific filtering
   filter4 = WATSFilter(
       part_number="WIDGET-001",
       process_code="FINAL_TEST",  # Specific process
       days=14
   )

Measurement Paths
^^^^^^^^^^^^^^^^^

Reference test steps using friendly path format:

.. code-block:: python

   from pywats import MeasurementPath
   
   # Single step
   path1 = MeasurementPath("Voltage Tests/5V Rail")
   
   # Multiple steps (list)
   paths = [
       MeasurementPath("Voltage Tests/3.3V Rail"),
       MeasurementPath("Voltage Tests/5V Rail"),
       MeasurementPath("Temperature/Ambient")
   ]
   
   measurements = api.analytics.get_aggregated_measurements(
       filter_obj,
       measurement_paths=paths
   )

---

Common Use Cases
----------------

Dashboard - Product Yield Overview
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a manufacturing dashboard showing yield for multiple products:

.. code-block:: python

   from pywats import pyWATS, WATSFilter, StatusFilter
   from datetime import datetime, timedelta
   
   api = pyWATS(base_url="...", token="...")
   
   products = ["WIDGET-001", "BOARD-PCB-2000", "ASSEMBLY-TOP"]
   time_periods = [1, 7, 30]  # Days
   
   print("Product Yield Dashboard")
   print("=" * 60)
   
   for product in products:
       print(f"\n{product}:")
       for days in time_periods:
           filter_obj = WATSFilter(
               part_number=product,
               status=StatusFilter.ALL,
               days=days
           )
           yield_data = api.analytics.get_yield(filter_obj)
           print(f"  Last {days:2d} days: {yield_data.yield_pct:5.1f}% "
                 f"({yield_data.passed}/{yield_data.total})")

Trend Analysis with Measurements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Track measurement trends over time:

.. code-block:: python

   from pywats import MeasurementPath
   from datetime import datetime, timedelta
   
   # Analyze voltage measurement stability over 4 weeks
   for week in range(4):
       start = datetime.now() - timedelta(weeks=week+1)
       end = datetime.now() - timedelta(weeks=week)
       
       filter_obj = WATSFilter(
           part_number="WIDGET-001",
           start_date_time=start,
           end_date_time=end
       )
       
       measurements = api.analytics.get_aggregated_measurements(
           filter_obj,
           measurement_paths=MeasurementPath("Voltage/3.3V Rail")
       )
       
       if measurements:
           meas = measurements[0]
           print(f"Week {4-week}: Avg={meas.avg:.3f}V "
                 f"Cpk={meas.cpk:.2f} (n={meas.count})")

Process Comparison
^^^^^^^^^^^^^^^^^^

Compare yield across different manufacturing processes:

.. code-block:: python

   processes = ["ICT", "FUNCTIONAL", "FINAL_TEST"]
   
   for process in processes:
       filter_obj = WATSFilter(
           part_number="WIDGET-001",
           process_code=process,
           days=7
       )
       yield_data = api.analytics.get_yield(filter_obj)
       print(f"{process:15s}: {yield_data.yield_pct:5.1f}% FPY")

Failure Analysis
^^^^^^^^^^^^^^^^

Identify most common failure modes:

.. code-block:: python

   from pywats import StatusFilter
   
   # Get failed tests
   filter_obj = WATSFilter(
       part_number="WIDGET-001",
       status=StatusFilter.FAILED,
       days=7
   )
   
   # Get serial numbers of failed units
   failures = api.analytics.get_serial_number_history(filter_obj)
   
   print(f"Failed units in last 7 days: {len(failures)}")
   for fail in failures[:10]:  # Show first 10
       print(f"  {fail.serial_number} - {fail.execution_time}")

---

Advanced Features
-----------------

Dynamic Yield Analysis
^^^^^^^^^^^^^^^^^^^^^^

Multi-dimensional yield analysis with grouping:

.. code-block:: python

   from pywats import DimensionBuilder
   
   # Group by process and operation
   dimensions = DimensionBuilder.build(["process", "operation"])
   
   yield_data = api.analytics.get_dynamic_yield(
       filter_obj,
       dimensions=dimensions
   )
   
   # Results grouped by process and operation
   for item in yield_data:
       print(f"{item.process_name} / {item.operation_name}: "
             f"{item.yield_pct:.1f}%")

OEE (Overall Equipment Effectiveness)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Calculate OEE for manufacturing stations:

.. code-block:: python

   oee_data = api.analytics.get_oee_analysis(
       filter_obj,
       include_availability=True,
       include_performance=True,
       include_quality=True
   )
   
   print(f"OEE: {oee_data.oee:.1f}%")
   print(f"  Availability: {oee_data.availability:.1f}%")
   print(f"  Performance: {oee_data.performance:.1f}%")
   print(f"  Quality: {oee_data.quality:.1f}%")

Unit Flow Visualization
^^^^^^^^^^^^^^^^^^^^^^^

Track unit movement through production:

.. code-block:: python

   # Get unit flow data for visualization
   flow_data = api.analytics.get_unit_flow(
       filter_obj,
       include_paths=True
   )
   
   # Shows unit movement between processes
   for flow in flow_data:
       print(f"{flow.from_process} -> {flow.to_process}: "
             f"{flow.unit_count} units")

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.analytics.async_service.AsyncAnalyticsService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. autoclass:: pywats.domains.analytics.async_repository.AsyncAnalyticsRepository
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

Yield Data
^^^^^^^^^^

.. autoclass:: pywats.domains.analytics.models.YieldData
   :members:
   :undoc-members:
   :show-inheritance:

Measurement Models
^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.analytics.models.AggregatedMeasurement
   :members:
   :undoc-members:
   :show-inheritance:

Process Models
^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.analytics.models.ProcessInfo
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.analytics.models.LevelInfo
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.analytics.models.ProductGroup
   :members:
   :undoc-members:
   :show-inheritance:

Enums
-----

.. automodule:: pywats.domains.analytics.enums
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Use Type-Safe Enums**
   Always use ``StatusFilter``, ``RunFilter``, etc. instead of magic strings for better IDE support and fewer errors.

2. **Leverage Async for Performance**
   When querying multiple products or time periods, use ``AsyncWATS`` and ``asyncio.gather()`` for significant performance gains.

3. **Cache Process Lists**
   Process and operation lists change infrequently. Cache them instead of querying on every request.

4. **Filter Early**
   Use specific ``WATSFilter`` criteria to reduce data transfer and improve response times.

5. **Handle Large Datasets**
   For large datasets, consider using ``start_date_time``/``end_date_time`` instead of ``days`` for more precise control.

---

Related Documentation
---------------------

- :doc:`../usage/analytics-domain` - Detailed usage guide with more examples
- :doc:`../domains/report` - Report domain (data source for analytics)
- :doc:`../domains/production` - Production tracking
- :doc:`../getting-started` - Installation and setup

---

Domain Health
-------------

**Score:** 54/60 (A) - Excellent, production-ready

See :doc:`../../domain_health/analytics` for detailed domain health assessment.

**Strengths:**
- Perfect Service→Repository→HttpClient architecture
- 100% ErrorHandler coverage
- Comprehensive documentation with examples
- Type-safe enums for better DX
- Clean internal API separation

**Recent Improvements (Jan 2026):**
- Added ``Raises:`` sections to all 20 service methods
- Enhanced model documentation with examples
- Improved test coverage for POST analytics methods
