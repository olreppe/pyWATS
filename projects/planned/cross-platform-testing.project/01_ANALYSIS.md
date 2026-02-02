# Cross-Platform Testing - Analysis

**Date:** 2026-02-02  
**Author:** Development Team

---

## Problem Statement

pyWATS is an open-source library with users on Windows, Linux, and macOS, but development primarily happens on Windows. Without cross-platform testing, we risk shipping "crap that's painful to install" or bugs that only surface on non-Windows platforms.

**Current Pain Points:**
- No automated testing on Linux/macOS before release
- Path/filesystem assumptions may break on case-sensitive filesystems
- Qt GUI behavior untested across platforms
- Install/packaging issues discovered by users, not CI
- No confidence that wheels work on all platforms

---

## Requirements

### Functional Requirements

1. **API Testing**
   - Unit + integration tests must pass on Windows, Linux, macOS
   - Tests must run against Python 3.10, 3.11, 3.12, 3.13
   - httpx mocking for endpoint-independent tests
   - pathlib enforcement (no os.path assumptions)

2. **GUI Testing**
   - Smoke tests: QApplication creation, main window init, close
   - Headless execution via Qt offscreen platform
   - Signal/slot behavior validation
   - qasync integration tests

3. **CI/CD**
   - GitHub Actions matrix: 3 OS × 4 Python versions
   - Separate jobs for API-only, client-headless, client (GUI)
   - Build time target: <10 minutes per matrix
   - Fail fast on first error

4. **Packaging**
   - cibuildwheel integration for cross-platform wheels
   - Wheel smoke tests: pip install + import validation
   - sdist build verification

### Non-Functional Requirements

- **Performance:** CI builds should complete in <10 min
- **Maintainability:** Single workflow file, minimal duplication
- **Cost:** Use free GitHub Actions tier (2000 min/month for public repos)
- **Developer Experience:** Local tox testing before pushing to CI

---

## Constraints

1. **Hardware:** No local Linux/macOS machines available
2. **Time:** Must leverage existing tools (tox, pytest, GitHub Actions)
3. **Scope:** Focus on "installability + smoke tests," not pixel-perfect GUI testing
4. **Budget:** Free tier only (no paid CI runners)

---

## Technical Approach

### 1. Local Testing (Windows Developer)

**tox for Multi-Python:**
```toml
[tool.tox]
envlist = py310,py311,py312,py313
deps = pytest, httpx, pytest-cov
commands = pytest tests/
```

**WSL2 + Docker:**
- WSL2 for path case-sensitivity + permissions testing
- Docker for headless Linux client testing
- Validate packaging in clean Ubuntu container

**Enforcements:**
- Pre-commit hook: Check for `os.path` usage (must use `pathlib`)
- mypy strict mode: Catch type issues early
- flake8 line length: 120 chars

### 2. GitHub Actions CI Matrix

**API-Only Job** (fast baseline):
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.10', '3.11', '3.12', '3.13']
steps:
  - pip install .
  - pytest tests/domains/ tests/integration/
```

**Client-Headless Job** (CLI + watcher):
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    python-version: ['3.10', '3.13']
steps:
  - pip install .[client-headless]
  - pywats-client --help
  - pytest tests/client/ -k "not gui"
```

**GUI Smoke Job** (Qt offscreen):
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.10', '3.13']
steps:
  - pip install .[client]
  - export QT_QPA_PLATFORM=offscreen  # Linux
  - pytest tests/client/gui/ --timeout=30
```

### 3. cibuildwheel Integration

**Build Matrix:**
- Windows: x86_64
- macOS: x86_64, arm64 (Apple Silicon)
- Linux: x86_64, aarch64 (via QEMU)

**Validation:**
```yaml
- name: Build wheels
  uses: pypa/cibuildwheel@v2.16
  env:
    CIBW_BUILD: cp310-* cp311-* cp312-* cp313-*
    CIBW_TEST_COMMAND: python -c "import pywats; import pywats_client"
```

### 4. GUI Headless Testing Strategy

**What to Test:**
- Widget creation without crashes
- Signals/slots wiring
- qasync event loop integration
- Basic navigation flows

**What NOT to Test:**
- Pixel-perfect rendering
- Native menu bar behavior (macOS-specific)
- System tray across desktop environments
- Wayland vs X11 differences

**Smoke Test Template:**
```python
def test_gui_smoke(qtbot):
    """Verify main window can be created and closed."""
    app = QApplication.instance() or QApplication([])
    
    with qtbot.waitSignal(timeout=5000):
        window = MainWindow()
        window.show()
        qtbot.addWidget(window)
    
    window.close()
    assert True  # If we get here, no crash
```

---

## Dependencies

### External Tools
- **tox** - Local multi-Python testing
- **pytest** - Test framework
- **pytest-qt** - Qt test fixtures (qtbot)
- **cibuildwheel** - Cross-platform wheel building
- **Docker** - Linux container testing

### GitHub Actions
- `actions/setup-python@v5` - Python version management
- `pypa/cibuildwheel@v2.16` - Wheel building action
- Ubuntu runner: Xvfb for GUI tests
- Windows runner: Native Qt support
- macOS runner: Native Qt support

### Python Packages
- `httpx` - Already used for API client
- `pytest-timeout` - Prevent hanging GUI tests
- `pytest-xvfb` - Linux virtual display (optional)

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| macOS-specific GUI bugs | Medium | High | Document known issues; rely on user reports |
| Qt plugin availability on Linux CI | Low | Medium | Pin Qt version; use offscreen platform |
| cibuildwheel build time >20 min | Medium | Medium | Limit to Python 3.10 + 3.13 for wheels initially |
| CI cost exceeds free tier | Low | High | Monitor usage; optimize matrix (reduce redundant jobs) |
| Headless tests hang indefinitely | Medium | Medium | Use pytest-timeout; set 30s limits on GUI tests |

---

## Alternatives Considered

1. **VM Testing Locally** ❌
   - Requires VirtualBox/VMware licenses + disk space
   - Slow iteration cycle
   - Not sustainable for continuous testing

2. **Third-Party CI (CircleCI, Travis)** ❌
   - GitHub Actions is free for open source
   - Native integration with repository
   - Better matrix support

3. **Manual Testing Only** ❌
   - Doesn't scale
   - Users find bugs after release
   - No confidence in packaging

4. **Docker-Only CI** ❌
   - Misses Windows + macOS issues
   - GUI testing is harder in containers

---

## Open Questions

1. **Should we test Python 3.9?**
   - Decision: No, pyproject.toml requires >=3.10

2. **How to handle optional dependencies in CI?**
   - Decision: Separate jobs for `[client]`, `[client-headless]`, base install

3. **Should we publish wheels immediately?**
   - Decision: Build in CI for validation, publish manually at first

4. **What's the timeout for GUI tests?**
   - Decision: 30 seconds per test (pytest-timeout)

5. **Linux GUI test display backend?**
   - Decision: QT_QPA_PLATFORM=offscreen (no Xvfb needed)

---

## Success Metrics

- **Coverage:** 90%+ of tests pass on all platforms
- **Build Time:** CI matrix completes in <10 min
- **Install Success:** `pip install` works on fresh Ubuntu/macOS/Windows
- **Issue Rate:** <5 platform-specific bugs per quarter

---

## Next Steps

1. Create tox.ini for local multi-Python testing
2. Draft GitHub Actions workflow (.github/workflows/test.yml)
3. Write GUI smoke test template
4. Configure cibuildwheel
5. Document cross-platform testing in contributor guide

---

**Status:** Analysis complete, ready for implementation planning
