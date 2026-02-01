# Active Projects

This folder contains active, in-progress projects for pyWATS development.

---

## 🤖 For AI Agents

**CRITICAL:** Before starting any project, read [.agent_instructions.md](.agent_instructions.md)

All agents MUST follow the structured workflow defined there:
1. Create project folder with 4 required markdown files
2. Follow analysis → planning → implementation → completion phases
3. Update TODO.md and PROGRESS.md continuously
4. Move completed projects to `docs/internal_documentation/completed/{quarter}/`

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

1. **Active** - Projects in progress live in `projects/`
2. **Complete** - Moved to `docs/internal_documentation/completed/{quarter}/`
3. **Archived** - Cancelled projects go to `docs/internal_documentation/archive/`

---

## 📋 Current Projects

(No active projects at this time)

---

## 🔗 Resources

- **Agent Workflow:** [.agent_instructions.md](.agent_instructions.md)
- **Micro-Sprint Guide:** [planned/ai-assisted-micro-sprint-workflow.md](planned/ai-assisted-micro-sprint-workflow.md)
- **GitHub Issues Workflow:** [planned/GitHubCopilot-BestPractices.md](planned/GitHubCopilot-BestPractices.md)
- **Completed Projects:** `docs/internal_documentation/completed/`

---

**Last Updated:** February 1, 2026
