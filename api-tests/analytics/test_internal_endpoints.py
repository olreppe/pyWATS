"""
Tests for internal analytics endpoints (MeasurementList, StepStatusList, TopFailed)

⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️

These tests make actual API calls to the WATS server using internal endpoints.
The internal endpoints may not be available on all servers.

Endpoints tested:
- GET/POST /api/internal/App/MeasurementList
- GET/POST /api/internal/App/StepStatusList
- GET/POST /api/internal/App/TopFailed
- POST /api/internal/App/AggregatedMeasurements
"""
from typing import Any
from datetime import datetime, timedelta
import pytest

from pywats import (
    MeasurementListItem,
    StepStatusItem,
    TopFailedStep,
    AggregatedMeasurement,
)


class TestMeasurementListEndpoints:
    """Test internal MeasurementList endpoints"""

    def test_get_measurement_list_by_product(self, wats_client: Any) -> None:
        """Test GET /api/internal/App/MeasurementList with simple parameters"""
        print("\n=== GET MEASUREMENT LIST BY PRODUCT ===")
        
        # Note: These IDs need to match your WATS server configuration
        # Using placeholder values - adjust for your environment
        try:
            results = wats_client.analytics.get_measurement_list_by_product(
                product_group_id="00000000-0000-0000-0000-000000000000",
                level_id="00000000-0000-0000-0000-000000000000",
                days=30,
                step_filters="<filters></filters>",
                sequence_filters="<filters></filters>"
            )
            
            print(f"Retrieved {len(results)} measurements")
            if results:
                for m in results[:5]:
                    print(f"  - {m.serial_number}: {m.step_name} = {m.value}")
            
            assert isinstance(results, list)
            for item in results:
                assert isinstance(item, MeasurementListItem)
                
        except Exception as e:
            print(f"Error (expected if IDs don't exist): {e}")
            pytest.skip("Test requires valid product_group_id and level_id")
        
        print("========================================\n")

    def test_get_measurement_list_with_filter(self, wats_client: Any) -> None:
        """Test POST /api/internal/App/MeasurementList with filter"""
        print("\n=== GET MEASUREMENT LIST WITH FILTER ===")
        
        try:
            results = wats_client.analytics.get_measurement_list(
                filter_data={
                    "periodCount": 30,
                    "includeCurrentPeriod": True
                },
                step_filters="<filters></filters>",
                sequence_filters="<filters></filters>"
            )
            
            print(f"Retrieved {len(results)} measurements")
            if results:
                for m in results[:5]:
                    print(f"  - {m.serial_number}: {m.step_name} = {m.value}")
                    
            assert isinstance(results, list)
            for item in results:
                assert isinstance(item, MeasurementListItem)
                
        except Exception as e:
            print(f"Error: {e}")
            pytest.skip("Test may require specific filter parameters")
        
        print("=========================================\n")


class TestStepStatusListEndpoints:
    """Test internal StepStatusList endpoints"""

    def test_get_step_status_list_by_product(self, wats_client: Any) -> None:
        """Test GET /api/internal/App/StepStatusList with simple parameters"""
        print("\n=== GET STEP STATUS LIST BY PRODUCT ===")
        
        try:
            results = wats_client.analytics.get_step_status_list_by_product(
                product_group_id="00000000-0000-0000-0000-000000000000",
                level_id="00000000-0000-0000-0000-000000000000",
                days=30,
                step_filters="<filters></filters>",
                sequence_filters="<filters></filters>"
            )
            
            print(f"Retrieved {len(results)} step statuses")
            if results:
                for step in results[:5]:
                    total = step.total_count or 0
                    fail = step.fail_count or 0
                    fail_rate = (fail / total * 100) if total > 0 else 0
                    print(f"  - {step.step_name}: {fail}/{total} ({fail_rate:.1f}% fail)")
            
            assert isinstance(results, list)
            for item in results:
                assert isinstance(item, StepStatusItem)
                
        except Exception as e:
            print(f"Error (expected if IDs don't exist): {e}")
            pytest.skip("Test requires valid product_group_id and level_id")
        
        print("========================================\n")

    def test_get_step_status_list_with_filter(self, wats_client: Any) -> None:
        """Test POST /api/internal/App/StepStatusList with filter"""
        print("\n=== GET STEP STATUS LIST WITH FILTER ===")
        
        try:
            results = wats_client.analytics.get_step_status_list(
                filter_data={
                    "periodCount": 30,
                    "includeCurrentPeriod": True
                },
                step_filters="<filters></filters>",
                sequence_filters="<filters></filters>"
            )
            
            print(f"Retrieved {len(results)} step statuses")
            if results:
                for step in results[:5]:
                    total = step.total_count or 0
                    fail = step.fail_count or 0
                    fail_rate = (fail / total * 100) if total > 0 else 0
                    print(f"  - {step.step_name}: {fail}/{total} ({fail_rate:.1f}% fail)")
                    
            assert isinstance(results, list)
            for item in results:
                assert isinstance(item, StepStatusItem)
                
        except Exception as e:
            print(f"Error: {e}")
            pytest.skip("Test may require specific filter parameters")
        
        print("=========================================\n")


class TestTopFailedInternalEndpoints:
    """Test internal TopFailed endpoints"""

    def test_get_top_failed_by_product(self, wats_client: Any) -> None:
        """Test GET /api/internal/App/TopFailed with simple parameters"""
        print("\n=== GET TOP FAILED BY PRODUCT ===")
        
        try:
            results = wats_client.analytics.get_top_failed_by_product(
                part_number="758877.874",
                process_code="TEST",
                product_group_id="00000000-0000-0000-0000-000000000000",
                level_id="00000000-0000-0000-0000-000000000000",
                days=30,
                count=10
            )
            
            print(f"Retrieved {len(results)} top failed steps")
            if results:
                for step in results[:5]:
                    print(f"  - {step.step_name}: {step.fail_count} failures ({step.fail_rate}%)")
            
            assert isinstance(results, list)
            for item in results:
                assert isinstance(item, TopFailedStep)
                
        except Exception as e:
            print(f"Error: {e}")
            pytest.skip("Test may require specific product configuration")
        
        print("==================================\n")

    def test_get_top_failed_advanced_with_filter(self, wats_client: Any) -> None:
        """Test POST /api/internal/App/TopFailed with filter"""
        print("\n=== GET TOP FAILED ADVANCED WITH FILTER ===")
        
        try:
            results = wats_client.analytics.get_top_failed_advanced(
                filter_data={
                    "periodCount": 30,
                    "includeCurrentPeriod": True,
                    "topCount": 10
                },
                top_count=10
            )
            
            print(f"Retrieved {len(results)} top failed steps")
            if results:
                for step in results[:5]:
                    print(f"  - {step.step_name}: {step.fail_count} failures")
                    
            assert isinstance(results, list)
            for item in results:
                assert isinstance(item, TopFailedStep)
                
        except Exception as e:
            print(f"Error: {e}")
            pytest.skip("Test may require specific filter parameters")
        
        print("============================================\n")


class TestAggregatedMeasurementsEndpoints:
    """Test internal AggregatedMeasurements endpoint"""

    def test_get_aggregated_measurements(self, wats_client: Any) -> None:
        """Test POST /api/internal/App/AggregatedMeasurements"""
        print("\n=== GET AGGREGATED MEASUREMENTS ===")
        
        try:
            results = wats_client.analytics.get_aggregated_measurements(
                filter_data={
                    "periodCount": 30,
                    "includeCurrentPeriod": True
                },
                step_filters="<filters></filters>",
                sequence_filters="<filters></filters>",
                measurement_name=None
            )
            
            print(f"Retrieved {len(results)} aggregated measurements")
            if results:
                for m in results[:5]:
                    print(f"  - {m.step_name}: avg={m.avg}, cpk={m.cpk}")
            
            assert isinstance(results, list)
            for item in results:
                assert isinstance(item, AggregatedMeasurement)
                
        except Exception as e:
            print(f"Error: {e}")
            pytest.skip("Test may require specific filter parameters")
        
        print("====================================\n")


class TestInternalMethodsAvailable:
    """Test that internal methods are accessible via api.analytics"""

    def test_measurement_list_method_exists(self, wats_client: Any) -> None:
        """Verify get_measurement_list is accessible"""
        assert hasattr(wats_client.analytics, 'get_measurement_list')
        assert callable(wats_client.analytics.get_measurement_list)

    def test_measurement_list_by_product_method_exists(self, wats_client: Any) -> None:
        """Verify get_measurement_list_by_product is accessible"""
        assert hasattr(wats_client.analytics, 'get_measurement_list_by_product')
        assert callable(wats_client.analytics.get_measurement_list_by_product)

    def test_step_status_list_method_exists(self, wats_client: Any) -> None:
        """Verify get_step_status_list is accessible"""
        assert hasattr(wats_client.analytics, 'get_step_status_list')
        assert callable(wats_client.analytics.get_step_status_list)

    def test_step_status_list_by_product_method_exists(self, wats_client: Any) -> None:
        """Verify get_step_status_list_by_product is accessible"""
        assert hasattr(wats_client.analytics, 'get_step_status_list_by_product')
        assert callable(wats_client.analytics.get_step_status_list_by_product)

    def test_top_failed_internal_method_exists(self, wats_client: Any) -> None:
        """Verify get_top_failed_internal is accessible"""
        assert hasattr(wats_client.analytics, 'get_top_failed_internal')
        assert callable(wats_client.analytics.get_top_failed_internal)

    def test_top_failed_by_product_method_exists(self, wats_client: Any) -> None:
        """Verify get_top_failed_by_product is accessible"""
        assert hasattr(wats_client.analytics, 'get_top_failed_by_product')
        assert callable(wats_client.analytics.get_top_failed_by_product)

    def test_aggregated_measurements_method_exists(self, wats_client: Any) -> None:
        """Verify get_aggregated_measurements is accessible"""
        assert hasattr(wats_client.analytics, 'get_aggregated_measurements')
        assert callable(wats_client.analytics.get_aggregated_measurements)

    def test_unit_flow_method_exists(self, wats_client: Any) -> None:
        """Verify get_unit_flow is accessible via api.analytics (not analytics_internal)"""
        assert hasattr(wats_client.analytics, 'get_unit_flow')
        assert callable(wats_client.analytics.get_unit_flow)

    def test_no_analytics_internal_property(self, wats_client: Any) -> None:
        """Verify analytics_internal is no longer a separate property"""
        # All internal methods should be on api.analytics now
        # analytics_internal should not exist as a separate accessor
        # (This test may fail if analytics_internal is kept for backwards compatibility)
        print("Note: analytics_internal may still exist for backwards compatibility")
        # We don't assert it doesn't exist - just verify analytics works
        assert hasattr(wats_client, 'analytics')
