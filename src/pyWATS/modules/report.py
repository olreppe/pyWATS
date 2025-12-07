"""Report Module for pyWATS

Provides high-level operations for querying and working with test reports.
"""
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING
from uuid import UUID
from datetime import datetime

from ..models.report_query import (
    ReportHeader, WATSFilter, Attachment,
    YieldData, ProcessInfo, LevelInfo, ProductGroup
)
from ..rest_api import ReportApi

# Import UUT/UUR models for type hints and working with reports
if TYPE_CHECKING:
    from ..models.report import UUTReport, UURReport


class ReportModule:
    """
    Report management module.
    
    Provides operations for:
    - Querying report headers (UUT and UUR)
    - Getting full report data (WSJF/WSXF formats)
    - Creating and submitting new reports (UUTReport/UURReport)
    - Managing attachments
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Query UUT reports
        filter = WATSFilter(part_number="PART-001", top_count=100)
        headers = api.report.query_uut_headers(filter)
        
        # Get a full report as WSJF
        report_data = api.report.get_wsjf("report-uuid")
        
        # Submit a new report
        api.report.submit_wsjf(report_data)
    """
    
    def __init__(self, api: ReportApi):
        """
        Initialize ReportModule with REST API client.
        
        Args:
            api: ReportApi instance for making HTTP requests
        """
        self._api = api
    
    # -------------------------------------------------------------------------
    # Query Operations
    # -------------------------------------------------------------------------
    
    def query_uut_headers(self, filter: Optional[WATSFilter] = None) -> List[ReportHeader]:
        """
        Query UUT (Unit Under Test) report headers.
        
        GET /api/Report/Query/Header?reportType=uut
        
        Args:
            filter: Optional WATSFilter for filtering results
            
        Returns:
            List of ReportHeader objects
        """
        # REST API now returns List[ReportHeader] directly
        return self._api.query_headers("uut", filter)
    
    def query_uur_headers(self, filter: Optional[WATSFilter] = None) -> List[ReportHeader]:
        """
        Query UUR (Unit Under Repair) report headers.
        
        GET /api/Report/Query/Header?reportType=uur
        
        Args:
            filter: Optional WATSFilter for filtering results
            
        Returns:
            List of ReportHeader objects
        """
        # REST API now returns List[ReportHeader] directly
        return self._api.query_headers("uur", filter)
    
    def query_headers(
        self,
        report_type: str = "uut",
        filter: Optional[WATSFilter] = None
    ) -> List[ReportHeader]:
        """
        Query report headers by type.
        
        GET /api/Report/Query/Header
        
        Args:
            report_type: Report type ("uut" or "uur")
            filter: Optional WATSFilter for filtering results
            
        Returns:
            List of ReportHeader objects
        """
        # REST API now returns List[ReportHeader] directly
        return self._api.query_headers(report_type, filter)
    
    def query_headers_by_misc_info(
        self,
        description: str,
        string_value: str,
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        """
        Get report headers by searching for misc information.
        
        GET /api/Report/Query/HeaderByMiscInfo
        
        Args:
            description: Misc info description
            string_value: Misc info string value
            top: Optional max number of results
            
        Returns:
            List of ReportHeader objects
        """
        # REST API now returns List[ReportHeader] directly
        return self._api.query_headers_by_misc_info(description, string_value, top)
    
    # -------------------------------------------------------------------------
    # Get Report Data
    # -------------------------------------------------------------------------
    
    def get_wsjf(self, report_id: Union[str, UUID]) -> Optional[Union["UUTReport", "UURReport"]]:
        """
        Get report in WATS Standard JSON Format (WSJF).
        
        GET /api/Report/Wsjf/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Report data as UUTReport or UURReport, or None
        """
        # REST API now returns Optional[Union[UUTReport, UURReport]] directly
        return self._api.get_wsjf(str(report_id))
    
    def get_wsxf(self, report_id: Union[str, UUID]) -> Optional[bytes]:
        """
        Get report in WATS Standard XML Format (WSXF).
        
        GET /api/Report/Wsxf/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Report data in WSXF format as bytes, or None
        """
        # REST API now returns Optional[bytes] directly
        return self._api.get_wsxf(str(report_id))
    
    # -------------------------------------------------------------------------
    # Submit Reports
    # -------------------------------------------------------------------------
    
    def submit_wsjf(self, report_data: Dict[str, Any]) -> Optional[str]:
        """
        Submit a report in WATS Standard JSON Format.
        
        POST /api/Report/WSJF
        
        Args:
            report_data: Report data in WSJF format
            
        Returns:
            Report ID if successful, None otherwise
        """
        # REST API now returns Optional[str] directly
        return self._api.post_wsjf(report_data)
    
    def submit_wsxf(self, report_xml: str) -> Optional[str]:
        """
        Submit a report in WATS Standard XML Format.
        
        POST /api/Report/WSXF
        
        Args:
            report_xml: Report data in WSXF format (XML string)
            
        Returns:
            Report ID if successful, None otherwise
        """
        # REST API now returns Optional[str] directly
        return self._api.post_wsxf(report_xml)
    
    # -------------------------------------------------------------------------
    # Attachment Operations
    # -------------------------------------------------------------------------
    
    def get_attachment(
        self,
        attachment_id: Optional[str] = None,
        step_id: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Get an attachment from a report.
        
        GET /api/Report/Attachment
        
        Args:
            attachment_id: The attachment ID
            step_id: The step ID
            
        Returns:
            Attachment content as bytes, or None
        """
        # REST API now returns Optional[bytes] directly
        return self._api.get_attachment(attachment_id, step_id)
    
    def get_attachments_as_zip(self, report_id: Union[str, UUID]) -> Optional[bytes]:
        """
        Get all attachments for a report as a zip archive.
        
        GET /api/Report/Attachments/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Zip archive content as bytes, or None
        """
        # REST API now returns Optional[bytes] directly
        return self._api.get_attachments_as_zip(str(report_id))
    
    def get_certificate(self, report_id: Union[str, UUID]) -> Optional[bytes]:
        """
        Get certificate for a report.
        
        GET /api/Report/Certificate/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Certificate content as bytes (usually PDF), or None
        """
        # REST API now returns Optional[bytes] directly
        return self._api.get_certificate(str(report_id))
    
    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------
    
    def get_reports_by_serial(
        self,
        serial_number: str,
        report_type: str = "uut",
        top_count: int = 100
    ) -> List[ReportHeader]:
        """
        Get reports for a specific serial number.
        
        Args:
            serial_number: Unit serial number
            report_type: Report type ("uut" or "uur")
            top_count: Maximum number of results
            
        Returns:
            List of ReportHeader objects
        """
        filter = WATSFilter(serialNumber=serial_number, topCount=top_count)
        return self.query_headers(report_type, filter)
    
    def get_reports_by_part(
        self,
        part_number: str,
        revision: Optional[str] = None,
        report_type: str = "uut",
        top_count: int = 100
    ) -> List[ReportHeader]:
        """
        Get reports for a specific product.
        
        Args:
            part_number: Product part number
            revision: Optional product revision
            report_type: Report type ("uut" or "uur")
            top_count: Maximum number of results
            
        Returns:
            List of ReportHeader objects
        """
        filter = WATSFilter(
            partNumber=part_number,
            revision=revision,
            topCount=top_count
        )
        return self.query_headers(report_type, filter)
    
    def get_reports_by_date_range(
        self,
        date_from: datetime,
        date_to: datetime,
        report_type: str = "uut",
        top_count: int = 1000
    ) -> List[ReportHeader]:
        """
        Get reports within a date range.
        
        Args:
            date_from: Start date
            date_to: End date
            report_type: Report type ("uut" or "uur")
            top_count: Maximum number of results
            
        Returns:
            List of ReportHeader objects
        """
        filter = WATSFilter(
            dateFrom=date_from,
            dateTo=date_to,
            topCount=top_count
        )
        return self.query_headers(report_type, filter)
    
    # -------------------------------------------------------------------------
    # UUT/UUR Report Operations
    # -------------------------------------------------------------------------
    
    def get_uut_report(self, report_id: Union[str, UUID]) -> "UUTReport":
        """
        Get a UUT report as a UUTReport object.
        
        Args:
            report_id: Report UUID
            
        Returns:
            UUTReport object
        """
        from ..models.report import UUTReport
        data = self.get_wsjf(report_id)
        return UUTReport.model_validate(data)
    
    def get_uur_report(self, report_id: Union[str, UUID]) -> "UURReport":
        """
        Get a UUR report as a UURReport object.
        
        Args:
            report_id: Report UUID
            
        Returns:
            UURReport object
        """
        from ..models.report import UURReport
        data = self.get_wsjf(report_id)
        return UURReport.model_validate(data)
    
    def create_uut_report(
        self,
        part_number: str,
        serial_number: str,
        revision: str,
        process_code: int,
        station_name: str,
        location: str,
        purpose: str,
        **kwargs
    ) -> "UUTReport":
        """
        Create a new UUT report.
        
        Args:
            part_number: Product part number
            serial_number: Unit serial number
            revision: Product revision
            process_code: Test process code
            station_name: Test station name
            location: Test location
            purpose: Test purpose
            **kwargs: Additional UUTReport fields
            
        Returns:
            New UUTReport object (not yet submitted)
        """
        from ..models.report import UUTReport
        return UUTReport(
            pn=part_number,
            sn=serial_number,
            rev=revision,
            process_code=process_code,
            station_name=station_name,
            location=location,
            purpose=purpose,
            **kwargs
        )
    
    def create_uur_report(
        self,
        part_number: str,
        serial_number: str,
        revision: str,
        process_code: int,
        station_name: str,
        location: str,
        purpose: str,
        **kwargs
    ) -> "UURReport":
        """
        Create a new UUR report.
        
        Args:
            part_number: Product part number
            serial_number: Unit serial number
            revision: Product revision
            process_code: Repair process code
            station_name: Repair station name
            location: Repair location
            purpose: Repair purpose
            **kwargs: Additional UURReport fields
            
        Returns:
            New UURReport object (not yet submitted)
        """
        from ..models.report import UURReport
        return UURReport(
            pn=part_number,
            sn=serial_number,
            rev=revision,
            process_code=process_code,
            station_name=station_name,
            location=location,
            purpose=purpose,
            **kwargs
        )
    
    def submit(self, report: Union["UUTReport", "UURReport"]) -> Optional[str]:
        """
        Submit a UUT or UUR report to WATS.
        
        Args:
            report: UUTReport or UURReport object to submit
            
        Returns:
            Report ID if successful, None otherwise
        """
        # Convert Pydantic model to dict using model_dump with by_alias=True
        report_data = report.model_dump(by_alias=True, exclude_none=True)
        return self.submit_wsjf(report_data)
