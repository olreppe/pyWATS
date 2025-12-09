# Working with Parallel Branches - Background Task Workflow

## Overview

Yes! You can have automated agents (like GitHub Copilot) work on tasks in a specific branch in the background while you continue working on your local branch. This document explains how to set up and manage this workflow effectively.

## How It Works

When you use GitHub Copilot Workspace or similar automation tools, they:

1. **Create a dedicated branch** for the task (e.g., `copilot/feature-name`)
2. **Work independently** in that branch without affecting your local work
3. **Create a Pull Request** with their changes
4. **Continue working** even while you work locally on different branches

## Benefits

- ✅ **Non-blocking workflow**: Continue your work without waiting for automated tasks
- ✅ **Parallel development**: Multiple branches can be worked on simultaneously
- ✅ **Code review integration**: Review automated changes via Pull Requests before merging
- ✅ **Safe isolation**: Agent work is isolated in separate branches
- ✅ **Easy integration**: Merge agent changes when ready via standard Git workflow

## Workflow Examples

### Example 1: Agent Works While You Develop Locally

```bash
# You're working on your feature
git checkout -b my-feature-branch
# ... make changes ...
git commit -m "Add new feature"

# Meanwhile, in GitHub, you assign a task to Copilot
# Copilot creates: copilot/background-task
# Copilot works on the task and creates a PR

# Later, you can review and merge the Copilot PR
git checkout main
git pull origin main  # Now includes copilot's merged changes
git checkout my-feature-branch
git rebase main  # Integrate the background work
```

### Example 2: Multiple Parallel Tasks

You can have multiple agents or automated tasks running simultaneously:

```
Your repo:
├── main (production)
├── your-feature-branch (you're working here)
├── copilot/refactoring (agent working)
├── copilot/docs-update (agent working)
└── copilot/bug-fix (agent working)
```

Each branch is independent, and you can merge them in any order once reviewed.

### Example 3: Continuous Local Development

```bash
# Day 1: You start a feature
git checkout -b implement-new-api
# ... work on implementation ...

# You assign documentation task to Copilot
# Copilot creates branch: copilot/api-documentation

# Day 2: You continue your work
git checkout implement-new-api
# ... continue coding ...

# Copilot finishes and creates PR for documentation
# You review PR while continuing your implementation

# Day 3: Merge Copilot's work when ready
# Your work continues uninterrupted
```

## Best Practices

### 1. Branch Naming Conventions

- **Your branches**: `feature/xyz`, `bugfix/xyz`, `your-name/task`
- **Agent branches**: Usually auto-named like `copilot/task-name`
- **Keep branches focused**: One task/feature per branch

### 2. Communication

- Use clear task descriptions when assigning work to agents
- Review agent PRs promptly to catch any issues early
- Add comments on PRs for any concerns or questions

### 3. Integration Strategy

**Option A: Merge agent work first** (if your work depends on it)
```bash
# Review and merge agent PR
git checkout main
git pull origin main

# Rebase your work on updated main
git checkout your-branch
git rebase main
```

**Option B: Merge your work first** (if independent)
```bash
# Merge your PR first
# Then agent's PR can be rebased/merged after
```

**Option C: Parallel merge** (if completely independent)
```bash
# Both PRs can be merged independently
# Resolve any conflicts during merge
```

### 4. Conflict Resolution

If agent work and your work touch the same files:

```bash
# After both changes are committed to their branches
git checkout your-branch
git fetch origin
git merge origin/main  # If agent's work was merged
# Resolve conflicts
git commit
```

## GitHub Copilot Specific Workflow

### Starting a Background Task

1. **Via GitHub Issues**:
   - Create or comment on an issue
   - Mention `@copilot` with your task
   - Copilot creates a branch and PR

2. **Via GitHub Copilot Workspace**:
   - Open Copilot Workspace
   - Describe the task
   - Select target branch (or create new)
   - Copilot works in background branch

3. **Via PR Comments**:
   - Create a PR
   - Ask Copilot to make changes
   - Changes appear as new commits

### Monitoring Background Work

- Check PR status in GitHub
- Review commits as they're pushed
- Comment on PRs for adjustments
- Approve and merge when satisfied

## Common Scenarios

### Scenario 1: "I need docs updated while I code"

```bash
# You: Working on feature implementation
# Agent: Updates documentation in parallel branch
# Result: Both completed, merge docs PR, then your PR
```

### Scenario 2: "Refactor old code while I build new features"

```bash
# You: Building new features in your branch
# Agent: Refactoring legacy code in background branch  
# Result: Independent changes, test both, merge separately
```

### Scenario 3: "Fix bugs while I develop"

```bash
# You: Developing new feature (takes days)
# Agent: Fixes urgent bugs in background branches
# Result: Bug fixes merged immediately, feature merged when ready
```

## Safety and Isolation

### Your Work is Protected

- Agent branches **don't affect your local branches**
- Changes only merge via Pull Requests
- You control when to integrate agent changes
- Full Git history maintained

### Testing Before Integration

```bash
# Test agent changes before merging
git fetch origin
git checkout copilot/task-branch
# Run tests
pytest
# If good, approve PR for merge
```

## Advanced: Multiple Agent Tasks

You can queue multiple tasks:

```bash
Task Queue:
1. copilot/add-logging (In Progress)
2. copilot/update-deps (Queued)
3. copilot/refactor-tests (Queued)

Your work: feature/new-api (Independent)
```

Each task gets its own branch and PR, processed in order or in parallel depending on dependencies.

## Troubleshooting

### "Agent and I modified the same file"

- Review changes in the PR diff
- Merge via GitHub's conflict resolution UI
- Or merge locally and resolve conflicts manually

### "I want to cancel agent's work"

- Close the PR without merging
- Delete the agent's branch (optional)
- Your local work is unaffected

### "I want agent to use my latest changes"

- Push your changes to a branch
- Ask agent to base their work on your branch
- Or merge your changes first, then agent rebases

## Summary

**Yes, you can work on your branch locally while agents work on other branches in the background!**

Key points:
- ✅ Branches are independent and isolated
- ✅ You control integration via Pull Requests
- ✅ Multiple parallel tasks are supported
- ✅ Your local work is never disrupted
- ✅ Standard Git workflows apply

This is one of the main advantages of Git's branching model combined with modern automation tools like GitHub Copilot Workspace.

## Visual Aids

For visual learners, see:
- [Workflow Diagrams](WORKFLOW_DIAGRAM.md) - Visual representations of parallel branch workflows
- [Example Script](examples/parallel_branch_workflow.sh) - Executable demonstration script

## Additional Resources

- [Git Branching Documentation](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Pull Request Best Practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)

---

*For pyWATS-specific development, see [README.md](../README.md) and [REST_API_INSTRUCTION.md](REST_API_INSTRUCTION.md)*
