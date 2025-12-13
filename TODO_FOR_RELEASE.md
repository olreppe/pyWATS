# TODO List for pyWATS Package Release

This document provides a comprehensive checklist of tasks needed to prepare pyWATS for release as individual pip packages.

## ✅ Completed Tasks

### Package Structure & Configuration
- [x] Create package directory structure (`packages/`)
- [x] Create separate `pyproject.toml` for each package:
  - [x] `pywats` - Core API library
  - [x] `pywats-client-service` - Client service framework
  - [x] `pywats-client-headless` - CLI and HTTP API
  - [x] `pywats-client-gui` - Desktop GUI application
- [x] Define package metadata (name, version, description, authors)
- [x] Define package dependencies and inter-package relationships
- [x] Configure package discovery and source paths
- [x] Create `MANIFEST.in` files for each package

### Documentation
- [x] Create LICENSE file (MIT License)
- [x] Create README.md for each package with:
  - [x] Installation instructions
  - [x] Usage examples
  - [x] Feature descriptions
  - [x] Requirements
- [x] Create CHANGELOG.md for each package
- [x] Create comprehensive guides:
  - [x] RELEASE_GUIDE.md - Complete release process
  - [x] PACKAGE_OVERVIEW.md - Package comparison and selection
  - [x] MIGRATION_GUIDE.md - Migration from monorepo to packages
  - [x] RELEASE_CHECKLIST.md - Detailed release checklist template

### Build & Release Scripts
- [x] Create `scripts/build_all_packages.sh` - Build all packages
- [x] Create `scripts/test_local_install.sh` - Test local installations
- [x] Create `scripts/upload_to_testpypi.sh` - Upload to TestPyPI
- [x] Create `scripts/release_to_pypi.sh` - Release to production PyPI
- [x] Make all scripts executable

### Configuration
- [x] Update `.gitignore` to exclude build artifacts

---

## 🔲 Remaining Tasks

### 1. Version Management (HIGH PRIORITY)

- [ ] **Update version numbers** to match across all packages:
  - [ ] `packages/pywats/pyproject.toml` → version = "2.0.0"
  - [ ] `packages/pywats-client-service/pyproject.toml` → version = "2.0.0"
  - [ ] `packages/pywats-client-headless/pyproject.toml` → version = "2.0.0"
  - [ ] `packages/pywats-client-gui/pyproject.toml` → version = "2.0.0"
  - [ ] `src/pyWATS/__init__.py` → `__version__ = "2.0.0"`
  - [ ] Root `pyproject.toml` → Update to reflect new structure

- [ ] **Decide on initial version number**:
  - Option 1: Start at 1.0.0 (first official release)
  - Option 2: Continue at 2.0.0 (major architecture change)
  - **Recommendation**: 2.0.0 (reflects the major refactoring)

### 2. Update Author/Maintainer Information (HIGH PRIORITY)

- [ ] Replace placeholder emails in all `pyproject.toml` files:
  - Currently: `support@virinco.com`
  - Update to: Actual contact email
  - Or: Create GitHub team email

- [ ] Verify copyright information in LICENSE
- [ ] Verify author names are correct

### 3. Dependency Audit & Security (HIGH PRIORITY)

- [ ] **Audit all dependencies for security vulnerabilities**:
  ```bash
  pip install safety
  safety check -r requirements.txt
  ```

- [ ] **Update dependencies** to latest compatible versions:
  - [ ] httpx - Check for updates
  - [ ] pydantic - Check for updates (note: v2.0+ may have breaking changes)
  - [ ] PySide6 - Check for updates
  - [ ] python-dateutil - Check for updates
  - [ ] watchdog - Check for updates
  - [ ] aiohttp - Check for updates
  - [ ] aiofiles - Check for updates

- [ ] **Verify minimum version requirements**:
  - [ ] Test with minimum specified versions
  - [ ] Test with latest versions
  - [ ] Document any compatibility issues

### 4. Update Main README (MEDIUM PRIORITY)

- [ ] Update root README.md to reference new package structure
- [ ] Add installation instructions for each package
- [ ] Add links to package-specific READMEs
- [ ] Add migration guide link
- [ ] Update examples to show pip installation

### 5. Testing (HIGH PRIORITY)

#### Unit Tests
- [ ] Ensure all existing tests pass:
  ```bash
  pytest tests/
  ```
- [ ] Update test imports if needed for package structure
- [ ] Verify test coverage is adequate

#### Build Testing
- [ ] Build all packages locally:
  ```bash
  bash scripts/build_all_packages.sh
  ```
- [ ] Verify build output (wheels and source distributions)
- [ ] Check package contents are correct
- [ ] Verify no unwanted files are included

#### Installation Testing
- [ ] Test local installation:
  ```bash
  bash scripts/test_local_install.sh
  ```
- [ ] Test in clean virtual environment
- [ ] Test on multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)

#### Functional Testing
- [ ] Test core API functionality
- [ ] Test client-service functionality
- [ ] Test headless client CLI commands
- [ ] Test GUI client (if display available)
- [ ] Test converters work correctly
- [ ] Test queue processing

### 6. Platform Testing (MEDIUM PRIORITY)

- [ ] **Test on Windows**:
  - [ ] Installation
  - [ ] CLI commands
  - [ ] GUI application
  
- [ ] **Test on macOS**:
  - [ ] Installation
  - [ ] CLI commands
  - [ ] GUI application
  
- [ ] **Test on Linux**:
  - [ ] Installation
  - [ ] CLI commands
  - [ ] GUI application
  - [ ] Systemd service setup

### 7. PyPI Account Setup (HIGH PRIORITY)

- [ ] **Create PyPI account** (if not exists):
  - Go to https://pypi.org/account/register/
  
- [ ] **Create TestPyPI account** (for testing):
  - Go to https://test.pypi.org/account/register/
  
- [ ] **Generate API tokens**:
  - [ ] PyPI API token for production uploads
  - [ ] TestPyPI API token for testing
  
- [ ] **Configure `~/.pypirc`** with tokens:
  ```ini
  [distutils]
  index-servers =
      pypi
      testpypi

  [pypi]
  username = __token__
  password = pypi-YOUR_API_TOKEN_HERE

  [testpypi]
  repository = https://test.pypi.org/legacy/
  username = __token__
  password = pypi-YOUR_TESTPYPI_TOKEN_HERE
  ```

- [ ] **Reserve package names on PyPI** (optional but recommended):
  - [ ] pywats
  - [ ] pywats-client-service
  - [ ] pywats-client-headless
  - [ ] pywats-client-gui

### 8. Pre-Release Testing (HIGH PRIORITY)

- [ ] **Upload to TestPyPI**:
  ```bash
  bash scripts/upload_to_testpypi.sh
  ```

- [ ] **Test installation from TestPyPI**:
  ```bash
  pip install --index-url https://test.pypi.org/simple/ \
              --extra-index-url https://pypi.org/simple/ \
              pywats
  ```

- [ ] **Verify TestPyPI package pages**:
  - [ ] Check README renders correctly
  - [ ] Verify metadata is correct
  - [ ] Test download links work

- [ ] **Fix any issues found** and re-upload if necessary

### 9. Documentation Review (MEDIUM PRIORITY)

- [ ] **Review all documentation for accuracy**:
  - [ ] Package READMEs
  - [ ] CHANGELOGs
  - [ ] RELEASE_GUIDE.md
  - [ ] PACKAGE_OVERVIEW.md
  - [ ] MIGRATION_GUIDE.md

- [ ] **Check all links work**:
  - [ ] GitHub links
  - [ ] Documentation links
  - [ ] PyPI links (after upload)

- [ ] **Verify code examples are correct**:
  - [ ] Copy/paste examples and test them
  - [ ] Ensure imports are correct
  - [ ] Check for typos

### 10. CI/CD Setup (OPTIONAL but RECOMMENDED)

- [ ] **Create GitHub Actions workflow** for:
  - [ ] Automated testing on push
  - [ ] Automated building on tag
  - [ ] Automated PyPI release on tag
  - [ ] Multi-platform testing (Windows, macOS, Linux)
  - [ ] Multi-version testing (Python 3.8-3.12)

Example workflow: `.github/workflows/release.yml`

### 11. Additional Documentation (LOW PRIORITY)

- [ ] Create CONTRIBUTING.md (for open source contributors)
- [ ] Create CODE_OF_CONDUCT.md (if open source)
- [ ] Create SECURITY.md (security policy)
- [ ] Update wiki (if applicable)
- [ ] Create video tutorials (optional)

### 12. Release Preparation (BEFORE RELEASE)

- [ ] **Final code review**:
  - [ ] Check for TODO/FIXME comments
  - [ ] Remove debug code
  - [ ] Check for hard-coded credentials
  - [ ] Verify no sensitive data in code

- [ ] **Update all CHANGELOGs** with release date

- [ ] **Create release notes** summarizing:
  - New features
  - Breaking changes
  - Bug fixes
  - Migration steps

- [ ] **Tag release in git** (after everything is ready):
  ```bash
  git tag -a v2.0.0 -m "Release version 2.0.0"
  git push origin v2.0.0
  ```

### 13. Production Release (WHEN READY)

- [ ] **Final checklist review**:
  - [ ] All tests passing
  - [ ] All documentation reviewed
  - [ ] TestPyPI upload successful
  - [ ] Version numbers synchronized
  - [ ] Git tagged

- [ ] **Release to PyPI**:
  ```bash
  bash scripts/release_to_pypi.sh
  ```

- [ ] **Verify PyPI uploads**:
  - [ ] https://pypi.org/project/pywats/
  - [ ] https://pypi.org/project/pywats-client-service/
  - [ ] https://pypi.org/project/pywats-client-headless/
  - [ ] https://pypi.org/project/pywats-client-gui/

- [ ] **Create GitHub Release**:
  - Go to https://github.com/olreppe/pyWATS/releases
  - Create release from tag
  - Add release notes
  - Publish

- [ ] **Test installation from PyPI**:
  ```bash
  pip install pywats
  pip install pywats-client-headless
  pip install pywats-client-gui
  ```

### 14. Post-Release (AFTER RELEASE)

- [ ] **Monitor for issues**:
  - [ ] Check PyPI download statistics
  - [ ] Monitor GitHub issues
  - [ ] Check for installation problems

- [ ] **Announce release** (if applicable):
  - [ ] Post on company website
  - [ ] Email to users
  - [ ] Social media
  - [ ] Relevant forums/communities

- [ ] **Update project website** (if applicable)

- [ ] **Plan next release**:
  - [ ] Review feedback
  - [ ] Prioritize features
  - [ ] Update roadmap

---

## Priority Summary

### Must Do Before First Release (HIGH PRIORITY)
1. Update version numbers across all packages
2. Update author/maintainer information
3. Audit dependencies for security
4. Build and test packages locally
5. Create PyPI accounts and configure credentials
6. Test on TestPyPI
7. Run full test suite

### Should Do Before First Release (MEDIUM PRIORITY)
1. Update main README
2. Test on multiple platforms (Windows, macOS, Linux)
3. Review all documentation
4. Test with multiple Python versions

### Nice to Have (LOW PRIORITY)
1. Set up CI/CD with GitHub Actions
2. Create additional documentation (CONTRIBUTING, etc.)
3. Create video tutorials

---

## Quick Start for Release Manager

If you're ready to proceed with release:

1. **Complete HIGH PRIORITY tasks** above
2. **Review RELEASE_CHECKLIST.md** for detailed steps
3. **Follow RELEASE_GUIDE.md** for complete process
4. **Use scripts/** for automation:
   - `build_all_packages.sh` - Build packages
   - `test_local_install.sh` - Test locally
   - `upload_to_testpypi.sh` - Test on TestPyPI
   - `release_to_pypi.sh` - Release to production

---

## Questions to Answer

Before proceeding with release, answer these questions:

1. **What version number should we start with?**
   - [ ] 1.0.0 (first release)
   - [ ] 2.0.0 (major refactor)
   - [ ] Other: _______

2. **What is the official contact email?**
   - Current: support@virinco.com
   - Confirm or update: _______

3. **Are all dependencies at the correct versions?**
   - [ ] Yes
   - [ ] No (need to update)

4. **Is the project open source or proprietary?**
   - [ ] Open Source (need CONTRIBUTING.md, CODE_OF_CONDUCT.md)
   - [ ] Proprietary (may need different license)

5. **Who will manage the PyPI account?**
   - Name: _______
   - Email: _______

6. **When is the target release date?**
   - Target: _______

---

## Resources

- **Python Packaging Guide**: https://packaging.python.org/
- **PyPI Documentation**: https://pypi.org/help/
- **TestPyPI**: https://test.pypi.org/
- **Semantic Versioning**: https://semver.org/
- **Keep a Changelog**: https://keepachangelog.com/

---

## Notes

Add any additional notes or decisions here:

```
- 
- 
- 
```
