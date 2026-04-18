# TODO — Manual Inspection Domain

**Created:** March 20, 2026  
**Last Updated:** March 25, 2026

---

## Phase 1 — pyWATS ManualInspection Domain ✅

### 1.1 Models (`src/pywats/domains/manual_inspection/models.py`)
- ✅ Define `TestSequenceDefinition` model (17 fields from C# reference)
- ✅ Define `TestSequenceRelation` model (7 fields)
- ✅ Define `TestSequenceInstance` model (8 fields)
- ✅ Define `RelationConflict` model (6 fields)
- ✅ Define `MiSequence` model (4 fields)
- ✅ Verify field names against C# reference

### 1.2 Routes (`src/pywats/core/routes.py`)
- ✅ Add `Routes.ManualInspection.Internal` nested class (all endpoints internal-only)

### 1.3 Repository (`src/pywats/domains/manual_inspection/async_repository.py`)
- ✅ Implement `AsyncManualInspectionRepository`
- ✅ Add `_internal_get/post/put/delete` helpers (Referer header required)
- ✅ Cover all P0 and P1 endpoints

### 1.4 Service (`src/pywats/domains/manual_inspection/async_service.py`)
- ✅ Implement `AsyncManualInspectionService`
- ✅ No separate sync service — SyncServiceWrapper handles it

### 1.5 Registration
- ✅ Create `src/pywats/domains/manual_inspection/__init__.py`
- ✅ Add `from . import manual_inspection` to `src/pywats/domains/__init__.py`
- ✅ Add `@property def manual_inspection` to `pyWATS` class in `src/pywats/pywats.py`

### 1.6 Tests (49 passing)
- ✅ `tests/domains/manual_inspection/test_models.py` (15 tests)
- ✅ `tests/domains/manual_inspection/test_repository.py` (21 tests)
- ✅ `tests/domains/manual_inspection/test_service.py` (13 tests)

### 1.7 Docs & Examples
- ✅ `examples/domains/manual_inspection_examples.py`
- ✅ Update `CHANGELOG.md`

### Deferred (Phase 1)
- ✗ XAML endpoints (P2)
- ✗ WWF binary endpoint (P2, needs stream handling)
- ✗ Sphinx RST docs

---

## Phase 2 — Manual Inspection Apps in `pywats_ui`

> Starts after Phase 1 is stable  
> Both apps live in `src/pywats_ui/apps/`

### 2A — Sequence Designer (`sequence_designer/`)
- ✗ Scaffold app in `src/pywats_ui/apps/sequence_designer/`
- ✗ Register in `pywats_ui` launcher
- ✗ Definition list view (browse / create / delete)
- ✗ Sequence editor view (step authoring)
- ✗ Per-step configuration panel
- ✗ Relation manager view (link definitions to products/processes)

### 2B — Operator Interface (`operator_interface/`)
- ✗ Scaffold app in `src/pywats_ui/apps/operator_interface/`
- ✗ Register in `pywats_ui` launcher
- ✗ Unit scan / serial number entry view
- ✗ Sequence loader (resolves sequence from product/process relation)
- ✗ Step execution screen + OI execution engine (`engine/`)
- ✗ Result builder → UUTReport construction
- ✗ Submit results to WATS via pyWATS
- ✗ Result summary view
- ✗ Basic layout configuration (station name, branding)

---

## Phase 3 — Extended Step Types

> Starts after Phase 2 OI engine is stable

- ✗ Conditional flow (if/else, for/next branching in executor)
- ✗ Dynamic subsequence call (runtime name resolution)
- ✗ Multi-numeric limit step (multiple inputs + limits in one step)
- ✗ Advanced box build integration (product.BoxBuild templates)
- ✗ Relative limits (step expression evaluation)
- ✗ Batch inspection mode (multi-unit session)
- ✗ Python step (configurable script with OI/UUTReport API access)
- ✗ pyScript prototype (expression language for limits / conditions)
- ✗ Security model decision for Python steps
