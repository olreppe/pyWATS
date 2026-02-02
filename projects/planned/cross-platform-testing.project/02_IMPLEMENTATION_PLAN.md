# Cross-Platform Testing - Implementation Plan

**Created:** 2026-02-02  
**Phases:** 4  
**Total Duration:** 4 weeks

---

## Phase 1: Local Testing Infrastructure (Week 1)

### Objectives
- Enable multi-Python testing on Windows dev machine
- Enforce pathlib usage
- Set up WSL2 + Docker validation

### Tasks

1. **Create tox.ini** (2 hours)
   - Envlist: py310, py311, py312, py313
   - Deps: pytest, pytest-cov, httpx
   - Commands: pytest with coverage
   - Test locally: `tox -e py310`

2. **Add pathlib enforcement** (3 hours)
   - Create pre-commit hook script
   - Grep search for `os.path` usage
   - Refactor flagged code to use `pathlib.Path`
   - Add test: verify no `os.path` in source

3. **WSL2 setup validation** (2 hours)
   - Install Ubuntu 22.04 in WSL2
   - Clone repo in WSL2 filesystem
   - Run `pytest` in WSL2 environment
   - Document differences found

4. **Docker smoke test** (3 hours)
   - Create Dockerfile.test (Ubuntu base + Python 3.13)
   - Build: `docker build -f Dockerfile.test -t pywats-test .`
   - Run: `docker run pywats-test pytest`
   - Validate package install in clean environment

**Deliverables:**
- `tox.ini` configuration
- `scripts/pre-commit-pathlib-check.ps1`
- WSL2 testing documentation
- `Dockerfile.test`

**Success Criteria:**
- tox runs successfully on Windows
- No `os.path` usage in source code
- pytest passes in WSL2 and Docker

---

## Phase 2: GitHub Actions CI Matrix (Week 2)

### Objectives
- Set up multi-OS, multi-Python CI workflow
- Separate jobs for different install extras
- Fail fast on errors

### Tasks

1. **Create base workflow file** (3 hours)
   - Path: `.github/workflows/test.yml`
   - Matrix: os=[ubuntu-latest, windows-latest, macos-latest]
   - Matrix: python-version=['3.10', '3.11', '3.12', '3.13']
   - Steps: checkout, setup-python, install deps, pytest

2. **API-only test job** (2 hours)
   - Install: `pip install .`
   - Run: `pytest tests/domains/ tests/integration/`
   - Cache pip dependencies
   - Full matrix (3 OS × 4 Python = 12 jobs)

3. **Client-headless job** (3 hours)
   - Install: `pip install .[client-headless]`
   - Smoke: `pywats-client --help`
   - Run: `pytest tests/client/ -k "not gui"`
   - Reduced matrix: ubuntu + windows, Python 3.10 + 3.13 (4 jobs)

4. **Optimize caching** (2 hours)
   - Use `actions/cache@v3` for pip
   - Cache key: hash of requirements + pyproject.toml
   - Verify cache hit rate in workflow logs

5. **Test workflow locally** (2 hours)
   - Use `act` tool to run GitHub Actions locally
   - Verify job execution order
   - Check failure scenarios

**Deliverables:**
- `.github/workflows/test.yml`
- Workflow badge in README.md
- CI documentation in CONTRIBUTING.md

**Success Criteria:**
- All jobs pass on first run
- Build time <10 min for full matrix
- Cache hit rate >80%

---

## Phase 3: GUI Headless Testing (Week 3)

### Objectives
- Enable Qt GUI testing without display
- Validate across platforms
- Prevent hanging tests

### Tasks

1. **Install pytest-qt** (1 hour)
   - Add to `[client]` extras in pyproject.toml
   - Add to dev dependencies
   - Verify qtbot fixture availability

2. **Create GUI smoke test template** (4 hours)
   - File: `tests/client/gui/test_smoke.py`
   - Test: Create QApplication, MainWindow, close
   - Use qtbot.waitSignal with timeout
   - Test all major windows/dialogs

3. **Configure offscreen platform** (3 hours)
   - Ubuntu: Set `QT_QPA_PLATFORM=offscreen` in workflow
   - Windows: Use default platform
   - macOS: Use default platform
   - Add pytest-timeout: 30s per test

4. **Add GUI job to workflow** (2 hours)
   - Matrix: ubuntu + windows + macos, Python 3.10 + 3.13
   - Install: `pip install .[client] pytest-qt pytest-timeout`
   - Run: `pytest tests/client/gui/ --timeout=30`
   - Platform env vars per OS

5. **Test signal/slot behavior** (2 hours)
   - Test: Button click → slot triggered
   - Test: Async task completion signal
   - Test: qasync event loop integration
   - Validate across platforms

**Deliverables:**
- `tests/client/gui/test_smoke.py`
- Updated `.github/workflows/test.yml` with gui job
- GUI testing documentation

**Success Criteria:**
- GUI tests pass on all 3 platforms
- No hanging tests (timeout enforcement works)
- qtbot fixtures available in all tests

---

## Phase 4: Wheel Building & Packaging (Week 4)

### Objectives
- Build cross-platform wheels
- Validate installation from wheels
- Prepare for PyPI publishing

### Tasks

1. **Configure cibuildwheel** (3 hours)
   - Add `.github/workflows/build-wheels.yml`
   - Matrix: cp310, cp311, cp312, cp313
   - Platforms: windows, macos (x86_64 + arm64), manylinux
   - Test command: `python -c "import pywats; import pywats_client"`

2. **Handle binary dependencies** (4 hours)
   - Qt bundling strategy (rely on pip install PySide6)
   - Verify pywin32 only on Windows
   - Check watchdog builds on all platforms
   - Test wheel in clean venv

3. **Local wheel testing** (2 hours)
   - Build: `python -m build`
   - Install: `pip install dist/*.whl`
   - Run: smoke tests
   - Verify extras install correctly

4. **Add wheel artifacts to workflow** (2 hours)
   - Upload wheels as GitHub Actions artifacts
   - Retention: 90 days
   - Download URL in PR comments
   - Test installation from artifact

5. **Document release process** (1 hour)
   - Update `docs/release/RELEASE_PROCESS.md`
   - Include wheel validation steps
   - PyPI upload checklist
   - Version bump procedure

**Deliverables:**
- `.github/workflows/build-wheels.yml`
- Wheel validation documentation
- Updated release process docs

**Success Criteria:**
- Wheels build successfully for all platforms
- `pip install <wheel>` works on fresh system
- Import smoke tests pass from wheel

---

## Phase 5: Documentation & Finalization (Ongoing)

### Objectives
- Document cross-platform testing for contributors
- Create troubleshooting guide
- Update CONTRIBUTING.md

### Tasks

1. **Contributor guide** (2 hours)
   - Add section: "Testing Across Platforms"
   - Document tox usage
   - Document WSL2 + Docker validation
   - Link to CI workflows

2. **Troubleshooting guide** (2 hours)
   - Common CI failures and fixes
   - Qt platform plugin issues
   - Wheel build failures
   - Cache invalidation

3. **Update CHANGELOG** (1 hour)
   - Add under `[Unreleased]` → `Added`
   - Entry: "Cross-platform CI testing (Windows, Linux, macOS)"
   - Entry: "Automated wheel building with cibuildwheel"
   - Entry: "Qt GUI headless smoke tests"

4. **README badge** (30 min)
   - Add workflow status badge
   - Link to Actions page
   - Display build status prominently

**Deliverables:**
- Updated CONTRIBUTING.md
- docs/CROSS_PLATFORM_TROUBLESHOOTING.md
- CHANGELOG entry
- README badge

**Success Criteria:**
- Contributors can run tests locally on Windows
- CI failures have documented resolutions
- README shows build status

---

## Risk Mitigation Strategies

### Risk: macOS-specific GUI bugs
- **Mitigation:** Focus on API + headless tests; document known macOS issues
- **Fallback:** Tag issues with "macos-only" for community help

### Risk: CI build time exceeds 10 min
- **Mitigation:** Reduce matrix size (test 3.10 + 3.13 only for GUI)
- **Fallback:** Split into separate workflows (api-fast, gui-slow)

### Risk: Qt offscreen platform not available
- **Mitigation:** Fall back to Xvfb on Linux
- **Fallback:** Skip GUI tests on platforms without display support

### Risk: cibuildwheel fails for Qt
- **Mitigation:** Exclude Qt from wheel deps (users install separately)
- **Fallback:** Publish sdist only, document wheel limitations

---

## Dependencies & Prerequisites

**Before Starting:**
- WSL2 installed on dev machine
- Docker Desktop installed
- GitHub Actions enabled on repository
- Python 3.10-3.13 installed via pyenv/asdf

**External Services:**
- GitHub Actions (free tier)
- PyPI account (for future publishing)

---

## Testing Strategy

### Unit Testing
- All phases: Add tests for new scripts/configs
- tox.ini: Test locally before committing
- Workflow files: Use `act` to test locally

### Integration Testing
- Phase 2: Trigger workflow on PR to test branch
- Phase 3: Verify GUI tests on all platforms
- Phase 4: Install wheel and run full test suite

### Acceptance Testing
- Install pyWATS from wheel on fresh Windows/Linux/macOS VM
- Run examples from docs
- Verify CLI commands work

---

## Rollback Plan

If CI becomes unstable:
1. Revert workflow changes
2. Fall back to manual testing
3. Document issues for future retry

If wheel building fails:
1. Continue publishing sdist only
2. Document wheel limitations
3. Investigate offline with cibuildwheel docs

---

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| 1. Local Testing | 1 week | None |
| 2. CI Matrix | 1 week | Phase 1 complete |
| 3. GUI Testing | 1 week | Phase 2 complete |
| 4. Wheel Building | 1 week | Phase 3 complete |
| 5. Documentation | Ongoing | All phases |

**Total:** 4 weeks + ongoing documentation

---

## Next Steps

1. Review this plan with team
2. Create Phase 1 tasks in TODO.md
3. Schedule kickoff meeting
4. Begin tox.ini implementation

**Status:** Implementation plan ready for approval
