# Implementation Plan: Cross-Platform Service Launcher

**Related Docs:**
- [README](README.md) | [Analysis](01_ANALYSIS.md) | [Progress](03_PROGRESS.md) | [TODO](04_TODO.md)

---

## Overview

Transform pyWATS Client from Qt-dependent service management to cross-platform CLI-based approach with optional GUI components.

**Duration:** 1 week  
**Complexity:** Medium  

---

## Phase 1: ServiceManager Core (Days 1-2)

### Step 1.1: Create ServiceManager Base Class
**File(s):** `src/pywats_client/service_manager.py` (new)  
**Action:**
- Create `ServiceManager` class with platform detection
- Implement `is_running()` using `psutil` to find pywats_client processes
- Implement `get_status()` to return detailed status dict
- Implement `clean_stale_locks()` to remove orphaned lock files

**Code Structure:**
```python
class ServiceManager:
    def __init__(self, instance_id: str = "default"):
        self.instance_id = instance_id
        self.platform = platform.system()
        self.lock_dir = Path(tempfile.gettempdir()) / "pyWATS_Client"
    
    def is_running(self) -> bool:
        """Check if service process is running using psutil"""
    
    def get_status(self) -> dict:
        """Get detailed status: running, pid, uptime, etc."""
    
    def clean_stale_locks(self) -> int:
        """Remove lock files for dead processes, return count cleaned"""
    
    def start(self) -> bool:
        """Start service (platform-specific)"""
    
    def stop(self) -> bool:
        """Stop service (platform-specific)"""
    
    def restart(self) -> bool:
        """Restart service"""
```

**Verification:** Unit tests for process detection and lock cleanup

---

### Step 1.2: Implement Windows Service Start/Stop
**File(s):** `src/pywats_client/service_manager.py`  
**Action:**
- Add `_start_windows()` method
- Try Windows Service (sc start) first, fall back to subprocess
- Add `_stop_windows()` method with graceful shutdown

**Verification:** Manual test on Windows - start/stop works

---

### Step 1.3: Implement Linux Service Start/Stop
**File(s):** `src/pywats_client/service_manager.py`  
**Action:**
- Add `_start_linux()` method
- Try systemctl --user start, fall back to subprocess
- Add `_stop_linux()` method

**Verification:** Manual test on Linux VM - start/stop works

---

### Step 1.4: Implement macOS Service Start/Stop
**File(s):** `src/pywats_client/service_manager.py`  
**Action:**
- Add `_start_macos()` method
- Try launchctl start, fall back to subprocess
- Add `_stop_macos()` method

**Verification:** Manual test on macOS - start/stop works

---

## Phase 2: CLI Commands (Days 2-3)

### Step 2.1: Create CLI Entry Point
**File(s):** `src/pywats_client/cli.py` (new)  
**Action:**
- Create `click`-based CLI with commands: start, stop, restart, status, gui
- Import ServiceManager
- Add --instance-id option for all commands
- Add --verbose flag for debugging

**Code Structure:**
```python
import click
from .service_manager import ServiceManager

@click.group()
@click.option('--instance-id', default='default')
@click.pass_context
def cli(ctx, instance_id):
    """pyWATS Client Service Manager"""
    ctx.obj = ServiceManager(instance_id)

@cli.command()
@click.pass_obj
def start(manager):
    """Start pyWATS Client service"""
    
@cli.command()
@click.pass_obj
def stop(manager):
    """Stop pyWATS Client service"""
```

**Verification:** `pywats-client --help` shows all commands

---

### Step 2.2: Implement 'start' Command
**File(s):** `src/pywats_client/cli.py`  
**Action:**
- Clean stale locks before starting
- Check if already running
- Start service and wait for confirmation
- Print status and log file location

**Verification:** `pywats-client start` successfully starts service

---

### Step 2.3: Implement 'stop' Command
**File(s):** `src/pywats_client/cli.py`  
**Action:**
- Check if running
- Send graceful shutdown signal
- Wait for process to exit (timeout 30s)
- Force kill if timeout exceeded

**Verification:** `pywats-client stop` gracefully stops service

---

### Step 2.4: Implement 'status' and 'restart' Commands
**File(s):** `src/pywats_client/cli.py`  
**Action:**
- `status`: Show running/stopped, PID, uptime, log location
- `restart`: Stop then start with verification

**Verification:** All CLI commands work as expected

---

## Phase 3: Decouple Tray from Service (Day 3-4)

### Step 3.1: Make Tray Icon Optional
**File(s):** 
- `src/pywats_client/service/async_client_service.py`
- `src/pywats_client/__main__.py`

**Action:**
- Add try/except around Qt imports
- Only start tray if `HAS_QT = True` and not headless mode
- Log info message if tray unavailable

**Code Changes:**
```python
# At module level
try:
    from PySide6.QtWidgets import QApplication
    HAS_QT = True
except ImportError:
    HAS_QT = False
    logger.info("Qt not available - tray icon disabled")

# In service startup
if HAS_QT and not self._headless:
    from .service.service_tray import ServiceTrayIcon
    self._tray = ServiceTrayIcon(instance_id)
```

**Verification:** Service starts in headless mode without Qt installed

---

### Step 3.2: Add 'gui' Command to Launch Dashboard
**File(s):** `src/pywats_client/cli.py`  
**Action:**
- Add `gui` command that checks for Qt
- If Qt unavailable, print helpful error message
- If service not running, start it first
- Launch GUI dashboard

**Verification:** `pywats-client gui` launches dashboard (if Qt available)

---

### Step 3.3: Update Tray Icon to Use ServiceManager
**File(s):** `src/pywats_client/service/service_tray.py`  
**Action:**
- Import ServiceManager
- Use ServiceManager for start/stop/restart actions instead of IPC
- More reliable than IPC for service control

**Verification:** Tray icon start/stop buttons work correctly

---

## Phase 4: Testing & Documentation (Days 4-5)

### Step 4.1: Create Unit Tests
**File(s):** `tests/client/test_service_manager.py` (new)  
**Action:**
- Test `is_running()` with mock processes
- Test `clean_stale_locks()` with fake lock files
- Test `get_status()` returns correct format
- Test platform detection

**Verification:** `pytest tests/client/test_service_manager.py -v` - all pass

---

### Step 4.2: Create Integration Tests
**File(s):** `tests/integration/test_cli_commands.py` (new)  
**Action:**
- Test CLI commands with real service
- Test start → status → stop workflow
- Test lock file cleanup on startup
- Test error handling (service already running, etc.)

**Verification:** Integration tests pass on Windows and Linux

---

### Step 4.3: Update Documentation
**File(s):**
- `docs/guides/installation.md` - Add CLI usage
- `docs/getting-started.md` - Update service management section
- `README.md` - Add cross-platform service management feature
- Create `docs/guides/service-management.md` - Comprehensive guide

**Content:**
- Basic usage: `pywats-client start/stop/status`
- Platform-specific notes (systemd, Windows Service, launchd)
- Troubleshooting (stale locks, port conflicts)
- Migration from old approach

**Verification:** Documentation review, links work

---

### Step 4.4: Update pyproject.toml Entry Points
**File(s):** `pyproject.toml`  
**Action:**
- Add `pywats-client` console script entry point
- Ensure `psutil` and `click` in dependencies

```toml
[project.scripts]
pywats-client = "pywats_client.cli:cli"

[project.dependencies]
psutil = ">=5.9.0"
click = ">=8.0.0"
```

**Verification:** After install, `pywats-client` command available globally

---

## Phase 5: Installer Integration (Day 5)

### Step 5.1: Windows Installer Updates
**File(s):** `deployment/windows/installer.iss` (or similar)  
**Action:**
- Create Start Menu shortcut to `pywats-client gui`
- Optional: Desktop shortcut
- Optional: Run at startup registry entry

**Verification:** Fresh install on Windows VM - shortcut works

---

### Step 5.2: Linux Package Updates
**File(s):** `deployment/debian/control`, `deployment/rpm/*.spec`  
**Action:**
- Ensure CLI script packaged
- Update systemd service file if needed

**Verification:** Fresh install on Ubuntu - CLI works

---

### Step 5.3: macOS Package Updates
**File(s):** `deployment/macos/setup_app.py`  
**Action:**
- Include CLI in app bundle
- Update launchd plist if needed

**Verification:** Fresh install on macOS - CLI works

---

## Testing Strategy

### Unit Tests
- `test_service_manager.py` - Core service manager logic
- `test_cli.py` - CLI command parsing and flow
- Mock `psutil` calls, filesystem operations

### Integration Tests
- `test_cli_integration.py` - Real service start/stop/restart
- Test on Windows, Linux, macOS
- Verify lock file cleanup
- Verify process detection

### Manual Tests
1. **Fresh Install:** Install on clean system, verify CLI works
2. **Crash Recovery:** Kill service process, verify lock cleanup on restart
3. **Multi-Instance:** Test with multiple instance IDs
4. **GUI Optional:** Test headless install (no Qt), verify service still works

---

## Rollback Plan

If issues arise:
1. **Keep old service startup** - Don't remove until new approach verified
2. **Feature flag** - Add `USE_NEW_SERVICE_MANAGER=false` env var to disable
3. **Documentation** - Document rollback procedure
4. **Git tag** - Tag release before merging for easy revert

---

## Success Metrics

- ✅ Service starts/stops on all 3 platforms without Qt
- ✅ CLI commands work consistently across platforms
- ✅ Stale lock files automatically cleaned
- ✅ All tests pass (unit + integration)
- ✅ Documentation complete and accurate
- ✅ Zero breaking changes for existing users

---

## Future Enhancements (Out of Scope)

- Auto-update mechanism
- Service health monitoring
- Log rotation via CLI
- Config validation via CLI
- Performance metrics via `pywats-client metrics`

---

**Estimated Total Time:** 5 days (40 hours)  
**Risk Level:** Low-Medium (well-understood problem, straightforward solution)  
**Breaking Changes:** None (additive only)
