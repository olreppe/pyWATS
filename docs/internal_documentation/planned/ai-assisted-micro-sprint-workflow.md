# AI-Assisted Micro-Sprint Workflow (VS Code + GitHub Copilot)

This guide describes a proven workflow for using GitHub Copilot (or similar agents) in VS Code to run efficient, multi-document, short software development sprints.

---

## 📁 Folder Layout

Use a clear folder structure for each session:

```
.project/
├── 01_ANALYSIS.md
├── 02_IMPLEMENTATION_PLAN.md
├── 03_PROGRESS.md
├── 04_TODO.md
├── src/...
```

---

## 🔗 Document Cross-Linking

Add links at the top of each document:

```md
**Related Docs:**
- [Analysis](./01_ANALYSIS.md)
- [Implementation Plan](./02_IMPLEMENTATION_PLAN.md)
- [Progress Tracker](./03_PROGRESS.md)
- [TODO](./04_TODO.md)
```

---

## ✅ Central TODO.md

Maintain a central `TODO.md` file as the **source of truth**:

```md
# TODO.md

## ✅ Completed
- [x] Add validation to user input form
- [x] Refactor auth middleware

## 🚧 In Progress
- [ ] Implement new "quick search" feature

## 🧠 Planned
- [ ] Migrate config system to YAML
- [ ] Replace local storage with IndexedDB
```

Ask the agent to update this file regularly.

---

## 🧠 Agent Prompts by Phase

| Phase | Example Prompt |
|-------|----------------|
| Analysis → Plan | “Read `01_ANALYSIS.md`. Based on that, update the implementation plan in `02_IMPLEMENTATION_PLAN.md`.” |
| Plan → Code | “Based on `02_IMPLEMENTATION_PLAN.md`, implement step 1 in the appropriate file in `/src`. Track this in `03_PROGRESS.md` and update `TODO.md`.” |
| Progress tracking | “Mark the previous task in `03_PROGRESS.md` as completed. What is the next planned step from `TODO.md`?” |

---

## 📌 VS Code Tips

- **Pin tabs** for the core documents to keep them visible
- Use **Copilot Chat** with explicit file mentions
- Consider **external tools** (e.g. ChatGPT with uploads) for complex planning

---

## 🧭 Summary of Best Practices

| Tip | Why it helps |
|-----|--------------|
| Use strict doc naming (`01_*.md`) | Maintains agent memory and order |
| Cross-link docs | Keeps navigation easy |
| Have a single `TODO.md` | Avoids scattered task tracking |
| Update progress after each step | Keeps clarity in multi-hour sessions |
| Pin documents in VS Code | Improves Copilot’s context awareness |
