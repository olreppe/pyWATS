# Analysis — Manual Inspection Domain

**Created:** March 20, 2026  
**Last Updated:** March 21, 2026

---

## Phase 1 — API Surface (pyWATS Domain)

All endpoints live under `/api/internal/ManualInspection/`. Key groupings:

- **Definitions** — CRUD for inspection definitions (`PostDefinition`, `PutDefinitionNew`, `GetTestSequenceDefinition(s)`, `GetDefinitionCopy`)
- **Relations** — Link definitions to products/processes (`PostRelation`, `PutRelation`, `DeleteRelationNew`, `GetRelations`, `GetRelationConflicts(New)`)
- **Sequences** — Manage inspection step sequences (`GetSequences`, `PutSequence`, `DeleteSequence`)
- **Unit Details** — Per-unit inspection results (`GetMiDetails`, `GetMiDetailsNew`, `GetInstancesCount`)
- **Workflow/XAML** — Workflow definitions (`GetTestSequenceDefinitionXaml`, `PutTestSequenceDefinitionXaml`, `GetWatswwfContent`)
- **Validation** — `ValidateMiscInfo`, `PutStringTest`

### Phase 1 Risks & Constraints

- Endpoint response schemas are not yet confirmed — will need to test against a live server or inspect C# reference code
- `GetWatswwfContent` returns a binary workflow file; needs special stream/bytes handling (deferred)
- Two parallel "new" endpoint variants exist (`GetMiDetailsNew`, `GetRelationConflictsNew`) — likely newer API versions; prefer `*New` unless incompatible
- Internal endpoints may require elevated permissions vs. public API

### Phase 1 Open Questions

1. Should `GetMiDetails` vs `GetMiDetailsNew` both be exposed, or only the newer variant?
2. Are the XAML/WWF endpoints needed for the initial release?
3. What C# models define the request/response shapes for `PostDefinition` and `PutDefinitionNew`?

---

## Phase 2 — pyWATS-OI (Qt6 Operator Interface)

### Requirements

- Desktop application built with **Qt6 / PySide6**
- Connects to WATS via the pyWATS ManualInspection domain (Phase 1)
- Operator workflow: scan unit → load matching sequence → step through inspection → submit results
- Mimics the WATS web app MI flow as a functional baseline
- More customizable than the web app (layout, branding, step display)
- Used as the integration test harness for the ManualInspection domain

### Architecture Sketch

```
pyWATS-OI/
├── main.py                  # Entry point
├── app/
│   ├── ui/                  # Qt6 widgets / screens
│   ├── engine/              # Sequence execution engine
│   ├── config/              # OI configuration (station, server, layout)
│   └── session/             # Active inspection session state
└── requirements.txt
```

### Phase 2 Risks & Constraints

- Qt6 / PySide6 licensing must be evaluated for distribution
- OI is a new standalone application — needs its own project structure and packaging
- Result submission must exactly match what the WATS web app produces (field parity)

### Phase 2 Open Questions

1. Will pyWATS-OI be distributed as part of pyWATS or as a separate package?
2. What is the minimum Qt6/PySide6 version requirement?
3. What authentication flow does OI use — same token as pyWATS, or separate config?
4. Does OI need offline/disconnected mode?

---

## Phase 3 — Extended Step Types

### Requirements

All extended step types are executed **locally by the OI engine** and write results back to
WATS via pyWATS. They are not WATS server features — WATS sees the output as normal UUTReport data.

| Step Type | Description | Key Design Questions |
|-----------|-------------|----------------------|
| **Conditional flow** | if/else, for/next, branching between steps/subsequences | How are conditions expressed? pyScript or Python? |
| **Dynamic subsequence call** | Call a subsequence by a computed name (from part number, tag, scanned input, etc.) | How is the name computed? Full Python expression? |
| **Multi-numeric limit step** | Single step with multiple measurement limits | How are pass/fail criteria aggregated? |
| **Advanced box build** | Integration with `product.BoxBuild` templates for assembly tracking | Needs Product domain BoxBuild API |
| **Relative limits** | Limits derived from earlier step results (e.g., ±5% of step A value) | Expression language needed — candidate for **pyScript** |
| **Batch inspection** | Work on multiple units simultaneously; apply a step to all or a selection | Session model must handle multiple active UUTs |
| **Python step** | Fully configurable step running a Python script; reads/writes UUTReport and OI GUI | Security model: sandboxed? trusted scripts only? |

### pyScript — Candidate Scripting/Markup Language

A lightweight language for:
- Configuring OI GUI layout (panels, colors, custom field display)
- Writing step condition expressions (relative limits, dynamic names, conditional flow)
- Designed to be readable by non-developers

**Decision needed:** Full custom DSL vs. a restricted Python subset (e.g., `ast.literal_eval` + safe evaluator).

### Phase 3 Risks & Constraints

- Python step security: arbitrary code execution in operator context — sandboxing strategy TBD
- Conditional flow and dynamic calls require a runtime sequence execution engine (not just a linear walker)
- Batch inspection requires significant session state refactoring vs. single-unit mode
- pyScript parsing/evaluation adds implementation complexity — consider deferring to a separate sub-project

### Phase 3 Open Questions

1. Is pyScript a new DSL or a restricted Python subset?
2. What is the security model for Python steps (sandboxed subprocess, restricted globals, etc.)?
3. Should batch inspection be a mode in OI or a separate application?
4. How do relative limits interact with the WATS step limit model when writing back to WATS?
