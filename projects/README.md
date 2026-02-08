# Active Projects

This folder contains active, in-progress projects for pyWATS development.

---

## 🤖 For AI Agents

**CRITICAL:** Before starting any project, read [.agent_instructions.md](.agent_instructions.md)

All agents MUST follow the structured workflow defined there:
1. Create project folder with 4 required markdown files
2. Follow analysis → planning → implementation → completion phases
3. Update TODO.md and PROGRESS.md continuously
4. Move completed projects to `projects/completed/{quarter}/`

---

## 📁 Project Structure (Required)

Each project MUST have this structure:

```
projects/{project-name}/
├── README.md                    # Project overview, status, links
├── 01_ANALYSIS.md              # Requirements, constraints, research
├── 02_IMPLEMENTATION_PLAN.md   # Step-by-step plan
├── 03_PROGRESS.md              # Real-time tracking
├── 04_TODO.md                  # Task checklist
├── tests/                      # Project-specific tests
├── scripts/                    # Automation scripts
└── notes/                      # Working notes
```

See [.agent_instructions.md](.agent_instructions.md) for templates and detailed workflow.

---

## 🎯 Lifecycle

1. **Active** - Projects in progress live in `projects/active/`
2. **Complete** - Moved to `projects/completed/{quarter}/` with timestamp
3. **Archived** - Cancelled projects go to `projects/archive/`

---

## 📋 Current Projects

### 1. GUI Client Separation (15% complete - PAUSED)
- **Location:** `active/gui-client-separation.project/`
- **Status:** Phase 1 complete, awaiting next sprint
- **Priority:** P2

---

## 📚 Recently Completed (2026-Q1)

### Logging Infrastructure Consolidation ✅
- **Completed:** February 3, 2026
- **Status:** 100% complete, 1756 tests passing
- **Location:** `projects/completed/2026-q1/02031400-logging-consolidation/`
- **Highlights:**
  - Unified logging framework (`configure_logging`)
  - 50+ dedicated tests (97%+ pass rate)
  - Zero breaking changes
  - Production-ready structured logging (JSON, rotation, correlation IDs)

### Sphinx Logging Documentation ✅
- **Completed:** February 3, 2026
- **Status:** 100% complete, clean Sphinx build
- **Location:** `projects/completed/2026-q1/` (see timestamped folders)
- **Highlights:**
  - Complete API reference for logging infrastructure
  - 800+ lines of documentation (logging.rst, client/logging.rst)
  - 35+ type-safe code examples
  - Fixed Sphinx import errors (models, analytics)

---

## 🔗 Resources

- **Agent Workflow:** [.agent_instructions.md](.agent_instructions.md)
- **Micro-Sprint Guide:** [planned/ai-assisted-micro-sprint-workflow.md](planned/ai-assisted-micro-sprint-workflow.md)
- **GitHub Issues Workflow:** [planned/GitHubCopilot-BestPractices.md](planned/GitHubCopilot-BestPractices.md)
- **Completed Projects:** [completed/](completed/)

---

**Last Updated:** February 1, 2026
