"""
Tests for analytics module - statistics and KPI endpoints

These tests make actual API calls to the WATS server.
"""
from typing import Any
import pytest


class TestAnalyticsVersion:
    """Test analytics version endpoint"""

    def test_get_version(self, wats_client: Any) -> None:
        """Test getting API version"""
        print("\n=== GET VERSION ===")
        
        version = wats_client.analytics.get_version()
        
        print(f"API Version: {version}")
        print("===================\n")
        
        assert version is not None


class TestProductGroups:
    """Test product group retrieval"""

    def test_get_product_groups(self, wats_client: Any) -> None:
        """Test getting product groups"""
        print("\n=== GET PRODUCT GROUPS ===")
        
        groups = wats_client.analytics.get_product_groups()
        
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
        
        processes = wats_client.analytics.get_processes()
        
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
        
        levels = wats_client.analytics.get_levels()
        
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
        
        summary = wats_client.analytics.get_yield_summary(part_number=part_number, days=7)
        
        print(f"Yield summary: {summary}")
        print("=========================\n")

    def test_get_dynamic_yield(self, wats_client: Any) -> None:
        """Test getting dynamic yield data"""
        print("\n=== GET DYNAMIC YIELD ===")
        
        # Use minimal filter
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=10)
        
        result = wats_client.analytics.get_dynamic_yield(filter_obj)
        
        print(f"Dynamic yield result: {result}")
        print("=========================\n")

    def test_get_volume_yield(self, wats_client: Any) -> None:
        """Test getting volume yield"""
        print("\n=== GET VOLUME YIELD ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=10)
        
        result = wats_client.analytics.get_volume_yield(filter_obj)
        
        print(f"Volume yield: {result}")
        print("========================\n")

    def test_dynamic_yield_1_day_by_part_number(self, wats_client: Any) -> None:
        """Test dynamic yield for 1 day with part_number dimension only - no other filters"""
        print("\n=== DYNAMIC YIELD - 1 DAY BY PART NUMBER ===")
        
        from pywats.domains.report import WATSFilter, DateGrouping
        
        # Only period_count, date_grouping, and dimensions - no other filters
        filter_obj = WATSFilter(
            period_count=1,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber"
        )
        
        print(f"Filter payload: {filter_obj.model_dump(by_alias=True, exclude_none=True)}")
        
        result = wats_client.analytics.get_dynamic_yield(filter_obj)
        
        print(f"Result type: {type(result)}")
        if isinstance(result, list):
            print(f"Retrieved {len(result)} rows")
            for idx, row in enumerate(result[:5]):
                print(f"  Row {idx+1}: {row}")
        else:
            print(f"Result: {result}")
        print("============================================\n")
        
        assert result is not None
        assert isinstance(result, list), "Result should be a list"

    def test_dynamic_yield_7_days_by_part_number(self, wats_client: Any) -> None:
        """Test dynamic yield for 7 days with part_number dimension only - no other filters"""
        print("\n=== DYNAMIC YIELD - 7 DAYS BY PART NUMBER ===")
        
        from pywats.domains.report import WATSFilter, DateGrouping
        
        # Only period_count, date_grouping, and dimensions - no other filters
        filter_obj = WATSFilter(
            period_count=7,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber"
        )
        
        print(f"Filter payload: {filter_obj.model_dump(by_alias=True, exclude_none=True)}")
        
        result = wats_client.analytics.get_dynamic_yield(filter_obj)
        
        print(f"Result type: {type(result)}")
        if isinstance(result, list):
            print(f"Retrieved {len(result)} rows")
            for idx, row in enumerate(result[:5]):
                print(f"  Row {idx+1}: {row}")
        else:
            print(f"Result: {result}")
        print("=============================================\n")
        
        assert result is not None
        assert isinstance(result, list), "Result should be a list"

    def test_dynamic_yield_30_days_by_part_number(self, wats_client: Any) -> None:
        """Test dynamic yield for 30 days with part_number dimension only - no other filters"""
        print("\n=== DYNAMIC YIELD - 30 DAYS BY PART NUMBER ===")
        
        from pywats.domains.report import WATSFilter, DateGrouping
        
        # Only period_count, date_grouping, and dimensions - no other filters
        filter_obj = WATSFilter(
            period_count=30,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber"
        )
        
        print(f"Filter payload: {filter_obj.model_dump(by_alias=True, exclude_none=True)}")
        
        result = wats_client.analytics.get_dynamic_yield(filter_obj)
        
        print(f"Result type: {type(result)}")
        if isinstance(result, list):
            print(f"Retrieved {len(result)} rows")
            for idx, row in enumerate(result[:5]):
                print(f"  Row {idx+1}: {row}")
        else:
            print(f"Result: {result}")
        print("==============================================\n")
        
        assert result is not None
        assert isinstance(result, list), "Result should be a list"

    def test_dynamic_yield_comparison_across_periods(self, wats_client: Any) -> None:
        """Test and compare dynamic yield across different time periods (1, 7, 30 days)"""
        print("\n=== DYNAMIC YIELD - PERIOD COMPARISON ===")
        
        from pywats.domains.report import WATSFilter, DateGrouping
        
        periods = [1, 7, 30]
        results = {}
        
        for period_count in periods:
            # Only period_count, date_grouping, and dimensions - no other filters
            filter_obj = WATSFilter(
                period_count=period_count,
                date_grouping=DateGrouping.DAY,
                dimensions="partNumber"
            )
            result = wats_client.analytics.get_dynamic_yield(filter_obj)
            results[period_count] = result
            
            if isinstance(result, list):
                print(f"{period_count} day(s): {len(result)} rows")
            else:
                print(f"{period_count} day(s): {result}")
        
        print("\nComparison summary:")
        for period_count, result in results.items():
            count = len(result) if isinstance(result, list) else "N/A"
            print(f"  {period_count:2d} day(s): {count} rows")
        
        print("==========================================\n")
        
        # Verify all periods returned data
        for period_count, result in results.items():
            assert result is not None, f"No result for {period_count} days"
            assert isinstance(result, list), f"Result for {period_count} days should be a list"


class TestTopFailed:
    """Test top failed analysis"""

    def test_get_top_failed(self, wats_client: Any) -> None:
        """Test getting top failed steps"""
        print("\n=== GET TOP FAILED ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=10)
        
        result = wats_client.analytics.get_top_failed(filter_obj)
        
        print(f"Top failed: {result}")
        print("======================\n")


class TestReportRetrieval:
    """Test report data retrieval through app service"""

    def test_get_uut_reports(self, wats_client: Any) -> None:
        """Test getting UUT reports through app service"""
        print("\n=== GET UUT REPORTS ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=5)
        
        reports = wats_client.analytics.get_uut_reports(filter_obj)
        
        print(f"Retrieved {len(reports)} UUT reports")
        print("=======================\n")
        
        assert isinstance(reports, list)

    def test_get_uur_reports(self, wats_client: Any) -> None:
        """Test getting UUR reports through app service"""
        print("\n=== GET UUR REPORTS ===")
        
        from pywats.domains.report import WATSFilter
        filter_obj = WATSFilter(top_count=5)
        
        reports = wats_client.analytics.get_uur_reports(filter_obj)
        
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
            history = wats_client.analytics.get_serial_number_history(serial_number)
            print(f"History entries: {len(history) if history else 0}")
        except ServerError as e:
            # Server may not support this endpoint or have data
            print(f"Server error (known issue): {e}")
            history = []
        
        print("=================================\n")


class TestAlarmLogs:
    """Test alarm and notification log retrieval (internal API)"""

    def test_get_alarm_logs(self, wats_client: Any) -> None:
        """Test getting all alarm logs"""
        print("\n=== GET ALARM LOGS ===")
        
        alarms = wats_client.analytics.get_alarm_logs(top_count=20)
        
        print(f"Retrieved {len(alarms)} alarm logs")
        for alarm in alarms[:5]:
            print(f"  - [{alarm.alarm_type_name}] {alarm.name}")
            print(f"    Time: {alarm.log_date}")
            if alarm.part_number:
                print(f"    Product: {alarm.part_number}")
        print("======================\n")
        
        assert isinstance(alarms, list)

    def test_get_alarm_logs_by_type(self, wats_client: Any) -> None:
        """Test getting alarm logs filtered by type"""
        from pywats import AlarmType
        
        print("\n=== GET ALARM LOGS BY TYPE ===")
        
        # Test filtering by yield alarms
        yield_alarms = wats_client.analytics.get_alarm_logs(
            alarm_type=AlarmType.YIELD_VOLUME,
            top_count=10
        )
        
        print(f"Retrieved {len(yield_alarms)} yield alarms")
        for alarm in yield_alarms[:3]:
            print(f"  - {alarm.name}")
            if alarm.fpy is not None:
                print(f"    FPY: {alarm.fpy_percent:.1f}%")
            if alarm.fpy_trend is not None:
                print(f"    Trend: {alarm.fpy_trend_percent:+.1f}%")
        
        # Verify all returned alarms are of the correct type
        for alarm in yield_alarms:
            assert alarm.type == AlarmType.YIELD_VOLUME, f"Expected YIELD_VOLUME, got {alarm.type}"
        
        print("==============================\n")

    def test_get_alarm_logs_with_date_filter(self, wats_client: Any) -> None:
        """Test getting alarm logs with date range filter"""
        from datetime import datetime, timedelta
        
        print("\n=== GET ALARM LOGS WITH DATE FILTER ===")
        
        date_from = datetime.now() - timedelta(days=30)
        date_to = datetime.now()
        
        alarms = wats_client.analytics.get_alarm_logs(
            date_from=date_from,
            date_to=date_to,
            top_count=20
        )
        
        print(f"Retrieved {len(alarms)} alarms from last 30 days")
        
        # Count by type
        type_counts: dict = {}
        for alarm in alarms:
            type_name = alarm.alarm_type_name
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        print("Alarm counts by type:")
        for type_name, count in sorted(type_counts.items()):
            print(f"  - {type_name}: {count}")
        
        print("========================================\n")
        
        assert isinstance(alarms, list)

    def test_alarm_log_model_properties(self, wats_client: Any) -> None:
        """Test AlarmLog model computed properties"""
        from pywats import AlarmType
        
        print("\n=== TEST ALARM LOG PROPERTIES ===")
        
        alarms = wats_client.analytics.get_alarm_logs(top_count=50)
        
        if not alarms:
            pytest.skip("No alarm logs available")
        
        # Test alarm_type_name property
        for alarm in alarms:
            assert alarm.alarm_type_name is not None
            assert "Unknown" not in alarm.alarm_type_name or alarm.type not in [1, 2, 3, 4, 5]
        
        # Test yield alarm percentage properties
        yield_alarms = [a for a in alarms if a.type == AlarmType.YIELD_VOLUME]
        if yield_alarms:
            alarm = yield_alarms[0]
            print(f"Yield alarm: {alarm.name}")
            if alarm.fpy is not None:
                print(f"  FPY raw: {alarm.fpy}")
                print(f"  FPY percent: {alarm.fpy_percent:.1f}%")
                assert alarm.fpy_percent == alarm.fpy * 100
            if alarm.fpy_trend is not None:
                print(f"  FPY trend raw: {alarm.fpy_trend}")
                print(f"  FPY trend percent: {alarm.fpy_trend_percent:+.1f}%")
                assert alarm.fpy_trend_percent == alarm.fpy_trend * 100
        
        print("==================================\n")
