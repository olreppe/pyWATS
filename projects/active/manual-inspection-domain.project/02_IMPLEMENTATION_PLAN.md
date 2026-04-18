# Implementation Plan — Manual Inspection Domain

**Created:** March 20, 2026  
**Last Updated:** March 21, 2026

---

## Codebase Conventions (from review)

Before implementing, the following actual patterns were verified against the existing domains:

| Convention | Detail |
|------------|--------|
| **Async-only implementation** | All domains use only `async_repository.py` + `async_service.py`. No separate `service.py` / `repository.py`. Sync access is provided automatically via `SyncServiceWrapper` in `pywats.py`. |
| **Routes pattern** | Routes are nested classes inside the global `Routes` class in `src/pywats/core/routes.py`. All ManualInspection endpoints are internal-only and go under a nested `Internal` class (e.g. `Routes.ManualInspection.Internal.GET_DEFINITIONS`). |
| **Internal API Referer header** | Internal API calls require a `Referer` header set to `base_url`. Repositories accept `base_url` and use a shared `_internal_get()` helper. |
| **Model base** | Models inherit from `PyWATSModel` (Pydantic). Use `validation_alias` + `serialization_alias` for PascalCase API fields. |
| **Registration** | Each new domain requires two changes: (1) add to `src/pywats/domains/__init__.py`, (2) add `@property` in `pyWATS` class in `src/pywats/pywats.py` returning a `SyncServiceWrapper`. |
| **`__init__.py` exports** | Domain `__init__.py` exports models + async classes via `__all__`. |

---

## API Endpoints to Cover

All endpoints live under `/api/internal/ManualInspection/`.

| Method | Endpoint | Purpose | Priority |
|--------|----------|---------|----------|
| `GET` | `GetTestSequenceDefinitions` | List all MI definitions | P0 |
| `GET` | `GetTestSequenceDefinition` | Get single definition by id | P0 |
| `GET` | `GetDefinitionCopy/{Id}` | Get a copy of a definition | P1 |
| `GET` | `GetInstancesCount/{Id}` | How many instances of a definition | P1 |
| `GET` | `GetMiDetails/{id}` | MI details for a unit (legacy) | P1 |
| `GET` | `GetMiDetailsNew/{id}` | MI details for a unit (preferred) | P0 |
| `GET` | `GetRelations/{Id}` | Relations for a definition | P0 |
| `GET` | `GetRelationConflicts/{Id}` | Relation conflicts (legacy) | P1 |
| `GET` | `GetRelationConflictsNew/{Id}` | Relation conflicts (preferred) | P0 |
| `GET` | `GetSequences` | List sequences | P1 |
| `GET` | `GetTestSequenceDefinitionXaml` | XAML content for a definition | P2 |
| `GET` | `GetWatswwfContent/{Id}` | Workflow binary file | P2 (deferred — binary/stream) |
| `POST` | `PostDefinition` | Create new MI definition | P0 |
| `POST` | `PostRelation` | Create relation | P0 |
| `PUT` | `PutDefinitionNew` | Update definition | P0 |
| `PUT` | `PutRelation` | Update relation | P0 |
| `PUT` | `PutSequence` | Update sequence | P1 |
| `PUT` | `PutStringTest` | Update string test | P1 |
| `PUT` | `PutTestSequenceDefinitionXaml` | Update XAML content | P2 |
| `PUT` | `ValidateMiscInfo` | Validate misc info | P1 |
| `PUT` | `DeleteRelationNew` | Remove relation (uses PUT, not DELETE) | P0 |
| `DELETE` | `DeleteSequence` | Delete sequence | P1 |

> **Open questions (from `01_ANALYSIS.md`):**
> 1. `GetMiDetails` vs `GetMiDetailsNew` — expose both or only preferred?  
> 2. Are XAML/WWF endpoints needed for initial release? (Currently P2 / deferred)  
> 3. What C# models define request/response shapes for `PostDefinition` and `PutDefinitionNew`?

---

## Phase 1 — Models (`models.py`)

**File:** `src/pywats/domains/manual_inspection/models.py`

Define Pydantic models (inherit `PyWATSModel`) for:

| Class | Purpose | Key fields (TBC from C# reference) |
|-------|---------|--------------------------------------|
| `ManualInspectionDefinition` | Definition entity | `id`, `name`, `part_number`, `revision`, `description` |
| `ManualInspectionRelation` | Link between definition and product/process | `id`, `definition_id`, `product_id`, `process_id`, `active` |
| `ManualInspectionSequence` | Inspection step sequence | `id`, `definition_id`, `steps` (list) |
| `MiDetails` | Per-unit inspection result | `unit_id`, `definition_id`, `status`, `completed_at` |
| `RelationConflict` | Conflict info | `relation_id`, `conflict_type`, `description` |

> Reference `reference/csharp_report_models/` and `reference/csharp_code_CORE/` for field names.  
> All API fields use PascalCase — map them with `validation_alias`/`serialization_alias`.

---

## Phase 2 — Routes

**File:** `src/pywats/core/routes.py`

Add `ManualInspection` as a nested class inside `Routes` (following the same pattern as `Routes.Product`, `Routes.Asset`, etc.):

```python
class ManualInspection:
    """⚠️ Internal Manual Inspection API routes."""
    BASE = "/api/internal/ManualInspection"

    class Internal:
        """All ManualInspection endpoints are internal-only."""
        BASE = "/api/internal/ManualInspection"

        GET_DEFINITIONS = f"{BASE}/GetTestSequenceDefinitions"
        GET_DEFINITION = f"{BASE}/GetTestSequenceDefinition"
        GET_SEQUENCES = f"{BASE}/GetSequences"
        POST_DEFINITION = f"{BASE}/PostDefinition"
        PUT_DEFINITION = f"{BASE}/PutDefinitionNew"
        POST_RELATION = f"{BASE}/PostRelation"
        PUT_RELATION = f"{BASE}/PutRelation"
        DELETE_RELATION = f"{BASE}/DeleteRelationNew"
        VALIDATE_MISC_INFO = f"{BASE}/ValidateMiscInfo"
        GET_XAML = f"{BASE}/GetTestSequenceDefinitionXaml"
        PUT_XAML = f"{BASE}/PutTestSequenceDefinitionXaml"
        PUT_SEQUENCE = f"{BASE}/PutSequence"
        PUT_STRING_TEST = f"{BASE}/PutStringTest"

        @staticmethod
        def get_definition_copy(definition_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetDefinitionCopy/{definition_id}"

        @staticmethod
        def get_instances_count(definition_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetInstancesCount/{definition_id}"

        @staticmethod
        def get_mi_details(unit_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetMiDetails/{unit_id}"

        @staticmethod
        def get_mi_details_new(unit_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetMiDetailsNew/{unit_id}"

        @staticmethod
        def get_relations(definition_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetRelations/{definition_id}"

        @staticmethod
        def get_relation_conflicts(definition_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetRelationConflicts/{definition_id}"

        @staticmethod
        def get_relation_conflicts_new(definition_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetRelationConflictsNew/{definition_id}"

        @staticmethod
        def get_wwf_content(definition_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/GetWatswwfContent/{definition_id}"

        @staticmethod
        def delete_sequence(sequence_id: int) -> str:
            return f"{Routes.ManualInspection.Internal.BASE}/DeleteSequence/{sequence_id}"
```

---

## Phase 3 — Repository (`async_repository.py`)

**File:** `src/pywats/domains/manual_inspection/async_repository.py`

Thin data-access layer — each public method maps 1:1 to an endpoint. No business logic.

Pattern: mirrors `AsyncProcessRepository`.
- Constructor takes `http_client`, `error_handler`, `base_url` 
- All calls go through `_internal_get()` / `_internal_post()` / `_internal_put()` / `_internal_delete()` helpers that attach the `Referer` header
- Returns raw dicts/lists; deserialization happens in the service layer

Method groups:
```
Definitions:  get_definitions(), get_definition(id), get_definition_copy(id), get_instances_count(id)
              post_definition(payload), put_definition(payload)
Relations:    get_relations(definition_id), get_relation_conflicts(id), get_relation_conflicts_new(id)
              post_relation(payload), put_relation(payload), delete_relation(payload)
Sequences:    get_sequences(), put_sequence(payload), delete_sequence(id)
Unit details: get_mi_details(unit_id), get_mi_details_new(unit_id)
Misc:         validate_misc_info(payload), put_string_test(payload)
XAML (P2):    get_xaml(definition_id), put_xaml(definition_id, content)
WWF (P2):     get_wwf_content(definition_id)  ← returns bytes
```

---

## Phase 4 — Service (`async_service.py`)

**File:** `src/pywats/domains/manual_inspection/async_service.py`

Business logic layer — provides typed, user-friendly API. Deserializes raw dicts into model instances.

> **No `service.py`** — sync access is provided via `SyncServiceWrapper` in `pywats.py` (same pattern as all other domains).

Method groups:
```
list_definitions() → List[ManualInspectionDefinition]
get_definition(id) → ManualInspectionDefinition
create_definition(name, ...) → ManualInspectionDefinition
update_definition(id, ...) → ManualInspectionDefinition
copy_definition(id) → ManualInspectionDefinition
get_instances_count(id) → int
get_mi_details(unit_id) → MiDetails          (prefers _new variant)
list_relations(definition_id) → List[ManualInspectionRelation]
get_relation_conflicts(definition_id) → List[RelationConflict]  (prefers _new variant)
create_relation(definition_id, ...) → ManualInspectionRelation
update_relation(...) → ManualInspectionRelation
delete_relation(...) → None
list_sequences() → List[ManualInspectionSequence]
update_sequence(...) → None
delete_sequence(id) → None
validate_misc_info(...) → dict
put_string_test(...) → dict
```

> Caching: this domain is unlikely to need TTL caching (data is mutable CRUD) — no cache layer planned unless benchmarks show otherwise.

---

## Phase 5 — Domain Registration

**Two files must be updated:**

### 5a — `src/pywats/domains/manual_inspection/__init__.py`
```python
from .models import ManualInspectionDefinition, ManualInspectionRelation, \
    ManualInspectionSequence, MiDetails, RelationConflict
from .async_repository import AsyncManualInspectionRepository
from .async_service import AsyncManualInspectionService

__all__ = [
    "ManualInspectionDefinition", "ManualInspectionRelation",
    "ManualInspectionSequence", "MiDetails", "RelationConflict",
    "AsyncManualInspectionRepository", "AsyncManualInspectionService",
]
```

### 5b — `src/pywats/domains/__init__.py`
Add `from . import manual_inspection` and include in `__all__`.

### 5c — `src/pywats/pywats.py`
Add `@property def manual_inspection(self) -> SyncServiceWrapper:` on the `pyWATS` class, constructing `AsyncManualInspectionRepository` + `AsyncManualInspectionService` and wrapping in `SyncServiceWrapper`. Follow the `process` property as template.

---

## Phase 6 — Tests

**Files:**
- `tests/domains/manual_inspection/test_models.py` — model parse/serialize round-trips
- `tests/domains/manual_inspection/test_repository.py` — mocked HTTP, assert correct URLs and Referer header
- `tests/domains/manual_inspection/test_service.py` — mocked repository, assert model deserialization + logic

---

## Phase 7 — Docs & Examples

- `examples/manual_inspection/basic_usage.py` — list definitions, get MI details for a unit, create a relation
- Update `CHANGELOG.md` under `[Unreleased]`
- Update `README.md` if domain listing is present

---

## Deferred / Out of Scope (Phase 1)

| Item | Reason |
|------|--------|
| `GetWatswwfContent` | Returns binary workflow file; needs special stream handling |
| XAML PUT/GET (`PutTestSequenceDefinitionXaml`, `GetTestSequenceDefinitionXaml`) | Niche use case; defer to follow-up iteration |
| Sphinx RST API docs | After implementation is stable |

---

---

# Phase 2 — Manual Inspection Apps in `pywats_ui`

> **Depends on:** Phase 1 complete (ManualInspection domain available in pyWATS)

## Overview

Two new apps are added to `src/pywats_ui/apps/`, sitting alongside `configurator`,
`yield_monitor`, `aichat`, etc.:

| App | Path | Purpose |
|-----|------|---------|
| **Sequence Designer** | `src/pywats_ui/apps/sequence_designer/` | Author and manage MI definitions, steps, and relations — the authoring tool |
| **Operator Interface** | `src/pywats_ui/apps/operator_interface/` | Shop-floor execution of any manual work — scan unit, step through sequence, submit results |

Both apps follow the `pywats_ui` app conventions (see `src/pywats_ui/.agent_instructions.md`)
and reuse the existing framework, widgets, and launcher infrastructure.

## Application Structure

```
src/pywats_ui/apps/
├── sequence_designer/
│   ├── __init__.py
│   ├── main_window.py             # Definition list + editor shell
│   ├── views/
│   │   ├── definition_list_view.py  # Browse / create / delete definitions
│   │   ├── sequence_editor_view.py  # Drag-and-drop step authoring
│   │   ├── step_config_panel.py     # Per-step configuration sidebar
│   │   └── relation_manager_view.py # Link definitions to products/processes
│   └── widgets/                   # App-specific reusable widgets
└── operator_interface/
    ├── __init__.py
    ├── main_window.py             # OI shell / navigation
    ├── engine/                    # Sequence execution engine
    │   ├── executor.py              # Drives step transitions
    │   ├── session.py               # Active inspection session state
    │   └── result_builder.py        # Constructs UUTReport from results
    ├── views/
    │   ├── unit_scan_view.py        # Scan / enter serial number
    │   ├── sequence_view.py         # Step-by-step inspection screen
    │   └── result_summary_view.py   # Per-unit result review
    └── config/
        └── oi_config.py             # Station / layout config (pyScript Phase 3)
```

## Operator Workflow

```
1. Operator scans / enters serial number
2. OI resolves matching MI sequence (via relation lookup on product/process)
3. Sequence loads; operator steps through each inspection item
4. Results recorded per step (pass/fail/value/comment)
5. On completion, UUTReport submitted to WATS via pyWATS
6. Summary shown; ready for next unit
```

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| GUI framework | PySide6 (Qt6) — same as rest of `pywats_ui` | Consistent with existing apps |
| Packaging | Part of `pywats_ui` package, not standalone | Reuses framework, launcher, widgets |
| Async/sync | Sync pyWATS calls in QThread worker | Avoids blocking Qt event loop |
| Auth | Same token as pyWATS / existing `pywats_ui` config | Re-uses existing config mechanism |
| Result format | Standard UUTReport via `pyWATS.report` | Full WATS compatibility |
| Layout config | Static first, pyScript in Phase 3 | Incremental complexity |
| App entry points | Registered in `pywats_ui` launcher like other apps | Consistent UX for all apps |

## Open Questions

1. Should Sequence Designer and Operator Interface share any widgets/engine code, or stay completely separate?
2. Does OI need offline/disconnected mode (queue results locally)?
3. Should OI be launchable standalone (direct entry point) in addition to via the launcher?

---

---

# Phase 3 — Extended Step Types

> **Depends on:** Phase 2 OI engine stable and integrated with Phase 1

## Overview

Extended step types are executed **locally by the OI engine**. WATS sees only the final
UUTReport outputs — these are not new WATS server features. The OI engine interprets
them on-device.

## Step Type Specifications

### 3.1 Conditional Flow

Add if/else, for/next (loop), and goto-style branching to sequences/subsequences.

- **Condition expressions:** Reference step results by name/index
- **Implementation:** OI `executor.py` evaluates conditions before advancing
- **WATS output:** Conditional steps may produce skipped/bypassed step records
- **Expression language:** Candidate for pyScript (see 3.7)

### 3.2 Dynamic Subsequence Call

Call a subsequence by a computed name rather than a hardcoded reference.

- **Name sources:** Part number, scanned tag value, pyWATS product tag, any session variable
- **Resolution:** OI engine resolves name at runtime, loads matching subsequence definition
- **Fallback:** Configurable — skip, fail, or prompt operator if name resolves to nothing

### 3.3 Multi-Numeric Limit Step

A single inspection step presenting multiple measurement inputs, each with its own limit.

- **UI:** Multiple numeric input fields in one step card
- **Pass/fail:** Configurable — all must pass, or majority, or custom logic
- **WATS output:** Multiple numeric measurement sub-steps under one parent step

### 3.4 Advanced Box Build

Integration with `pyWATS.product.BoxBuild` templates for assembly/component tracking.

- **Flow:** OI fetches BoxBuild template for the current part number, operator scans component serial numbers
- **Validation:** Component serial numbers validated against template constraints
- **WATS output:** Populated BoxBuild report submitted alongside UUTReport
- **Dependency:** Requires Product domain BoxBuild API (`src/pywats/domains/product/`)

### 3.5 Relative Limits

Limits derived from the results of earlier steps in the same sequence.

- **Example:** Step B limit = Step A value ± 5%
- **Expression syntax:** `{step_a.value} * 1.05` (candidate for pyScript)
- **Evaluation:** OI engine resolves expressions at the moment the step is reached
- **WATS output:** Resolved numeric limits stored in measurement record

### 3.6 Batch Inspection

Work on multiple units simultaneously in one OI session.

- **Scan mode:** Operator scans 1..N units at session start
- **Step modes:**
  - **All units:** Same step presented once, result applied to all
  - **Per-unit:** Step presented individually for each unit
  - **Selection:** Operator selects which units to include in a step
- **Session state:** `session.py` extended to hold `List[UnitSession]`
- **WATS output:** Separate UUTReport submitted per unit

### 3.7 Python Step

Fully configurable step running an operator-defined Python script.

- **Script scope:** Can read/write `UUTReport`, display custom UI in OI, read session variables
- **Security model (TBD):** Options:
  - Trusted-scripts-only (hash-verified at load time)
  - Restricted globals (no `import os`, `subprocess`, etc.)
  - Isolated subprocess with IPC to OI
- **API surface exposed to scripts:**
  ```python
  step.result          # Read/write step result
  session.unit         # Current unit under test
  session.report       # UUTReport builder
  oi.show_prompt(msg)  # Display message in OI GUI
  oi.ask_value(label)  # Prompt operator for input
  ```

## pyScript — Scripting/Markup Language

A lightweight language for two purposes:
1. **GUI layout config:** Define OI screen layout, colors, field visibility without Python
2. **Step expressions:** Condition expressions, relative limits, dynamic names

**Approach options (decision needed):**

| Option | Pros | Cons |
|--------|------|------|
| Restricted Python subset (safe `eval`) | Familiar syntax, easy to implement | Security surface harder to audit |
| Custom mini-DSL (parsed with `lark` or similar) | Full control, minimal attack surface | More upfront work |
| Jinja2 / template expressions | Proven, well-documented | Template syntax unfamiliar to operators |

**Recommended path:** Start with restricted Python `eval` (allowlist of safe builtins), prototype
for relative limits and condition expressions. Evaluate if a true DSL is warranted once usage patterns
are clearer.

## Phase 3 Open Questions

1. **pyScript:** Custom DSL vs. restricted Python subset vs. template language?
2. **Python step security:** Sandboxed subprocess vs. restricted eval globals?
3. **Batch inspection:** Same OI window, or separate batch view/mode?
4. **Relative limits and WATS:** How do resolved dynamic limits map to WATS measurement limit fields?
5. **Sequence engine refactor:** Does Phase 3 require a significant rewrite of the Phase 2 executor?
