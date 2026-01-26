# Internal Documentation Workflow Guide

**Purpose**: This folder contains all working documents, implementation plans, analysis reports, and agent-generated documentation. This README defines the workflow for organizing and managing internal documentation.

---

## 📁 Folder Structure

```
docs/internal_documentation/
├── README.md                    # This file - workflow guide
├── TYPE_SAFETY_AUDIT.md         # Active reference documents
├── WIP/                         # Work In Progress tracking
│   ├── completed/              # ✅ Finished work
│   ├── to_do/                  # 🚧 Active/planned work
│   └── ideas/                  # 💡 Future ideas & proposals
```

---

## 📋 Document Categories

### ✅ **Completed** (`WIP/completed/`)
Implementation plans, analysis reports, and summaries that have been **fully executed** and are kept for historical reference.

**Criteria**:
- Status markers: ✅ IMPLEMENTED, ✅ COMPLETED, ✅ DONE
- Implementation is in production code
- No outstanding action items
- Valuable for understanding past decisions

**Examples**:
- `TYPE_SAFETY_IMPLEMENTATION_PLAN.md` - Fully implemented type safety improvements
- `BATCH_IMPLEMENTATION_PLAN.md` - Batch operations now in core
- `PERFORMANCE_OPTIMIZATIONS.md` - Completed optimization work

**When to move here**: Immediately after completing all work items in a plan

---

### 🚧 **To Do** (`WIP/to_do/`)
Active work in progress or planned implementations that are **ready to execute** or **currently being worked on**.

**Criteria**:
- Status markers: 📋 PLANNED, 🚧 IN PROGRESS, TODO
- Has clear action items or implementation steps
- Intended to be worked on in near future (next 1-3 months)
- Blocking or high-priority work

**Examples**:
- `ASYNC_IMPLEMENTATION_PLAN.md` - Planned async API support
- `EXCEPTION_HANDLING_PLAN.md` - ErrorHandler standardization work
- `RETRY_IMPLEMENTATION_PLAN.md` - Retry logic implementation

**When to move here**: When creating new implementation plans or starting analysis for upcoming work

---

### 💡 **Ideas** (`WIP/ideas/`)
Proposals, explorations, and recommendations that are **good ideas** but **not yet scheduled** for implementation.

**Criteria**:
- Interesting concepts worth preserving
- Requires further validation or prioritization
- May depend on other work being completed first
- Long-term improvements (3+ months out)
- "Nice to have" vs "must have"

**Examples**:
- `TARGET_PLATFORM_IMPLEMENTATION_PLAN.md` - Future deployment improvements
- `MCP_RECOMMENDATIONS.md` - Model Context Protocol integration ideas
- `MCP_ANALYSIS.md` - Analysis of MCP capabilities

**When to move here**: When documenting explorations, brainstorming, or future roadmap items

---

### 📚 **Reference** (Root level)
Architecture documentation, domain knowledge, and reference materials that don't have a clear "completion" state. These are **living documents** that get updated over time.

**Criteria**:
- Architecture diagrams and specifications
- Domain knowledge and terminology guides
- API design conventions and standards
- Release procedures and checklists

**Examples**:
- `TYPE_SAFETY_AUDIT.md` - Comprehensive codebase audit reference

**Location**: Keep at root of `internal_documentation/` for easy access

---

## 🤖 Agent Workflow

### Starting New Work

**When a user requests new development work:**

1. **Check existing docs first**:
   ```
   - Search WIP/to_do/ for related plans
   - Search WIP/completed/ for prior art
   - Search WIP/ideas/ for relevant proposals
   ```

2. **Create planning document**:
   - Place in `WIP/to_do/`
   - Use clear naming: `{TOPIC}_IMPLEMENTATION_PLAN.md`
   - Include status header: `**Status**: 🚧 IN PROGRESS`
   - Add date and objective

3. **Structure the plan**:
   ```markdown
   # {Feature} Implementation Plan
   
   **Status**: 🚧 IN PROGRESS
   **Priority**: HIGH/MEDIUM/LOW
   **Estimated Effort**: X hours/days
   **Target Version**: X.Y.Z
   
   ## Overview
   Brief description of what and why
   
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