# Migration Guide: Monorepo to Separate Packages

This guide helps you migrate from the monorepo development setup to the new separate pip packages.

## Overview of Changes

**Before (Monorepo)**:
- Single repository with all code
- Development install: `pip install -e .`
- All dependencies installed together
- One configuration file

**After (Separate Packages)**:
- Four distinct pip packages
- Install only what you need
- Cleaner dependency management
- Same functionality, better distribution

## For End Users

### If You Were Using the GUI

**Before**:
```bash
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS
pip install -e ".[client]"
python -m pywats_client
```

**After**:
```bash
pip install pywats-client-gui
pywats-client-gui
```

### If You Were Using Headless Mode

**Before**:
```bash
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS
pip install -e ".[client-headless]"
python -m pywats_client --no-gui
```

**After**:
```bash
pip install pywats-client-headless
pywats-client start --api
```

### If You Were Using Just the API

**Before**:
```bash
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS
pip install -e .
```

**After**:
```bash
pip install pywats
```

## For Developers

### Development Setup

**Before**:
```bash
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS
pip install -e ".[dev]"
```

**After**:
```bash
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS

# Option 1: Install all packages in development mode
pip install -e packages/pywats
pip install -e packages/pywats-client-service
pip install -e packages/pywats-client-headless
pip install -e packages/pywats-client-gui

# Option 2: Install just what you're working on
pip install -e "packages/pywats[dev]"  # API development
pip install -e "packages/pywats-client-gui[dev]"  # GUI development
```

### Import Changes

Good news: **No import changes needed!** The package structure remains the same.

```python
# Still works exactly the same
from pywats import pyWATS
from pywats_client.core import WATSClient
from pywats_client.gui import app
```

### Configuration Files

**No changes needed**. Configuration files remain compatible:
- `~/.pywats_client/config.json` - Same location, same format
- Converter directories - Same structure
- Queue directories - Same structure

## Code Compatibility

### API Code - No Changes
```python
# This code works exactly the same
from pywats import pyWATS

api = pyWATS(base_url="...", token="...")
products = api.product.get_products()
```

### Client Code - No Changes
```python
# This code works exactly the same
from pywats_client.core import ClientConfig
config = ClientConfig.load_or_create(path)
```

### Converter Code - No Changes
```python
# Converters work exactly the same
from pywats_client.converters import BaseConverter

class MyConverter(BaseConverter):
    # Same as before
    pass
```

## Testing Your Migration

### 1. Verify Installation

```bash
# Check versions
python -c "from pywats import pyWATS; print(pyWATS.__version__)"

# Test imports
python -c "from pywats_client.core import WATSClient; print('OK')"
```

### 2. Test Your Existing Scripts

Your existing Python scripts should work without modification:

```bash
# Your old scripts should still work
python my_test_script.py
python my_converter.py
```

### 3. Test Configuration

```bash
# Check config loads correctly
pywats-client config show

# Test connection
pywats-client test-connection
```

## Package Dependencies

Understanding the new dependency structure:

```
Your Application
    ↓
┌─────────────────────────────────┐
│  What you install               │
├─────────────────────────────────┤
│ pywats-client-gui               │
│   ↓                             │
│ pywats-client-service           │
│   ↓                             │
│ pywats (core API)               │
└─────────────────────────────────┘
    ↓
[httpx, pydantic, PySide6, etc.]
```

You only need to install the top-level package; pip handles the rest.

## Common Migration Scenarios

### Scenario 1: Production Test Station (GUI)

**Before**:
1. Clone repo on each station
2. Install with pip install -e ".[client]"
3. Run python -m pywats_client

**After**:
1. Install: `pip install pywats-client-gui`
2. Run: `pywats-client-gui`

**Advantages**:
- No git required on test stations
- Easier updates: `pip install --upgrade pywats-client-gui`
- Cleaner installation

---

### Scenario 2: Raspberry Pi Test Station

**Before**:
1. Clone repo
2. Install with pip install -e ".[client-headless]"
3. Run python -m pywats_client --no-gui

**After**:
1. Install: `pip install pywats-client-headless`
2. Configure: `pywats-client config init`
3. Run: `pywats-client start --daemon --api`

**Advantages**:
- Smaller installation (no git history)
- Proper systemd integration
- Better CLI interface

---

### Scenario 3: CI/CD Pipeline

**Before**:
```yaml
steps:
  - git clone repo
  - pip install -e .
  - python scripts/submit_results.py
```

**After**:
```yaml
steps:
  - pip install pywats
  - python scripts/submit_results.py
```

**Advantages**:
- Faster CI builds (no git clone)
- Exact version control
- Smaller container images

---

### Scenario 4: Custom Application

**Before**:
```bash
# Install full monorepo
pip install git+https://github.com/olreppe/pyWATS.git
```

**After**:
```bash
# Install only what you need
pip install pywats  # Just API
# or
pip install pywats pywats-client-service  # API + converters
```

**Advantages**:
- Smaller dependencies
- Faster installation
- Clearer requirements

## Updating Deployment

### Docker

**Before**:
```dockerfile
FROM python:3.11
RUN git clone https://github.com/olreppe/pyWATS.git
WORKDIR /pyWATS
RUN pip install -e ".[client-headless]"
CMD ["python", "-m", "pywats_client", "--no-gui"]
```

**After**:
```dockerfile
FROM python:3.11
RUN pip install pywats-client-headless
CMD ["pywats-client", "start", "--api"]
```

**Size reduction**: ~50-100MB smaller image

---

### Requirements.txt

**Before**:
```
-e git+https://github.com/olreppe/pyWATS.git#egg=pywats
```

**After**:
```
pywats==2.0.0
# or
pywats-client-headless==2.0.0
# or
pywats-client-gui==2.0.0
```

---

### Systemd Service

**Before**:
```ini
[Service]
WorkingDirectory=/opt/pyWATS
ExecStart=/usr/bin/python3 -m pywats_client --no-gui
```

**After**:
```ini
[Service]
ExecStart=/usr/local/bin/pywats-client start --daemon --api
```

## Version Pinning

### Development
```bash
# Install latest
pip install pywats-client-gui
```

### Production
```bash
# Pin specific version
pip install pywats-client-gui==2.0.0
```

### Requirements File
```
# Exact version (recommended for production)
pywats==2.0.0
pywats-client-headless==2.0.0

# Or version range (for flexibility)
pywats>=2.0.0,<3.0.0
pywats-client-headless>=2.0.0,<3.0.0
```

## Rollback Plan

If you need to rollback to the monorepo setup:

```bash
# Uninstall packages
pip uninstall pywats pywats-client-service pywats-client-headless pywats-client-gui

# Clone and install monorepo
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS
pip install -e ".[client]"  # or .[client-headless]
```

## Benefits of Migration

1. **Simpler Installation**: One pip command instead of git clone
2. **Smaller Footprint**: Install only what you need
3. **Better Updates**: `pip install --upgrade` instead of git pull
4. **Version Control**: Pin exact versions in production
5. **Faster CI/CD**: No git operations needed
6. **Better Packaging**: Standard Python package distribution
7. **PyPI Integration**: Available via `pip install` globally

## Getting Help

If you encounter issues during migration:

1. Check this guide for your specific scenario
2. Review [PACKAGE_OVERVIEW.md](PACKAGE_OVERVIEW.md) for package selection
3. See [RELEASE_GUIDE.md](RELEASE_GUIDE.md) for version information
4. Open an issue: https://github.com/olreppe/pyWATS/issues

## Migration Checklist

Use this checklist to ensure a smooth migration:

- [ ] Identify which package(s) you need
- [ ] Read the relevant README for your package
- [ ] Uninstall old monorepo installation (if applicable)
- [ ] Install new package(s)
- [ ] Test imports in Python
- [ ] Test your existing scripts
- [ ] Verify configuration files work
- [ ] Test your converters
- [ ] Update deployment scripts/Dockerfiles
- [ ] Update documentation/README files
- [ ] Pin versions in requirements.txt
- [ ] Test in staging environment
- [ ] Deploy to production

## Summary

The migration is straightforward:
- **Functionality remains the same**
- **No code changes needed**
- **Installation is simpler**
- **Updates are easier**

Choose your package and install with pip. That's it!
