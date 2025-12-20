# pyWATS Release Checklist

> Checklist for transitioning from beta to stable release (v1.0.0)

## Automated Release Process

Use the release script for version bumping and release branch creation:

```powershell
# Preview what will happen (dry run)
.\scripts\release.ps1 -BumpType patch -DryRun

# Patch release (0.1.0 -> 0.1.1)
.\scripts\release.ps1 -BumpType patch

# Minor release (0.1.0 -> 0.2.0)
.\scripts\release.ps1 -BumpType minor

# Major release (0.1.0 -> 1.0.0)
.\scripts\release.ps1 -BumpType major

# Release only agent package
.\scripts\release.ps1 -BumpType patch -Package agent
```

**What the script does:**
1. ✅ Validates you're on `main` with clean working tree
2. ✅ Creates a `release/vX.Y.Z` branch (preserved for rollback)
3. ✅ Bumps version in pyproject.toml files
4. ✅ Tags the release (`vX.Y.Z`)
5. ✅ Pushes branch and tag to origin
6. ✅ Updates main branch with version bump

**Rollback:**
```powershell
# See all release branches
git branch -r | Select-String "release/"

# Checkout a previous release
git checkout release/v0.1.0
```

---

## Pre-Release Tasks

### 🔴 Breaking Changes to Make

- [ ] **Remove `app` → `analytics` backward compatibility shim**
  - Delete `src/pywats/domains/app/` folder entirely
  - Remove `app` alias from `src/pywats/domains/__init__.py`
  - Remove `app` property from `src/pywats/pywats.py`
  - Update any remaining documentation references
  - Files affected:
    - `src/pywats/domains/app/__init__.py` (delete)
    - `src/pywats/domains/__init__.py` (remove `from . import app`)
    - `src/pywats/pywats.py` (remove `def app()` property)
    - `src/pywats/domains/analytics/__init__.py` (remove `AppService`, `AppRepository` aliases)

- [ ] **Remove deprecated aliases in analytics module**
  - Remove `AppService = AnalyticsService` alias
  - Remove `AppRepository = AnalyticsRepository` alias

### 🟡 Documentation Updates

- [ ] Update README.md with stable API examples
- [ ] Review and update all DOMAIN_STATUS/*.md files
- [ ] Ensure all public methods have docstrings with examples
- [ ] Generate API reference documentation
- [ ] Update CHANGELOG.md with all changes since last release
- [ ] **Complete and review examples in `examples/` directory**
  - Review and correct domain-specific details (UUT vs UUR, etc.)
  - Ensure examples follow pyWATS architecture (fluent API pattern)
  - Test examples against actual WATS server

### 🟢 Quality Assurance

- [ ] All tests passing (unit, acceptance, integration)
- [ ] No `**kwargs` in public service methods (LLM-friendly)
- [ ] All models use Pydantic (no dataclasses)
- [ ] Consistent error handling across all domains
- [ ] Type hints on all public methods

### 🔵 Package & Distribution

- [ ] Update version in `pyproject.toml` to `1.0.0`
- [ ] Update `__version__` in `src/pywats/__init__.py`
- [ ] Verify `__wats_server_version__` is current
- [ ] Test PyPI installation: `pip install pywats`
- [ ] Verify all dependencies are correctly specified

### ⚪ Final Verification

- [ ] Fresh virtual environment install test
- [ ] Run full test suite against production WATS server
- [ ] Verify backward compatibility notes in CHANGELOG
- [ ] Tag release in git: `git tag -a v1.0.0 -m "Release 1.0.0"`

---

## Post-Release Tasks

- [ ] Publish to PyPI
- [ ] Create GitHub release with release notes
- [ ] Update any external documentation
- [ ] Announce release (if applicable)

---

## Notes

### Module Naming: analytics vs App

The `analytics` module maps to the WATS backend `/api/App/*` endpoints.

**Why the different names?**
1. "App" is the legacy backend controller name in WATS
2. "analytics" clearly describes the domain's purpose (yield stats, KPIs, failure analysis)
3. LLMs/Agents searching for "statistics" or "yield" won't find "app"

This is purely a naming choice for better developer experience - all API calls go to `/api/App/*`.

### Usage

```python
from pywats.domains.analytics import AnalyticsService, YieldData

# All calls go to /api/App/* endpoints
yield_data = api.analytics.get_dynamic_yield(filter)
```
