import httpx

from pywats.core.client import HttpClient
from pywats_agent.agent.datastore import InMemoryDataStore
from pywats_agent.agent.executor import ToolExecutor
from pywats_agent.agent.registry import ToolRegistry
from pywats_agent.agent.tooling import AgentTool, ToolInput


def _mock_transport_handler(request: httpx.Request) -> httpx.Response:
    # Simple deterministic response for trace tests
    return httpx.Response(200, json={"ok": True, "path": str(request.url)})


def test_http_client_capture_traces_records_request_details() -> None:
    client = HttpClient(base_url="https://example.test", token="dummy")
    # Ensure we don't make network calls
    client._client = httpx.Client(
        base_url=client.base_url,
        headers={"Accept": "application/json"},
        transport=httpx.MockTransport(_mock_transport_handler),
        follow_redirects=True,
    )

    with client.capture_traces() as traces:
        resp = client.get("/api/App/Health", params={"x": 1})

    assert resp.is_success is True
    assert len(traces) == 1

    t = traces[0]
    assert t["method"] == "GET"
    assert t["url"].endswith("/api/App/Health")
    assert t["params"] == {"x": 1}
    assert t["status_code"] == 200
    assert t["response_bytes"] > 0
    assert t["duration_ms"] >= 0


class _DummyInput(ToolInput):
    pass


class _DummyTool(AgentTool[_DummyInput]):
    name = "dummy_trace_tool"
    description = "Dummy tool that performs a single HTTP call"
    input_model = _DummyInput

    def run(self, input_obj: _DummyInput):
        resp = self._api._http_client.get("/api/App/Health", params={"y": 2})
        return True, "ok", {"status": resp.status_code}, {}


class _DummyApi:
    def __init__(self) -> None:
        self._http_client = HttpClient(base_url="https://example.test", token="dummy")
        self._http_client._client = httpx.Client(
            base_url=self._http_client.base_url,
            headers={"Accept": "application/json"},
            transport=httpx.MockTransport(_mock_transport_handler),
            follow_redirects=True,
        )


def test_executor_stores_http_trace_out_of_band() -> None:
    registry = ToolRegistry()
    registry.register(_DummyTool)

    datastore = InMemoryDataStore()
    executor = ToolExecutor(_DummyApi(), registry=registry, datastore=datastore)

    env = executor.execute("dummy_trace_tool", {})

    assert env.ok is True
    assert env.metrics.get("http_trace_count") == 1
    trace_key = env.metrics.get("http_trace_key")
    assert isinstance(trace_key, str) and trace_key.startswith("mem://")

    traces = datastore.get(trace_key)
    assert isinstance(traces, list)
    assert traces and traces[0]["url"].endswith("/api/App/Health")
