"""
Tests for app module - statistics and KPI endpoints

These tests make actual API calls to the WATS server.
"""
from typing import Any
import pytest


class TestAppVersion:
    """Test app version endpoint"""

    def test_get_version(self, wats_client: Any) -> None:
        """Test getting API version"""
        print("\n=== GET VERSION ===")
        
        version = wats_client.app.get_version()
        
        print(f"API Version: {version}")
        print("===================\n")
        
        assert version is not None


class TestProductGroups:
    """Test product group retrieval"""

    def test_get_product_groups(self, wats_client: Any) -> None:
        """Test getting product groups"""
        print("\n=== GET PRODUCT GROUPS ===")
        
        groups = wats_client.app.get_product_groups()
        
        print(f"Retrieved {len(groups)} product groups")
        for g in groups[:5]:
            print(f"  - {g}")
        print("==========================\n")
        
        assert isinstance(groups, list)


class TestProcesses:
    """Test process/operation retrieval"""

    def test_get_processes(self, wats_client: Any) -> None:
        """Test getting process list"""
        print("\n=== GET PROCESSES ===")
        
        processes = wats_client.app.get_processes()
        
        print(f"Retrieved {len(processes)} processes")
        for p in processes[:5]:
            print(f"  - {p}")
        print("=====================\n")
        
        assert isinstance(processes, list)


class TestLevels:
    """Test level/station data retrieval"""

    def test_get_levels(self, wats_client: Any) -> None:
        """Test getting levels"""
        print("\n=== GET LEVELS ===")
        
        levels = wats_client.app.get_levels()
        
        print(f"Retrieved {len(levels)} levels")
        for lvl in levels[:5]:
            print(f"  - {lvl}")
        print("==================\n")
        
        assert isinstance(levels, list)


class TestYieldStatistics:
    """Test yield statistics endpoints"""

    def test_get_yield_summary(self, wats_client: Any) -> None:
        """Test getting yield summary for a product"""
        print("\n=== GET YIELD SUMMARY ===")
        
        # First get a product to use
        products = wats_client.product.get_products()
        if not products:
            pytest.skip("No products available")
        
        part_number = products[0].part_number
        print(f"Getting yield for: {part_number}")
        
        summary = wats_client.app.get_yield_summary(part_number=part_number, days=7)
        
        print(f"Yield summary: {summary}")
        print("=========================\n")

    def test_get_dynamic_yield(self, wats_client: Any) -> None:
        """Test getting dynamic yield data"""
        print("\n=== GET DYNAMIC YIELD ===")
        
        # Use minimal filter
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=10)
        
        result = wats_client.app.get_dynamic_yield(filter_obj)
        
        print(f"Dynamic yield result: {result}")
        print("=========================\n")

    def test_get_volume_yield(self, wats_client: Any) -> None:
        """Test getting volume yield"""
        print("\n=== GET VOLUME YIELD ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=10)
        
        result = wats_client.app.get_volume_yield(filter_obj)
        
        print(f"Volume yield: {result}")
        print("========================\n")


class TestTopFailed:
    """Test top failed analysis"""

    def test_get_top_failed(self, wats_client: Any) -> None:
        """Test getting top failed steps"""
        print("\n=== GET TOP FAILED ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=10)
        
        result = wats_client.app.get_top_failed(filter_obj)
        
        print(f"Top failed: {result}")
        print("======================\n")


class TestReportRetrieval:
    """Test report data retrieval through app service"""

    def test_get_uut_reports(self, wats_client: Any) -> None:
        """Test getting UUT reports through app service"""
        print("\n=== GET UUT REPORTS ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=5)
        
        reports = wats_client.app.get_uut_reports(filter_obj)
        
        print(f"Retrieved {len(reports)} UUT reports")
        print("=======================\n")
        
        assert isinstance(reports, list)

    def test_get_uur_reports(self, wats_client: Any) -> None:
        """Test getting UUR reports through app service"""
        print("\n=== GET UUR REPORTS ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=5)
        
        reports = wats_client.app.get_uur_reports(filter_obj)
        
        print(f"Retrieved {len(reports)} UUR reports")
        print("=======================\n")
        
        assert isinstance(reports, list)


class TestSerialNumberHistory:
    """Test serial number history lookup"""

    def test_get_serial_number_history(self, wats_client: Any) -> None:
        """Test getting history for a serial number - server may return 500"""
        from pywats.core.exceptions import ServerError
        
        print("\n=== GET SERIAL NUMBER HISTORY ===")
        
        # First get a known serial number from reports
        headers = wats_client.report.query_uut_headers()
        if not headers:
            pytest.skip("No report headers available")
        
        serial_number = headers[0].serial_number
        print(f"Getting history for: {serial_number}")
        
        try:
            history = wats_client.app.get_serial_number_history(serial_number)
            print(f"History entries: {len(history) if history else 0}")
        except ServerError as e:
            # Server may not support this endpoint or have data
            print(f"Server error (known issue): {e}")
            history = []
        
        print("=================================\n")
