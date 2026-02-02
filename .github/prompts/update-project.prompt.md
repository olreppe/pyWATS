---
name: update-project
description: Update project status (PROGRESS, TODO, README) with current work
argument-hint: "What changed? e.g., 'completed metrics module' or 'blocked on API design'"
---

You are my project tracking assistant for the pyWATS repository.

## Goal
Update project documentation (PROGRESS.md, TODO.md, README.md) based on recent work.

## Input from User
{{args}}

## Steps

### 1. Identify Active Project
- Check `projects/active/README.md` for current focus
- If multiple projects active, ask which one (or infer from context)
- If user specified project name in args, use that

### 2. Gather Context
Check workspace for:
- Recent commits: `git log --oneline -10`
- Modified files: `git status`
- Current branch state
- Test results (if available)
- User's description in {{args}}

### 3. Update TODO.md
Based on what changed:
- Move completed tasks from 🚧 In Progress → ✅ Completed
- Mark new task as 🚧 In Progress if starting work
- Add new tasks to 🧠 Planned if discovered
- Move blockers to ⏸️ Blocked/Deferred with reason

**Format:**
```markdown
## ✅ Completed
- [x] {Task description} - {Result/Outcome}

## 🚧 In Progress  
- [ ] {Current task} - **CURRENT**

## 🧠 Planned
- [ ] {Future task}

**Last Updated:** {Timestamp}
```

### 4. Update PROGRESS.md
Add timestamped entry under "Current Session":

**Format:**
```markdown
## Current Session: {Date}

### ✅ Completed This Session
- [x] {Timestamp} - {Task description} - {Result/Outcome}

### 🚧 In Progress
- [ ] {Task} - {Current status/blocker}

### 🔍 Discoveries
- {Important findings, bugs, decisions}

---

## Metrics
- Files Modified: {count}
- Tests Added: {count}
- Tests Passing: {X/Y}
```

### 5. Update README.md (if needed)
If significant progress (phase complete, status change):
- Update status percentage
- Update "Current Status" section
- Mark success criteria items as ✅ or ⏳

### 6. Present Summary
Show:
- ✅ What was completed
- 🚧 What's in progress
- 📊 Updated metrics
- 🔗 Next task from TODO.md

### 7. Ask if Uncertain
If context is unclear:
- "Which task did you complete?"
- "Are you starting new work or finishing existing?"
- "Any blockers encountered?"

## Output Format
1. Show proposed updates as diffs/patches
2. Brief summary of changes
3. List any assumptions made
4. Remind about next task

## Reference
- Workflow: `.github/copilot-instructions.md`
- Templates: `projects/.agent_instructions.md`
