# Windows Service Launcher

**Project ID:** windows-service-launcher  
**Sprint Size:** 1-2 weeks  
**Priority:** High  
**Status:** Ready to Start  

---

## 🎯 Goal

Make pyWATS Client service easy to start, stop, and manage for Windows users without requiring technical knowledge or PowerShell commands.

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
