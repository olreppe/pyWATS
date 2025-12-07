# Report Module Progress

This document reflects the CURRENT state of `ReportModule` (treated as source of truth).

## Public API Surface (current)

Implemented (no backend call):
- create_uut_report: Builds UUTReport (in-memory factory).
- create_uur_report: Builds UURReport (in-memory factory).
- export_report: Placeholder; returns target path only (no file writing yet).

Implemented (calls backend):
- submit_report: Persists (create/update) via WSJF POST endpoint (report_post_wsjf).
- find_report_headers: Calls report_header_query; lacks OData parameter support.
- delete_report: Calls internal report_delete_reports; success assumption (needs response validation).

Implemented (partial / incomplete):
- load_report: Calls report_get_report_as_wsjf successfully; WSJF -> UUT/UUR model conversion NOT implemented (always raises after fetch).

Placeholders (tagged "Move to ?" in code):
- get_production_statistics: Returns mock dict; awaits real statistics endpoint.
- get_quality_metrics: Returns mock dict; awaits real statistics endpoint.

## Removed / Clarified

- Former semantic confusion: A public `create_report` that performed submission has been eliminated (now only `submit_report` does network I/O).
- `_post_wsjf_report` is an internal helper used by `submit_report`.

## Current Status Summary

| Function | Network | Status | Next Action |
|----------|---------|--------|-------------|
| create_uut_report | No | Complete | None |
| create_uur_report | No | Complete | None |
| submit_report | Yes | Complete | Add optional update semantics doc |
| load_report | Yes | Incomplete | Implement WSJF → domain model parser |
| find_report_headers | Yes | Partial | Add OData params (filter/top/skip/orderby) |
| delete_report | Yes | Partial | Parse/verify response payload |
| export_report | No | Mock | Implement JSON/XML/CSV serialization |
| get_production_statistics | No | Placeholder | Replace with real endpoint when available |
| get_quality_metrics | No | Placeholder | Replace with real endpoint when available |

## TODO Backlog (Ordered)

1. Implement WSJF response parsing in `load_report`:
   - Map WSJF structure to UUTReport/UURReport (detect type from payload).
   - Handle attachments & chartdata integration.

2. Add OData parameter support to `find_report_headers`:
   - Update OpenAPI spec OR manually extend generated client.
   - Support: $filter, $top, $skip, $orderby.

3. Strengthen `delete_report`:
   - Inspect response structure (IDs deleted, error list).
   - Return bool based on actual outcome; optionally raise if not deleted.

4. Implement `export_report` serialization:
   - JSON: write file with `model_dump_json`.
   - XML: define mapping or simple dict->XML helper.
   - CSV: minimal flat export (header rows + measurements if present).

5. Decide on update semantics:
   - Document that `submit_report` is an upsert (server decides create/update).
   - Optionally introduce `update_report` as an alias if clarity needed.

6. Statistics placeholders:
   - Replace mocks once `statistics` endpoints are exposed in public API.
   - Provide unified parameter normalization (`_build_filter_params` reuse).

7. Error handling & logging:
   - Optional: integrate structured logging for network failures.

8. Type refinement:
   - Narrow `http_client` union if practical (protocol/interface).

## Deferred / Nice-to-Have

- Batch submission helper (submit multiple reports with partial failure strategy).
- Async variants (`async_submit_report`, etc.) if async client is supported.
- Caching layer for recently loaded reports.

## Risks / Notes

- Until load parsing is implemented, consumers cannot round-trip a report.
- Missing OData filters may cause performance issues for large datasets.
- Export without actual file output may mislead users; document clearly.

## Definition of Done Updates

A function is "Complete" when:
- Public docstring matches behavior.
- Network calls validate HTTP status and parse response.
- Returns domain models (not raw JSON).
- Raises `WATSException` (or subclass) with actionable message.

Current functions not meeting DoD: load_report, find_report_headers, delete_report, export_report, statistics placeholders.

--- 
Last updated: (auto)