# Target Platform Implementation Plan

**Document**: pyWATS Client Deployment Roadmap  
**Objective**: Out-of-the-box installation for non-technical factory floor users  
**Reference**: `target_platforms_for_non_technical_out_of_the_box_installation.md`

---

## Executive Summary

This plan maps the pyWATS client's current implementation against target platform requirements and provides actionable phases for achieving **"install once, run forever"** deployment quality.

### Current Implementation Status

| Platform | Status | Gap Level | Notes |
|----------|--------|-----------|-------|
| Windows Server 2019/2022 | 🟡 Partial | Medium | Native service works, needs hardening |
| Windows IoT LTSC | 🟡 Partial | Medium | Untested, likely works |
| Ubuntu LTS | 🟢 Good | Low | systemd support exists |
| Debian Stable | 🟢 Good | Low | Same as Ubuntu (systemd) |
| RHEL/Rocky/Alma | 🟠 Basic | Medium | systemd works, needs RPM |
| VM Appliance | 🔴 Missing | High | No pre-built images |
| Docker | 🟢 Good | Low | Multi-stage Dockerfile exists |

---

## Phase 1: Windows Server & IoT Hardening (Priority 1)

**Goal**: First-class Windows service experience that IT departments trust

### 1.1 Windows Native Service Improvements

**Current State**: `windows_native_service.py` using pywin32  
**Gap**: Needs production hardening for enterprise environments

#### Tasks

- [ ] **Service recovery options** - Auto-restart on failure
  ```python
  # Add to windows_native_service.py
  def configure_service_recovery(service_name: str):
      """Configure service to auto-restart on failure."""
      # sc.exe failure pyWATS_Service reset= 86400 actions= restart/5000/restart/5000/restart/5000
  ```

- [ ] **Event Log integration** - Write to Windows Event Log, not just files
  ```python
  # Add Windows Event Log handler alongside file logging
  import win32evtlogutil
  win32evtlogutil.ReportEvent(...)
  ```

- [ ] **Service account support** - Run as `NT SERVICE\pyWATS` or dedicated service account
  ```python
  # Allow --service-account flag during install
  python -m pywats_client install-service --service-account "NT SERVICE\pyWATS"
  ```

- [ ] **Delayed auto-start** - Start after network services are ready
  ```python
  # Set SERVICE_DELAYED_AUTO_START in service config
  ```

- [ ] **Pre-shutdown notification** - Clean shutdown on Windows restart
  ```python
  # Handle SERVICE_CONTROL_PRESHUTDOWN for graceful cleanup
  ```

### 1.2 Silent/Unattended Installation

**Current State**: Interactive `python -m pywats_client install-service`  
**Gap**: IT departments need silent installs for deployment scripts

#### Tasks

- [ ] **Silent install mode** - No prompts, all config via flags/env vars
  ```powershell
  # Target usage for IT deployment scripts
  python -m pywats_client install-service `
      --silent `
      --server-url "https://wats.company.com" `
      --api-token "$env:WATS_TOKEN" `
      --watch-folder "C:\TestReports"
  ```

- [ ] **Exit codes** - Proper return codes for scripted deployment
  | Code | Meaning |
  |------|---------|
  | 0 | Success |
  | 1 | General error |
  | 2 | Missing requirements (Python version, privileges) |
  | 3 | Configuration error |
  | 4 | Service already installed |

- [ ] **Pre-flight checks** - Validate before attempting install
  - Python version ≥ 3.10
  - Admin privileges
  - Network connectivity to WATS server
  - Disk space for logs/queue

### 1.3 Windows IoT Enterprise LTSC Testing

**Current State**: Untested  
**Gap**: IoT LTSC has restrictions not present in standard Windows

#### Tasks

- [ ] **Create IoT LTSC test VM** - Windows 10 IoT Enterprise LTSC 2021
- [ ] **Test restrictions**:
  - Limited shell access
  - Restricted PowerShell execution policies
  - UWP vs Win32 application sandboxing
  - Long-term servicing channel update behavior
- [ ] **Document workarounds** - Any IoT-specific installation notes
- [ ] **Validate service persistence** - Service survives restricted updates

### 1.4 MSI Installer (Future)

**Current State**: pip install only  
**Gap**: IT departments prefer MSI for GPO deployment

#### Tasks (Stretch Goal)

- [ ] **Evaluate cx_Freeze or PyInstaller** - Bundle Python + pyWATS
- [ ] **WiX Toolset or NSIS** - Create MSI/MSIX package
- [ ] **Upgrade handling** - Clean upgrade path without data loss
- [ ] **Uninstall cleanup** - Remove service, config, logs (optional)

---

## Phase 2: Ubuntu LTS Excellence (Priority 2)

**Goal**: The best Linux experience starts with Ubuntu

### 2.1 Current systemd Implementation Review

**Current State**: `unix_service.py` → `LinuxServiceInstaller`  
**Gap**: Good foundation, needs polish

#### Current Capabilities ✅
- systemd unit file generation
- Security hardening (NoNewPrivileges, PrivateTmp, ProtectSystem)
- User-level service support
- Multi-instance support
- journalctl integration

#### Tasks

- [ ] **Verify security hardening** - Test `ProtectSystem=strict` doesn't break functionality
- [ ] **Add socket activation** (optional) - Start on-demand via systemd socket
- [ ] **Test upgrade path** - Reinstall over existing service cleanly
- [ ] **Validate after reboot** - Service starts automatically, no manual intervention

### 2.2 DEB Package Creation

**Current State**: pip install only  
**Gap**: Ubuntu shops want `.deb` packages for apt management

#### Tasks

- [ ] **Create debian/ packaging structure**
  ```
  debian/
  ├── control          # Package metadata
  ├── rules            # Build instructions
  ├── postinst         # Post-install script (creates service)
  ├── prerm            # Pre-remove script (stops service)
  ├── postrm           # Post-remove script (cleanup)
  └── pywats.service   # systemd unit file
  ```

- [ ] **Package dependencies**
  ```
  Depends: python3 (>= 3.10), python3-pip
  Recommends: python3-pyside6
  ```

- [ ] **Build with stdeb or debhelper**
  ```bash
  # Option 1: stdeb (Python-native)
  python setup.py --command-packages=stdeb.command bdist_deb
  
  # Option 2: debhelper (traditional)
  dpkg-buildpackage -us -uc
  ```

- [ ] **Repository hosting** - Consider GitHub Releases or PPA

### 2.3 Headless Mode Validation

**Current State**: `pywats-api[client-headless]` extra  
**Gap**: Needs thorough testing on minimal systems

#### Tasks

- [ ] **Test on Ubuntu Server (no desktop)** - Verify no GUI dependencies leak
- [ ] **Test on Raspberry Pi OS** - ARM64 Linux is common in edge gateways
- [ ] **Memory profiling** - Ensure headless mode is truly lightweight
- [ ] **Signal handling** - Clean shutdown on SIGTERM/SIGINT

---

## Phase 3: Debian & Enterprise Linux (Priority 3)

### 3.1 Debian Stable

**Current State**: Should work (same as Ubuntu)  
**Gap**: Untested, may have older Python

#### Tasks

- [ ] **Test on Debian 11 (Bullseye)** - Python 3.9 default (may need backport)
- [ ] **Test on Debian 12 (Bookworm)** - Python 3.11 default ✅
- [ ] **Document Python version requirements** - Clear guidance for Debian 11 users

### 3.2 RHEL / Rocky Linux / AlmaLinux

**Current State**: systemd works, no RPM package  
**Gap**: Enterprise customers expect RPM

#### Tasks

- [ ] **Create RPM spec file**
  ```
  pywats.spec
  ├── %prep     # Prepare sources
  ├── %build    # Build (pip wheel)
  ├── %install  # Install to BUILDROOT
  ├── %post     # Post-install (enable service)
  ├── %preun    # Pre-uninstall (stop service)
  └── %files    # Package contents
  ```

- [ ] **Test on RHEL 8** - Python 3.8 (may need newer Python)
- [ ] **Test on RHEL 9** - Python 3.9/3.11 available
- [ ] **SELinux compatibility** - Test with enforcing mode
- [ ] **Consider COPR for package hosting** - Fedora's community package repo

---

## Phase 4: Deployment Multipliers (Priority 4)

### 4.1 Docker Improvements

**Current State**: Multi-stage Dockerfile, headless client stage  
**Gap**: Good for developers, needs production polish

#### Current Dockerfile Structure ✅
```dockerfile
# Stage: base        → Common dependencies
# Stage: api         → Minimal API library
# Stage: client-headless → Full headless client (default)
# Stage: dev         → Development with all extras
```

#### Tasks

- [ ] **Add health check endpoint** - HTTP health check for orchestrators
  ```dockerfile
  HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8080/health || exit 1
  ```

- [ ] **Document docker-compose.yml** - Production-ready example
  ```yaml
  services:
    pywats:
      image: virinco/pywats-client:latest
      volumes:
        - ./config:/app/config
        - ./reports:/app/watch
      environment:
        - PYWATS_SERVER_URL=https://wats.company.com
        - PYWATS_API_TOKEN=${WATS_TOKEN}
      restart: unless-stopped
  ```

- [ ] **Multi-arch builds** - linux/amd64 + linux/arm64
- [ ] **Container registry** - Push to Docker Hub or GitHub Container Registry

### 4.2 VM Appliance

**Current State**: None  
**Gap**: IT departments want "import OVA, configure IP, done"

#### Tasks

- [ ] **Choose base OS** - Ubuntu Server 22.04 LTS (minimal cloud image)
- [ ] **Automation tooling** - Packer for reproducible builds
- [ ] **First-boot configuration**
  - Network configuration wizard
  - WATS server URL / API token input
  - Watch folder configuration
- [ ] **Export formats**
  - OVA (VMware, VirtualBox)
  - QCOW2 (KVM/QEMU)
  - VHD (Hyper-V)

#### Stretch Goal
- [ ] **Cloud marketplace images** - AWS AMI, Azure VM image

---

## Implementation Timeline

```
┌─────────────────────────────────────────────────────────────────────┐
│ Phase 1: Windows Hardening                          (Weeks 1-4)    │
├─────────────────────────────────────────────────────────────────────┤
│ • Service recovery + Event Log integration          [Week 1-2]     │
│ • Silent install + exit codes                       [Week 2]       │
│ • Windows IoT LTSC testing                          [Week 3]       │
│ • Documentation updates                             [Week 4]       │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 2: Ubuntu LTS Excellence                      (Weeks 5-7)    │
├─────────────────────────────────────────────────────────────────────┤
│ • systemd hardening review                          [Week 5]       │
│ • DEB package creation                              [Week 5-6]     │
│ • Headless mode testing (Server + Pi)               [Week 6-7]     │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 3: Enterprise Linux                           (Weeks 8-10)   │
├─────────────────────────────────────────────────────────────────────┤
│ • Debian testing                                    [Week 8]       │
│ • RPM package creation                              [Week 8-9]     │
│ • RHEL/Rocky testing + SELinux                      [Week 9-10]    │
├─────────────────────────────────────────────────────────────────────┤
│ Phase 4: Deployment Multipliers                     (Weeks 11-14)  │
├─────────────────────────────────────────────────────────────────────┤
│ • Docker production polish                          [Week 11]      │
│ • VM appliance (Packer + cloud-init)                [Week 12-13]   │
│ • Multi-arch container builds                       [Week 14]      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Success Criteria

### Windows Server / IoT LTSC
- [ ] Service appears in Services.msc and Task Manager
- [ ] Service survives Windows Update restarts
- [ ] IT can deploy via GPO/SCCM with silent install
- [ ] Event Log shows meaningful entries (not just file logs)

### Ubuntu / Debian
- [ ] `apt install pywats-client` works (from hosted repo)
- [ ] Service auto-starts after reboot
- [ ] `journalctl -u pywats` shows logs
- [ ] Clean uninstall removes service but preserves config (optional)

### RHEL / Rocky
- [ ] `dnf install pywats-client` works (from COPR or internal repo)
- [ ] SELinux in enforcing mode doesn't break functionality
- [ ] Passes enterprise security scanning

### Docker
- [ ] `docker run -d virinco/pywats-client` works with bind mounts
- [ ] Health check endpoint responds
- [ ] Graceful shutdown on `docker stop`

### VM Appliance
- [ ] Import OVA → Configure IP → Configure WATS → Running in <15 minutes
- [ ] No SSH/command-line required for basic setup
- [ ] Survives hypervisor snapshot/restore

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| pywin32 version incompatibility | Pin version, test on Windows Server 2019/2022 |
| Python 3.10+ not available on older RHEL | Document pyenv/deadsnakes installation |
| PySide6 issues on locked-down systems | Ensure headless mode has zero GUI dependencies |
| SELinux policy denials | Create custom SELinux module if needed |
| Container registry costs | Start with GitHub Container Registry (free for public) |

---

## Dependency Analysis by Platform

### Windows Server 2019/2022

#### Python Runtime
| Requirement | Details | Risk |
|-------------|---------|------|
| Python ≥3.10 | Must install from python.org or Microsoft Store | 🟡 Medium |
| PATH configuration | May conflict with existing Python installations | 🟡 Medium |
| Virtual environments | Recommended to isolate from system Python | 🟢 Low |

**Python Sources:**
- ✅ python.org installer (recommended)
- ✅ Microsoft Store (easy, auto-updates)
- ⚠️ winget (`winget install Python.Python.3.11`)
- ❌ Chocolatey (avoid - inconsistent PATH handling)

#### Core Dependencies
```
httpx[http2]>=0.24.0    → Pure Python, no issues
pydantic>=2.0.0         → Pure Python, no issues  
watchdog>=3.0.0         → Uses ReadDirectoryChangesW on Windows ✅
aiofiles>=23.0.0        → Pure Python, no issues
```

#### Windows-Specific Dependencies
```
pywin32>=306            → CRITICAL for native service
```

**pywin32 Known Issues:**
| Issue | Description | Mitigation |
|-------|-------------|------------|
| Version mismatch | pywin32 version must match Python version exactly | Pin `pywin32>=306` (supports 3.10-3.13) |
| Missing DLLs | `pywintypes3X.dll` not found after pip install | Run `python Scripts/pywin32_postinstall.py -install` |
| Service registration | Requires admin privileges | Document elevation requirement |
| 32-bit vs 64-bit | Must match Python bitness | Always use 64-bit Python on Server |

**Post-install script requirement:**
```powershell
# Required after pip install on some systems
python -c "import win32serviceutil"  # Test if working
# If ImportError, run:
python "$env:VIRTUAL_ENV\Scripts\pywin32_postinstall.py" -install
```

#### GUI Dependencies (if using `client` extra)
```
PySide6>=6.4.0          → 300MB+ download, Qt runtime
```

**PySide6 on Windows Server:**
| Issue | Description | Mitigation |
|-------|-------------|------------|
| No Desktop Experience | Server Core lacks GUI subsystem | Use `client-headless` extra only |
| Missing VC++ Runtime | Qt requires Visual C++ Redistributable | Include VC++ 2019 in install docs |
| RDP rendering | GUI works over RDP but may be slow | Not relevant for headless service |

---

### Windows 10/11 IoT Enterprise LTSC

#### Unique Constraints
| Constraint | Impact | Workaround |
|------------|--------|------------|
| Locked-down shell | May not have PowerShell unrestricted | Use `cmd.exe` fallback for install |
| No Microsoft Store | Can't use Store Python | Must use python.org installer |
| AppLocker policies | May block unsigned executables | Document AppLocker exceptions |
| Windows Defender | May quarantine pywin32 DLLs | Document exclusion paths |
| LTSC update model | No feature updates for 10 years | Good for stability, but may have old bugs |

#### Python Installation on IoT LTSC
```powershell
# LTSC may have restricted execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# If Microsoft Store blocked, use direct installer
# Download: https://www.python.org/ftp/python/3.11.x/python-3.11.x-amd64.exe
# Silent install:
python-3.11.x-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
```

#### IoT-Specific Issues
| Issue | Symptom | Solution |
|-------|---------|----------|
| Write Filter (FBWF/UWF) | Changes lost on reboot | Disable filter during install, or install to unfiltered volume |
| Embedded Lockdown Manager | Apps blocked from running | Add pyWATS to allowed list |
| Limited disk space | Typical IoT has 32-64GB SSD | Use `client-headless` (no PySide6) |
| No .NET Framework | Some pywin32 features need .NET | Core service functionality works without |

---

### Ubuntu LTS (20.04 / 22.04 / 24.04)

#### Python Availability
| Ubuntu Version | Default Python | Status |
|----------------|----------------|--------|
| 20.04 (Focal) | Python 3.8 | ❌ Too old, need deadsnakes PPA |
| 22.04 (Jammy) | Python 3.10 | ✅ Meets requirement |
| 24.04 (Noble) | Python 3.12 | ✅ Meets requirement |

**For Ubuntu 20.04:**
```bash
# Add deadsnakes PPA for Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

#### System Dependencies
```bash
# Required for httpx HTTP/2 support
sudo apt install libssl-dev

# Required for watchdog inotify backend
# (usually pre-installed, but verify)
sudo apt install python3-dev

# For GUI (PySide6) - NOT needed for headless
sudo apt install \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    libegl1 \
    libxcb-cursor0
```

#### Known Issues
| Issue | Description | Mitigation |
|-------|-------------|------------|
| PySide6 xcb plugin | `qt.qpa.plugin: Could not load the Qt platform plugin "xcb"` | Install `libxcb-*` packages, or use headless |
| inotify watch limit | Default 8192 watches may be low for large watch folders | Increase via `fs.inotify.max_user_watches` |
| pip externally-managed | Ubuntu 24.04 restricts pip in system Python | Use `python3 -m venv` always |
| systemd user session | User services don't start at boot without `loginctl enable-linger` | Use system-wide service instead |

**inotify tuning for large deployments:**
```bash
# /etc/sysctl.d/60-pywats.conf
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 512
```

---

### Debian Stable (11 Bullseye / 12 Bookworm)

#### Python Availability
| Debian Version | Default Python | Status |
|----------------|----------------|--------|
| 11 (Bullseye) | Python 3.9 | ❌ Too old, need backport |
| 12 (Bookworm) | Python 3.11 | ✅ Meets requirement |

**For Debian 11:**
```bash
# Option 1: Use pyenv (recommended)
curl https://pyenv.run | bash
pyenv install 3.11.7
pyenv global 3.11.7

# Option 2: Build from source (not recommended for production)
```

#### Debian-Specific Issues
| Issue | Description | Mitigation |
|-------|-------------|------------|
| Older packages | Debian stable = conservative versions | Use pip in venv, not apt |
| Missing wheel | `pip install` compiles from source | `pip install wheel` first |
| Minimal installs | Server installs missing common tools | Install `build-essential` if compilation needed |

---

### RHEL / Rocky Linux / AlmaLinux

#### Python Availability
| RHEL Version | Default Python | Status |
|--------------|----------------|--------|
| RHEL 8 | Python 3.8 (appstream) | ❌ Too old |
| RHEL 8 | Python 3.11 (appstream module) | ✅ `dnf module enable python311` |
| RHEL 9 | Python 3.9 (default) | ❌ Too old |
| RHEL 9 | Python 3.11 (appstream) | ✅ `dnf install python3.11` |

**Enable Python 3.11 on RHEL 8:**
```bash
sudo dnf module reset python3
sudo dnf module enable python311
sudo dnf install python3.11 python3.11-pip python3.11-devel
```

#### SELinux Considerations
| Context | Default Policy | pyWATS Needs |
|---------|----------------|--------------|
| File watching | OK | Read access to watch folders |
| Network access | OK | Outbound HTTPS to WATS server |
| Service files | httpd_sys_content_t | May need custom context |
| Log files | var_log_t | `/var/log/pywats/` needs correct context |

**SELinux troubleshooting:**
```bash
# Check for denials
sudo ausearch -m avc -ts recent

# Generate policy module from denials
sudo ausearch -m avc -ts recent | audit2allow -M pywats
sudo semodule -i pywats.pp

# Or set permissive for pywats (not recommended for production)
# sudo semanage permissive -a pywats_t
```

#### FIPS Mode
| Requirement | Impact |
|-------------|--------|
| FIPS 140-2 mode | May affect SSL/TLS libraries |
| Approved algorithms | httpx uses standard OpenSSL, should be OK |
| Validation | Test on FIPS-enabled system before deployment |

---

### Docker (Linux)

#### Base Image Options
| Image | Size | Python | Recommendation |
|-------|------|--------|----------------|
| `python:3.11-slim` | ~150MB | 3.11 | ✅ Current choice |
| `python:3.11-alpine` | ~50MB | 3.11 | ⚠️ musl libc issues with some packages |
| `python:3.11` | ~900MB | 3.11 | ❌ Too large |
| `ubuntu:22.04` | ~80MB | None | Need to install Python |

**Alpine Issues:**
```
# These packages may fail on Alpine due to musl vs glibc:
# - watchdog (C extension)
# - cryptography (used by httpx for HTTP/2)
# Stick with -slim images
```

#### Container-Specific Dependencies
```dockerfile
# Required in slim image for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
```

#### Volume Mounts
| Mount | Purpose | Permission Issue |
|-------|---------|------------------|
| `/app/config` | Configuration files | UID/GID must match host |
| `/app/watch` | Report watch folder | May need `:z` on SELinux hosts |
| `/app/logs` | Log files | Container user needs write access |

**Permission fix for rootless containers:**
```yaml
services:
  pywats:
    user: "1000:1000"  # Match host user
    volumes:
      - ./config:/app/config:z  # :z for SELinux relabeling
```

---

### VM Appliance (OVA)

#### Base OS Recommendation
| Option | Pros | Cons |
|--------|------|------|
| Ubuntu Server 22.04 | Best Python support, easy updates | Larger image |
| Debian 12 minimal | Smaller, stable | Manual Python setup |
| Alpine Linux | Tiny (~50MB) | Package compatibility issues |

**Recommended: Ubuntu Server 22.04 LTS minimal cloud image**

#### First-Boot Configuration
| Component | Technology |
|-----------|------------|
| Network config | cloud-init or netplan |
| Service setup | systemd unit (pre-installed) |
| Config wizard | Simple curses TUI or web config page |

#### Hypervisor Compatibility
| Format | Hypervisor | Notes |
|--------|------------|-------|
| OVA | VMware, VirtualBox | Universal, largest compatibility |
| QCOW2 | KVM, Proxmox | Thin provisioning support |
| VHD/VHDX | Hyper-V | Required for Windows Server hosts |
| VMDK | VMware | Native format, best performance |

---

## Quick Wins (Can Start Immediately)

1. **Silent install flag** - Add `--silent` to `install-service` command
2. **Exit codes** - Return proper codes from CLI commands
3. **Windows IoT test** - Spin up LTSC VM and run existing installer
4. **Docker health endpoint** - Add simple HTTP health check to headless client

---

## Related Documentation

- [CLIENT_GAP_ANALYSIS.md](CLIENT_GAP_ANALYSIS.md) - C# vs Python implementation gaps
- [WINDOWS_SERVICE.md](../WINDOWS_SERVICE.md) - Current Windows service documentation
- [LINUX_SERVICE.md](../LINUX_SERVICE.md) - Current Linux service documentation
- [DOCKER.md](../DOCKER.md) - Current Docker documentation

---

*Last Updated*: 2025-01-XX  
*Owner*: pyWATS Development Team
