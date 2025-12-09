# FAQ: Parallel Branch Workflows

## General Questions

### Q1: Can you do tasks for me in a specific branch (in the background) while I work on my branch locally?

**A: YES, absolutely!** This is one of the core benefits of using Git with automated agents like GitHub Copilot.

- You work on your local branch (`feature/my-work`)
- Agent works on a separate remote branch (`copilot/agent-task`)
- Both branches are independent and isolated
- You merge changes via Pull Requests when ready
- No waiting, no blocking, full parallel workflow

See: [Quick Reference](QUICK_REFERENCE_PARALLEL_WORK.md)

---

### Q2: Will the agent's work interfere with my local changes?

**A: No.** Your local branch and the agent's remote branch are completely separate until you explicitly merge them.

Changes only integrate when:
- You review the agent's Pull Request
- You approve and merge it
- You optionally pull those changes into your branch

---

### Q3: What if the agent and I edit the same file?

**A: Git handles this gracefully.**

- If changes are to different parts of the file: Git merges automatically
- If changes conflict: Git asks you to resolve conflicts during merge
- Conflicts are resolved once, at integration time, not during development

Example:
```bash
# Agent merged their PR first
git checkout your-branch
git rebase main
# Git: "Conflict in config.py - please resolve"
# You resolve, keeping the parts you need from both versions
git add config.py
git rebase --continue
```

---

### Q4: How many parallel tasks can I have?

**A: Unlimited!** Git supports as many branches as you need.

Common scenarios:
- You: 1 feature branch (local)
- Agent 1: Documentation update (remote)
- Agent 2: Bug fix (remote)
- Agent 3: Refactoring (remote)
- Agent 4: Dependency updates (remote)

Each is independent. Merge in any order.

---

### Q5: Do I need special tools or setup?

**A: No.** Just standard Git and GitHub.

What you have already:
- Git (for version control)
- GitHub (for remote repository)
- GitHub Copilot (built into GitHub)

That's it! No plugins, no special configuration needed.

---

## Workflow Questions

### Q6: How do I start a background task?

**Option 1: Via GitHub Issue**
```
Create or comment on an issue:
"@copilot Please refactor the authentication module to use JWT"
```

**Option 2: Via GitHub Copilot Workspace**
```
1. Go to your repository on GitHub
2. Click "Code" → "Open with Copilot"
3. Describe the task
4. Copilot creates branch and works on it
```

**Option 3: Via Pull Request comments**
```
On any PR, comment:
"@copilot Please add type hints to all functions"
```

---

### Q7: How do I check the agent's progress?

**Check on GitHub:**
- Go to Pull Requests tab
- Find the agent's PR (usually named like "copilot/task-name")
- View commits, diff, and status checks

**Check locally:**
```bash
git fetch origin
git checkout copilot/task-name
# Review the changes
git log
git diff main..HEAD
```

---

### Q8: Can I cancel an agent's task?

**A: Yes, easily.**

On GitHub:
- Close the agent's Pull Request
- Optionally delete the branch

Your work is completely unaffected. The agent's branch just won't be merged.

---

### Q9: What order should I merge PRs?

**It depends on dependencies:**

**Independent work:** Any order
```
Agent's docs PR: Merge anytime
Your feature PR: Merge anytime
```

**Dependent work:** Prerequisite first
```
Agent's API refactor: Merge first (breaking changes)
Your new feature: Rebase on updated main, then merge
```

**Urgent work:** Priority first
```
Agent's bug fix: Merge immediately (critical)
Your feature: Can wait, merge later
```

---

### Q10: How do I integrate agent's merged changes into my branch?

**Option A: Rebase (clean history)**
```bash
git checkout main
git pull origin main
git checkout your-branch
git rebase main
```

**Option B: Merge (preserves history)**
```bash
git checkout your-branch
git merge main
```

Both work! Rebase is cleaner, merge is simpler.

---

## Technical Questions

### Q11: How does Git keep branches separate?

Git stores each branch as a separate pointer to commits. Changes in one branch don't affect other branches until you merge.

```
Commit graph:
       A---B---C  main
            \
             D---E  your-branch
              \
               F---G  copilot/task
```

Each branch is independent. Merging combines them.

---

### Q12: What if I pull changes and get conflicts?

**Resolve conflicts step by step:**

```bash
git pull origin main
# Git: "Conflict in file.py"

# Open file.py, you'll see:
<<<<<<< HEAD
your changes
=======
agent's changes
>>>>>>> main

# Edit to keep what you need
# Remove conflict markers
# Save file

git add file.py
git commit -m "Resolve merge conflict"
```

---

### Q13: Can I test agent's changes before merging?

**Yes! Multiple ways:**

**1. Checkout agent's branch locally:**
```bash
git fetch origin
git checkout copilot/task-name
npm test  # or pytest, etc.
```

**2. Merge into test branch:**
```bash
git checkout -b test-integration
git merge origin/copilot/task-name
git merge your-feature-branch
# Test everything together
```

**3. Wait for CI/CD:**
```
Agent's PR automatically runs tests
Check status on GitHub before merging
```

---

### Q14: What if I accidentally push to the wrong branch?

**Reset the branch:**

```bash
# Oh no, I pushed to copilot/task-name by mistake
git checkout copilot/task-name
git reset --hard origin/copilot/task-name  # Reset to agent's version
git checkout your-branch  # Back to safety
```

Note: Only do this if you haven't already pushed! Once pushed, you may need to coordinate with others.

---

### Q15: Can the agent work on my local branch?

**No, and that's a good thing!**

Agents work on remote branches only. This means:
- ✅ Your local work is never interrupted
- ✅ You control when to integrate changes
- ✅ You always have an escape hatch (just don't merge)

If you want agent to build on your work:
```bash
# Push your branch
git push origin your-branch

# Ask agent to work on it
"@copilot Please add tests to the your-branch branch"
```

---

## Best Practices Questions

### Q16: Should I rebase or merge?

**Use rebase when:**
- You want clean, linear history
- Your branch is private (not shared with others)
- You're comfortable with rebase

**Use merge when:**
- You want to preserve all history
- Branch is shared with others
- You prefer simplicity

Both are valid! Choose what you're comfortable with.

---

### Q17: How often should I integrate agent's changes?

**Two approaches:**

**Approach 1: Integrate frequently**
```
Agent finishes task → Review → Merge → Pull into your branch
Benefit: Stay up to date, smaller conflicts
```

**Approach 2: Integrate at milestones**
```
Agent completes multiple tasks → Review all → Merge all → Update once
Benefit: Less interruption, batch updates
```

Choose based on how coupled the work is.

---

### Q18: Should I assign multiple tasks to agents at once?

**Yes, if they're independent!**

Good parallel tasks:
- ✅ Update documentation (agent 1)
- ✅ Fix unrelated bug (agent 2)
- ✅ Refactor old module (agent 3)

Avoid parallel dependent tasks:
- ❌ Refactor API (agent 1)
- ❌ Add new API endpoint (agent 2) ← depends on agent 1

---

### Q19: What should I do if agent's work is incorrect?

**Several options:**

**1. Request changes via PR review:**
```
Comment on the PR: "Please update the error handling logic"
Agent will make additional commits
```

**2. Fix it yourself:**
```
Checkout agent's branch
Make corrections
Push changes
Merge PR
```

**3. Close and redo:**
```
Close PR
Request agent to try again with clearer instructions
```

---

### Q20: How do I avoid merge conflicts?

**Best practices:**

1. **Divide work by files:**
   - You: Work on feature modules
   - Agent: Work on documentation

2. **Integrate frequently:**
   - Pull main regularly
   - Rebase your branch often

3. **Communicate clearly:**
   - Be specific about what agent should change
   - Avoid overlapping tasks

4. **Accept some conflicts:**
   - Small conflicts are normal
   - Easy to resolve
   - Don't over-optimize to avoid them

---

## Troubleshooting

### Q21: "I can't see the agent's branch"

**Solution:**
```bash
git fetch origin
git branch -a  # Lists all branches including remote
```

---

### Q22: "Git says I have uncommitted changes"

**Solution:**
```bash
# Save your work
git stash

# Switch to agent's branch
git checkout copilot/task-name

# Later, restore your work
git checkout your-branch
git stash pop
```

---

### Q23: "I merged the wrong PR!"

**Solution:**
```bash
# Revert the merge commit
git revert -m 1 <merge-commit-hash>
git push origin main
```

This creates a new commit that undoes the merge, keeping history intact.

---

### Q24: "My branch is behind main"

**This is normal!** Update when you're ready:

```bash
git checkout your-branch
git pull origin main
# Or: git rebase origin/main
```

---

### Q25: "Agent created wrong branch name"

**No problem:**

```bash
# Rename the branch on GitHub
git fetch origin
git checkout copilot/wrong-name
git branch -m copilot/correct-name
git push origin copilot/correct-name
git push origin --delete copilot/wrong-name
```

Or just work with the name agent chose - branch names don't affect functionality.

---

## Summary

**Bottom Line:**
- ✅ Yes, agents can work on background branches while you work locally
- ✅ Branches are isolated and safe
- ✅ You control integration via Pull Requests
- ✅ Standard Git workflow - nothing special needed
- ✅ Parallel work speeds up development

**Most Important:**
- Your local work is never disrupted by agent work
- Changes only integrate when you explicitly merge PRs
- Conflicts (if any) are resolved at merge time
- You can have unlimited parallel branches

This is exactly what Git and GitHub were designed for! 🎉

---

## Still Have Questions?

- See full workflow guide: [WORKFLOW_PARALLEL_BRANCHES.md](WORKFLOW_PARALLEL_BRANCHES.md)
- See quick reference: [QUICK_REFERENCE_PARALLEL_WORK.md](QUICK_REFERENCE_PARALLEL_WORK.md)
- See visual diagrams: [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)
- Run example script: `bash docs/examples/parallel_branch_workflow.sh`
