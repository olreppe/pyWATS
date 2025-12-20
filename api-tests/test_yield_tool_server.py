"""
Server integration tests for yield tool.

These tests actually query the WATS server to verify:
1. The yield tool gets data correctly
2. "Top runners" queries work
3. Default 30-day window is applied
4. Tool description priority guides correct tool selection

Run with:
    pytest api-tests/test_yield_tool_server.py -v -s
"""
from typing import Any
import pytest
from datetime import datetime, timedelta
from pywats import pyWATS


# =============================================================================
# Server Configuration
# =============================================================================

# NOTE: This token is for ANALYTICS/AGENT TESTING ONLY.
# It has read-only access to yield/statistics endpoints.
# It CANNOT be used for general API operations or any write operations.
WATS_SERVER = "https://live.wats.com"
WATS_TOKEN = "QWdlbnREZWJ1ZzpwbTJQZDA4UTY3SjU3NnpyNWImMkwyUHRXOUhCUjI="


@pytest.fixture(scope="module")
def wats_client() -> pyWATS:
    """Create WATS client with live server credentials."""
    return pyWATS(base_url=WATS_SERVER, token=WATS_TOKEN)


class TestYieldToolServerIntegration:
    """Test yield tool against actual server."""

    def test_top_runners_by_product_last_30_days(self, wats_client: Any) -> None:
        """
        Test "Top 10 runners by partnumber and testoperation".
        
        This tests the primary use case that should go to analyze_yield:
        - perspective="by product" gives products grouped by part number
        - Default 30 days is used
        - Results sorted by volume (unit_count)
        """
        print("\n=== TOP RUNNERS BY PRODUCT (LAST 30 DAYS) ===")
        
        from pywats_agent.tools.yield_tool import YieldAnalysisTool, YieldFilter
        
        tool = YieldAnalysisTool(wats_client)
        
        # This is what should be called for "Top 10 runners"
        filter_obj = YieldFilter(
            perspective="by product",  # Group by part number
            days=30,  # Default 30 days
        )
        
        result = tool.analyze(filter_obj)
        
        print(f"Success: {result.success}")
        print(f"Summary:\n{result.summary}")
        
        # Should succeed
        assert result.success, f"Tool failed: {result.error}"
        
        # Should have data
        assert result.data is not None
        
        # Should have products in data
        if isinstance(result.data, list) and len(result.data) > 0:
            print(f"\nTop runners (by volume):")
            # Sort by unit_count (volume)
            sorted_data = sorted(result.data, key=lambda x: x.get('unit_count', 0), reverse=True)
            for i, item in enumerate(sorted_data[:10], 1):
                part = item.get('part_number', item.get('partNumber', 'Unknown'))
                units = item.get('unit_count', 0)
                fpy = item.get('fpy', item.get('yield', 0))
                print(f"  {i}. {part}: {units:,} units, FPY={fpy:.1f}%")
        
        print("==============================================\n")

    def test_top_runners_by_product_and_operation(self, wats_client: Any) -> None:
        """
        Test "Top 10 runners by partnumber and testoperation".
        
        Groups data by both part number AND test operation.
        This shows top runners per process.
        """
        print("\n=== TOP RUNNERS BY PRODUCT AND OPERATION ===")
        
        from pywats_agent.tools.yield_tool import YieldAnalysisTool, YieldFilter
        
        tool = YieldAnalysisTool(wats_client)
        
        # Use custom dimensions to group by both
        filter_obj = YieldFilter(
            dimensions="partNumber;testOperation",  # Both dimensions
            days=30,
        )
        
        result = tool.analyze(filter_obj)
        
        print(f"Success: {result.success}")
        print(f"Summary:\n{result.summary}")
        
        assert result.success, f"Tool failed: {result.error}"
        assert result.data is not None
        
        if isinstance(result.data, list) and len(result.data) > 0:
            print(f"\nTop runners by product/operation (by volume):")
            sorted_data = sorted(result.data, key=lambda x: x.get('unit_count', 0), reverse=True)
            for i, item in enumerate(sorted_data[:10], 1):
                part = item.get('part_number', item.get('partNumber', 'Unknown'))
                op = item.get('test_operation', item.get('testOperation', 'Unknown'))
                units = item.get('unit_count', 0)
                fpy = item.get('fpy', item.get('yield', 0))
                print(f"  {i}. {part} / {op}: {units:,} units, FPY={fpy:.1f}%")
        
        print("=============================================\n")

    def test_default_30_days_applied(self, wats_client: Any) -> None:
        """
        Test that default 30 days is correctly applied.
        
        The YieldFilter defaults to days=30, matching WATS server behavior.
        """
        print("\n=== VERIFY DEFAULT 30 DAYS ===")
        
        from pywats_agent.tools.yield_tool import YieldFilter, build_wats_filter
        
        # Create filter with NO explicit days
        filter_obj = YieldFilter(
            perspective="by product"
        )
        
        # Verify default
        assert filter_obj.days == 30, "Default days should be 30"
        
        # Build WATS filter
        wats_params = build_wats_filter(filter_obj)
        
        # Check date range is approximately 30 days
        if "date_from" in wats_params and "date_to" in wats_params:
            date_from = wats_params["date_from"]
            date_to = wats_params["date_to"]
            delta = (date_to - date_from).days
            print(f"Date range: {date_from} to {date_to} ({delta} days)")
            assert 29 <= delta <= 31, f"Expected ~30 days, got {delta}"
        
        print("==============================\n")

    def test_yield_by_station(self, wats_client: Any) -> None:
        """
        Test "Which station is best/worst?" query.
        
        Uses perspective="by station" to compare stations.
        """
        print("\n=== YIELD BY STATION ===")
        
        from pywats_agent.tools.yield_tool import YieldAnalysisTool, YieldFilter
        
        tool = YieldAnalysisTool(wats_client)
        
        filter_obj = YieldFilter(
            perspective="by station",
            days=30,
        )
        
        result = tool.analyze(filter_obj)
        
        print(f"Success: {result.success}")
        print(f"Summary:\n{result.summary}")
        
        assert result.success, f"Tool failed: {result.error}"
        
        if isinstance(result.data, list) and len(result.data) > 0:
            # Sort by FPY to find best/worst
            sorted_by_fpy = sorted(
                [d for d in result.data if d.get('unit_count', 0) >= 10],  # Min volume
                key=lambda x: x.get('fpy', x.get('yield', 0)),
                reverse=True
            )
            
            print(f"\nBest performing stations (min 10 units):")
            for item in sorted_by_fpy[:3]:
                station = item.get('station_name', item.get('stationName', 'Unknown'))
                units = item.get('unit_count', 0)
                fpy = item.get('fpy', item.get('yield', 0))
                print(f"  ✅ {station}: FPY={fpy:.1f}% ({units:,} units)")
            
            print(f"\nWorst performing stations (min 10 units):")
            for item in sorted_by_fpy[-3:]:
                station = item.get('station_name', item.get('stationName', 'Unknown'))
                units = item.get('unit_count', 0)
                fpy = item.get('fpy', item.get('yield', 0))
                print(f"  ⚠️  {station}: FPY={fpy:.1f}% ({units:,} units)")
        
        print("========================\n")

    def test_yield_trend_daily(self, wats_client: Any) -> None:
        """
        Test "What's the yield trend?" query.
        
        Uses perspective="daily" to show yield over time.
        """
        print("\n=== YIELD TREND (DAILY) ===")
        
        from pywats_agent.tools.yield_tool import YieldAnalysisTool, YieldFilter
        
        tool = YieldAnalysisTool(wats_client)
        
        filter_obj = YieldFilter(
            perspective="daily",
            days=14,  # Last 2 weeks
        )
        
        result = tool.analyze(filter_obj)
        
        print(f"Success: {result.success}")
        print(f"Summary:\n{result.summary}")
        
        assert result.success, f"Tool failed: {result.error}"
        
        if isinstance(result.data, list) and len(result.data) > 0:
            print(f"\nDaily yield trend:")
            for item in result.data[-7:]:  # Last 7 days
                period = item.get('period', item.get('date', 'Unknown'))
                units = item.get('unit_count', 0)
                fpy = item.get('fpy', item.get('yield', 0))
                print(f"  {period}: FPY={fpy:.1f}% ({units:,} units)")
        
        print("===========================\n")


class TestToolSelectionPriority:
    """Test that tool descriptions correctly prioritize analyze_yield."""
    
    def test_analyze_yield_description_has_primary_marker(self) -> None:
        """Test that analyze_yield description starts with PRIMARY TOOL."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        desc = YieldAnalysisTool.description
        
        # Should start with PRIMARY TOOL
        assert "PRIMARY TOOL" in desc, "Description should contain PRIMARY TOOL"
        assert desc.strip().startswith("PRIMARY TOOL"), \
            "Description should START with PRIMARY TOOL"
        
        # Should mention key use cases
        assert "top runner" in desc.lower(), "Should mention top runners"
        assert "best/worst" in desc.lower() or "best" in desc.lower(), \
            "Should mention best/worst performers"
        assert "trend" in desc.lower(), "Should mention trends"
        assert "volume" in desc.lower(), "Should mention volume"
    
    def test_test_step_tool_description_has_secondary_marker(self) -> None:
        """Test that test step tool is marked as SECONDARY."""
        from pywats_agent.tools.test_step_analysis_tool import TestStepAnalysisTool
        
        desc = TestStepAnalysisTool.description
        
        # Should have SECONDARY marker
        assert "SECONDARY" in desc, "Should be marked as SECONDARY TOOL"
        
        # Should redirect yield queries
        assert "analyze_yield" in desc, "Should mention analyze_yield"
    
    def test_deviation_tool_description_has_specialized_marker(self) -> None:
        """Test that deviation tool is marked as SPECIALIZED."""
        from pywats_agent.tools.yield_pkg.deviation_tool import YieldDeviationTool
        
        desc = YieldDeviationTool.description
        
        # Should have SPECIALIZED marker
        assert "SPECIALIZED" in desc or "after analyze_yield" in desc.lower(), \
            "Should be marked as specialized drill-down"
        
        # Should have DO NOT USE section
        assert "DO NOT USE" in desc or "❌" in desc, \
            "Should list queries NOT to use this for"
    
    def test_root_cause_tool_description_has_investigation_marker(self) -> None:
        """Test that root cause tool is marked for INVESTIGATION."""
        from pywats_agent.tools.root_cause.analysis_tool import RootCauseAnalysisTool
        
        desc = RootCauseAnalysisTool.description
        
        # Should have INVESTIGATION marker
        assert "INVESTIGATION" in desc, "Should be marked as INVESTIGATION TOOL"
        
        # Should redirect simple yield queries
        assert "analyze_yield" in desc, "Should mention analyze_yield for simple queries"


class TestYieldToolTopRunnersQuery:
    """
    Test the exact query: "Top 10 runners by partnumber and testoperation"
    
    This query should:
    1. Use analyze_yield (not other tools)
    2. Default to 30 days
    3. Group by partNumber;testOperation
    4. Return volume-sorted results
    """
    
    def test_top_runners_query_structure(self, wats_client: Any) -> None:
        """Test the exact structure for top runners query."""
        print("\n=== EXACT TOP RUNNERS QUERY ===")
        
        from pywats_agent.tools.yield_tool import YieldAnalysisTool, YieldFilter
        
        tool = YieldAnalysisTool(wats_client)
        
        # This is exactly what should be generated for:
        # "Top 10 runners by partnumber and testoperation"
        filter_obj = YieldFilter(
            dimensions="partNumber;testOperation",  # By part number AND test operation
            days=30,  # Default 30 days
        )
        
        result = tool.analyze(filter_obj)
        
        assert result.success, f"Query failed: {result.error}"
        assert result.data is not None, "Should return data"
        
        # Results should be sortable by volume
        if isinstance(result.data, list):
            print(f"Retrieved {len(result.data)} product/operation combinations")
            
            # Sort by volume and show top 10
            sorted_data = sorted(
                result.data, 
                key=lambda x: x.get('unit_count', 0), 
                reverse=True
            )[:10]
            
            print("\n📊 TOP 10 RUNNERS BY PART NUMBER AND TEST OPERATION:")
            print("-" * 60)
            for i, item in enumerate(sorted_data, 1):
                part = item.get('part_number', item.get('partNumber', 'Unknown'))
                op = item.get('test_operation', item.get('testOperation', 'Unknown'))
                units = item.get('unit_count', 0)
                fpy = item.get('fpy', item.get('yield', 0))
                print(f"{i:2}. {part:30} | {op:15} | {units:>8,} units | FPY {fpy:>5.1f}%")
            print("-" * 60)
        
        print("================================\n")
    
    def test_top_runners_uses_yield_tool_not_step_tool(self) -> None:
        """Verify "top runners" query maps to yield tool, not step tool."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        from pywats_agent.tools.test_step_analysis_tool import TestStepAnalysisTool
        
        yield_desc = YieldAnalysisTool.description.lower()
        step_desc = TestStepAnalysisTool.description.lower()
        
        # "top runners" should be in yield tool description
        assert "top runner" in yield_desc, "Yield tool should mention top runners"
        
        # "top runners" should NOT be in step tool description as a use case
        # (step tool should redirect to yield tool)
        assert "do not use" in step_desc or "analyze_yield" in step_desc, \
            "Step tool should redirect yield-related queries"
    
    def test_verify_default_30_days_in_schema(self) -> None:
        """Verify parameter schema shows 30 days default."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        schema = YieldAnalysisTool.get_parameters_schema()
        
        days_schema = schema["properties"]["days"]
        assert days_schema.get("default") == 30, \
            "Default days should be 30 in schema"
