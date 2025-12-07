"""
App/Statistics API Endpoints

Provides all REST API calls for KPIs, statistics, and analytics.

Public API Endpoints (from Swagger):
- POST /api/App/AggregatedMeasurements - Get aggregated measurements
- POST /api/App/DynamicRepair - Calculate repair stats (PREVIEW)
- POST /api/App/DynamicYield - Calculate yield (PREVIEW)
- GET/POST /api/App/HighVolume - High volume list
- POST /api/App/HighVolumeByProductGroup - Yield by product group sorted by volume
- GET /api/App/Levels - Get all ClientGroups
- POST /api/App/Measurements - Get measurements (PREVIEW)
- POST /api/App/OeeAnalysis - OEE analysis
- GET /api/App/Processes - Get processes
- GET /api/App/ProductGroups - Get all ProductGroups
- GET /api/App/RelatedRepairHistory - Get repaired failures history
- POST /api/App/SerialNumberHistory - Serial number history
- POST /api/App/TestStepAnalysis - Get step/measurement stats (PREVIEW)
- GET/POST /api/App/TopFailed - Get top failed steps
- POST /api/App/UurReport - Get UUR report headers
- GET/POST /api/App/UutReport - Get UUT report headers
- GET /api/App/Version - Get server/api version
- GET/POST /api/App/VolumeYield - Volume/Yield list
- GET/POST /api/App/WorstYield - Worst yield list
- POST /api/App/WorstYieldByProductGroup - Yield by product group sorted by lowest yield
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient, Response


class AppApi:
    """
    App/Statistics API endpoints.
    
    Endpoints for retrieving KPIs, statistics, yield data, and analytics.
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Version and System Info
    # =========================================================================
    
    def get_version(self) -> 'Response':
        """
        Get server/api version.
        
        GET /api/App/Version
        
        Returns:
            Response with version info
        """
        return self._http.get("/api/App/Version")
    
    # =========================================================================
    # Configuration: Processes, Levels, Product Groups
    # =========================================================================
    
    def get_processes(self) -> 'Response':
        """
        Get processes.
        
        GET /api/App/Processes
            
        Returns:
            Response with list of processes
        """
        return self._http.get("/api/App/Processes")
    
    def get_levels(self) -> 'Response':
        """
        Retrieves all ClientGroups (levels).
        
        GET /api/App/Levels
        
        Returns:
            Response with list of levels/client groups
        """
        return self._http.get("/api/App/Levels")
    
    def get_product_groups(self) -> 'Response':
        """
        Retrieves all ProductGroups.
        
        GET /api/App/ProductGroups
        
        Returns:
            Response with product groups
        """
        return self._http.get("/api/App/ProductGroups")
    
    # =========================================================================
    # Yield Statistics
    # =========================================================================
    
    def get_dynamic_yield(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Calculate yield by custom dimensions (PREVIEW).
        
        POST /api/App/DynamicYield
        
        Args:
            filter_data: Filter data including dimensions, topCount, periodCount, etc.
            
        Returns:
            Response with yield statistics
        """
        return self._http.post("/api/App/DynamicYield", data=filter_data)
    
    def get_volume_yield(
        self,
        filter_data: Optional[Dict[str, Any]] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> 'Response':
        """
        Volume/Yield list filtered by productGroup and level.
        
        POST /api/App/VolumeYield
        
        Args:
            filter_data: Filter data dictionary (for POST)
            product_group: Product group filter (for GET)
            level: Level filter (for GET)
            
        Returns:
            Response with volume/yield data
        """
        if filter_data:
            return self._http.post("/api/App/VolumeYield", data=filter_data)
        else:
            params: Dict[str, Any] = {}
            if product_group:
                params["productGroup"] = product_group
            if level:
                params["level"] = level
            return self._http.get("/api/App/VolumeYield", params=params if params else None)
    
    def get_high_volume(
        self,
        filter_data: Optional[Dict[str, Any]] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> 'Response':
        """
        High Volume list filtered by productGroup and level.
        
        GET/POST /api/App/HighVolume
        
        Args:
            filter_data: Filter data dictionary (for POST)
            product_group: Product group filter (for GET)
            level: Level filter (for GET)
            
        Returns:
            Response with high volume data
        """
        if filter_data:
            return self._http.post("/api/App/HighVolume", data=filter_data)
        else:
            params: Dict[str, Any] = {}
            if product_group:
                params["productGroup"] = product_group
            if level:
                params["level"] = level
            return self._http.get("/api/App/HighVolume", params=params if params else None)
    
    def get_high_volume_by_product_group(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Yield by product group sorted by volume.
        
        POST /api/App/HighVolumeByProductGroup
        
        Args:
            filter_data: Filter data dictionary
            
        Returns:
            Response with high volume data by product group
        """
        return self._http.post("/api/App/HighVolumeByProductGroup", data=filter_data)
    
    def get_worst_yield(
        self,
        filter_data: Optional[Dict[str, Any]] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> 'Response':
        """
        Worst Yield list filtered by productGroup and level.
        
        GET/POST /api/App/WorstYield
        
        Args:
            filter_data: Filter data dictionary (for POST)
            product_group: Product group filter (for GET)
            level: Level filter (for GET)
            
        Returns:
            Response with worst yield data
        """
        if filter_data:
            return self._http.post("/api/App/WorstYield", data=filter_data)
        else:
            params: Dict[str, Any] = {}
            if product_group:
                params["productGroup"] = product_group
            if level:
                params["level"] = level
            return self._http.get("/api/App/WorstYield", params=params if params else None)
    
    def get_worst_yield_by_product_group(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Yield by product group sorted by lowest yield.
        
        POST /api/App/WorstYieldByProductGroup
        
        Args:
            filter_data: Filter data dictionary
            
        Returns:
            Response with worst yield data by product group
        """
        return self._http.post("/api/App/WorstYieldByProductGroup", data=filter_data)
    
    # =========================================================================
    # Repair Statistics
    # =========================================================================
    
    def get_dynamic_repair(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Calculate repair statistics by custom dimensions (PREVIEW).
        
        POST /api/App/DynamicRepair
        
        Args:
            filter_data: Filter data including dimensions, topCount, periodCount, etc.
            
        Returns:
            Response with repair statistics
        """
        return self._http.post("/api/App/DynamicRepair", data=filter_data)
    
    def get_related_repair_history(
        self,
        part_number: str,
        revision: str
    ) -> 'Response':
        """
        Get list of repaired failures related to the part number and revision.
        
        GET /api/App/RelatedRepairHistory
        
        Args:
            part_number: Product part number
            revision: Product revision
            
        Returns:
            Response with repair history
        """
        params: Dict[str, Any] = {
            "partNumber": part_number,
            "revision": revision
        }
        return self._http.get("/api/App/RelatedRepairHistory", params=params)
    
    # =========================================================================
    # Failure Analysis
    # =========================================================================
    
    def get_top_failed(
        self,
        filter_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> 'Response':
        """
        Get the top failed steps for the reports with the specified parameters.
        
        GET/POST /api/App/TopFailed
        
        Args:
            filter_data: Filter data dictionary (for POST)
            **kwargs: Query parameters (for GET)
            
        Returns:
            Response with top failed steps
        """
        if filter_data:
            return self._http.post("/api/App/TopFailed", data=filter_data)
        else:
            return self._http.get("/api/App/TopFailed", params=kwargs if kwargs else None)
    
    def get_test_step_analysis(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Get step and measurement statistics (PREVIEW).
        
        POST /api/App/TestStepAnalysis
        
        Args:
            filter_data: Filter data dictionary
            
        Returns:
            Response with step analysis
        """
        return self._http.post("/api/App/TestStepAnalysis", data=filter_data)
    
    # =========================================================================
    # Measurements
    # =========================================================================
    
    def get_measurements(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Get numeric measurements by measurement path (PREVIEW).
        
        POST /api/App/Measurements
        
        A maximum of 10000 measurements are returned.
        Requesting with empty filter returns measurements from the last 
        seven days most failed steps.
        
        Args:
            filter_data: Filter data dictionary
            
        Returns:
            Response with measurements
        """
        return self._http.post("/api/App/Measurements", data=filter_data)
    
    def get_aggregated_measurements(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Get aggregated numeric measurements by measurement path.
        
        POST /api/App/AggregatedMeasurements
        
        A maximum of 10000 measurements are returned.
        Requesting with empty filter returns measurements from the last 
        seven days most failed steps.
        
        Args:
            filter_data: Filter data dictionary
            
        Returns:
            Response with aggregated measurements
        """
        return self._http.post("/api/App/AggregatedMeasurements", data=filter_data)
    
    # =========================================================================
    # OEE (Overall Equipment Effectiveness)
    # =========================================================================
    
    def get_oee_analysis(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Overall Equipment Effectiveness - analysis.
        
        POST /api/App/OeeAnalysis
        
        Supported filters: productGroup, level, partNumber, revision, 
        stationName, testOperation, status, swFilename, swVersion, 
        socket, dateFrom, dateTo
        
        Args:
            filter_data: Filter data with targetOutput and other parameters
            
        Returns:
            Response with OEE data
        """
        return self._http.post("/api/App/OeeAnalysis", data=filter_data)
    
    # =========================================================================
    # Serial Number and Unit History
    # =========================================================================
    
    def get_serial_number_history(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Serial Number History.
        
        POST /api/App/SerialNumberHistory
        
        Supported filters: productGroup, level, serialNumber, partNumber,
        batchNumber, miscValue
        
        Args:
            filter_data: Filter data dictionary
            
        Returns:
            Response with serial number history
        """
        return self._http.post("/api/App/SerialNumberHistory", data=filter_data)
    
    def get_uut_reports(
        self,
        filter_data: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> 'Response':
        """
        Returns UUT report header info like Test Reports in Reporting.
        
        GET/POST /api/App/UutReport
        
        Uses watsfilter with Supported filters: productGroup, level, 
        serialNumber, partNumber, revision, batchNumber, stationName, 
        testOperation, status, miscValue, dateFrom, dateTo, topCount
        
        By default the 1000 newest reports that match the filter are returned.
        
        Note: This API is not suitable for workflow or production management,
        use the Production module instead.
        
        Args:
            filter_data: Filter data dictionary (for POST)
            **kwargs: Query parameters (for GET)
            
        Returns:
            Response with UUT reports
        """
        if filter_data:
            return self._http.post("/api/App/UutReport", data=filter_data)
        else:
            return self._http.get("/api/App/UutReport", params=kwargs if kwargs else None)
    
    def get_uur_reports(self, filter_data: Dict[str, Any]) -> 'Response':
        """
        Returns UUR report header info like Repair Reports in Reporting.
        
        POST /api/App/UurReport
        
        Uses watsfilter with supported filters: productGroup, level, 
        serialNumber, partNumber, revision, batchNumber, stationName, 
        testOperation, status, miscValue, dateFrom, dateTo, topCount
        
        By default the 1000 newest reports that match the filter are returned.
        
        Note: This API is not suitable for workflow or production management,
        use the Production module instead.
        
        Args:
            filter_data: Filter data dictionary
            
        Returns:
            Response with UUR reports
        """
        return self._http.post("/api/App/UurReport", data=filter_data)
