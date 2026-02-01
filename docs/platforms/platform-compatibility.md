# Platform Compatibility Guide

> **Last Updated**: February 1, 2026  
> **pyWATS Version**: 0.2.0b1 (Beta)

This document describes the supported platforms, deployment modes, and compatibility considerations for pyWATS.

---

## Quick Compatibility Matrix

| Platform | Library | Client GUI | Client Headless | Service/Daemon |
|----------|---------|------------|-----------------|----------------|
| **Windows 10/11** | ✅ Full | ✅ Full | ✅ Full | ✅ Native Service |
| **Windows Server 2019/2022** | ✅ Full | ⚠️ GUI may require features | ✅ Full | ✅ Native Service |
| **Windows IoT Enterprise LTSC** | ✅ Full | ⚠️ UWF workarounds | ✅ Full | ✅ Native Service |
| **Ubuntu 22.04/24.04 LTS** | ✅ Full | ✅ Full | ✅ Full | ✅ systemd |
| **Debian 11/12** | ✅ Full | ✅ Full | ✅ Full | ✅ systemd |
| **RHEL 8/9** | ✅ Full | ✅ Full | ✅ Full | ✅ systemd + SELinux |
| **Rocky Linux 8/9** | ✅ Full | ✅ Full | ✅ Full | ✅ systemd + SELinux |
| **AlmaLinux 8/9** | ✅ Full | ✅ Full | ✅ Full | ✅ systemd + SELinux |
| **macOS 12+ (Monterey+)** | ✅ Full | ✅ Full | ✅ Full | ✅ launchd |
| **Raspberry Pi OS (64-bit)** | ✅ Full | ⚠️ Qt may be slow | ✅ Recommended | ✅ systemd |
| **Docker** | ✅ Full | ❌ No GUI | ✅ Full | ✅ Container |
| **Kubernetes** | ✅ Full | ❌ No GUI | ✅ Full | ✅ Pod |

**Legend:**
- ✅ **Full** - Fully supported and tested
- ⚠️ **Limited** - Works with noted limitations
- ❌ **No** - Not supported for this platform

---

## Detailed Platform Support

### Windows

#### Windows 10/11 Professional/Enterprise
**Status**: ✅ Primary development platform

| Feature | Support Level |
|---------|---------------|
| pyWATS Library | ✅ Full |
| GUI Client | ✅ Full (Qt6) |
| Headless Client | ✅ Full |
| Windows Service | ✅ Native with pywin32 |
| Pre-shutdown Handling | ✅ SERVICE_CONTROL_PRESHUTDOWN |
| Event Log Integration | ✅ Windows Event Log |
| Auto-start on Boot | ✅ Delayed Auto-Start |
| Auto-recovery on Crash | ✅ Service Recovery Options |

**Requirements:**
- Python 3.10+ (64-bit recommended)
- Visual C++ Redistributable 2019+
- Administrator rights for service installation

**Installation:**
```powershell
pip install pywats-api[client]
pywats-client install-service
```

#### Windows Server 2019/2022
**Status**: ✅ Fully supported

Same as Windows 10/11 with additional notes:
- Server Core: Use headless mode (`pywats-api[client-headless]`)
- Desktop Experience: Full GUI available
- Remote Desktop: GUI works over RDP

#### Windows IoT Enterprise LTSC (2019/2021)
**Status**: ⚠️ Supported with workarounds

**Special Considerations:**
- **Unified Write Filter (UWF)**: Add exclusions for config directories
- **AppLocker**: Create exception rules for Python and pyWATS
- **Windows Defender**: Add exclusions for performance

See [WINDOWS_IOT_LTSC.md](WINDOWS_IOT_LTSC.md) for detailed setup guide.

---

### Linux

#### Ubuntu 22.04/24.04 LTS
**Status**: ✅ Primary Linux platform

| Feature | Support Level |
|---------|---------------|
| pyWATS Library | ✅ Full |
| GUI Client | ✅ Full (Qt6) |
| Headless Client | ✅ Full |
| systemd Service | ✅ Full integration |
| Health Endpoint | ✅ HTTP /health |
| DEB Package | ✅ Available |
| Unattended Install | ✅ dpkg + debconf |

**Requirements:**
- Python 3.10+ (ships with 22.04+)
- libxcb and Qt dependencies for GUI
- systemd for service mode

**Installation (PyPI):**
```bash
sudo apt update
sudo apt install python3-pip python3-venv
pip install pywats-api[client-headless]
```

**Installation (DEB Package):**
```bash
sudo dpkg -i pywats-client_*.deb
sudo systemctl enable pywats-client
sudo systemctl start pywats-client
```

#### Debian 11 (Bullseye) / 12 (Bookworm)
**Status**: ✅ Fully supported

Same as Ubuntu with Debian-specific notes:
- Debian 11: Python 3.9 (upgrade to 3.10+ required)
- Debian 12: Python 3.11 (native support)

#### RHEL 8/9, Rocky Linux 8/9, AlmaLinux 8/9
**Status**: ✅ Fully supported (SELinux-ready)

| Feature | Support Level |
|---------|---------------|
| pyWATS Library | ✅ Full |
| GUI Client | ✅ Full (Qt6) |
| Headless Client | ✅ Full |
| systemd Service | ✅ Full integration |
| SELinux | ✅ Policy module included |
| RPM Package | ✅ Available |
| FIPS Mode | ⚠️ May require OpenSSL config |

**Requirements:**
- Python 3.9+ (RHEL 8) or 3.11+ (RHEL 9)
- EPEL repository for additional dependencies
- SELinux in enforcing mode supported

**Installation (PyPI):**
```bash
sudo dnf install python3 python3-pip
pip install pywats-api[client-headless]
```

**Installation (RPM Package):**
```bash
sudo rpm -i pywats-client-*.rpm
sudo systemctl enable pywats-client
sudo systemctl start pywats-client
```

**SELinux Setup:**
```bash
cd selinux/
sudo ./install-selinux.sh
```

---

### macOS

#### macOS 12+ (Monterey, Ventura, Sonoma, Sequoia)
**Status**: ✅ Fully supported

| Feature | Support Level |
|---------|---------------|
| pyWATS Library | ✅ Full |
| GUI Client | ✅ Full (Qt6) |
| Headless Client | ✅ Full |
| launchd Service | ✅ Full integration |
| Apple Silicon (M1/M2/M3) | ✅ Native ARM64 |
| Intel | ✅ x86_64 |

**Requirements:**
- Python 3.10+ (Homebrew recommended)
- Xcode Command Line Tools
- Code signing for Gatekeeper (optional)

**Installation:**
```bash
brew install python@3.12
pip install pywats-api[client]
```

See [MACOS_SERVICE.md](MACOS_SERVICE.md) for launchd setup.

---

### Embedded / IoT

#### Raspberry Pi 4/5 (64-bit OS)
**Status**: ✅ Recommended for headless

| Feature | Support Level |
|---------|---------------|
| pyWATS Library | ✅ Full |
| GUI Client | ⚠️ Works but slow |
| Headless Client | ✅ Recommended |
| systemd Service | ✅ Full integration |

**Notes:**
- Use 64-bit Raspberry Pi OS
- Headless mode recommended for performance
- 4GB+ RAM recommended for GUI

**Installation:**
```bash
pip install pywats-api[client-headless]
```

See [HEADLESS_GUIDE.md](src/pywats_client/control/HEADLESS_GUIDE.md) for embedded setup.

---

### Containers

#### Docker
**Status**: ✅ Production-ready

| Feature | Support Level |
|---------|---------------|
| pyWATS Library | ✅ Full |
| Headless Client | ✅ Full |
| Multi-arch | ✅ amd64 + arm64 |
| Health Checks | ✅ HTTP /health |
| Security Scanning | ✅ Trivy in CI |

**Images Available:**
- `ghcr.io/olreppe/pywats-api:latest` - API library only
- `ghcr.io/olreppe/pywats-client:latest` - Headless client

**Quick Start:**
```bash
docker run -d \
  -e PYWATS_SERVER_URL=https://your-server.wats.com \
  -e PYWATS_API_TOKEN=your-token \
  -v /reports:/app/reports \
  ghcr.io/olreppe/pywats-client:latest
```

See [DOCKER.md](DOCKER.md) for complete container guide.

#### Kubernetes
**Status**: ✅ Production-ready

- Horizontal Pod Autoscaler support
- Liveness/Readiness probes via /health endpoint
- ConfigMap/Secret for configuration
- Persistent Volume Claims for report storage

---

### Virtual Machine Appliance
**Status**: ✅ Available

Pre-built appliance for easy deployment:

| Format | Use Case |
|--------|----------|
| OVA | VMware ESXi, vSphere, VirtualBox |
| QCOW2 | KVM, Proxmox, OpenStack |
| VHD | Hyper-V, Azure |

**Features:**
- Ubuntu 22.04 LTS base
- pyWATS pre-installed
- First-boot configuration wizard
- Automatic updates via apt

---

## Python Version Support

| Python Version | Support Status |
|---------------|----------------|
| 3.9 | ⚠️ Deprecated (works, not tested) |
| 3.10 | ✅ Minimum supported |
| 3.11 | ✅ Recommended |
| 3.12 | ✅ Full support |
| 3.13 | ⚠️ Untested (expected to work) |

---

## Architecture Support

| Architecture | Library | Client |
|-------------|---------|--------|
| x86_64 (AMD64) | ✅ Full | ✅ Full |
| ARM64 (AArch64) | ✅ Full | ✅ Full |
| ARM32 | ⚠️ Should work | ❌ Not tested |

---

## Network Requirements

### Outbound Connections

| Destination | Port | Protocol | Purpose |
|-------------|------|----------|---------|
| WATS Server | 443 | HTTPS | API communication |
| PyPI | 443 | HTTPS | Package installation |
| GitHub | 443 | HTTPS | Updates (optional) |

### Inbound Connections (Optional)

| Port | Protocol | Purpose |
|------|----------|---------|
| 8080 | HTTP | Health endpoint |
| 8765 | HTTP | Control API (headless) |

### Proxy Support

pyWATS supports HTTP/HTTPS proxies via environment variables:
```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1,.internal.domain
```

---

## Platform-Specific Implementation Details (v0.2.0+)

This section documents platform-specific behaviors for new components introduced in v0.2.0.

### Converter Sandboxing

**Feature**: Process isolation for converter execution with resource limits.

| Platform | Support | Resource Limits | Notes |
|----------|---------|-----------------|-------|
| Linux | ✅ Full | CPU, Memory, File Descriptors, Processes | Uses `resource.setrlimit()` for all limits |
| macOS | ✅ Full | CPU, Memory, File Descriptors, Processes | Uses `resource.setrlimit()` for all limits |
| Windows | ⚠️ Partial | Timeout only | No native `resource` module - only timeout enforced |

**Linux/macOS Details:**
- **CPU Limit**: Uses `RLIMIT_CPU` (hard CPU time limit)
- **Memory Limit**: Uses `RLIMIT_AS` (address space limit)
- **File Descriptors**: Uses `RLIMIT_NOFILE` (max open files)
- **Process Limit**: Uses `RLIMIT_NPROC` (prevents fork bombs)
- **Session Isolation**: `os.setsid()` creates new session

**Windows Details:**
- Resource limits (`setrlimit`) not available on Windows
- Sandbox still provides:
  - ✅ Process isolation (separate subprocess)
  - ✅ Timeout enforcement (kills process after timeout)
  - ✅ Environment variable restrictions
  - ✅ Static code analysis (AST validation)
  - ❌ Memory limits (not enforced)
  - ❌ CPU limits (not enforced)
  - ❌ File descriptor limits (not enforced)

**Fallback Behavior:**
- If `setrlimit()` fails (e.g., permission denied), sandbox logs warning but continues
- Sandboxing is enabled by default on all platforms
- To disable sandboxing for trusted converters: `trusted_mode=True`

**Configuration:**
```python
from pywats_client.converters.sandbox import ResourceLimits, SandboxConfig

# Default limits (work on all platforms)
config = SandboxConfig(
    resource_limits=ResourceLimits(
        timeout_seconds=300,        # ✅ All platforms
        cpu_time_seconds=120,       # ✅ Linux/macOS only
        memory_mb=512,              # ✅ Linux/macOS only
        max_open_files=50,          # ✅ Linux/macOS only
        max_processes=1             # ✅ Linux/macOS only
    )
)
```

**Related Files:**
- [src/pywats_client/converters/sandbox.py](../src/pywats_client/converters/sandbox.py)
- [docs/guides/converter-security.md](../guides/converter-security.md)
- [tests/client/test_sandbox.py](../tests/client/test_sandbox.py)

---

### IPC Communication (Service ↔ GUI)

**Feature**: Inter-process communication for service control.

| Platform | Transport | Address |
|----------|-----------|---------|
| Windows | TCP | `127.0.0.1:<port>` (port derived from instance ID) |
| Linux | Unix Socket | `/tmp/pywats_service_<instance_id>.sock` |
| macOS | Unix Socket | `/tmp/pywats_service_<instance_id>.sock` |

**Transport Selection Logic:**
```python
if sys.platform == "win32":
    # Windows: Use TCP localhost with deterministic port
    port = hash(instance_id) % 50000 + 10000
    await asyncio.start_server(handler, "127.0.0.1", port)
else:
    # Linux/macOS: Use Unix domain socket
    socket_path = f"/tmp/pywats_service_{instance_id}.sock"
    await asyncio.start_unix_server(handler, socket_path)
```

**Why Different Transports?**
- **Unix Sockets** (Linux/macOS):
  - ✅ Faster than TCP (no network stack)
  - ✅ File system permissions for security
  - ✅ Automatic cleanup on process exit
  - ❌ Not available on Windows

- **TCP Localhost** (Windows):
  - ✅ Cross-platform support
  - ✅ Works on all Windows versions
  - ⚠️ Requires firewall rules (localhost-only)
  - ⚠️ Port conflicts possible (mitigated by hash)

**Security:**
- All platforms use shared secret authentication (256-bit tokens)
- Rate limiting: 100 requests/minute per client (configurable)
- Windows: Firewall automatically allows localhost
- Linux/macOS: Socket file has 0600 permissions

**Related Files:**
- [src/pywats_client/service/async_ipc_server.py](../src/pywats_client/service/async_ipc_server.py)
- [src/pywats_client/service/async_ipc_client.py](../src/pywats_client/service/async_ipc_client.py)
- [docs/guides/ipc-security.md](../guides/ipc-security.md)

---

### Instance Management

**Feature**: Multi-instance lock files and PID tracking.

| Platform | Lock File Location | PID File Location |
|----------|-------------------|-------------------|
| Windows | `%TEMP%\pyWATS_Client\instance_<id>.lock` | Same |
| Linux | `/tmp/pywats_client/instance_<id>.lock` | `/var/run/pywats/instance_<id>.pid` (service) |
| macOS | `/tmp/pywats_client/instance_<id>.lock` | `~/Library/Application Support/pyWATS/instance_<id>.pid` |

**Platform-Specific Paths:**
```python
if os.name == 'nt':
    # Windows
    lock_base = Path(os.environ.get('TEMP', '')) / 'pyWATS_Client'
else:
    # Linux/macOS
    lock_base = Path('/tmp') / 'pywats_client'

lock_file = lock_base / f"instance_{instance_id}.lock"
```

**Stale Lock Detection:**
- All platforms: Check if PID in lock file is still running
- Windows: `psutil.pid_exists()` or Windows API
- Linux/macOS: `os.kill(pid, 0)` signal check
- Stale locks are automatically removed on acquisition

**Multi-Instance Support:**
- Each instance identified by unique ID (e.g., "production", "test")
- Lock files prevent duplicate instances
- GUI can discover all running instances

**Related Files:**
- [src/pywats_client/core/instance_manager.py](../src/pywats_client/core/instance_manager.py)

---

### Health Server (Docker/Kubernetes)

**Feature**: HTTP health check endpoint for monitoring.

| Platform | Default Port | Bind Address | Protocol |
|----------|-------------|--------------|----------|
| All | 8080 | 0.0.0.0 | HTTP/1.1 |

**Endpoints:**
- `GET /health` - Basic health (200 OK / 503 Unavailable)
- `GET /health/live` - Liveness probe (process alive?)
- `GET /health/ready` - Readiness probe (accepting work?)
- `GET /health/details` - JSON status details

**Platform Compatibility:**
- ✅ Windows: Works (bind to 0.0.0.0)
- ✅ Linux: Works (bind to 0.0.0.0)
- ✅ macOS: Works (bind to 0.0.0.0)
- ✅ Docker: Full support (HEALTHCHECK)
- ✅ Kubernetes: Full support (livenessProbe/readinessProbe)

**Docker Example:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD curl -f http://localhost:8080/health || exit 1
```

**Kubernetes Example:**
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 30
```

**Related Files:**
- [src/pywats_client/service/health_server.py](../src/pywats_client/service/health_server.py)

---

### Security & Encryption

**Feature**: Secret storage and file encryption.

| Component | Windows | Linux | macOS |
|-----------|---------|-------|-------|
| Secret Storage | Windows Credential Manager (DPAPI) | `~/.config/pywats/secrets/` (0600) | Keychain or file |
| IPC Auth Secret | `%LOCALAPPDATA%\pyWATS\secrets\` | `~/.config/pywats/secrets/` | `~/Library/Application Support/pyWATS/secrets/` |
| File Locking | Windows file handles | `fcntl.flock()` | `fcntl.flock()` |

**Windows Specifics:**
- Uses Data Protection API (DPAPI) when available
- Falls back to file-based storage with ACLs
- Credential Manager integration for tokens

**Linux Specifics:**
- File-based secrets with 0600 permissions
- Optional: Integration with system keyring (gnome-keyring, kwallet)
- SELinux context: `pywats_secrets_t`

**macOS Specifics:**
- Prefers macOS Keychain
- Falls back to file-based storage

**Related Files:**
- [src/pywats_client/core/security.py](../src/pywats_client/core/security.py)
- [src/pywats_client/core/encryption.py](../src/pywats_client/core/encryption.py)
- [src/pywats_client/core/file_utils.py](../src/pywats_client/core/file_utils.py)

---

## WATS Server Compatibility

| WATS Server Version | pyWATS Support |
|--------------------|----------------|
| < 2025.3.9.824 | ❌ Not supported |
| 2025.3.9.824+ | ✅ Full support |
| 2026.x | ✅ Full support |

---

## Related Documentation

- [Installation Guide](INSTALLATION.md) - Detailed installation instructions
- [Getting Started](GETTING_STARTED.md) - Quick start tutorial
- [Docker Guide](DOCKER.md) - Container deployment
- [Windows IoT LTSC](WINDOWS_IOT_LTSC.md) - IoT-specific guidance
- [Linux Service](LINUX_SERVICE.md) - systemd configuration
- [macOS Service](MACOS_SERVICE.md) - launchd configuration
- [Headless Guide](src/pywats_client/control/HEADLESS_GUIDE.md) - Embedded/server deployment
- [IPC Security Guide](../guides/ipc-security.md) - IPC authentication and rate limiting
- [Converter Security Guide](../guides/converter-security.md) - Sandboxing explained
- [Safe File Handling Guide](../guides/safe-file-handling.md) - Atomic file operations
