# WATS New / What’s New — spec (implementation intentionally removed)

This document captures the intended behavior for a future **“WATS New / What’s New”** reporting tool.

Status: **SPEC ONLY**. The previous prototype implementation and tests were removed to avoid disrupting the current toolset.

---

## Goal

Provide an **enterprise-first “what changed?”** summary for quality/yield KPIs over a recent time window (e.g., last 7/30 days), then guide drill-down into the most actionable drivers.

The tool should answer:
- “What got better / worse since the prior equal period?”
- “Where (product / station / process) did it change most?”
- “What failure modes or steps are driving the change?”

---

## Inputs (minimal)

Recommended parameters (keep small; avoid over-flexibility):
- `period_count` (int): window size in days (default 7 or 30)
- Optional scoping:
  - `part_number` or `product_group`
  - `station_name`
  - `process_code`
- `top_n` (int): how many “movers” to show (default 5–10)

If the user did not supply explicit `date_from/date_to`, prefer using `period_count` and let the backend compute boundaries.

---

## Outputs

### 1) Executive summary (single screenful)
Return a short text summary plus structured data suitable for a table:
- Overall yield KPIs for current period (FPY, units)
- Trend vs prior equal period
- “Confidence / caveats” notes when comparisons are unreliable

### 2) Top movers (guided drill-down)
Rank the largest changes by a few stable dimensions:
- By `partNumber`
- By station/level
- By process

Then for each top mover, provide:
- current yield
- delta vs prior
- volume (unit_count)

### 3) Root drivers (actionable)
For the top 1–3 movers:
- top failed steps / failure signatures
- optionally: step analysis to show which test step(s) contribute most
- link out identifiers needed to run existing tools (yield / root cause / dimensional)

---

## Trend handling (important)

Many WATS yield/KPI responses already include **built-in trend deltas** vs the prior equal period.

### Preferred approach
- **Use backend-provided delta fields when present** to avoid extra baseline queries.

### “0% fallback” caveat
Backend may sometimes return `+0%/-0%` when the prior period has no data or the baseline fields are missing.

Tool behavior:
- If delta fields are present but baseline context appears missing, include a caution note like:
  - “Trend may be a fallback (prior-period baseline missing); treat 0% deltas carefully.”

---

## How this composes with existing tools

This tool should not replace existing deep tools; it should route to them:
- Yield tool: confirm the KPI change and validate volumes
- Dimensional analysis: identify which slices moved most
- Root cause: translate the change into likely failure categories
- Debug tool: verify connectivity/health when queries fail

---

## Implementation notes (for later)

- Avoid adding new client-model fields purely for trend keys unless they are stable; prefer extracting unknown keys from raw payloads when available.
- Be mindful of packaging/import behavior: if `pywats` is imported from site-packages during tests, local edits to `src/pywats/...` won’t be exercised unless installed editable.

---

## Test plan (for later)

Minimum tests:
1. Schema/definition exists (name/description/parameters)
2. Non-mocked “smoke” execution against a real server fixture (skippable when not configured)
3. Output always includes:
   - summary text
   - structured table-like data for top movers
   - explicit warning when trend reliability is questionable
