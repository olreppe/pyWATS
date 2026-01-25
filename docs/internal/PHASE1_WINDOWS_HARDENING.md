# Phase 1: Windows Service Hardening

**Sprint**: Phase 1 Quick Wins  
**Branch**: `main`  
**Started**: 2026-01-25  
**Status**: ✅ Complete (Quick Wins)

---

## Objective

Implement production-ready Windows service features that IT departments expect:
- Silent installation for scripted deployments
- Proper exit codes for CI/CD integration
- Service recovery options (auto-restart on failure)
- Pre-flight validation checks

---

## Task Checklist

### 1. Silent Install Mode
**Goal**: `python -m pywats_client install-service --silent` works without prompts

- [x] Add `--silent` flag to install-service command
- [x] Add `--server-url` flag for initial configuration
- [x] Add `--api-token` flag for initial configuration  
- [x] Add `--watch-folder` flag for initial configuration
- [x] Suppress all print output when `--silent` is active
- [x] Write configuration file during silent install

### 2. Exit Codes
**Goal**: Scripted installers can check return code to determine success/failure

| Code | Constant | Meaning |
|------|----------|---------|
| 0 | `EXIT_SUCCESS` | Success |
| 1 | `EXIT_ERROR` | General error |
| 2 | `EXIT_MISSING_REQUIREMENTS` | Python version, privileges, pywin32 |
| 10 | `EXIT_ALREADY_INSTALLED` | Service already exists |
| 11 | `EXIT_NOT_INSTALLED` | Service not found (for uninstall) |
| 14 | `EXIT_PERMISSION_DENIED` | Need Administrator |
| 41 | `EXIT_SERVER_UNREACHABLE` | Server connectivity issue |

- [x] Create `exit_codes.py` module with constants
- [x] Update `install-service` to use exit codes
- [x] Update `uninstall-service` to use exit codes
- [x] Document exit codes in WINDOWS_SERVICE.md

### 3. Pre-flight Checks
**Goal**: Validate environment before attempting install

- [x] Check Python version ≥ 3.10
- [x] Check admin/root privileges
- [x] Check pywin32 availability (if --native)
- [x] Check network connectivity to WATS server (if --server-url provided)
- [ ] Check disk space for logs/queue (optional - deferred)

### 4. Service Recovery (Windows-specific)
**Goal**: Service auto-restarts on crash

- [x] Configure recovery via `sc.exe failure` after install
- [x] First failure: Restart after 5 seconds
- [x] Second failure: Restart after 5 seconds
- [x] Subsequent failures: Restart after 30 seconds
- [x] Reset failure count after 24 hours
- [x] Configure delayed auto-start (starts after network ready)

### 5. Windows Event Log Integration
**Goal**: Service writes to Windows Event Log (Application log)

- [x] Register event source during install
- [x] Log service start/stop to Event Log
- [x] Log errors to Event Log
- [x] Provide `log_event()` helper function for application use
- [ ] Remove event source during uninstall (skipped - may be used by other instances)

---

## Files Modified

| File | Changes |
|------|---------|
| `src/pywats_client/control/exit_codes.py` | NEW - Exit code constants |
| `src/pywats_client/__main__.py` | Silent install, pre-flight checks, exit codes |
| `src/pywats_client/control/windows_native_service.py` | Service recovery, event log |
| `docs/WINDOWS_SERVICE.md` | Document new flags and exit codes |

---

## Testing

### Manual Testing
```powershell
# Test silent install (should return 0)
python -m pywats_client install-service --native --silent
echo $LASTEXITCODE

# Test duplicate install (should return 4)
python -m pywats_client install-service --native --silent
echo $LASTEXITCODE

# Test uninstall (should return 0)
python -m pywats_client uninstall-service --native --silent
echo $LASTEXITCODE

# Test uninstall when not installed (should return 5)
python -m pywats_client uninstall-service --native --silent
echo $LASTEXITCODE

# Test with configuration
python -m pywats_client install-service --native --silent `
    --server-url "https://wats.company.com" `
    --api-token "xxx" `
    --watch-folder "C:\TestReports"
```

### Automated Testing
- [ ] Add unit tests for pre-flight checks
- [ ] Add integration test for silent install/uninstall cycle

---

## Progress Log

### 2026-01-25
- Created tracking document
- ✅ Created `exit_codes.py` module with all exit code constants
- ✅ Added `--silent` flag to install-service and uninstall-service
- ✅ Added `--server-url`, `--api-token`, `--watch-folder` flags for silent install
- ✅ Added `--skip-preflight` flag  
- ✅ Implemented pre-flight checks (Python version, admin privileges, pywin32, server connectivity)
- ✅ Added `is_service_installed()` function for duplicate detection
- ✅ Added `silent` parameter to `install_service()` and `uninstall_service()`
- ✅ Tested exit codes work correctly (EXIT_PERMISSION_DENIED = 14 when not admin)
- ✅ Implemented service recovery (auto-restart on failure via sc.exe failure)
- ✅ Implemented delayed auto-start (starts after network services ready)
- ✅ Added Windows Event Log integration:
  - `register_event_source()` - registers "pyWATS" in Application log
  - `log_event(message, type, id)` - write to Event Log from anywhere
  - Auto-registers during service install
  - Logs install/uninstall events

---

## Rollback Plan

All changes are additive (new flags). Existing behavior preserved when flags not used.
No database migrations or breaking changes.

---

## Next Steps (After This Sprint)

1. ~~Windows IoT LTSC testing~~ (manual testing needed)
2. ~~Service recovery implementation~~ ✅ Done
3. ~~Event Log integration~~ ✅ Done
4. ~~Update documentation~~ ✅ Done

## Remaining Work (Phase 1 Continued)

- [ ] Windows IoT LTSC validation (requires test VM)
- [ ] MSI installer (stretch goal - Phase 1.4)
- [ ] Disk space pre-flight check (low priority)
