"""Query service - business logic layer.

High-level operations for report queries and statistics.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime

from .models import WATSFilter, ReportHeader, YieldData
from .enums import DateGrouping
from .repository import QueryRepository


class QueryService:
    """
    Query business logic.

    Provides high-level operations for querying reports and
    calculating statistics.
    """

    def __init__(self, repository: QueryRepository):
        """
        Initialize with repository.

        Args:
            repository: QueryRepository for data access
        """
        self._repo = repository

    # =========================================================================
    # Report Header Queries
    # =========================================================================

    def find_reports(
        self,
        report_type: str = "uut",
        serial_number: Optional[str] = None,
        part_number: Optional[str] = None,
        revision: Optional[str] = None,
        station_name: Optional[str] = None,
        status: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        top_count: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Find reports matching criteria.

        Args:
            report_type: Report type ("uut" or "uur")
            serial_number: Filter by serial number
            part_number: Filter by part number
            revision: Filter by revision
            station_name: Filter by station name
            status: Filter by status
            date_from: Filter by start date
            date_to: Filter by end date
            top_count: Max number of results

        Returns:
            List of ReportHeader objects
        """
        filter_data = WATSFilter(
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            station_name=station_name,
            status=status,
            date_from=date_from,
            date_to=date_to,
            top_count=top_count
        )
        return self._repo.query_headers(report_type, filter_data)

    def find_reports_by_filter(
        self,
        filter_data: WATSFilter,
        report_type: str = "uut"
    ) -> List[ReportHeader]:
        """
        Find reports using a filter object.

        Args:
            filter_data: WATSFilter object
            report_type: Report type ("uut" or "uur")

        Returns:
            List of ReportHeader objects
        """
        return self._repo.query_headers(report_type, filter_data)

    def find_reports_by_misc_info(
        self,
        description: str,
        value: str,
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Find reports by misc info values.

        Args:
            description: Misc info description
            value: Misc info value
            top: Max number of results

        Returns:
            List of ReportHeader objects
        """
        return self._repo.query_headers_by_misc_info(description, value, top)

    def find_recent_reports(
        self,
        report_type: str = "uut",
        count: int = 100
    ) -> List[ReportHeader]:
        """
        Get most recent reports.

        Args:
            report_type: Report type ("uut" or "uur")
            count: Number of recent reports

        Returns:
            List of ReportHeader objects
        """
        filter_data = WATSFilter(top_count=count)
        return self._repo.query_headers(report_type, filter_data)

    def find_failing_reports(
        self,
        part_number: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        top_count: Optional[int] = 100
    ) -> List[ReportHeader]:
        """
        Find reports with failed status.

        Args:
            part_number: Filter by part number
            date_from: Filter by start date
            date_to: Filter by end date
            top_count: Max number of results

        Returns:
            List of failing ReportHeader objects
        """
        filter_data = WATSFilter(
            part_number=part_number,
            status="Failed",
            date_from=date_from,
            date_to=date_to,
            top_count=top_count
        )
        return self._repo.query_headers("uut", filter_data)

    # =========================================================================
    # Yield Statistics
    # =========================================================================

    def get_yield(
        self,
        part_number: Optional[str] = None,
        station_name: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        date_grouping: DateGrouping = DateGrouping.DAY
    ) -> List[YieldData]:
        """
        Get yield statistics.

        Args:
            part_number: Filter by part number
            station_name: Filter by station name
            date_from: Filter by start date
            date_to: Filter by end date
            date_grouping: How to group dates

        Returns:
            List of YieldData objects
        """
        filter_data = WATSFilter(
            part_number=part_number,
            station_name=station_name,
            date_from=date_from,
            date_to=date_to,
            date_grouping=date_grouping
        )
        return self._repo.get_yield(filter_data)

    def get_first_pass_yield(
        self,
        part_number: str,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> Optional[float]:
        """
        Get first pass yield for a product.

        Args:
            part_number: Product part number
            date_from: Filter by start date
            date_to: Filter by end date

        Returns:
            First pass yield as percentage, or None
        """
        yield_data = self.get_yield(
            part_number=part_number,
            date_from=date_from,
            date_to=date_to,
            date_grouping=DateGrouping.NONE
        )
        if yield_data:
            return yield_data[0].fpy
        return None

    # =========================================================================
    # Attachments
    # =========================================================================

    def get_attachment(
        self,
        attachment_id: Optional[int] = None,
        step_id: Optional[int] = None
    ) -> Optional[bytes]:
        """
        Get attachment content.

        Args:
            attachment_id: Attachment ID
            step_id: Step ID

        Returns:
            Attachment content as bytes
        """
        return self._repo.get_attachment(attachment_id, step_id)

    def download_all_attachments(self, report_id: str) -> Optional[bytes]:
        """
        Download all attachments for a report as zip.

        Args:
            report_id: Report ID

        Returns:
            Zip file content as bytes
        """
        return self._repo.get_attachments_zip(report_id)

    # =========================================================================
    # Certificate
    # =========================================================================

    def get_certificate(self, report_id: str) -> Optional[bytes]:
        """
        Get certificate for a report.

        Args:
            report_id: Report ID

        Returns:
            Certificate content as bytes
        """
        return self._repo.get_certificate(report_id)

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def create_filter(
        self,
        **kwargs
    ) -> WATSFilter:
        """
        Create a filter object with provided parameters.

        Args:
            **kwargs: Filter parameters

        Returns:
            WATSFilter object
        """
        return WATSFilter(**kwargs)
