# Future Improvements Implementation Plan

**Created:** 2026-01-29  
**Status:** Planning / Review  
**Target Release:** 0.3.0 or later

---

## Overview

This document outlines implementation plans for three long-term improvements identified during the code review:

| # | Improvement | Complexity | Effort | Priority |
|---|-------------|------------|--------|----------|
| 1 | ~~Integrate pywats_events with core~~ | ~~High~~ | ~~2-3 days~~ | ❌ Not Recommended |
| 2 | Add coverage reporting to CI | Low | 2-4 hours | High |
| 3 | Create quick reference cheat sheet | Low | 1-2 hours | Medium |

---

## 1. ~~Integrate pywats_events with Core~~ → LOCAL EVENT BUS ONLY

### ⚠️ Architectural Review Conclusion

After analysis, the **webhook/WebSocket transports are NOT recommended** for a client library:

| Component | Verdict | Reason |
|-----------|---------|--------|
| Local event bus | ✅ Keep | Appropriate for internal client coordination |
| Webhook receiver | ❌ Remove | Inverts client-server relationship; clients shouldn't run HTTP servers |
| WebSocket client | ❌ Defer | WATS server doesn't emit events; building for non-existent feature |

### Why Webhooks Don't Belong in a Client

1. **Architecture inversion** - Client must run HTTP server to receive calls
2. **Network topology** - Factory floor PCs behind NAT/firewall can't receive inbound connections
3. **Security concern** - Opening ports on client machines is inappropriate
4. **Missing server support** - WATS backend doesn't emit webhooks anyway

### What's Actually Useful

The **local event bus** in `pywats_events` is appropriate for:
- Decoupling `pywats_client` internal components
- Example: Report submitted → UI updates, logging triggers, queue status changes
- Observer pattern with minimal overhead (~100 lines)

### Revised Recommendation

| Action | Scope |
|--------|-------|
| **Keep** | Local event bus for `pywats_client` internal use |
| **Move to ideas/** | Webhook/WebSocket transport code |
| **Delete or archive** | Transport abstractions that imply server→client push |

### If Server Push Is Ever Needed

The correct approach would be:
1. WATS **server team** implements WebSocket or Server-Sent Events
2. `pywats` adds a simple **client** to connect and receive
3. Dependency flows correctly: client depends on server capability

### Complexity Assessment: **NOT APPLICABLE**

This item is **deprioritized** - no implementation planned.
The existing local event bus in `pywats_client` is sufficient for current needs.

---

## 2. Add Coverage Reporting to CI

### Current State

- Tests exist but no coverage measurement
- No minimum coverage threshold enforced
- CI runs tests but doesn't report coverage

### Goal

- Measure test coverage on every PR/push
- Enforce minimum coverage threshold (e.g., 80%)
- Display coverage badge in README
- Coverage reports viewable in CI artifacts

### Implementation Plan

#### Step 1: Add pytest-cov dependency (10 min)
```toml
# pyproject.toml [project.optional-dependencies]
dev = [
    ...
    "pytest-cov>=4.0.0",
]
```

#### Step 2: Configure coverage (15 min)
```toml
# pyproject.toml
[tool.coverage.run]
source = ["src/pywats", "src/pywats_client", "src/pywats_events"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/examples/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@abstractmethod",
]
fail_under = 80
show_missing = true
```

#### Step 3: Update CI workflow (30 min)

```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-report=xml --cov-report=html --cov-fail-under=80
    
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: false
```

#### Step 4: Add coverage badge (10 min)

```markdown
# README.md
[![codecov](https://codecov.io/gh/olreppe/pyWATS/branch/main/graph/badge.svg)](https://codecov.io/gh/olreppe/pyWATS)
```

### Files to Modify

| File | Change |
|------|--------|
| `pyproject.toml` | Add pytest-cov, coverage config |
| `.github/workflows/test.yml` | Add coverage steps |
| `README.md` | Add coverage badge |
| `pytest.ini` | Optional: add default coverage flags |

### Risks

| Risk | Mitigation |
|------|------------|
| Initial coverage may be <80% | Start with lower threshold, increase over time |
| Slow CI with coverage | Use `--cov-report=xml` only in CI |

### Complexity Assessment: **LOW**

- Well-established tooling
- No code changes, just configuration
- Can be done incrementally

### Recommended Starting Threshold

Based on review, estimate current coverage ~60-70%. Suggest:
1. Start with `fail_under = 60` 
2. Increase to 70% after 2 weeks
3. Target 80% by 0.3.0 release

---

## 3. Create Quick Reference Cheat Sheet

### Current State

- Comprehensive documentation exists but is verbose
- No single-page quick reference
- Users need to read multiple files for common patterns

### Goal

Create a **1-page PDF/Markdown** quick reference covering:
- Installation & setup
- Basic API usage patterns
- Common async patterns
- Error handling
- Configuration options
- Links to full docs

### Implementation Plan

#### Step 1: Outline content (30 min)

```
CHEAT SHEET SECTIONS:
├── Installation (pip install, optional deps)
├── Quick Start (3 lines to connect)
├── Async Patterns (AsyncWATS, context manager)
├── Sync Patterns (run_sync wrapper)
├── Common Operations
│   ├── Reports (create, query, filter)
│   ├── Assets (CRUD)
│   ├── Products (lookup)
│   └── Analytics (yield queries)
├── Error Handling (try/except patterns)
├── Configuration (env vars, config file)
└── Getting Help (links, support)
```

#### Step 2: Write content (1 hour)

Create `docs/CHEAT_SHEET.md` with:
- Code snippets for every pattern
- Side-by-side async/sync examples
- OData filter builder quick examples
- Common gotchas section

#### Step 3: PDF version (30 min, optional)

- Use `mdpdf` or similar to generate PDF
- Add to release artifacts
- Consider A4 single-page layout

### Example Content Preview

```markdown
# pyWATS Quick Reference

## Installation
```bash
pip install pywats[client]  # Full install
pip install pywats          # API only
```

## Connect
```python
from pywats import AsyncWATS

async with AsyncWATS(url, token=token) as api:
    reports = await api.report.get_reports()
```

## Common Operations

| Task | Code |
|------|------|
| Get reports | `await api.report.get_reports()` |
| Filter reports | `await api.report.query(filter="status eq 'Passed'")` |
| Create asset | `await api.asset.create(serial="SN123", part_number="PN456")` |
| Safe OData filter | `ODataFilterBuilder().field("status").eq("Passed").build()` |

## Error Handling
```python
from pywats.exceptions import WATSAPIError, AuthenticationError

try:
    result = await api.report.get_report(id)
except AuthenticationError:
    # Token expired or invalid
except WATSAPIError as e:
    print(f"API error: {e.status_code} - {e.message}")
```
```

### Files to Create

| File | Purpose |
|------|---------|
| `docs/CHEAT_SHEET.md` | Main quick reference |
| `docs/CHEAT_SHEET.pdf` | Printable version (optional) |

### Complexity Assessment: **LOW**

- No code changes
- Documentation only
- Can leverage existing examples

---

## Implementation Priority Recommendation

Based on effort vs. value:

### Recommended Order

1. **Coverage reporting** (2-4 hours) - Quick win, immediate CI benefit
2. **Cheat sheet** (1-2 hours) - Quick win, improves onboarding
3. ~~**Event integration**~~ - **Not recommended** (architectural mismatch for client library)

### Timeline Estimate

| Item | Start | Duration | Milestone |
|------|-------|----------|-----------|
| Coverage reporting | Now | 0.5 day | 0.2.0b3 |
| Cheat sheet | After coverage | 0.5 day | 0.2.0b3 |
| ~~Event integration~~ | N/A | N/A | ❌ Deprioritized |

---

## Questions for Review

Before proceeding, please confirm:

1. **Coverage threshold:** Start at 60% or aim higher?
2. **Codecov vs GitHub native:** Preference for coverage service?
3. **Cheat sheet format:** Markdown only, or also PDF?

---

## Approval

- [x] Plan reviewed
- [x] Event integration deprioritized (architectural mismatch)
- [ ] Ready to proceed with Coverage (#2)
- [ ] Ready to proceed with Cheat Sheet (#3)
