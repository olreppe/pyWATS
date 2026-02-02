# Cross-Platform Testing - TODO

**Legend:** ✅ Done | 🚧 In Progress | ✗ Not Started | ⏸️ Blocked | 🔄 Needs Review

---

## Phase 1: Local Testing Infrastructure

### tox Configuration
- [ ] ✗ Create tox.ini with py310-py313 envlist
- [ ] ✗ Add pytest + pytest-cov deps
- [ ] ✗ Configure coverage reporting
- [ ] ✗ Test locally: `tox -e py310`

### pathlib Enforcement
- [ ] ✗ Create pre-commit pathlib check script
- [ ] ✗ Grep search for `os.path` usage in codebase
- [ ] ✗ Refactor flagged code to use `pathlib.Path`
- [ ] ✗ Add test: verify no `os.path` imports in src/

### WSL2 Validation
- [ ] ✗ Install Ubuntu 22.04 in WSL2
- [ ] ✗ Clone repo in WSL2 filesystem
- [ ] ✗ Run pytest in WSL2 environment
- [ ] ✗ Document path case-sensitivity issues found

### Docker Testing
- [ ] ✗ Create Dockerfile.test (Ubuntu + Python 3.13)
- [ ] ✗ Build image: `docker build -f Dockerfile.test`
- [ ] ✗ Run tests: `docker run pywats-test pytest`
- [ ] ✗ Validate clean install in container

---

## Phase 2: GitHub Actions CI Matrix

### Workflow Setup
- [ ] ✗ Create `.github/workflows/test.yml`
- [ ] ✗ Configure matrix: 3 OS × 4 Python versions
- [ ] ✗ Add checkout + setup-python steps
- [ ] ✗ Configure pip caching with actions/cache

### API-Only Job
- [ ] ✗ Add job: install base package
- [ ] ✗ Run: `pytest tests/domains/ tests/integration/`
- [ ] ✗ Full matrix (12 jobs)
- [ ] ✗ Verify cache hit rate >80%

### Client-Headless Job
- [ ] ✗ Add job: install [client-headless] extras
- [ ] ✗ Smoke test: `pywats-client --help`
- [ ] ✗ Run: `pytest tests/client/ -k "not gui"`
- [ ] ✗ Reduced matrix (4 jobs)

### Optimization
- [ ] ✗ Test workflow locally with `act`
- [ ] ✗ Verify build time <10 min
- [ ] ✗ Add workflow badge to README.md
- [ ] ✗ Update CONTRIBUTING.md with CI docs

---

## Phase 3: GUI Headless Testing

### pytest-qt Setup
- [ ] ✗ Add pytest-qt to [client] extras
- [ ] ✗ Add pytest-timeout dependency
- [ ] ✗ Verify qtbot fixture works locally

### Smoke Tests
- [ ] ✗ Create `tests/client/gui/test_smoke.py`
- [ ] ✗ Test: QApplication + MainWindow creation
- [ ] ✗ Test: Window close without crash
- [ ] ✗ Test: All major dialogs/windows

### Platform Configuration
- [ ] ✗ Ubuntu: Set QT_QPA_PLATFORM=offscreen
- [ ] ✗ Windows: Use default Qt platform
- [ ] ✗ macOS: Use default Qt platform
- [ ] ✗ Add pytest-timeout: 30s per test

### CI Integration
- [ ] ✗ Add gui job to workflow
- [ ] ✗ Matrix: 3 OS × 2 Python (3.10, 3.13)
- [ ] ✗ Run: `pytest tests/client/gui/ --timeout=30`
- [ ] ✗ Verify no hanging tests

### Signal/Slot Testing
- [ ] ✗ Test: Button click triggers slot
- [ ] ✗ Test: Async task completion signal
- [ ] ✗ Test: qasync event loop integration
- [ ] ✗ Validate across all platforms

---

## Phase 4: Wheel Building & Packaging

### cibuildwheel Configuration
- [ ] ✗ Create `.github/workflows/build-wheels.yml`
- [ ] ✗ Configure build matrix: cp310-cp313
- [ ] ✗ Platforms: windows, macos (x86_64 + arm64), manylinux
- [ ] ✗ Test command: import smoke test

### Binary Dependencies
- [ ] ✗ Verify PySide6 bundling strategy
- [ ] ✗ Test pywin32 Windows-only marker
- [ ] ✗ Check watchdog builds on all platforms
- [ ] ✗ Test wheel in clean venv

### Local Validation
- [ ] ✗ Build: `python -m build`
- [ ] ✗ Install: `pip install dist/*.whl`
- [ ] ✗ Run: full test suite from wheel
- [ ] ✗ Verify extras install correctly

### CI Artifacts
- [ ] ✗ Upload wheels as GitHub Actions artifacts
- [ ] ✗ Set retention: 90 days
- [ ] ✗ Test download + install from artifact
- [ ] ✗ Add artifact URL to PR comments

### Documentation
- [ ] ✗ Update `docs/release/RELEASE_PROCESS.md`
- [ ] ✗ Document wheel validation steps
- [ ] ✗ Create PyPI upload checklist
- [ ] ✗ Document version bump procedure

---

## Phase 5: Documentation & Finalization

### Contributor Guide
- [ ] ✗ Add "Testing Across Platforms" section
- [ ] ✗ Document tox usage
- [ ] ✗ Document WSL2 + Docker validation
- [ ] ✗ Link to CI workflows

### Troubleshooting
- [ ] ✗ Create `docs/CROSS_PLATFORM_TROUBLESHOOTING.md`
- [ ] ✗ Document common CI failures
- [ ] ✗ Document Qt platform plugin issues
- [ ] ✗ Document wheel build failures
- [ ] ✗ Document cache invalidation

### Final Updates
- [ ] ✗ Update CHANGELOG under [Unreleased]
- [ ] ✗ Add workflow status badge to README
- [ ] ✗ Review all documentation for completeness
- [ ] ✗ Create COMPLETION_SUMMARY.md

---

## Blockers

_None currently_

---

## Notes

- Project created from CROSS_PLATFORM_TESTING.md analysis
- Targeting Q1 2026 completion (4 weeks)
- Waiting for approval to move from planned → active

---

**Last Updated:** 2026-02-02
