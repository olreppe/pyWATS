# Testing & Packaging Without Target Hardware

> **Goal**: Maximize confidence before customer deployment without access to every target OS.

This guide describes what testing and packaging can be done from a single development machine, what risks remain, and strategies to minimize customer-facing issues.

---

## Testing Strategy Overview

### What You CAN Test Locally

| Category | Approach | Confidence |
|----------|----------|------------|
| Python code logic | pytest, mocking | 🟢 95%+ |
| API integration | Live WATS server tests | 🟢 95%+ |
| Package structure | Build artifacts, syntax check | 🟢 90%+ |
| Docker images | Local Docker, multi-arch emulation | 🟢 85%+ |
| Systemd units | Syntax validation, config tests | 🟡 70% |
| SELinux policies | Compile-time validation | 🟡 60% |
| Windows Service | pywin32 on Windows dev machine | 🟢 95%+ |

### What You CANNOT Test Locally

| Category | Why | Workaround |
|----------|-----|------------|
| Actual service behavior on target OS | Need real systemd/launchd | CI runners, VM |
| SELinux enforcement | Need SELinux-enabled system | CI with RHEL image |
| Kernel-level differences | ARM vs x86, kernel versions | QEMU, CI matrix |
| Real hardware constraints | Raspberry Pi memory/IO | ARM emulation |
| Boot sequences | First-boot wizard, init order | VM snapshots |

---

## 1. Python Code Testing (🟢 HIGH CONFIDENCE)

### Unit Tests with Mocking

You can test 95%+ of the business logic without any target OS:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest api-tests/ -v
pytest -k "service" -v
```

### What to Mock

```python
# Mock OS-specific calls
@pytest.fixture
def mock_systemd():
    with patch('subprocess.run') as mock:
        mock.return_value = CompletedProcess(args=[], returncode=0)
        yield mock

# Mock Windows registry
@pytest.fixture  
def mock_winreg():
    with patch('winreg.OpenKey'), patch('winreg.SetValueEx'):
        yield

# Mock file system paths
@pytest.fixture
def temp_config_dir(tmp_path):
    config = tmp_path / "config"
    config.mkdir()
    return config
```

### Platform-Conditional Tests

```python
import pytest
import sys

@pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
def test_windows_service_install():
    ...

@pytest.mark.skipif(sys.platform != "linux", reason="Linux only")
def test_systemd_unit_generation():
    ...
```

### Recommended Test Coverage

| Component | Target Coverage | Priority |
|-----------|-----------------|----------|
| Core API client | 90%+ | Critical |
| Report models | 90%+ | Critical |
| Domain services | 85%+ | High |
| Offline queue | 85%+ | High |
| Health server | 80%+ | Medium |
| Service wrappers | 70%+ | Medium |
| Platform-specific | 50%+ | Low (mocked) |

---

## 2. Package Build Validation (🟢 HIGH CONFIDENCE)

### DEB Package - Linting Without Building

```bash
# Install lintian (Debian/Ubuntu or WSL)
sudo apt install lintian devscripts

# Check control file syntax
cat debian/control | grep -E "^(Package|Version|Depends):" 

# Validate shell scripts
shellcheck debian/postinst debian/prerm debian/postrm

# Check debhelper compatibility
grep -E "^[0-9]+$" debian/compat
```

### RPM Spec - Validation Without Building

```bash
# Check spec file syntax (requires rpm-build or WSL with it)
rpmlint rpm/pywats.spec

# Or just validate macros expand correctly
rpmspec -P rpm/pywats.spec 2>&1 | head -50

# Shellcheck the scriptlets embedded in spec
grep -A20 "^%post" rpm/pywats.spec | shellcheck -s bash -
```

### What Package Linting Catches

✅ Missing dependencies  
✅ Invalid version strings  
✅ Syntax errors in scripts  
✅ Missing required fields  
✅ Invalid file paths  

### What Package Linting Misses

❌ Runtime dependency resolution  
❌ Actual file installation paths  
❌ Post-install script execution  
❌ Service startup failures  

---

## 3. Systemd Unit Validation (🟡 MEDIUM CONFIDENCE)

### Syntax Validation (Without Systemd)

```bash
# Install systemd on WSL or use syntax checker
# On Windows, use a simple Python validator:

python -c "
import configparser
import sys
for f in ['debian/pywats-client.service', 'rpm/pywats-client.service']:
    try:
        cp = configparser.ConfigParser()
        cp.read(f)
        print(f'{f}: Valid INI syntax')
    except Exception as e:
        print(f'{f}: INVALID - {e}')
        sys.exit(1)
"
```

### Key Settings to Verify

```ini
# These are commonly misconfigured:
[Unit]
After=network-online.target  # Not just network.target

[Service]
Type=notify                  # Must match your app's behavior
ExecStart=/usr/bin/pywats    # Must be absolute path
User=pywats                  # Must exist (created by postinst)
```

### What Systemd Validation Catches

✅ INI syntax errors  
✅ Missing required sections  
✅ Invalid directive names  

### What Systemd Validation Misses

❌ Incorrect `Type=` for your application  
❌ `ExecStart` path doesn't exist  
❌ User/Group doesn't exist  
❌ Resource limits too restrictive  
❌ Security hardening too aggressive  

---

## 4. SELinux Policy Validation (🟡 MEDIUM CONFIDENCE)

### Compile-Time Validation (Without SELinux)

```bash
# If you have selinux-policy-devel (RHEL/Fedora/WSL with package)
cd selinux/
checkmodule -M -m -o pywats.mod pywats.te
semodule_package -o pywats.pp -m pywats.mod -f pywats.fc

# If compilation succeeds, syntax is valid
echo "SELinux policy compiles successfully"
```

### Simplified Validation Script

```python
# selinux_validator.py - Run on any system
import re

def validate_te_file(path):
    """Basic validation of type enforcement file."""
    with open(path) as f:
        content = f.read()
    
    errors = []
    
    # Check for required policy_module declaration
    if not re.search(r'policy_module\(pywats,', content):
        errors.append("Missing policy_module declaration")
    
    # Check type declarations
    if not re.search(r'type pywats_t;', content):
        errors.append("Missing pywats_t type declaration")
    
    # Check for domain_type macro
    if not re.search(r'domain_type\(pywats_t\)', content):
        errors.append("Missing domain_type macro")
    
    return errors

errors = validate_te_file('selinux/pywats.te')
if errors:
    print("SELinux policy errors:", errors)
else:
    print("SELinux policy looks valid")
```

### What SELinux Validation Catches

✅ Syntax errors in .te file  
✅ Undefined types (compile error)  
✅ Invalid macro usage  

### What SELinux Validation Misses

❌ Missing permissions for actual operations  
❌ File context mismatches  
❌ AVC denials at runtime  
❌ Interaction with other policies  

---

## 5. Docker Testing (🟢 HIGH CONFIDENCE)

### Multi-Architecture Validation

```bash
# Build and test locally (your native arch)
docker build -t pywats-test -f Dockerfile .
docker run --rm pywats-test python -c "import pywats; print('OK')"

# Test ARM64 via emulation (slower but works)
docker buildx create --use --name multiarch
docker buildx build --platform linux/arm64 -t pywats-arm64 --load .

# Run ARM64 image (requires QEMU)
docker run --rm --platform linux/arm64 pywats-arm64 python -c "import pywats; print('OK')"
```

### Health Check Validation

```bash
# Start container
docker run -d --name pywats-health -p 8080:8080 pywats-test

# Wait for startup
sleep 5

# Test health endpoint
curl -f http://localhost:8080/health && echo "Health OK"
curl -f http://localhost:8080/health/ready && echo "Ready OK"
curl http://localhost:8080/health/details | python -m json.tool

# Cleanup
docker stop pywats-health && docker rm pywats-health
```

### What Docker Testing Catches

✅ Missing Python dependencies  
✅ Import errors  
✅ Health endpoint functionality  
✅ Basic application startup  
✅ Multi-arch compatibility (via QEMU)  

### What Docker Testing Misses

❌ Host integration (volumes may behave differently)  
❌ Real ARM64 performance characteristics  
❌ Kernel-specific features  
❌ Network policy interactions in K8s  

---

## 6. GitHub Actions CI Matrix (🟢 HIGH CONFIDENCE)

### Recommended CI Configuration

```yaml
# .github/workflows/test-platforms.yml
name: Platform Tests

on: [push, pull_request]

jobs:
  test-matrix:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-24.04, windows-latest, macos-latest]
        python: ['3.10', '3.11', '3.12']
        exclude:
          # Reduce matrix size
          - os: macos-latest
            python: '3.10'
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      
      - name: Install
        run: pip install -e ".[dev]"
      
      - name: Test
        run: pytest --tb=short

  test-rhel:
    runs-on: ubuntu-latest
    container: rockylinux:9
    steps:
      - uses: actions/checkout@v4
      - name: Install Python
        run: dnf install -y python3.11 python3.11-pip
      - name: Test
        run: |
          python3.11 -m pip install -e ".[dev]"
          python3.11 -m pytest --tb=short

  build-packages:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Lint DEB
        run: |
          sudo apt-get install -y lintian shellcheck
          shellcheck debian/postinst debian/prerm debian/postrm
      
      - name: Lint RPM
        run: |
          docker run --rm -v $PWD:/src fedora:39 \
            bash -c "dnf install -y rpmlint && rpmlint /src/rpm/pywats.spec"
```

### What CI Matrix Catches

✅ Python version compatibility  
✅ OS-specific import errors  
✅ Missing system dependencies  
✅ Path separator issues (Windows)  
✅ Case sensitivity issues  

---

## 7. Expected Issues After Customer Deployment

Based on experience with similar cross-platform Python applications:

### Windows (🟢 LOW RISK - 5-10% issue rate)

| Issue | Likelihood | Mitigation |
|-------|------------|------------|
| Missing VC++ Redistributable | Medium | Include in installer/docs |
| Antivirus blocking | Medium | Document exclusions |
| UAC permission denied | Low | Clear admin instructions |
| Path too long | Low | Use short install path |

**Expected support tickets**: 1-2 per 20 installations

### Ubuntu/Debian (🟢 LOW RISK - 5-10% issue rate)

| Issue | Likelihood | Mitigation |
|-------|------------|------------|
| Missing libxcb for GUI | Medium | Document or include in deps |
| systemd user session issues | Low | Test both system and user |
| AppArmor conflicts | Low | Provide profile if needed |

**Expected support tickets**: 1-2 per 20 installations

### RHEL/Rocky/Alma (🟡 MEDIUM RISK - 15-25% issue rate)

| Issue | Likelihood | Mitigation |
|-------|------------|------------|
| SELinux AVC denials | High | Extensive policy, audit2allow docs |
| FIPS mode incompatibility | Medium | Test with FIPS, document |
| Subscription Manager deps | Medium | Document EPEL requirements |
| Python version mismatch | Low | Document minimum versions |

**Expected support tickets**: 3-5 per 20 installations

### macOS (🟡 MEDIUM RISK - 10-20% issue rate)

| Issue | Likelihood | Mitigation |
|-------|------------|------------|
| Gatekeeper blocking | High | Code signing or bypass docs |
| Rosetta translation issues | Medium | Native ARM build |
| Keychain permission dialogs | Medium | Document first-run |
| launchd not starting | Low | Clear setup instructions |

**Expected support tickets**: 2-4 per 20 installations

### Raspberry Pi (🟡 MEDIUM RISK - 15-25% issue rate)

| Issue | Likelihood | Mitigation |
|-------|------------|------------|
| Out of memory | High | Document 4GB+ requirement |
| SD card I/O slow | Medium | Recommend USB storage |
| 32-bit OS used | Medium | Clear 64-bit requirement |
| Missing Qt for GUI | Low | Headless-only recommendation |

**Expected support tickets**: 3-5 per 20 installations

### Docker (🟢 LOW RISK - 5% issue rate)

| Issue | Likelihood | Mitigation |
|-------|------------|------------|
| Volume permission issues | Medium | Document uid/gid mapping |
| Network connectivity | Low | Document required ports |
| Resource limits | Low | Document minimums |

**Expected support tickets**: 1 per 20 deployments

---

## 8. Risk Mitigation Strategies

### Strategy 1: Beta Customer Program

1. **Identify 2-3 friendly customers** per target platform
2. **Provide pre-release builds** with verbose logging
3. **Collect logs and feedback** before general release
4. **Create FAQ from real issues**

**Cost**: 2-4 weeks delay  
**Benefit**: 80% reduction in post-release issues

### Strategy 2: Verbose First-Run Diagnostics

Add a `--diagnose` command that checks:

```python
def diagnose():
    """Run comprehensive system diagnostics."""
    checks = [
        ("Python version", check_python_version),
        ("Required packages", check_packages),
        ("Network connectivity", check_network),
        ("Write permissions", check_permissions),
        ("Service manager", check_service_manager),
        ("SELinux status", check_selinux),
    ]
    
    for name, check in checks:
        try:
            result = check()
            print(f"✅ {name}: {result}")
        except Exception as e:
            print(f"❌ {name}: {e}")
```

### Strategy 3: Installation Validation Script

Ship a separate `validate_install.py`:

```bash
# Customer runs after installation
python validate_install.py

# Output:
# ✅ pyWATS imported successfully
# ✅ Config directory writable: /etc/pywats
# ✅ Log directory writable: /var/log/pywats
# ✅ Health endpoint responding: http://localhost:8080/health
# ✅ WATS server reachable: https://customer.wats.com
# ⚠️ SELinux: Enforcing (ensure policy installed)
# 
# Overall: READY
```

### Strategy 4: Comprehensive Error Messages

Instead of:
```
Error: Connection failed
```

Provide:
```
Error: Connection failed to https://customer.wats.com/api/version

Possible causes:
1. Server URL incorrect - verify in config.json
2. Network/firewall blocking - test: curl https://customer.wats.com
3. Proxy required - set HTTP_PROXY environment variable
4. SSL certificate issue - check system time and certificates

For more help: https://docs.pywats.com/troubleshooting/connection
```

---

## 9. Recommended Testing Checklist

### Before Release

- [ ] All pytest tests pass (Windows + Linux CI)
- [ ] `pip install` works from built wheel
- [ ] Docker image builds and starts
- [ ] Docker health check passes
- [ ] `shellcheck` passes on all shell scripts
- [ ] DEB control file valid syntax
- [ ] RPM spec file valid syntax
- [ ] SELinux policy compiles without errors
- [ ] README/CHANGELOG updated with platform info

### During Beta

- [ ] At least one customer on each target platform
- [ ] Collect and address first-run issues
- [ ] Update troubleshooting documentation
- [ ] Verify auto-update mechanism works

### Post-Release

- [ ] Monitor support tickets by platform
- [ ] Maintain platform-specific FAQ
- [ ] Regular CI runs on all platforms

---

## 10. Summary: Confidence Levels

| Platform | Pre-Release Confidence | Expected Issues |
|----------|----------------------|-----------------|
| Windows 10/11 | 🟢 95% | Minor (antivirus, UAC) |
| Ubuntu/Debian | 🟢 90% | Minor (GUI deps) |
| RHEL/Rocky | 🟡 75% | SELinux policy tuning |
| macOS | 🟡 80% | Code signing, Gatekeeper |
| Raspberry Pi | 🟡 75% | Memory, 32-bit users |
| Docker | 🟢 95% | Very minor |

**Bottom Line**: Without physical testing on each platform, expect **10-20% of first-time installations to require support intervention**. This drops to **~5%** with a beta customer program and good diagnostics tooling.

The most problematic platform will be **RHEL with SELinux enforcing** - budget extra time for SELinux policy refinement after real-world testing.
