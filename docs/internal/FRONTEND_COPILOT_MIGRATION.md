# Frontend Copilot Migration Guide (Canonical Tool Envelope)

This guide is for **frontend clients** ("Copilot" UI) that integrate with the `pywats_agent` tool system.

The primary change is that tool execution returns an **LLM-safe envelope** and stores bulk results out-of-band.

> BETA policy: breaking changes are expected.

---

## What changed (high level)

### 1) Tool execution result shape changed

**Before (legacy):** tools typically returned an `AgentResult`:

- `success: bool`
- `summary: string`
- `data: object | object[] | null` (often large)
- `metadata: object`
- `error: string | null`

**Now (canonical):** tools return a `ToolResultEnvelope`:

- `ok: bool`
- `summary: string` (bounded)
- `preview?: { rows: object[] }` (bounded)
- `data_key?: string` (handle to full data stored out-of-band)
- `metrics: object` (counts/truncation/etc)
- `warnings: string[]`
- `error?: string` (error code / exception name)

Frontend impact:
- Render `summary` and (optionally) a small `preview`.
- Do **not** expect bulk `data` to be inline.
- If you need full results, request them from your backend using `data_key`.

### 2) Context-default behavior is not automatic

The legacy executor could apply `AgentContext` defaults when `apply_context=True`.

The canonical executor (`ToolExecutor`) does **not** apply context defaults. If your UI previously relied on implicit defaults (e.g., current part number), you must apply them in your own orchestration layer (typically in your backend).

### 3) Public API exports moved to canonical

Prefer importing canonical entry points from `pywats_agent`:

- `ToolExecutor`
- `ToolResultEnvelope`
- `DataStore` / `InMemoryDataStore`
- `ToolRegistry` / `ToolProfile`

---

## The new data flow (recommended)

1. Frontend sends user message to your LLM backend.
2. Backend provides tool definitions (OpenAI function schemas) from `ToolExecutor`.
3. LLM produces a tool call.
4. Backend executes the tool via `ToolExecutor.execute(...)`.
5. Backend returns the **envelope** to the LLM (for reasoning) and to the frontend (for display).
6. If the frontend needs full data (tables/export), it asks the backend to resolve `data_key`.

The key idea: **the LLM never receives bulk rows**.

---

## Concrete payload examples

### Example: success with preview + data_key

```json
{
  "ok": true,
  "summary": "Yield analysis for WIDGET-001 grouped by station (last 7 days)…",
  "data_key": "ds_01jft2qv1y3c…",
  "preview": {
    "rows": [
      {"stationName": "Station-A", "fpy": 0.982, "units": 312},
      {"stationName": "Station-B", "fpy": 0.955, "units": 287}
    ]
  },
  "metrics": {
    "tool": "analyze_yield",
    "row_count": 5,
    "columns": ["stationName", "fpy", "units"],
    "preview_size_chars": 431,
    "data_key": "ds_01jft2qv1y3c…"
  },
  "warnings": [
    "Full data stored out-of-band; use data_key to retrieve"
  ]
}
```

### Example: tool not enabled

```json
{
  "ok": false,
  "summary": "Tool 'control_panel' is not enabled",
  "error": "tool_not_enabled",
  "metrics": {},
  "warnings": []
}
```

### Example: unexpected error

```json
{
  "ok": false,
  "summary": "Error executing 'analyze_yield': <message>",
  "error": "SomeException",
  "metrics": {},
  "warnings": []
}
```

---

## Frontend TypeScript types (suggested)

```ts
export type ToolResultPreview = {
  rows: Record<string, unknown>[];
};

export type ToolResultEnvelope = {
  ok: boolean;
  summary: string;
  data_key?: string | null;
  preview?: ToolResultPreview | null;
  metrics: Record<string, unknown>;
  warnings: string[];
  error?: string | null;
};
```

Rendering guidance:
- Always display `summary`.
- If `preview?.rows?.length`, show a small table.
- If `metrics.preview_truncated` is truthy, display a subtle “preview truncated” hint.
- Treat `data_key` as opaque.

---

## Backend: resolving `data_key`

`data_key` is a handle to a `DataStore` entry.

- In tests, `InMemoryDataStore` is used.
- In production, use a durable store (Redis, DB, blob store). Add TTL/expiry.

Backend pseudocode:

```python
# 1) execute
env = executor.execute(tool_name, params)

# 2) respond to UI
return {
  "tool": tool_name,
  "result": env.model_dump(),
}

# 3) resolve full data later
full = datastore.get(data_key)  # implement this on your backend
return {"data": full}
```

Security note:
- Treat `data_key` like a capability token. Scope it to the user/session.
- Apply authorization checks when resolving it.

---

## Tooling surface changes

### Tool definitions

- `ToolExecutor.get_tool_definitions()` returns OpenAI function schemas.
- `ToolExecutor.get_openai_tools()` returns `[{"type":"function","function": ...}]`.

### Tool set

The default registry includes (at least):
- `analyze_yield`
- `analyze_test_steps`
- `get_measurement_statistics`
- `get_measurement_data`
- `analyze_unit`
- `analyze_subunits`
- `control_panel`
- `analyze_root_cause`
- `analyze_failure_modes`
- `analyze_process_capability`

If you use profiles/allowlists, ensure the backend enables the tools the UI expects.

---

## Migration checklist

- [ ] Update result parsing to the envelope fields (`ok/summary/preview/data_key`).
- [ ] Stop relying on inline bulk `data`.
- [ ] Add a backend endpoint/mechanism to resolve `data_key` (optional, but required for full tables/exports).
- [ ] Move context defaults into your orchestration layer (UI or backend).
- [ ] Refresh tool list and descriptions in any UI tool-picker/debug panels.
