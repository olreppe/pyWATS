# APP Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and updated for `pywats.domains.app`.

## 1. Service Functions
- **Overview:** `AppService` surfaces KPIs, statistical chases, and reporting insights by wrapping `AppRepository` helpers with domain-friendly method names; it also reuses `WATSFilter`/`ReportHeader` from the `report` domain to keep filter construction consistent.
- **Key Operations:**
  - System metadata (`get_version`, `get_processes`, `get_levels`, `get_product_groups`).
  - Yield/reliability KPIs (`get_dynamic_yield/repair`, `get_volume_yield`, `get_high_volume`, `get_worst_yield`, `get_top_failed`, `get_test_step_analysis`).
  - Metric analyses (`get_aggregated_measurements`, `get_measurements`, `get_oee_analysis`) plus related repair/history helpers (`get_related_repair_history`, `get_serial_number_history`, `get_uut_reports`, `get_uur_reports`).
  - Convenience helpers that build `WATSFilter` payloads from product codes (`get_yield_summary`).
- **Open Questions:** Should some of the heavy analytics methods (e.g., `get_high_volume`, `get_worst_yield`, `get_oee_analysis`) be grouped into a secondary `AnalyticsService` so callers can pick the area they need without the 200+ line `AppService` surface?

## 2. Model Surface
- **Model Files:**
  - `models.py` – defines `YieldData`, `ProcessInfo`, `LevelInfo`, and `ProductGroup`, all inheriting from `PyWATSModel` with explicit aliasing for WATS JSON keys.
- **Class Summary:**
  - `YieldData` – flexible yield metrics supporting multiple pass yield types and counts.
  - `ProcessInfo` – modeling process flags (test/repair/WIP) with backward-compatible `process_code`/`process_name` aliases.
  - `LevelInfo`/`ProductGroup` – small DTOs used by combo boxes/filters.
- **Model Quality Notes:** `ProcessInfo` carries both public and internal metadata (properties, `process_id`), so splitting the public subset from the internal fields might keep the domain-specific contract leaner.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
AppService --> AppRepository --> HttpClient
AppService --> WATSFilter / ReportHeader
AppService --> YieldData / ProcessInfo models
```

- **Refactor Ideas:** Introduce an `AppAnalyticsService` for heavy POST/filters and keep `AppService` as the orchestrator for user-facing KPI entry points.

## 4. Inline Documentation
- **Domain Knowledge Additions:** The service docstrings now call out the data sources (GET vs POST) so callers know which endpoints run after filtering. `ProcessInfo` carries `process_code` and `process_name` properties to keep backwards compatibility with older API consumers.
- **Doc Gaps:** The difference between `get_high_volume`/`get_high_volume_by_product_group` (POST vs GET) could be highlighted near the method docstrings to avoid accidental misuse of GET URLs when a filter object is provided.

## 5. Acceptance Testing
- **Test Scenarios:**
  1. `test_get_processes_uses_repository` – ensures `AppService.get_processes` proxies to the repository and returns `ProcessInfo` instances.
  2. `test_get_dynamic_yield_passes_filters` – verifies `WATSFilter` objects are forwarded unchanged to `AppRepository.get_dynamic_yield`.
  3. `test_get_serial_number_history_forwards_filters` – confirms the serial history helper just returns the repository list of `ReportHeader`s.
  All tests live under [tests/acceptance/app/test_app_acceptance.py](tests/acceptance/app/test_app_acceptance.py).
- **Data Setup Notes:** Tests rely on a dummy repository that returns lightweight models and records the last filter arguments.
- **Verification Steps:** Assert the stub repository captured calls, filter objects, and returned headers.

## 6. Pending Work
- **Next Steps:** Expand acceptance coverage for the high-volume/worst-yield analytics (especially POST-based methods) and add unit tests around `get_yield_summary` helper wiring.
- **Blockers:** No major blockers—need representative data for the POST helper methods to make assertions meaningful.