"""Report service - business logic layer.

High-level operations for test report management.
"""
from typing import Optional, Union, List
from datetime import datetime

from ...models.report import UUTReport, UURReport, SequenceCall, StepList
from ...models.report.common_types import ResultStatus
from .repository import ReportRepository


class ReportService:
    """
    Report business logic.

    Provides high-level operations for creating, submitting,
    and analyzing test reports.
    """

    def __init__(self, repository: ReportRepository):
        """
        Initialize with repository.

        Args:
            repository: ReportRepository for data access
        """
        self._repo = repository

    # =========================================================================
    # Report Submission
    # =========================================================================

    def submit_uut_report(self, report: UUTReport) -> Optional[str]:
        """
        Submit a UUT test report.

        Args:
            report: UUTReport object

        Returns:
            Report ID if successful
        """
        return self._repo.post_wsjf(report)

    def submit_uur_report(self, report: UURReport) -> Optional[str]:
        """
        Submit a UUR repair report.

        Args:
            report: UURReport object

        Returns:
            Report ID if successful
        """
        return self._repo.post_wsjf(report)

    def submit_xml_report(self, xml_content: str) -> Optional[str]:
        """
        Submit an XML (WSXF) format report.

        Args:
            xml_content: Report as XML string

        Returns:
            Report ID if successful
        """
        return self._repo.post_wsxf(xml_content)

    # =========================================================================
    # Report Retrieval
    # =========================================================================

    def get_report(
        self, report_id: str
    ) -> Optional[Union[UUTReport, UURReport]]:
        """
        Get a report by ID.

        Args:
            report_id: Report ID (GUID)

        Returns:
            UUTReport or UURReport
        """
        return self._repo.get_wsjf(report_id)

    def get_uut_report(self, report_id: str) -> Optional[UUTReport]:
        """
        Get a UUT report by ID.

        Args:
            report_id: Report ID (GUID)

        Returns:
            UUTReport or None
        """
        return self._repo.get_uut_report(report_id)

    def get_uur_report(self, report_id: str) -> Optional[UURReport]:
        """
        Get a UUR report by ID.

        Args:
            report_id: Report ID (GUID)

        Returns:
            UURReport or None
        """
        return self._repo.get_uur_report(report_id)

    def get_report_as_xml(self, report_id: str) -> Optional[str]:
        """
        Get a report in XML format.

        Args:
            report_id: Report ID (GUID)

        Returns:
            XML string or None
        """
        return self._repo.get_wsxf(report_id)

    # =========================================================================
    # Report Factory Methods
    # =========================================================================

    @staticmethod
    def create_uut_report(
        pn: str,
        sn: str,
        rev: str = "1",
        process_code: int = 0,
        station_name: str = "TestStation",
        location: str = "TestLab",
        purpose: str = "Production",
        status: ResultStatus = ResultStatus.PASSED,
        start_time: Optional[datetime] = None,
        **kwargs
    ) -> UUTReport:
        """
        Create a new UUT test report.

        Args:
            pn: Part number
            sn: Serial number
            rev: Revision (default "1")
            process_code: Process code (default 0)
            station_name: Station name
            location: Location
            purpose: Purpose
            status: Result status (default PASSED)
            start_time: Start time (default: now)
            **kwargs: Additional root parameters

        Returns:
            UUTReport object
        """
        return UUTReport.create_basic(
            pn=pn,
            sn=sn,
            rev=rev,
            process_code=process_code,
            station_name=station_name,
            location=location,
            purpose=purpose,
            status=status,
            start=start_time or datetime.now(),
            **kwargs
        )

    @staticmethod
    def create_uur_report(
        pn: str,
        sn: str,
        rev: str = "1",
        process_code: int = 0,
        station_name: str = "RepairStation",
        location: str = "RepairLab",
        purpose: str = "Repair",
        status: ResultStatus = ResultStatus.PASSED,
        user: str = "Technician",
        start_time: Optional[datetime] = None,
        **kwargs
    ) -> UURReport:
        """
        Create a new UUR repair report.

        Args:
            pn: Part number
            sn: Serial number
            rev: Revision (default "1")
            process_code: Process code (default 0)
            station_name: Station name
            location: Location
            purpose: Purpose
            status: Result status (default PASSED)
            user: User who performed repair
            start_time: Start time (default: now)
            **kwargs: Additional root parameters

        Returns:
            UURReport object
        """
        return UURReport.create_basic(
            pn=pn,
            sn=sn,
            rev=rev,
            process_code=process_code,
            station_name=station_name,
            location=location,
            purpose=purpose,
            status=status,
            user=user,
            start=start_time or datetime.now(),
            **kwargs
        )

    # =========================================================================
    # Report Analysis
    # =========================================================================

    @staticmethod
    def is_passing(report: Union[UUTReport, UURReport]) -> bool:
        """
        Check if a report has passing status.

        Args:
            report: Report to check

        Returns:
            True if report is passing
        """
        root = report.root
        if root and root.status:
            return root.status == ResultStatus.PASSED
        return False

    @staticmethod
    def count_steps(report: UUTReport) -> int:
        """
        Count total steps in a report.

        Args:
            report: UUT report

        Returns:
            Total number of steps
        """
        root = report.root
        if root and root.steps:
            return len(root.steps)
        return 0

    @staticmethod
    def count_failing_steps(report: UUTReport) -> int:
        """
        Count failing steps in a report.

        Args:
            report: UUT report

        Returns:
            Number of failing steps
        """
        count = 0
        root = report.root
        if root and root.steps:
            for step in root.steps:
                if step.status == ResultStatus.FAILED:
                    count += 1
        return count

    @staticmethod
    def get_step_by_name(
        report: UUTReport, name: str
    ) -> Optional[SequenceCall]:
        """
        Find a step by name.

        Args:
            report: UUT report
            name: Step name to find

        Returns:
            SequenceCall if found
        """
        root = report.root
        if root and root.steps:
            for step in root.steps:
                if step.name == name:
                    return step
        return None
