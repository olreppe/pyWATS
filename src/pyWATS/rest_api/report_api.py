"""
Report API Endpoints

Provides all REST API calls for report management.
All methods return typed model objects instead of raw responses.

Public API Endpoints (from Swagger):
- GET /api/Report/Attachment - Get attachment by attachmentId or stepId
- GET /api/Report/Attachments/{id} - Get all attachments as zip
- GET /api/Report/Certificate/{id} - Get certificate
- GET /api/Report/Query/Header - Query report headers with filter
- GET /api/Report/Query/HeaderByMiscInfo - Query by misc info
- POST /api/Report/WSJF - Post new WSJF report
- GET /api/Report/Wsjf/{id} - Get report in WSJF format
- POST /api/Report/WSXF - Post new WSXF report
- GET /api/Report/Wsxf/{id} - Get report in WSXF format
"""

from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..models import (
    ReportHeader, WATSFilter, UUTReport, UURReport, Report
)


class ReportApi:
    """
    Report API endpoints.
    
    Endpoints for creating, retrieving, and managing test reports (UUT/UUR).
    All methods return typed model objects.
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Report Query
    # =========================================================================
    
    def query_headers(
        self,
        report_type: str = "uut",
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None
    ) -> List[ReportHeader]:
        """
        Query report headers matching the specified filter.
        
        GET /api/Report/Query/Header
        
        Args:
            report_type: Report type ("uut" or "uur")
            filter_data: WATSFilter object or dict with keys like:
                - productGroup, level, serialNumber, partNumber
                - revision, batchNumber, stationName, testOperation
                - status, miscValue, dateFrom, dateTo, topCount
            
        Returns:
            List of ReportHeader objects
        """
        params: Dict[str, Any] = {"reportType": report_type}
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                params.update(filter_data.model_dump(by_alias=True, exclude_none=True))
            else:
                params.update(filter_data)
        response = self._http.get("/api/Report/Query/Header", params=params)
        if response.is_success and response.data:
            return [ReportHeader.model_validate(item) for item in response.data]
        return []
    
    def query_headers_by_misc_info(
        self,
        description: str,
        string_value: str,
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Get report header data by searching for misc information.
        
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
        response = self._http.get("/api/Report/Query/HeaderByMiscInfo", params=params)
        if response.is_success and response.data:
            return [ReportHeader.model_validate(item) for item in response.data]
        return []
    
    # =========================================================================
    # Report WSJF (WATS Standard JSON Format)
    # =========================================================================
    
    def post_wsjf(
        self, report: Union[UUTReport, UURReport, Dict[str, Any]]
    ) -> Optional[str]:
        """
        Post a new WSJF report.
        
        POST /api/Report/WSJF
        
        Args:
            report: UUTReport, UURReport object or report data dict in WSJF format
            
        Returns:
            Report ID if successful, None otherwise
        """
        if isinstance(report, (UUTReport, UURReport)):
            data = report.model_dump(by_alias=True, exclude_none=True)
        else:
            data = report
        response = self._http.post("/api/Report/WSJF", data=data)
        if response.is_success and response.data:
            # Response typically contains the report ID
            return response.data.get("id") if isinstance(response.data, dict) else str(response.data)
        return None
    
    def get_wsjf(self, report_id: str) -> Optional[Union[UUTReport, UURReport]]:
        """
        Return a report in WSJF (WATS Standard JSON Format).
        
        GET /api/Report/Wsjf/{id}
        
        Args:
            report_id: The report ID (GUID)
            
        Returns:
            UUTReport or UURReport object, or None if not found
        """
        response = self._http.get(f"/api/Report/Wsjf/{report_id}")
        if response.is_success and response.data:
            # Determine type based on report content
            if response.data.get("uur"):
                return UURReport.model_validate(response.data)
            return UUTReport.model_validate(response.data)
        return None
    
    # =========================================================================
    # Report WSXF (WATS Standard XML Format)
    # =========================================================================
    
    def post_wsxf(self, report_xml: str) -> Optional[str]:
        """
        Post a new WSXF report.
        
        POST /api/Report/WSXF
        
        Args:
            report_xml: Report data in WSXF (XML) format
            
        Returns:
            Report ID if successful, None otherwise
        """
        headers = {"Content-Type": "application/xml"}
        response = self._http.post("/api/Report/WSXF", data=report_xml, headers=headers)
        if response.is_success and response.data:
            return response.data.get("id") if isinstance(response.data, dict) else str(response.data)
        return None
    
    def get_wsxf(self, report_id: str) -> Optional[bytes]:
        """
        Return a report in WSXF (WATS Standard XML Format).
        
        GET /api/Report/Wsxf/{id}
        
        Args:
            report_id: The report ID (GUID)
            
        Returns:
            Report XML as bytes, or None if not found
        """
        response = self._http.get(f"/api/Report/Wsxf/{report_id}")
        if response.is_success:
            return response.raw
        return None
    
    # =========================================================================
    # Attachments
    # =========================================================================
    
    def get_attachment(
        self,
        attachment_id: Optional[str] = None,
        step_id: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Get an attachment from a report using either attachmentId or stepId.
        
        GET /api/Report/Attachment
        
        Args:
            attachment_id: The attachment ID
            step_id: The step ID
            
        Returns:
            Attachment data as bytes, or None if not found
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
    
    def get_attachments_as_zip(self, report_id: str) -> Optional[bytes]:
        """
        Returns all attachments connected to a report as a zip archive.
        
        GET /api/Report/Attachments/{id}
        
        Args:
            report_id: The report ID
            
        Returns:
            Zip archive as bytes, or None if not found
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
            report_id: The report ID
            
        Returns:
            Certificate data as bytes, or None if not found
        """
        response = self._http.get(f"/api/Report/Certificate/{report_id}")
        if response.is_success:
            return response.raw
        return None
