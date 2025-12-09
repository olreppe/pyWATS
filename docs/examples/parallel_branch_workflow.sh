#!/bin/bash

# Example: Working with Parallel Branches
# This script demonstrates how to work on your local branch
# while an agent works on a separate branch in the background

# ============================================================
# SCENARIO: You're implementing a new feature while asking
# an agent to update documentation in parallel
# ============================================================

echo "=== Parallel Branch Workflow Example ==="
echo ""

# ------------------------------------------------------------
# STEP 1: You start working on your feature
# ------------------------------------------------------------
echo "📝 STEP 1: Start your feature work"
echo "$ git checkout -b feature/new-api-endpoint"
echo "Switched to a new branch 'feature/new-api-endpoint'"
echo ""
echo "# You make changes to your feature"
echo "$ vim src/pywats/modules/new_endpoint.py"
echo "$ git add src/pywats/modules/new_endpoint.py"
echo "$ git commit -m 'Add new API endpoint implementation'"
echo "[feature/new-api-endpoint abc1234] Add new API endpoint implementation"
echo ""

# ------------------------------------------------------------
# STEP 2: Meanwhile, assign task to agent via GitHub
# ------------------------------------------------------------
echo "🤖 STEP 2: Assign documentation task to agent"
echo ""
echo "On GitHub, you create an issue or comment:"
echo "  '@copilot Please update all API documentation to include"
echo "   the new endpoint patterns and add examples.'"
echo ""
echo "Copilot creates a new branch: copilot/update-api-docs"
echo "Copilot opens PR #42 with documentation updates"
echo ""

# ------------------------------------------------------------
# STEP 3: Both continue working independently
# ------------------------------------------------------------
echo "⚡ STEP 3: Parallel work happens"
echo ""
echo "YOU (on feature/new-api-endpoint):"
echo "$ git commit -m 'Add input validation'"
echo "$ git commit -m 'Add error handling'"
echo "$ git commit -m 'Add unit tests'"
echo ""
echo "AGENT (on copilot/update-api-docs):"
echo "  Commit: 'Update API documentation structure'"
echo "  Commit: 'Add new endpoint examples'"
echo "  Commit: 'Update README with new patterns'"
echo "  PR #42 is ready for review"
echo ""

# ------------------------------------------------------------
# STEP 4: Review agent's work without disrupting yours
# ------------------------------------------------------------
echo "👀 STEP 4: Review agent's work (optional)"
echo ""
echo "# Fetch latest changes from remote"
echo "$ git fetch origin"
echo ""
echo "# Check agent's branch without affecting your work"
echo "$ git checkout copilot/update-api-docs"
echo "Switched to branch 'copilot/update-api-docs'"
echo ""
echo "# Review the changes"
echo "$ git log --oneline -3"
echo "def5678 Update README with new patterns"
echo "abc9012 Add new endpoint examples"
echo "xyz3456 Update API documentation structure"
echo ""
echo "# Run any tests to verify"
echo "$ pytest tests/test_docs.py"
echo "✓ All tests passed"
echo ""
echo "# Return to your work"
echo "$ git checkout feature/new-api-endpoint"
echo "Switched to branch 'feature/new-api-endpoint'"
echo ""

# ------------------------------------------------------------
# STEP 5: Merge agent's PR (via GitHub)
# ------------------------------------------------------------
echo "✅ STEP 5: Agent's work is complete"
echo ""
echo "On GitHub, you review PR #42 and click 'Merge pull request'"
echo "The copilot/update-api-docs branch is merged into main"
echo ""

# ------------------------------------------------------------
# STEP 6: Continue your work, integrate when ready
# ------------------------------------------------------------
echo "🔄 STEP 6: Optionally integrate agent's changes"
echo ""
echo "# Update your local main branch"
echo "$ git checkout main"
echo "$ git pull origin main"
echo "Updating abc1234..def5678"
echo "Fast-forward"
echo " docs/API.md | 50 ++++++++"
echo " README.md   | 10 ++"
echo ""
echo "# Integrate into your feature branch (if needed)"
echo "$ git checkout feature/new-api-endpoint"
echo "$ git rebase main"
echo "Successfully rebased and updated refs/heads/feature/new-api-endpoint"
echo ""
echo "# Or use merge if you prefer"
echo "# $ git merge main"
echo ""

# ------------------------------------------------------------
# STEP 7: Complete your work
# ------------------------------------------------------------
echo "🎉 STEP 7: Finish your feature"
echo ""
echo "$ git push origin feature/new-api-endpoint"
echo "# Open PR #43 on GitHub"
echo "# Both your feature and agent's docs are now complete!"
echo ""

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
echo "=== SUMMARY ==="
echo ""
echo "Timeline:"
echo "  Day 1 AM:  You start feature/new-api-endpoint"
echo "  Day 1 AM:  Assign docs task to agent"
echo "  Day 1 PM:  Agent works on copilot/update-api-docs"
echo "  Day 1 PM:  You continue on feature/new-api-endpoint"
echo "  Day 2 AM:  Agent finishes, PR #42 merged"
echo "  Day 2 PM:  You finish, open PR #43"
echo ""
echo "Benefits:"
echo "  ✓ No waiting - you worked in parallel"
echo "  ✓ No conflicts - separate branches"
echo "  ✓ Independent reviews - each PR reviewed separately"
echo "  ✓ Clean history - proper Git workflow"
echo ""
echo "Branches:"
echo "  main                        (production)"
echo "  ├─ feature/new-api-endpoint (your work)"
echo "  └─ copilot/update-api-docs  (agent work - merged)"
echo ""

# ------------------------------------------------------------
# Advanced Scenarios
# ------------------------------------------------------------
echo "=== ADVANCED SCENARIOS ==="
echo ""
echo "Multiple parallel tasks:"
echo "$ git branch -a"
echo "* feature/new-api-endpoint           (you)"
echo "  remotes/origin/copilot/update-docs  (agent 1)"
echo "  remotes/origin/copilot/fix-bug-123  (agent 2)"
echo "  remotes/origin/copilot/refactor-db  (agent 3)"
echo ""
echo "Each can be worked on, reviewed, and merged independently!"
echo ""

echo "=== END OF EXAMPLE ==="
