# Local Testing Guide

Run these commands locally **before pushing** to catch CI/CD failures early.

## Quick Start

```powershell
# Full validation (recommended before push)
.\scripts\validate_before_push.ps1

# Quick iteration during development
.\scripts\quick_test.ps1

# Skip specific checks
.\scripts\validate_before_push.ps1 -SkipTests
.\scripts\validate_before_push.ps1 -Fast  # Skip slow tests
```

## What Gets Checked

### 1. Type Checking
```powershell
python -m mypy src/pywats --config-file pyproject.toml
```

### 2. Unit Tests
```powershell
python -m pytest tests/ -v --tb=short -x -m "not server"
```

### 3. Import Check
```powershell
python -c "import pywats"
```

### 4. Package Build
```powershell
python -m build --sdist --wheel .
```

## Install Pre-Commit Hook (Optional)

Automatically validate before each commit:

```powershell
# Windows
Copy-Item scripts\pre-commit-hook.ps1 .git\hooks\pre-commit
```

To bypass: `git commit --no-verify`

## Reproduce Exact CI Environment

### Test on Multiple Python Versions

```powershell
# Using pyenv or similar
pyenv local 3.10 3.11 3.12
foreach ($ver in @("3.10", "3.11", "3.12")) {
    python$ver -m pytest tests/ -x
}
```

### Test Docker Build

```powershell
cd deployment\docker
docker build -t pywats-test -f Dockerfile ..\..
docker run --rm pywats-test python -c "import pywats; print('OK')"
```

### Test Rocky Linux

```powershell
docker run --rm -v ${PWD}:/src rockylinux:9 bash -c "
    cd /src
    dnf install -y python3.11 python3.11-pip gcc
    python3.11 -m pip install -e .[dev]
    python3.11 -m pytest tests/ -x
"
```

## Common Issues

### Import Errors
If you get `NameError: name 'Result' is not defined`:
- Check all imports in the file
- Run: `python -c "from pywats.shared.result import Result"`

### Type Check Failures
```powershell
# See exactly what mypy sees
python -m mypy src/pywats --show-error-codes --show-traceback
```

### Test Failures
```powershell
# Run specific test
python -m pytest tests/client/test_async_client_service.py::TestAsyncServiceStatus -v

# See full output
python -m pytest tests/ -v --tb=long --no-header -x
```

## Best Practice Workflow

```powershell
# 1. Make changes
# 2. Quick test during development
.\scripts\quick_test.ps1

# 3. Before committing
.\scripts\validate_before_push.ps1

# 4. If all passes, commit and push
git add .
git commit -m "Your message"
git push
```

## Continuous Integration Locally

Run the exact GitHub Actions matrix:

```powershell
# Install act (https://github.com/nektos/act)
choco install act-cli

# Run GitHub Actions locally
act -j test  # Run test job
act -j type-checking  # Run type checking
act push  # Run all push triggers
```
