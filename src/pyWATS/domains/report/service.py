"""Report service - business logic layer.

All business operations for test reports (UUT/UUR).
"""
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, timedelta

from .repository import ReportRepository
from .models import WATSFilter, ReportHeader
from .enums import DateGrouping
from ...core import HttpClient
from ...models.report import UUTReport, UURReport


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
        filter_data = WATSFilter(serial_number=serial_number, top=top)
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
        filter_data = WATSFilter(part_number=part_number, top=top)
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
        filter_data = WATSFilter(start=start_date, end=end_date)
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
        filter_data = WATSFilter(start=start_date, end=end_date, top=top)
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
        filter_data = WATSFilter(start=today, end=tomorrow, top=top)
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
