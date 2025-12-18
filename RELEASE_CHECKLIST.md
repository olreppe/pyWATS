# pyWATS Release Checklist

> Checklist for transitioning from beta to stable release (v1.0.0)

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

### Why remove `app` alias?

The `app` domain was renamed to `analytics` because:
1. "app" is ambiguous (could mean application, root module, etc.)
2. "analytics" clearly describes the domain's purpose (yield stats, KPIs, failure analysis)
3. LLMs/Agents searching for "statistics" or "yield" won't find "app"

The backward compatibility shim (`api.app` → `api.analytics`) exists only for beta users.
It should be removed in v1.0.0 to keep the API surface clean.

### Migration Guide for Beta Users

```python
# Before (deprecated)
from pywats.domains.app import AppService
yield_data = api.app.get_dynamic_yield(filter)

# After (v1.0.0+)
from pywats.domains.analytics import AnalyticsService
yield_data = api.analytics.get_dynamic_yield(filter)
```
