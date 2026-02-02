# pyWATS Copilot Commands - Quick Reference

**Print this page and keep it on your wall!**  
**Last Updated:** February 2, 2026

---

## 🚀 Available Commands

Type `/` in GitHub Copilot Chat to activate these commands:

---

### `/new-project`
**Create new project structure**

Creates complete project folder with README, ANALYSIS, PLAN, PROGRESS, TODO templates.

**Usage:**
```
/new-project cache-optimization to improve API response times
/new-project async-improvements for converter performance
```

**Creates:**
- `projects/active/{name}.project/` folder
- All 4 required markdown files
- Updates active projects list

**When to use:** Starting any new feature or improvement initiative

---

### `/update-project`
**Update project status and tracking**

Updates PROGRESS, TODO, and README based on recent work. Smart context gathering from git.

**Usage:**
```
/update-project completed Phase 1, starting Phase 2
/update-project finished metrics module implementation
/update-project blocked on API design decision
```

**Updates:**
- PROGRESS.md with timestamped entries
- TODO.md (✅ completed, 🚧 in progress)
- README.md if significant progress

**When to use:** After completing tasks, at end of day, when status changes

---

### `/close-project`
**Complete and archive project**

Full closure workflow: tests, docs, CHANGELOG, archive to completed/.

**Usage:**
```
/close-project observability-enhancement
/close-project (uses current active project)
```

**Performs:**
- Creates COMPLETION_SUMMARY.md
- Moves tests to active suite
- Moves examples to examples/
- Updates CHANGELOG.md
- Archives to completed/{quarter}/
- Commits and pushes

**When to use:** When all success criteria met and project ready to close

---

### `/update-changelog`
**Add entry to CHANGELOG.md**

Formats and adds entry under [Unreleased] with proper category and format.

**Usage:**
```
/update-changelog added Prometheus metrics module
/update-changelog fixed UUR property instantiation bug
/update-changelog improved async client performance
```

**Smart features:**
- Auto-determines category (Added/Fixed/Improved/etc.)
- Proper formatting (Keep a Changelog standard)
- Checks for duplicates
- Inserts in correct section

**When to use:** When feature/fix is complete and merged to main

---

### `/run-prerelease`
**Run pre-release validation**

Comprehensive checks: pytest, mypy, flake8, examples, CHANGELOG, version consistency.

**Usage:**
```
/run-prerelease
/run-prerelease tests only
/run-prerelease quick (skips examples)
```

**Checks:**
- ✅ Tests (target: 97%+ pass rate)
- ✅ Type checking (target: <20 mypy errors)
- ✅ Linting (no critical issues)
- ✅ Examples run successfully
- ✅ CHANGELOG complete
- ✅ Version numbers consistent

**Output:** GO ✅ | NO-GO ❌ | CAUTION ⚠️ recommendation

**When to use:** Before any release, after major changes, weekly health check

---

## 📋 Typical Workflows

### New Feature Development
```
1. /new-project {name} {description}
2. Work on it...
3. /update-project {progress}
4. /update-changelog {feature added}
5. /run-prerelease
6. /close-project {name}
```

### Quick Bug Fix
```
1. Fix the bug
2. /update-changelog fixed {bug description}
3. /run-prerelease tests only
4. Commit and push
```

### Daily Development
```
Morning:   /update-project starting {task}
Afternoon: /update-project completed {task}, starting {next}
Evening:   /update-changelog {what was added/fixed}
```

### Pre-Release
```
1. /run-prerelease
2. Review CHANGELOG [Unreleased] section
3. Fix any issues
4. Bump version
5. Release
```

---

## 🎯 Key Shortcuts

| Command | Arguments | Quick Description |
|---------|-----------|-------------------|
| `/new-project` | name description | Create project structure |
| `/update-project` | what changed | Update status docs |
| `/close-project` | [project-name] | Archive completed project |
| `/update-changelog` | what changed | Add CHANGELOG entry |
| `/run-prerelease` | [check-type] | Validate for release |

---

## 💡 Pro Tips

✅ **Be specific:** More context = better results  
✅ **Chain commands:** Use multiple in sequence for full workflows  
✅ **Review changes:** Prompts show diffs, you decide to commit  
✅ **Update incrementally:** CHANGELOG as you go, not at release  
✅ **Context-aware:** Prompts check git commits and file changes  

---

## 📚 Reference

**Full Documentation:** `.github/prompts/README.md`  
**Custom Instructions:** `.github/copilot-instructions.md`  
**Project Templates:** `projects/.agent_instructions.md`  
**Standards:** CHANGELOG (Keep a Changelog), Commits (Conventional)

---

## 🔧 Quality Gates

**Before Release:**
- Tests: 416+ passing (97%+ rate)
- Mypy: <20 errors
- Linting: No critical issues
- Examples: Execute successfully
- CHANGELOG: Complete [Unreleased] section

---

**Last Generated:** February 2, 2026  
**Auto-update:** Run `.\scripts\update-prompt-cheatsheet.ps1`  
**Version:** 1.0
