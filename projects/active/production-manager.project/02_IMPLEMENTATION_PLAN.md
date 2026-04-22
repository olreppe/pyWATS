# Implementation Plan — Production Manager

**Created:** April 8, 2026  
**Last Updated:** April 8, 2026

---

## Overview

Rename and restructure the `sequence_designer` app into `production_manager` — a unified
UI matching the WATS web "Production Manager" view. The sequence designer becomes one tab
among four. The Relations tab gets full CRUD with a relation-type dropdown, and a new
Instructions (PDF) tab is added.

---

## Existing Codebase (What We Have)

| File | Status | Reuse Plan |
|------|--------|------------|
| `main.py` | ✅ Working | Rename refs → `ProductionManagerWindow` |
| `main_window.py` | ✅ Working | Major refactor: rename class, add toolbar actions, add 4th tab |
| `models.py` | ✅ Working | Keep as-is (StepNode, SequenceModel, StepType) |
| `server_bridge.py` | ✅ Working | Extend with `save_relation()`, `delete_relation()`, `create_definition()` etc. |
| `widgets/__init__.py` | ✅ Working | Keep |
| `widgets/definition_tree.py` | ✅ Working | Keep as-is (already status-colored tree) |
| `widgets/designer_tab.py` | ✅ Working | Keep as-is (already full designer tab) |
| `widgets/flow_canvas.py` | ✅ Working | Keep as-is |
| `widgets/outline_tree.py` | ✅ Working | Keep as-is |
| `widgets/overview_tab.py` | ✅ Working | Keep as-is (already matches WATS layout) |
| `widgets/property_editor.py` | ✅ Working | Keep as-is |
| `widgets/relations_tab.py` | ✅ Working | **Extend** with Add/Delete/Edit + relation-type dropdown |
| `widgets/toolbox.py` | ✅ Working | Keep as-is |

---

## Phase 1 — Rename & Restructure (Directory + Imports)

**Goal:** Move `sequence_designer/` → `production_manager/` and update all references.

### 1.1 Rename Directory
- Rename `src/pywats_ui/apps/sequence_designer/` → `src/pywats_ui/apps/production_manager/`
- This is a file-system rename; all files inside keep their names

### 1.2 Update `__init__.py`
- Change module docstring from "Sequence Designer" → "Production Manager"

### 1.3 Update `main.py`
- Change import: `from .main_window import ProductionManagerWindow`
- Change `app.setApplicationName("pyWATS Production Manager")`
- Change window instantiation to `ProductionManagerWindow()`

### 1.4 Update `main_window.py`
- Rename class: `SequenceDesignerWindow` → `ProductionManagerWindow`
- Update window title: `"pyWATS — Production Manager"`
- Update about dialog text

### 1.5 Update `launcher.py`
- Rename dict key: `"sequence_designer"` → `"production_manager"`
- Rename method: `launch_sequence_designer()` → `launch_production_manager()`
- Update import path: `from pywats_ui.apps.production_manager.main_window import ProductionManagerWindow`
- Update tray menu label: `"🏭 Production Manager"`

### 1.6 Update Internal Imports
All widget files import from `..server_bridge` / `..models` — these are relative imports
and will work unmodified after the directory rename. Only files that import using absolute
paths need updating (launcher, tests).

### 1.7 Update Tests
- Rename `tests/ui/sequence_designer/` → `tests/ui/production_manager/`
- Update import paths in test files

### 1.8 Verification
- `pytest tests/ui/production_manager/` passes
- App launches via `python -m pywats_ui.apps.production_manager.main`
- Launcher `launch_production_manager()` opens the window

---

## Phase 2 — Toolbar Matching WATS Production Manager

**Goal:** Replicate the WATS toolbar: `+ New… | Copy | Move to draft | Move to pending | Release | Tag manager… | Delete | Revoke | Move Entity`

### 2.1 Toolbar Actions (left-to-right from screenshot)

| Action | Icon/Label | Shortcut | Handler | Server Call |
|--------|-----------|----------|---------|-------------|
| **+ New…** | `"+ New…"` | `Ctrl+N` | `_on_new()` | `POST PostDefinition` |
| **Copy** | `"Copy"` | — | `_on_copy()` | `GET GetDefinitionCopy/{id}` |
| **Move to draft** | `"Move to draft"` | — | `_on_move_to_draft()` | `PUT PutDefinitionNew` (Status=0) |
| **Move to pending** | `"Move to pending"` | — | `_on_move_to_pending()` | `PUT PutDefinitionNew` (Status=1) |
| **Release** | `"Release"` | — | `_on_release()` | `PUT PutDefinitionNew` (Status=2) |
| _separator_ | | | | |
| **Delete** | `"Delete"` | `Del` | `_on_delete()` | `PUT PutDefinitionNew` (Status=3) — same as Revoke |
| **Revoke** | `"Revoke"` | — | `_on_revoke()` | `PUT PutDefinitionNew` (Status=3) |

> **Note:** "Tag manager" and "Move Entity" are **not implemented** — not needed for pyWATS.
> Delete and Revoke both set Status=3 (Revoked). Delete is shown for Draft/Pending items,
> Revoke is shown for Released items. Both use the same API call.

### 2.2 State-Dependent Button Enabling

| Action | Draft (0) | Pending (1) | Released (2) | Revoked (3) | No selection |
|--------|-----------|-------------|--------------|-------------|--------------|
| Copy | ✅ | ✅ | ✅ | ✅ | ❌ |
| Move to draft | ❌ | ✅ | ❌ | ❌ | ❌ |
| Move to pending | ✅ | ❌ | ❌ | ❌ | ❌ |
| Release | ❌ | ✅ | ❌ | ❌ | ❌ |
| Delete | ✅ | ✅ | ❌ | ❌ | ❌ |
| Revoke | ❌ | ❌ | ✅ | ❌ | ❌ |

### 2.3 Implementation in `main_window.py`
- Add action fields (`self._act_copy`, `self._act_move_draft`, etc.)
- Add `_update_toolbar_state()` method called on `_on_definition_selected()`
- Wire each action to the appropriate `ServerBridge` method

### 2.4 ServerBridge Extensions
Add methods to `server_bridge.py`:

```python
def copy_definition(self, definition_id: str) -> None: ...
def update_definition_status(self, definition_id: str, new_status: int) -> None: ...
```

> **Note:** No separate delete method needed — `update_definition_status(id, 3)` handles
> both Delete (for Draft/Pending) and Revoke (for Released).

Add corresponding signals:
```python
definition_copied = Signal(dict)
definition_updated = Signal(dict)
```

---

## Phase 3 — Relations Tab Enhancement

**Goal:** Add CRUD operations matching the WATS Relations tab with the relation-type dropdown.

### 3.1 Current State
- `RelationsTab` displays a read-only table (Active, Relation type, Value, Product name, Test operations)
- Data loaded from `ServerBridge.load_relations()`

### 3.2 New UI Elements

#### Toolbar (above table)
- **`+ Add`** button — opens inline edit row
- **`Delete`** button — removes selected relation (with confirmation)
- **`Edit`** button — makes selected row editable

#### Relation-Type Dropdown (in edit mode)
From screenshot, the dropdown options are:
- Part number
- Product revision
- Serial number
- Batch number

These map to the `TestSequenceRelation` model fields:
| UI Label | `EntitySchema` | `EntityKey` |
|----------|---------------|-------------|
| Part number | `"Product"` | `"PartNumber"` |
| Product revision | `"Product"` | `"Revision"` |
| Serial number | `"Unit"` | `"SerialNumber"` |
| Batch number | `"Unit"` | `"BatchNumber"` |

#### Edit Row Layout
When adding/editing a relation:
1. **Relation type** — Dropdown (Part number / Product revision / Serial number / Batch number)
2. **Value** — Text field (supports wildcards like `%`, `ABC123%`)
3. **OK** / **Cancel** buttons (green OK, gray Cancel — matching screenshot)

### 3.3 ServerBridge Extensions
```python
def create_relation(self, definition_id: str, entity_schema: str, entity_key: str, entity_value: str) -> None: ...
def update_relation(self, relation: dict) -> None: ...
def delete_relation(self, relation: dict) -> None: ...
```

Signals:
```python
relation_created = Signal(dict)
relation_updated = Signal(dict)
relation_deleted = Signal()
```

### 3.4 Implementation Steps
1. Add toolbar with Add/Delete/Edit buttons to `RelationsTab`
2. Add `_RELATION_TYPES` constant mapping UI labels → schema/key pairs
3. Implement `_start_add()` — insert editable row at bottom with dropdown + text field + OK/Cancel
4. Implement `_start_edit()` — make selected row editable
5. Implement `_on_delete()` — confirmation dialog → `ServerBridge.delete_relation()`
6. Implement `_on_save()` — validate → `ServerBridge.create_relation()` or `update_relation()`
7. Implement `_on_cancel()` — discard editable row
8. Wire signals to refresh table after mutations

---

## Phase 4 — Instructions (PDF) Tab

**Goal:** Add a fourth tab for managing attached PDF instruction documents.

### 4.1 New File
- `src/pywats_ui/apps/production_manager/widgets/instructions_tab.py`

### 4.2 UI Layout

```
┌──────────────────────────────────────────────────┐
│  📄 Instructions (PDF)                           │
│  ┌─────────────────────────────────────────────┐ │
│  │ Toolbar: [+ Add] [✕ Delete] [📥 Download]  │ │
│  ├─────────────────────────────────────────────┤ │
│  │  Filename        │ Size    │ Uploaded        │ │
│  │─────────────────────────────────────────────│ │
│  │  Assembly_Guide.pdf │ 2.4 MB │ 2024-02-21   │ │
│  │  QC_Checklist.pdf   │ 850 KB │ 2024-03-15   │ │
│  └─────────────────────────────────────────────┘ │
│  2 documents                                     │
└──────────────────────────────────────────────────┘
```

### 4.3 Features
- **Table columns:** Filename, Size, Uploaded date
- **Add:** File picker dialog (`.pdf` filter) → upload via `POST /api/internal/Blob/mi`
- **Delete:** Confirmation → remove via `DELETE /api/internal/Blob/mi`
- **Download / Open:** `GET /api/internal/Blob/mi` → save-as or open in system PDF viewer
- **Status label:** Document count

### 4.4 API Integration — Blob Endpoints

All MI media is managed via the `/api/internal/Blob/mi` endpoints:

| Action | Method | Endpoint | Notes |
|--------|--------|----------|-------|
| List / Download | `GET` | `/api/internal/Blob/mi` | Returns media list or file content |
| Upload | `POST` | `/api/internal/Blob/mi` | HttpContent poststream with file contents |
| Delete | `DELETE` | `/api/internal/Blob/mi` | Remove media attachment |

These need to be added to `Routes` in `src/pywats/core/routes.py` and wired
through `ServerBridge`.

### 4.5 Registration in `main_window.py`
```python
from .widgets.instructions_tab import InstructionsTab

self._instructions_tab = InstructionsTab(self._bridge)
self._tabs.addTab(self._instructions_tab, "Instructions (PDF)")
```

---

## Phase 5 — Header / Entity Count Bar

**Goal:** Match the WATS header showing the app name and entity count.

### 5.1 Header Bar
From the screenshot, the top-left shows:
```
🏭 Production manager    + New...
   50 entities
```

### 5.2 Implementation
- Add a header widget above the splitter in `main_window.py`
- Show app title + entity count (from `len(definitions)`)
- Update count when definitions are loaded

---

## Phase 6 — Polish & Verification

### 6.1 Definition Tree Enhancements
- Support folder names (currently shows "Folder" placeholder — need VirtualFolder name from API)
- Checkbox column for bulk operations (visible in screenshot)
- Drag handles (the `⠿` grip icons in the screenshot, for reordering)

### 6.2 Status Bar
- Show connection info, selected definition, and entity count

### 6.3 Testing
- Update existing tests in `tests/ui/production_manager/`
- Add tests for new Relations tab CRUD operations
- Add tests for InstructionsTab
- Add tests for toolbar state management
- Verify all imports resolve correctly

### 6.4 Documentation
- Update examples if any reference `sequence_designer`
- Update CHANGELOG under `[Unreleased]`

---

## Implementation Order

| Step | Phase | Effort | Dependencies |
|------|-------|--------|--------------|
| 1 | Phase 1 — Rename & Restructure | Small | None |
| 2 | Phase 2 — Toolbar | Medium | Phase 1 |
| 3 | Phase 3 — Relations CRUD | Medium | Phase 1, ServerBridge extensions |
| 4 | Phase 4 — Instructions tab | Medium | Phase 1 |
| 5 | Phase 5 — Header bar | Small | Phase 1 |
| 6 | Phase 6 — Polish | Small-Medium | All above |

Phases 2–5 are independent of each other and can be done in any order after Phase 1.

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Import breakage after rename | Medium | Low | Relative imports already used in widgets; only launcher/tests need path updates |
| Blob endpoint query params unknown | Medium | Medium | Inspect WATS API traffic to determine how definition_id is passed to Blob endpoints |
| Folder names not available from API | Medium | Low | Continue showing "Folder" or derive from definition grouping |
| Bulk operations (checkboxes) need batch API calls | Low | Low | Defer to Phase 6 polish |
