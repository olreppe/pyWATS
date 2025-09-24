"""
TDM Reports Module

Provides report generation and export capabilities including Excel worksheets,
data exports, and custom report generation.
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pathlib import Path
import tempfile

from ..mes.base import MESBase
from .models import StatisticsFilter, AnalyticsResult
from ..rest_api.client import WATSClient
from ..rest_api.models.common import PublicWatsFilter
from ..connection import WATSConnection


class Reports(MESBase):
    """
    Reports management for WATS TDM.
    
    Provides functionality for:
    - Excel worksheet generation
    - Data export capabilities
    - Custom report creation
    - Report formatting and distribution
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Reports module.
        
        Args:
            connection: WATS connection or client instance
        """
        super().__init__(connection)
    
    def create_dynamic_yield_excel_worksheet(
        self,
        filter_data: PublicWatsFilter,
        dimensions: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> str:
        """
        Create a dynamic yield Excel worksheet.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            filter_data: WATS filter for data selection
            dimensions: Optional dimensions string
            output_file: Optional output file path (if not provided, uses temp file)
            
        Returns:
            Path to the generated Excel file
            
        Raises:
            WATSAPIException: On API errors
        """
        # Use the existing internal endpoint from rest_api
        from ..rest_api.endpoints.internal import create_dynamic_yield_excel_worksheet
        
        excel_content = create_dynamic_yield_excel_worksheet(
            filter_data=filter_data,
            dimensions=dimensions,
            client=self._client
        )
        
        # Save to file
        if not output_file:
            output_file = str(Path(tempfile.gettempdir()) / f"yield_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'wb') as f:
            f.write(excel_content)
        
        return str(output_path)
    
    def create_measurement_report(
        self,
        measurement_names: List[str],
        part_number: Optional[str] = None,
        days: Optional[int] = 30,
        output_file: Optional[str] = None,
        format_type: str = "excel"
    ) -> str:
        """
        Create a measurement analysis report.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            measurement_names: List of measurements to include
            part_number: Optional part number filter
            days: Number of days to include (default: 30)
            output_file: Optional output file path
            format_type: Report format ("excel", "csv", "pdf")
            
        Returns:
            Path to the generated report file
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "measurementNames": measurement_names,
            "days": days or 30,
            "formatType": format_type
        }
        
        if part_number:
            data["partNumber"] = part_number
        
        try:
            # Get report data from server
            response = self._rest_post_json("/api/internal/Reports/CreateMeasurementReport", data)
            
            # Generate output file name if not provided
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                extension = self._get_file_extension(format_type)
                output_file = str(Path(tempfile.gettempdir()) / f"measurement_report_{timestamp}.{extension}")
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle different format types
            if format_type.lower() == "excel":
                self._create_excel_report(response.get("data", {}), output_path)
            elif format_type.lower() == "csv":
                self._create_csv_report(response.get("data", {}), output_path)
            elif format_type.lower() == "pdf":
                self._create_pdf_report(response.get("data", {}), output_path)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
            return str(output_path)
        
        except Exception as e:
            raise Exception(f"Failed to create measurement report: {str(e)}")
    
    def create_yield_summary_report(
        self,
        part_numbers: List[str],
        days: Optional[int] = 30,
        output_file: Optional[str] = None,
        include_trends: bool = True
    ) -> str:
        """
        Create a yield summary report for multiple part numbers.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_numbers: List of part numbers to include
            days: Number of days to analyze (default: 30)
            output_file: Optional output file path
            include_trends: Include trend analysis
            
        Returns:
            Path to the generated report file
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "partNumbers": part_numbers,
            "days": days or 30,
            "includeTrends": include_trends
        }
        
        try:
            response = self._rest_post_json("/api/internal/Reports/CreateYieldSummaryReport", data)
            
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = str(Path(tempfile.gettempdir()) / f"yield_summary_{timestamp}.xlsx")
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create Excel report with yield data
            self._create_yield_excel_report(response.get("data", {}), output_path)
            
            return str(output_path)
        
        except Exception as e:
            raise Exception(f"Failed to create yield summary report: {str(e)}")
    
    def create_top_failures_report(
        self,
        count: int = 10,
        days: Optional[int] = 30,
        part_number: Optional[str] = None,
        output_file: Optional[str] = None
    ) -> str:
        """
        Create a top failures analysis report.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            count: Number of top failures to include
            days: Number of days to analyze (default: 30)
            part_number: Optional part number filter
            output_file: Optional output file path
            
        Returns:
            Path to the generated report file
            
        Raises:
            WATSAPIException: On API errors
        """
        # Get top failed data using analytics module
        from .analytics import Analytics
        analytics = Analytics(self._client)
        
        top_failed = analytics.get_top_failed(
            part_number=part_number,
            days=days,
            count=count
        )
        
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = str(Path(tempfile.gettempdir()) / f"top_failures_{timestamp}.xlsx")
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create Excel report with top failures data
        report_data = {
            "topFailed": [item.dict() for item in top_failed],
            "parameters": {
                "count": count,
                "days": days,
                "partNumber": part_number
            }
        }
        
        self._create_top_failures_excel_report(report_data, output_path)
        
        return str(output_path)
    
    def export_raw_data(
        self,
        filter_data: Union[PublicWatsFilter, StatisticsFilter],
        output_file: Optional[str] = None,
        format_type: str = "csv",
        include_measurements: bool = True,
        include_steps: bool = True
    ) -> str:
        """
        Export raw test data based on filter criteria.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            filter_data: Filter criteria for data selection
            output_file: Optional output file path
            format_type: Export format ("csv", "json", "excel")
            include_measurements: Include measurement data
            include_steps: Include step data
            
        Returns:
            Path to the exported data file
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "includeMeasurements": include_measurements,
            "includeSteps": include_steps,
            "formatType": format_type
        }
        
        # Add filter data
        if isinstance(filter_data, PublicWatsFilter):
            data["publicFilter"] = filter_data.dict(exclude_none=True, by_alias=True)
        else:
            data["statisticsFilter"] = filter_data.dict(exclude_none=True, by_alias=True)
        
        try:
            response = self._rest_post_json("/api/internal/Reports/ExportRawData", data)
            
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                extension = self._get_file_extension(format_type)
                output_file = str(Path(tempfile.gettempdir()) / f"raw_data_export_{timestamp}.{extension}")
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Handle different export formats
            if format_type.lower() == "csv":
                self._create_csv_export(response.get("data", {}), output_path)
            elif format_type.lower() == "json":
                self._create_json_export(response.get("data", {}), output_path)
            elif format_type.lower() == "excel":
                self._create_excel_export(response.get("data", {}), output_path)
            else:
                raise ValueError(f"Unsupported format type: {format_type}")
            
            return str(output_path)
        
        except Exception as e:
            raise Exception(f"Failed to export raw data: {str(e)}")
    
    def _get_file_extension(self, format_type: str) -> str:
        """Get file extension for format type."""
        extensions = {
            "excel": "xlsx",
            "csv": "csv",
            "json": "json",
            "pdf": "pdf"
        }
        return extensions.get(format_type.lower(), "txt")
    
    def _create_excel_report(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create Excel report from data."""
        try:
            import pandas as pd
            
            # Create Excel writer
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Write measurements data if available
                if "measurements" in data:
                    measurements_df = pd.DataFrame(data["measurements"])
                    measurements_df.to_excel(writer, sheet_name='Measurements', index=False)
                
                # Write summary data if available
                if "summary" in data:
                    summary_df = pd.DataFrame([data["summary"]])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
        except ImportError:
            # Fallback: create simple text file if pandas not available
            with open(output_path.with_suffix('.txt'), 'w') as f:
                f.write(str(data))
    
    def _create_csv_report(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create CSV report from data."""
        try:
            import pandas as pd
            
            if "measurements" in data:
                measurements_df = pd.DataFrame(data["measurements"])
                measurements_df.to_csv(output_path, index=False)
            else:
                # Create simple CSV from available data
                import csv
                with open(output_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Key', 'Value'])
                    for key, value in data.items():
                        writer.writerow([key, str(value)])
                        
        except ImportError:
            # Fallback without pandas
            import csv
            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Data'])
                writer.writerow([str(data)])
    
    def _create_pdf_report(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create PDF report from data."""
        # For now, create a text file (PDF generation requires additional libraries)
        with open(output_path.with_suffix('.txt'), 'w') as f:
            f.write("WATS TDM Report\\n")
            f.write(f"Generated: {datetime.now()}\\n\\n")
            
            for key, value in data.items():
                f.write(f"{key}: {value}\\n")
    
    def _create_yield_excel_report(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create Excel report specifically for yield data."""
        try:
            import pandas as pd
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Yield summary sheet
                if "yieldData" in data:
                    yield_df = pd.DataFrame(data["yieldData"])
                    yield_df.to_excel(writer, sheet_name='Yield Summary', index=False)
                
                # Trend data sheet if available
                if "trendData" in data:
                    trend_df = pd.DataFrame(data["trendData"])
                    trend_df.to_excel(writer, sheet_name='Trends', index=False)
                    
        except ImportError:
            # Fallback
            with open(output_path.with_suffix('.txt'), 'w') as f:
                f.write(str(data))
    
    def _create_top_failures_excel_report(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create Excel report for top failures data."""
        try:
            import pandas as pd
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Top failures sheet
                if "topFailed" in data:
                    failures_df = pd.DataFrame(data["topFailed"])
                    failures_df.to_excel(writer, sheet_name='Top Failures', index=False)
                
                # Parameters sheet
                if "parameters" in data:
                    params_df = pd.DataFrame([data["parameters"]])
                    params_df.to_excel(writer, sheet_name='Parameters', index=False)
                    
        except ImportError:
            # Fallback
            with open(output_path.with_suffix('.txt'), 'w') as f:
                f.write(str(data))
    
    def _create_csv_export(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create CSV export from raw data."""
        self._create_csv_report(data, output_path)
    
    def _create_json_export(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create JSON export from raw data."""
        import json
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _create_excel_export(self, data: Dict[str, Any], output_path: Path) -> None:
        """Create Excel export from raw data."""
        self._create_excel_report(data, output_path)