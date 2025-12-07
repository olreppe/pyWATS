"""Report Module for pyWATS

Provides high-level operations for querying and working with test reports.
"""
from typing import List, Optional, Union, TYPE_CHECKING
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

""" 
API INFO / SWAGGER DOC
get /api/Report/Attachment
Get an attachment from a report using either attachmentId or stepId.

get /api/Report/Attachments/{id}
Returns all attachments connected to a report as a zip archive

get /api/Report/Certificate/{id}
get /api/Report/Query/Header
Returns a list of most recent reports matching the specified filter.

get /api/Report/Query/HeaderByMiscInfo
Get report header data by searching for misc information

post /api/Report/WSJF
Post a new WSJF report.

get /api/Report/Wsjf/{id}
Return a report in WSJF (Wats Standard JSON Format).

post /api/Report/WSXF
Post a new WSXF report.

get /api/Report/Wsxf/{id}
Return a report in WSXF (Wats Standard Xml Format)



"""



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
        filter_dict = filter.to_dict() if filter else {}
        response = self._api.query_headers("uut", filter_dict)
        data = response.data if response.data else []
        return [ReportHeader.from_dict(h) for h in data]
    
    def query_uur_headers(self, filter: Optional[WATSFilter] = None) -> List[ReportHeader]:
        """
        Query UUR (Unit Under Repair) report headers.
        
        GET /api/Report/Query/Header?reportType=uur
        
        Args:
            filter: Optional WATSFilter for filtering results
            
        Returns:
            List of ReportHeader objects
        """
        filter_dict = filter.to_dict() if filter else {}
        response = self._api.query_headers("uur", filter_dict)
        data = response.data if response.data else []
        return [ReportHeader.from_dict(h) for h in data]
    
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
        filter_dict = filter.to_dict() if filter else {}
        response = self._api.query_headers(report_type, filter_dict)
        data = response.data if response.data else []
        return [ReportHeader.from_dict(h) for h in data]
    
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
        response = self._api.query_headers_by_misc_info(description, string_value, top)
        data = response.data if response.data else []
        return [ReportHeader.from_dict(h) for h in data]
    
    # -------------------------------------------------------------------------
    # Get Report Data
    # -------------------------------------------------------------------------
    
    def get_wsjf(self, report_id: Union[str, UUID]) -> dict:
        """
        Get report in WATS Standard JSON Format (WSJF).
        
        GET /api/Report/Wsjf/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Report data in WSJF format
        """
        response = self._api.get_wsjf(str(report_id))
        return response.data
    
    def get_wsxf(self, report_id: Union[str, UUID]) -> str:
        """
        Get report in WATS Standard XML Format (WSXF).
        
        GET /api/Report/Wsxf/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Report data in WSXF format (XML string)
        """
        response = self._api.get_wsxf(str(report_id))
        return response.data
    
    # -------------------------------------------------------------------------
    # Submit Reports
    # -------------------------------------------------------------------------
    
    def submit_wsjf(self, report_data: dict) -> dict:
        """
        Submit a report in WATS Standard JSON Format.
        
        POST /api/Report/WSJF
        
        Args:
            report_data: Report data in WSJF format
            
        Returns:
            Submission result
        """
        response = self._api.post_wsjf(report_data)
        return response.data
    
    def submit_wsxf(self, report_xml: str) -> dict:
        """
        Submit a report in WATS Standard XML Format.
        
        POST /api/Report/WSXF
        
        Args:
            report_xml: Report data in WSXF format (XML string)
            
        Returns:
            Submission result
        """
        response = self._api.post_wsxf(report_xml)
        return response.data
    
    # -------------------------------------------------------------------------
    # Attachment Operations
    # -------------------------------------------------------------------------
    
    def get_attachment(
        self,
        attachment_id: Optional[str] = None,
        step_id: Optional[str] = None
    ) -> bytes:
        """
        Get an attachment from a report.
        
        GET /api/Report/Attachment
        
        Args:
            attachment_id: The attachment ID
            step_id: The step ID
            
        Returns:
            Attachment content as bytes
        """
        response = self._api.get_attachment(attachment_id, step_id)
        return response.raw
    
    def get_attachments_as_zip(self, report_id: Union[str, UUID]) -> bytes:
        """
        Get all attachments for a report as a zip archive.
        
        GET /api/Report/Attachments/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Zip archive content as bytes
        """
        response = self._api.get_attachments_as_zip(str(report_id))
        return response.raw
    
    def get_certificate(self, report_id: Union[str, UUID]) -> bytes:
        """
        Get certificate for a report.
        
        GET /api/Report/Certificate/{id}
        
        Args:
            report_id: Report UUID
            
        Returns:
            Certificate content as bytes (usually PDF)
        """
        response = self._api.get_certificate(str(report_id))
        return response.raw
    
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
        filter = WATSFilter(serial_number=serial_number, top_count=top_count)
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
            part_number=part_number,
            revision=revision,
            top_count=top_count
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
            date_from=date_from,
            date_to=date_to,
            top_count=top_count
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
    
    def submit(self, report: Union["UUTReport", "UURReport"]) -> dict:
        """
        Submit a UUT or UUR report to WATS.
        
        Args:
            report: UUTReport or UURReport object to submit
            
        Returns:
            Submission result with report ID
        """
        # Convert Pydantic model to dict using model_dump with by_alias=True
        report_data = report.model_dump(by_alias=True, exclude_none=True)
        return self.submit_wsjf(report_data)
