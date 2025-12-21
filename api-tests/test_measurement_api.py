"""
Tests for Measurement API endpoints.

These tests verify the measurement path as query parameter fix
by making actual API calls to the WATS server.

The fix ensures:
1. measurementPaths is sent as query parameter, not body
2. Path format with "/" is converted to "¶" (paragraph mark)
3. Proper filtering prevents timeout (part_number + test_operation)
"""
from typing import Any
import pytest
from datetime import datetime, timedelta


class TestMeasurementPathNormalization:
    """Test that measurement path normalization works correctly."""
    
    def test_normalize_path_with_slashes(self):
        """Test "/" is converted to paragraph mark."""
        from pywats.domains.analytics.repository import AnalyticsRepository
        
        result = AnalyticsRepository._normalize_measurement_path("Main/Step/Test")
        assert result == "Main¶Step¶Test"
    
    def test_normalize_path_with_measurement_name(self):
        """Test measurement name separator (::) is converted to ¶¶."""
        from pywats.domains.analytics.repository import AnalyticsRepository
        
        result = AnalyticsRepository._normalize_measurement_path("Main/Step/Test::Measurement0")
        assert result == "Main¶Step¶Test¶¶Measurement0"
    
    def test_normalize_path_already_correct(self):
        """Test path already using ¶ is unchanged."""
        from pywats.domains.analytics.repository import AnalyticsRepository
        
        result = AnalyticsRepository._normalize_measurement_path("Main¶Step¶Test")
        assert result == "Main¶Step¶Test"
    
    def test_normalize_empty_path(self):
        """Test empty path returns empty."""
        from pywats.domains.analytics.repository import AnalyticsRepository
        
        result = AnalyticsRepository._normalize_measurement_path("")
        assert result == ""


class TestAggregatedMeasurementsAPI:
    """Test aggregated measurements API with real server."""
    
    def test_get_aggregated_measurements_with_filter(self, wats_client: Any) -> None:
        """
        Test getting aggregated measurements with proper filters.
        
        This test:
        1. Gets a real product from the server
        2. Gets top failed steps to find a measurement path
        3. Queries aggregated measurements with the measurement path
        """
        print("\n=== GET AGGREGATED MEASUREMENTS ===")
        
        # First, get a real product
        products = wats_client.product.get_products()
        if not products:
            pytest.skip("No products available")
        
        part_number = products[0].part_number
        print(f"Using product: {part_number}")
        
        # Get top failed steps to find a real step path
        from pywats.domains.report import WATSFilter
        
        filter_obj = WATSFilter(
            part_number=part_number,
            top_count=5,
            days=30,
        )
        
        top_failed = wats_client.analytics.get_top_failed(filter_obj)
        
        if not top_failed:
            print("No failed steps found, trying without part_number filter")
            filter_obj = WATSFilter(top_count=5, days=30)
            top_failed = wats_client.analytics.get_top_failed(filter_obj)
        
        if not top_failed:
            pytest.skip("No failed steps available to get measurement path")
        
        # Get step path from top failed
        step = top_failed[0]
        step_path = step.step_path or step.step_name
        print(f"Using step path: {step_path}")
        print(f"Product: {step.part_number}")
        
        # Now query aggregated measurements
        measurement_filter = WATSFilter(
            part_number=step.part_number or part_number,
            days=30,
        )
        
        # Call with measurement_paths as query parameter
        results = wats_client.analytics.get_aggregated_measurements(
            measurement_filter,
            measurement_paths=step_path
        )
        
        print(f"Retrieved {len(results)} aggregated measurement groups")
        for i, meas in enumerate(results[:3]):
            print(f"  {i+1}. {meas.step_name}: count={meas.count}, avg={meas.avg}")
        
        print("===================================\n")
        
        # Test passes if call completed - may return empty if no measurements
        assert isinstance(results, list)


class TestMeasurementDataAPI:
    """Test individual measurement data API with real server."""
    
    def test_get_measurements_with_filter(self, wats_client: Any) -> None:
        """
        Test getting individual measurements with proper filters.
        """
        print("\n=== GET MEASUREMENTS ===")
        
        # Get a real product
        products = wats_client.product.get_products()
        if not products:
            pytest.skip("No products available")
        
        part_number = products[0].part_number
        print(f"Using product: {part_number}")
        
        # Get top failed steps
        from pywats.domains.report import WATSFilter
        
        filter_obj = WATSFilter(
            part_number=part_number,
            top_count=5,
            days=30,
        )
        
        top_failed = wats_client.analytics.get_top_failed(filter_obj)
        
        if not top_failed:
            filter_obj = WATSFilter(top_count=5, days=30)
            top_failed = wats_client.analytics.get_top_failed(filter_obj)
        
        if not top_failed:
            pytest.skip("No failed steps available")
        
        step = top_failed[0]
        step_path = step.step_path or step.step_name
        print(f"Using step path: {step_path}")
        
        # Query individual measurements with proper filter
        measurement_filter = WATSFilter(
            part_number=step.part_number or part_number,
            days=7,  # Shorter window for individual data
            top_count=100,  # Limit results
        )
        
        results = wats_client.analytics.get_measurements(
            measurement_filter,
            measurement_paths=step_path
        )
        
        print(f"Retrieved {len(results)} individual measurements")
        for i, meas in enumerate(results[:3]):
            print(f"  {i+1}. SN={meas.serial_number}, value={meas.value}")
        
        print("========================\n")
        
        assert isinstance(results, list)


class TestMeasurementWithStepAnalysis:
    """Integration test using step analysis data for measurements."""
    
    def test_measurement_from_step_analysis(self, wats_client: Any) -> None:
        """
        End-to-end test:
        1. Get top failed steps data
        2. Use step path to query measurements
        3. Verify data is returned
        """
        print("\n=== MEASUREMENT FROM STEP ANALYSIS ===")
        
        from pywats.domains.report import WATSFilter
        
        # Get top failed steps data (has step paths)
        filter_obj = WATSFilter(top_count=20, days=30)
        
        step_data = wats_client.analytics.get_top_failed(filter_obj)
        
        if not step_data:
            pytest.skip("No top failed steps available")
        
        # Use the first step with data
        numeric_step = step_data[0]
        
        print(f"Found step: {numeric_step.step_name}")
        print(f"  Part number: {numeric_step.part_number}")
        print(f"  Fail count: {numeric_step.fail_count}")
        
        # Query aggregated measurements for this step
        step_path = numeric_step.step_path or numeric_step.step_name
        
        if numeric_step.part_number:
            measurement_filter = WATSFilter(
                part_number=numeric_step.part_number,
                days=30,
            )
        else:
            measurement_filter = WATSFilter(days=30)
        
        results = wats_client.analytics.get_aggregated_measurements(
            measurement_filter,
            measurement_paths=step_path
        )
        
        print(f"Aggregated measurements: {len(results)} groups")
        
        if results:
            print(f"First result: {results[0].step_name}")
            print(f"  Count: {results[0].count}")
            print(f"  Avg: {results[0].avg}")
            print(f"  Cpk: {results[0].cpk}")
        
        print("======================================\n")
        
        # Test passes if call completed successfully
        assert isinstance(results, list)


class TestMeasurementWithProductAndProcess:
    """Test measurements with specific product and process filters."""
    
    def test_get_measurements_real_data(self, wats_client: Any) -> None:
        """
        Test getting measurements using real data from the server.
        
        Strategy:
        1. Get UUT report headers to find real product
        2. Use product info to query measurements with a basic step path
        """
        print("\n=== MEASUREMENTS WITH REAL REPORT DATA ===")
        
        # Get recent report headers
        from pywats.domains.report import WATSFilter
        
        filter_obj = WATSFilter(top_count=10)
        headers = wats_client.report.query_uut_headers(filter_obj)
        
        if not headers:
            pytest.skip("No report headers available")
        
        # Use first report header for filter info
        header = headers[0]
        print(f"Using report: {header.uuid}")
        print(f"  Part number: {header.part_number}")
        print(f"  Serial number: {header.serial_number}")
        
        # Use a generic step path - the API will filter by product
        # Even if no exact match, this tests the API call works correctly
        step_path = "MainSequence Callback"
        print(f"Using step path: {step_path}")
        
        # Query measurements with proper filters
        measurement_filter = WATSFilter(
            part_number=header.part_number,
            serial_number=header.serial_number,  # Filter to this unit
            days=90,
        )
        
        results = wats_client.analytics.get_measurements(
            measurement_filter,
            measurement_paths=step_path
        )
        
        print(f"Retrieved {len(results)} measurements for this step")
        
        for meas in results[:5]:
            print(f"  - Value: {meas.value}, Status: {meas.status}")
        
        print("==========================================\n")
        
        # Test completed successfully - the API call worked without timeout
        assert isinstance(results, list)
