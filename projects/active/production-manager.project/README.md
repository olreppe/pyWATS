# Production Manager

**Created:** April 8, 2026  
**Last Updated:** April 8, 2026  
**Status:** 🚧 In Progress (0%)

---

## Problem Statement

The current `sequence_designer` app in `src/pywats_ui/apps/sequence_designer/` was built as
a narrow tool focused on the sequence flow editor. It already contains elements of a broader
Production Manager (definition tree, overview tab, relations tab), but it is named and
structured as if it were only the designer canvas.

The WATS web application exposes the same features under a unified **"Production Manager"**
view with 50+ entities, a left-side definition tree, and four tabs:

1. **Sequence overview** — metadata, status badge, timestamps, options/toggles
2. **Sequence designer** — visual step-flow editor (the current app's core)
3. **Relations** — link definitions to part numbers, revisions, serial numbers, batches
4. **Instructions (PDF)** — list of attached PDF documents

This project renames and restructures the app to `production_manager`, making the sequence
designer one tab among several, and adds the missing Instructions (PDF) tab with full
Add/Delete/Edit/View operations for managing relation types and PDF attachments.

---

## Objectives

1. Rename `src/pywats_ui/apps/sequence_designer/` → `src/pywats_ui/apps/production_manager/`
2. Rename the window class from `SequenceDesignerWindow` → `ProductionManagerWindow`
3. Restructure `main_window.py` with the WATS-matching toolbar and four tabs
4. Add a full-featured **Relations tab** with Add/Delete/Edit supporting relation-type
   dropdown (Part number, Product revision, Serial number, Batch number)
5. Add an **Instructions (PDF) tab** for managing attached PDF documents
6. Update launcher, entry point, tests, and all imports
7. Keep all existing sequence designer widget code intact (just re-homed)

---

## Success Criteria

- App launches as "pyWATS Production Manager" from launcher and standalone
- Left panel shows definition tree with status-colored items (Draft/Pending/Released/Revoked)
- Toolbar includes: Copy, Move to draft, Move to pending, Release, Tag manager, Delete, Revoke, Move Entity
- All four tabs functional: Sequence overview, Sequence designer, Relations, Instructions (PDF)
- Relations tab supports Add/Delete/Edit with relation-type dropdown
- Instructions tab shows a list of attached PDFs with Add/Remove actions
- Existing sequence designer functionality preserved
- All imports updated, no broken references
- Tests updated and passing

---

## Scope

**In scope:**
- Directory rename and restructure
- Toolbar matching WATS Production Manager (screenshot)
- Four-tab layout
- Relations tab with CRUD + relation-type dropdown
- Instructions (PDF) tab with list view
- Launcher + entry point updates

**Out of scope (future):**
- Operator Interface app (Phase 2B of MI project)
- Extended step types (Phase 3)
- XAML parsing into StepNode tree
- PDF viewer/preview widget
