"""Tests for the yield analysis tool."""
import pytest
from pywats_agent.tools.yield_tool import (
    AnalysisPerspective,
    PERSPECTIVE_ALIASES,
    PERSPECTIVE_TO_DIMENSIONS,
    resolve_perspective,
    YieldFilter,
    build_wats_filter,
    get_available_perspectives,
)


class TestPerspectiveResolution:
    """Tests for perspective resolution from natural language."""

    def test_resolve_exact_enum_value(self):
        """Direct enum values should resolve."""
        assert resolve_perspective("trend") == AnalysisPerspective.TREND
        assert resolve_perspective("daily") == AnalysisPerspective.DAILY
        assert resolve_perspective("by_station") == AnalysisPerspective.BY_STATION

    def test_resolve_common_aliases(self):
        """Common natural language aliases should resolve."""
        # Station aliases
        assert resolve_perspective("by station") == AnalysisPerspective.BY_STATION
        assert resolve_perspective("per station") == AnalysisPerspective.BY_STATION
        assert resolve_perspective("compare stations") == AnalysisPerspective.BY_STATION
        assert resolve_perspective("by tester") == AnalysisPerspective.BY_STATION
        assert resolve_perspective("by equipment") == AnalysisPerspective.BY_STATION
        
    def test_resolve_time_aliases(self):
        """Time-based aliases should resolve."""
        assert resolve_perspective("over time") == AnalysisPerspective.TREND
        assert resolve_perspective("timeline") == AnalysisPerspective.TREND
        assert resolve_perspective("day by day") == AnalysisPerspective.DAILY
        assert resolve_perspective("week by week") == AnalysisPerspective.WEEKLY
        assert resolve_perspective("monthly") == AnalysisPerspective.MONTHLY
        
    def test_resolve_product_aliases(self):
        """Product-related aliases should resolve."""
        assert resolve_perspective("by product") == AnalysisPerspective.BY_PRODUCT
        assert resolve_perspective("by part number") == AnalysisPerspective.BY_PRODUCT
        assert resolve_perspective("by revision") == AnalysisPerspective.BY_REVISION
        assert resolve_perspective("by product group") == AnalysisPerspective.BY_PRODUCT_GROUP
        
    def test_resolve_combined_perspectives(self):
        """Combined perspectives should resolve."""
        assert resolve_perspective("station trend") == AnalysisPerspective.STATION_TREND
        assert resolve_perspective("product trend") == AnalysisPerspective.PRODUCT_TREND
        assert resolve_perspective("station over time") == AnalysisPerspective.STATION_TREND
        
    def test_resolve_case_insensitive(self):
        """Resolution should be case-insensitive."""
        assert resolve_perspective("BY STATION") == AnalysisPerspective.BY_STATION
        assert resolve_perspective("Trend") == AnalysisPerspective.TREND
        assert resolve_perspective("DAILY") == AnalysisPerspective.DAILY
        
    def test_resolve_with_extra_spaces(self):
        """Resolution should handle extra whitespace."""
        assert resolve_perspective("  by station  ") == AnalysisPerspective.BY_STATION
        assert resolve_perspective("trend ") == AnalysisPerspective.TREND
        
    def test_resolve_none_input(self):
        """None input should return None."""
        assert resolve_perspective(None) is None
        
    def test_resolve_empty_string(self):
        """Empty string should return None."""
        assert resolve_perspective("") is None
        
    def test_resolve_unknown_perspective(self):
        """Unknown perspectives should return None."""
        assert resolve_perspective("foobar") is None
        assert resolve_perspective("xyz123") is None


class TestPerspectiveToDimensions:
    """Tests for perspective to dimensions mapping."""
    
    def test_station_dimensions(self):
        """BY_STATION should map to stationName."""
        assert PERSPECTIVE_TO_DIMENSIONS[AnalysisPerspective.BY_STATION] == "stationName"
        
    def test_trend_dimensions(self):
        """TREND should map to period."""
        assert PERSPECTIVE_TO_DIMENSIONS[AnalysisPerspective.TREND] == "period"
        
    def test_combined_dimensions(self):
        """Combined perspectives should have multiple dimensions."""
        assert PERSPECTIVE_TO_DIMENSIONS[AnalysisPerspective.STATION_TREND] == "stationName;period"
        assert PERSPECTIVE_TO_DIMENSIONS[AnalysisPerspective.PRODUCT_TREND] == "partNumber;period"
        
    def test_revision_includes_part_number(self):
        """BY_REVISION should include partNumber and revision."""
        dims = PERSPECTIVE_TO_DIMENSIONS[AnalysisPerspective.BY_REVISION]
        assert "partNumber" in dims
        assert "revision" in dims


class TestYieldFilter:
    """Tests for YieldFilter model."""
    
    def test_default_values(self):
        """Default values should be set correctly."""
        f = YieldFilter()
        assert f.days == 30
        assert f.perspective is None
        assert f.part_number is None
        assert f.include_current_period is True
        
    def test_with_perspective(self):
        """Filter with perspective should work."""
        f = YieldFilter(perspective="by station", part_number="WIDGET-001")
        assert f.perspective == "by station"
        assert f.part_number == "WIDGET-001"


class TestBuildWatsFilter:
    """Tests for building WATS API filter from YieldFilter."""
    
    def test_basic_filter(self):
        """Basic filter should include date range."""
        f = YieldFilter(days=7)
        params = build_wats_filter(f)
        
        assert "date_from" in params
        assert "date_to" in params
        assert params["include_current_period"] is True
        
    def test_filter_with_perspective(self):
        """Filter with perspective should include dimensions."""
        f = YieldFilter(perspective="by station", days=7)
        params = build_wats_filter(f)
        
        assert params["dimensions"] == "stationName"
        
    def test_filter_with_part_number(self):
        """Filter with part_number should pass through."""
        f = YieldFilter(part_number="WIDGET-001")
        params = build_wats_filter(f)
        
        assert params["part_number"] == "WIDGET-001"
        
    def test_filter_with_station(self):
        """Filter with station_name should pass through."""
        f = YieldFilter(station_name="Line1-EOL")
        params = build_wats_filter(f)
        
        assert params["station_name"] == "Line1-EOL"
        
    def test_filter_daily_includes_date_grouping(self):
        """Daily perspective should set date_grouping."""
        f = YieldFilter(perspective="daily")
        params = build_wats_filter(f)
        
        assert params["date_grouping"] == "DAY"
        
    def test_filter_weekly_grouping(self):
        """Weekly perspective should set date_grouping to WEEK."""
        f = YieldFilter(perspective="weekly")
        params = build_wats_filter(f)
        
        assert params["date_grouping"] == "WEEK"
        
    def test_custom_dimensions_override(self):
        """Custom dimensions should override perspective."""
        f = YieldFilter(
            perspective="by station",  # Would normally be stationName
            dimensions="partNumber;stationName"  # Override
        )
        params = build_wats_filter(f)
        
        assert params["dimensions"] == "partNumber;stationName"


class TestGetAvailablePerspectives:
    """Tests for perspective discovery."""
    
    def test_returns_categories(self):
        """Should return categorized perspectives."""
        perspectives = get_available_perspectives()
        
        assert "time_based" in perspectives
        assert "equipment" in perspectives
        assert "product" in perspectives
        assert "process" in perspectives
        assert "combined" in perspectives
        
    def test_time_based_options(self):
        """Time-based should include trend, daily, etc."""
        perspectives = get_available_perspectives()
        
        assert "trend" in perspectives["time_based"]
        assert "daily" in perspectives["time_based"]
        assert "weekly" in perspectives["time_based"]


class TestAliasCompleteness:
    """Tests to ensure alias coverage."""
    
    def test_all_perspectives_have_aliases(self):
        """Every perspective should have at least one alias."""
        all_perspectives = set(AnalysisPerspective)
        perspectives_with_aliases = set(PERSPECTIVE_ALIASES.values())
        
        # Check each perspective has at least one alias
        for p in all_perspectives:
            assert p in perspectives_with_aliases, f"{p} has no aliases"
            
    def test_common_terms_covered(self):
        """Common manufacturing terms should be covered."""
        common_terms = [
            "by station", "by tester", "by equipment",
            "by product", "by part", "by part number",
            "trend", "over time", "daily", "weekly",
            "by operator", "by batch", "by lot"
        ]
        
        for term in common_terms:
            result = resolve_perspective(term)
            assert result is not None, f"'{term}' should resolve to a perspective"
