"""
TDM Analytics Module

Provides advanced analytical capabilities including aggregated measurements,
step analysis, yield calculations, and data correlation analysis.
"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime

from ..mes.base import MESBase
from .models import (
    AggregatedMeasurement, MeasurementData, StepStatus, 
    TopFailedStep, YieldData, StatisticsFilter, AnalyticsResult
)
from ..rest_api.client import WATSClient
from ..rest_api.models.common import PublicWatsFilter
from ..connection import WATSConnection


class Analytics(MESBase):
    """
    Analytics management for WATS TDM.
    
    Provides functionality for:
    - Aggregated measurement analysis
    - Step status analysis
    - Top failed step identification
    - Yield calculations
    - Measurement correlations
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Analytics module.
        
        Args:
            connection: WATS connection or client instance
        """
        super().__init__(connection)
    
    def get_aggregated_measurements(
        self,
        product_group_id: str,
        level_id: str,
        days: int,
        step_filters: Optional[str] = None,
        sequence_filters: Optional[str] = None,
        measurement_name: Optional[str] = None,
        filter_data: Optional[PublicWatsFilter] = None
    ) -> List[AggregatedMeasurement]:
        """
        Get aggregated measurement data.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            product_group_id: Product group ID
            level_id: Level ID
            days: Number of days to analyze
            step_filters: Optional XML step filter
            sequence_filters: Optional XML sequence filter
            measurement_name: Optional specific measurement name
            filter_data: Optional WATS filter for POST request
            
        Returns:
            List of AggregatedMeasurement objects
            
        Raises:
            WATSAPIException: On API errors
        """
        # Use the existing internal endpoint from rest_api
        from ..rest_api.endpoints.internal import get_aggregated_measurements_internal
        
        response = get_aggregated_measurements_internal(
            product_group_id=product_group_id,
            level_id=level_id,
            days=days,
            step_filters=step_filters or "",
            sequence_filters=sequence_filters or "",
            measurement_name=measurement_name,
            filter_data=filter_data,
            client=self._client
        )
        
        measurements_data = response.get("measurements", [])
        return [AggregatedMeasurement.parse_obj(item) for item in measurements_data]
    
    def get_measurement_list(
        self,
        product_group_id: Optional[str] = None,
        level_id: Optional[str] = None,
        days: Optional[int] = None,
        step_filters: Optional[str] = None,
        sequence_filters: Optional[str] = None,
        filter_data: Optional[PublicWatsFilter] = None
    ) -> List[MeasurementData]:
        """
        Get measurements for a step.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            product_group_id: Product group ID
            level_id: Level ID
            days: Number of days to analyze
            step_filters: Optional XML step filter
            sequence_filters: Optional XML sequence filter
            filter_data: Optional WATS filter for POST request
            
        Returns:
            List of MeasurementData objects
            
        Raises:
            WATSAPIException: On API errors
        """
        # Use the existing internal endpoint from rest_api
        from ..rest_api.endpoints.internal import get_measurement_list
        
        response = get_measurement_list(
            product_group_id=product_group_id,
            level_id=level_id,
            days=days,
            step_filters=step_filters,
            sequence_filters=sequence_filters,
            filter_data=filter_data,
            client=self._client
        )
        
        measurements_data = response.get("measurements", [])
        return [MeasurementData.parse_obj(item) for item in measurements_data]
    
    def get_step_status_list(
        self,
        product_group_id: Optional[str] = None,
        level_id: Optional[str] = None,
        days: Optional[int] = None,
        step_filters: Optional[str] = None,
        sequence_filters: Optional[str] = None,
        filter_data: Optional[PublicWatsFilter] = None
    ) -> List[StepStatus]:
        """
        Get statuses for a step.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            product_group_id: Product group ID
            level_id: Level ID
            days: Number of days to analyze
            step_filters: Optional XML step filter
            sequence_filters: Optional XML sequence filter
            filter_data: Optional WATS filter for POST request
            
        Returns:
            List of StepStatus objects
            
        Raises:
            WATSAPIException: On API errors
        """
        # Use the existing internal endpoint from rest_api
        from ..rest_api.endpoints.internal import get_step_status_list
        
        response = get_step_status_list(
            product_group_id=product_group_id,
            level_id=level_id,
            days=days,
            step_filters=step_filters,
            sequence_filters=sequence_filters,
            filter_data=filter_data,
            client=self._client
        )
        
        steps_data = response.get("steps", [])
        return [StepStatus.parse_obj(item) for item in steps_data]
    
    def get_top_failed(
        self,
        part_number: Optional[str] = None,
        process_code: Optional[str] = None,
        product_group_id: Optional[str] = None,
        level_id: Optional[str] = None,
        days: Optional[int] = None,
        count: Optional[int] = None,
        filter_data: Optional[PublicWatsFilter] = None
    ) -> List[TopFailedStep]:
        """
        Get top failed steps.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Part number of reports
            process_code: Process code of reports
            product_group_id: Product group of reports
            level_id: Level of reports
            days: Number of days ago reports were submitted
            count: Number of items to return
            filter_data: Optional WATS filter for POST request
            
        Returns:
            List of TopFailedStep objects
            
        Raises:
            WATSAPIException: On API errors
        """
        # Use the existing internal endpoint from rest_api
        from ..rest_api.endpoints.internal import get_top_failed_internal
        
        response = get_top_failed_internal(
            part_number=part_number,
            process_code=process_code,
            product_group_id=product_group_id,
            level_id=level_id,
            days=days,
            count=count,
            filter_data=filter_data,
            client=self._client
        )
        
        failed_steps_data = response.get("topFailed", [])
        return [TopFailedStep.parse_obj(item) for item in failed_steps_data]
    
    def calculate_yield(
        self,
        part_number: Optional[str] = None,
        process_code: Optional[str] = None,
        days: Optional[int] = 30,
        filter_data: Optional[StatisticsFilter] = None
    ) -> YieldData:
        """
        Calculate yield for specified criteria.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Optional part number filter
            process_code: Optional process code filter
            days: Number of days to analyze (default: 30)
            filter_data: Optional additional filter criteria
            
        Returns:
            YieldData with yield calculations
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {}
        if part_number:
            params["partNumber"] = part_number
        if process_code:
            params["processCode"] = process_code
        if days is not None:
            params["days"] = days
        
        try:
            if filter_data:
                response = self._rest_post_json(
                    "/api/internal/Analytics/CalculateYield",
                    filter_data
                )
            else:
                response = self._rest_get_json("/api/internal/Analytics/CalculateYield")
            
            return YieldData.parse_obj(response)
        except Exception as e:
            # Return empty yield data on error
            return YieldData(
                part_number=part_number,
                process_code=process_code,
                total_units=0,
                passed_units=0,
                failed_units=0,
                yield_percentage=0.0,
                date_range=f"Last {days} days" if days else None
            )
    
    def get_measurement_correlation(
        self,
        measurement_names: List[str],
        part_number: Optional[str] = None,
        days: Optional[int] = 30
    ) -> AnalyticsResult:
        """
        Get correlation analysis between measurements.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            measurement_names: List of measurement names to correlate
            part_number: Optional part number filter
            days: Number of days to analyze (default: 30)
            
        Returns:
            AnalyticsResult with correlation data
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "measurementNames": measurement_names,
            "days": days or 30
        }
        
        if part_number:
            data["partNumber"] = part_number
        
        try:
            response = self._rest_post_json(
                "/api/internal/Analytics/GetMeasurementCorrelation",
                data
            )
            
            return AnalyticsResult(
                success=True,
                data=response,
                message="Correlation analysis completed successfully"
            )
        except Exception as e:
            return AnalyticsResult(
                success=False,
                message=f"Failed to get measurement correlation: {str(e)}"
            )
    
    def get_process_capability(
        self,
        measurement_name: str,
        part_number: str,
        lower_spec_limit: Optional[float] = None,
        upper_spec_limit: Optional[float] = None,
        days: Optional[int] = 30
    ) -> AnalyticsResult:
        """
        Calculate process capability indices (Cp, Cpk).
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            measurement_name: Measurement to analyze
            part_number: Part number filter
            lower_spec_limit: Optional lower specification limit
            upper_spec_limit: Optional upper specification limit
            days: Number of days to analyze (default: 30)
            
        Returns:
            AnalyticsResult with process capability data
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "measurementName": measurement_name,
            "partNumber": part_number,
            "days": days or 30
        }
        
        if lower_spec_limit is not None:
            data["lowerSpecLimit"] = lower_spec_limit
        if upper_spec_limit is not None:
            data["upperSpecLimit"] = upper_spec_limit
        
        try:
            response = self._rest_post_json(
                "/api/internal/Analytics/GetProcessCapability",
                data
            )
            
            return AnalyticsResult(
                success=True,
                data=response,
                message="Process capability analysis completed successfully"
            )
        except Exception as e:
            return AnalyticsResult(
                success=False,
                message=f"Failed to get process capability: {str(e)}"
            )
    
    def get_control_chart_data(
        self,
        measurement_name: str,
        part_number: str,
        chart_type: str = "xbar_r",
        days: Optional[int] = 30
    ) -> AnalyticsResult:
        """
        Get control chart data for statistical process control.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            measurement_name: Measurement to analyze
            part_number: Part number filter
            chart_type: Type of control chart ("xbar_r", "xbar_s", "individual")
            days: Number of days to analyze (default: 30)
            
        Returns:
            AnalyticsResult with control chart data
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "measurementName": measurement_name,
            "partNumber": part_number,
            "chartType": chart_type,
            "days": days or 30
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Analytics/GetControlChartData",
                data
            )
            
            return AnalyticsResult(
                success=True,
                data=response,
                message="Control chart data retrieved successfully"
            )
        except Exception as e:
            return AnalyticsResult(
                success=False,
                message=f"Failed to get control chart data: {str(e)}"
            )