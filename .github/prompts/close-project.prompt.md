---
name: close-project
description: Complete project and archive (COMPLETION_SUMMARY, move to completed/, update CHANGELOG)
argument-hint: "Project name to close, e.g., 'observability-enhancement' or leave empty for current project"
---

You are my project completion assistant for the pyWATS repository.

## Goal
Complete a project following the full closure checklist from `.agent_instructions.md`.

## Input from User
{{args}}

## Steps

### 1. Identify Project to Close
- If user specified name in {{args}}, use that
- Otherwise check `projects/active/README.md` for likely candidate
- Verify project is actually complete (all success criteria met)
- If not complete, warn user and ask for confirmation

### 2. Run Completion Checklist

**Code Integration:**
- ✅ All tasks in TODO.md marked complete?
- ✅ All tests passing? (run `pytest`)
- ✅ Type hints verified? (check `mypy` if applicable)

**Test Suite Integration:**
- Move tests from `projects/{name}/tests/` → `tests/` (appropriate subdirectory)
- Verify discovery: `pytest --collect-only -q | Measure-Object -Line`
- Run new tests: `pytest tests/{path}/` to verify
- Document new test count

**Examples Integration:**
- Check for `projects/{name}/examples/`
- Move to `examples/{appropriate-folder}/`
- Update `examples/README.md` if needed
- Verify examples run

**Documentation Updates:**
- Check if main `README.md` needs update (user-facing features)
- Check if `docs/guides/` needs new guide
- Check if domain health docs need update

### 3. Update CHANGELOG.md

**Add entry under `[Unreleased]` section:**

Determine category (Added/Changed/Fixed/Improved)

Format:
```markdown
### {Category}
- **{Feature Name}**: {Brief description}
  - **{Capability 1}**: {Details}
  - **{Capability 2}**: {Details}
  - **Tests**: {X new tests added} (if significant)
  - **Files**: {Key files, if helpful}
```

Check for duplicates - don't add if already documented

### 4. Create COMPLETION_SUMMARY.md

In project folder, create comprehensive summary:
```markdown
# Completion Summary: {Project Name}

**Completed:** {Date}
**Duration:** {Estimate}
**Total Effort:** {Hours estimate}

## Deliverables
- Source Files Modified: {count} files
- Tests Added: {count} tests (all passing)
- Documentation: {list}
- Examples: {list}

## Test Results
- Total Tests: {new count} (up from {previous})
- New Tests: {count}
- All Passing: ✅

## Key Achievements
- {Achievement 1}
- {Achievement 2}

## Known Limitations
- {Any limitations}

## Future Work
- {Future enhancements}
```

### 5. Archive Project

**Move entire folder:**
```
projects/active/{name}.project/ 
  → docs/internal_documentation/completed/{current-quarter}/{name}.project/
```

Determine quarter: 2026-q1, 2026-q2, etc.

**Update `projects/active/README.md`:**
- Remove from "Current Active Items"
- Add to "Recently Completed" section

### 6. Commit and Push

**Commit message:**
```
docs: Complete and archive {project-name}

- Created COMPLETION_SUMMARY.md with deliverables
- Moved {X} tests to active test suite
- Moved {Y} examples to examples/
- Updated CHANGELOG.md under [Unreleased]
- Archived to completed/{quarter}/

Deliverables: {key achievements}
```

**Commands:**
```bash
git add -A
git commit -m "{message}"
git push origin main
```

### 7. Present Summary

Show:
- ✅ Project closed successfully
- 📊 Final stats (files, tests, docs)
- 📝 CHANGELOG entry added
- 📁 Archived to: `completed/{quarter}/{name}.project/`
- 🔗 Commit hash

### 8. Verify Completion

Before proceeding, check:
- All tests still passing after moves?
- CHANGELOG entry makes sense?
- Project folder moved correctly?
- No loose ends in TODO.md?

If issues found, pause and report.

## Output Format
1. Show proposed CHANGELOG entry
2. Show COMPLETION_SUMMARY content
3. Confirm with user before moving/committing
4. Execute moves and commit
5. Final summary with links

## Reference
- Checklist: `projects/.agent_instructions.md` → Section "📦 Completion Checklist"
- Standards: `.github/copilot-instructions.md`
