# ASSET Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and updated for `pywats.domains.asset`.

## 1. Service Functions
- **Overview:** `AssetService` orchestrates asset lifecycle workflows by delegating CRUD, status, state, and calibration/maintenance concerns to `AssetRepository`. It adds logging with structured events so calling code can rely on persistence + audit traces without touching HTTP details.
- **Key Operations:**
  - Basic CRUD (`get_assets`, `get_asset`, `create_asset`, `update_asset`, `delete_asset`) with optional OData filtering and serial/ID flexibility.
  - Status & state helpers (`get_status`, `get_asset_state`, `set_asset_state`, `is_in_alarm`, `is_in_warning`) that enrich repository responses before returning booleans or dictionaries.
  - Count & calibration helpers (`increment_count`, `reset_running_count`, `record_calibration`, `post_calibration`, `post_maintenance`) that wrap `AssetRepository` endpoints while emitting log lines when actions succeed.
  - Alarm/maintenance helpers (`get_assets_in_alarm`, `get_assets_in_warning`) that iterate through the asset ledger and reuse the translated status payload.
- **Open Questions:** The service mixes user-facing CRUD with heavy status polling; would splitting into `AssetInventoryService` (CRUD) and `AssetHealthService` (status/count/calc) reduce the surface area and make tests easier to reason about?

## 2. Model Surface
- **Model Files:**
  - `models.py` – defines `Asset`, `AssetType`, and `AssetLog`, each aligned with the alias-heavy WATS schema.
- **Class Summary:**
  - `Asset` – the canonical asset definition with status/metadata, hierarchical parent references, OEM counts, calibration windows, and lists for `asset_children` and `asset_log`.
  - `AssetType` – configuration for different asset categories (limits, thresholds, intervals, icons, readonly flag).
  - `AssetLog` – timestamped entries that track maintenance/calibration events tied to serial numbers.
- **Model Quality Notes:** All models live in one file even though `Asset` alone is ~200 lines; splitting `AssetLog`/`AssetType` into helper modules (or nested `models/` package) would make the intent clearer. The aliasing strategy is consistent, but some fields (e.g., `tags: List[Setting]`) could be shared via `shared.models` if other domains repeat the same pattern.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
AssetService ----------> AssetRepository ----------> HttpClient
AssetService ----------> Asset / AssetType / AssetLog data models
```

- **Refactor Ideas:** Provide a separate adapter for status-heavy flows so that `get_assets_in_alarm`/`get_status` do not traverse every asset every call; use a subset of repository helpers or caches when `translate` is turned off.

## 4. Inline Documentation
- **Domain Knowledge Additions:** Docstrings describe the OData parameters and log semantics, but the `AssetState` enum values (OK, MAINTENANCE, etc.) deserve inline reminders when transitions are triggered (e.g., `set_asset_state` should note when to switch from warning to alarm).
- **Doc Gaps:** `get_assets_in_alarm`/`get_assets_in_warning` barely note the performance hit of fetching status per asset; add a warning for consumers or create a bulk-status repository endpoint in the future.

## 5. Acceptance Testing
- **Test Scenarios:**
  1. `test_create_asset_calls_repository` – the service should build an `Asset` from the provided serial/type info, hand it to `AssetRepository.save`, and return the persisted model ([tests/acceptance/asset/test_asset_acceptance.py](tests/acceptance/asset/test_asset_acceptance.py)).
  2. `test_delete_asset_by_serial_number_resolves_identifier` – deleting via serial should resolve the asset by serial, use the retrieved ID, and confirm the repository delete call used the resolved identifier.
  3. `test_set_asset_state_updates_repository` – invoking `set_asset_state` with a friendly `AssetState` enum should translate to a repository call that includes the same serial and record the state change.
- **Data Setup Notes:** Use stub repositories that capture calls instead of hitting `HttpClient`. Create `Asset` placeholders with a `uuid4` type ID so validation passes.
- **Verification Steps:** Ensure the stub repository’s `saved`, `deleted`, and `state_updates` logs match the expectations for each scenario (serial/type, resolved IDs, state transitions).

## 6. Pending Work
- **Next Steps:** Extend acceptance tests to cover status polling (`get_status`) and lifecycle helpers (`record_calibration`/`post_maintenance`) with mocked status payloads.
- **Blockers:** Need an `HttpClient` stub or fixture that can feed deterministic alarm states before adding bulk status tests.
