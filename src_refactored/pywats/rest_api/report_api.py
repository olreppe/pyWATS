"""
Report API Endpoints

Provides all REST API calls for report management.

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

from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient, Response


class ReportApi:
    """
    Report API endpoints.
    
    Endpoints for creating, retrieving, and managing test reports (UUT/UUR).
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Report Query
    # =========================================================================
    
    def query_headers(
        self,
        report_type: str = "uut",
        filter_data: Optional[Dict[str, Any]] = None
    ) -> 'Response':
        """
        Query report headers matching the specified filter.
        
        GET /api/Report/Query/Header
        
        Args:
            report_type: Report type ("uut" or "uur")
            filter_data: Filter dictionary with keys like:
                - productGroup, level, serialNumber, partNumber
                - revision, batchNumber, stationName, testOperation
                - status, miscValue, dateFrom, dateTo, topCount
            
        Returns:
            Response with report headers
        """
        params: Dict[str, Any] = {"reportType": report_type}
        if filter_data:
            params.update(filter_data)
        return self._http.get("/api/Report/Query/Header", params=params)
    
    def query_headers_by_misc_info(
        self,
        description: str,
        string_value: str,
        top: Optional[int] = None
    ) -> 'Response':
        """
        Get report header data by searching for misc information.
        
        GET /api/Report/Query/HeaderByMiscInfo
        
        Args:
            description: Misc info description
            string_value: Misc info string value
            top: Number of records to return
            
        Returns:
            Response with report headers
        """
        params: Dict[str, Any] = {
            "description": description,
            "stringValue": string_value
        }
        if top:
            params["$top"] = top
        return self._http.get("/api/Report/Query/HeaderByMiscInfo", params=params)
    
    # =========================================================================
    # Report WSJF (WATS Standard JSON Format)
    # =========================================================================
    
    def post_wsjf(self, report_data: Dict[str, Any]) -> 'Response':
        """
        Post a new WSJF report.
        
        POST /api/Report/WSJF
        
        Args:
            report_data: Report data in WSJF format
            
        Returns:
            Response with submission result
        """
        return self._http.post("/api/Report/WSJF", data=report_data)
    
    def get_wsjf(self, report_id: str) -> 'Response':
        """
        Return a report in WSJF (WATS Standard JSON Format).
        
        GET /api/Report/Wsjf/{id}
        
        Args:
            report_id: The report ID (GUID)
            
        Returns:
            Response with report in WSJF format
        """
        return self._http.get(f"/api/Report/Wsjf/{report_id}")
    
    # =========================================================================
    # Report WSXF (WATS Standard XML Format)
    # =========================================================================
    
    def post_wsxf(self, report_xml: str) -> 'Response':
        """
        Post a new WSXF report.
        
        POST /api/Report/WSXF
        
        Args:
            report_xml: Report data in WSXF (XML) format
            
        Returns:
            Response with submission result
        """
        headers = {"Content-Type": "application/xml"}
        return self._http.post("/api/Report/WSXF", data=report_xml, headers=headers)
    
    def get_wsxf(self, report_id: str) -> 'Response':
        """
        Return a report in WSXF (WATS Standard XML Format).
        
        GET /api/Report/Wsxf/{id}
        
        Args:
            report_id: The report ID (GUID)
            
        Returns:
            Response with report in WSXF format
        """
        return self._http.get(f"/api/Report/Wsxf/{report_id}")
    
    # =========================================================================
    # Attachments
    # =========================================================================
    
    def get_attachment(
        self,
        attachment_id: Optional[str] = None,
        step_id: Optional[str] = None
    ) -> 'Response':
        """
        Get an attachment from a report using either attachmentId or stepId.
        
        GET /api/Report/Attachment
        
        Args:
            attachment_id: The attachment ID
            step_id: The step ID
            
        Returns:
            Response with attachment data
        """
        params: Dict[str, Any] = {}
        if attachment_id:
            params["attachmentId"] = attachment_id
        if step_id:
            params["stepId"] = step_id
        return self._http.get("/api/Report/Attachment", params=params)
    
    def get_attachments_as_zip(self, report_id: str) -> 'Response':
        """
        Returns all attachments connected to a report as a zip archive.
        
        GET /api/Report/Attachments/{id}
        
        Args:
            report_id: The report ID
            
        Returns:
            Response with zip archive of attachments
        """
        return self._http.get(f"/api/Report/Attachments/{report_id}")
    
    # =========================================================================
    # Certificate
    # =========================================================================
    
    def get_certificate(self, report_id: str) -> 'Response':
        """
        Get certificate for a report.
        
        GET /api/Report/Certificate/{id}
        
        Args:
            report_id: The report ID
            
        Returns:
            Response with certificate data
        """
        return self._http.get(f"/api/Report/Certificate/{report_id}")
