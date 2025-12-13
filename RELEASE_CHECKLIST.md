# Release Checklist Template

Use this checklist for each release. Copy and fill in version number.

---

## Release X.Y.Z Checklist

**Version**: _________  
**Release Date**: _________  
**Release Manager**: _________

---

### Pre-Release Tasks

#### Version Numbers
- [ ] Update version in `packages/pywats/pyproject.toml`
- [ ] Update version in `packages/pywats-client-service/pyproject.toml`
- [ ] Update version in `packages/pywats-client-headless/pyproject.toml`
- [ ] Update version in `packages/pywats-client-gui/pyproject.toml`
- [ ] Update version in `src/pyWATS/__init__.py` (`__version__`)
- [ ] Update version in `src/pywats_client/__init__.py` (if applicable)

**All versions should match**: X.Y.Z

#### Changelogs
- [ ] Update `packages/pywats/CHANGELOG.md`
- [ ] Update `packages/pywats-client-service/CHANGELOG.md`
- [ ] Update `packages/pywats-client-headless/CHANGELOG.md`
- [ ] Update `packages/pywats-client-gui/CHANGELOG.md`
- [ ] Set release date in all CHANGELOGs

#### Documentation
- [ ] Update main README.md with new version
- [ ] Review and update package READMEs
- [ ] Update MIGRATION_GUIDE.md if needed
- [ ] Update PACKAGE_OVERVIEW.md if needed
- [ ] Check all documentation links work
- [ ] Update screenshots if UI changed (GUI package)

#### Code Quality
- [ ] Run all tests: `pytest`
- [ ] Run linters:
  - [ ] `black --check src/`
  - [ ] `isort --check src/`
  - [ ] `flake8 src/`
- [ ] Run type checker: `mypy src/` (if configured)
- [ ] Check for TODOs/FIXMEs in code
- [ ] Review open issues on GitHub

#### Dependencies
- [ ] Audit dependencies for security vulnerabilities
- [ ] Update dependencies if needed
- [ ] Verify minimum version requirements
- [ ] Test with minimum supported Python version (3.8)
- [ ] Test with latest Python version (3.12)

#### Git
- [ ] Ensure all changes are committed
- [ ] Branch is up to date with main
- [ ] No merge conflicts
- [ ] All CI checks passing

---

### Build Phase

#### Clean Build Environment
- [ ] Remove old build artifacts:
  ```bash
  find packages -type d -name "build" -exec rm -rf {} +
  find packages -type d -name "dist" -exec rm -rf {} +
  find packages -type d -name "*.egg-info" -exec rm -rf {} +
  ```

#### Build Packages
- [ ] Run build script: `bash scripts/build_all_packages.sh`
- [ ] Verify all 4 packages built successfully
- [ ] Check package sizes are reasonable
- [ ] Inspect package contents:
  ```bash
  tar -tzf packages/pywats/dist/*.tar.gz | less
  unzip -l packages/pywats/dist/*.whl | less
  ```

#### Verify Build
- [ ] All expected files included
- [ ] No unexpected files (e.g., .pyc, __pycache__)
- [ ] LICENSE included in each package
- [ ] README and CHANGELOG included
- [ ] Check package metadata:
  ```bash
  twine check packages/*/dist/*
  ```

---

### Testing Phase

#### Local Installation Testing
- [ ] Run test script: `bash scripts/test_local_install.sh`
- [ ] Test imports for each package
- [ ] Test CLI commands work
- [ ] Manual smoke tests:
  - [ ] Core API: Connect to WATS server
  - [ ] Headless: Start service, check HTTP API
  - [ ] GUI: Launch and check UI loads

#### Environment Testing
- [ ] Test on Python 3.8
- [ ] Test on Python 3.9
- [ ] Test on Python 3.10
- [ ] Test on Python 3.11
- [ ] Test on Python 3.12
- [ ] Test on Windows
- [ ] Test on macOS
- [ ] Test on Linux

#### Integration Testing
- [ ] Test with real WATS server
- [ ] Test converter functionality
- [ ] Test queue processing
- [ ] Test report submission
- [ ] Test error handling

---

### TestPyPI Phase

#### Upload to TestPyPI
- [ ] Upload: `bash scripts/upload_to_testpypi.sh`
- [ ] Verify upload succeeded for all packages

#### Verify TestPyPI
- [ ] Check package pages:
  - [ ] https://test.pypi.org/project/pywats/
  - [ ] https://test.pypi.org/project/pywats-client-service/
  - [ ] https://test.pypi.org/project/pywats-client-headless/
  - [ ] https://test.pypi.org/project/pywats-client-gui/
- [ ] Check metadata displays correctly
- [ ] Check README renders properly
- [ ] Check download links work

#### Test Installation from TestPyPI
- [ ] Create fresh virtual environment
- [ ] Install core: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats`
- [ ] Install headless: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats-client-headless`
- [ ] Install GUI: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats-client-gui`
- [ ] Test functionality

#### TestPyPI Issues
- [ ] Document any issues found
- [ ] Fix issues and rebuild if necessary
- [ ] Re-upload to TestPyPI if needed

---

### PyPI Release Phase

#### Final Verification
- [ ] All TestPyPI tests passed
- [ ] All issues resolved
- [ ] Confirmed ready to release

#### Upload to PyPI
- [ ] Run release script: `bash scripts/release_to_pypi.sh`
- [ ] Confirm upload when prompted
- [ ] Verify upload succeeded for all packages:
  - [ ] pywats
  - [ ] pywats-client-service
  - [ ] pywats-client-headless
  - [ ] pywats-client-gui

#### Verify PyPI
- [ ] Check package pages:
  - [ ] https://pypi.org/project/pywats/
  - [ ] https://pypi.org/project/pywats-client-service/
  - [ ] https://pypi.org/project/pywats-client-headless/
  - [ ] https://pypi.org/project/pywats-client-gui/
- [ ] Check metadata displays correctly
- [ ] Check README renders properly
- [ ] Check all badges/links work
- [ ] Verify download statistics start appearing

---

### Post-Release Tasks

#### Git Tagging
- [ ] Create git tag:
  ```bash
  git tag -a vX.Y.Z -m "Release version X.Y.Z"
  git push origin vX.Y.Z
  ```

#### GitHub Release
- [ ] Go to https://github.com/olreppe/pyWATS/releases
- [ ] Click "Create a new release"
- [ ] Select tag vX.Y.Z
- [ ] Set release title: "pyWATS vX.Y.Z"
- [ ] Copy release notes from CHANGELOGs
- [ ] Publish release

#### Verification
- [ ] Create clean virtual environment
- [ ] Install from PyPI:
  ```bash
  pip install pywats
  pip install pywats-client-headless
  pip install pywats-client-gui
  ```
- [ ] Test basic functionality
- [ ] Check installed versions match

#### Documentation Updates
- [ ] Update main repository README
- [ ] Update installation instructions
- [ ] Update any external documentation
- [ ] Update wiki (if applicable)

#### Communication
- [ ] Post release announcement (if applicable)
- [ ] Update project website (if applicable)
- [ ] Notify users/customers (if applicable)
- [ ] Post on relevant channels (Slack, Discord, etc.)

---

### Rollback Plan (if needed)

If critical issues are discovered:

- [ ] Document the issue
- [ ] Decide: patch release or yank version?
- [ ] If yanking: `pip install twine && twine yank <package> <version>`
- [ ] If patching: Start new release cycle with X.Y.Z+1
- [ ] Communicate issue to users
- [ ] Fix issue and release patch

---

### Post-Release Review

#### Metrics
- [ ] Monitor download statistics
- [ ] Check for installation issues
- [ ] Monitor issue tracker for problems

#### Documentation
- [ ] Archive this completed checklist
- [ ] Update release process based on lessons learned
- [ ] Document any issues encountered

---

### Notes

```
Add any notes about this release here:
- 
- 
- 
```

---

### Sign-Off

**Release Manager**: _________ **Date**: _________

**QA Verified**: _________ **Date**: _________

**Documentation Updated**: _________ **Date**: _________

---

## Quick Reference Commands

```bash
# Build all packages
bash scripts/build_all_packages.sh

# Test local installation
bash scripts/test_local_install.sh

# Upload to TestPyPI
bash scripts/upload_to_testpypi.sh

# Release to PyPI
bash scripts/release_to_pypi.sh

# Tag release
git tag -a vX.Y.Z -m "Release version X.Y.Z"
git push origin vX.Y.Z

# Clean build artifacts
find packages -type d -name "build" -exec rm -rf {} +
find packages -type d -name "dist" -exec rm -rf {} +
find packages -type d -name "*.egg-info" -exec rm -rf {} +
```
