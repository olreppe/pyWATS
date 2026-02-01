# GitHub Copilot Best Practices

A guide to using GitHub Copilot effectively in VS Code, including workflows, limitations, and enhancements using Issues and structured documents.

---

## 🧠 Understanding GitHub Copilot

GitHub Copilot provides real-time code suggestions based on:
- Open files
- Recent edits
- File names
- Comments and context near the cursor

Copilot does **not** persist long-term memory between sessions and can lose track of multiple documents unless you guide it.

---

## ✅ Best Practices for Effective Copilot Use

### 1. **Use Structured Documents**
Break your sprint into clear documents:
- `01_ANALYSIS.md`
- `02_IMPLEMENTATION_PLAN.md`
- `03_PROGRESS.md`
- `04_TODO.md`

Use pinned tabs in VS Code to keep them visible and give Copilot more consistent context.

---

### 2. **Prompt Copilot Chat Effectively**
Instead of vague commands, be specific:
> “Based on `02_IMPLEMENTATION_PLAN.md`, implement the first task in `src/utils/formatter.ts`. Update `03_PROGRESS.md` after.”

---

### 3. **Maintain a Central TODO List**
Track what’s planned, in progress, and done:
```md
## ✅ Completed
- [x] Refactor auth logic

## 🚧 In Progress
- [ ] Implement feature toggle

## 🧠 Planned
- [ ] Add audit log
```

Let Copilot update this list step by step.

---

### 4. **Use GitHub Issues for Execution**
Once a task moves from draft to actionable:
- Promote `.md` section to a GitHub Issue
- Use labels like `feature`, `p1`, `in-progress`
- Link PRs to Issues (`closes #12`)
- Use checklists to track subtasks

---

## 🧩 Docs vs. Issues: When to Use Each

| Use Case | Use Docs | Use Issues |
|----------|----------|-------------|
| Fast ideation | ✅ | ❌ |
| Local experiments | ✅ | ❌ |
| Long-term tracking | ❌ | ✅ |
| Collaboration | ❌ | ✅ |
| Task progress | ❌ | ✅ |
| Automation | ❌ | ✅ |

---

## 🧱 Scaling GitHub Issues

- **Labels**: `feature`, `bug`, `tech-debt`, `p1`
- **Milestones**: Group Issues into sprints or releases
- **Projects**: Use kanban boards for active tasks
- **Search**: Filter with `label:bug is:open milestone:"Sprint 1"`

---

## 🚀 Hybrid Workflow Example

1. Write analysis in `.md`
2. Generate checklist in implementation plan
3. Promote major features to GitHub Issues
4. Use Issues to track work and reference in commits/PRs
5. Use `.md` progress file or `TODO.md` locally during dev
6. Ask Copilot to update both `.md` and Issues

---

## 🧠 Final Tips

- Use pinned tabs and naming conventions
- Always specify which file or doc Copilot should refer to
- Rephrase prompts to help Copilot refocus
- Consider linking `.md` docs to GitHub Issues for traceability
- Use Copilot + Issues + Chat + Docs for full-cycle sprint workflows

---

This guide helps you make GitHub Copilot not just a code helper — but a **sprint partner**.
