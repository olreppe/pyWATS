# Analysis — Production Manager

**Created:** April 8, 2026  
**Last Updated:** April 8, 2026

---

## Current State

### Existing `sequence_designer` App

The current app at `src/pywats_ui/apps/sequence_designer/` already implements ~70% of the
Production Manager layout:

- **Left panel:** `DefinitionTree` — status-colored tree grouped by VirtualFolderId ✅
- **Tab 1 (Sequence overview):** `OverviewTab` — name, description, status badge, timestamps, options ✅
- **Tab 2 (Sequence designer):** `DesignerTab` — flow canvas, outline, toolbox, property editor ✅
- **Tab 3 (Relations):** `RelationsTab` — read-only table ✅ (needs CRUD)
- **Tab 4 (Instructions PDF):** ❌ Missing entirely
- **Toolbar:** Connect, Refresh, + New ✅ (needs expansion to match WATS toolbar)

### WATS Production Manager Reference (from screenshots)

**Toolbar actions (left to right):**
`+ New…` · `Copy` · `Move to draft` · `Move to pending` · `Release` · `Tag manager…` · `Delete` · `Revoke` · `Move Entity`

**Header:**
`Production manager` with entity count (e.g., "50 entities")

**Definition tree (left):**
- Folder hierarchy with expand/collapse
- Checkboxes for bulk selection
- Drag handles (⠿ grip icons)
- Color by status: green (Released), gray (Draft), amber (Pending), red (Revoked)
- Version number column
- Search bar at top

**Relations tab (from screenshot):**
- Toolbar: `+ Add`, `✕ Delete`, `✏ Edit`
- Drag-to-group column headers
- Table columns: Active (checkbox), Relation type, Value, Product name, Test operations
- Relation type dropdown when editing: Part number, Product revision, Serial number, Batch number
- OK / Cancel buttons on edit row (green OK button)

---

## API Endpoints Required

### Already wired in ServerBridge
| Action | Endpoint | Status |
|--------|----------|--------|
| List definitions | `GET GetTestSequenceDefinitions` | ✅ |
| Get definition | `GET GetTestSequenceDefinition` | ✅ |
| Get XAML | `GET GetTestSequenceDefinitionXaml` | ✅ |
| List relations | `GET GetRelations/{id}` | ✅ |
| Save XAML | `PUT PutTestSequenceDefinitionXaml` | ✅ |

### Needed for Production Manager toolbar
| Action | Endpoint | Status |
|--------|----------|--------|
| Create definition | `POST PostDefinition` | Need to wire |
| Update definition (status changes) | `PUT PutDefinitionNew` | Need to wire |
| Copy definition | `GET GetDefinitionCopy/{id}` | Need to wire |
| Delete / Revoke definition | `PUT PutDefinitionNew` (set Status=3 Revoked) | Need to wire |

> **Confirmed:** There is no separate delete endpoint. Deletion is achieved by revoking
> (setting Status=3). The "Delete" toolbar button should revoke the definition.

### Needed for Relations CRUD
| Action | Endpoint | Status |
|--------|----------|--------|
| Create relation | `POST PostRelation` | Need to wire |
| Update relation | `PUT PutRelation` | Need to wire |
| Delete relation | `DELETE DeleteRelationNew` | Need to wire |
| Check conflicts | `GET GetRelationConflictsNew/{id}` | Need to wire |

### Needed for Instructions (PDF) — Blob Endpoints
| Action | Endpoint | Status |
|--------|----------|--------|
| Get MI media | `GET /api/internal/Blob/mi` | Need to wire |
| Upload MI media | `POST /api/internal/Blob/mi` (HttpContent poststream) | Need to wire |
| Delete MI media | `DELETE /api/internal/Blob/mi` | Need to wire |

---

## Constraints

1. **Relative imports:** Widget files use `..server_bridge` and `..models` — these survive
   a directory rename automatically.
2. **Launcher uses absolute imports:** Must update `pywats_ui.apps.sequence_designer` →
   `pywats_ui.apps.production_manager` in `launcher.py`.
3. **Test imports:** `tests/ui/sequence_designer/` imports use package paths that need updating.
4. **No breaking changes to domain layer:** The `manual_inspection` domain in `src/pywats/`
   is unaffected — only the UI app is changing.

---

## Open Questions — Resolved

1. ✅ **PDF attachment API:** Uses Blob endpoints under `/api/internal/Blob/mi` — GET (list/download),
   POST (upload via HttpContent poststream), DELETE (remove).
2. ✅ **Tag manager:** Disregarded — not needed for Production Manager.
3. ✅ **Move Entity:** Disregarded — not needed for Production Manager.
4. ✅ **Definition deletion:** No separate delete endpoint. Deletion = Revoking (Status=3 via
   `PUT PutDefinitionNew`). The Delete and Revoke toolbar buttons perform the same operation.
5. ⏳ **Folder names:** Still unknown. Will be answered later. Tree continues showing
   "Folder" placeholder until resolved.
