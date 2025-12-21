from typing import Any

import pytest

from pywats import pyWATS
from pywats.domains.report import WATSFilter


# NOTE: These are server integration tests. They must query a WATS environment
# that contains recent asset-linked reports. The provided curl example targets
# https://live.wats.com.
WATS_SERVER = "https://live.wats.com"
WATS_TOKEN = "QWdlbnREZWJ1ZzpwbTJQZDA4UTY3SjU3NnpyNWImMkwyUHRXOUhCUjI="


@pytest.fixture(scope="module")
def live_wats_client() -> pyWATS:
    """Create WATS client with live server credentials."""
    return pyWATS(base_url=WATS_SERVER, token=WATS_TOKEN)


def _print_dynamic_yield_rows(title: str, rows: list[Any], limit: int = 10) -> None:
    print(f"\n=== {title} ===")
    print(f"Rows: {len(rows)}")
    for i, row in enumerate(rows[:limit], 1):
        # YieldData is a PyWATSModel, but keep this generic.
        if hasattr(row, "model_dump"):
            print(f"  {i}. {row.model_dump(exclude_none=True)}")
        else:
            print(f"  {i}. {row}")
    print("=" * (len(title) + 8))


@pytest.mark.integration
def test_dynamic_yield_last_30_days_by_misc_info_dimensions(live_wats_client: Any) -> None:
    """Verify server returns data when grouping by misc-info dimensions."""

    filter_obj = WATSFilter(
        # No filters: rely on server default (last 30 days).
        dimensions="miscInfoDescription",
    )

    print("\nDynamicYield payload (misc):")
    print(filter_obj.model_dump(by_alias=True, exclude_none=True))

    rows = live_wats_client.analytics.get_dynamic_yield(filter_obj)

    assert isinstance(rows, list), "Expected list response"
    _print_dynamic_yield_rows("DynamicYield (miscInfoDescription)", rows)
    assert len(rows) > 0, "Expected server to return at least one row for misc-info dimension"


@pytest.mark.integration
def test_dynamic_yield_last_30_days_by_asset_dimensions(live_wats_client: Any) -> None:
    """Verify server returns data when grouping by asset dimensions."""

    # Match the working curl: no filters + asset in dimension.
    filter_obj = WATSFilter(
        # No filters: rely on server default (last 30 days).
        dimensions="assetName",
    )

    print("\nDynamicYield payload (asset):")
    print(filter_obj.model_dump(by_alias=True, exclude_none=True))

    rows = live_wats_client.analytics.get_dynamic_yield(filter_obj)

    assert isinstance(rows, list), "Expected list response"
    _print_dynamic_yield_rows("DynamicYield (assetName)", rows)
    assert len(rows) > 0, "Expected server to return at least one row for assetName dimension"
