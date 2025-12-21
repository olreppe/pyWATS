# Agent + toolset (LLM layer) — how it works

This document explains how the **`pywats_agent`** layer is structured, what problems it solves, and how a user question becomes one or more **tool calls** that return a final answer (optionally with a visualization payload).

> Scope: the *agent/tooling layer* (tool definitions, execution, selection guidance, results & visualization).  
> Not scope: the underlying domain services (e.g., `pywats.domains.*`) except where tools call into them.

---

## 1) Mental model

Think of the system as three cooperating pieces:

1. **LLM (planner / selector)**
   - Reads the user question.
   - Decides whether to call a tool.
   - Chooses which tool(s) and with what parameters.

2. **Tool runtime (executor)**
   - Receives a tool call request (tool name + arguments).
   - Validates arguments.
   - Creates a backend session (API client / auth / environment) as needed.
   - Runs tool logic.
   - Returns structured output + errors (if any).

3. **Result packaging**
   - Produces a final **text answer** for chat.
   - Optionally attaches **UI visualization payload** (charts/tables/KPIs) for front-ends.

The goal is that **tools do the deterministic work**, and the LLM does **selection + narration**.

---

## 2) Core concepts

### 2.1 Tools
A *tool* is a callable unit with:
- A **stable name** (used by the LLM to call it)
- A **description** (used by the LLM to decide when to call it)
- A **parameter schema** (so calls can be validated)
- An **implementation** that queries/aggregates data and returns results

Tools typically live under:

- `pywats_agent.tools.*`  
  - domain-focused tool modules (yield, steps, deviations, root cause, etc.)
  - shared helpers in `pywats_agent.tools.shared.*`

**Important rule:** public imports should come from `pywats_agent.tools` (not internal subpaths).  
This keeps tests and callers stable even if internal files move.

---

### 2.2 Tool descriptions and selection priority
Tool selection is largely driven by the **description text** you expose.

In this repository, descriptions are expected to include **selection markers** so the LLM reliably chooses the correct tool when multiple tools sound similar (example markers tested in CI):

- `PRIMARY TOOL` (the main tool for the task category)
- `SECONDARY TOOL` (use only when the primary tool doesn’t fit)
- `SPECIALIZED TOOL` / `INVESTIGATION TOOL` (narrow, expert tools)

This is not “cosmetic”: tests assert these markers exist and that certain tools actively **redirect** the LLM away from incorrect usage (e.g., step tool says “do not use for yield questions; use analyze_yield”).

**Why this matters:** LLMs tend to overuse “familiar” tools unless explicitly guided. Markers + redirect language reduce wrong-tool calls.

---

### 2.3 Sessions / API access
Most tools need a configured backend connection. The pattern is:

- Tool runtime / executor creates a session (auth, base URL, tenant, etc.)
- Tool implementation calls domain/service functions using that session
- Tools remain “thin”: parameter parsing + orchestration, not low-level HTTP

If you see “session creator” mentioned in exports, those are the helpers that standardize how tools obtain sessions.

---

### 2.4 Agent result model
A typical agent response is represented as a structured object (e.g., `AgentResult`) containing:

- `text` (final user-facing explanation)
- optional `data` (structured results useful to downstream code)
- optional **visualization payload** for UI (charts/tables/KPIs)

Two common serialization targets:
- **LLM / OpenAI-compatible output**: excludes large UI payloads by default
- **UI output**: includes visualization payload

This prevents sending large chart payloads back into the LLM context unnecessarily.

---

## 3) End-to-end flow (step-by-step)

### Step 0 — User asks a question
Example:
> “Show yield trend per day for the last 30 days, split by station.”

### Step 1 — LLM chooses a tool
Based on tool descriptions and markers:
- picks the **yield analysis tool** (PRIMARY TOOL)
- avoids step-analysis tool (SECONDARY TOOL) because description says not to use it for yield

### Step 2 — LLM emits a tool call
Tool call contains:
- tool name (e.g., `analyze_yield`)
- arguments JSON (date grouping, dimensions, filters, etc.)

### Step 3 — Tool executor validates and runs
Executor responsibilities:
- validate arguments against the tool schema
- create/obtain session
- call tool implementation
- catch exceptions and return structured error if needed

### Step 4 — Tool returns structured data (and optional viz)
Tool returns:
- aggregated results (rows, metrics)
- optionally: a chart payload (series + axes + reference lines)

### Step 5 — Agent returns final answer
Agent assembles:
- a short narrative (what was computed)
- key numeric highlights
- attaches visualization payload for UI (if present)

---

## 4) Visualization layer (charts/tables/KPIs)

The visualization component is designed to be:
- **serializable** (to `dict` / JSON)
- **UI-friendly** (front-end can render without extra logic)
- **optional** (agent still works without it)

### Common building blocks
- `ChartType` — enum of supported chart kinds (line, bar, pareto, control, scatter, etc.)
- `DataSeries` — one series of data points + series options
- `ReferenceLine` — target/limit lines (e.g., UCL/LCL, thresholds)
- `ChartPayload` — a full chart (type + series + metadata)
- `TablePayload` + `TableColumn` — tabular visualization
- `KPIPayload` — single KPI value, optional trend and thresholds
- `VizBuilder` — convenience builder for constructing payloads consistently
- `merge_visualizations` — merge multiple viz outputs into one payload (dashboards)
- `empty_visualization` — explicit “no viz” placeholder

### Why a builder exists
The builder enforces consistent output shape so:
- tools don’t handcraft JSON ad hoc
- tests can validate a stable contract
- UIs can render reliably

---

## 5) “Temporal” and adaptive time handling

Several tools accept time ranges like:
- “last 7 days”
- “last month”
- “per week”
- “period count”

The time subsystem typically does:
1. interpret user intent (explicit dates vs relative time)
2. choose grouping granularity (DAY/WEEK/MONTH)
3. decide whether to **omit** date boundaries when the API can compute them

**Design constraint (from tests):**  
If the user did *not* specify an explicit date range and the API can infer it (e.g., “period_count”), some tool calls should **omit `date_from` / `date_to`** to let the backend calculate defaults.

---

## 6) Shared helpers (`pywats_agent.tools.shared`)

Shared helpers exist to avoid duplicating logic across tools, such as:
- resolving process/station/product IDs from user-friendly names
- validation and normalization of dimensions/filters
- time parsing / grouping selection
- consistent session creation

### Runtime typing pitfall (important for 3.10+)
If a helper uses `TYPE_CHECKING` imports but references those types in runtime-evaluated annotations, Python 3.10 can raise `NameError`.

**Preferred patterns:**
- Add `from __future__ import annotations` at file top, **or**
- quote forward references: `-> "ProcessInfo"`

This is a common CI-only failure because local environments may differ.

---

## 7) Packaging and public API guarantees

### Public surface
Code outside the package (including tests) should only rely on:
- `pywats_agent` (top-level exports)
- `pywats_agent.tools` (tool exports)

Avoid importing from:
- `pywats_agent.tools.shared.*` directly (internal)
- deep module paths that can move

### Why this matters
- prevents “shadowing” issues where multiple `pywats_agent` directories exist
- makes refactors possible without breaking users/tests
- keeps installs consistent in CI

---

## 8) Adding a new tool (recommended checklist)

1. **Create the tool module**
   - Decide tool name and purpose
   - Keep implementation deterministic and testable

2. **Write a tool description**
   - Include an explicit selection marker:
     - `PRIMARY TOOL` / `SECONDARY TOOL` / `SPECIALIZED TOOL` / `INVESTIGATION TOOL`
   - Add “do not use when…” guidance if there’s overlap with other tools

3. **Define and validate parameters**
   - Use a schema model (pydantic/dataclass) if that’s the repo standard
   - Reject invalid dimensions and ambiguous filter combinations

4. **Add to `pywats_agent.tools.__init__`**
   - Ensure it is exported via the public API

5. **Add tests**
   - Selection tests (description markers / redirect text)
   - Parameter shaping tests (date omission rules, dimension normalization)
   - Result shape tests (data + optional viz)

---

## 9) Local “pre-release” verification

Before tagging a release, run the same checks CI runs (lint + tests) locally.

- PowerShell (Windows):
  - `.\scripts\pre_release_check.ps1`

This catches common release-breakers:
- flake8 undefined names (e.g., missing `Any`)
- import shadowing / wrong module paths
- runtime annotation `NameError` issues
- agent test suite failures (`api-agent-tests/`)

---

## 10) Troubleshooting guide (common failures)

### A) “ImportError: cannot import name X from pywats_agent”
Likely causes:
- missing export in `pywats_agent/__init__.py` or `pywats_agent/tools/__init__.py`
- package shadowing (two different `pywats_agent` folders on `PYTHONPATH`)

Fix:
- export the symbol in the public `__init__.py`
- ensure only one `pywats_agent` is installed/visible

---

### B) “NameError: ProcessInfo is not defined” (or similar)
Cause:
- runtime evaluation of annotations referencing a type only imported under `TYPE_CHECKING`

Fix:
- `from __future__ import annotations`, or quote the annotation

---

### C) PyPI publish fails: “File already exists”
Cause:
- same version/tag published once already; PyPI forbids re-upload of the same filename/version

Fix:
- bump version (next beta), rebuild and republish
- avoid force-pushing tags that already triggered publishing

---

## 11) Minimal usage examples

### Install (API package)
```bash
pip install pywats-api
```

### Import tools (public API)
```python
from pywats_agent.tools import (
    # examples — actual tool names depend on your exports
    # analyze_yield_tool,
    # analyze_test_steps_tool,
)
```

### Build a visualization (conceptual)
```python
from pywats_agent import VizBuilder

viz = (
    VizBuilder()
    .line_chart(title="Yield trend", x_label="Date", y_label="Yield (%)")
    # .add_series(...)
    .build()
)
```

---

## 12) What to read next in the codebase

If you want to trace behavior in source:
- `pywats_agent/__init__.py` — public exports
- `pywats_agent/executor.py` — tool execution runtime
- `pywats_agent/tools/__init__.py` — tool registry + public tool exports
- `pywats_agent/tools/shared/*` — shared resolvers/time parsing/session helpers
- visualization models & builder (where `VizBuilder`, payload models live)

---

### Notes / maintenance rules
- Keep tool descriptions explicit and stable (tests rely on markers).
- Keep imports “public” in tests and docs (avoid internal paths).
- Run the pre-release script before tagging.
- Treat Python 3.10 as the baseline (avoid runtime typing pitfalls).