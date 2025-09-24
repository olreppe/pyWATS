"""
TDM Statistics Module

Provides statistical analysis and trend monitoring capabilities for test data.
This module includes functionality for retrieving last results, trend analysis,
alert management, and performance counters.
"""

from typing import Optional, List, Union
from datetime import datetime, timedelta

from ..mes.base import MESBase
from .models import (
    TrendData, TrendDataPoint, LastResultData, AlertLevels, 
    StatisticsFilter, AnalyticsResult
)
from ..rest_api.client import WATSClient
from ..connection import WATSConnection


class Statistics(MESBase):
    """
    Statistics management for WATS TDM.
    
    Provides functionality for:
    - Last result retrieval
    - Trend analysis
    - Alert level management
    - Performance counters and startup tracking
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Statistics module.
        
        Args:
            connection: WATS connection or client instance
        """
        super().__init__(connection)
    
    def get_last_result(
        self, 
        part_number: str, 
        operation_key: str
    ) -> Optional[LastResultData]:
        """
        Get last test result for product operation.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Product part number
            operation_key: Operation identifier
            
        Returns:
            LastResultData or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "partNumber": part_number,
            "operationKey": operation_key
        }
        
        try:
            response = self._rest_get_json("/api/internal/Statistics/GetLastResult")
            
            if response.get("result"):
                return LastResultData(
                    part_number=part_number,
                    operation_key=operation_key,
                    result=response.get("result"),
                    timestamp=response.get("timestamp"),
                    value=response.get("value"),
                    unit=response.get("unit"),
                    status=response.get("status")
                )
            
            return None
        except Exception:
            return None
    
    def get_trend(
        self, 
        part_number: str, 
        operation_key: str,
        days: Optional[int] = 30
    ) -> TrendData:
        """
        Get trend data for product operation.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Product part number
            operation_key: Operation identifier
            days: Number of days to include (default: 30)
            
        Returns:
            TrendData with data points
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "partNumber": part_number,
            "operationKey": operation_key
        }
        
        if days is not None:
            params["days"] = days
        
        response = self._rest_get_json("/api/internal/Statistics/GetTrend")
        trend_points_data = response.get("trendPoints", [])
        
        # Convert raw data to TrendDataPoint objects
        data_points = []
        for point in trend_points_data:
            data_points.append(TrendDataPoint(
                timestamp=point.get("timestamp"),
                value=point.get("value"),
                count=point.get("count"),
                status=point.get("status")
            ))
        
        return TrendData(
            part_number=part_number,
            operation_key=operation_key,
            data_points=data_points,
            total_count=response.get("totalCount", 0),
            start_date=response.get("startDate"),
            end_date=response.get("endDate")
        )
    
    def reset_startup_counters(self) -> bool:
        """
        Reset startup counters.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        try:
            response = self._rest_post_json("/api/internal/Statistics/ResetStartupCounters")
            return response.get("success", False)
        except Exception:
            return False
    
    def set_alert_levels(
        self,
        part_number: str,
        warning_level: float,
        critical_level: float,
        total_count: int,
        last_count: int
    ) -> bool:
        """
        Set alert levels for product.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Product part number
            warning_level: Warning threshold level
            critical_level: Critical threshold level
            total_count: Total count threshold
            last_count: Last count threshold
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        alert_levels = AlertLevels(
            part_number=part_number,
            warning_level=warning_level,
            critical_level=critical_level,
            total_count=total_count,
            last_count=last_count
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Statistics/SetAlertLevels",
                alert_levels
            )
            return response.get("success", False)
        except Exception:
            return False
    
    def get_alert_levels(self, part_number: str) -> Optional[AlertLevels]:
        """
        Get alert levels for product.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Product part number
            
        Returns:
            AlertLevels or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {"partNumber": part_number}
        
        try:
            response = self._rest_get_json("/api/internal/Statistics/GetAlertLevels")
            
            if response.get("found", False):
                return AlertLevels.parse_obj(response)
            
            return None
        except Exception:
            return None
    
    def get_statistics_summary(
        self, 
        filter_data: Optional[StatisticsFilter] = None
    ) -> AnalyticsResult:
        """
        Get statistics summary for filtered data.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            filter_data: Optional filter criteria
            
        Returns:
            AnalyticsResult with summary statistics
            
        Raises:
            WATSAPIException: On API errors
        """
        try:
            if filter_data:
                response = self._rest_post_json(
                    "/api/internal/Statistics/GetSummary",
                    filter_data
                )
            else:
                response = self._rest_get_json("/api/internal/Statistics/GetSummary")
            
            return AnalyticsResult(
                success=True,
                data=response,
                message="Statistics summary retrieved successfully"
            )
        except Exception as e:
            return AnalyticsResult(
                success=False,
                message=f"Failed to get statistics summary: {str(e)}"
            )
    
    def get_performance_metrics(
        self,
        part_number: Optional[str] = None,
        days: Optional[int] = 7
    ) -> AnalyticsResult:
        """
        Get performance metrics for specified criteria.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Optional part number filter
            days: Number of days to analyze (default: 7)
            
        Returns:
            AnalyticsResult with performance metrics
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {}
        if part_number:
            params["partNumber"] = part_number
        if days is not None:
            params["days"] = days
        
        try:
            response = self._rest_get_json("/api/internal/Statistics/GetPerformanceMetrics")
            
            return AnalyticsResult(
                success=True,
                data=response,
                message="Performance metrics retrieved successfully"
            )
        except Exception as e:
            return AnalyticsResult(
                success=False,
                message=f"Failed to get performance metrics: {str(e)}"
            )
    
    def get_trend_analysis(
        self,
        part_number: str,
        measurement_name: Optional[str] = None,
        days: Optional[int] = 30
    ) -> AnalyticsResult:
        """
        Get comprehensive trend analysis.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Product part number
            measurement_name: Optional specific measurement to analyze
            days: Number of days to analyze (default: 30)
            
        Returns:
            AnalyticsResult with trend analysis data
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "partNumber": part_number,
            "days": days or 30
        }
        
        if measurement_name:
            params["measurementName"] = measurement_name
        
        try:
            response = self._rest_get_json("/api/internal/Statistics/GetTrendAnalysis")
            
            return AnalyticsResult(
                success=True,
                data=response,
                message="Trend analysis completed successfully"
            )
        except Exception as e:
            return AnalyticsResult(
                success=False,
                message=f"Failed to get trend analysis: {str(e)}"
            )
    
    def dispose(self) -> None:
        """
        Dispose of resources.
        
        Note: In Python, this is handled by garbage collection,
        but we provide this method for API compatibility.
        """
        # Close any open resources if needed
        pass