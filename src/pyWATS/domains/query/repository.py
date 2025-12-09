"""Query repository - data access layer.

API interactions for report queries and statistics.
"""
from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ...core import WATSClient

from .models import WATSFilter, ReportHeader, YieldData


class QueryRepository:
    """
    Query data access layer.

    Handles all WATS API interactions for report queries.
    """

    def __init__(self, client: "WATSClient"):
        """
        Initialize with HTTP client.

        Args:
            client: WATSClient for making HTTP requests
        """
        self._http = client

    # =========================================================================
    # Report Header Queries
    # =========================================================================

    def query_headers(
        self,
        report_type: str = "uut",
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None
    ) -> List[ReportHeader]:
        """
        Query report headers matching the filter.

        GET /api/Report/Query/Header

        Args:
            report_type: Report type ("uut" or "uur")
            filter_data: WATSFilter object or dict

        Returns:
            List of ReportHeader objects
        """
        params: Dict[str, Any] = {"reportType": report_type}
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                params.update(
                    filter_data.model_dump(by_alias=True, exclude_none=True)
                )
            else:
                params.update(filter_data)
        response = self._http.get("/api/Report/Query/Header", params=params)
        if response.is_success and response.data:
            return [
                ReportHeader.model_validate(item)
                for item in response.data
            ]
        return []

    def query_headers_by_misc_info(
        self,
        description: str,
        string_value: str,
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Get report headers by misc info search.

        GET /api/Report/Query/HeaderByMiscInfo

        Args:
            description: Misc info description
            string_value: Misc info string value
            top: Number of records to return

        Returns:
            List of ReportHeader objects
        """
        params: Dict[str, Any] = {
            "description": description,
            "stringValue": string_value
        }
        if top:
            params["$top"] = top
        response = self._http.get(
            "/api/Report/Query/HeaderByMiscInfo", params=params
        )
        if response.is_success and response.data:
            return [
                ReportHeader.model_validate(item)
                for item in response.data
            ]
        return []

    # =========================================================================
    # Yield Queries
    # =========================================================================

    def get_yield(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None
    ) -> List[YieldData]:
        """
        Get yield statistics with filter.

        POST /api/Stats/Yield

        Args:
            filter_data: WATSFilter object or dict

        Returns:
            List of YieldData objects
        """
        data: Dict[str, Any] = {}
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                data = filter_data.model_dump(by_alias=True, exclude_none=True)
            else:
                data = filter_data
        response = self._http.post("/api/Stats/Yield", data=data)
        if response.is_success and response.data:
            return [
                YieldData.model_validate(item)
                for item in response.data
            ]
        return []

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

        GET /api/Report/Attachment

        Args:
            attachment_id: Attachment ID
            step_id: Step ID

        Returns:
            Attachment content as bytes or None
        """
        params: Dict[str, Any] = {}
        if attachment_id:
            params["attachmentId"] = attachment_id
        if step_id:
            params["stepId"] = step_id
        response = self._http.get("/api/Report/Attachment", params=params)
        if response.is_success:
            return response.raw
        return None

    def get_attachments_zip(self, report_id: str) -> Optional[bytes]:
        """
        Get all attachments for a report as zip.

        GET /api/Report/Attachments/{id}

        Args:
            report_id: Report ID

        Returns:
            Zip file content as bytes or None
        """
        response = self._http.get(f"/api/Report/Attachments/{report_id}")
        if response.is_success:
            return response.raw
        return None

    # =========================================================================
    # Certificate
    # =========================================================================

    def get_certificate(self, report_id: str) -> Optional[bytes]:
        """
        Get certificate for a report.

        GET /api/Report/Certificate/{id}

        Args:
            report_id: Report ID

        Returns:
            Certificate content as bytes or None
        """
        response = self._http.get(f"/api/Report/Certificate/{report_id}")
        if response.is_success:
            return response.raw
        return None
