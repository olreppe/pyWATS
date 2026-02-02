# GitHub Copilot Prompt Files for pyWATS

This directory contains reusable prompt files (commands) for common pyWATS workflows.

## 🚀 Quick Start

In VS Code Copilot Chat, type `/` to see available commands:

```
/new-project cache-optimization to improve API response times
/update-project completed metrics module implementation
/close-project observability-enhancement
/update-changelog added Prometheus metrics module
/run-prerelease
```

## 📋 Available Commands

### Project Management

**`/new-project`** - Create new project structure
- **Usage:** `/new-project {name} {brief description}`
- **Example:** `/new-project async-improvements to add async support for converters`
- **Creates:**
  - `projects/active/{name}.project/` folder
  - README.md, ANALYSIS.md, PLAN.md, PROGRESS.md, TODO.md
  - Updates `projects/active/README.md`
- **Reference:** `projects/.agent_instructions.md`

**`/update-project`** - Update project status
- **Usage:** `/update-project {what changed}`
- **Example:** `/update-project completed Phase 1, starting Phase 2`
- **Updates:**
  - `PROGRESS.md` with timestamped entries
  - `TODO.md` with task status (✅ completed, 🚧 in progress)
  - `README.md` if significant progress
- **Smart:** Checks git commits and file changes to infer progress

**`/close-project`** - Complete and archive project
- **Usage:** `/close-project {project-name}` or just `/close-project` for current
- **Example:** `/close-project observability-enhancement`
- **Performs:**
  - Creates COMPLETION_SUMMARY.md
  - Moves tests to active test suite
  - Moves examples to examples/
  - Updates CHANGELOG.md
  - Archives to `completed/{quarter}/`
  - Commits and pushes
- **Checklist:** Full completion workflow from `.agent_instructions.md`

### Development Workflows

**`/update-changelog`** - Add CHANGELOG entry
- **Usage:** `/update-changelog {what changed}`
- **Example:** `/update-changelog added cache module with TTL support`
- **Smart:**
  - Determines category (Added/Fixed/Improved/etc.)
  - Formats entry properly
  - Checks for duplicates
  - Inserts under `[Unreleased]`
- **Format:** Follows Keep a Changelog standard

**`/run-prerelease`** - Run pre-release checks
- **Usage:** `/run-prerelease` or `/run-prerelease {specific check}`
- **Example:** `/run-prerelease tests only`
- **Runs:**
  - pytest (all tests)
  - mypy (type checking)
  - flake8 (linting)
  - Example validation (3-5 key examples)
  - CHANGELOG review
  - Version consistency check
- **Output:** GO/NO-GO recommendation with specific issues

## 🎯 Workflow Examples

### Starting New Feature Work

```bash
# 1. Create project
/new-project performance-benchmarking to establish baseline metrics

# 2. Work on it... then update
/update-project implemented benchmark harness, completed Phase 1

# 3. Update CHANGELOG as features complete
/update-changelog added performance benchmarking framework

# 4. Before release
/run-prerelease

# 5. Complete project
/close-project performance-benchmarking
```

### Quick Bug Fix

```bash
# 1. Make fix
# 2. Update changelog
/update-changelog fixed UUR property instantiation bug

# 3. Verify
/run-prerelease tests only
```

### Daily Development

```bash
# Morning: Check status
/update-project starting work on async client

# Afternoon: Log progress
/update-project completed async HTTP client, starting async services

# Evening: Update changelog
/update-changelog improved async client performance with connection pooling
```

## 🔧 How It Works

**Prompt Files:**
- Stored in `.github/prompts/*.prompt.md`
- Triggered by typing `/command-name` in Copilot Chat
- Accept arguments via `{{args}}`
- Follow structured workflow templates

**Custom Instructions:**
- Stored in `.github/copilot-instructions.md`
- Always active (Copilot follows these rules automatically)
- Define pyWATS-specific standards and preferences

**Integration:**
- Prompts reference `projects/.agent_instructions.md` for detailed templates
- Follow CHANGELOG format from `.github/copilot-instructions.md`
- Use workspace context (git, files, tests) intelligently

## 📚 Reference

**Project Structure Templates:**
- Full templates: `projects/.agent_instructions.md`
- Quick reference: `.github/copilot-instructions.md`

**Standards:**
- CHANGELOG format: Keep a Changelog (https://keepachangelog.com/)
- Commit messages: Conventional Commits style
- Python: Type hints, pytest, mypy strict mode

**Quality Gates:**
- Tests: 97%+ pass rate (416+ tests)
- Type checking: <20 mypy errors
- Examples: Must execute successfully

## 🆘 Troubleshooting

**Command not showing up?**
- Reload VS Code window
- Check file is in `.github/prompts/` with `.prompt.md` extension
- Verify YAML frontmatter has `name:` field

**Command not working as expected?**
- Check `.github/copilot-instructions.md` for context
- Verify `projects/.agent_instructions.md` templates
- Try being more specific in arguments

**Need to customize?**
- Edit prompt files directly
- Add new commands by creating new `.prompt.md` files
- Update `.github/copilot-instructions.md` for new standards

## 💡 Pro Tips

1. **Chain commands:** Use multiple commands in sequence for full workflows
2. **Be specific:** More context in arguments = better results
3. **Review before commit:** Prompts show changes, you decide to commit
4. **Update prompts:** Improve prompts based on what works for your workflow
5. **CHANGELOG incrementally:** Update as features complete, not at release time

---

**Last Updated:** February 2, 2026  
**Version:** 1.0  
**Feedback:** Update prompts based on your workflow preferences!
