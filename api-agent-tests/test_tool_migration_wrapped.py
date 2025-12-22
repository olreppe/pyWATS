from __future__ import annotations

from pywats_agent.agent import InMemoryDataStore, ToolExecutor


def test_migrated_wrapped_tools_execute_and_return_data_key(monkeypatch):
    # Patch the v1 tools inside the wrapper module, so we don't need a real WATS server.
    from pywats_agent.agent.tools import wrapped
    from pywats_agent.result import AgentResult

    class DummyYield:
        def __init__(self, api):
            pass

        def analyze(self, filter_input):
            return AgentResult.ok(
                data=[{"station": "A", "fpy": 99.0}] * 50,
                summary="ok yield",
                metadata={"source": "dummy"},
            )

    monkeypatch.setattr(wrapped, "YieldAnalysisTool", DummyYield)

    ds = InMemoryDataStore()
    ex = ToolExecutor.with_default_tools(api=None, datastore=ds, profile_name="minimal")

    result = ex.execute("analyze_yield", {"perspective": "by station", "days": 7})

    assert result.ok is True
    assert result.data_key is not None
    assert result.preview is not None
    assert "rows" in result.preview

    full = ds.get(result.data_key)
    assert isinstance(full, list)
    assert len(full) == 50


def test_wrapped_tools_prefix_kpis_on_success(monkeypatch):
    # Patch the v1 tools inside the wrapper module.
    from pywats_agent.agent.tools import wrapped
    from pywats_agent.result import AgentResult
    from pywats_agent.agent import InMemoryDataStore, ToolExecutor

    class DummyYield:
        def __init__(self, api):
            pass

        def analyze(self, filter_input):
            return AgentResult.ok(
                data=[{"x": 1}] * 3,
                summary="some verbose summary",
                metadata={},
            )

    monkeypatch.setattr(wrapped, "YieldAnalysisTool", DummyYield)

    ds = InMemoryDataStore()
    ex = ToolExecutor.with_default_tools(api=None, datastore=ds, profile_name="minimal")
    env = ex.execute("analyze_yield", {})

    assert env.ok is True
    assert env.summary.startswith("KPIS:"), env.summary


def test_wrapped_tools_convert_empty_list_to_no_data(monkeypatch):
    # Ensure empty list does not become an empty preview/data_key-only response.
    from pywats_agent.agent.tools import wrapped
    from pywats_agent.result import AgentResult
    from pywats_agent.agent import InMemoryDataStore, ToolExecutor

    class DummyYield:
        def __init__(self, api):
            pass

        def analyze(self, filter_input):
            return AgentResult.ok(
                data=[],
                summary="",
                metadata={},
            )

    monkeypatch.setattr(wrapped, "YieldAnalysisTool", DummyYield)

    ds = InMemoryDataStore()
    ex = ToolExecutor.with_default_tools(api=None, datastore=ds, profile_name="minimal")
    env = ex.execute("analyze_yield", {})

    assert env.ok is True
    assert env.data_key is None
    assert env.preview is None
    assert env.summary.startswith("NO_DATA:"), env.summary
