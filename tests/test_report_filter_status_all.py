import pytest

from pywats.domains.report.models import WATSFilter


@pytest.mark.parametrize(
    "raw_status",
    [
        "all",
        "ALL",
        "  all  ",
    ],
)
def test_wats_filter_normalizes_status_all_to_none(raw_status: str) -> None:
    f = WATSFilter(status=raw_status)

    assert f.status is None

    payload = f.model_dump(by_alias=True, exclude_none=True)
    assert "status" not in payload


def test_wats_filter_keeps_real_status_values() -> None:
    f = WATSFilter(status="P")

    assert f.status == "P"

    payload = f.model_dump(by_alias=True, exclude_none=True)
    assert payload["status"] == "P"
