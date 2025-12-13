# pyWATS Release Guide

This guide covers the complete process for releasing pyWATS packages to PyPI.

## Package Structure

The pyWATS project is organized into four separate pip packages:

1. **pywats** - Core API library
2. **pywats-client-service** - Client service framework (converter management, queue processing)
3. **pywats-client-headless** - CLI and HTTP API for headless operation
4. **pywats-client-gui** - Desktop GUI application with Qt

### Package Dependencies

```
pywats (core API)
    ↓
pywats-client-service (depends on pywats)
    ↓
    ├── pywats-client-headless (depends on pywats + pywats-client-service)
    └── pywats-client-gui (depends on pywats + pywats-client-service)
```

## Prerequisites

### 1. Install Build Tools

```bash
pip install --upgrade pip setuptools wheel twine build
```

### 2. Create PyPI Accounts

- Register at [PyPI](https://pypi.org/account/register/)
- Register at [TestPyPI](https://test.pypi.org/account/register/) (for testing)

### 3. Configure PyPI Credentials

Create `~/.pypirc`:

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

**Security Note**: Use API tokens, not passwords. Generate tokens from your PyPI account settings.

## Pre-Release Checklist

### For Each Package:

- [ ] Update version number in `pyproject.toml`
- [ ] Update `CHANGELOG.md` with new version and changes
- [ ] Update `README.md` if needed
- [ ] Verify all dependencies are correct and up-to-date
- [ ] Update author/maintainer information
- [ ] Run tests: `pytest`
- [ ] Run linters: `black`, `isort`, `flake8`
- [ ] Check security vulnerabilities in dependencies

### Repository-Wide:

- [ ] Ensure `LICENSE` file exists and is correct
- [ ] Update main `README.md` in root
- [ ] Tag the release in git
- [ ] Update documentation

## Version Numbers

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 2.0.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Version Synchronization

**All four packages should use the same version number** for consistency, even if some packages have no changes.

Example: If releasing version 2.1.0:
- pywats: 2.1.0
- pywats-client-service: 2.1.0
- pywats-client-headless: 2.1.0
- pywats-client-gui: 2.1.0

## Build Process

### Build Individual Package

```bash
# Navigate to package directory
cd packages/pywats

# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build package
python -m build

# Output will be in dist/
# - pywats-2.0.0.tar.gz (source distribution)
# - pywats-2.0.0-py3-none-any.whl (wheel distribution)
```

### Build All Packages

```bash
# Use the build script
bash scripts/build_all_packages.sh
```

## Testing Builds Locally

### Install from Local Build

```bash
# Install from wheel
pip install packages/pywats/dist/pywats-2.0.0-py3-none-any.whl

# Or install from source
pip install packages/pywats/dist/pywats-2.0.0.tar.gz
```

### Test Installation

```python
# Test pywats
python -c "from pywats import pyWATS; print(pyWATS.__version__)"

# Test client-service
python -c "from pywats_client.core import WATSClient; print('OK')"

# Test headless
python -c "from pywats_client.control import cli; print('OK')"

# Test GUI
python -c "from pywats_client.gui import app; print('OK')"
```

## Release to TestPyPI (Recommended First)

Test your packages on TestPyPI before releasing to production:

```bash
# Upload to TestPyPI
cd packages/pywats
twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats
```

**Note**: `--extra-index-url` is needed because TestPyPI doesn't have all dependencies.

## Release to PyPI (Production)

### Upload Individual Package

```bash
cd packages/pywats
twine upload dist/*
```

### Upload All Packages

**Important**: Upload in dependency order!

```bash
# 1. Core API first
cd packages/pywats
twine upload dist/*

# 2. Client service second
cd ../pywats-client-service
twine upload dist/*

# 3. Headless client
cd ../pywats-client-headless
twine upload dist/*

# 4. GUI client
cd ../pywats-client-gui
twine upload dist/*
```

### Automated Upload Script

```bash
bash scripts/release_to_pypi.sh
```

## Post-Release

### 1. Tag Release in Git

```bash
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

### 2. Create GitHub Release

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Select the tag you just created
4. Add release notes (copy from CHANGELOG.md)
5. Publish release

### 3. Verify Installation

```bash
# Create clean virtual environment
python -m venv test_env
source test_env/bin/activate  # or test_env\Scripts\activate on Windows

# Install from PyPI
pip install pywats
pip install pywats-client-headless
pip install pywats-client-gui

# Test
python -c "from pywats import pyWATS; print(pyWATS.__version__)"
pywats-client --version
```

### 4. Update Documentation

- Update installation instructions
- Update version numbers in documentation
- Announce release on relevant channels

## Troubleshooting

### Build Errors

```bash
# Clean everything and rebuild
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "*.egg-info" -exec rm -rf {} +
find . -type d -name "build" -exec rm -rf {} +
find . -type d -name "dist" -exec rm -rf {} +
```

### Upload Errors

**Error**: "File already exists"
- You cannot upload the same version twice
- Increment version number and rebuild

**Error**: "Invalid credentials"
- Check your `~/.pypirc` file
- Regenerate API tokens if needed

**Error**: "Package name already taken"
- Choose a different name
- Check if you have permissions for the package

### Dependency Issues

**Problem**: Users can't install due to dependency conflicts

**Solution**: 
- Test with fresh virtual environments
- Use version ranges instead of pinned versions
- Document known compatibility issues

## Release Checklist Template

Copy this for each release:

```markdown
## Release X.Y.Z Checklist

### Pre-Release
- [ ] Update version in all 4 packages
- [ ] Update CHANGELOGs
- [ ] Run all tests
- [ ] Run linters
- [ ] Update documentation
- [ ] Review dependencies

### Build
- [ ] Build pywats
- [ ] Build pywats-client-service
- [ ] Build pywats-client-headless
- [ ] Build pywats-client-gui
- [ ] Test local installations

### TestPyPI
- [ ] Upload to TestPyPI
- [ ] Test installation from TestPyPI
- [ ] Verify functionality

### PyPI
- [ ] Upload pywats
- [ ] Upload pywats-client-service
- [ ] Upload pywats-client-headless
- [ ] Upload pywats-client-gui
- [ ] Verify PyPI pages look correct

### Post-Release
- [ ] Tag release in Git
- [ ] Create GitHub release
- [ ] Test clean installation from PyPI
- [ ] Update documentation
- [ ] Announce release
```

## Automation (Future)

Consider setting up:

- **GitHub Actions**: Automate builds and tests
- **Automated versioning**: Use tools like `bump2version`
- **Automated releases**: Trigger releases on git tags
- **Automated testing**: Test on multiple Python versions

## Support

For questions or issues with the release process:
- Create an issue on GitHub
- Contact the maintainers
- Check PyPI documentation: https://packaging.python.org/
