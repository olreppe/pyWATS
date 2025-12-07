"""
App/Statistics API Endpoints

Provides all REST API calls for KPIs, statistics, and analytics.
All methods return typed responses instead of raw Response objects.

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

from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..models import (
    WATSFilter, YieldData, ProcessInfo, LevelInfo, ProductGroup, ReportHeader
)


class AppApi:
    """
    App/Statistics API endpoints.
    
    Endpoints for retrieving KPIs, statistics, yield data, and analytics.
    All methods return typed responses.
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Version and System Info
    # =========================================================================
    
    def get_version(self) -> Optional[Dict[str, Any]]:
        """
        Get server/api version.
        
        GET /api/App/Version
        
        Returns:
            Version info dictionary or None
        """
        response = self._http.get("/api/App/Version")
        if response.is_success and response.data:
            return response.data
        return None
    
    # =========================================================================
    # Configuration: Processes, Levels, Product Groups
    # =========================================================================
    
    def get_processes(self) -> List[ProcessInfo]:
        """
        Get processes.
        
        GET /api/App/Processes
            
        Returns:
            List of ProcessInfo objects
        """
        response = self._http.get("/api/App/Processes")
        if response.is_success and response.data:
            return [ProcessInfo.model_validate(item) for item in response.data]
        return []
    
    def get_levels(self) -> List[LevelInfo]:
        """
        Retrieves all ClientGroups (levels).
        
        GET /api/App/Levels
        
        Returns:
            List of LevelInfo objects
        """
        response = self._http.get("/api/App/Levels")
        if response.is_success and response.data:
            return [LevelInfo.model_validate(item) for item in response.data]
        return []
    
    def get_product_groups(self) -> List[ProductGroup]:
        """
        Retrieves all ProductGroups.
        
        GET /api/App/ProductGroups
        
        Returns:
            List of ProductGroup objects
        """
        response = self._http.get("/api/App/ProductGroups")
        if response.is_success and response.data:
            return [ProductGroup.model_validate(item) for item in response.data]
        return []
    
    # =========================================================================
    # Yield Statistics
    # =========================================================================
    
    def get_dynamic_yield(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[YieldData]:
        """
        Calculate yield by custom dimensions (PREVIEW).
        
        POST /api/App/DynamicYield
        
        Args:
            filter_data: WATSFilter object or dict with dimensions, topCount, periodCount, etc.
            
        Returns:
            List of YieldData objects
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/DynamicYield", data=data)
        if response.is_success and response.data:
            return [YieldData.model_validate(item) for item in response.data]
        return []
    
    def get_volume_yield(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> List[YieldData]:
        """
        Volume/Yield list filtered by productGroup and level.
        
        POST /api/App/VolumeYield
        
        Args:
            filter_data: WATSFilter object or dict (for POST)
            product_group: Product group filter (for GET)
            level: Level filter (for GET)
            
        Returns:
            List of YieldData objects
        """
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                data = filter_data.model_dump(by_alias=True, exclude_none=True)
            else:
                data = filter_data
            response = self._http.post("/api/App/VolumeYield", data=data)
        else:
            params: Dict[str, Any] = {}
            if product_group:
                params["productGroup"] = product_group
            if level:
                params["level"] = level
            response = self._http.get("/api/App/VolumeYield", params=params if params else None)
        if response.is_success and response.data:
            return [YieldData.model_validate(item) for item in response.data]
        return []
    
    def get_high_volume(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> List[YieldData]:
        """
        High Volume list filtered by productGroup and level.
        
        GET/POST /api/App/HighVolume
        
        Args:
            filter_data: WATSFilter object or dict (for POST)
            product_group: Product group filter (for GET)
            level: Level filter (for GET)
            
        Returns:
            List of YieldData objects
        """
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                data = filter_data.model_dump(by_alias=True, exclude_none=True)
            else:
                data = filter_data
            response = self._http.post("/api/App/HighVolume", data=data)
        else:
            params: Dict[str, Any] = {}
            if product_group:
                params["productGroup"] = product_group
            if level:
                params["level"] = level
            response = self._http.get("/api/App/HighVolume", params=params if params else None)
        if response.is_success and response.data:
            return [YieldData.model_validate(item) for item in response.data]
        return []
    
    def get_high_volume_by_product_group(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[YieldData]:
        """
        Yield by product group sorted by volume.
        
        POST /api/App/HighVolumeByProductGroup
        
        Args:
            filter_data: WATSFilter object or dict
            
        Returns:
            List of YieldData objects
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/HighVolumeByProductGroup", data=data)
        if response.is_success and response.data:
            return [YieldData.model_validate(item) for item in response.data]
        return []
    
    def get_worst_yield(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None
    ) -> List[YieldData]:
        """
        Worst Yield list filtered by productGroup and level.
        
        GET/POST /api/App/WorstYield
        
        Args:
            filter_data: WATSFilter object or dict (for POST)
            product_group: Product group filter (for GET)
            level: Level filter (for GET)
            
        Returns:
            List of YieldData objects
        """
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                data = filter_data.model_dump(by_alias=True, exclude_none=True)
            else:
                data = filter_data
            response = self._http.post("/api/App/WorstYield", data=data)
        else:
            params: Dict[str, Any] = {}
            if product_group:
                params["productGroup"] = product_group
            if level:
                params["level"] = level
            response = self._http.get("/api/App/WorstYield", params=params if params else None)
        if response.is_success and response.data:
            return [YieldData.model_validate(item) for item in response.data]
        return []
    
    def get_worst_yield_by_product_group(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[YieldData]:
        """
        Yield by product group sorted by lowest yield.
        
        POST /api/App/WorstYieldByProductGroup
        
        Args:
            filter_data: WATSFilter object or dict
            
        Returns:
            List of YieldData objects
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/WorstYieldByProductGroup", data=data)
        if response.is_success and response.data:
            return [YieldData.model_validate(item) for item in response.data]
        return []
    
    # =========================================================================
    # Repair Statistics
    # =========================================================================
    
    def get_dynamic_repair(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate repair statistics by custom dimensions (PREVIEW).
        
        POST /api/App/DynamicRepair
        
        Args:
            filter_data: WATSFilter object or dict with dimensions, topCount, periodCount, etc.
            
        Returns:
            List of repair statistics dictionaries
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/DynamicRepair", data=data)
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else [response.data]
        return []
    
    def get_related_repair_history(
        self,
        part_number: str,
        revision: str
    ) -> List[Dict[str, Any]]:
        """
        Get list of repaired failures related to the part number and revision.
        
        GET /api/App/RelatedRepairHistory
        
        Args:
            part_number: Product part number
            revision: Product revision
            
        Returns:
            List of repair history dictionaries
        """
        params: Dict[str, Any] = {
            "partNumber": part_number,
            "revision": revision
        }
        response = self._http.get("/api/App/RelatedRepairHistory", params=params)
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else [response.data]
        return []
    
    # =========================================================================
    # Failure Analysis
    # =========================================================================
    
    def get_top_failed(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> List[Dict[str, Any]]:
        """
        Get the top failed steps for the reports with the specified parameters.
        
        GET/POST /api/App/TopFailed
        
        Args:
            filter_data: WATSFilter object or dict (for POST)
            **kwargs: Query parameters (for GET)
            
        Returns:
            List of failed step dictionaries
        """
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                data = filter_data.model_dump(by_alias=True, exclude_none=True)
            else:
                data = filter_data
            response = self._http.post("/api/App/TopFailed", data=data)
        else:
            response = self._http.get("/api/App/TopFailed", params=kwargs if kwargs else None)
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else [response.data]
        return []
    
    def get_test_step_analysis(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get step and measurement statistics (PREVIEW).
        
        POST /api/App/TestStepAnalysis
        
        Args:
            filter_data: WATSFilter object or dict
            
        Returns:
            Step analysis dictionary
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/TestStepAnalysis", data=data)
        if response.is_success and response.data:
            return response.data
        return {}
    
    # =========================================================================
    # Measurements
    # =========================================================================
    
    def get_measurements(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Get numeric measurements by measurement path (PREVIEW).
        
        POST /api/App/Measurements
        
        A maximum of 10000 measurements are returned.
        Requesting with empty filter returns measurements from the last 
        seven days most failed steps.
        
        Args:
            filter_data: WATSFilter object or dict
            
        Returns:
            List of measurement dictionaries
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/Measurements", data=data)
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else [response.data]
        return []
    
    def get_aggregated_measurements(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Get aggregated numeric measurements by measurement path.
        
        POST /api/App/AggregatedMeasurements
        
        A maximum of 10000 measurements are returned.
        Requesting with empty filter returns measurements from the last 
        seven days most failed steps.
        
        Args:
            filter_data: WATSFilter object or dict
            
        Returns:
            List of aggregated measurement dictionaries
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/AggregatedMeasurements", data=data)
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else [response.data]
        return []
    
    # =========================================================================
    # OEE (Overall Equipment Effectiveness)
    # =========================================================================
    
    def get_oee_analysis(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Overall Equipment Effectiveness - analysis.
        
        POST /api/App/OeeAnalysis
        
        Supported filters: productGroup, level, partNumber, revision, 
        stationName, testOperation, status, swFilename, swVersion, 
        socket, dateFrom, dateTo
        
        Args:
            filter_data: WATSFilter object or dict with targetOutput and other parameters
            
        Returns:
            OEE analysis dictionary
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/OeeAnalysis", data=data)
        if response.is_success and response.data:
            return response.data
        return {}
    
    # =========================================================================
    # Serial Number and Unit History
    # =========================================================================
    
    def get_serial_number_history(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[ReportHeader]:
        """
        Serial Number History.
        
        POST /api/App/SerialNumberHistory
        
        Supported filters: productGroup, level, serialNumber, partNumber,
        batchNumber, miscValue
        
        Args:
            filter_data: WATSFilter object or dict
            
        Returns:
            List of ReportHeader objects
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/SerialNumberHistory", data=data)
        if response.is_success and response.data:
            return [ReportHeader.model_validate(item) for item in response.data]
        return []
    
    def get_uut_reports(
        self,
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None,
        **kwargs: Any
    ) -> List[ReportHeader]:
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
            filter_data: WATSFilter object or dict (for POST)
            **kwargs: Query parameters (for GET)
            
        Returns:
            List of ReportHeader objects
        """
        if filter_data:
            if isinstance(filter_data, WATSFilter):
                data = filter_data.model_dump(by_alias=True, exclude_none=True)
            else:
                data = filter_data
            response = self._http.post("/api/App/UutReport", data=data)
        else:
            response = self._http.get("/api/App/UutReport", params=kwargs if kwargs else None)
        if response.is_success and response.data:
            return [ReportHeader.model_validate(item) for item in response.data]
        return []
    
    def get_uur_reports(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[ReportHeader]:
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
            filter_data: WATSFilter object or dict
            
        Returns:
            List of ReportHeader objects
        """
        if isinstance(filter_data, WATSFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = filter_data
        response = self._http.post("/api/App/UurReport", data=data)
        if response.is_success and response.data:
            return [ReportHeader.model_validate(item) for item in response.data]
        return []
