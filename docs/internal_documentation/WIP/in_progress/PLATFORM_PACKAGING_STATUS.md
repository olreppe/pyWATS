# Platform Support, Packaging & Testing Status

**Created:** January 27, 2026  
**Status:** 🔄 In Progress  
**Purpose:** Comprehensive analysis of platform support, packaging formats, and simulated testing strategy

---

## Executive Summary

### Current State Assessment

| Platform | Library | Client | Packaging | Installer | Status |
|----------|---------|--------|-----------|-----------|--------|
| **Windows 10/11** | ✅ 100% | ✅ 100% | ⚠️ PyPI only | ❌ No MSI | Needs installer |
| **Windows Server** | ✅ 100% | ✅ 100% | ⚠️ PyPI only | ❌ No MSI | Needs installer |
| **Windows IoT LTSC** | ✅ 100% | ✅ 100% | ⚠️ PyPI only | ❌ No MSI | Needs testing |
| **Ubuntu/Debian** | ✅ 100% | ✅ 100% | ✅ DEB ready | ✅ APT | Ready |
| **RHEL/Rocky/Alma** | ✅ 100% | ✅ 100% | ✅ RPM ready | ✅ YUM/DNF | Ready |
| **macOS** | ✅ 100% | ✅ 100% | ⚠️ PyPI only | ❌ No PKG/DMG | Needs installer |
| **Raspberry Pi** | ✅ 100% | ✅ 100% | ✅ DEB ready | ✅ APT | Ready |
| **Docker** | ✅ 100% | ✅ 100% | ✅ Dockerfile | ✅ Container | Ready |

### Key Gaps

1. **No native Windows installer (MSI)** - Enterprise IT needs GPO deployment
2. **No macOS installer (PKG/DMG)** - Users expect drag-and-drop
3. **No standalone executables** - Requires Python pre-installed
4. **Limited simulated testing** - No comprehensive CI/CD for all platforms

---

## Part 1: Current Packaging Infrastructure

### What Exists Today

#### 1. PyPI Package (All Platforms)
```
✅ Working: pip install pywats-api
✅ Working: pip install pywats-api[client]
✅ Working: pip install pywats-api[client-headless]
```

**Limitations:**
- Requires Python 3.10+ pre-installed
- Requires pip knowledge
- Not suitable for enterprise GPO deployment

#### 2. Debian/Ubuntu DEB Package
```
📁 deployment/debian/
├── control         ✅ Complete - dependencies, metadata
├── postinst        ✅ Complete - creates user, sets permissions
├── prerm           ✅ Complete - stops service
├── postrm          ✅ Complete - removes user (optional)
├── pywats-client.service  ✅ Complete - systemd unit
├── rules           ✅ Complete - debhelper build
└── changelog       ✅ Complete
```

**Build Command:** `dpkg-buildpackage -b -uc -us`

**Status:** ✅ Ready for production (needs CI/CD automation)

#### 3. RHEL/Rocky RPM Package
```
📁 deployment/rpm/
├── pywats.spec              ✅ Complete - full spec with scriptlets
├── pywats-client.service    ✅ Complete - systemd unit
└── config.json              ✅ Complete - default config
```

**Build Command:** `rpmbuild -bb pywats.spec`

**Status:** ✅ Ready for production (needs CI/CD automation)

#### 4. SELinux Policy
```
📁 deployment/selinux/
├── pywats.te        ✅ Complete - type enforcement
├── pywats.fc        ✅ Complete - file contexts  
└── install-selinux.sh ✅ Complete - installation script
```

**Status:** ✅ Compiles successfully - needs field testing on enforcing RHEL

#### 5. Docker Images
```
📁 deployment/docker/
├── Dockerfile       ✅ Complete - multi-stage (api, client-headless)
└── docker-compose.yml ✅ Complete
```

**CI/CD:** `.github/workflows/docker.yml` - builds and pushes to GHCR

**Architectures:** linux/amd64, linux/arm64

**Status:** ✅ Ready for production

#### 6. VM Appliances (Packer)
```
📁 deployment/packer/
├── pywats-appliance.pkr.hcl  ✅ Template exists
├── files/                    ✅ Setup scripts
└── http/                     ✅ Autoinstall configs
```

**Status:** ⚠️ Template exists but not actively built/published

---

## Part 2: Missing Packaging (Action Required)

### 🔴 Priority 1: Windows MSI Installer

**Why Critical:**
- Enterprise IT requires MSI for GPO (Group Policy) deployment
- Silent install capability mandatory for automation
- Clean upgrade/uninstall paths expected
- Most pyWATS customers are Windows-based manufacturing

**Recommended Approach: cx_Freeze + WiX**

```
📁 deployment/windows/ (TO CREATE)
├── build_msi.py              # Build script
├── pywats.wxs               # WiX manifest
├── freeze_config.py         # cx_Freeze configuration
├── installer_banner.png     # Branding
├── license.rtf              # License for installer
└── README.md
```

**Technical Stack:**
```python
# cx_Freeze configuration (freeze_config.py)
from cx_Freeze import setup, Executable

build_options = {
    "packages": ["pywats", "pywats_client", "httpx", "pydantic"],
    "excludes": ["tkinter", "test", "unittest"],
    "include_msvcr": True,  # Include Visual C++ Runtime
}

executables = [
    Executable(
        "src/pywats_client/__main__.py",
        base="Win32GUI" if gui else None,  # or "Win32Service"
        target_name="pywats-client.exe",
        icon="assets/pywats.ico",
    )
]
```

**Installer Features Required:**
- [ ] Silent install: `msiexec /i pywats-client.msi /qn`
- [ ] Custom install path
- [ ] Service registration (optional during install)
- [ ] Preserve config on upgrade
- [ ] Clean uninstall with config retention option
- [ ] Code signing (Authenticode)
- [ ] Version/upgrade handling (major/minor/patch)

**Estimated Effort:** 2-3 weeks

**Alternative: NSIS**
- Lighter weight than WiX
- Easier scripting
- Still supports silent install
- Less "enterprise" feel than MSI

### 🟡 Priority 2: macOS Installer (PKG/DMG)

**Why Important:**
- macOS users expect .app bundles
- Drag-to-Applications paradigm
- Code signing required for Gatekeeper
- notarization required for modern macOS

**Recommended Approach: py2app + pkgbuild**

```
📁 deployment/macos/ (TO CREATE)
├── build_app.py             # py2app build script
├── setup.py                 # py2app configuration
├── Info.plist               # App bundle metadata
├── pywats.icns              # macOS icon
├── create_dmg.sh            # DMG creation script
├── Distribution.xml         # Package distribution
└── README.md
```

**Packaging Flow:**
```bash
# 1. Build .app bundle
python setup.py py2app

# 2. Sign the app
codesign --deep --force --sign "Developer ID Application: Virinco AS" dist/pyWATS.app

# 3. Create installer package
pkgbuild --root dist/pyWATS.app --install-location /Applications --identifier com.virinco.pywats pywats.pkg

# 4. Create DMG
create-dmg dist/pyWATS.app dist/pyWATS-installer.dmg

# 5. Notarize
xcrun notarytool submit pywats.pkg --keychain-profile "virinco-notary" --wait
```

**Estimated Effort:** 2 weeks (includes signing/notarization pipeline)

### 🟢 Priority 3: Standalone Executables (All Platforms)

**Why Useful:**
- No Python installation required
- Single binary deployment
- Easier for non-technical users

**Recommended: PyInstaller (cross-platform)**

```python
# pyinstaller.spec
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src/pywats_client/__main__.py'],
    pathex=[],
    binaries=[],
    datas=[('src/pywats_client/gui/resources', 'resources')],
    hiddenimports=['pywats', 'pywats_client', 'httpx', 'pydantic'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pywats-client',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI mode
    icon='assets/pywats.ico'
)
```

**Platforms:**
- Windows: `.exe` (single file or folder)
- Linux: ELF binary (AppImage preferred)
- macOS: `.app` bundle

**Estimated Effort:** 1-2 weeks

---

## Part 3: Simulated Testing Strategy

Based on [TESTING_WITHOUT_HARDWARE.md](../next_up/TESTING_WITHOUT_HARDWARE.md), here's the implementation plan:

### Stage 1: Local Testing (Current ✅)

**What We Have:**
- pytest with 619 tests
- Coverage reporting
- Mock-based unit tests
- Integration tests against live WATS server

**Confidence Level:** 🟢 95% for Python code

### Stage 2: CI/CD Matrix Testing (Mostly Complete ✅)

**Current `.github/workflows/test-platforms.yml`:**
| Platform | Python Versions | Status |
|----------|-----------------|--------|
| Ubuntu 22.04 | 3.10, 3.11, 3.12 | ✅ Active |
| Ubuntu 24.04 | 3.11, 3.12 | ✅ Active |
| Windows Latest | 3.10, 3.11, 3.12 | ✅ Active |
| macOS Latest | 3.11, 3.12 | ✅ Active |
| Rocky Linux 9 | 3.11 | ✅ Active (container) |

**Gaps:**
- [ ] RHEL 8 testing (different Python ecosystem)
- [ ] Windows Server testing (currently uses Windows Latest)
- [ ] Actual service installation tests (currently skipped)

### Stage 3: Package Build Validation (Partial ⚠️)

**Current:**
- ✅ Shell script linting (shellcheck)
- ✅ DEB control file validation
- ✅ RPM spec linting (in container)
- ✅ Systemd unit syntax validation
- ✅ SELinux policy compilation

**Gaps:**
- [ ] Actual DEB package build in CI
- [ ] Actual RPM package build in CI
- [ ] Package installation testing in clean VMs
- [ ] MSI build (blocked - no MSI infrastructure yet)

### Stage 4: Docker Validation (Complete ✅)

**Current:**
- ✅ Native arch build and test
- ✅ ARM64 build via QEMU emulation
- ✅ Health endpoint validation
- ✅ Import verification

### Stage 5: Enhanced Testing (TO IMPLEMENT)

#### 5.1 Add Package Build Jobs

```yaml
# Add to test-platforms.yml
build-deb:
  name: Build DEB Package
  runs-on: ubuntu-22.04
  steps:
    - uses: actions/checkout@v4
    - name: Install build dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y devscripts debhelper dh-python python3-all
    
    - name: Build DEB package
      run: |
        cd deployment/debian
        dpkg-buildpackage -b -uc -us
    
    - name: Test DEB installation
      run: |
        sudo dpkg -i ../pywats-client_*.deb || sudo apt-get -f install -y
        systemctl status pywats-client || true
        python3 -c "import pywats; print('DEB install OK')"
    
    - name: Upload DEB artifact
      uses: actions/upload-artifact@v4
      with:
        name: deb-package
        path: ../*.deb

build-rpm:
  name: Build RPM Package
  runs-on: ubuntu-latest
  container: rockylinux:9
  steps:
    - uses: actions/checkout@v4
    - name: Install build dependencies
      run: |
        dnf install -y rpm-build python3-devel python3-setuptools
    
    - name: Build RPM package
      run: |
        rpmbuild -bb deployment/rpm/pywats.spec
    
    - name: Test RPM installation
      run: |
        rpm -ivh ~/rpmbuild/RPMS/noarch/pywats-client-*.rpm
        systemctl status pywats-client || true
```

#### 5.2 Add Service Integration Tests

```yaml
test-systemd-integration:
  name: Test systemd Integration
  runs-on: ubuntu-22.04
  steps:
    - uses: actions/checkout@v4
    - name: Setup Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install pyWATS
      run: pip install -e ".[client-headless]"
    
    - name: Install systemd unit
      run: |
        sudo cp deployment/debian/pywats-client.service /etc/systemd/system/
        sudo systemctl daemon-reload
    
    - name: Create config
      run: |
        sudo mkdir -p /etc/pywats
        echo '{"server": {"url": "https://demo.wats.com"}}' | sudo tee /etc/pywats/config.json
    
    - name: Start service
      run: |
        sudo systemctl start pywats-client
        sleep 5
        sudo systemctl status pywats-client
    
    - name: Test health endpoint
      run: |
        curl -f http://localhost:8080/health || echo "Health check (expected if no WATS token)"
    
    - name: Check logs
      run: |
        sudo journalctl -u pywats-client --no-pager -n 50
```

#### 5.3 Add Windows Service Test

```yaml
test-windows-service:
  name: Test Windows Service
  runs-on: windows-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install pyWATS with service support
      run: pip install -e ".[client]"
    
    - name: Test service installation (dry-run)
      run: |
        python -m pywats_client service --help
        # Note: Actual service install requires admin, may not work in CI
      shell: pwsh
```

---

## Part 4: Implementation Roadmap

### Phase 1: CI/CD Hardening (Week 1)
**Goal:** Ensure all existing packages are automatically built and tested

- [ ] Add DEB package build job to CI
- [ ] Add RPM package build job to CI
- [ ] Add systemd integration test
- [ ] Add Windows service dry-run test
- [ ] Publish build artifacts to GitHub Releases

### Phase 2: Windows MSI Installer (Weeks 2-4)
**Goal:** Enterprise-ready Windows installer

- [ ] Set up cx_Freeze build environment
- [ ] Create WiX project for MSI packaging
- [ ] Implement silent install support
- [ ] Add service registration to installer
- [ ] Set up code signing (Authenticode)
- [ ] Add MSI build to CI/CD
- [ ] Test GPO deployment in lab

### Phase 3: macOS Installer (Weeks 5-6)
**Goal:** macOS-native distribution

- [ ] Set up py2app build
- [ ] Create .app bundle
- [ ] Set up code signing (Developer ID)
- [ ] Create DMG with installer
- [ ] Set up notarization pipeline
- [ ] Add to CI/CD (macOS runner)

### Phase 4: Standalone Executables (Week 7)
**Goal:** Zero-dependency binaries

- [ ] Create PyInstaller spec files
- [ ] Build Windows .exe
- [ ] Build Linux AppImage
- [ ] Build macOS .app (separate from PKG)
- [ ] Add to release artifacts

### Phase 5: Beta Customer Program (Weeks 8-10)
**Goal:** Real-world validation

- [ ] Identify 2-3 customers per platform
- [ ] Provide pre-release packages
- [ ] Collect installation logs
- [ ] Document common issues
- [ ] Create FAQ/troubleshooting guide
- [ ] Refine packages based on feedback

---

## Part 5: Testing Confidence Matrix

### Without Hardware (Simulated)

| Test Category | Approach | Confidence | Gap |
|---------------|----------|------------|-----|
| Python code logic | pytest, mocking | 🟢 95% | None |
| API integration | Live WATS tests | 🟢 95% | Rate limiting |
| Package structure | Linting, syntax | 🟢 90% | Runtime deps |
| DEB package | Build in CI | 🟡 75% | Install testing |
| RPM package | Build in CI | 🟡 75% | Install testing |
| SELinux policy | Compile check | 🟡 60% | AVC denials |
| systemd units | Syntax + start | 🟡 80% | Real boot |
| Windows Service | Dry-run only | 🟡 70% | Admin install |
| Docker images | QEMU emulation | 🟢 85% | Real ARM |
| MSI installer | Not yet | ❌ 0% | Not built |
| macOS PKG | Not yet | ❌ 0% | Not built |

### With Hardware/Beta (Target)

| Test Category | Approach | Target Confidence |
|---------------|----------|-------------------|
| Windows 10/11 install | Customer beta | 🟢 95% |
| Windows Server | Customer beta | 🟢 95% |
| Windows IoT LTSC | Lab VM + customer | 🟢 90% |
| Ubuntu LTS | CI + customer | 🟢 98% |
| RHEL/Rocky | CI + customer | 🟢 90% |
| Raspberry Pi | Customer beta | 🟡 85% |
| Docker | CI complete | 🟢 95% |

---

## Part 6: Resource Requirements

### Tools & Accounts Needed

| Tool | Purpose | Cost | Status |
|------|---------|------|--------|
| cx_Freeze | Windows bundling | Free (OSS) | Not installed |
| WiX Toolset | MSI creation | Free (OSS) | Not installed |
| Code signing cert | Authenticode | ~$200-500/yr | Needed |
| Apple Developer | macOS signing | $99/yr | Needed |
| py2app | macOS bundling | Free (OSS) | Not installed |
| PyInstaller | Cross-platform | Free (OSS) | Not installed |

### Estimated Total Effort

| Phase | Effort | Priority |
|-------|--------|----------|
| CI/CD Hardening | 1 week | 🔴 Critical |
| Windows MSI | 3 weeks | 🔴 Critical |
| macOS PKG | 2 weeks | 🟡 Medium |
| Standalone Exes | 1 week | 🟢 Nice-to-have |
| Beta Program | 3 weeks | 🔴 Critical |
| **Total** | **10 weeks** | |

---

## Part 7: Immediate Action Items

### This Week

1. **Create `deployment/windows/` folder structure**
   - Initial cx_Freeze configuration
   - WiX project skeleton
   - Build script

2. **Enhance CI/CD**
   - Add DEB build job
   - Add RPM build job  
   - Add artifact upload

3. **Document installer requirements**
   - GPO deployment checklist
   - Silent install parameters
   - Upgrade scenarios

### Next Sprint

1. **Windows MSI prototype**
   - Basic installer that works
   - Service registration
   - Silent install

2. **Set up code signing**
   - Acquire certificate
   - Configure CI/CD

3. **Identify beta customers**
   - Windows enterprise
   - RHEL/SELinux environment
   - Raspberry Pi deployment

---

## Appendix: File References

### Existing Documentation
- [Platform Compatibility](../../platforms/platform-compatibility.md) - Full compatibility matrix
- [Windows IoT LTSC](../../platforms/windows-iot-ltsc.md) - IoT-specific setup
- [Testing Without Hardware](../next_up/TESTING_WITHOUT_HARDWARE.md) - Testing strategy guide
- [Deployment README](../../../deployment/README.md) - Current deployment files

### CI/CD Workflows
- [test-platforms.yml](../../../.github/workflows/test-platforms.yml) - Multi-platform testing
- [docker.yml](../../../.github/workflows/docker.yml) - Docker builds
- [publish.yml](../../../.github/workflows/publish.yml) - PyPI publishing

### Package Files
- [deployment/debian/](../../../deployment/debian/) - DEB packaging
- [deployment/rpm/](../../../deployment/rpm/) - RPM packaging
- [deployment/docker/](../../../deployment/docker/) - Docker files
- [deployment/selinux/](../../../deployment/selinux/) - SELinux policy
