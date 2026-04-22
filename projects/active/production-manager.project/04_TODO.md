# TODO — Production Manager

**Created:** April 8, 2026  
**Last Updated:** April 8, 2026

---

## Phase 1 — Rename & Restructure ✅

- ✅ Rename `src/pywats_ui/apps/sequence_designer/` → `production_manager/`
- ✅ Update `__init__.py` module docstring
- ✅ Update `main.py` (imports, app name, window class)
- ✅ Rename `SequenceDesignerWindow` → `ProductionManagerWindow` in `main_window.py`
- ✅ Update `launcher.py` (dict key, method name, import path, tray label)
- ✅ Rename `tests/ui/sequence_designer/` → `tests/ui/production_manager/`
- ✅ Update test import paths
- ✅ Verify app launches and tests pass (27/27 passing)

## Phase 2 — Toolbar Matching WATS ✅

- ✅ Add toolbar actions: Copy, Move to draft, Move to pending, Release, Delete, Revoke
- ✅ Implement `_update_toolbar_state()` for status-dependent enabling
- ✅ Add `ServerBridge` methods: `copy_definition()`, `update_definition_status()`
- ✅ Wire toolbar signals to ServerBridge
- ✅ Add confirmation dialogs for destructive actions (Delete/Revoke, Release)

## Phase 3 — Relations Tab CRUD ✅

- ✅ Add toolbar (+ Add, ✕ Delete, ✏ Edit) to `RelationsTab`
- ✅ Define `_RELATION_TYPES` mapping (Part number, Product revision, Serial number, Batch number)
- ✅ Implement inline add row with relation-type dropdown + value field + OK/Cancel
- ✅ Implement inline edit for existing rows
- ✅ Implement delete with confirmation
- ✅ Add `ServerBridge` methods: `create_relation()`, `delete_relation()`
- ✅ Wire signals to refresh table after mutations

## Phase 4 — Instructions (PDF) Tab ✅

- ✅ Create `widgets/instructions_tab.py`
- ✅ Implement file list table (Filename, Size, Uploaded date)
- ✅ Add toolbar (+ Add, ✕ Delete, 📥 Download)
- ✅ Implement file picker for PDF upload (POST Blob/mi)
- ✅ Implement download (GET Blob/mi) and delete (DELETE Blob/mi)
- ✅ Add `ServerBridge` methods: `load_media()`, `upload_media()`, `delete_media()`, `download_media()`
- ✅ Register tab in `main_window.py`

## Phase 5 — Header / Entity Count ✅

- ✅ Add header widget showing "Production manager" + entity count
- ✅ Update count when definitions load

## Phase 6 — Polish & Verification

- ✗ Add Blob routes to `src/pywats/core/routes.py` (currently using raw URLs in bridge)
- ✗ Definition tree: folder name resolution (pending API info)
- ✗ Definition tree: checkbox column for bulk operations
- ✗ Update CHANGELOG.md
- ✗ Run full test suite
- ✗ Verify all examples still work
