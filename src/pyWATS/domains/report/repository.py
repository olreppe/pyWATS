"""Report repository - data access layer.

All API interactions for test reports.
"""
from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ...core import WATSClient

from ...models.report import UUTReport, UURReport


class ReportRepository:
    """
    Report data access layer.

    Handles all WATS API interactions for test reports.
    """

    def __init__(self, client: "WATSClient"):
        """
        Initialize with HTTP client.

        Args:
            client: WATSClient for making HTTP requests
        """
        self._http = client

    # =========================================================================
    # Report WSJF (JSON Format)
    # =========================================================================

    def post_wsjf(
        self, report: Union[UUTReport, UURReport, Dict[str, Any]]
    ) -> Optional[str]:
        """
        Post a new WSJF report.

        POST /api/Report/WSJF

        Args:
            report: UUTReport, UURReport or report data dict

        Returns:
            Report ID if successful, None otherwise
        """
        if isinstance(report, (UUTReport, UURReport)):
            data = report.model_dump(by_alias=True, exclude_none=True)
        else:
            data = report
        response = self._http.post("/api/Report/WSJF", data=data)
        if response.is_success and response.data:
            if isinstance(response.data, dict):
                return response.data.get("id")
            return str(response.data)
        return None

    def get_wsjf(
        self, report_id: str
    ) -> Optional[Union[UUTReport, UURReport]]:
        """
        Get a report in WSJF format.

        GET /api/Report/Wsjf/{id}

        Args:
            report_id: The report ID (GUID)

        Returns:
            UUTReport or UURReport, or None
        """
        response = self._http.get(f"/api/Report/Wsjf/{report_id}")
        if response.is_success and response.data:
            if response.data.get("uur"):
                return UURReport.model_validate(response.data)
            return UUTReport.model_validate(response.data)
        return None

    def get_uut_report(self, report_id: str) -> Optional[UUTReport]:
        """
        Get a UUT report by ID.

        GET /api/Report/Wsjf/{id}

        Args:
            report_id: The report ID (GUID)

        Returns:
            UUTReport or None
        """
        report = self.get_wsjf(report_id)
        if isinstance(report, UUTReport):
            return report
        return None

    def get_uur_report(self, report_id: str) -> Optional[UURReport]:
        """
        Get a UUR report by ID.

        GET /api/Report/Wsjf/{id}

        Args:
            report_id: The report ID (GUID)

        Returns:
            UURReport or None
        """
        report = self.get_wsjf(report_id)
        if isinstance(report, UURReport):
            return report
        return None

    # =========================================================================
    # Report WSXF (XML Format)
    # =========================================================================

    def post_wsxf(self, xml_content: str) -> Optional[str]:
        """
        Post a new WSXF (XML) report.

        POST /api/Report/WSXF

        Args:
            xml_content: Report as XML string

        Returns:
            Report ID if successful, None otherwise
        """
        headers = {"Content-Type": "application/xml"}
        response = self._http.post(
            "/api/Report/WSXF",
            data=xml_content,
            headers=headers
        )
        if response.is_success and response.data:
            if isinstance(response.data, dict):
                return response.data.get("id")
            return str(response.data)
        return None

    def get_wsxf(self, report_id: str) -> Optional[str]:
        """
        Get a report in WSXF (XML) format.

        GET /api/Report/Wsxf/{id}

        Args:
            report_id: The report ID (GUID)

        Returns:
            XML string or None
        """
        response = self._http.get(f"/api/Report/Wsxf/{report_id}")
        if response.is_success:
            # Raw response for XML
            return response.raw.decode("utf-8") if response.raw else None
        return None
