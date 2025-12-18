"""Analytics service - business logic layer.

All business operations for statistics, KPIs, yield analysis, and dashboard data.
Note: Maps to the WATS /api/App/* endpoints (backend naming).
"""
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union

from .repository import AnalyticsRepository
from .models import (
    YieldData,
    ProcessInfo,
    LevelInfo,
    ProductGroup,
    StepAnalysisRow,
)
from ..report.models import WATSFilter, ReportHeader


class AnalyticsService:
    """
    Analytics/Statistics business logic layer.

    Provides high-level operations for yield statistics, KPIs, failure analysis,
    and production analytics. This module wraps the WATS /api/App/* endpoints.
    
    Example:
        >>> api = pyWATS(base_url="...", token="...")
        >>> # Get yield statistics
        >>> yield_data = api.analytics.get_dynamic_yield(
        ...     WATSFilter(part_number="WIDGET-001", period_count=30)
        ... )
        >>> # Get top failures
        >>> failures = api.analytics.get_top_failed(part_number="WIDGET-001")
    """

    def __init__(self, repository: AnalyticsRepository):
        """
        Initialize with AnalyticsRepository.

        Args:
            repository: AnalyticsRepository instance for data access
        """
        self._repository = repository

    # =========================================================================
    # System Info
    # =========================================================================

    def get_version(self) -> Dict[str, Any]:
        """
        Get WATS API version information.

        Returns:
            Version information dictionary
        """
        return self._repository.get_version() or {}

    def get_processes(self) -> List[ProcessInfo]:
        """
        Get all defined test processes/operations.

        Returns:
            List of ProcessInfo objects
        """
        return self._repository.get_processes()

    def get_levels(self) -> List[LevelInfo]:
        """
        Get all production levels.

        Returns:
            List of LevelInfo objects
        """
        return self._repository.get_levels()

    def get_product_groups(self) -> List[ProductGroup]:
        """
        Get all product groups.

        Returns:
            List of ProductGroup objects
        """
        return self._repository.get_product_groups()

    # =========================================================================
    # Yield Statistics
    # =========================================================================

    def get_dynamic_yield(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[YieldData]:
        """
        Get dynamic yield statistics by custom dimensions (PREVIEW).

        Supported dimensions: partNumber, productName, stationName, location,
        purpose, revision, testOperation, processCode, swFilename, swVersion,
        productGroup, level, period, batchNumber, operator, fixtureId, etc.

        Args:
            filter_data: WATSFilter with dimensions and filters

        Returns:
            List of YieldData objects
        """
        return self._repository.get_dynamic_yield(filter_data)

    def get_dynamic_repair(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Get dynamic repair statistics by custom dimensions (PREVIEW).

        Args:
            filter_data: WATSFilter with dimensions and filters

        Returns:
            List of repair statistics data
        """
        return self._repository.get_dynamic_repair(filter_data)

    def get_volume_yield(
        self,
        filter_data: Optional[WATSFilter] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None,
    ) -> List[YieldData]:
        """
        Get volume/yield statistics.

        Args:
            filter_data: Optional WATSFilter for POST request
            product_group: Optional product group filter (for GET)
            level: Optional level filter (for GET)

        Returns:
            List of YieldData objects
        """
        return self._repository.get_volume_yield(
            filter_data=filter_data, product_group=product_group, level=level
        )

    def get_worst_yield(
        self,
        filter_data: Optional[WATSFilter] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None,
    ) -> List[YieldData]:
        """
        Get worst yield statistics.

        Args:
            filter_data: Optional WATSFilter for POST request
            product_group: Optional product group filter (for GET)
            level: Optional level filter (for GET)

        Returns:
            List of YieldData objects
        """
        return self._repository.get_worst_yield(
            filter_data=filter_data, product_group=product_group, level=level
        )

    def get_worst_yield_by_product_group(
        self, filter_data: WATSFilter
    ) -> List[YieldData]:
        """
        Get worst yield by product group.

        Args:
            filter_data: WATSFilter with parameters

        Returns:
            List of YieldData objects by product group
        """
        return self._repository.get_worst_yield_by_product_group(filter_data)

    # =========================================================================
    # High Volume Analysis
    # =========================================================================

    def get_high_volume(
        self,
        filter_data: Optional[WATSFilter] = None,
        product_group: Optional[str] = None,
        level: Optional[str] = None,
    ) -> List[YieldData]:
        """
        Get high volume product list.

        Args:
            filter_data: Optional WATSFilter for POST request
            product_group: Optional product group filter (for GET)
            level: Optional level filter (for GET)

        Returns:
            List of YieldData objects
        """
        return self._repository.get_high_volume(
            filter_data=filter_data, product_group=product_group, level=level
        )

    def get_high_volume_by_product_group(
        self, filter_data: WATSFilter
    ) -> List[YieldData]:
        """
        Get yield by product group sorted by volume.

        Args:
            filter_data: WATSFilter with parameters

        Returns:
            List of YieldData objects by product group
        """
        return self._repository.get_high_volume_by_product_group(filter_data)

    # =========================================================================
    # Failure Analysis
    # =========================================================================

    def get_top_failed(
        self,
        filter_data: Optional[WATSFilter] = None,
        *,
        product_group: Optional[str] = None,
        level: Optional[str] = None,
        part_number: Optional[str] = None,
        revision: Optional[str] = None,
        top_count: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get top failed test steps.

        Can be called with a WATSFilter (uses POST) or with explicit parameters (uses GET).

        Args:
            filter_data: Optional WATSFilter for POST request (takes precedence)
            product_group: Filter by product group (GET only)
            level: Filter by production level (GET only)
            part_number: Filter by part number (GET only)
            revision: Filter by revision (GET only)
            top_count: Maximum number of results (GET only)

        Returns:
            List of top failed step data with failure counts and rates
        """
        return self._repository.get_top_failed(
            filter_data,
            product_group=product_group,
            level=level,
            part_number=part_number,
            revision=revision,
            top_count=top_count,
        )

    def get_test_step_analysis(
        self, filter_data: Union[WATSFilter, Dict[str, Any]]
    ) -> List[StepAnalysisRow]:
        """
        Get test step analysis data (PREVIEW).

        Args:
            filter_data: WATSFilter with analysis parameters

        Returns:
            List of StepAnalysisRow rows
        """
        return self._repository.get_test_step_analysis(filter_data)

    def get_test_step_analysis_for_operation(
        self,
        part_number: str,
        test_operation: str,
        *,
        revision: Optional[str] = None,
        days: int = 30,
        run: int = 1,
        max_count: int = 10000,
    ) -> List[StepAnalysisRow]:
        """Convenience wrapper for TestStepAnalysis.

        The WATS API requires `partNumber` and `testOperation`.
        Defaults are aligned with the swagger notes:
        - maxCount: 10000
        - dateFrom: now - 30 days
        - run: 1 (first)
        """
        if not part_number:
            raise ValueError("part_number is required")
        if not test_operation:
            raise ValueError("test_operation is required")

        filter_data = WATSFilter(
            part_number=part_number,
            test_operation=test_operation,
            revision=revision,
            max_count=max_count,
            date_from=datetime.now() - timedelta(days=days),
            run=run,
        )
        return self.get_test_step_analysis(filter_data)

    # =========================================================================
    # Repair History
    # =========================================================================

    def get_related_repair_history(
        self, part_number: str, revision: str
    ) -> List[Dict[str, Any]]:
        """
        Get list of repaired failures related to the part number and revision.

        Args:
            part_number: Product part number
            revision: Product revision

        Returns:
            List of repair history records
        """
        return self._repository.get_related_repair_history(
            part_number, revision
        )

    # =========================================================================
    # Measurement Analysis
    # =========================================================================

    def get_aggregated_measurements(
        self, filter_data: WATSFilter
    ) -> List[Dict[str, Any]]:
        """
        Get aggregated measurement statistics.

        Args:
            filter_data: WATSFilter with measurement filters

        Returns:
            List of aggregated measurement data
        """
        return self._repository.get_aggregated_measurements(filter_data)

    def get_measurements(
        self, filter_data: WATSFilter
    ) -> List[Dict[str, Any]]:
        """
        Get measurement data (PREVIEW).

        Args:
            filter_data: WATSFilter with measurement filters

        Returns:
            List of measurement data
        """
        return self._repository.get_measurements(filter_data)

    # =========================================================================
    # OEE Analysis
    # =========================================================================

    def get_oee_analysis(self, filter_data: WATSFilter) -> Dict[str, Any]:
        """
        Get Overall Equipment Effectiveness analysis.

        Supported filters: productGroup, level, partNumber, revision,
        stationName, testOperation, status, swFilename, swVersion,
        socket, dateFrom, dateTo

        Args:
            filter_data: WATSFilter with OEE parameters

        Returns:
            OEE analysis data
        """
        return self._repository.get_oee_analysis(filter_data)

    # =========================================================================
    # Serial Number History
    # =========================================================================

    def get_serial_number_history(
        self, filter_data: WATSFilter
    ) -> List[ReportHeader]:
        """
        Get test history for a serial number.

        Supported filters: productGroup, level, serialNumber, partNumber,
        batchNumber, miscValue

        Args:
            filter_data: WATSFilter with serial number and other filters

        Returns:
            List of ReportHeader objects
        """
        return self._repository.get_serial_number_history(filter_data)

    # =========================================================================
    # UUT/UUR Reports
    # =========================================================================

    def get_uut_reports(
        self,
        filter_data: Optional[WATSFilter] = None,
        *,
        product_group: Optional[str] = None,
        level: Optional[str] = None,
        part_number: Optional[str] = None,
        revision: Optional[str] = None,
        serial_number: Optional[str] = None,
        status: Optional[str] = None,
        top_count: Optional[int] = None,
    ) -> List[ReportHeader]:
        """
        Get UUT report headers (like Test Reports in Reporting).

        Can be called with a WATSFilter (uses POST) or with explicit parameters (uses GET).
        By default the 1000 newest reports that match the filter are returned.

        Note: This API is not suitable for workflow or production management,
        use the Production module instead.

        Args:
            filter_data: Optional WATSFilter for POST request (takes precedence)
            product_group: Filter by product group (GET only)
            level: Filter by production level (GET only)
            part_number: Filter by part number (GET only)
            revision: Filter by revision (GET only)
            serial_number: Filter by serial number (GET only)
            status: Filter by status: 'Passed', 'Failed', 'Error' (GET only)
            top_count: Maximum number of results, default 1000 (GET only)

        Returns:
            List of ReportHeader objects
        """
        return self._repository.get_uut_reports(
            filter_data,
            product_group=product_group,
            level=level,
            part_number=part_number,
            revision=revision,
            serial_number=serial_number,
            status=status,
            top_count=top_count,
        )

    def get_uur_reports(self, filter_data: WATSFilter) -> List[ReportHeader]:
        """
        Get UUR report headers (like Repair Reports in Reporting).

        By default the 1000 newest reports that match the filter are returned.
        Use topCount filter to change this.

        Note: This API is not suitable for workflow or production management,
        use the Production module instead.

        Args:
            filter_data: WATSFilter with filter parameters

        Returns:
            List of ReportHeader objects
        """
        return self._repository.get_uur_reports(filter_data)

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def get_yield_summary(
        self,
        part_number: str,
        revision: Optional[str] = None,
        days: int = 30,
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
        filter_data = WATSFilter(
            part_number=part_number,
            revision=revision,
            period_count=days,
            dimensions="partNumber;period",
        )
        return self.get_dynamic_yield(filter_data)

    def get_station_yield(
        self, station_name: str, days: int = 7
    ) -> List[YieldData]:
        """
        Get yield statistics for a specific test station.

        Args:
            station_name: Test station name
            days: Number of days to include (default: 7)

        Returns:
            List of YieldData objects
        """
        filter_data = WATSFilter(
            station_name=station_name,
            period_count=days,
            dimensions="stationName;period",
        )
        return self.get_dynamic_yield(filter_data)
