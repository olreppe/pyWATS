# PRODUCTION Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and updated for `pywats.domains.production`.

## 1. Service Functions
- **Overview:** `ProductionService` coordinates unit creation, verification, phase management, and assembly relationships. It caches phase metadata (via `UnitPhase`/`UnitPhaseFlag`) and exposes friendly helpers for unit verification grades, process updates, and parent/child attachments.
- **Key Operations:**
  - Unit CRUD (`get_unit`, `create_units`, `update_unit`) and verification (`verify_unit`, `get_unit_grade`, `is_unit_passing`).
  - Phase helpers (`get_phases`, `get_phase`, `get_phase_id`, `set_unit_phase`, `set_unit_process`) with base URL-aware caching to avoid repeated HTTP calls.
  - Unit change & assembly operations (`get_unit_changes`, `acknowledge_unit_change`, `add_child_unit`, `remove_child_unit`, `check_child_units`) that mirror real box build and repair flows.
- **Open Questions:** Should phase caching live in a dedicated `UnitPhaseCache` or `ProductionPhaseService` so consumers can rely on a single source of truth and the unit service can focus on coordination?

## 2. Model Surface
- **Model Files:**
  - `models.py` – includes `Unit`, `UnitChange`, `UnitPhase`, `ProductionBatch`, `UnitVerification`, `UnitVerificationGrade`, and `SerialNumberType`.
- **Class Summary:**
  - `Unit` – represents a production unit (serial, batch, location, phases, tags, sub-units, and optional product/revision links).
  - `UnitPhase` – captures server-defined phases (ID, code, name) and powers-of-two semantics referenced by `UnitPhaseFlag`.
  - `UnitChange` – tracks historical changes to parent relationships, part numbers, or phase IDs.
  - `UnitVerification` / `UnitVerificationGrade` – describe per-process verification results and aggregate pass/fail signals.
  - `SerialNumberType` / `ProductionBatch` – small helpers for serial number formatting and batch metadata.
- **Model Quality Notes:** The models cover numerous nested responsibilities; breaking them into a `/models` subpackage (e.g., `models/unit.py`, `models/verification.py`) would make targeted tests easier and shrink the import surface for repositories that only need a subset.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
ProductionService --> ProductionRepository --> HttpClient
ProductionService --> Unit / UnitPhase / UnitVerification models
```

- **Refactor Ideas:** The assembly helpers (adding/removing child units, checking child units) logically belong with production templates, so consider exposing a dedicated `ProductionAssemblyService` that keeps unit-level helpers inside a smaller core service.

## 4. Inline Documentation
- **Domain Knowledge Additions:** The large comment block in `ProductionService` clearly distinguishes between box build templates and runtime assemblies. Highlighting those flows is helpful, but the next step is to document expected failure modes (e.g., when `add_child_unit` is rejected) so testers know when to check logs versus repository returns.
- **Doc Gaps:** `get_unit_changes` mentions pagination via `$top/$skip` but `UnitChange` lacks guidance on how to interpret `new_unit_phase_id` values; add references to `UnitPhaseFlag` or the server docs.

## 5. Acceptance Testing
- **Test Scenarios:**
  1. `test_create_units_invokes_repository` – ensures `create_units` forwards a sequence of `Unit` objects to `ProductionRepository.save_units` and returns the repository result ([tests/acceptance/production/test_production_acceptance.py](tests/acceptance/production/test_production_acceptance.py)).
  2. `test_set_unit_phase_accepts_enum` – confirms `UnitPhaseFlag` input resolves to the numeric phase ID before calling `set_unit_phase` on the repository.
  3. `test_add_child_unit_routes_call` – verifies assembly helpers simply delegate to the repository when wiring parent/child serial numbers.
- **Data Setup Notes:** Use minimal `Unit` instances (serial + part number) so the service validation passes, and a stub repository captures call parameters instead of hitting `HttpClient`.
- **Verification Steps:** Assert the stub’s `saved_units`, `phase_calls`, and `child_calls` sequences match each scenario’s expectations.

## 6. Pending Work
- **Next Steps:** Add acceptance coverage for verification flows (`verify_unit`, `get_unit_grade`, `is_unit_passing`) and assembly checks (`check_child_units`).
- **Blockers:** Realistic verification payloads require replicating `UnitVerificationGrade.results`, so gather sample responses or reuse server fixtures before writing those tests.
