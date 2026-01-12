"""Tests for DynamicRepair endpoint - comprehensive validation.

These tests make actual API calls to the WATS server.

Swagger summary (PREVIEW):
- POST /api/App/DynamicRepair
- Repair statistics calculated by custom dimensions defined in the `dimensions` filter.
- Multiple values are separated with semicolon (;)

Supported KPIs:
- repairReportCount
- repairCount

Note:
- These are integration tests and may legitimately return empty lists if the
  environment has no repair data.
"""

from typing import Any

import pytest


class TestDynamicRepairBasic:
    def test_dynamic_repair_default_filter(self, wats_client: Any) -> None:
        """Default filter from swagger: top 10 from last 30 days."""
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            top_count=10,
            period_count=30,
            date_grouping=DateGrouping.DAY,
            include_current_period=True,
            dimensions="repairCount desc;repairReportCount desc;partNumber;repairOperation",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)

    def test_dynamic_repair_by_part_number(self, wats_client: Any) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            top_count=10,
            period_count=30,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)

    def test_dynamic_repair_by_repair_operation(self, wats_client: Any) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            top_count=10,
            period_count=30,
            date_grouping=DateGrouping.DAY,
            dimensions="repairOperation",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)


class TestDynamicRepairDimensions:
    def test_dynamic_repair_part_and_period(self, wats_client: Any) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            period_count=7,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber;period",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)

    def test_dynamic_repair_multi_dimension(self, wats_client: Any) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            top_count=20,
            period_count=30,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber;repairOperation;period",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)


class TestDynamicRepairKPIs:
    def test_dynamic_repair_sort_by_repair_count(self, wats_client: Any) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            top_count=10,
            period_count=30,
            date_grouping=DateGrouping.DAY,
            dimensions="repairCount desc;partNumber",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)

    def test_dynamic_repair_sort_by_repair_report_count(self, wats_client: Any) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            top_count=10,
            period_count=30,
            date_grouping=DateGrouping.DAY,
            dimensions="repairReportCount desc;partNumber",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)


class TestDynamicRepairTimeRanges:
    @pytest.mark.parametrize("days", [1, 7, 30])
    def test_dynamic_repair_by_part_number_across_periods(
        self, wats_client: Any, days: int
    ) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping

        filter_obj = WATSFilter(
            period_count=days,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert result is not None
        assert isinstance(result, list)


class TestDynamicRepairDataValidation:
    def test_dynamic_repair_data_types(self, wats_client: Any) -> None:
        from pywats.domains.report import WATSFilter, DateGrouping
        from pywats.domains.analytics import RepairStatistics

        filter_obj = WATSFilter(
            top_count=5,
            period_count=30,
            date_grouping=DateGrouping.DAY,
            dimensions="partNumber;repairOperation",
        )

        result = wats_client.analytics.get_dynamic_repair(filter_obj)

        assert isinstance(result, list)

        if not result:
            pytest.skip("No repair data available to validate")

        first = result[0]
        assert isinstance(first, RepairStatistics)

        if first.repair_count is not None:
            assert isinstance(first.repair_count, int)
        if first.repair_report_count is not None:
            assert isinstance(first.repair_report_count, int)
        if first.repair_rate is not None:
            assert isinstance(first.repair_rate, (int, float))
