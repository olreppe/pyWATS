"""Tests for potential time filter conflicts.

This module tests the interaction between different time filter parameters
to identify potential issues when combining:
- date_from/date_to (explicit date range)
- period_count (number of periods to return)
- date_grouping (how to group: DAY, WEEK, MONTH, etc.)
- days (convenience parameter)

The WATS API default filter uses periodCount WITHOUT date range:
{
    "periodCount": 30,
    "dateGrouping": 1,
    "includeCurrentPeriod": true
}

This raises questions about what happens when we combine these parameters.
"""
import pytest
from datetime import datetime, timedelta
from pywats_agent.tools.yield_pkg import (
    YieldFilter,
    build_wats_filter,
)


pytestmark = pytest.mark.agent


class TestTimeFilterConflicts:
    """Test potential conflicts between time filter parameters.
    
    The WATS API documentation shows that the default filter uses
    periodCount/dateGrouping WITHOUT explicit date ranges. This suggests
    that combining both may lead to unexpected behavior.
    
    FIX IMPLEMENTED: When period_count is set WITHOUT explicit date_from,
    we now omit date_from/date_to and let the API calculate from period_count.
    """
    
    def test_period_count_without_explicit_dates_omits_date_range(self):
        """When using period_count without explicit date_from, omit date range.
        
        This follows WATS API default behavior where periodCount is used
        without dateFrom/dateTo.
        """
        filter_obj = YieldFilter(
            perspective="daily",
            period_count=7,
            # days=30 is default but should be ignored when period_count is set
        )
        
        params = build_wats_filter(filter_obj)
        
        # period_count should be set
        assert "period_count" in params, "period_count should be in params"
        assert params["period_count"] == 7
        
        # date_from/date_to should NOT be set (let API calculate from period_count)
        assert "date_from" not in params, "date_from should NOT be set when using period_count"
        assert "date_to" not in params, "date_to should NOT be set when using period_count"
        
    def test_period_count_with_explicit_date_from_has_both(self):
        """When period_count is used WITH explicit date_from, include both.
        
        User explicitly provided a date range, so respect both settings.
        """
        explicit_date = datetime(2024, 1, 1)
        filter_obj = YieldFilter(
            perspective="daily",
            period_count=7,
            date_from=explicit_date  # User explicitly set this
        )
        
        params = build_wats_filter(filter_obj)
        
        # Both should be set since user explicitly provided date_from
        assert "period_count" in params
        assert params["period_count"] == 7
        assert "date_from" in params
        assert params["date_from"] == explicit_date
        
    def test_date_grouping_without_period_count_uses_days(self):
        """Test date_grouping without period_count uses date range from days.
        
        When using daily/weekly/monthly perspective without period_count,
        calculate date range from 'days' parameter.
        """
        filter_obj = YieldFilter(
            perspective="weekly",
            days=90  # 90 days of data, grouped by week
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "WEEK"
        # Without period_count, should have date range
        assert "date_from" in params
        assert "date_to" in params
        assert "period_count" not in params or params.get("period_count") is None
        
    def test_explicit_date_range_without_period_count(self):
        """Test explicit date range without period_count."""
        filter_obj = YieldFilter(
            perspective="daily",
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 1, 31),
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_from"] == datetime(2024, 1, 1)
        assert params["date_to"] == datetime(2024, 1, 31)
        assert "period_count" not in params


class TestDateRangeCalculation:
    """Test how date ranges are calculated."""
    
    def test_days_sets_date_from_relative_to_now(self):
        """The 'days' parameter should set date_from relative to date_to."""
        before = datetime.now()
        filter_obj = YieldFilter(days=7)
        params = build_wats_filter(filter_obj)
        after = datetime.now()
        
        # date_to should be approximately now
        date_to = params["date_to"]
        assert before <= date_to <= after
        
        # date_from should be 7 days before date_to
        date_from = params["date_from"]
        expected_from = date_to - timedelta(days=7)
        
        # Allow some tolerance for test execution time
        delta = abs((date_from - expected_from).total_seconds())
        assert delta < 2, f"date_from off by {delta} seconds"
        
    def test_explicit_date_from_overrides_days(self):
        """Explicit date_from should override the 'days' calculation."""
        explicit_date = datetime(2024, 6, 1)
        filter_obj = YieldFilter(
            date_from=explicit_date,
            days=30  # This should be ignored when date_from is set
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_from"] == explicit_date


class TestRecommendedPatterns:
    """Test recommended patterns for time-based queries.
    
    Based on WATS API behavior, document recommended patterns.
    """
    
    def test_last_n_periods_pattern(self):
        """Pattern for 'give me the last 7 days of daily yield'.
        
        Recommended: Use perspective + period_count
        Question: Should we also need date_from?
        """
        filter_obj = YieldFilter(
            perspective="daily",
            period_count=7
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "DAY"
        assert params["period_count"] == 7
        # Currently also sets date_from - is this correct?
        
    def test_date_range_pattern(self):
        """Pattern for 'yield from Jan 1 to Jan 31'.
        
        Recommended: Use explicit date_from + date_to
        """
        filter_obj = YieldFilter(
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 1, 31)
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_from"] == datetime(2024, 1, 1)
        assert params["date_to"] == datetime(2024, 1, 31)
        
    def test_daily_trend_for_date_range_pattern(self):
        """Pattern for 'daily yield trend from Jan 1 to Jan 31'.
        
        Uses explicit dates + date_grouping.
        """
        filter_obj = YieldFilter(
            perspective="daily",
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 1, 31)
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["date_grouping"] == "DAY"
        assert params["date_from"] == datetime(2024, 1, 1)
        assert params["date_to"] == datetime(2024, 1, 31)
        # No period_count - should return all days in range


class TestWATSAPIBehaviorAssumptions:
    """Document assumptions about WATS API behavior.
    
    These tests encode our understanding of how the API handles
    different parameter combinations. If these fail, our understanding
    may be wrong.
    """
    
    def test_assumption_period_count_is_last_n(self):
        """We assume periodCount=7 with DAY grouping means 'last 7 days'.
        
        The API description says periodCount is 'Number of periods to return'.
        Combined with dateGrouping=DAY, this should be last 7 days.
        """
        # This is an assumption - no way to verify without API call
        pass
        
    def test_assumption_date_range_overrides_period_count(self):
        """We assume date range takes precedence over period_count.
        
        If date range is Jan 1-31 and period_count=7, we assume
        the API uses the date range and ignores period_count.
        
        OR the API returns 7 periods within that date range.
        
        This is unclear from the documentation.
        """
        # This assumption needs verification with actual API
        pass
        
    def test_assumption_include_current_period_affects_last_period(self):
        """We assume includeCurrentPeriod affects the current incomplete period.
        
        If today is Jan 15 and we ask for monthly data, includeCurrentPeriod=True
        should include January (incomplete), while False should exclude it.
        """
        # This is an assumption - documented for verification
        pass


class TestPotentialBugScenarios:
    """Test scenarios that previously had bugs - now fixed.
    
    These tests verify the fix works correctly.
    """
    
    def test_period_count_7_daily_omits_date_range(self):
        """FIXED: Using period_count=7 now correctly omits date range.
        
        User intent: "Give me the last 7 days of daily yield"
        Fixed behavior: Sends periodCount=7, NO dateFrom/dateTo
        """
        filter_obj = YieldFilter(
            perspective="daily",
            period_count=7
            # days defaults to 30 but is ignored when period_count is set
        )
        
        params = build_wats_filter(filter_obj)
        
        # Verify fix: period_count without date range
        assert params["period_count"] == 7, "User wants 7 periods"
        assert "date_from" not in params, "date_from should be omitted"
        assert "date_to" not in params, "date_to should be omitted"
        
    def test_weekly_with_period_count_5_omits_date_range(self):
        """FIXED: Weekly for 5 weeks correctly omits date range.
        
        User intent: "Give me weekly yield for the last 5 weeks"
        Fixed behavior: Sends periodCount=5, dateGrouping=WEEK, NO date range
        """
        filter_obj = YieldFilter(
            perspective="weekly",
            period_count=5
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["period_count"] == 5
        assert params["date_grouping"] == "WEEK"
        assert "date_from" not in params, "Let API calculate 5 weeks back"
        
    def test_monthly_with_period_count_3_omits_date_range(self):
        """FIXED: Monthly for 3 months correctly omits date range.
        
        User intent: "Give me monthly yield for the last 3 months"
        Fixed behavior: Sends periodCount=3, dateGrouping=MONTH, NO date range
        """
        filter_obj = YieldFilter(
            perspective="monthly",
            period_count=3
        )
        
        params = build_wats_filter(filter_obj)
        
        assert params["period_count"] == 3
        assert params["date_grouping"] == "MONTH"
        assert "date_from" not in params, "Let API calculate 3 months back"
        
    def test_user_can_still_use_explicit_date_range_with_period_count(self):
        """User can still combine explicit date range with period_count if desired.
        
        This is an advanced use case where user wants specific control.
        """
        filter_obj = YieldFilter(
            perspective="daily",
            period_count=7,
            date_from=datetime(2024, 1, 1),  # Explicit date
            date_to=datetime(2024, 1, 31)
        )
        
        params = build_wats_filter(filter_obj)
        
        # Both should be present since user explicitly set date_from
        assert params["period_count"] == 7
        assert params["date_from"] == datetime(2024, 1, 1)
        assert params["date_to"] == datetime(2024, 1, 31)
        
    def test_days_parameter_still_works_without_period_count(self):
        """The 'days' parameter still works when period_count is not set.
        
        User intent: "Give me yield for the last 14 days"
        Behavior: Calculate date range from days parameter
        """
        filter_obj = YieldFilter(
            days=14
            # No period_count
        )
        
        params = build_wats_filter(filter_obj)
        
        # Should have date range calculated from days
        assert "date_from" in params
        assert "date_to" in params
        assert "period_count" not in params
        
        # Verify the date range is approximately 14 days
        delta = (params["date_to"] - params["date_from"]).days
        assert delta == 14
