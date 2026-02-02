Report Domain
=============

The Report domain provides comprehensive test report creation, submission, and querying capabilities for WATS. It enables you to:

- Create UUT (Unit Under Test) reports with hierarchical step structures
- Create UUR (Unit Under Repair) reports for tracking repairs and rework
- Submit reports in WSJF (JSON) and WSXF (XML) formats
- Query report headers using OData filters
- Download full reports and attachments
- Track unit testing and repair history

**Use Cases:**
- Automated test equipment (ATE) integration
- Manufacturing test data submission
- Repair and rework tracking
- Test result analysis and traceability
- Historical test data retrieval
- Failure documentation and root cause analysis

**Domain Health:** A- (53/60) - Very Good, production-ready

---

Quick Start
-----------

Create and Submit a Simple Test Report (Active Mode)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a basic UUT report using the service factory method. In Active mode (default), 
status is automatically calculated based on measurements and limits:

.. code-block:: python

   from pywats import AsyncWATS
   from pywats.domains.report import ImportMode, set_import_mode
   from pywats.shared.enums import CompOp
   from datetime import datetime
   
   async with AsyncWATS(base_url="https://wats.example.com", token="your-token") as api:
       # Active mode is the default - status auto-calculated from measurements
       set_import_mode(ImportMode.Active)
       
       # Create UUT report using service factory
       report = api.report.create_uut_report(
           operator="TestOperator",
           part_number="WIDGET-001",
           revision="A",
           serial_number="SN-2026-12345",
           operation_type=100,  # FCT test operation
       )
       
       # Get root sequence and add test steps
       root = report.get_root_sequence_call()
       
       # Add numeric test - status auto-calculated from limits
       root.add_numeric_step(
           name="Voltage Test",
           value=5.02,
           unit="V",
           comp_op=CompOp.GELE,  # Type-safe enum
           low_limit=4.8,
           high_limit=5.2
           # status NOT needed - automatically Passed since value is in range
       )
       
       # Add another test that will auto-fail
       root.add_numeric_step(
           name="Current Test",
           value=0.350,          # Out of range!
           unit="A",
           comp_op=CompOp.GELE,
           low_limit=0.100,
           high_limit=0.200
           # status automatically Failed since value exceeds high_limit
       )
       
       # Submit to WATS
       response = await api.report.submit_report(report)
       print(f"Report submitted: {response.id}")

Using Service Methods for Report Creation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Report service provides factory methods for creating UUT and UUR reports:

.. code-block:: python

   # Sync API example
   from pywats import pyWATS
   from pywats.shared.enums import CompOp
   
   api = pyWATS(base_url="https://wats.example.com", token="your-token")
   
   # Service factory automatically applies station info if configured
   report = api.report.create_uut_report(
       operator="TestOperator",
       part_number="BOARD-PCB-2000",
       revision="B",
       serial_number="SN-TEST-001",
       operation_type=100,
   )
   
   # Add test steps - status auto-calculated in Active mode
   root = report.get_root_sequence_call()
   root.add_numeric_step(
       name="3.3V Rail",
       value=3.31,
       unit="V",
       comp_op=CompOp.GELE,  # Type-safe enum
       low_limit=3.2,
       high_limit=3.4
   )
   
   # Submit
   response = api.report.submit_report(report)
   print(f"Report ID: {response.id}")

Query Reports
^^^^^^^^^^^^^

Query report headers using OData filters:

.. code-block:: python

   from pywats.domains.report import ReportType, build_serial_filter
   
   # Get recent reports (last 7 days)
   headers = await api.report.get_recent_headers(count=100)
   
   for header in headers:
       print(f"{header.serial_number}: {header.result} ({header.start_utc})")
   
   # Query by serial number
   headers = await api.report.query_headers(
       report_type=ReportType.UUT,
       odata_filter=build_serial_filter("SN-2026-12345")
   )
   
   # Get full report by UUID
   full_report = await api.report.get_report(headers[0].uuid)
   print(f"Steps: {len(full_report.root.steps)}")

Create Repair Report (UUR)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a UUR (Unit Under Repair) report to track repairs:

.. code-block:: python

   from pywats.domains.report import UURReport
   
   # Create UUR from failed UUT report
   uur = api.report.create_uur_report(
       failed_uut_report,
       operator="RepairTech",
       comment="Investigating failure"
   )
   
   # Document the failure
   uur.add_failure_to_main_unit(
       category="Component",
       code="Defect Component",
       comment="Capacitor C12 failed voltage spec",
       component_ref="C12"
   )
   
   # Add repair metadata
   uur.add_misc_info("Action", "Replaced capacitor C12")
   uur.execution_time = 1800.0  # 30 minutes
   
   # Submit repair report
   await api.report.submit_report(uur)

---

Core Concepts
-------------

Report Types
^^^^^^^^^^^^

pyWATS supports two main report types:

.. code-block:: python

   from pywats.domains.report import UUTReport, UURReport, ReportType
   
   # UUT Report - Unit Under Test (test results)
   uut = UUTReport(
       pn="WIDGET-001",
       sn="SN-12345",
       rev="A",
       process_code=100,  # Test operation
       # ... other fields
   )
   
   # UUR Report - Unit Under Repair (repair/rework)
   uur = UURReport(
       pn="WIDGET-001",
       sn="SN-12345",
       rev="A",
       test_operation_code=100,    # Original test
       repair_process_code=500,    # Repair operation
       # ... other fields
   )
   
   # Query by report type
   ReportType.UUT  # "U" - Test reports
   ReportType.UUR  # "R" - Repair reports

Step Type Hierarchy
^^^^^^^^^^^^^^^^^^^

UUT reports contain hierarchical test steps:

.. code-block:: python

   from pywats.domains.report import (
       SequenceCall,      # Container for child steps
       NumericStep,       # Numeric measurement with limits
       PassFailStep,      # Boolean pass/fail test (BooleanStep)
       StringValueStep,   # String comparison test (StringStep)
       MultiNumericStep,  # Multiple numeric measurements
       ActionStep,        # Action or message
       ChartStep,         # Chart/graph data
       GenericStep,       # Generic step type
   )
   from pywats.shared.enums import CompOp
   
   # Sequence calls contain child steps
   root = report.get_root_sequence_call()
   
   # Add a sub-sequence
   power_tests = root.add_sequence_call(
       name="Power Supply Tests",
       file_name="power_tests.py",
       version="1.0.0"
   )
   
   # Add steps to sub-sequence
   power_tests.add_numeric_step(
       name="3.3V Rail",
       value=3.31,
       unit="V",
       comp_op=CompOp.GELE,  # Type-safe enum
       low_limit=3.2,
       high_limit=3.4
   )

Comparison Operators
^^^^^^^^^^^^^^^^^^^^

Numeric and string steps support various comparison operators:

.. code-block:: python

   from pywats.shared.enums import CompOp
   
   # Numeric comparisons
   CompOp.LOG      # Log only, no comparison
   CompOp.EQ       # Equal to
   CompOp.NE       # Not equal
   CompOp.LT       # Less than (high limit only)
   CompOp.LE       # Less than or equal (high limit only)
   CompOp.GT       # Greater than (low limit only)
   CompOp.GE       # Greater than or equal (low limit only)
   CompOp.GELE     # low <= value <= high (most common)
   CompOp.GELT     # low <= value < high
   CompOp.GTLT     # low < value < high
   CompOp.GTLE     # low < value <= high
   
   # String comparisons
   CompOp.CASESENSIT   # Case sensitive match
   CompOp.IGNORECASE   # Case insensitive match
   
   # Example usage
   root.add_numeric_step(
       name="Voltage",
       value=5.0,
       comp_op=CompOp.GELE,  # Type-safe enum
       low_limit=4.5,
       high_limit=5.5
   )

Step Status
^^^^^^^^^^^

Steps and reports have execution status:

.. code-block:: python

   from pywats.domains.report.report_models.common_types import StepStatus, ReportStatus
   
   # Step status (single letter API format)
   StepStatus.Passed      # "P" - Test passed
   StepStatus.Failed      # "F" - Test failed
   StepStatus.Skipped     # "S" - Test skipped
   StepStatus.Done        # "D" - Completed (no pass/fail)
   StepStatus.Error       # "E" - Error occurred
   StepStatus.Terminated  # "T" - Terminated early
   
   # Report status (full word format)
   ReportStatus.Passed
   ReportStatus.Failed
   ReportStatus.Error
   ReportStatus.Terminated
   
   # Flexible status input
   status = StepStatus("Passed")  # Full word
   status = StepStatus("P")       # Single letter
   status = StepStatus("pass")    # Case insensitive
   status = StepStatus("OK")      # Alias

OData Filters
^^^^^^^^^^^^^

Query reports using OData filter syntax:

.. code-block:: python

   from pywats.domains.report import (
       build_serial_filter,
       build_part_number_filter,
       build_date_range_filter,
       combine_filters
   )
   from datetime import datetime, timedelta
   
   # Build individual filters
   serial_filter = build_serial_filter("SN-12345")
   # Result: "serialNumber eq 'SN-12345'"
   
   part_filter = build_part_number_filter("WIDGET-001")
   # Result: "partNumber eq 'WIDGET-001'"
   
   date_filter = build_date_range_filter(
       start_date=datetime.now() - timedelta(days=7),
       end_date=datetime.now()
   )
   # Result: "start ge 2026-01-19T... and start le 2026-01-26T..."
   
   # Combine multiple filters
   combined = combine_filters([serial_filter, part_filter])
   # Result: "serialNumber eq 'SN-12345' and partNumber eq 'WIDGET-001'"
   
   # Use in query
   headers = await api.report.query_uut_headers(
       odata_filter=combined,
       top=100
   )

Query Parameters
^^^^^^^^^^^^^^^^

Build OData query parameters for report queries:

.. code-block:: python

   from pywats.domains.report import (
       build_query_params,
       get_expand_fields,
       is_uut_report_type
   )
   
   # Build query parameters
   params = build_query_params(
       odata_filter="partNumber eq 'WIDGET-001'",
       top=100,
       skip=0,
       orderby="start desc",
       expand=["subUnits", "miscInfo"]
   )
   # Result: {"$filter": "...", "$top": 100, "$orderby": "start desc", "$expand": "subUnits,miscInfo"}
   
   # Get expand fields based on report type
   expand = get_expand_fields(
       is_uut=True,
       include_subunits=True,
       include_misc_info=True
   )
   # Result: ["subUnits", "miscInfo"]
   
   # Check report type
   is_test = is_uut_report_type(ReportType.UUT)  # True
   is_repair = is_uut_report_type(ReportType.UUR)  # False

---

Common Use Cases
----------------

Automated Test Equipment (ATE) Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Integrate test equipment with WATS:

.. code-block:: python

   from pywats import AsyncWATS
   from pywats.domains.report import ImportMode, set_import_mode
   from pywats.shared.enums import CompOp
   from datetime import datetime
   
   async with AsyncWATS(base_url="...", token="...") as api:
       
       async def run_test_and_report(part_number: str, serial_number: str):
           """Run automated test and submit results to WATS."""
           
           # Active mode (default) - status auto-calculated
           set_import_mode(ImportMode.Active)
           
           # Create report using service factory
           report = api.report.create_uut_report(
               operator="ATE-System",
               part_number=part_number,
               serial_number=serial_number,
               revision="A",
               operation_type=100,
           )
           
           root = report.get_root_sequence_call()
           
           # Run power supply tests
           power_seq = root.add_sequence_call(name="Power Tests")
           
           voltage = measure_voltage()  # Your test equipment code
           power_seq.add_numeric_step(
               name="5V Rail",
               value=voltage,
               unit="V",
               comp_op=CompOp.GELE,  # Type-safe enum
               low_limit=4.8,
               high_limit=5.2
               # No status needed - auto-calculated from limits
           )
           
           current = measure_current()
           power_seq.add_numeric_step(
               name="Current",
               value=current,
               unit="A",
               comp_op=CompOp.GELE,
               low_limit=0.1,
               high_limit=0.2
               # Auto-fails if current out of range
           )
           
           # Report result auto-calculated from step failures
           # No need to manually track all_passed or set report.result
           
           # Submit to WATS
           response = await api.report.submit_report(report)
           return response

Repair Workflow
^^^^^^^^^^^^^^^

Track repair activities:

.. code-block:: python

   from pywats.domains.report import ReportType
   from uuid import UUID
   
   async def complete_repair_workflow(serial_number: str):
       """Find failed unit, create repair report, submit."""
       
       # Find failed UUT report
       headers = await api.report.query_headers(
           report_type=ReportType.UUT,
           odata_filter=f"serialNumber eq '{serial_number}' and result eq 'Failed'",
           top=1,
           orderby="start desc"
       )
       
       if not headers:
           print(f"No failed reports found for {serial_number}")
           return
       
       # Get full UUT report
       uut_report = await api.report.get_report(headers[0].uuid)
       
       # Create UUR from failed UUT
       uur = api.report.create_uur_report(
           uut_report,
           operator="RepairTech",
           comment="Standard repair"
       )
       
       # Document failure
       uur.add_failure_to_main_unit(
           category="Component",
           code="Defect Component",
           comment="Replaced failed capacitor",
           component_ref="C12"
       )
       
       # Add repair metadata
       uur.add_misc_info("WorkOrder", "WO-2026-001")
       uur.add_misc_info("RepairType", "Component Replacement")
       uur.execution_time = 1800.0  # 30 minutes
       
       # Submit repair
       response = await api.report.submit_report(uur)
       print(f"Repair submitted: {response}")

Serial Number History
^^^^^^^^^^^^^^^^^^^^^

Track all tests for a serial number:

.. code-block:: python

   from pywats.domains.report import build_serial_filter
   
   async def get_unit_history(serial_number: str):
       """Get complete test and repair history for a unit."""
       
       # Get all UUT reports
       uut_headers = await api.report.query_headers(
           report_type=ReportType.UUT,
           odata_filter=build_serial_filter(serial_number),
           orderby="start asc"
       )
       
       # Get all UUR reports
       uur_headers = await api.report.query_headers(
           report_type=ReportType.UUR,
           odata_filter=build_serial_filter(serial_number),
           orderby="start asc"
       )
       
       print(f"History for {serial_number}:")
       print(f"  UUT Reports: {len(uut_headers)}")
       for h in uut_headers:
           print(f"    {h.start_utc}: {h.result} - Process {h.process_code}")
       
       print(f"  UUR Reports: {len(uur_headers)}")
       for h in uur_headers:
           print(f"    {h.start_utc}: Repair - Process {h.process_code}")

Batch Data Import
^^^^^^^^^^^^^^^^^

Import historical test data:

.. code-block:: python

   from pywats.domains.report import ImportMode
   import csv
   
   async def import_historical_data(csv_file: str):
       """Import test data from CSV file."""
       
       with open(csv_file, 'r') as f:
           reader = csv.DictReader(f)
           
           for row in reader:
               report = UUTReport(
                   pn=row['PartNumber'],
                   sn=row['SerialNumber'],
                   rev=row['Revision'],
                   process_code=int(row['ProcessCode']),
                   station_name=row['Station'],
                   location=row['Location'],
                   purpose="Production",
                   result=row['Result'],
                   start=datetime.fromisoformat(row['TestDate'])
               )
               
               # Use Import mode to preserve exact status
               # (no auto-calculation or failure propagation)
               report.import_mode = ImportMode.Import
               
               root = report.get_root_sequence_call()
               
               # Add test data from CSV
               root.add_numeric_step(
                   name=row['TestName'],
                   value=float(row['Value']),
                   unit=row['Unit'],
                   status=row['Status']  # Preserved as-is in Import mode
               )
               
               await api.report.submit_report(report)
               print(f"Imported: {row['SerialNumber']}")

Failed Unit Analysis
^^^^^^^^^^^^^^^^^^^^

Analyze failure patterns:

.. code-block:: python

   from pywats.domains.report import build_date_range_filter, combine_filters
   from datetime import datetime, timedelta
   from collections import Counter
   
   async def analyze_failures(part_number: str, days: int = 30):
       """Analyze failure patterns for a product."""
       
       # Build filter for failed reports
       date_filter = build_date_range_filter(
           start_date=datetime.now() - timedelta(days=days),
           end_date=datetime.now()
       )
       part_filter = f"partNumber eq '{part_number}'"
       result_filter = "result eq 'Failed'"
       
       odata_filter = combine_filters([date_filter, part_filter, result_filter])
       
       # Get failed reports
       headers = await api.report.query_headers(
           report_type=ReportType.UUT,
           odata_filter=odata_filter,
           expand=["miscInfo"]
       )
       
       print(f"Failed units for {part_number} (last {days} days): {len(headers)}")
       
       # Analyze failure steps
       failure_steps = Counter()
       
       for header in headers:
           if header.caused_uut_failure:
               failure_steps[header.caused_uut_failure] += 1
       
       print("\nTop failure steps:")
       for step, count in failure_steps.most_common(10):
           print(f"  {step}: {count}")

---

Advanced Features
-----------------

Report Attachments
^^^^^^^^^^^^^^^^^^

Attach files, images, and binary data to reports:

.. code-block:: python

   from pywats.domains.report import Attachment
   
   # Create report
   report = UUTReport(pn="WIDGET-001", sn="SN-001", rev="A", ...)
   
   # Attach binary data (in-memory)
   test_log = b"Test log data..."
   report.attach_bytes(
       name="TestLog.txt",
       content=test_log,
       content_type="text/plain"
   )
   
   # Attach image (base64 encoded in memory)
   with open("board_photo.jpg", "rb") as f:
       image_data = f.read()
   report.attach_bytes(
       name="BoardPhoto",
       content=image_data,
       content_type="image/jpeg"
   )
   
   # For file operations, use pywats_client.io.AttachmentIO
   # from pywats_client.io import AttachmentIO
   # info = AttachmentIO.read_file("test_data.bin")
   # report.attach_bytes(name="TestData", content=info.content, content_type=info.mime_type)
   
   await api.report.submit_report(report)

Sub-Units and Assemblies
^^^^^^^^^^^^^^^^^^^^^^^^^

Track sub-assemblies and daughter boards:

.. code-block:: python

   from pywats.domains.report import SubUnit
   
   # Create main unit report
   report = UUTReport(pn="MAIN-BOARD", sn="MB-001", rev="A", ...)
   
   # Add sub-unit (daughter board)
   sub1 = report.add_sub_unit(
       pn="DAUGHTER-BOARD-A",
       sn="DB-A-123",
       rev="1",
       part_type="DaughterBoard"
   )
   
   # Add another sub-unit (module)
   sub2 = report.add_sub_unit(
       pn="POWER-MODULE",
       sn="PM-456",
       rev="2",
       part_type="Module"
   )
   
   await api.report.submit_report(report)
   
   # Query reports by sub-unit
   from pywats.domains.report import build_subunit_part_filter
   
   headers = await api.report.query_headers(
       report_type=ReportType.UUT,
       odata_filter=build_subunit_part_filter("DAUGHTER-BOARD-A")
   )

Charts and Waveforms
^^^^^^^^^^^^^^^^^^^^

Add chart data for waveforms and multi-point measurements:

.. code-block:: python

   from pywats.domains.report import Chart, ChartSeries, ChartType
   
   report = api.report.create_uut_report(
       operator="TestOp",
       part_number="WIDGET-001",
       serial_number="SN-001",
       revision="A",
       operation_type=100
   )
   root = report.get_root_sequence_call()
   
   # Add chart step (status can be omitted for non-measurement steps)
   chart = root.add_chart_step(name="Frequency Response")
   
   # Create chart with series data
   chart.chart = Chart(
       chart_type=ChartType.Line,
       x_label="Frequency (Hz)",
       y_label="Amplitude (dB)",
       series=[
           ChartSeries(
               name="Channel 1",
               x_values=[100, 1000, 10000, 20000],
               y_values=[-0.5, 0.0, -0.3, -1.2]
           )
       ]
   )
   
   await api.report.submit_report(report)

Misc Info (Custom Metadata)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Add custom key-value metadata to reports:

.. code-block:: python

   from pywats.domains.report import MiscInfo
   
   report = UUTReport(pn="WIDGET-001", sn="SN-001", rev="A", ...)
   
   # Add misc info
   report.add_misc_info("Operator", "John Smith")
   report.add_misc_info("WorkOrder", "WO-2026-Q1-001")
   report.add_misc_info("Batch", "BATCH-001")
   report.add_misc_info("Temperature", "25°C")
   report.add_misc_info("Humidity", "45%")
   
   await api.report.submit_report(report)
   
   # Query by misc info
   headers = await api.report.query_headers(
       report_type=ReportType.UUT,
       odata_filter="miscInfo/any(m: m/description eq 'WorkOrder' and m/value eq 'WO-2026-Q1-001')"
   )

Import Mode vs Active Mode
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Control automatic status calculation:

.. code-block:: python

   from pywats.domains.report import ImportMode
   from pywats.shared.enums import CompOp
   
   # Active Mode (default) - automatic behaviors:
   # - Auto-calculate status from comp/limits
   # - Propagate failures up hierarchy
   # - Default status is Passed if not set
   report_active = UUTReport(pn="WIDGET-001", sn="SN-001", rev="A", ...)
   report_active.import_mode = ImportMode.Active  # Default
   
   root = report_active.get_root_sequence_call()
   root.add_numeric_step(
       name="Voltage",
       value=5.0,
       comp_op=CompOp.GELE,  # Type-safe enum
       low_limit=4.5,
       high_limit=5.5
       # Status auto-calculated: Passed (value within limits)
   )
   
   # Import Mode - passive, preserve exact data:
   # - No auto-calculation
   # - No failure propagation
   # - Store data exactly as provided
   report_import = UUTReport(pn="WIDGET-001", sn="SN-002", rev="A", ...)
   report_import.import_mode = ImportMode.Import
   
   root = report_import.get_root_sequence_call()
   root.add_numeric_step(
       name="Voltage",
       value=5.0,
       status=StepStatus.Failed  # Explicit status required
       # Status preserved as Failed even though value is valid
   )

Pagination and Large Queries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Handle large result sets efficiently:

.. code-block:: python

   from pywats.domains.report import build_query_params
   
   async def get_all_reports(part_number: str):
       """Get all reports using pagination."""
       
       page_size = 100
       skip = 0
       all_headers = []
       
       while True:
           # Build query with pagination
           params = build_query_params(
               odata_filter=f"partNumber eq '{part_number}'",
               top=page_size,
               skip=skip,
               orderby="start desc"
           )
           
           headers = await api.report.query_uut_headers(**params)
           
           if not headers:
               break
           
           all_headers.extend(headers)
           skip += page_size
           
           print(f"Fetched {len(all_headers)} reports...")
           
           if len(headers) < page_size:
               break  # Last page
       
       return all_headers

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.report.async_service.AsyncReportService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. autoclass:: pywats.domains.report.async_repository.AsyncReportRepository
   :members:
   :undoc-members:
   :show-inheritance:

---

Models Documentation
--------------------

Query Models
^^^^^^^^^^^^

.. autoclass:: pywats.domains.report.models.WATSFilter
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.models.ReportHeader
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.models.AttachmentMetadata
   :members:
   :undoc-members:
   :show-inheritance:

Report Models
^^^^^^^^^^^^^

.. autoclass:: pywats.domains.report.report_models.UUTReport
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.UURReport
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.Report
   :members:
   :undoc-members:
   :show-inheritance:

Step Models
^^^^^^^^^^^

.. autoclass:: pywats.domains.report.report_models.Step
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.SequenceCall
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.NumericStep
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.PassFailStep
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.StringValueStep
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.MultiNumericStep
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.ChartStep
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.GenericStep
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.ActionStep
   :members:
   :undoc-members:
   :show-inheritance:

Supporting Models
^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.report.report_models.MiscInfo
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.SubUnit
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.Attachment
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.Chart
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.Asset
   :members:
   :undoc-members:
   :show-inheritance:

Enums
-----

.. autoclass:: pywats.domains.report.enums.ReportType
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.enums.DateGrouping
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.enums.ImportMode
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.common_types.StepStatus
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.report.report_models.common_types.ReportStatus
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.shared.enums.CompOp
   :members:
   :undoc-members:
   :show-inheritance:

Filter Builders
---------------

.. automodule:: pywats.domains.report.filter_builders
   :members:
   :undoc-members:
   :show-inheritance:

Query Helpers
-------------

.. automodule:: pywats.domains.report.query_helpers
   :members:
   :undoc-members:
   :show-inheritance:

Factory Tools
-------------

.. autofunction:: pywats.tools.test_uut.create_test_uut_report

---

Best Practices
--------------

1. **Use Factory Methods for Report Creation**
   Always use ``create_uut_report()`` or ``create_uur_report()`` from the service to ensure proper initialization with station info and required fields.

2. **Set Process Codes Correctly**
   UUT reports use ``process_code`` (test operation), while UUR reports use both ``test_operation_code`` (original test) and ``repair_process_code`` (repair operation).

3. **Use Type-Safe Enums**
   Use ``StepStatus``, ``ReportStatus``, ``CompOp``, and ``ReportType`` enums instead of strings for better IDE support and compile-time validation.

4. **Leverage Import Mode for Historical Data**
   When importing historical test data, use ``ImportMode.Import`` to preserve exact status values and prevent auto-calculation.

5. **Build OData Filters with Helper Functions**
   Use ``build_serial_filter()``, ``build_part_number_filter()``, and ``combine_filters()`` instead of manually constructing OData filter strings.

6. **Handle Large Queries with Pagination**
   For queries returning many results, use ``top`` and ``skip`` parameters to paginate results and avoid memory issues.

7. **Document Repairs Thoroughly**
   When creating UUR reports, always include failure category/code and detailed comments. Use misc info for additional repair metadata.

8. **Validate Comparison Operators**
   Ensure numeric steps use appropriate ``comp_op`` for the test type (GELE for ranges, GE/LE for single limits, LOG for logging only).

9. **Use Sequence Calls for Organization**
   Group related test steps into sequence calls for better report organization and readability.

10. **Attach Supporting Documentation**
    Add photos, logs, and waveform data as attachments to provide complete test documentation and aid in failure analysis.

---

Related Documentation
---------------------

- :doc:`../usage/report-domain` - Detailed usage guide with more examples
- :doc:`../domains/analytics` - Analytics domain (uses report data)
- :doc:`../domains/process` - Process configuration
- :doc:`../getting-started` - Installation and setup

---

Domain Health
-------------

**Score:** 53/60 (A-) - Very Good, production-ready

See :doc:`../../domain_health/report` for detailed domain health assessment.

**Strengths:**
- Excellent Service→Repository→HttpClient architecture
- Clean separation with filter_builders and query_helpers modules
- 100% ErrorHandler coverage
- Comprehensive UUT/UUR report model support
- Type-safe enums for better developer experience
- Shared Attachment class between UUT/UUR
- 134 passing tests with good coverage

**Recent Improvements (Jan 2026):**
- Added ``Raises:`` sections to all service methods
- Extracted filter building logic to ``filter_builders.py``
- Extracted query parameter logic to ``query_helpers.py``
- Refactored UURReport from 644 to 426 lines (34% reduction)
- Unified Attachment class for UUT/UUR reports
- Enhanced documentation with practical examples

**Complexity Note:**
The Report domain is intentionally complex due to:
- Dual report types (UUT test reports and UUR repair reports)
- Extensive step type hierarchy (SequenceCall, NumericStep, PassFailStep, etc.)
- Dual process code systems (test_operation vs repair_operation)
- Multiple serialization formats (WSJF JSON, WSXF XML)
- Attachment and certificate handling
- Sub-unit tracking and failure documentation

This complexity is inherent to the domain and well-managed through clear abstractions.

---

**Next Review Due:** 2026-04-26 or before major refactoring
