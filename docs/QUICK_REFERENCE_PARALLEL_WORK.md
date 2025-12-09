# Quick Reference: Working with Background Tasks

> **💡 New to this workflow?** See [visual diagrams](WORKFLOW_DIAGRAM.md) and [example script](examples/parallel_branch_workflow.sh) for interactive learning!

## TL;DR

**Question**: Can you do tasks for me in a specific branch (in the background) while I work on my branch locally?

**Answer**: **YES!** Absolutely. Here's how:

## The Simple Version

```
┌─────────────────────────────────────────────────────┐
│  Your Computer (Local)                              │
│  └─ your-feature-branch ← You work here           │
└─────────────────────────────────────────────────────┘
                    ↕ (independent)
┌─────────────────────────────────────────────────────┐
│  GitHub (Remote)                                    │
│  ├─ main                                           │
│  ├─ copilot/background-task ← Agent works here    │
│  └─ copilot/another-task ← Agent works here too   │
└─────────────────────────────────────────────────────┘
```

## Three-Step Workflow

### 1️⃣ Start Your Work
```bash
git checkout -b my-feature
# Code away... commits happen locally
```

### 2️⃣ Assign Background Task
- Create GitHub issue or comment
- Tag `@copilot` with task description
- Agent creates new branch and works there

### 3️⃣ Both Continue Independently
- You: Keep coding on `my-feature`
- Agent: Works on `copilot/task-name`
- No conflicts, no waiting!

## Real Example

```bash
# Monday 9 AM - You start
$ git checkout -b implement-auth
$ # ... coding ...

# Monday 10 AM - Assign to Copilot
# "Update all API documentation"
# Copilot creates: copilot/docs-update

# Monday-Tuesday - Parallel work
# You: commit, commit, commit on implement-auth
# Copilot: commit, commit, commit on copilot/docs-update

# Wednesday - Copilot finishes first
# Copilot opens PR #123
# You review & merge PR #123

# Thursday - You finish
# You open PR #124
# Merges cleanly (or minor conflicts if same files)
```

## Common Commands

### See all branches
```bash
git branch -a
```

### Check agent's work without affecting yours
```bash
git fetch origin
git checkout copilot/task-name
# Look around, test, etc.
git checkout my-feature  # Back to your work
```

### Integrate agent's merged work
```bash
git checkout main
git pull origin main
git checkout my-feature
git rebase main  # Or: git merge main
```

## When to Merge

| Scenario | Strategy |
|----------|----------|
| Agent's work is prerequisite | Merge agent PR first, rebase yours |
| Your work is urgent | Merge yours first, agent rebases |
| Completely independent | Merge in any order |
| Same files touched | Merge one, resolve conflicts in the other |

## FAQ

**Q: Will agent changes break my local work?**  
A: No. Changes are in separate branches.

**Q: Can I have multiple agents working?**  
A: Yes. Each gets their own branch.

**Q: What if we edit the same file?**  
A: Git will help you merge/resolve conflicts when you integrate.

**Q: Can I see agent's progress?**  
A: Yes. Check the PR on GitHub.

**Q: Can I cancel agent's work?**  
A: Yes. Close the PR. Your work is unaffected.

**Q: Do I need special tools?**  
A: No. Just Git and GitHub. Copilot is built-in.

## Bottom Line

✅ **YES** - Agents can work in background branches while you work locally  
✅ **SAFE** - Your local work is completely isolated  
✅ **FLEXIBLE** - Merge when you're ready, in any order  
✅ **STANDARD** - Uses normal Git branching and PRs  

This is exactly what Git branching was designed for!

---

**Learn More:**
- 📖 [Complete Workflow Guide](WORKFLOW_PARALLEL_BRANCHES.md) - Detailed instructions and best practices
- 📊 [Visual Diagrams](WORKFLOW_DIAGRAM.md) - See the workflow in pictures
- ❓ [FAQ](FAQ_PARALLEL_WORKFLOWS.md) - 25+ common questions answered
- 🎬 [Example Script](examples/parallel_branch_workflow.sh) - Run: `bash docs/examples/parallel_branch_workflow.sh`
