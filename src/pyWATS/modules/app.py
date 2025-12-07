"""App Module for pyWATS

Provides operations for statistics, KPIs, and dashboard data.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models import (
    WATSFilter, YieldData, ProcessInfo, LevelInfo, ProductGroup, ReportHeader
)
from ..rest_api import AppApi


"""

API INFO / SWAGGER DOC:
post /api/App/AggregatedMeasurements
Get aggregated numeric measurements by measurement path. A maximum of 10000 measurements are returned. Requesting the endpoint with a empty filter will return measurements from the last seven days most failed steps

post /api/App/DynamicRepair
PREVIEW - Calculate repair statistics by custom dimensions.

post /api/App/DynamicYield
PREVIEW - Calculate yield by custom dimensions.

get /api/App/HighVolume
High Volume list filtered by productGroup and level

post /api/App/HighVolume
Yield sorted by volume.

post /api/App/HighVolumeByProductGroup
Yield by product group sorted by volume.

get /api/App/Levels
Retrieves all ClientGroups

post /api/App/Measurements
PREVIEW - Get numeric measurements by measurement path. A maximum of 10000 measurments are returned. Requesting the endpoint with a empty filter will return measurements from the last seven days most failed steps

post /api/App/OeeAnalysis
Overall Equipment Effectiveness - analysis

Supported filters: productGroup, level, partNumber, revision, stationName, testOperation, status, swFilename, swVersion, socket, dateFrom, dateTo

get /api/App/Processes
Get processes.

get /api/App/ProductGroups
Retrieves all ProductGroups

get /api/App/RelatedRepairHistory
Get list of repaired failures related to the part number and revision.

post /api/App/SerialNumberHistory
Serial Number History.

Supported filters: productGroup, level, serialNumber, partNumber, batchNumber, miscValue

post /api/App/TestStepAnalysis
PREVIEW - Get step and measurement statistics.

get /api/App/TopFailed
Get the top failed steps for the reports with the specified parameters.

post /api/App/TopFailed
Get the top failed steps for the reports with the specified parameters.

post /api/App/UurReport
Returns UUR report header info like Repair Reports in Reporting.

Uses watsfilter with supported filters: productGroup, level, serialNumber, partNumber, revision, batchNumber, stationName, testOperation, status, miscValue, dateFrom, dateTo, topCount

By default the 1000 newest reports that matches the filter are returned, use the topCount filter to change this.

This API is not suitable for workflow or production management, instead use the Production module.

get /api/App/UutReport
Returns UUT report header info like Test Reports in Reporting. The 1000 newest reports that matches the filter are returned.

This API is not suitable for workflow or production management, instead use the Production module.

post /api/App/UutReport
Returns UUT report header info like Test Reports in Reporting.

Uses watsfilter with Supported filters: productGroup, level, serialNumber, partNumber, revision, batchNumber, stationName, testOperation, status, miscValue, dateFrom, dateTo, topCount

By default the 1000 newest reports that matches the filter are returned, use the topCount filter to change this.

This API is not suitable for workflow or production management, instead use the Production module.

get /api/App/Version
Get server/api version

get /api/App/VolumeYield
Volume/Yield list filtered by productGroup and level

post /api/App/VolumeYield
Volume/Yield list filtered by productGroup and level

get /api/App/WorstYield
Worst Yield list filtered by productGroup and level

post /api/App/WorstYield
Yield sorted by lowest yield.

post /api/App/WorstYieldByProductGroup
Yield by product group sorted by lowest yield.




"""



class AppModule:
    """
    App/Statistics module.
    
    Provides operations for:
    - Dynamic yield and repair statistics
    - High volume and volume/yield analysis
    - Top failed steps analysis
    - Test step and measurement analysis
    - OEE (Overall Equipment Effectiveness)
    - Serial number history
    - System configuration (processes, levels, product groups)
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Get dynamic yield statistics
        filter = WATSFilter(product_group="Electronics", period_count=30)
        yield_data = api.app.get_dynamic_yield(filter)
        
        # Get top failed steps
        top_failed = api.app.get_top_failed(product_group_id=1, top_count=10)
        
        # Get all processes
        processes = api.app.get_processes()
    """
    
    def __init__(self, api: AppApi):
        """
        Initialize AppModule with REST API client.
        
        Args:
            api: AppApi instance for making HTTP requests
        """
        self._api = api
    
    # -------------------------------------------------------------------------
    # System Info
    # -------------------------------------------------------------------------
    
    def get_version(self) -> Dict[str, Any]:
        """
        Get WATS API version information.
        
        Returns:
            Version information dictionary
        """
        return self._api.get_version() or {}
    
    def get_processes(self) -> List[ProcessInfo]:
        """
        Get all defined test processes/operations.
        
        Returns:
            List of ProcessInfo objects
        """
        return self._api.get_processes()
    
    def get_levels(self) -> List[LevelInfo]:
        """
        Get all production levels.
        
        Returns:
            List of LevelInfo objects
        """
        return self._api.get_levels()
    
    def get_product_groups(self) -> List[ProductGroup]:
        """
        Get all product groups.
            
        Returns:
            List of ProductGroup objects
        """
        return self._api.get_product_groups()
    
    # -------------------------------------------------------------------------
    # Yield Statistics
    # -------------------------------------------------------------------------
    
    def get_dynamic_yield(self, filter: WATSFilter) -> List[YieldData]:
        """
        Get dynamic yield statistics by custom dimensions (PREVIEW).
        
        Supported dimensions: partNumber, productName, stationName, location,
        purpose, revision, testOperation, processCode, swFilename, swVersion,
        productGroup, level, period, batchNumber, operator, fixtureId, etc.
        
        Args:
            filter: WATSFilter with dimensions and filters
            
        Returns:
            List of YieldData objects
        """
        return self._api.get_dynamic_yield(filter)
    
    def get_dynamic_repair(self, filter: WATSFilter) -> List[Dict[str, Any]]:
        """
        Get dynamic repair statistics by custom dimensions (PREVIEW).
        
        Args:
            filter: WATSFilter with dimensions and filters
            
        Returns:
            List of repair statistics data
        """
        return self._api.get_dynamic_repair(filter)
    
    def get_volume_yield(
        self,
        filter: Optional[WATSFilter] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> List[YieldData]:
        """
        Get volume/yield statistics.
        
        Args:
            filter: Optional WATSFilter for POST request
            product_group: Optional product group filter (for GET)
            level: Optional level filter (for GET)
            
        Returns:
            List of YieldData objects
        """
        if filter:
            return self._api.get_volume_yield(filter_data=filter)
        else:
            return self._api.get_volume_yield(product_group=product_group, level=level)
    
    def get_worst_yield(
        self,
        filter: Optional[WATSFilter] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> List[YieldData]:
        """
        Get worst yield statistics.
        
        Args:
            filter: Optional WATSFilter for POST request
            product_group: Optional product group filter (for GET)
            level: Optional level filter (for GET)
            
        Returns:
            List of YieldData objects
        """
        if filter:
            return self._api.get_worst_yield(filter_data=filter)
        else:
            return self._api.get_worst_yield(product_group=product_group, level=level)
    
    def get_worst_yield_by_product_group(self, filter: WATSFilter) -> List[YieldData]:
        """
        Get worst yield by product group.
        
        Args:
            filter: WATSFilter with parameters
            
        Returns:
            List of YieldData objects by product group
        """
        return self._api.get_worst_yield_by_product_group(filter)
    
    # -------------------------------------------------------------------------
    # High Volume Analysis
    # -------------------------------------------------------------------------
    
    def get_high_volume(
        self,
        filter: Optional[WATSFilter] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> List[YieldData]:
        """
        Get high volume product list.
        
        Args:
            filter: Optional WATSFilter for POST request
            product_group: Optional product group filter (for GET)
            level: Optional level filter (for GET)
            
        Returns:
            List of YieldData objects
        """
        if filter:
            return self._api.get_high_volume(filter_data=filter)
        else:
            return self._api.get_high_volume(product_group=product_group, level=level)
    
    def get_high_volume_by_product_group(self, filter: WATSFilter) -> List[YieldData]:
        """
        Get yield by product group sorted by volume.
        
        Args:
            filter: WATSFilter with parameters
        
        Returns:
            List of YieldData objects by product group
        """
        return self._api.get_high_volume_by_product_group(filter)
    
    # -------------------------------------------------------------------------
    # Failure Analysis
    # -------------------------------------------------------------------------
    
    def get_top_failed(
        self,
        filter: Optional[WATSFilter] = None,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Get top failed test steps.
        
        Args:
            filter: Optional WATSFilter for POST request
            **kwargs: Additional query parameters for GET
            
        Returns:
            List of top failed step data
        """
        if filter:
            return self._api.get_top_failed(filter_data=filter)
        else:
            return self._api.get_top_failed(**kwargs)
    
    def get_test_step_analysis(self, filter: WATSFilter) -> Dict[str, Any]:
        """
        Get test step analysis data (PREVIEW).
        
        Args:
            filter: WATSFilter with analysis parameters
            
        Returns:
            Test step analysis data
        """
        return self._api.get_test_step_analysis(filter) or {}
    
    # -------------------------------------------------------------------------
    # Repair History
    # -------------------------------------------------------------------------
    
    def get_related_repair_history(
        self,
        part_number: str,
        revision: str
    ) -> List[Dict[str, Any]]:
        """
        Get list of repaired failures related to the part number and revision.
        
        Args:
            part_number: Product part number
            revision: Product revision
            
        Returns:
            List of repair history records
        """
        return self._api.get_related_repair_history(part_number, revision)
    
    # -------------------------------------------------------------------------
    # Measurement Analysis
    # -------------------------------------------------------------------------
    
    def get_aggregated_measurements(self, filter: WATSFilter) -> List[Dict[str, Any]]:
        """
        Get aggregated measurement statistics.
        
        Args:
            filter: WATSFilter with measurement filters
            
        Returns:
            List of aggregated measurement data
        """
        return self._api.get_aggregated_measurements(filter)
    
    def get_measurements(self, filter: WATSFilter) -> List[Dict[str, Any]]:
        """
        Get measurement data (PREVIEW).
        
        Args:
            filter: WATSFilter with measurement filters
            
        Returns:
            List of measurement data
        """
        return self._api.get_measurements(filter)
    
    # -------------------------------------------------------------------------
    # OEE Analysis
    # -------------------------------------------------------------------------
    
    def get_oee_analysis(self, filter: WATSFilter) -> Dict[str, Any]:
        """
        Get Overall Equipment Effectiveness analysis.
        
        Supported filters: productGroup, level, partNumber, revision,
        stationName, testOperation, status, swFilename, swVersion,
        socket, dateFrom, dateTo
        
        Args:
            filter: WATSFilter with OEE parameters
            
        Returns:
            OEE analysis data
        """
        return self._api.get_oee_analysis(filter) or {}
    
    # -------------------------------------------------------------------------
    # Serial Number History
    # -------------------------------------------------------------------------
    
    def get_serial_number_history(self, filter: WATSFilter) -> List[ReportHeader]:
        """
        Get test history for a serial number.
        
        Supported filters: productGroup, level, serialNumber, partNumber,
        batchNumber, miscValue
        
        Args:
            filter: WATSFilter with serial number and other filters
            
        Returns:
            List of ReportHeader objects
        """
        return self._api.get_serial_number_history(filter)
    
    # -------------------------------------------------------------------------
    # UUT/UUR Reports
    # -------------------------------------------------------------------------
    
    def get_uut_reports(
        self,
        filter: Optional[WATSFilter] = None,
        **kwargs
    ) -> List[ReportHeader]:
        """
        Get UUT report headers (like Test Reports in Reporting).
        
        By default the 1000 newest reports that match the filter are returned.
        Use topCount filter to change this.
        
        Note: This API is not suitable for workflow or production management,
        use the Production module instead.
        
        Args:
            filter: Optional WATSFilter for POST request
            **kwargs: Query parameters for GET request
            
        Returns:
            List of ReportHeader objects
        """
        if filter:
            return self._api.get_uut_reports(filter_data=filter)
        else:
            return self._api.get_uut_reports(**kwargs)
    
    def get_uur_reports(self, filter: WATSFilter) -> List[ReportHeader]:
        """
        Get UUR report headers (like Repair Reports in Reporting).
        
        By default the 1000 newest reports that match the filter are returned.
        Use topCount filter to change this.
        
        Note: This API is not suitable for workflow or production management,
        use the Production module instead.
        
        Args:
            filter: WATSFilter with filter parameters
            
        Returns:
            List of ReportHeader objects
        """
        return self._api.get_uur_reports(filter)
    
    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------
    
    def get_yield_summary(
        self,
        part_number: str,
        revision: Optional[str] = None,
        days: int = 30
    ) -> List[YieldData]:
        """
        Get yield summary for a product over a time period.
        
        Args:
            part_number: Product part number
            revision: Optional product revision
            days: Number of days to include (default: 30)
            
        Returns:
            List of YieldData objects
        """
        filter = WATSFilter(
            partNumber=part_number,
            revision=revision,
            periodCount=days,
            dimensions="partNumber;period"
        )
        return self.get_dynamic_yield(filter)
    
    def get_station_yield(
        self,
        station_name: str,
        days: int = 7
    ) -> List[YieldData]:
        """
        Get yield statistics for a specific test station.
        
        Args:
            station_name: Test station name
            days: Number of days to include (default: 7)
            
        Returns:
            List of YieldData objects
        """
        filter = WATSFilter(
            stationName=station_name,
            periodCount=days,
            dimensions="stationName;period"
        )
        return self.get_dynamic_yield(filter)
