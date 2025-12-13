# Quick Start: Release pyWATS Packages

This is a condensed guide to get you releasing packages as quickly as possible. For detailed information, see the full documentation.

## TL;DR - Complete Release Process

```bash
# 1. Update versions and metadata (do this manually in pyproject.toml files)

# 2. Build packages
bash scripts/build_all_packages.sh

# 3. Test locally
bash scripts/test_local_install.sh

# 4. Upload to TestPyPI (for testing)
bash scripts/upload_to_testpypi.sh

# 5. Test from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats

# 6. Release to PyPI (production)
bash scripts/release_to_pypi.sh

# 7. Tag release
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0

# 8. Create GitHub release at https://github.com/olreppe/pyWATS/releases
```

## Prerequisites (One-Time Setup)

### 1. Install Build Tools
```bash
pip install --upgrade pip setuptools wheel twine build
```

### 2. Create PyPI Accounts
- PyPI: https://pypi.org/account/register/
- TestPyPI: https://test.pypi.org/account/register/

### 3. Generate API Tokens
- PyPI: https://pypi.org/manage/account/token/
- TestPyPI: https://test.pypi.org/manage/account/token/

### 4. Configure `~/.pypirc`
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR_PRODUCTION_TOKEN_HERE

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TEST_TOKEN_HERE
```

## Before First Release

### 1. Update Version Numbers
Edit these files to set version to `2.0.0` (or your chosen version):
- `packages/pywats/pyproject.toml`
- `packages/pywats-client-service/pyproject.toml`
- `packages/pywats-client-headless/pyproject.toml`
- `packages/pywats-client-gui/pyproject.toml`
- `src/pyWATS/__init__.py` (`__version__ = "2.0.0"`)

### 2. Update Author Information
Replace `support@virinco.com` with actual contact email in all `pyproject.toml` files.

### 3. Run Tests
```bash
pytest tests/
```

## The Four Packages

1. **pywats** - Core API library (everyone needs this)
2. **pywats-client-service** - Client framework (dependency for clients)
3. **pywats-client-headless** - CLI + HTTP API (for servers/Raspberry Pi)
4. **pywats-client-gui** - Desktop GUI (for operators)

They're released together in dependency order (1→2→3/4).

## Release Steps (Detailed)

### Step 1: Build All Packages
```bash
bash scripts/build_all_packages.sh
```
This creates wheel and source distributions in `packages/*/dist/`

### Step 2: Test Local Installation
```bash
bash scripts/test_local_install.sh
```
This creates a temporary venv, installs packages, and tests imports.

### Step 3: Upload to TestPyPI
```bash
bash scripts/upload_to_testpypi.sh
```
This uploads to TestPyPI for testing.

### Step 4: Test from TestPyPI
```bash
# Create clean environment
python -m venv test_env
source test_env/bin/activate  # or: test_env\Scripts\activate on Windows

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pywats-client-headless

# Test
python -c "from pywats import pyWATS; print(pyWATS.__version__)"
pywats-client --version

# Clean up
deactivate
rm -rf test_env
```

### Step 5: Release to PyPI (Production)
```bash
bash scripts/release_to_pypi.sh
```
⚠️ This uploads to production PyPI. Cannot be undone!

### Step 6: Verify Release
Check packages appeared:
- https://pypi.org/project/pywats/
- https://pypi.org/project/pywats-client-service/
- https://pypi.org/project/pywats-client-headless/
- https://pypi.org/project/pywats-client-gui/

### Step 7: Tag Release
```bash
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

### Step 8: Create GitHub Release
1. Go to https://github.com/olreppe/pyWATS/releases
2. Click "Create a new release"
3. Select tag `v2.0.0`
4. Title: "pyWATS v2.0.0"
5. Copy release notes from CHANGELOGs
6. Publish

### Step 9: Final Verification
```bash
# Create clean environment
python -m venv verify_env
source verify_env/bin/activate

# Install from PyPI
pip install pywats
pip install pywats-client-headless
pip install pywats-client-gui

# Test
python -c "from pywats import pyWATS; print(pyWATS.__version__)"
pywats-client --version
pywats-client-gui --version

# Clean up
deactivate
rm -rf verify_env
```

## Troubleshooting

### Build Failed
```bash
# Clean and retry
find packages -type d -name "build" -exec rm -rf {} +
find packages -type d -name "dist" -exec rm -rf {} +
find packages -type d -name "*.egg-info" -exec rm -rf {} +
bash scripts/build_all_packages.sh
```

### Upload Failed - "File already exists"
You can't upload the same version twice. Increment version and rebuild.

### Upload Failed - "Invalid credentials"
- Check `~/.pypirc` file exists and has correct format
- Verify API tokens are correct
- Regenerate tokens if needed

### Package Won't Install
- Check dependencies in `pyproject.toml`
- Verify package name is correct
- Check PyPI page for error messages

## For Subsequent Releases

1. Update version numbers in all `pyproject.toml` files
2. Update CHANGELOGs with new version and date
3. Run tests
4. Follow release steps above

## Quick Reference - File Locations

```
pyWATS/
├── packages/
│   ├── pywats/
│   │   ├── pyproject.toml          # Configure this
│   │   ├── README.md
│   │   ├── CHANGELOG.md            # Update this
│   │   └── MANIFEST.in
│   ├── pywats-client-service/
│   ├── pywats-client-headless/
│   └── pywats-client-gui/
├── scripts/
│   ├── build_all_packages.sh       # Use this
│   ├── test_local_install.sh       # Use this
│   ├── upload_to_testpypi.sh       # Use this
│   └── release_to_pypi.sh          # Use this
├── src/
│   ├── pyWATS/
│   │   └── __init__.py             # Update __version__
│   └── pywats_client/
├── LICENSE                          # Already created
├── RELEASE_GUIDE.md                # Detailed guide
├── PACKAGE_OVERVIEW.md             # Package comparison
├── MIGRATION_GUIDE.md              # User migration guide
├── RELEASE_CHECKLIST.md            # Detailed checklist
└── TODO_FOR_RELEASE.md             # Complete TODO list
```

## Need Help?

- **Detailed guide**: See `RELEASE_GUIDE.md`
- **Complete TODO list**: See `TODO_FOR_RELEASE.md`
- **Detailed checklist**: See `RELEASE_CHECKLIST.md`
- **Package info**: See `PACKAGE_OVERVIEW.md`
- **User migration**: See `MIGRATION_GUIDE.md`
- **Python packaging docs**: https://packaging.python.org/

## Summary

1. ✅ Update version numbers
2. ✅ Build: `bash scripts/build_all_packages.sh`
3. ✅ Test locally: `bash scripts/test_local_install.sh`
4. ✅ Upload to TestPyPI: `bash scripts/upload_to_testpypi.sh`
5. ✅ Test from TestPyPI
6. ✅ Release to PyPI: `bash scripts/release_to_pypi.sh`
7. ✅ Tag: `git tag -a v2.0.0 -m "Release 2.0.0"`
8. ✅ Push tag: `git push origin v2.0.0`
9. ✅ Create GitHub release
10. ✅ Verify installation from PyPI

**You're ready to release!** 🚀
