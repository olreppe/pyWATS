# pyWATS Project - Copilot Custom Instructions

**Project:** pyWATS Python API  
**Type:** Manufacturing test data management library  
**Standards:** Python 3.8+, type hints, pytest, mypy strict mode

---

## 🎯 Core Principles

1. **Type Safety First** - Use type hints everywhere, mypy strict mode enabled
2. **Test Coverage** - Maintain 97%+ test pass rate (416+ tests)
3. **Documentation** - User-facing docs ship with package
4. **Backward Compatibility** - Breaking changes require migration guides
5. **Project Structure** - Follow `.agent_instructions.md` for all projects

---

## 📁 Project Workflow Standards

### When Creating Projects
- **Structure:** Always create in `projects/active/{name}.project/` with:
  - `README.md` - Status, objectives, success criteria
  - `01_ANALYSIS.md` - Requirements, constraints, risks
  - `02_IMPLEMENTATION_PLAN.md` - Step-by-step phases
  - `03_PROGRESS.md` - Real-time updates with timestamps
  - `04_TODO.md` - Task checklist (✅ ✗ 🚧)
- **Timestamps:** All documents MUST include `Created` and `Last Updated` timestamps
- **Reference:** See `projects/.agent_instructions.md` for full templates

### When Updating Projects
- **TODO.md:** Mark task 🚧 BEFORE starting, ✅ IMMEDIATELY after completion
- **PROGRESS.md:** Add timestamped entry after each significant step
- **README.md:** Update status percentage when phases complete
- **Last Updated:** Update timestamp header when making significant changes
- **Frequency:** Update during work (not batched at end) for crash recovery

### When Closing Projects
Follow completion checklist in `.agent_instructions.md`:
1. All tests passing
2. Move project tests to `tests/` suite
3. Move examples to `examples/`
4. Update `CHANGELOG.md` under `[Unreleased]`
5. Create `COMPLETION_SUMMARY.md` with timestamps
6. Rename folder to `MMDDHHMM-{project-name}.project/` format
7. Move to `projects/completed/{quarter}/` (e.g., `projects/completed/2026-q1/`)
8. Commit and push

---

## 📝 CHANGELOG Standards

**Location:** `CHANGELOG.md` (repository root)

**Format:** Keep a Changelog (https://keepachangelog.com/)

**Categories (in order):**
- `Added` - New features
- `Changed` - Changes to existing functionality
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features
- `Fixed` - Bug fixes
- `Security` - Security fixes
- `Improved` - Performance, docs, or quality improvements

**Entry Format:**
```markdown
### Added
- **Feature Name**: Brief description
  - **Capability 1**: Details with example
  - **Capability 2**: Details
  - **Tests**: X new tests added (if significant)
```

**When to Update:**
- Add entry when feature/fix is complete and merged to main
- Update under `[Unreleased]` section
- Agent should check existing entries to avoid duplicates
- Include file paths when helpful: `src/pywats/core/metrics.py`

---

## 🧪 Testing Standards

**Commands:**
- Run all: `pytest`
- Run domain: `pytest tests/domains/{domain}/`
- Run with coverage: `pytest --cov=src/pywats`
- Count tests: `pytest --collect-only -q | Measure-Object -Line`

**Requirements:**
- All new features must have tests
- Tests must be in active suite (not project folder)
- Test names should be descriptive: `test_get_product_with_valid_id_returns_product`
- Use fixtures from `tests/conftest.py`

**Current Status:** 416 passing, 12 skipped (97% pass rate)

---

## 📚 Documentation Standards

**User-Facing Docs (Ship with Package):**
- `docs/guides/*.md` - Conceptual guides
- `docs/api/*.rst` - Sphinx API reference
- `examples/*/*.py` - Runnable examples with detailed comments
- `README.md` - Quick start and overview
- `CHANGELOG.md` - Version history

**Internal Docs (Development Only):**
- `docs/internal_documentation/` - Architecture, health checks, analysis
- `projects/` - Active work tracking
- `.agent_instructions.md` - Workflow standards

**Rules:**
- Examples must be runnable and tested
- API docs use Sphinx RST format
- Guides use Markdown
- Code examples in guides must show imports and full context

---

## 🔍 Code Review Standards

**Before Committing:**
1. Run `pytest` - all tests must pass
2. Run `mypy src/pywats` - check for type errors (target <20 errors)
3. Check `get_errors()` - no compile/lint errors
4. Verify examples execute without errors
5. Update CHANGELOG if user-facing change

**Commit Message Format:**
```
type(scope): Brief description

- Detailed change 1
- Detailed change 2  
- Tests: X passing
- Docs: Updated guides/examples
```

**Types:** feat, fix, docs, test, refactor, perf, chore

---

## 🚀 Pre-Release Checklist

**Run via:** `.\scripts\pre_release_check.ps1` or manually:

1. **Tests:** `pytest` - All passing
2. **Type Checking:** `mypy src/pywats` - Minimize errors (<20)
3. **Linting:** `flake8 src/pywats --max-line-length=120`
4. **Examples:** Run 3-5 key examples to verify
5. **CHANGELOG:** Review `[Unreleased]` section for completeness
6. **Version:** Update in `pyproject.toml` and `docs/api/conf.py`
7. **Documentation:** Regenerate Sphinx docs if API changed

---

## 🗂️ File Organization

**Source Code:**
- `src/pywats/` - Main package
- `src/pywats/domains/{domain}/` - Domain services
- `src/pywats/core/` - Shared utilities (cache, metrics, etc.)
- `src/pywats_client/` - Client service components

**Tests:**
- `tests/domains/{domain}/` - Domain-specific tests
- `tests/integration/` - Cross-domain integration tests
- `tests/client/` - Client service tests
- `tests/fixtures/` - Shared test data

**Documentation:**
- `docs/guides/` - User guides (installation, architecture, patterns)
- `docs/api/` - Sphinx API reference
- `docs/internal_documentation/` - Internal analysis and planning
- `examples/` - Runnable example scripts

**Projects:**
- `projects/active/` - Current work (max 5 projects)
- `projects/planned/` - Future initiatives
- `docs/internal_documentation/completed/` - Archived completed projects

---

## 🎨 Python Style Guide

**Standards:**
- Type hints on all functions: `def get_product(id: str) -> Product:`
- Docstrings: Google style for public APIs
- Line length: 120 characters (not 80)
- Imports: Standard lib → Third party → Local
- Naming: `snake_case` for functions/variables, `PascalCase` for classes
- Enums: Use for type-safe options (see `StatusFilter`, `Dimension`, etc.)

**Example:**
```python
from typing import Optional
from pywats.models import Product

def get_product(product_id: str, include_bom: bool = False) -> Optional[Product]:
    """Get product by ID.
    
    Args:
        product_id: Unique product identifier
        include_bom: Include bill of materials
        
    Returns:
        Product instance or None if not found
    """
    # Implementation
```

---

## 🤖 Agent Behavior Defaults

**When Asked for Status:**
- Check `projects/active/README.md` first
- Reference recent commits: `git log --oneline -10`
- Check test results: `pytest --collect-only`
- Update PROGRESS.md if working on active project

**When Making Changes:**
- Read existing code/docs before editing
- Verify tests pass after changes
- Update CHANGELOG if user-facing
- Commit with descriptive message

**When Creating Documentation:**
- Check existing docs for similar content
- Use examples from `examples/` folder
- Include code that actually runs
- Cross-reference related guides

**When Blocked:**
- Document blocker in project TODO.md with ⏸️
- Ask clarifying questions
- Don't guess at implementation details
- Suggest alternatives if possible

---

## 🏷️ Domain Knowledge

**WATS Terminology:**
- **Unit** - Device being tested (has serial number)
- **Report** - Test result from single test execution  
- **Run** - Test execution sequence (Run 1, Run 2, etc.)
- **Process** - Type of test (ICT, FCT, EOL, etc.)
- **UUT** - Unit Under Test report
- **UUR** - Unit Under Repair report

**Architecture:**
- **API Layer** - `src/pywats/` - Main synchronous API
- **Client Layer** - `src/pywats_client/` - Service/GUI components
- **Async Support** - Async variants for all domain services
- **Converters** - File format converters (isolated process execution)

---

## 📊 Quality Metrics (Current)

- **Test Pass Rate:** 97% (416 passing, 12 skipped)
- **Mypy Errors:** 16 (down from 740 - 98% improvement)
- **Domain Health Scores:** 54-80/80 across 9 domains
- **Documentation:** 8/8 domains with Sphinx docs + 137 examples
- **Python Version:** 3.14.0 (target 3.8+ compatibility)

---

---

## 🎯 Context-Specific Instruction Overlays

Agents MUST load additional instruction files based on task context using the **combined approach**.

### Instruction Manifest
See `.instruction_manifest.md` for complete overlay system and loading algorithm.

### Combined Loading Approach

**Load overlays from THREE sources (in order):**

1. **Context Keywords** (from task description)
   - "implement", "service", "model", "api" → `.source_code_instructions.md`
   - "doc", "example" → `.docs_instructions.md`
   - "test", "fixture" → `.test_instructions.md`
   - "release", "changelog" → `.deployment_instructions.md`
   - "project" → `projects/.agent_instructions.md`

2. **File Path Patterns** (from current file)
   - `src/**` → `.source_code_instructions.md` (P0 - MOST CRITICAL!)
   - `docs/**`, `examples/**` → `.docs_instructions.md`
   - `tests/**` → `.test_instructions.md`
   - `CHANGELOG.md`, `pyproject.toml` → `.deployment_instructions.md`
   - `projects/active/**` → `projects/.agent_instructions.md`

3. **Directory Walk** (walk up from current file)
   - Check each parent directory for `.agent_instructions.md`
   - Load all found (most specific = highest priority)
   - Example: `src/pywats/domains/.agent_instructions.md`

### Active Overlays

| Overlay | Context | Priority | Purpose |
|---------|---------|----------|---------|
| `.source_code_instructions.md` | src/ (production code) | **P0** | Type-safe source code (MOST CRITICAL) |
| `.docs_instructions.md` | docs/, examples/ | **P0** | Type-safe documentation code |
| `.test_instructions.md` | tests/ | **P0** | Type-safe test fixtures |
| `.deployment_instructions.md` | CHANGELOG, releases | **P1** | Release standards, endpoint risk |
| `projects/.agent_instructions.md` | projects/active/ | **P1** | Project structure |
| `{dir}/.agent_instructions.md` | Any directory | **P2** | Directory-specific patterns |

### Agent Workflow (MANDATORY)

**Before starting ANY task:**

```
1. Parse task description for keywords
2. Identify current file path
3. Load base instructions (.github/copilot-instructions.md)
4. Load context overlays (from keywords)
5. Load file path overlays
6. Walk directory tree for .agent_instructions.md files
7. Announce loaded overlays to user
8. Proceed with combined instruction set
```

### Agent Announcement (REQUIRED)

**ALWAYS state which overlays are loaded:**

```
"Loading instruction overlays for this task:
 - .docs_instructions.md (P0 - type-safe documentation)
 - .test_instructions.md (P0 - type-safe tests)
 - src/pywats/domains/.agent_instructions.md (P2 - domain patterns)

Proceeding with combined instruction set..."
```

### Creating New Directory Overlays

**To add directory-specific instructions:**

1. Create `.agent_instructions.md` in target directory
2. Use standard instruction template (see `.instruction_manifest.md`)
3. Define priority level (P0/P1/P2)
4. Include validation steps
5. Update `.instruction_manifest.md` registry

**No need to modify base instructions** - directory overlays are auto-discovered!

---

**Last Updated:** February 3, 2026  
**Reference:** `.instruction_manifest.md` for complete overlay system
