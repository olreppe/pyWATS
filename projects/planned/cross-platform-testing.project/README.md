# Cross-Platform Testing Project

**Status:** 📋 Planned  
**Completion:** 0%  
**Created:** 2026-02-02  
**Target:** Q1 2026

---

## Overview

Establish comprehensive cross-platform testing infrastructure for pyWATS to ensure reliability across Windows, Linux, and macOS without requiring local VMs or hardware.

**Key Focus:**
- API layer testing (80-90% of cross-platform risk)
- WSL2 + Docker for Linux simulation
- Qt/PySide6 GUI headless testing
- GitHub Actions CI matrix (ubuntu/windows/macos)
- Wheel building with cibuildwheel

---

## Objectives

1. **API Testing** - Unit/integration tests with httpx mocking, multi-Python tox matrix
2. **Linux Simulation** - WSL2 + Docker for path/permissions/packaging validation
3. **GUI Headless Tests** - Qt offscreen smoke tests for widget/signal behavior
4. **CI Matrix** - GitHub Actions workflows for 3 OS × 4 Python versions
5. **Packaging Confidence** - cibuildwheel for cross-platform wheel validation

---

## Success Criteria

- [ ] pytest suite passes on Windows/Linux/macOS (Python 3.10-3.13)
- [ ] GUI smoke tests run headless on all platforms
- [ ] cibuildwheel produces installable wheels for all OS/architectures
- [ ] CI matrix runs on every PR with <10 min build time
- [ ] pathlib usage enforced (no OS-specific path assumptions)

---

## Stakeholders

**Owner:** Development Team  
**Users:** All pyWATS library users (cross-platform compatibility)

---

## Timeline

- **Phase 1:** Local testing improvements (tox, pathlib enforcement) - 1 week
- **Phase 2:** GitHub Actions CI matrix setup - 1 week
- **Phase 3:** GUI headless testing - 1 week
- **Phase 4:** cibuildwheel integration - 1 week

**Estimated Completion:** 4 weeks from start

---

## Dependencies

- GitHub Actions runner availability (ubuntu-latest, windows-latest, macos-latest)
- Qt platform plugins (QPA offscreen support)
- cibuildwheel package
- Docker for local Linux testing

---

## Risks

- **Medium:** macOS-specific GUI issues (menu bar, retina scaling) may require real hardware
- **Low:** Qt platform plugin availability issues on Linux CI
- **Low:** cibuildwheel configuration complexity for Qt/binary deps
- **Medium:** CI build time may exceed 10 min on slow matrix jobs

---

## Related Projects

- test-coverage-enhancement (active) - overlaps with test infrastructure
- client-components-polish (active) - GUI smoke tests will validate client stability

---

## References

- [Cross-Platform Testing Analysis](CROSS_PLATFORM_TESTING.md)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [cibuildwheel](https://cibuildwheel.readthedocs.io/)
- [Qt QPA](https://doc.qt.io/qt-6/qpa.html)
