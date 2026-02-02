# Cross-Platform Service Launcher

**Created:** February 2, 2026  
**Status:** 🚧 In Progress  
**Priority:** HIGH

---

## Quick Links
- [Analysis](01_ANALYSIS.md)
- [Implementation Plan](02_IMPLEMENTATION_PLAN.md)
- [Progress Tracker](03_PROGRESS.md)
- [TODO List](04_TODO.md)

---

## Objective

Make pyWATS Client service easy to start, stop, and manage across all platforms (Windows, Linux, macOS) without requiring GUI dependencies or technical knowledge. Eliminate the circular dependency where the tray icon (which requires Qt/GUI) is needed to manage a headless service.

**Key Goals:**
1. Cross-platform CLI for service management (`pywats-client start/stop/status`)
2. Remove Qt dependency from headless service core
3. Automatic stale lock file cleanup
4. Platform-native service integration (Windows Service, systemd, launchd)
5. Optional tray icon for GUI installations only

---

## Success Criteria
- [ ] CLI commands work on Windows, Linux, and macOS
- [ ] Service can start/stop without any GUI components
- [ ] Stale lock files automatically cleaned on startup
- [ ] Tray icon is optional (only loaded if Qt available)
- [ ] `psutil`-based cross-platform process management
- [ ] All existing tests pass
- [ ] New tests for ServiceManager and CLI

---

## Current Status

**Phase 1: Analysis** ✅ Complete
- Analyzed current tray icon dependency problem
- Evaluated cross-platform service management options
- Recommended hybrid approach (CLI + optional tray)

**Phase 2: Implementation Plan** 🚧 In Progress
- Creating detailed implementation plan
- Structuring project files

**Next:** Begin implementation of ServiceManager and CLI

---

## Architecture Decision

**Chosen Approach:** Hybrid CLI + Optional Tray

```
┌─────────────────────────────────────────┐
│         pywats-client CLI               │
│  (Cross-platform, no GUI deps)          │
├─────────────────────────────────────────┤
│ • start    - Start service              │
│ • stop     - Stop service               │
│ • restart  - Restart service            │
│ • status   - Check status               │
│ • gui      - Launch GUI (if Qt avail)   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│  ServiceManager (psutil-based)          │
│  Platform detection + process control   │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│    Headless Service (No Qt/GUI)         │
│    Pure background processing           │
└─────────────────────────────────────────┘
              ↓ (optional)
┌─────────────────────────────────────────┐
│   Qt GUI/Tray (Separate, Optional)      │
│   Only if pywats-api[client] installed  │
└─────────────────────────────────────────┘
```

---

## 📋 Problem Statement

Users have no reliable way to start/restart the pyWATS Client service after closing the GUI:

1. **No Persistent Entry Point**
   - Closing GUI = no way to reopen it
   - No Start Menu shortcut
   - Users must know PowerShell commands

2. **Stale Lock File Crashes**
   - Service crashes can leave stale lock files in `%TEMP%\pyWATS_Client\instance_*.lock`
   - Service won't restart due to "already running" check
   - Users have no way to detect or fix this

3. **Circular Dependency**
   - Tray icon only appears when service is running
   - If service crashes → tray icon disappears → no way to restart

---

## ✅ Acceptance Criteria

**Must Have:**
- [ ] Start Menu shortcut "WATS Client" that always works
- [ ] Launcher detects and cleans stale lock files automatically
- [ ] Simple "Start Client" button for non-technical users
- [ ] Desktop icon (optional during installation)

**Should Have:**
- [ ] Status indicator (service running/stopped)
- [ ] Basic error messages ("Service failed to start - check logs")
- [ ] One-click log viewing

**Nice to Have:**
- [ ] Persistent tray icon (separate from service)
- [ ] Auto-start with Windows option
- [ ] Installer creates shortcuts automatically

---

## 🏗️ Solution Architecture

### Option 1: Simple Launcher (Quick Win - Recommended)

**Scope:** 3-5 days

```
launcher.exe
├─ Check for stale lock files → clean if found
├─ Check if service is running
├─ If not running → start service
└─ Launch dashboard GUI
```

**Files to Create:**
- `scripts/launcher/launcher.py` - Main launcher logic
- `scripts/launcher/launcher.spec` - PyInstaller spec
- `scripts/launcher/build_launcher.ps1` - Build script
- `deployment/windows/create_shortcut.ps1` - Installer helper

**Deliverables:**
- `pyWATS_Client.exe` launcher
- Start Menu shortcut creation script
- User documentation update

---

### Option 2: Persistent Tray Icon (Better UX)

**Scope:** 1-2 weeks (if time permits)

```
tray_app.exe (always running)
├─ Persistent tray icon
├─ Menu: Start Service, Stop Service, Open Dashboard
├─ Status indicator (green/red)
└─ Manages → pywats_client_service.exe
              └─ Hosts → Dashboard GUI
```

**Additional Work:**
- Separate tray application
- Service lifecycle management
- Auto-start registry entry
- More complex installer

**Decision:** Start with Option 1, evaluate Option 2 later

---

## 📂 Files Involved

**Create:**
- `scripts/launcher/launcher.py` (~150 lines)
- `scripts/launcher/build_launcher.ps1` (~50 lines)
- `deployment/windows/install_shortcuts.ps1` (~80 lines)

**Modify:**
- `run_client.ps1` - Add lock file cleanup
- `docs/platforms/windows.md` - Document new launcher
- `README.md` - Update installation instructions

---

## 🧪 Testing Strategy

**Manual Tests:**
1. Clean install → verify shortcut created
2. Start service via launcher → verify opens correctly
3. Kill service (simulate crash) → verify lock cleanup works
4. Double-click shortcut → verify service starts if not running

**Edge Cases:**
- Service already running
- Port already in use
- Lock file from different user
- Missing configuration file

---

## 🚀 Implementation Steps

1. **Create launcher.py** (2 hours)
   - Lock file detection & cleanup
   - Service status check
   - Start service logic
   - Launch GUI

2. **PyInstaller packaging** (1 hour)
   - Create .spec file
   - Build script
   - Test executable

3. **Shortcut creation** (2 hours)
   - PowerShell script to create shortcuts
   - Include in installer
   - Test on clean Windows install

4. **Documentation** (1 hour)
   - Update installation guide
   - Add troubleshooting section
   - User-facing documentation

5. **Testing** (2 hours)
   - Manual testing all scenarios
   - Edge case validation
   - User acceptance testing

**Total Estimate:** 8-10 hours (1-2 days)

---

## 📚 Reference

- Original Analysis: See `docs/internal_documentation/completed/2026-q1/CLIENT_LAUNCHER_UX_IMPROVEMENT.md` for full 230-line analysis
- C# Launcher Investigation: Research WATS Client Launcher behavior for inspiration

---

## 🔗 Dependencies

**Blocked By:** None  
**Blocks:** Future installer improvements, auto-update feature

---

**Ready to Start:** ✅ All requirements clear, solution designed, no blockers
