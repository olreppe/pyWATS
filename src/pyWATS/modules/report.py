"""
Report module for WATS API.

This module provides functionality for generating reports, analytics,
loading and managing test reports from the WATS system.
"""

from typing import List, Optional, Dict, Any, Union, TYPE_CHECKING, cast
from datetime import datetime
from uuid import UUID, uuid4
import json  # Add this import at the top
import warnings

from .base import BaseModule
from ..exceptions import WATSException, WATSNotFoundError
from ..models.report import UUTReport, UURReport, Report

if TYPE_CHECKING:
    from ..rest_api._http_client import WatsHttpClient
    from ..rest_api.public.client import AuthenticatedClient, Client

# Import REST API endpoints
from ..rest_api.public.api.report import (
    report_header_query,
    report_get_report_as_wsjf,
    report_post_wsjf
)
from ..rest_api.internal.api.report import (
    report_delete_reports
)
from ..rest_api.public.models.virinco_wats_web_dashboard_models_o_data_report_header import (
    VirincoWATSWebDashboardModelsODataReportHeader
)


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

    http_client: Union['WatsHttpClient', 'AuthenticatedClient', 'Client']  # Add explicit type hint
    def __init__(self, client: Union['WatsHttpClient', 'AuthenticatedClient', 'Client']):
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
            process_code=int(operation_type) or 10,
            station_name=station_name or "Unknown",
            location=location or "Unknown", 
            purpose=purpose or "Development",
            start=datetime.now().astimezone(),  # Use local timezone-aware datetime
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
            process_code=1,
            station_name=station_name or "Unknown",
            location=location or "Unknown",
            purpose=purpose or "Development", 
            start=datetime.now().astimezone(),  # Use local timezone-aware datetime
            info=uur_info
        )
        
        return report
    
    def submit_report(self, report: Union[UUTReport, UURReport]) -> str:
        """
        Submit (persist) a report to WATS.

        This transmits an already constructed report model (created with
        create_uut_report / create_uur_report) to the server.

        Args:
            report: Report model instance

        Returns:
            Server-assigned report UUID (string)
        """
        if not isinstance(report, (UUTReport, UURReport)):
            raise WATSException("Report must be a UUTReport or UURReport instance")
        try:
            return self._post_wsjf_report(report)
        except Exception as e:
            raise WATSException(f"Failed to submit report: {e}")

    def _post_wsjf_report(self, report: Union[UUTReport, UURReport]) -> str:
        """
        Internal helper performing the POST (create/update) against the WSJF endpoint.

        Args:
            report: Report model instance.

        Returns:
            Report UUID string.

        Raises:
            WATSException on failure.
        """
        try:
            if not isinstance(report, (UUTReport, UURReport)):
                raise ValueError("Report must be a UUTReport or UURReport instance")

            wsjf_data = report.model_dump(by_alias=True, mode='json', exclude_none=True)

            from ..rest_api.public.api.report import report_post_wsjf as rp
            kwargs = rp._get_kwargs(body=wsjf_data)
            raw_response = self.http_client.get_httpx_client().request(**kwargs)

            if raw_response.status_code != 200:
                raise WATSException(
                    f"Failed to submit report - HTTP {raw_response.status_code}: {raw_response.text}"
                )

            from ..rest_api.public.models.virinco_wats_models_store_insert_report_result import (
                VirincoWATSModelsStoreInsertReportResult
            )
            response_json = raw_response.json()

            if isinstance(response_json, list) and response_json:
                result_dict = response_json[0]
            elif isinstance(response_json, dict):
                result_dict = response_json
            else:
                raise WATSException(f"Unexpected response format: {type(response_json)}")

            parsed_result = VirincoWATSModelsStoreInsertReportResult.from_dict(result_dict)

            if getattr(parsed_result, 'id', None):
                return str(parsed_result.id)
            if getattr(parsed_result, 'uuid', None):
                return str(parsed_result.uuid)

            return str(
                result_dict.get('ID')
                or result_dict.get('uuid')
                or result_dict.get('Report_ID')
            )

        except WATSException:
            raise
        except Exception as e:
            raise WATSException(f"Failed to submit (WSJF) report: {e}")
        
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
            uuid_id = UUID(report_id)
            
            # Use REST API endpoint - no direct Client usage
            response = report_get_report_as_wsjf.sync(
                id=uuid_id,
                client=self.http_client,  # WatsHttpClient, not raw Client
                detail_level=5,
                include_chartdata=True,
                include_attachments=True
            )
            
            if response is None:
                raise WATSNotFoundError(f"Report {report_id} not found")
            
            # TODO: Convert WSJF response to UUTReport/UURReport
            # Need to implement parser: wsjf_to_report(response)
            raise WATSException(
                "Report loading implementation in progress - "
                "received response but conversion to UUTReport/UURReport not yet implemented"
            )
            
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
            
        Note:
            OData query parameters (filter, top, skip, orderby) are not currently
            exposed by the generated client. This needs to be fixed in the OpenAPI spec
            or by manually adding query parameters to the generated endpoint.
        """
        try:
            # TODO: Once the generated client supports OData parameters, pass them here
            # response = report_header_query.sync(
            #     client=self.http_client,
            #     filter=filter,
            #     top=top,
            #     skip=skip,
            #     orderby=orderby
            # )
            
            # Use REST API endpoint - no direct Client usage
            response = report_header_query.sync(client=self.http_client)
            
            if response is None:
                return []
            
            return response
            
        except Exception as e:
            raise WATSException(f"Failed to find report headers: {str(e)}")
        
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
            uuid_id = UUID(report_id)
            
            # Cast to satisfy type checker - WatsHttpClient inherits from AuthenticatedClient
            from ..rest_api.internal.client import AuthenticatedClient as InternalAuthenticatedClient
            from typing import cast

            # Use REST API endpoint from internal API
            response = report_delete_reports.sync(
                client=cast(InternalAuthenticatedClient, self.http_client),
                body=[uuid_id]
            )
            
            if response is None:
                raise WATSException("Failed to delete report - no response received")
            
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
            
        Note:
            This is a local operation and doesn't use REST API endpoints.
            It serializes the report model to the specified format.
        """
        try:
            if not isinstance(report, (UUTReport, UURReport)):
                raise ValueError("Report must be a UUTReport or UURReport instance")
                
            if format not in ["json", "xml", "csv"]:
                raise ValueError("Format must be one of: json, xml, csv")
                
            if not path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = f"report_{report.id}_{timestamp}.{format}"
                
            # TODO: Implement actual file writing
            # if format == "json":
            #     with open(path, 'w') as f:
            #         f.write(report.model_dump_json(by_alias=True, indent=2))
            # elif format == "xml":
            #     # Convert to XML format
            #     pass
            # elif format == "csv":
            #     # Convert to CSV format
            #     pass
            
            return path
            
        except Exception as e:
            raise WATSException(f"Failed to export report: {str(e)}")
    # Move to?
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
            
        Note:
            This is a placeholder until the actual REST API endpoint is available.
            Will use rest_api.public.statistics.* when implemented.
        """
        try:
            params = self._build_filter_params(
                start_date=self._format_date(start_date),
                end_date=self._format_date(end_date),
                product_id=product_id
            )
            
            # TODO: Use actual REST API endpoint when available
            # from ..rest_api.public.api.statistics import get_production_statistics
            # response = get_production_statistics.sync(
            #     client=self.http_client,
            #     **params
            # )
            
            return {
                "message": "Report functionality will be implemented with actual API endpoints",
                "parameters": params,
                "type": "production_statistics"
            }
            
        except Exception as e:
            raise WATSException(f"Failed to generate production statistics: {str(e)}")
    # Move to ?
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
            
        Note:
            This is a placeholder until the actual REST API endpoint is available.
            Will use rest_api.public.statistics.* when implemented.
        """
        try:
            params = self._build_filter_params(
                start_date=self._format_date(start_date),
                end_date=self._format_date(end_date)
            )
            
            # TODO: Use actual REST API endpoint when available
            # from ..rest_api.public.api.statistics import get_quality_metrics
            # response = get_quality_metrics.sync(client=self.http_client, **params)
            
            return {
                "message": "Quality metrics functionality will be implemented with actual API endpoints",
                "parameters": params,
                "type": "quality_metrics"
            }
            
        except Exception as e:
            raise WATSException(f"Failed to get quality metrics: {str(e)}")
    
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
    