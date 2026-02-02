---
name: new-project
description: Create a new project with full structure (README, ANALYSIS, PLAN, PROGRESS, TODO)
argument-hint: "Project name and brief description, e.g., 'cache-optimization to improve API performance'"
---

You are my project setup assistant for the pyWATS repository.

## Goal
Create a complete new project structure in `projects/active/{name}.project/` with all required documents.

## Input from User
{{args}}

## Steps

### 1. Parse Input
Extract:
- Project name (kebab-case for folder)
- Brief description/objective
- If missing, ask before proceeding

### 2. Create Project Structure
Create folder: `projects/active/{name}.project/`

Create these 4 required files from templates in `projects/.agent_instructions.md`:

**README.md:**
- Status: 🚧 In Progress
- Priority: (ask user: P1-P4 or leave as TBD)
- Timeline: (estimate or TBD)
- Objective: {from user input}
- Success Criteria: (draft 3-5 items, mark with ⏳)
- Quick Links: to other docs

**01_ANALYSIS.md:**
- Problem Statement: {from description}
- Requirements: {Functional, Non-Functional - draft or TBD}
- Constraints: {Technical, Time, Breaking Changes}
- Architecture Impact: {How this affects existing code}
- Risk Assessment: {HIGH/MEDIUM/LOW categories}

**02_IMPLEMENTATION_PLAN.md:**
- Phase breakdown (at least Phase 1 outlined)
- Step-by-step actions with file paths
- Testing Strategy
- Rollback Plan

**03_PROGRESS.md:**
- Current Session heading with today's date
- Empty Completed, In Progress, Discoveries sections
- Metrics section (Files Modified: 0, Tests: 0/0)

**04_TODO.md:**
- At least 3-5 initial tasks under 🧠 Planned
- Empty Completed, In Progress, Blocked sections

Optional subdirectories:
- `tests/` - For project-specific tests (to be moved to main suite on completion)
- `scripts/` - For automation scripts
- `notes/` - For working notes

### 3. Update Active Projects List
Add entry to `projects/active/README.md` under "Current Active Items"

### 4. Present Summary
Show:
- ✅ Project folder created
- ✅ 4 documents generated
- 📋 Next steps: Review ANALYSIS, refine PLAN, start implementation
- 🔗 Link to: `projects/active/{name}.project/README.md`

### 5. Ask Clarifications
If any critical information is missing:
- Priority level?
- Timeline estimate?
- Key requirements?
- Known constraints?

## Output Format
1. Create all files
2. Show brief summary (not full file contents)
3. Ask for any missing critical details
4. Remind: "Update TODO.md BEFORE starting each task (mark 🚧), and IMMEDIATELY after completion (mark ✅)"

## Reference
- Templates: `projects/.agent_instructions.md`
- Workflow rules: `.github/copilot-instructions.md`
