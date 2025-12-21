from __future__ import annotations

from pydantic import Field

from pywats_agent.agent import (
    AgentToolV2,
    InMemoryDataStore,
    ResponsePolicy,
    ToolExecutorV2,
    ToolInput,
    ToolProfile,
    ToolRegistry,
)


class EchoInput(ToolInput):
    text: str = Field(min_length=1)


class EchoTool(AgentToolV2[EchoInput]):
    name = "echo"
    description = "Echo text and return a big list as data"
    input_model = EchoInput

    def run(self, input_obj: EchoInput):
        data = [{"i": i, "text": input_obj.text} for i in range(100)]
        return True, f"Echoed '{input_obj.text}' with {len(data)} rows", data, {"kind": "echo"}


def test_executor_v2_stores_data_out_of_band_and_previews():
    reg = ToolRegistry()
    reg.register(EchoTool)

    ds = InMemoryDataStore()
    policy = ResponsePolicy(preview_max_rows=5, preview_max_chars=10_000)

    ex = ToolExecutorV2(api=None, registry=reg, datastore=ds, policy=policy)

    result = ex.execute("echo", {"text": "hello"})

    assert result.ok is True
    assert "Echoed" in result.summary
    assert result.data_key is not None
    assert result.preview is not None
    assert len(result.preview["rows"]) == 5

    full = ds.get(result.data_key)
    assert isinstance(full, list)
    assert len(full) == 100


def test_executor_v2_tool_enablement_blocks_calls():
    reg = ToolRegistry()
    reg.register(EchoTool)

    ds = InMemoryDataStore()

    profile = ToolProfile(name="none", enabled_tools=())
    ex = ToolExecutorV2(api=None, registry=reg, datastore=ds, profile=profile)

    result = ex.execute("echo", {"text": "hello"})
    assert result.ok is False
    assert "not enabled" in result.summary


def test_executor_v2_openai_tool_schema_is_built_from_pydantic():
    reg = ToolRegistry()
    reg.register(EchoTool)

    ds = InMemoryDataStore()
    ex = ToolExecutorV2(api=None, registry=reg, datastore=ds)

    tools = ex.get_openai_tools()
    assert tools
    assert tools[0]["type"] == "function"
    assert tools[0]["function"]["name"] == "echo"
    props = tools[0]["function"]["parameters"]["properties"]
    assert "text" in props
