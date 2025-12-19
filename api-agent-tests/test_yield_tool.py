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


pytestmark = pytest.mark.agent  # Mark all tests in this module as agent tests


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


# =============================================================================
# YIELD DOMAIN KNOWLEDGE TESTS
# =============================================================================


class TestYieldDomainKnowledge:
    """
    Test yield domain knowledge is properly incorporated.
    
    Domain Knowledge Summary:
    - FPY/SPY/TPY/LPY are UNIT-BASED yield metrics
    - TRY (Test Report Yield) is REPORT-BASED
    - Unit Inclusion Rule: Unit included only if FIRST RUN matches filter
    - Repair Line Problem: Retest-only stations show 0 units
    """
    
    def test_yield_filter_has_yield_type_parameter(self):
        """Test that YieldFilter includes yield_type parameter."""
        # Default should be 'unit'
        filter_obj = YieldFilter()
        assert filter_obj.yield_type == "unit"
        
        # Can set to 'report'
        filter_obj = YieldFilter(yield_type="report")
        assert filter_obj.yield_type == "report"
    
    def test_yield_type_default_is_unit(self):
        """Verify unit-based yield is the default (most common use case)."""
        filter_obj = YieldFilter()
        assert filter_obj.yield_type == "unit", "Default yield_type should be 'unit' for FPY/SPY/TPY/LPY"
    
    def test_yield_filter_accepts_report_type(self):
        """Test that report-based yield (TRY) can be selected."""
        filter_obj = YieldFilter(yield_type="report")
        assert filter_obj.yield_type == "report", "Should accept 'report' for TRY analysis"


class TestYieldToolParameterSchema:
    """Test that yield_type appears correctly in parameter schema."""
    
    def test_yield_type_in_parameter_schema(self):
        """Test that yield_type appears in the OpenAI parameter schema."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        schema = YieldAnalysisTool.get_parameters_schema()
        
        # Check yield_type is in properties
        assert "yield_type" in schema["properties"], "yield_type should be in schema properties"
        
        # Check enum values
        yield_type_schema = schema["properties"]["yield_type"]
        assert yield_type_schema["type"] == "string"
        assert yield_type_schema["enum"] == ["unit", "report"]
        assert yield_type_schema["default"] == "unit"
    
    def test_yield_type_description_explains_metrics(self):
        """Test that yield_type description explains FPY vs TRY."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        schema = YieldAnalysisTool.get_parameters_schema()
        description = schema["properties"]["yield_type"]["description"]
        
        # Should explain unit-based metrics
        assert "FPY" in description or "unit" in description.lower()
        
        # Should explain report-based metrics
        assert "TRY" in description or "report" in description.lower()
        
        # Should mention repair line scenario
        assert "retest" in description.lower() or "repair" in description.lower()


class TestYieldToolDescription:
    """Test that tool descriptions include domain knowledge."""
    
    def test_tool_description_includes_domain_knowledge(self):
        """Test that the tool description includes yield domain knowledge."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        description = YieldAnalysisTool.description
        
        # Should explain unit-based metrics
        assert "FPY" in description
        
        # Should explain report-based metrics
        assert "TRY" in description or "Report" in description
        
        # Should mention unit inclusion rule
        assert "FIRST RUN" in description.upper() or "first run" in description.lower()
    
    def test_class_docstring_explains_unit_inclusion_rule(self):
        """Test that class docstring explains the unit inclusion rule."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should explain the unit inclusion rule
        assert "first run" in docstring.lower()
        assert "unit" in docstring.lower()
        
        # Should explain repair line scenario
        assert "repair" in docstring.lower() or "retest" in docstring.lower()


class TestRepairLineDetection:
    """
    Test repair line scenario detection.
    
    The repair line problem:
    - Retest-only stations never see first runs
    - Unit-based yield will show 0 units
    - Tool should detect this and suggest using report-based yield
    """
    
    def test_repair_line_check_exists(self):
        """Test that repair line check method exists."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        from unittest.mock import MagicMock
        
        mock_api = MagicMock()
        tool = YieldAnalysisTool(mock_api)
        
        # Method should exist
        assert hasattr(tool, '_check_repair_line_scenario')
    
    def test_repair_line_check_detects_station_filter(self):
        """Test that station filter triggers repair line warning."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        from unittest.mock import MagicMock
        
        mock_api = MagicMock()
        tool = YieldAnalysisTool(mock_api)
        
        # Filter with station name should trigger warning
        filter_with_station = YieldFilter(
            station_name="REPAIR-STATION-01",
            yield_type="unit"
        )
        
        warning = tool._check_repair_line_scenario(filter_with_station)
        assert warning is not None, "Station filter should trigger repair line warning"
        assert "report" in warning.lower(), "Warning should suggest using report type"
    
    def test_repair_line_check_detects_operator_filter(self):
        """Test that operator filter triggers repair line warning."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        from unittest.mock import MagicMock
        
        mock_api = MagicMock()
        tool = YieldAnalysisTool(mock_api)
        
        filter_with_operator = YieldFilter(
            operator="John",
            yield_type="unit"
        )
        
        warning = tool._check_repair_line_scenario(filter_with_operator)
        assert warning is not None, "Operator filter should trigger repair line warning"
    
    def test_no_warning_for_report_type(self):
        """Test that report yield_type doesn't trigger warning."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        from unittest.mock import MagicMock
        
        mock_api = MagicMock()
        tool = YieldAnalysisTool(mock_api)
        
        # Even with station filter, report type should not warn
        filter_report = YieldFilter(
            station_name="REPAIR-STATION-01",
            yield_type="report"
        )
        
        warning = tool._check_repair_line_scenario(filter_report)
        assert warning is None, "Report type should not trigger repair line warning"
    
    def test_no_warning_for_product_filter_only(self):
        """Test that product-only filter doesn't trigger warning."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        from unittest.mock import MagicMock
        
        mock_api = MagicMock()
        tool = YieldAnalysisTool(mock_api)
        
        # Product filter alone shouldn't warn (products have first runs)
        filter_product = YieldFilter(
            part_number="WIDGET-001",
            yield_type="unit"
        )
        
        warning = tool._check_repair_line_scenario(filter_product)
        assert warning is None, "Product-only filter should not trigger repair line warning"


class TestToolDefinitionExports:
    """Test tool definition export functions."""
    
    def test_tool_definition_structure(self):
        """Test that tool definition has correct structure."""
        from pywats_agent.tools.yield_tool import get_yield_tool_definition
        
        definition = get_yield_tool_definition()
        
        assert "name" in definition
        assert "description" in definition
        assert "parameters" in definition
        
        # Check name
        assert definition["name"] == "analyze_yield"
    
    def test_openai_schema_structure(self):
        """Test OpenAI function calling schema."""
        from pywats_agent.tools.yield_tool import get_yield_tool_openai_schema
        
        schema = get_yield_tool_openai_schema()
        
        assert schema["type"] == "function"
        assert "function" in schema
        assert schema["function"]["name"] == "analyze_yield"


# =============================================================================
# RTY AND PROCESS DOMAIN KNOWLEDGE TESTS
# =============================================================================


class TestRTYAndProcessKnowledge:
    """
    Test RTY (Rolled Throughput Yield) and process-aware domain knowledge.
    
    Key concepts:
    - Yield should always be considered per process (test_operation)
    - RTY = FPY1 x FPY2 x ... x FPYn (product of all process FPYs)
    - Top runners = highest volume products, per process
    """
    
    def test_tool_description_mentions_rty(self):
        """Test that tool description includes RTY information."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        description = YieldAnalysisTool.description
        
        # Should mention RTY
        assert "RTY" in description or "Rolled" in description
        
    def test_tool_description_mentions_process_context(self):
        """Test that tool description emphasizes process context."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        description = YieldAnalysisTool.description
        
        # Should emphasize yield is per process
        assert "process" in description.lower()
        assert "test_operation" in description.lower() or "operation" in description.lower()
    
    def test_tool_docstring_explains_rty(self):
        """Test that class docstring explains RTY calculation."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should explain RTY
        assert "RTY" in docstring or "Rolled Throughput" in docstring
        
    def test_tool_docstring_mentions_top_runners(self):
        """Test that docstring mentions top runners concept."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should mention top runners
        assert "top runner" in docstring.lower() or "volume" in docstring.lower()
    
    def test_tool_docstring_mentions_verification_rules(self):
        """Test that docstring mentions unit verification rules."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should mention verification rules
        assert "verification" in docstring.lower()


class TestByOperationPerspective:
    """Test the by operation perspective for discovering processes."""
    
    def test_by_operation_perspective_exists(self):
        """Test that BY_OPERATION perspective is available."""
        from pywats_agent.tools.yield_tool import AnalysisPerspective
        
        assert hasattr(AnalysisPerspective, 'BY_OPERATION')
    
    def test_by_operation_alias_resolves(self):
        """Test that common aliases resolve to BY_OPERATION."""
        from pywats_agent.tools.yield_tool import resolve_perspective, AnalysisPerspective
        
        # Test various aliases
        assert resolve_perspective("by operation") == AnalysisPerspective.BY_OPERATION
        assert resolve_perspective("by process") == AnalysisPerspective.BY_PROCESS
    
    def test_by_operation_maps_to_correct_dimension(self):
        """Test BY_OPERATION maps to testOperation dimension."""
        from pywats_agent.tools.yield_tool import (
            AnalysisPerspective, 
            PERSPECTIVE_TO_DIMENSIONS
        )
        
        dimension = PERSPECTIVE_TO_DIMENSIONS.get(AnalysisPerspective.BY_OPERATION)
        assert dimension is not None
        assert "testOperation" in dimension or "operation" in dimension.lower()


class TestProcessFilterParameter:
    """Test that test_operation parameter works for process filtering."""
    
    def test_yield_filter_accepts_test_operation(self):
        """Test that YieldFilter accepts test_operation parameter."""
        filter_obj = YieldFilter(
            part_number="WIDGET-001",
            test_operation="FCT"
        )
        
        assert filter_obj.test_operation == "FCT"
    
    def test_build_wats_filter_includes_test_operation(self):
        """Test that test_operation is passed to WATS filter."""
        filter_obj = YieldFilter(
            part_number="WIDGET-001",
            test_operation="FCT",
            days=30
        )
        
        params = build_wats_filter(filter_obj)
        
        assert "test_operation" in params
        assert params["test_operation"] == "FCT"
    
    def test_yield_filter_with_multiple_params(self):
        """Test YieldFilter with product and process together."""
        filter_obj = YieldFilter(
            part_number="WIDGET-001",
            test_operation="FCT",
            perspective="trend",
            days=7
        )
        
        assert filter_obj.part_number == "WIDGET-001"
        assert filter_obj.test_operation == "FCT"
        assert filter_obj.perspective == "trend"


class TestTopRunnersQueries:
    """Test queries for finding top runners (highest volume products)."""
    
    def test_by_product_with_process_filter(self):
        """Test by-product perspective with test_operation filter for top runners."""
        filter_obj = YieldFilter(
            test_operation="FCT",
            perspective="by product",
            days=30
        )
        
        params = build_wats_filter(filter_obj)
        
        # Should have dimensions for product grouping
        assert "dimensions" in params
        assert "partNumber" in params["dimensions"]
        
        # Should also filter by test operation
        assert params.get("test_operation") == "FCT"


# =============================================================================
# TEMPORAL YIELD KNOWLEDGE TESTS
# =============================================================================


class TestTemporalYieldKnowledge:
    """
    Test temporal/time-based yield domain knowledge.
    
    Key concepts:
    - date_from/date_to default to last 30 days if not specified
    - WATS assumes you want the most recent data
    - period_count and date_grouping for time-series analysis
    - Yield trend = change compared to previous equally-sized period
    - Periods can be safely summed due to first-pass-included rule
    """
    
    def test_default_days_is_30(self):
        """Test that default days is 30 (matching WATS server default)."""
        filter_obj = YieldFilter()
        assert filter_obj.days == 30, "Default days should be 30 (WATS server default)"
    
    def test_yield_filter_accepts_period_count(self):
        """Test that YieldFilter accepts period_count parameter."""
        filter_obj = YieldFilter(period_count=7)
        assert filter_obj.period_count == 7
    
    def test_yield_filter_accepts_date_grouping(self):
        """Test that YieldFilter accepts date_grouping parameter."""
        filter_obj = YieldFilter(date_grouping="WEEK")
        assert filter_obj.date_grouping == "WEEK"
    
    def test_build_wats_filter_includes_period_count(self):
        """Test that period_count is passed to WATS filter."""
        filter_obj = YieldFilter(
            perspective="daily",
            period_count=10,
            days=14
        )
        
        params = build_wats_filter(filter_obj)
        
        assert "period_count" in params
        assert params["period_count"] == 10
    
    def test_explicit_date_grouping_overrides_perspective(self):
        """Test that explicit date_grouping overrides perspective's default."""
        filter_obj = YieldFilter(
            perspective="daily",  # Would normally be DAY
            date_grouping="HOUR"  # Override to HOUR
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "HOUR", "Explicit date_grouping should override"
    
    def test_date_grouping_options_documented(self):
        """Test that valid date_grouping options are documented in the field."""
        # Check that the field description mentions valid options
        field_info = YieldFilter.model_fields.get("date_grouping")
        assert field_info is not None
        
        description = field_info.description
        # Should mention valid options
        assert "HOUR" in description
        assert "DAY" in description
        assert "WEEK" in description
        assert "MONTH" in description


class TestTimePerspectives:
    """Test time-based perspectives and their date_grouping mappings."""
    
    def test_daily_perspective_sets_day_grouping(self):
        """Test daily perspective sets DAY grouping."""
        filter_obj = YieldFilter(perspective="daily")
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "DAY"
    
    def test_weekly_perspective_sets_week_grouping(self):
        """Test weekly perspective sets WEEK grouping."""
        filter_obj = YieldFilter(perspective="weekly")
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "WEEK"
    
    def test_monthly_perspective_sets_month_grouping(self):
        """Test monthly perspective sets MONTH grouping."""
        filter_obj = YieldFilter(perspective="monthly")
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "MONTH"
    
    def test_trend_perspective_sets_day_grouping(self):
        """Test trend perspective defaults to DAY grouping."""
        filter_obj = YieldFilter(perspective="trend")
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "DAY"


class TestTemporalDocumentation:
    """Test that temporal yield knowledge is in documentation."""
    
    def test_tool_docstring_mentions_temporal_analysis(self):
        """Test that class docstring includes temporal analysis info."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should mention temporal analysis
        assert "time" in docstring.lower() or "temporal" in docstring.lower()
        
    def test_tool_docstring_mentions_date_defaults(self):
        """Test that docstring mentions default date behavior."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should mention 30 days default
        assert "30" in docstring
        
    def test_tool_docstring_mentions_yield_trend(self):
        """Test that docstring mentions yield trend metrics."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should mention trend/comparison
        assert "trend" in docstring.lower()
        
    def test_tool_docstring_mentions_period_aggregation(self):
        """Test that docstring mentions safe period aggregation."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        docstring = YieldAnalysisTool.__doc__
        
        # Should mention that periods can be aggregated/summed
        assert "period" in docstring.lower()
        assert "aggregat" in docstring.lower() or "sum" in docstring.lower()
    
    def test_tool_description_mentions_yield_over_time(self):
        """Test that tool description includes yield over time info."""
        from pywats_agent.tools.yield_tool import YieldAnalysisTool
        
        description = YieldAnalysisTool.description
        
        # Should mention time-based analysis
        assert "time" in description.lower() or "trend" in description.lower()


class TestPeriodicYieldQueries:
    """Test queries for periodic/time-series yield analysis."""
    
    def test_daily_yield_for_past_week(self):
        """Test creating a daily yield query for the past week."""
        filter_obj = YieldFilter(
            part_number="WIDGET-001",
            test_operation="FCT",
            perspective="daily",
            days=7
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["part_number"] == "WIDGET-001"
        assert params["test_operation"] == "FCT"
        assert params["date_grouping"] == "DAY"
        assert "dimensions" in params and "period" in params["dimensions"]
    
    def test_weekly_trend_with_period_count(self):
        """Test weekly trend with specific period count."""
        filter_obj = YieldFilter(
            perspective="weekly",
            period_count=4,
            days=28
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "WEEK"
        assert params["period_count"] == 4
    
    def test_monthly_yield_analysis(self):
        """Test monthly yield analysis query."""
        filter_obj = YieldFilter(
            product_group="Electronics",
            perspective="monthly",
            days=90
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["product_group"] == "Electronics"
        assert params["date_grouping"] == "MONTH"
        assert "dimensions" in params


class TestDateRangeHandling:
    """Test date range parameter handling."""
    
    def test_days_parameter_sets_date_from(self):
        """Test that days parameter correctly calculates date_from."""
        from datetime import datetime, timedelta
        
        filter_obj = YieldFilter(days=7)
        params = build_wats_filter(filter_obj)
        
        # date_to should be approximately now
        assert params["date_to"] is not None
        
        # date_from should be approximately 7 days before date_to
        delta = params["date_to"] - params["date_from"]
        assert abs(delta.days - 7) <= 1  # Allow small timing variance
    
    def test_explicit_date_range_overrides_days(self):
        """Test that explicit date_from overrides days parameter."""
        from datetime import datetime, timedelta
        
        explicit_from = datetime.now() - timedelta(days=90)
        filter_obj = YieldFilter(
            days=7,  # This should be ignored
            date_from=explicit_from
        )
        
        params = build_wats_filter(filter_obj)
        
        # Should use explicit date_from
        assert params["date_from"] == explicit_from


