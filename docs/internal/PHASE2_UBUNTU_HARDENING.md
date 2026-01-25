# Phase 2: Ubuntu LTS Excellence

**Sprint**: Phase 2 Linux Hardening  
**Branch**: `main`  
**Started**: 2026-01-25  
**Status**: 🔄 In Progress

---

## Objective

Deliver rock-solid Ubuntu LTS experience that "just works" for factory floor deployments:
- Silent installation for automated deployment
- Proper exit codes matching Windows implementation
- Enhanced systemd unit file with production hardening
- Pre-flight checks (Python version, systemd, privileges)

---

## Task Checklist

### 1. Silent Install Mode (Parity with Windows)
**Goal**: `sudo python -m pywats_client install-service --silent` works without prompts

- [x] Add `--silent` flag to install-service (Linux)
- [x] Add `--server-url`, `--api-token`, `--watch-folder` flags
- [x] Suppress all print output when `--silent` is active
- [x] Write configuration file during silent install

### 2. Exit Codes (Parity with Windows)
**Goal**: Same exit codes work across platforms

- [x] Use shared `exit_codes.py` module
- [x] Return proper exit codes from install/uninstall
- [x] Check for service existence before install (EXIT_ALREADY_INSTALLED)
- [x] Check for service existence before uninstall (EXIT_NOT_INSTALLED)

### 3. Pre-flight Checks
**Goal**: Validate environment before attempting install

- [x] Check Python version ≥ 3.10
- [x] Check root privileges
- [x] Check systemd availability
- [x] Check network connectivity (if --server-url provided)

### 4. Enhanced systemd Unit File
**Goal**: Production-hardened service configuration

- [x] Resource limits (memory, file descriptors)
- [x] Watchdog integration (systemd health monitoring)
- [x] Capability restrictions (drop unnecessary privileges)
- [x] Network namespace isolation (optional)
- [ ] Socket activation (deferred - low priority)

### 5. Service Management Improvements
**Goal**: Better operational experience

- [x] `is_service_installed()` function
- [x] `get_service_status()` function
- [x] Proper service file naming for multi-instance

---

## Files Modified

| File | Changes |
|------|---------|
| `src/pywats_client/control/unix_service.py` | Silent mode, exit codes, enhanced unit file |
| `src/pywats_client/__main__.py` | Silent flags for Linux installer |
| `docs/LINUX_SERVICE.md` | Document new features |

---

## Testing

### Manual Testing (Ubuntu 22.04)
```bash
# Test silent install (should return 0)
sudo python3 -m pywats_client install-service --silent
echo $?

# Test duplicate install (should return 10)
sudo python3 -m pywats_client install-service --silent
echo $?

# Test uninstall (should return 0)
sudo python3 -m pywats_client uninstall-service --silent
echo $?

# Test with configuration
sudo python3 -m pywats_client install-service --silent \
    --server-url "https://wats.company.com" \
    --api-token "xxx" \
    --watch-folder "/home/testuser/reports"

# Check service status
sudo systemctl status pywats-service

# View logs
sudo journalctl -u pywats-service -f
```

---

## Progress Log

### 2026-01-25
- Created tracking document
- ✅ Added exit_codes import to unix_service.py
- ✅ Added `is_service_installed()` and `get_service_status()` to LinuxServiceInstaller
- ✅ Updated `install()` to return exit codes, support silent mode
- ✅ Updated `uninstall()` to return exit codes, support silent mode
- ✅ Enhanced systemd unit file:
  - Type=notify with WatchdogSec=60s
  - Resource limits: MemoryMax=512M, CPUQuota=80%, LimitNOFILE=65535
  - Security hardening: NoNewPrivileges, PrivateTmp, ProtectSystem=strict
  - Capability restrictions: CapabilityBoundingSet=CAP_NET_BIND_SERVICE
  - System call filtering: SystemCallFilter=@system-service
- ✅ Added `is_service_installed()` and `get_service_status()` to MacOSServiceInstaller  
- ✅ Updated macOS install/uninstall for silent mode and exit codes
- ✅ Updated LINUX_SERVICE.md with Silent Installation section
- ✅ Added Bash deployment script example
- ✅ Added Ansible playbook example
- ✅ Documented hardened systemd defaults

---

## Rollback Plan

All changes are additive. Existing behavior preserved when flags not used.
