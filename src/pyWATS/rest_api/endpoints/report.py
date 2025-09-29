"""
Report Endpoints

Report management endpoints for retrieving and submitting test reports.
These endpoints are grouped by the "Report" tag in the OpenAPI specification.
"""

from typing import Optional, Dict, Any, List
from uuid import UUID
import httpx

from ..client import get_default_client, WATSClient
from ..exceptions import handle_response_error
from ..models import ReportHeader, InsertReportResult, UUTResult


def get_attachment(
    report_id: UUID,
    attachment_id: Optional[UUID] = None,
    step_id: Optional[int] = None,
    client: Optional[WATSClient] = None
) -> bytes:
    """
    Get an attachment from a report using either attachment_id or step_id.
    
    Args:
        report_id: ID of the report
        attachment_id: ID of the attachment (for repair reports)
        step_id: Step ID of the attachment (for test reports)
        client: Optional WATS client instance
        
    Returns:
        Attachment content as bytes
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"reportId": str(report_id)}
    if attachment_id:
        params["attachmentId"] = str(attachment_id)
    if step_id is not None:
        params["stepId"] = str(step_id)
    
    response = client.get("/api/Report/Attachment", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.content


def get_attachments(
    report_id: UUID,
    client: Optional[WATSClient] = None
) -> bytes:
    """
    Return all attachments connected to a report as a zip archive.
    
    Args:
        report_id: Report ID
        client: Optional WATS client instance
        
    Returns:
        Zip archive content as bytes
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get(f"/api/Report/Attachments/{report_id}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.content


def get_certificate(
    report_id: UUID,
    client: Optional[WATSClient] = None
) -> bytes:
    """
    Get certificate for a report.
    
    Args:
        report_id: Report ID
        client: Optional WATS client instance
        
    Returns:
        Certificate content as bytes
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get(f"/api/Report/Certificate/{report_id}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.content


def query_report_headers(
    odata_filter: Optional[str] = None,
    odata_top: Optional[int] = None,
    odata_orderby: Optional[str] = None,
    odata_skip: Optional[int] = None,
    odata_select: Optional[str] = None,
    odata_expand: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> List[ReportHeader]:
    """
    Query report headers with OData support.
    
    Returns a list of most recent reports matching the specified filter.
    By default top 10 reports are returned ordered by report start date/time.
    
    Args:
        odata_filter: OData $filter parameter
        odata_top: OData $top parameter  
        odata_orderby: OData $orderby parameter
        odata_skip: OData $skip parameter
        odata_select: OData $select parameter
        odata_expand: OData $expand parameter
        client: Optional WATS client instance
        
    Returns:
        List of report headers
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if odata_filter:
        params["$filter"] = odata_filter
    if odata_top is not None:
        params["$top"] = odata_top
    if odata_orderby:
        params["$orderby"] = odata_orderby
    if odata_skip is not None:
        params["$skip"] = odata_skip
    if odata_select:
        params["$select"] = odata_select
    if odata_expand:
        params["$expand"] = odata_expand
    
    response = client.get("/api/Report/Query/Header", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return [ReportHeader(**item) for item in data]


def get_header_by_misc_info(
    process_code: Optional[int] = None,
    serial_number: Optional[str] = None,
    description: Optional[str] = None,
    data: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> List[UUTResult]:
    """
    Get report header data by searching for misc information.
    
    Args:
        process_code: Report's process code
        serial_number: Report serial number
        description: Misc info description value
        data: Misc info data value
        client: Optional WATS client instance
        
    Returns:
        List of UUT results
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if process_code is not None:
        params["processCode"] = process_code
    if serial_number:
        params["serialNumber"] = serial_number
    if description:
        params["description"] = description
    if data:
        params["data"] = data
    
    response = client.get("/api/Report/Query/HeaderByMiscInfo", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    results = []
    for item in data:
        # Ensure item is a dict with string keys
        if isinstance(item, dict):
            # Provide default values if missing
            item = {str(k): v for k, v in item.items()}
            if "serialNumber" not in item:
                item["serialNumber"] = ""
            if "partNumber" not in item:
                item["partNumber"] = ""
            results.append(UUTResult(**item))
    return results


def submit_wsjf_report(
    wsjf_data: Dict[str, Any],
    client: Optional[WATSClient] = None
) -> InsertReportResult:
    """
    Submit a new WSJF (WATS Standard JSON Format) report.
    
    Args:
        wsjf_data: WSJF report data
        client: Optional WATS client instance
        
    Returns:
        Report insertion result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.post("/api/Report/WSJF", json=wsjf_data)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    
    # Handle case where server returns a list instead of dict
    if isinstance(data, list):
        if len(data) > 0:
            # Take the first item if it's a list
            result_data = data[0]
            # Map server response fields to our model fields
            mapped_data = {
                'success': True,  # If we got a response, assume success
                'reportId': result_data.get('ID') or result_data.get('uuid'),
                'message': 'Report submitted successfully',
                'errors': []
            }
            return InsertReportResult(**mapped_data)
        else:
            # Return empty result if list is empty
            return InsertReportResult(success=False, message="Empty response from server", reportId=None)
    
    # Handle normal dict response (fallback)
    return InsertReportResult(**data)


def get_wsjf_report(
    report_id: UUID,
    detail_level: Optional[int] = None,
    include_chartdata: Optional[bool] = None,
    include_attachments: Optional[bool] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Return a report in WSJF (WATS Standard JSON Format).
    
    Args:
        report_id: Unique ID of a WATS Report
        detail_level: Level of detail (0-7, where 0 is identifying data, 7 is full)
        include_chartdata: Include chart data (plots) - default true
        include_attachments: Include attachment data - default true
        client: Optional WATS client instance
        
    Returns:
        WSJF report data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if detail_level is not None:
        params["detailLevel"] = detail_level
    if include_chartdata is not None:
        params["includeChartdata"] = include_chartdata
    if include_attachments is not None:
        params["includeAttachments"] = include_attachments
    
    response = client.get(f"/api/Report/Wsjf/{report_id}", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def submit_wsxf_report(
    wsxf_data: str,
    client: Optional[WATSClient] = None
) -> InsertReportResult:
    """
    Submit a new WSXF (WATS Standard XML Format) report.
    
    Args:
        wsxf_data: WSXF report XML data
        client: Optional WATS client instance
        
    Returns:
        Report insertion result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.post(
        "/api/Report/WSXF",
        data=wsxf_data,
        headers={"Content-Type": "application/xml"}
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return InsertReportResult(**data)


def get_wsxf_report(
    report_id: UUID,
    detail_level: Optional[int] = None,
    include_attachments: Optional[bool] = None,
    include_chartdata: Optional[bool] = None,
    include_indexes: Optional[bool] = None,
    client: Optional[WATSClient] = None
) -> str:
    """
    Return a report in WSXF (WATS Standard XML Format).
    
    Args:
        report_id: Unique ID of a WATS Report
        detail_level: Level of detail (0-7, where 0 is identifying data, 7 is full)
        include_attachments: Include attachment data - default true
        include_chartdata: Include chart data (plots) - default true
        include_indexes: Include indexes - default true
        client: Optional WATS client instance
        
    Returns:
        WSXF report XML data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if detail_level is not None:
        params["detailLevel"] = detail_level
    if include_attachments is not None:
        params["includeAttachments"] = include_attachments
    if include_chartdata is not None:
        params["includeChartdata"] = include_chartdata
    if include_indexes is not None:
        params["includeIndexes"] = include_indexes
    
    response = client.get(f"/api/Report/Wsxf/{report_id}", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.text