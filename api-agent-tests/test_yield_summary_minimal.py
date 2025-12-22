from pywats_agent.tools.yield_pkg.tool import YieldAnalysisTool, YieldFilter


class _DummyApi:
    pass


class _Row:
    def __init__(self, *, unit_count: int, fpy: float, test_operation: str | None = None):
        self.unit_count = unit_count
        self.fpy = fpy
        self.test_operation = test_operation


def test_yield_summary_includes_fpy_and_counts_when_using_fpy_field() -> None:
    tool = YieldAnalysisTool(_DummyApi())
    filt = YieldFilter(part_number="WIDGET-001", test_operation="FCT", days=7)

    data = [_Row(unit_count=10, fpy=90.0)]
    s = tool._build_summary(data, filt, {})

    assert "KPIS:" in s
    assert "units=" in s
    assert "avg_fpy=" in s


def test_yield_summary_includes_rty_when_multiple_operations_present() -> None:
    tool = YieldAnalysisTool(_DummyApi())
    filt = YieldFilter(part_number="WIDGET-001", test_operation=None, days=30, perspective="by operation")

    data = [
        _Row(unit_count=100, fpy=95.0, test_operation="FCT"),
        _Row(unit_count=100, fpy=98.0, test_operation="EOL"),
    ]
    s = tool._build_summary(data, filt, {})

    assert "RTY" in s
