# PROCESS Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and updated for `pywats.domains.process`.

## 1. Service Functions
- **Overview:** The domain offers two entry points: `ProcessService` (public API + cache) for read-only lookups, and `ProcessServiceInternal` (internal API) for enriched process metadata, repair categories, and fail codes.
- **Key Operations:**
  - `ProcessService` manages an in-memory cache, exposes filtered getters (`get_test_operation`, `get_repair_operation`, `get_wip_operation`), and provides validation helpers plus default process-code resolution.
  - `ProcessServiceInternal` wraps `/api/internal/Process` endpoints to deliver full process entries, repair operation configurations, and flattened fail-code lists (`get_repair_categories`, `get_fail_codes`).
- **Open Questions:** Should the cache logic live in its own helper (e.g., `ProcessCache`) so automated refreshes can be reused by other services that need up-to-date process metadata?

## 2. Model Surface
- **Model Files:**
  - `models.py` – defines `ProcessInfo`, `RepairCategory`, and `RepairOperationConfig` with alias mapping for public/internal responses.
- **Class Summary:**
  - `ProcessInfo` – holds process identifiers, descriptive fields, and boolean flags; includes PascalCase support for internal endpoints.
  - `RepairCategory`/`RepairOperationConfig` – capture fail code hierarchies, masks, and metadata used by the internal service to determine valid repair choices.
- **Model Quality Notes:** The single file mixes public-facing fields with internal PascalCase data; consider splitting into `process.py` (public) and `repair.py` (internal configs) to keep the contract explicit.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
ProcessService --> ProcessRepository --> HttpClient
ProcessServiceInternal --> ProcessRepositoryInternal --> HttpClient
ProcessService --> ProcessInfo
ProcessServiceInternal --> RepairOperationConfig, RepairCategory
``` 

- **Refactor Ideas:** Introduce a shared `ProcessCache` helper that both services can reuse (internal API could still prime it for non-public clients).

## 4. Inline Documentation
- **Domain Knowledge Additions:** `ProcessService.refresh` now documents the threading lock and cache invalidation to emphasize thread safety. `ProcessRepositoryInternal` highlights the Referer header requirement and PascalCase mapping.
- **Doc Gaps:** `get_repair_operation_configs` currently returns raw dicts—consider documenting expected schema or wrapping in value objects so callers know what keys to expect.

## 5. Acceptance Testing
- **Test Scenarios:**
  1. `test_refresh_populates_cache` – validates that refreshing loads the cache from `get_processes` and updates the timestamp.
  2. `test_get_test_operation_by_name` – ensures the lookup returns the correct `ProcessInfo` when matching on name.
  3. `test_get_default_repair_code` – confirms the fallback value is pulled from the cached repair operation.
  All tests are located in [tests/acceptance/process/test_process_acceptance.py](tests/acceptance/process/test_process_acceptance.py).
- **Data Setup Notes:** Acceptance tests configure a dummy repository that returns three sample entries (test/repair/WIP).
- **Verification Steps:** Assert the stub repository call counts and returned values match expectations.

## 6. Pending Work
- **Next Steps:** Add coverage for `ProcessServiceInternal` (repair configs and fail-code flattening) with fixtures representing internal API responses.
- **Blockers:** Need more structured sample data from Product/Report teams before automating fail-code validations.