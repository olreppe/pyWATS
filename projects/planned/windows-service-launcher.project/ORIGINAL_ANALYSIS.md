# Client Launcher & Service Startup UX Improvement

**Date:** February 1, 2026  
**Priority:** High  
**Category:** User Experience / Client Service  

---

## Problem Statement

**Current Issue:** Users have no reliable way to start/restart the pyWATS Client service after closing the GUI.

### Specific Problems

1. **GUI Closes = No Access**
   - When GUI is closed, there's no way to restart it
   - No Start Menu shortcut
   - No desktop icon
   - Users must know PowerShell commands or file paths

2. **Tray Icon Dependency**
   - Tray icon only appears when service is running
   - If service crashes or is stopped, tray icon disappears
   - No way to restart service without tray icon access
   - Circular dependency: Need service running → to get tray icon → to start service

3. **Stale Lock File Issue** (Just encountered)
   - Service crashed leaving stale lock at `%TEMP%\pyWATS_Client\instance_*.lock`
   - Service won't start due to "already running" check
   - Users have no way to detect or fix this without technical knowledge

4. **Installation Gap**
   - No installer that creates Start Menu entries
   - No "run at startup" option
   - Manual pip install doesn't integrate with Windows

---

## Current C# Approach

**WATS Client Launcher** - Appears to be a separate launcher application that:
- Provides a persistent entry point (Start Menu, Desktop icon)
- Manages service lifecycle
- Likely handles lock file cleanup
- Gives users a reliable way to start the client

**Investigation needed:** How does the C# launcher work exactly?

---

## Proposed Solutions

### Solution 1: Standalone Launcher Application (Quick Fix)

Create a small launcher executable:
- Always-available Start Menu shortcut
- Checks if service is running
- Cleans stale lock files
- Starts service + GUI
- Simple UI: "Start WATS Client" button

**Files:**
```
scripts/launcher/
  ├── launcher.py          # Main launcher logic
  ├── launcher.spec        # PyInstaller spec
  └── icon.ico             # Application icon
```

**Installer creates:**
```
Start Menu: "WATS Client"
Desktop: "WATS Client" (optional)
```

---

### Solution 2: Persistent Tray Icon (Better UX)

Separate tray application from service:
- Tray icon runs independently
- Shows service status (running/stopped)
- Menu options:
  - Start Service
  - Stop Service
  - Open Dashboard
  - View Logs
  - Exit Tray Icon
- Survives service crashes
- Auto-start with Windows

**Architecture:**
```
tray_app.exe (always running)
  └── Manages → pywats_service.exe (on-demand)
                  └── Hosts → Dashboard GUI (optional)
```

---

### Solution 3: Windows Service + Launcher (Enterprise)

Register as proper Windows Service:
- Service: Background processing (converters, file watch)
- Launcher: GUI + tray icon (user-facing)
- Service runs as SYSTEM or user account
- Launcher auto-starts with user login

**Advantages:**
- Professional integration
- Service survives logoff
- Standard Windows management (services.msc)
- No lock file issues (Windows handles it)

---

## Quick Workarounds (Immediate)

**For Users Right Now:**

1. **Create Desktop Shortcut**
   ```
   Target: C:\Path\to\python.exe -m pywats_client
   Icon: Custom icon
   ```

2. **Start Menu Entry** (Manual)
   ```
   %APPDATA%\Microsoft\Windows\Start Menu\Programs\WATS Client.lnk
   ```

3. **PowerShell Script**
   ```powershell
   # run_wats_client.ps1
   python -m pywats_client
   ```

4. **Clean Stale Locks** (Document this)
   ```powershell
   Remove-Item "$env:TEMP\pyWATS_Client\*.lock" -Force
   ```

---

## Recommended Implementation Plan

### Phase 1: Quick Fix (1-2 days)
1. Create simple launcher script (`launcher.py`)
   - Check for stale locks → cleanup
   - Start service
   - Open GUI
2. Package with PyInstaller → `wats_client_launcher.exe`
3. Add to installer (create Start Menu shortcut)

### Phase 2: Better UX (1 week)
1. Separate tray icon application
   - Persistent (runs independently)
   - Service status monitoring
   - Lock file health checks
2. Auto-start with Windows (registry entry)
3. Proper installer (NSIS or WiX)

### Phase 3: Enterprise (2-4 weeks)
1. Windows Service registration
2. Service control integration
3. Multiple instance support (properly)
4. Clean architecture separation

---

## Technical Debt to Address

1. **Lock File Management**
   - Current `InstanceLock._is_process_running()` fails to detect stale locks
   - Need robust process detection (psutil library?)
   - Automatic cleanup on startup

2. **Service Lifecycle**
   - No graceful shutdown handling
   - No health monitoring
   - No automatic restart on crash

3. **Multi-Instance Handling**
   - Instance ID `e6909626` is... what? Random? Config-based?
   - How to handle multiple profiles (Instance A, B, C)?
   - Lock file location conflicts

---

## Related Issues

- Tray icon implementation needs review
- Service crash recovery needed
- Installation/deployment story incomplete
- Documentation missing for end users

---

## Success Criteria

**Users should be able to:**
1. ✅ Find "WATS Client" in Start Menu and launch it
2. ✅ See tray icon even if service is stopped
3. ✅ Start/stop service from tray icon
4. ✅ Access dashboard from tray icon
5. ✅ Service auto-starts with Windows (optional setting)
6. ✅ Stale locks cleaned automatically

**Developers should be able to:**
1. ✅ Run from source with `python -m pywats_client`
2. ✅ Package launcher easily
3. ✅ Test without installing

---

## References

- Current service: `src/pywats_client/control/service.py`
- Instance manager: `src/pywats_client/core/instance_manager.py`
- GUI: `src/pywats_client/gui/main_window.py`
- Tray icon: `src/pywats_client/gui/` (needs review)

---

**Next Steps:**
1. Review C# WATS Client Launcher implementation
2. Decide on Phase 1, 2, or 3 approach
3. Create launcher prototype
4. Test installation flow
