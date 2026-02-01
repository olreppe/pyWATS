# Internal Documentation Workflow Guide

**Purpose**: This folder contains all working documents, implementation plans, analysis reports, and agent-generated documentation. This README defines the workflow for organizing and managing internal documentation.

**Last Reorganized:** February 1, 2026

---

## 📁 Folder Structure

```
docs/internal_documentation/
├── README.md                    # This file - workflow guide
├── TYPE_STUBS.md               # Active reference documents
├── BETA_TESTING_PROGRAM.md     # Active programs
├── .agent_instructions.md      # Agent context
│
├── 📋 active/                  # Current work (1-5 items max)
├── 📅 planned/                 # Next 1-3 months (10-20 items)
├── ✅ completed/               # Historical record (organized by quarter)
│   └── 2026-q1/               # Jan-Mar 2026
│       ├── jan_architecture_review/
│       ├── jan_report_system/
│       └── feb_developer_experience/
├── 💡 ideas/                   # Future exploration (unlimited)
├── 📚 reference/               # Code samples, specs, analysis
│   └── csharp_code/           # C# reference implementations
├── 🛠️ scripts/                 # Utility scripts
└── 🗄️ archive_old/            # Pre-2026 historical docs
```

---

## 🎯 Simple 3-State Workflow

### 📋 **Active** (`active/`)
**What you're working on RIGHT NOW**

**Rule:** Maximum 5 items. If you can't finish it this week, move to planned.

**Criteria**:
- Actively editing TODAY
- Implementation in progress RIGHT NOW  
- Clear deliverable within 1 week
- Has your full attention

**When to add**: When you start working on it  
**When to remove**: 
- Completed → Move to `completed/YYYY-qN/theme/`
- Not working on it → Back to `planned/`
- Blocked → Move to `planned/` with blocker noted

---

### 📅 **Planned** (`planned/`)
**What's coming up in the NEXT 1-3 months**

**Rule:** Concrete enough to estimate, prioritized by value.

**Criteria**:
- Clear scope and acceptance criteria
- Estimated effort known
- Prioritized but not yet started
- Waiting for capacity or dependencies

**When to add**: When idea becomes concrete plan  
**When to remove**:
- Ready to start → Promote to `active/`
- Deprioritized → Downgrade to `ideas/`
- Dependencies unclear → Back to `ideas/` for research

---

### ✅ **Completed** (`completed/YYYY-qN/`)
**Historical record of finished work**

**Rule:** Organize by quarter and theme for easy reference.

**Structure**:
```
completed/
└── 2026-q1/
    ├── README.md  (summary of Q1 achievements)
    ├── jan_architecture_review/
    ├── jan_report_system/
    └── feb_developer_experience/
```

**Criteria**:
- Status markers: ✅ IMPLEMENTED, ✅ COMPLETED, ✅ DONE
- Implementation is in production code
- No outstanding action items
- Valuable for understanding past decisions

**When to add**: Immediately when work is finished  
**When to archive**: Annually - very old quarters to `archive_old/`

---

### 💡 **Ideas** (`ideas/`)
**Future exploration - not yet scheduled**

**Rule:** Any idea worth remembering. Review monthly to promote or archive.

**Structure**:
```
ideas/
├── README.md  (index with priority ratings)
├── integrations/  (CFX, MQTT, electronics test)
├── analytics/     (SPC, AI-assisted, caching)
├── deployment/    (packaging, easy install)
└── architecture/  (MCP, performance, models)
```

**Criteria**:
- Interesting concepts worth preserving
- Not concrete enough to estimate yet
- Requires research or validation
- Long-term improvements (3+ months)

**When to add**: Anytime you have an idea  
**When to remove**: Promote to `planned/` OR archive if obsolete

---

### 📚 **Reference** (`reference/`)
**Permanent knowledge base - code samples, specs, analysis**

**Rule:** Never delete - this is your institutional knowledge.

**Structure**:
```
reference/
├── csharp_code/      # C# implementations for comparison
├── api_specs/        # API specifications
├── example_reports/  # Sample report files
└── domain_analysis/  # Domain health assessments
```

**Contains**:
- Code samples for comparison (C# vs Python)
- API specifications and contracts
- Domain health assessments
- Architecture diagrams

**When to add**: Any reference material that helps understand the system

---

## 🔄 Workflow Examples

### Starting New Work
1. Have idea → Add to `ideas/category/IDEA_NAME.md`
2. Idea becomes concrete → Move to `planned/`
3. Ready to start → Move to `active/` (max 5!)
4. Work complete → Move to `completed/YYYY-qN/theme/`

### Weekly Review
1. Look at `active/` - Still working on these? If not, back to `planned/`
2. Look at `planned/` - Ready to promote to `active/`?
3. Check `ideas/` - Any new priorities for `planned/`?

### Quarterly Cleanup
1. Create new `completed/YYYY-qN/` folder with theme subfolders
2. Group this quarter's work by theme
3. Update `completed/YYYY-qN/README.md` with summary
4. Review `ideas/` - Archive obsolete items

---

## 🤖 Agent Instructions

### Creating New Plans

**Place new implementation plans in** `active/` **when actively working on them.**

**Structure:**
```markdown
# {Feature} Implementation Plan

**Status**: 🚧 IN PROGRESS
**Started**: YYYY-MM-DD
**Priority**: HIGH/MEDIUM/LOW
**Estimated Effort**: X hours/days

## Overview
What and why

## Implementation Steps
1. Step one
2. Step two

## Acceptance Criteria
- [ ] Criteria one
- [ ] Criteria two

## Progress
- [x] Completed step
- [ ] Next step
```

### Completing Work

**When work is finished:**
1. Update status to ✅ COMPLETED
2. Add completion date
3. Move to `completed/YYYY-qN/appropriate_theme/`
4. Update quarterly README

### Moving Between States

**Promote idea → planned:**
- Add concrete scope, acceptance criteria, effort estimate
- Move from `ideas/category/` to `planned/`

**Promote planned → active:**
- Ready to start work THIS WEEK
- Move from `planned/` to `active/`
- Ensure active has < 5 items

**Downgrade active → planned:**
- Not working on it anymore
- Blocked or waiting
- Move back to `planned/` with notes

---

## 📊 Current Status (February 1, 2026)

**Active:** 1 item (Sphinx Documentation)  
**Planned:** 4 items (Architecture debt, type safety analysis, Stage 4 improvements)  
**Ideas:** 15 items (CFX, MQTT, AI/SPC, MCP, etc.)  
**Completed Q1 2026:** ~67 documents across 3 major themes  
**Reference:** C# code samples, API specs  
**Archive:** Pre-2026 historical documentation (88 files)

---

## 🎯 Keep It Simple

**Golden Rules:**
1. **Active** = What I'm doing THIS WEEK (max 5)
2. **Planned** = What's NEXT (1-3 months)
3. **Completed** = What's DONE (organized by quarter + theme)
4. **Ideas** = What's SOMEDAY (review monthly)
5. **Reference** = What HELPS ME (never delete)

**Don't overthink it!** The system works when you use it naturally, not when it's too complicated to maintain.

---

Last Updated: February 1, 2026
   
   ## Current State
   What exists today
   
   ## Goals
   What we're trying to achieve
   
   ## Implementation Phases
   - [ ] Phase 1: ...
   - [ ] Phase 2: ...
   
   ## Testing Strategy
   How we'll verify success
   ```

### During Work

**As work progresses:**

1. **Update status regularly**:
   - Check off completed items: `- [x]`
   - Update status sections
   - Add "Implementation Notes" for decisions made

2. **Link to commits**:
   - Reference relevant commit SHAs
   - Link to PRs or branches
   - Document why decisions were made

3. **Keep related docs together**:
   - If analysis leads to implementation, keep both in `to_do/`
   - Reference related documents

### Completing Work

**When all work items are done:**

1. **Update final status**:
   ```markdown
   **Status**: ✅ COMPLETED
   **Completed**: YYYY-MM-DD
   **Implemented In**: vX.Y.Z
   ```

2. **Move to completed**:
   ```bash
   Move-Item "WIP/to_do/FEATURE_PLAN.md" "WIP/completed/"
   ```

3. **Update CHANGELOG.md**:
   - Add user-facing changes
   - Link to completed plan if needed

4. **Verify no orphaned references**:
   - Check if other docs reference this work
   - Update status in related documents

### Recording Ideas

**When exploring concepts or brainstorming:**

1. **Create idea document**:
   - Place in `WIP/ideas/`
   - Mark as: `**Status**: 💡 IDEA / PROPOSAL`
   - Include "Why This Matters" section

2. **Promotion to active work**:
   - When prioritized, move from `ideas/` → `to_do/`
   - Update status to 📋 PLANNED or 🚧 IN PROGRESS
   - Add concrete implementation phases

3. **Archiving old ideas**:
   - If idea becomes obsolete, add note at top
   - Move to archive or delete if no longer relevant

---

## 🎯 Best Practices

### For Agents

1. **Always check context first**: Before creating new docs, search existing ones
2. **Use consistent naming**: `{TOPIC}_{TYPE}.md` (e.g., `ASYNC_IMPLEMENTATION_PLAN.md`)
3. **Add metadata headers**: Status, date, priority, effort estimate
4. **Link related work**: Reference other docs, commits, issues
5. **Update status markers**: Keep status current as work progresses
6. **Move when done**: Immediately move completed work to `completed/`
7. **Clean as you go**: Remove obsolete docs, update references

### Document Status Markers

Use these consistently in document headers:

- ✅ `COMPLETED` - All work finished
- 🚧 `IN PROGRESS` - Currently being worked on
- 📋 `PLANNED` - Ready to start, not yet begun
- 💡 `IDEA` - Exploratory, not yet committed
- 📚 `REFERENCE` - Living document, no completion state
- 🔴 `BLOCKED` - Waiting on dependencies
- ⏸️ `PAUSED` - Deprioritized temporarily

### Naming Conventions

- **Plans**: `{TOPIC}_IMPLEMENTATION_PLAN.md`
- **Analysis**: `{TOPIC}_ANALYSIS.md` or `{TOPIC}_AUDIT.md`
- **Status**: `{TOPIC}_STATUS.md` or `{TOPIC}_SUMMARY.md`
- **Architecture**: `{COMPONENT}_ARCHITECTURE.md`
- **Guides**: `{TOPIC}_GUIDE.md`

---

## 📊 Maintenance

### Monthly Review

**Agents should help with periodic cleanup:**

1. **Audit `to_do/`**: 
   - Are plans still relevant?
   - Should any be completed?
   - Should any move to ideas?

2. **Audit `ideas/`**:
   - Are any ready to promote to `to_do/`?
   - Are any obsolete?

3. **Audit `completed/`**:
   - Should very old items be archived?
   - Are they still useful references?

### File Hygiene

- **Delete duplicates**: Merge similar documents
- **Update cross-references**: Fix broken links
- **Consistent formatting**: Follow markdown standards
- **Clear headers**: Every doc needs status and context

---

## 🔍 Quick Reference

| Task | Action | Folder |
|------|--------|--------|
| Starting new feature work | Create implementation plan | `WIP/to_do/` |
| Exploring an idea | Create proposal/analysis | `WIP/ideas/` |
| Finished implementation | Move plan to completed | `WIP/completed/` |
| Recording architecture | Create reference doc | Root level |
| Active bug investigation | Create analysis in | `WIP/to_do/` |
| Future enhancement idea | Create proposal in | `WIP/ideas/` |

---

## 📖 Example Workflow

**Scenario**: User asks to implement async support

1. **Agent searches**: `grep -r "async" WIP/`
2. **Finds**: `WIP/to_do/ASYNC_IMPLEMENTATION_PLAN.md` with 📋 PLANNED status
3. **Begins work**: Updates status to 🚧 IN PROGRESS
4. **Implements**: Checks off phases as completed
5. **Tests**: Validates all items in testing strategy
6. **Completes**: Updates status to ✅ COMPLETED, adds completion date
7. **Moves**: `Move-Item` to `WIP/completed/`
8. **Updates**: CHANGELOG.md with user-facing changes
9. **Commits**: References completed plan in commit message

---

## 📝 Template

Use this template for new implementation plans:

```markdown
# {Feature Name} Implementation Plan

**Status**: 🚧 IN PROGRESS  
**Priority**: HIGH | MEDIUM | LOW  
**Estimated Effort**: X hours/days  
**Created**: YYYY-MM-DD  
**Target Version**: vX.Y.Z

---

## Overview

Brief description of what we're building and why it matters.

## Current State

What exists today and why it needs to change.

## Goals

### Must Have
- [ ] Goal 1
- [ ] Goal 2

### Should Have
- [ ] Nice to have 1

### Won't Have
- Explicitly out of scope

## Implementation Phases

### Phase 1: {Name}
**Objective**: What this phase achieves

**Tasks**:
- [ ] Task 1
- [ ] Task 2

**Validation**: How we know it's done

### Phase 2: {Name}
...

## Testing Strategy

How we'll verify everything works.

## Documentation Updates

What docs need to be updated.

## Timeline

Estimated schedule for each phase.

---

**Implementation Notes**:
- YYYY-MM-DD: Decision made about X because Y
```

---

**Last Updated**: 2026-01-26  
**Maintained By**: AI Agents following this workflow