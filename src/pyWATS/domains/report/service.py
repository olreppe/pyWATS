"""Report service - business logic layer.

All business operations for test reports (UUT/UUR).
"""
from typing import Optional, List, Dict, Any, Union, overload
from datetime import datetime, timedelta
from uuid import uuid4, UUID

from .repository import ReportRepository
from .models import WATSFilter, ReportHeader
from .enums import DateGrouping
from ...core import HttpClient
from .report_models import UUTReport, UURReport
from .report_models.uut.uut_info import UUTInfo
from .report_models.uur.uur_info import UURInfo


class ReportService:
    """
    Report business logic layer.

    Provides high-level operations for working with WATS test reports.
    """

    def __init__(self, client: HttpClient):
        """
        Initialize with HttpClient.

        Args:
            client: HttpClient instance
        """
        self._repository = ReportRepository(client)

    # =========================================================================
    # Report Factory Methods
    # =========================================================================

    def create_uut_report(
        self,
        operator: str,
        part_number: str,
        revision: str,
        serial_number: str,
        operation_type: int,
        station_name: Optional[str] = None,
        location: Optional[str] = None,
        purpose: Optional[str] = None
    ) -> UUTReport:
        """
        Create a new UUT (Unit Under Test) report.

        Args:
            operator: Name of the test operator
            part_number: Part number of the unit being tested
            revision: Revision of the unit
            serial_number: Serial number of the unit
            operation_type: Process code/operation type
            station_name: Optional station name
            location: Optional location
            purpose: Optional purpose

        Returns:
            A new UUTReport object ready for adding steps and submission
        """
        uut_info = UUTInfo(
            operator=operator
        )

        report = UUTReport(
            id=uuid4(),
            type="T",
            pn=part_number,
            sn=serial_number,
            rev=revision,
            process_code=operation_type,
            station_name=station_name or "Unknown",
            location=location or "Unknown",
            purpose=purpose or "Development",
            start=datetime.now().astimezone(),
            info=uut_info
        )

        return report

    # =========================================================================
    # UUR Factory Methods - Multiple creation patterns
    # =========================================================================

    @overload
    def create_uur_report(
        self,
        uut_or_guid_or_pn: UUTReport,
        test_operation_code_pos: None = None,
        *,
        repair_process_code: int = 500,
        operator: Optional[str] = None,
        station_name: Optional[str] = None,
        location: Optional[str] = None,
        comment: Optional[str] = None
    ) -> UURReport: ...

    @overload
    def create_uur_report(
        self,
        uut_or_guid_or_pn: UUID,
        test_operation_code_pos: None = None,
        *,
        part_number: str,
        serial_number: str,
        test_operation_code: int,
        repair_process_code: int = 500,
        revision: str = "A",
        operator: Optional[str] = None,
        station_name: Optional[str] = None,
        location: Optional[str] = None,
        comment: Optional[str] = None
    ) -> UURReport: ...

    @overload
    def create_uur_report(
        self,
        uut_or_guid_or_pn: str,
        test_operation_code_pos: int,
        *,
        serial_number: str,
        repair_process_code: int = 500,
        revision: str = "A",
        operator: Optional[str] = None,
        station_name: Optional[str] = None,
        location: Optional[str] = None,
        comment: Optional[str] = None
    ) -> UURReport: ...

    def create_uur_report(
        self,
        uut_or_guid_or_pn: Union[UUTReport, UUID, str, None] = None,
        test_operation_code_pos: Optional[int] = None,
        *,
        # Common optional parameters
        operator: Optional[str] = None,
        part_number: Optional[str] = None,
        serial_number: Optional[str] = None,
        revision: str = "A",
        # Dual process codes (key UUR architectural feature)
        repair_process_code: int = 500,
        test_operation_code: Optional[int] = None,
        station_name: Optional[str] = None,
        location: Optional[str] = None,
        purpose: Optional[str] = None,
        comment: Optional[str] = None,
        # Legacy parameters (for backward compatibility)
        process_code: Optional[int] = None,
        operation_type: Optional[int] = None,
    ) -> UURReport:
        """
        Create a new UUR (Unit Under Repair) report.

        UUR reports require TWO process codes:
        
        1. **repair_process_code**: The type of repair operation (default: 500)
           - Must be a valid repair operation (isRepairOperation=true)
           - Common values: 500 (Repair), 510 (RMA Repair)
           - This becomes the top-level report process_code
        
        2. **test_operation_code**: The original test operation that failed
           - Must be a valid test operation (isTestOperation=true)  
           - Common values: 100 (End of line test), 50 (PCBA test), etc.
           - Automatically extracted from UUTReport if provided
           - Stored in uur_info.test_operation_code

        Supports multiple calling patterns:

        1. From UUTReport object (recommended):
           ```python
           uur = api.report.create_uur_report(
               failed_uut,
               repair_process_code=500,
               operator="RepairTech"
           )
           ```

        2. From UUT GUID (when you have the ID but not the full report):
           ```python
           uur = api.report.create_uur_report(
               uut_guid,
               part_number="PN-123",
               serial_number="SN-001",
               test_operation_code=100,
               repair_process_code=500
           )
           ```

        3. From part number and test operation code:
           ```python
           uur = api.report.create_uur_report(
               "PN-123", 100,  # part_number, test_operation_code
               serial_number="SN-001",
               repair_process_code=500
           )
           ```

        Args:
            uut_or_guid_or_pn: UUTReport object, UUID of referenced UUT, or part number
            test_operation_code_pos: Test operation code (positional, for pattern 3)
            operator: Name of the repair operator
            part_number: Part number (when not using UUTReport)
            serial_number: Serial number (when not using UUTReport)
            revision: Revision of the unit (default "A")
            repair_process_code: Repair operation type (default 500=Repair)
            test_operation_code: Original test operation that failed
            station_name: Optional station name
            location: Optional location  
            purpose: Optional purpose (default "Repair")
            comment: Optional comment for the repair
            process_code: Legacy - use test_operation_code instead
            operation_type: Legacy - use test_operation_code instead

        Returns:
            A new UURReport object ready for adding repair info and submission
        """
        # Resolve parameters based on calling pattern
        ref_uut_guid: Optional[UUID] = None
        pn: str = ""
        sn: str = ""
        rev: str = revision
        test_op_code: Optional[int] = None

        # Pattern 1: UUTReport object
        if isinstance(uut_or_guid_or_pn, UUTReport):
            uut = uut_or_guid_or_pn
            ref_uut_guid = uut.id
            pn = uut.pn
            sn = uut.sn
            rev = uut.rev or revision
            # Extract test operation code from the UUT
            test_op_code = test_operation_code or uut.process_code
            # Use UUT's station/location as defaults if not specified
            station_name = station_name or uut.station_name
            location = location or uut.location

        # Pattern 2: UUID
        elif isinstance(uut_or_guid_or_pn, UUID):
            ref_uut_guid = uut_or_guid_or_pn
            if not part_number:
                raise ValueError("part_number is required when creating UUR from UUID")
            if not serial_number:
                raise ValueError("serial_number is required when creating UUR from UUID")
            pn = part_number
            sn = serial_number
            rev = revision
            # Resolve test operation code from various sources
            test_op_code = (
                test_operation_code or 
                test_operation_code_pos or 
                process_code or 
                operation_type
            )
            if not test_op_code:
                raise ValueError("test_operation_code is required when creating UUR from UUID")

        # Pattern 3: part_number string with test_operation_code
        elif isinstance(uut_or_guid_or_pn, str):
            pn = uut_or_guid_or_pn
            # Resolve test operation code
            test_op_code = (
                test_operation_code_pos or
                test_operation_code or 
                process_code or 
                operation_type
            )
            if not test_op_code:
                raise ValueError("test_operation_code is required when creating UUR from part_number")
            if not serial_number:
                raise ValueError("serial_number is required when creating UUR from part_number")
            sn = serial_number
            rev = revision

        # Legacy fallback: use keyword arguments
        else:
            if part_number:
                pn = part_number
            if serial_number:
                sn = serial_number
            test_op_code = test_operation_code or process_code or operation_type

        if not pn:
            raise ValueError("part_number is required")
        if not sn:
            raise ValueError("serial_number is required")

        # Get current timestamp for timing fields
        now = datetime.now().astimezone()

        # Create UURInfo with dual process code architecture
        # Note: API requires processCode, confirmDate, finalizeDate, execTime in uur object
        uur_info = UURInfo(
            operator=operator or "Unknown",  # Required field from ReportInfo
            ref_uut=ref_uut_guid,
            comment=comment,
            # Set the test operation code (what failed)
            test_operation_code=test_op_code,
            process_code=test_op_code,  # API requires this in uur object
            # Required timing fields
            confirm_date=now,
            finalize_date=now,
            exec_time=0.0,  # Time spent on repair (seconds)
        )

        # Create report with repair process code at top level
        report = UURReport(
            id=uuid4(),
            type="R",
            pn=pn,
            sn=sn,
            rev=rev,
            process_code=repair_process_code,  # Repair operation (500, 510, etc.)
            station_name=station_name or "Unknown",
            location=location or "Unknown",
            purpose=purpose or "Repair",
            start=datetime.now().astimezone(),
            uur_info=uur_info
        )
        
        # Copy sub_units from UUT if creating from UUTReport
        if isinstance(uut_or_guid_or_pn, UUTReport):
            uut = uut_or_guid_or_pn
            self._copy_sub_units_to_uur(uut, report)

        return report
    
    def _copy_sub_units_to_uur(self, uut: UUTReport, uur: UURReport) -> None:
        """
        Copy sub_units from UUT to UUR report.
        
        UUR uses extended SubUnits with idx, parentIdx, and failures fields.
        The main unit (idx=0) is already created by UURReport.
        
        Args:
            uut: Source UUT report
            uur: Target UUR report
        """
        from .report_models.uur.uur_sub_unit import UURSubUnit
        
        if not uut.sub_units:
            return
            
        # Copy each sub_unit from UUT, starting from idx=1 (main is idx=0)
        for i, sub_unit in enumerate(uut.sub_units):
            uur_sub = UURSubUnit.from_sub_unit(
                sub_unit,
                idx=i + 1,  # Start from 1 since 0 is main unit
                parent_idx=0  # Default parent is main unit
            )
            if uur.sub_units is None:
                uur.sub_units = []
            uur.sub_units.append(uur_sub)

    def create_uur_from_uut(
        self,
        uut_report: UUTReport,
        operator: Optional[str] = None,
        comment: Optional[str] = None
    ) -> UURReport:
        """
        Create a UUR report linked to a UUT report.

        This is a convenience method that creates a repair report referencing
        the given UUT report, copying relevant metadata.

        Args:
            uut_report: The UUT report to create repair for
            operator: Operator performing the repair
            comment: Initial comment for the repair

        Returns:
            UURReport linked to the UUT
        """
        return self.create_uur_report(
            uut_report,
            operator=operator,
            comment=comment
        )

    # =========================================================================
    # Query Methods
    # =========================================================================

    def query_uut_headers(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None
    ) -> List[ReportHeader]:
        """
        Query UUT report headers.

        Args:
            filter_data: WATSFilter or filter dict

        Returns:
            List of ReportHeader objects
        """
        return self._repository.query_headers("uut", filter_data)

    def query_uur_headers(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None
    ) -> List[ReportHeader]:
        """
        Query UUR report headers.

        Args:
            filter_data: WATSFilter or filter dict

        Returns:
            List of ReportHeader objects
        """
        return self._repository.query_headers("uur", filter_data)

    def query_headers_by_misc_info(
        self,
        description: str,
        string_value: str,
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Query report headers by misc info.

        Args:
            description: Misc info description
            string_value: Misc info string value
            top: Number of records to return

        Returns:
            List of ReportHeader objects
        """
        return self._repository.query_headers_by_misc_info(
            description, string_value, top
        )

    # =========================================================================
    # Query Helpers
    # =========================================================================

    def get_headers_by_serial(
        self,
        serial_number: str,
        report_type: str = "uut",
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Get report headers by serial number.

        Args:
            serial_number: Serial number to search
            report_type: "uut" or "uur"
            top: Number of records to return

        Returns:
            List of ReportHeader
        """
        filter_data = WATSFilter(serial_number=serial_number, top_count=top)
        return self._repository.query_headers(report_type, filter_data)

    def get_headers_by_part_number(
        self,
        part_number: str,
        report_type: str = "uut",
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Get report headers by part number.

        Args:
            part_number: Part number to search
            report_type: "uut" or "uur"
            top: Number of records to return

        Returns:
            List of ReportHeader
        """
        filter_data = WATSFilter(part_number=part_number, top_count=top)
        return self._repository.query_headers(report_type, filter_data)

    def get_headers_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
        report_type: str = "uut"
    ) -> List[ReportHeader]:
        """
        Get report headers by date range.

        Args:
            start_date: Start date
            end_date: End date
            report_type: "uut" or "uur"

        Returns:
            List of ReportHeader
        """
        filter_data = WATSFilter(date_from=start_date, date_to=end_date)
        return self._repository.query_headers(report_type, filter_data)

    def get_recent_headers(
        self,
        days: int = 7,
        report_type: str = "uut",
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Get headers from the last N days.

        Args:
            days: Number of days back
            report_type: "uut" or "uur"
            top: Number of records to return

        Returns:
            List of ReportHeader
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        filter_data = WATSFilter(date_from=start_date, date_to=end_date, top_count=top)
        return self._repository.query_headers(report_type, filter_data)

    def get_todays_headers(
        self,
        report_type: str = "uut",
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Get today's report headers.

        Args:
            report_type: "uut" or "uur"
            top: Number of records to return

        Returns:
            List of ReportHeader
        """
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        filter_data = WATSFilter(date_from=today, date_to=tomorrow, top_count=top)
        return self._repository.query_headers(report_type, filter_data)

    # =========================================================================
    # WSJF (JSON Format) Operations
    # =========================================================================

    def get_report(
        self, report_id: str
    ) -> Optional[Union[UUTReport, UURReport]]:
        """
        Get a report in WSJF format.

        Args:
            report_id: Report ID (GUID)

        Returns:
            UUTReport or UURReport, or None
        """
        return self._repository.get_wsjf(report_id)

    def submit_report(
        self, report: Union[UUTReport, UURReport, Dict[str, Any]]
    ) -> Optional[str]:
        """
        Submit a new report.

        Args:
            report: Report to submit (UUTReport, UURReport or dict)

        Returns:
            Report ID if successful, None otherwise
        """
        return self._repository.post_wsjf(report)

    def submit(
        self, report: Union[UUTReport, UURReport, Dict[str, Any]]
    ) -> Optional[str]:
        """
        Submit a new report (alias for submit_report).

        Args:
            report: Report to submit (UUTReport, UURReport or dict)

        Returns:
            Report ID if successful, None otherwise
        """
        return self.submit_report(report)

    # =========================================================================
    # WSXF (XML Format) Operations
    # =========================================================================

    def get_report_xml(self, report_id: str) -> Optional[bytes]:
        """
        Get a report as XML (WSXF format).

        Args:
            report_id: Report ID (GUID)

        Returns:
            XML content as bytes or None
        """
        return self._repository.get_wsxf(report_id)

    def submit_report_xml(self, xml_content: str) -> Optional[str]:
        """
        Submit a report in XML format.

        Args:
            xml_content: Report as XML string

        Returns:
            Report ID if successful, None otherwise
        """
        return self._repository.post_wsxf(xml_content)

    # =========================================================================
    # Attachments
    # =========================================================================

    def get_attachment(
        self,
        attachment_id: Optional[str] = None,
        step_id: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Get attachment content.

        Args:
            attachment_id: Attachment ID
            step_id: Step ID

        Returns:
            Attachment content as bytes or None
        """
        return self._repository.get_attachment(attachment_id, step_id)

    def get_all_attachments(self, report_id: str) -> Optional[bytes]:
        """
        Get all attachments for a report as zip file.

        Args:
            report_id: Report ID

        Returns:
            Zip file content as bytes or None
        """
        return self._repository.get_attachments_as_zip(report_id)

    # =========================================================================
    # Certificate
    # =========================================================================

    def get_certificate(self, report_id: str) -> Optional[bytes]:
        """
        Get certificate for a report.

        Args:
            report_id: Report ID

        Returns:
            Certificate content as bytes or None
        """
        return self._repository.get_certificate(report_id)
