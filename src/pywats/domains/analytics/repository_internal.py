"""Analytics repository - internal API data access layer.

⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️

Uses internal WATS API endpoints that are not publicly documented.
These endpoints may change without notice. This module should be
replaced with public API endpoints as soon as they become available.

Unit Flow endpoints for production flow visualization:
- POST /api/internal/UnitFlow - Main query endpoint
- GET /api/internal/UnitFlow/Links - Get flow links
- GET /api/internal/UnitFlow/Nodes - Get flow nodes
- POST /api/internal/UnitFlow/SN - Query by serial numbers
- POST /api/internal/UnitFlow/SplitBy - Split flow by dimension
- POST /api/internal/UnitFlow/UnitOrder - Set unit ordering
- GET /api/internal/UnitFlow/Units - Get individual units

Step/Measurement filter endpoints:
- POST /api/internal/App/AggregatedMeasurements - Aggregated measurements with step filters
- GET/POST /api/internal/App/MeasurementList - Measurement list with step filters
- GET/POST /api/internal/App/StepStatusList - Step status list with filters

The internal API requires the Referer header to be set to the base URL.
"""
from typing import List, Optional, Dict, Any, Union

from ...core import HttpClient
from .models import (
    UnitFlowNode,
    UnitFlowLink,
    UnitFlowUnit,
    UnitFlowFilter,
    UnitFlowResult,
    AggregatedMeasurement,
    MeasurementListItem,
    StepStatusItem,
)


class AnalyticsRepositoryInternal:
    """
    Analytics data access layer using internal API.
    
    ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
    
    Provides access to Unit Flow functionality for production flow
    visualization and bottleneck analysis.
    
    Uses:
    - POST /api/internal/UnitFlow
    - GET /api/internal/UnitFlow/Links
    - GET /api/internal/UnitFlow/Nodes
    - POST /api/internal/UnitFlow/SN
    - POST /api/internal/UnitFlow/SplitBy
    - POST /api/internal/UnitFlow/UnitOrder
    - GET /api/internal/UnitFlow/Units
    
    The internal API requires the Referer header.
    """
    
    def __init__(self, http_client: HttpClient, base_url: str):
        """
        Initialize repository with HTTP client and base URL.
        
        Args:
            http_client: The HTTP client for API calls
            base_url: The base URL (needed for Referer header)
        """
        self._http = http_client
        self._base_url = base_url.rstrip('/')
    
    def _internal_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make an internal API GET request with Referer header.
        
        ⚠️ INTERNAL: Adds Referer header required by internal API.
        """
        response = self._http.get(
            endpoint,
            params=params,
            headers={"Referer": self._base_url}
        )
        if response.is_success:
            return response.data
        return None
    
    def _internal_post(self, endpoint: str, data: Any = None, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Make an internal API POST request with Referer header.
        
        ⚠️ INTERNAL: Adds Referer header required by internal API.
        """
        response = self._http.post(
            endpoint,
            data=data,
            params=params,
            headers={"Referer": self._base_url}
        )
        if response.is_success:
            return response.data
        return None
    
    # =========================================================================
    # Unit Flow Endpoints
    # =========================================================================
    
    def query_unit_flow(
        self, 
        filter_data: Optional[Union[UnitFlowFilter, Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Query unit flow data with filters.
        
        POST /api/internal/UnitFlow
        
        This is the main endpoint for unit flow queries. Returns nodes
        and links representing how units flow through production.
        
        Args:
            filter_data: UnitFlowFilter or dict with filter parameters
            
        Returns:
            Raw response data containing nodes and links, or None
        """
        if filter_data is None:
            data = {}
        elif isinstance(filter_data, UnitFlowFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = dict(filter_data)
        
        return self._internal_post("/api/internal/UnitFlow", data=data)
    
    def get_unit_flow_links(self) -> List[UnitFlowLink]:
        """
        Get all unit flow links.
        
        GET /api/internal/UnitFlow/Links
        
        Returns the links (edges) between nodes in the unit flow diagram.
        
        Returns:
            List of UnitFlowLink objects
        """
        data = self._internal_get("/api/internal/UnitFlow/Links")
        if data and isinstance(data, list):
            return [UnitFlowLink.model_validate(item) for item in data]
        return []
    
    def get_unit_flow_nodes(self) -> List[UnitFlowNode]:
        """
        Get all unit flow nodes.
        
        GET /api/internal/UnitFlow/Nodes
        
        Returns the nodes (operations/processes) in the unit flow diagram.
        
        Returns:
            List of UnitFlowNode objects
        """
        data = self._internal_get("/api/internal/UnitFlow/Nodes")
        if data and isinstance(data, list):
            return [UnitFlowNode.model_validate(item) for item in data]
        return []
    
    def query_unit_flow_by_serial_numbers(
        self, 
        serial_numbers: List[str],
        filter_data: Optional[Union[UnitFlowFilter, Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Query unit flow for specific serial numbers.
        
        POST /api/internal/UnitFlow/SN
        
        Traces the production flow path for specific units.
        
        Args:
            serial_numbers: List of serial numbers to query
            filter_data: Additional filter parameters
            
        Returns:
            Raw response data containing flow information, or None
        """
        if filter_data is None:
            data = {}
        elif isinstance(filter_data, UnitFlowFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = dict(filter_data)
        
        # Ensure serial numbers are included
        data["serialNumbers"] = serial_numbers
        
        return self._internal_post("/api/internal/UnitFlow/SN", data=data)
    
    def set_unit_flow_split_by(
        self, 
        split_by: str,
        filter_data: Optional[Union[UnitFlowFilter, Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Set the split-by dimension for unit flow analysis.
        
        POST /api/internal/UnitFlow/SplitBy
        
        Splits the flow diagram by a specific dimension (e.g., station, location).
        
        Args:
            split_by: Dimension to split by (e.g., "stationName", "location")
            filter_data: Additional filter parameters
            
        Returns:
            Raw response data with split flow, or None
        """
        if filter_data is None:
            data = {}
        elif isinstance(filter_data, UnitFlowFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = dict(filter_data)
        
        data["splitBy"] = split_by
        
        return self._internal_post("/api/internal/UnitFlow/SplitBy", data=data)
    
    def set_unit_flow_order(
        self, 
        unit_order: str,
        filter_data: Optional[Union[UnitFlowFilter, Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Set the unit ordering for flow analysis.
        
        POST /api/internal/UnitFlow/UnitOrder
        
        Controls how units are ordered in the flow visualization.
        
        Args:
            unit_order: Order specification (e.g., "startTime", "serialNumber")
            filter_data: Additional filter parameters
            
        Returns:
            Raw response data with ordered flow, or None
        """
        if filter_data is None:
            data = {}
        elif isinstance(filter_data, UnitFlowFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = dict(filter_data)
        
        data["unitOrder"] = unit_order
        
        return self._internal_post("/api/internal/UnitFlow/UnitOrder", data=data)
    
    def get_unit_flow_units(self) -> List[UnitFlowUnit]:
        """
        Get individual units from the unit flow.
        
        GET /api/internal/UnitFlow/Units
        
        Returns the list of individual units that have traversed the flow.
        
        Returns:
            List of UnitFlowUnit objects
        """
        data = self._internal_get("/api/internal/UnitFlow/Units")
        if data and isinstance(data, list):
            return [UnitFlowUnit.model_validate(item) for item in data]
        return []
    
    def set_unit_flow_visibility(
        self,
        show_list: Optional[List[str]] = None,
        hide_list: Optional[List[str]] = None,
        filter_data: Optional[Union[UnitFlowFilter, Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Control visibility of operations in the unit flow.
        
        POST /api/internal/UnitFlow (with showList/hideList)
        
        Show or hide specific operations/nodes in the flow diagram.
        This is related to the Show/HideList Operations feature.
        
        Args:
            show_list: List of operation IDs/names to show
            hide_list: List of operation IDs/names to hide
            filter_data: Additional filter parameters
            
        Returns:
            Raw response data with updated visibility, or None
        """
        if filter_data is None:
            data = {}
        elif isinstance(filter_data, UnitFlowFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = dict(filter_data)
        
        if show_list is not None:
            data["showList"] = show_list
        if hide_list is not None:
            data["hideList"] = hide_list
        
        return self._internal_post("/api/internal/UnitFlow", data=data)
    
    def expand_unit_flow_operations(
        self,
        expand: bool = True,
        filter_data: Optional[Union[UnitFlowFilter, Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Expand or collapse operations in the unit flow.
        
        POST /api/internal/UnitFlow (with expandOperations)
        
        Controls whether operations are shown expanded (showing sub-operations)
        or collapsed (aggregated view).
        
        Args:
            expand: True to expand, False to collapse
            filter_data: Additional filter parameters
            
        Returns:
            Raw response data with updated expansion, or None
        """
        if filter_data is None:
            data = {}
        elif isinstance(filter_data, UnitFlowFilter):
            data = filter_data.model_dump(by_alias=True, exclude_none=True)
        else:
            data = dict(filter_data)
        
        data["expandOperations"] = expand
        
        return self._internal_post("/api/internal/UnitFlow", data=data)
    # =========================================================================
    # Step/Measurement Filter Endpoints (Internal API)
    # =========================================================================
    
    def get_aggregated_measurements(
        self,
        filter_data: Dict[str, Any],
        step_filters: str,
        sequence_filters: str,
        measurement_name: Optional[str] = None
    ) -> List[AggregatedMeasurement]:
        """
        Get aggregated measurement data with step/sequence filters.
        
        POST /api/internal/App/AggregatedMeasurements
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Returns aggregated statistics (count, min, max, avg, stdev, cpk, etc.)
        for measurements matching the specified step and sequence filters.
        
        Args:
            filter_data: Filter parameters including:
                - serialNumber, partNumber, revision, batchNumber
                - stationName, testOperation, status, yield
                - productGroup, level, swFilename, swVersion
                - dateFrom, dateTo, dateGrouping, periodCount
                - includeCurrentPeriod, maxCount, minCount, topCount
            step_filters: XML string defining step filters (required).
                Get from TopFailed endpoint results.
            sequence_filters: XML string defining sequence filters (required).
                Get from TopFailed endpoint results.
            measurement_name: Optional name of the measurement to filter by.
            
        Returns:
            List of AggregatedMeasurement objects with statistics.
            
        Example:
            >>> # Get aggregated measurements with step filters
            >>> results = repo.get_aggregated_measurements(
            ...     filter_data={"partNumber": "WIDGET-001", "periodCount": 30},
            ...     step_filters="<filters>...</filters>",
            ...     sequence_filters="<filters>...</filters>",
            ...     measurement_name="Voltage"
            ... )
            >>> for m in results:
            ...     print(f"{m.step_name}: avg={m.avg}, cpk={m.cpk}")
        """
        params = {
            "stepFilters": step_filters,
            "sequenceFilters": sequence_filters,
        }
        if measurement_name:
            params["measurementName"] = measurement_name
            
        data = self._internal_post(
            "/api/internal/App/AggregatedMeasurements",
            data=filter_data,
            params=params
        )
        
        if data and isinstance(data, list):
            return [AggregatedMeasurement.model_validate(item) for item in data]
        return []
    
    def get_measurement_list_simple(
        self,
        product_group_id: str,
        level_id: str,
        days: int,
        step_filters: str,
        sequence_filters: str
    ) -> List[MeasurementListItem]:
        """
        Get measurement list using simple query parameters.
        
        GET /api/internal/App/MeasurementList
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Simple version that queries measurements by product group, level,
        and time range with step/sequence filters.
        
        Args:
            product_group_id: Product group ID (required)
            level_id: Level ID (required)
            days: Number of days to query (required)
            step_filters: XML string defining step filters (required)
            sequence_filters: XML string defining sequence filters (required)
            
        Returns:
            List of MeasurementListItem objects.
            
        Example:
            >>> # Get measurements for last 7 days
            >>> results = repo.get_measurement_list_simple(
            ...     product_group_id="pg-123",
            ...     level_id="level-456",
            ...     days=7,
            ...     step_filters="<filters>...</filters>",
            ...     sequence_filters="<filters>...</filters>"
            ... )
        """
        params = {
            "productGroupId": product_group_id,
            "levelId": level_id,
            "days": days,
            "stepFilters": step_filters,
            "sequenceFilters": sequence_filters,
        }
        
        data = self._internal_get("/api/internal/App/MeasurementList", params=params)
        
        if data and isinstance(data, list):
            return [MeasurementListItem.model_validate(item) for item in data]
        return []
    
    def get_measurement_list(
        self,
        filter_data: Dict[str, Any],
        step_filters: str,
        sequence_filters: str
    ) -> List[MeasurementListItem]:
        """
        Get measurement list with full filter support.
        
        POST /api/internal/App/MeasurementList
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Advanced version that allows full filter customization with
        step and sequence filters.
        
        Args:
            filter_data: Filter parameters including:
                - serialNumber, partNumber, revision, batchNumber
                - stationName, testOperation, status, yield
                - productGroup, level, swFilename, swVersion
                - dateFrom, dateTo, dateGrouping, periodCount
                - includeCurrentPeriod, maxCount, minCount, topCount
            step_filters: XML string defining step filters (required)
            sequence_filters: XML string defining sequence filters (required)
            
        Returns:
            List of MeasurementListItem objects with measurement details.
            
        Example:
            >>> # Get measurements with custom filters
            >>> results = repo.get_measurement_list(
            ...     filter_data={
            ...         "partNumber": "WIDGET-001",
            ...         "dateFrom": "2024-01-01T00:00:00",
            ...         "dateTo": "2024-01-31T23:59:59"
            ...     },
            ...     step_filters="<filters>...</filters>",
            ...     sequence_filters="<filters>...</filters>"
            ... )
            >>> for m in results:
            ...     print(f"{m.serial_number}: {m.step_name} = {m.value}")
        """
        params = {
            "stepFilters": step_filters,
            "sequenceFilters": sequence_filters,
        }
        
        data = self._internal_post(
            "/api/internal/App/MeasurementList",
            data=filter_data,
            params=params
        )
        
        if data and isinstance(data, list):
            return [MeasurementListItem.model_validate(item) for item in data]
        return []
    
    def get_step_status_list_simple(
        self,
        product_group_id: str,
        level_id: str,
        days: int,
        step_filters: str,
        sequence_filters: str
    ) -> List[StepStatusItem]:
        """
        Get step status list using simple query parameters.
        
        GET /api/internal/App/StepStatusList
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Simple version that queries step statuses by product group, level,
        and time range with step/sequence filters.
        
        Args:
            product_group_id: Product group ID (required)
            level_id: Level ID (required)
            days: Number of days to query (required)
            step_filters: XML string defining step filters (required)
            sequence_filters: XML string defining sequence filters (required)
            
        Returns:
            List of StepStatusItem objects.
            
        Example:
            >>> # Get step statuses for last 30 days
            >>> results = repo.get_step_status_list_simple(
            ...     product_group_id="pg-123",
            ...     level_id="level-456",
            ...     days=30,
            ...     step_filters="<filters>...</filters>",
            ...     sequence_filters="<filters>...</filters>"
            ... )
            >>> for step in results:
            ...     print(f"{step.step_name}: {step.pass_count}/{step.total_count}")
        """
        params = {
            "productGroupId": product_group_id,
            "levelId": level_id,
            "days": days,
            "stepFilters": step_filters,
            "sequenceFilters": sequence_filters,
        }
        
        data = self._internal_get("/api/internal/App/StepStatusList", params=params)
        
        if data and isinstance(data, list):
            return [StepStatusItem.model_validate(item) for item in data]
        return []
    
    def get_step_status_list(
        self,
        filter_data: Dict[str, Any],
        step_filters: str,
        sequence_filters: str
    ) -> List[StepStatusItem]:
        """
        Get step status list with full filter support.
        
        POST /api/internal/App/StepStatusList
        
        ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
        
        Advanced version that allows full filter customization with
        step and sequence filters.
        
        Args:
            filter_data: Filter parameters including:
                - serialNumber, partNumber, revision, batchNumber
                - stationName, testOperation, status, yield
                - productGroup, level, swFilename, swVersion
                - dateFrom, dateTo, dateGrouping, periodCount
                - includeCurrentPeriod, maxCount, minCount, topCount
            step_filters: XML string defining step filters (required)
            sequence_filters: XML string defining sequence filters (required)
            
        Returns:
            List of StepStatusItem objects with step status details.
            
        Example:
            >>> # Get step statuses with custom filters
            >>> results = repo.get_step_status_list(
            ...     filter_data={
            ...         "partNumber": "WIDGET-001",
            ...         "status": "Failed",
            ...         "periodCount": 30
            ...     },
            ...     step_filters="<filters>...</filters>",
            ...     sequence_filters="<filters>...</filters>"
            ... )
            >>> for step in results:
            ...     fail_rate = step.fail_count / step.total_count * 100
            ...     print(f"{step.step_name}: {fail_rate:.1f}% failure rate")
        """
        params = {
            "stepFilters": step_filters,
            "sequenceFilters": sequence_filters,
        }
        
        data = self._internal_post(
            "/api/internal/App/StepStatusList",
            data=filter_data,
            params=params
        )
        
        if data and isinstance(data, list):
            return [StepStatusItem.model_validate(item) for item in data]
        return []