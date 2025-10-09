"""
Report module for WATS API.

This module provides functionality for generating reports, analytics,
loading and managing test reports from the WATS system.
"""

from typing import List, Optional, Dict, Any, Union, cast
from datetime import datetime
from uuid import UUID, uuid4
import os
from .base import BaseModule
from ..exceptions import WATSException, WATSNotFoundError
from ..models.report import UUTReport, UURReport, Report

# Import REST API endpoints
from ..rest_api.public.api.report import (
    report_header_query,
    report_get_report_as_wsjf,
    report_post_wsjf
)
from ..rest_api.public.models.virinco_wats_web_dashboard_models_o_data_report_header import (
    VirincoWATSWebDashboardModelsODataReportHeader
)
from ..rest_api.public.models.report_get_report_as_wsjf_response_200 import (
    ReportGetReportAsWSJFResponse200
)
from ..rest_api.public.client import Client


class ReportModule(BaseModule):
    """
    Report and analytics module.
    
    Provides methods for:
    - Creating and managing test reports
    - Loading and managing test reports
    - Submitting reports to WATS
    - Generating statistical reports
    - Retrieving production analytics
    - Accessing performance metrics
    """
    
    def __init__(self, client):
        """Initialize the Report module."""
        super().__init__(client)
        self._pending_reports = []
    
    def create_uut_report(
        self, 
        operator: str, 
        part_number: str, 
        revision: str, 
        serial_number: str,
        operation_type: str, 
        sequence_file: str, 
        version: str,
        station_name: Optional[str] = None,
        location: Optional[str] = None,
        purpose: Optional[str] = None
    ) -> UUTReport:
        """
        Create a new UUT (Unit Under Test) report.
        
        Args:
            operator: Name of the test operator
            part_number: Part number of the unit being tested
            revision: Revision of the unit
            serial_number: Serial number of the unit
            operation_type: Type of operation being performed
            sequence_file: Test sequence file name
            version: Version of the test sequence
            station_name: Optional station name (defaults from app config)
            location: Optional location (defaults from app config)
            purpose: Optional purpose (defaults from app config)
            
        Returns:
            A new UUTReport object
        """
        from ..models.report.uut.uut_info import UUTInfo
        
        uut_info = UUTInfo(
            operator=operator
        )
        
        report = UUTReport(
            id=uuid4(),
            type="T",
            pn=part_number,
            sn=serial_number,
            rev=revision,
            process_code=1,  # Default process code
            station_name=station_name or "Unknown",
            location=location or "Unknown", 
            purpose=purpose or "Development",
            start=datetime.now(),
            info=uut_info
        )
        
        return report
    
    def create_uur_report(
        self,
        operator: str,
        repair_type: str,
        operation_type: str,
        serial_number: str,
        part_number: str,
        revision: str,
        station_name: Optional[str] = None,
        location: Optional[str] = None,
        purpose: Optional[str] = None
    ) -> UURReport:
        """
        Create a new UUR (Unit Under Repair) report.
        
        Args:
            operator: Name of the repair operator
            repair_type: Type of repair being performed
            operation_type: Type of operation
            serial_number: Serial number of the unit
            part_number: Part number of the unit
            revision: Revision of the unit
            station_name: Optional station name (defaults from app config)
            location: Optional location (defaults from app config)  
            purpose: Optional purpose (defaults from app config)
            
        Returns:
            A new UURReport object
        """
        from ..models.report.uur.uur_info import UURInfo
        
        uur_info = UURInfo(
            operator=operator
        )
        
        report = UURReport(
            id=uuid4(),
            type="R",
            pn=part_number,
            sn=serial_number,
            rev=revision,
            process_code=1,  # Default process code
            station_name=station_name or "Unknown",
            location=location or "Unknown",
            purpose=purpose or "Development", 
            start=datetime.now(),
            info=uur_info
        )
        
        return report
    
    def submit_report(self, report: Union[UUTReport, UURReport]) -> str:
        """
        Submit a report to WATS.
        
        Args:
            report: The report to submit
            
        Returns:
            Report ID from WATS
        """
        if not isinstance(report, (UUTReport, UURReport)):
            raise WATSException("Report must be a UUTReport or UURReport instance")
            
        # Convert the report to JSON and submit via API
        try:
            # For now, track it locally and generate a placeholder ID
            return self.create_report(report)
            
        except Exception as e:
            raise WATSException(f"Failed to submit report: {str(e)}")
    
    def submit_pending_reports(self) -> List[str]:
        """
        Submit all pending reports.
        
        Returns:
            List of report IDs that were submitted
        """
        try:
            report_ids = []
            for report in self._pending_reports:
                report_id = str(report.id)
                report_ids.append(report_id)
                
            # Clear pending reports after successful submission
            self._pending_reports = []
            return report_ids
            
        except Exception as e:
            raise WATSException(f"Failed to submit pending reports: {str(e)}")
    
    def get_operation_types(self) -> List[Dict[str, Any]]:
        """
        Get all available operation types.
        
        Returns:
            List of operation types
        """
        # This would make a GET request to /api/operation-types
        return [
            {"id": 1, "name": "Final Test", "description": "Final product testing"},
            {"id": 2, "name": "In-Circuit Test", "description": "ICT testing"}
        ]
    
    def get_operation_type(self, id_or_name: Union[str, int]) -> Dict[str, Any]:
        """
        Get a specific operation type by ID or name.
        
        Args:
            id_or_name: Operation type ID or name
            
        Returns:
            Operation type details
            
        Raises:
            WATSNotFoundError: If the operation type is not found
        """
        if not id_or_name:
            raise ValueError("Operation type ID or name must be provided")
            
        # This would make a GET request to /api/operation-types/{id_or_name}
        operation_types = self.get_operation_types()
        
        for op_type in operation_types:
            if (isinstance(id_or_name, int) and op_type["id"] == id_or_name) or \
               (isinstance(id_or_name, str) and op_type["name"] == id_or_name):
                return op_type
                
        raise WATSNotFoundError(f"Operation type '{id_or_name}' not found")
    
    def get_repair_types(self) -> List[Dict[str, Any]]:
        """
        Get all available repair types.
        
        Returns:
            List of repair types
        """
        # This would make a GET request to /api/repair-types
        return [
            {"id": 1, "name": "Component Replacement", "description": "Replace failed components"},
            {"id": 2, "name": "Rework", "description": "Circuit rework"}
        ]
    
    def get_root_fail_codes(self, repair_type: Union[str, int]) -> List[Dict[str, Any]]:
        """
        Get root failure codes for a repair type.
        
        Args:
            repair_type: Repair type ID or name
            
        Returns:
            List of failure codes
        """
        if not repair_type:
            raise ValueError("Repair type must be provided")
            
        # This would make a GET request to /api/repair-types/{repair_type}/fail-codes
        return [
            {"id": 1, "code": "COMP_FAIL", "description": "Component failure"},
            {"id": 2, "code": "SOLDER_FAIL", "description": "Solder joint failure"}
        ]

    def get_yield_monitor_statistics(self, 
                                   start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Get yield monitoring statistics.
        
        Args:
            start_date: Start date for statistics
            end_date: End date for statistics
            
        Returns:
            Yield statistics
        """
        # This would make a GET request to /api/statistics/yield-monitor
        return {
            "total_units": 1000,
            "passed_units": 950,
            "failed_units": 50,
            "yield_percentage": 95.0,
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            }
        }
    
    def load_report(self, report_id: str) -> Union[UUTReport, UURReport]:
        """
        Load a report by ID from WATS.
        
        Args:
            report_id: The ID of the report to load
            
        Returns:
            The loaded UUTReport or UURReport
            
        Raises:
            WATSNotFoundError: If the report is not found
            WATSException: If the load operation fails
        """
        self._validate_id(report_id, "report")
        
        try:
            # Convert string ID to UUID
            uuid_id = UUID(report_id)
            
            # Call the REST API to load the report
            response = report_get_report_as_wsjf.sync(
                id=uuid_id,
                client=cast(Client, self.http_client),
                detail_level=5,  # Full detail
                include_chartdata=True,
                include_attachments=True
            )
            
            if response is None:
                raise WATSNotFoundError(f"Report {report_id} not found")
            
            # TODO: Convert the REST API response to our model format
            # For now, we need to create a conversion method
            # The response is in WSJF format, need to parse it into UUTReport/UURReport
            
            # Placeholder - in real implementation, we'd parse the WSJF response
            raise WATSException(f"Report loading implementation in progress - received response but conversion to UUTReport/UURReport not yet implemented")
            
        except ValueError as e:
            raise WATSException(f"Invalid report ID format: {report_id}")
        except Exception as e:
            if isinstance(e, (WATSNotFoundError, WATSException)):
                raise
            raise WATSException(f"Failed to load report {report_id}: {str(e)}")
    
    def find_report_headers(self,
                           filter: Optional[str] = None,
                           top: Optional[int] = None,
                           skip: Optional[int] = None,
                           orderby: Optional[str] = None) -> List[VirincoWATSWebDashboardModelsODataReportHeader]:
        """
        Find report headers matching the filter criteria.
        
        Args:
            filter: OData filter expression
            top: Maximum number of reports to return  
            skip: Number of reports to skip
            orderby: Field to order results by
            
        Returns:
            List of report header model objects
            
        Raises:
            WATSException: If the query fails
        """
        try:
            # Build query parameters - the actual REST API handles these as query parameters in the URL
            # The report_header_query endpoint handles OData query parameters automatically
            
            # For now, we cannot pass the query parameters because the generated client 
            # doesn't expose them as function parameters
            # We would need to modify the httpx request directly or update the generated client
            
            # Call the REST API to get report headers
            response = report_header_query.sync(client=cast(Client, self.http_client))
            
            if response is None:
                return []
            
            return response
            
        except Exception as e:
            raise WATSException(f"Failed to find report headers: {str(e)}")
    
    def create_report(self, report: Union[UUTReport, UURReport]) -> str:
        """
        Create/submit a new report to WATS.
        
        TODO: !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        This nees investigation.
        do we really keep it here? The create_report() does submit()
        Confusing?
        In line with C# TDM?
             
        
        Args:
            report: The UUTReport or UURReport to submit
            
        Returns:
            The ID of the created report
            
        Raises:
            WATSException: If the creation fails
        """
        try:
            if not isinstance(report, (UUTReport, UURReport)):
                raise ValueError("Report must be a UUTReport or UURReport instance")
            
            # Convert the report to WSJF format for submission
            # TODO: Implement conversion from our models to WSJF format
            # For now, we need the report serialization logic
            
            # Call the REST API to submit the report
            response = report_post_wsjf.sync(client=cast(Client, self.http_client))
            
            if response is None:
                raise WATSException("Failed to submit report - no response received")
            
            # Extract the report ID from the response
            if hasattr(response, 'id'):
                return str(response.id)
            else:
                # TODO: Parse the actual response structure
                raise WATSException("Report creation implementation in progress - received response but ID extraction not yet implemented")
                
        except Exception as e:
            if isinstance(e, WATSException):
                raise
            raise WATSException(f"Failed to create report: {str(e)}")
    
    def delete_report(self, report_id: str) -> bool:
        """
        Delete a report from WATS.
        
        Args:
            report_id: The ID of the report to delete
            
        Returns:
            True if deletion was successful
            
        Raises:
            WATSNotFoundError: If the report is not found
            WATSException: If the deletion fails
        """
        self._validate_id(report_id, "report")
        
        try:
            # Convert string ID to UUID
            uuid_id = UUID(report_id)
            
            # The delete endpoint is only available in the internal API
            from ..rest_api.internal.api.report import report_delete_reports
            from ..rest_api.internal.client import Client as InternalClient
            
            # Call the REST API to delete the report
            # The endpoint accepts a list of UUIDs to delete
            response = report_delete_reports.sync(
                client=cast(InternalClient, self.http_client),
                body=[uuid_id]  # Pass as list of UUIDs
            )
            
            if response is None:
                raise WATSException("Failed to delete report - no response received")
            
            # Check if the deletion was successful
            # TODO: Parse the actual response structure to verify success
            return True
            
        except ValueError as e:
            raise WATSException(f"Invalid report ID format: {report_id}")
        except Exception as e:
            if isinstance(e, (WATSNotFoundError, WATSException)):
                raise
            raise WATSException(f"Failed to delete report {report_id}: {str(e)}")
    
    def export_report(self, 
                     report: Union[UUTReport, UURReport], 
                     format: str = "json", 
                     path: Optional[str] = None) -> str:
        """
        Export a report to a file.
        
        Args:
            report: The report to export
            format: Export format (json, xml, csv)
            path: Path where the report should be saved
            
        Returns:
            Path to the exported file
            
        Raises:
            WATSException: If the export fails
        """
        try:
            if not isinstance(report, (UUTReport, UURReport)):
                raise ValueError("Report must be a UUTReport or UURReport instance")
                
            if format not in ["json", "xml", "csv"]:
                raise ValueError("Format must be one of: json, xml, csv")
                
            if not path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = f"report_{report.id}_{timestamp}.{format}"
                
            # In a real implementation, this would:
            # 1. Serialize the report in the specified format
            # 2. Write it to the specified path
            # 3. Return the actual path
            
            return path
            
        except Exception as e:
            raise WATSException(f"Failed to export report: {str(e)}")
    
    def get_production_statistics(self, 
                                  start_date: Optional[Union[str, datetime]] = None,
                                  end_date: Optional[Union[str, datetime]] = None,
                                  product_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get production statistics for a specified time period.
        
        Args:
            start_date: Start date for the report (ISO format string or datetime)
            end_date: End date for the report (ISO format string or datetime)
            product_id: Optional product ID to filter by
            
        Returns:
            Production statistics data
            
        Raises:
            WATSException: If the report generation fails
        """
        try:
            # Build parameters
            params = self._build_filter_params(
                start_date=self._format_date(start_date),
                end_date=self._format_date(end_date),
                product_id=product_id
            )
            
            # For now, return a placeholder until we have the actual report endpoints
            return {
                "message": "Report functionality will be implemented with actual API endpoints",
                "parameters": params,
                "type": "production_statistics"
            }
            
        except Exception as e:
            raise WATSException(f"Failed to generate production statistics: {str(e)}")
    
    def get_quality_metrics(self,
                           start_date: Optional[Union[str, datetime]] = None,
                           end_date: Optional[Union[str, datetime]] = None) -> Dict[str, Any]:
        """
        Get quality metrics and yield information.
        
        Args:
            start_date: Start date for the metrics
            end_date: End date for the metrics
            
        Returns:
            Quality metrics data
            
        Raises:
            WATSException: If the metrics retrieval fails
        """
        try:
            params = self._build_filter_params(
                start_date=self._format_date(start_date),
                end_date=self._format_date(end_date)
            )
            
            return {
                "message": "Quality metrics functionality will be implemented with actual API endpoints",
                "parameters": params,
                "type": "quality_metrics"
            }
            
        except Exception as e:
            raise WATSException(f"Failed to get quality metrics: {str(e)}")
    
    def generate_custom_report(self, 
                              report_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a custom report based on configuration.
        
        Args:
            report_config: Configuration dictionary for the report
            
        Returns:
            Generated report data
            
        Raises:
            WATSException: If the report generation fails
        """
        try:
            if not isinstance(report_config, dict):
                raise WATSException("Report configuration must be a dictionary")
            
            return {
                "message": "Custom report functionality will be implemented with actual API endpoints",
                "config": report_config,
                "type": "custom_report"
            }
            
        except Exception as e:
            raise WATSException(f"Failed to generate custom report: {str(e)}")
    
    def _format_date(self, date_input: Optional[Union[str, datetime]]) -> Optional[str]:
        """
        Format date input to ISO string format.
        
        Args:
            date_input: Date as string or datetime object
            
        Returns:
            ISO formatted date string or None
        """
        if date_input is None:
            return None
        
        if isinstance(date_input, datetime):
            return date_input.isoformat()
        elif isinstance(date_input, str):
            return date_input
        else:
            raise WATSException(f"Invalid date format: {type(date_input)}")
    
    def get_available_reports(self) -> List[Dict[str, Any]]:
        """
        Get a list of available report types.
        
        Returns:
            List of available report configurations
        """
        return [
            {
                "name": "production_statistics",
                "description": "Production volume and throughput statistics",
                "parameters": ["start_date", "end_date", "product_id"]
            },
            {
                "name": "quality_metrics", 
                "description": "Quality metrics and yield information",
                "parameters": ["start_date", "end_date"]
            },
            {
                "name": "custom_report",
                "description": "Custom configurable reports",
                "parameters": ["report_config"]
            }
        ]