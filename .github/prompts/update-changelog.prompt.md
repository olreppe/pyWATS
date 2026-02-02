---
name: update-changelog
description: Add entry to CHANGELOG.md under [Unreleased] section
argument-hint: "What changed? e.g., 'added cache module' or 'fixed UUR property access bug'"
---

You are my changelog assistant for the pyWATS repository.

## Goal
Add a properly formatted entry to `CHANGELOG.md` under the `[Unreleased]` section.

## Input from User
{{args}}

## Steps

### 1. Gather Context
Check workspace for:
- Recent commits: `git log --oneline -10`
- Modified files: `git status` or `git diff --stat`
- User's description in {{args}}
- Current branch (might indicate feature)

### 2. Determine Category

**Categories (in order):**
- `Added` - New features, new modules, new capabilities
- `Changed` - Changes to existing functionality (API changes, behavior changes)
- `Deprecated` - Soon-to-be removed features
- `Removed` - Removed features or code
- `Fixed` - Bug fixes, error corrections
- `Security` - Security-related fixes
- `Improved` - Performance, documentation, or quality improvements (non-breaking)

**Decision rules:**
- New file/module → `Added`
- Bug fix → `Fixed`
- Performance/docs improvement → `Improved`
- API change → `Changed`
- When unsure → ask user

### 3. Format Entry

**Standard format:**
```markdown
### {Category}
- **{Feature/Module Name}**: {Brief description}
  - **{Capability 1}**: {Details with example if helpful}
  - **{Capability 2}**: {Details}
  - **Tests**: {X new tests added} (only if significant, e.g., 10+)
  - **Files**: {Key file paths} (only if helpful for reference)
```

**Examples:**

```markdown
### Added
- **Prometheus Metrics Module**: Comprehensive observability with metrics collection
  - **HTTP Tracking**: Request/response latency and error rates with decorator support
  - **System Metrics**: CPU, memory, and thread monitoring via background thread
  - **Queue Metrics**: Queue depth and processing time tracking
  - **Metrics Server**: `/metrics` endpoint in Prometheus format
  - **Tests**: 15 new tests for metrics collection and export
  - **Files**: `src/pywats/core/metrics.py` (395 lines)
```

```markdown
### Fixed
- **UUR Report Property Access**: Fixed `properties` attribute returning dict instead of UURProperties object
  - **Issue**: Direct dictionary access bypassed property validation
  - **Solution**: Proper instantiation of UURProperties model
  - **Files**: `src/pywats/domains/report/report_models/uur/uur_report.py`
```

```markdown
### Improved
- **Type Stub Accuracy**: Reduced mypy errors from 740 to 16 (98% improvement)
  - **Service Stubs**: Added proper typing imports to all 9 domain service .pyi files
  - **API Stubs**: Added missing `_run_sync` function to main pywats.pyi
  - **Tests**: All domain tests passing (416 tests, 97% pass rate)
```

### 4. Check for Duplicates

Before adding:
- Read current `[Unreleased]` section
- Check if similar entry already exists
- If duplicate, update existing entry instead of adding new
- If related but different, consider if they should be combined

### 5. Insert Entry

**Location:** Under `[Unreleased]` heading, in the appropriate category section

**Ordering:**
- Categories in standard order (Added, Changed, Deprecated, Removed, Fixed, Security, Improved)
- Entries within category: newest first (top of section)

**If category doesn't exist:** Create it in the correct order

### 6. Present Changes

Show:
- Proposed entry (formatted)
- Category chosen
- Location in CHANGELOG
- Any duplicates/conflicts found

### 7. Verify Format

Check:
- ✅ Uses proper Markdown (-, **, indentation)
- ✅ Feature name is bolded
- ✅ Sub-bullets use `**{Name}**:` format
- ✅ Descriptions are concise but informative
- ✅ No typos or grammar issues
- ✅ File paths use backticks if included

## Output Format
1. Show the proposed entry
2. Explain category choice
3. Show where it will be inserted (line number/context)
4. Make the update
5. Confirm: "✅ CHANGELOG.md updated under [{Category}]"

## Edge Cases

**Multiple related changes:**
```markdown
### Added
- **Client Examples**: Comprehensive example suite for client operations
  - **Attachment I/O**: File upload/download with progress tracking (`examples/client/attachment_io.py`, 250 lines)
  - **Error Handling**: Retry strategies and circuit breaker patterns (`examples/client/error_handling.py`, 400 lines)
  - **Configuration**: Environment-based configuration examples (`examples/client/configuration.py`, 400 lines)
  - **Batch Operations**: Parallel processing and bulk operations (`examples/client/batch_operations.py`, 347 lines)
  - **Documentation**: Navigation guide with use case index (`examples/client/README.md`, 243 lines)
```

**Breaking changes (Added vs Changed):**
- If adding NEW feature → `Added`
- If changing EXISTING API → `Changed` (note migration in description)

## Reference
- Format standard: `.github/copilot-instructions.md` → "CHANGELOG Standards"
- Examples: Read existing entries in `CHANGELOG.md`
