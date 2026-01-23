# Service/GUI Mode Separation - Architecture Refactor

**Branch:** `feature/separate-service-gui-mode`  
**Created:** 2026-01-23  
**Status:** In Progress

## Problem Statement

Currently, the pyWATS client auto-starts services every time the GUI is launched. This creates multiple service instances when the user just wants to open the GUI to change settings. The typical use case is:

- **Background service**: Running continuously in the background
- **GUI**: Opened occasionally just to view status or change configuration

## Current Architecture

### Entry Points
- `python -m pywats_client` → GUI mode (auto-starts services)
- `python -m pywats_client --no-gui` → Headless mode (legacy)
- `python -m pywats_client --daemon` → Daemon mode (routes to HeadlessService)
- CLI commands: `config`, `status`, `start`, `stop`, etc.

### Service Lifecycle
1. GUI launches via `gui/app.py:run_gui()`
2. MainWindow created with auto-start timer (100ms delay)
3. `main_window._do_auto_start_async()` starts services in background thread
4. Services run in same process as GUI

### Issues
- Every GUI launch = new service instance
- Instance lock prevents conflicts but shows errors
- Services stop when GUI closes
- No clean separation between service daemon and config UI

## Target Architecture

### Mode Separation

#### 1. Service Mode (Headless)
```bash
# Start background service
python -m pywats_client service

# Or with daemon flag (already exists)
python -m pywats_client --daemon
```

**Behavior:**
- Runs services without GUI
- Continues running until explicitly stopped
- Uses instance lock to prevent multiple services
- Logs to file and/or console
- Can run as Windows service or systemd unit

#### 2. GUI Mode (Configuration)
```bash
# Open GUI for configuration only
python -m pywats_client
# or
python -m pywats_client gui
```

**Behavior:**
- Shows connection status from running service (via IPC)
- Allows configuration changes
- Does NOT start services
- Connects to existing service for status display
- Shows "Service not running" if service is offline

### Communication Architecture

#### Option A: Named Pipes / Local Socket (Recommended)
- Service creates named pipe/socket on startup
- GUI connects to pipe to query status
- Bidirectional: GUI can send commands (start/stop/restart)
- Already have QLocalServer/QLocalSocket for single-instance detection

#### Option B: File-based Status (Simple)
- Service writes status to JSON file
- GUI reads status file periodically
- One-way: GUI can't control service
- Simpler but less flexible

#### Option C: HTTP API (Already Partially Implemented)
- Service runs HTTP API on localhost
- GUI makes HTTP requests for status
- Full control API available
- More overhead but very flexible

**Recommendation:** Use Option A (extend existing QLocalServer pattern)

## Implementation Plan

### Phase 1: Core Architecture Changes

#### 1.1 Add Service Mode CLI Command ✓ (Partially exists)
- File: `src/pywats_client/control/service.py`
- Current: Has `HeadlessService` class
- Action: Verify it works standalone, enhance if needed
- Expose via: `python -m pywats_client service`

#### 1.2 Remove Auto-Start from GUI
- File: `src/pywats_client/gui/main_window.py`
- Remove: `_do_auto_start_async()` method
- Remove: Auto-start timer in `__init__`
- Keep: Status display logic

#### 1.3 Implement Status IPC
- File: `src/pywats_client/services/ipc.py` (new)
- Create: `ServiceStatusServer` (runs in service mode)
- Create: `ServiceStatusClient` (used by GUI)
- Protocol: JSON messages over QLocalSocket
  - `GET_STATUS` → returns service status
  - `GET_SERVICES` → returns individual service states
  - `START_SERVICE` / `STOP_SERVICE` → control commands (optional)

#### 1.4 Update GUI Status Display
- File: `src/pywats_client/gui/pages/connection.py`
- Change: Poll IPC instead of direct status
- Show: "Service not running" vs "Service running"
- Update: All pages that check service status

### Phase 2: Service Control

#### 2.1 Start/Stop Commands
- Enhance: `pywats-client start` to launch service mode
- Enhance: `pywats-client stop` to gracefully shutdown
- Use: PID file for tracking running service

#### 2.2 Windows Integration (Future)
- Create: Windows service wrapper
- Support: `sc create` / `nssm` installation
- Auto-start: On system boot

### Phase 3: Testing & Documentation

#### 3.1 Testing
- Test: Service mode runs independently
- Test: GUI connects to running service
- Test: GUI shows "not running" when service offline
- Test: Single-instance still works for both modes

#### 3.2 Documentation
- Update: README with service vs GUI mode instructions
- Create: Service installation guide
- Update: CLI documentation

## File Changes Required

### New Files
- `src/pywats_client/services/ipc.py` - IPC communication layer
- `src/pywats_client/control/service_daemon.py` - Enhanced service mode (if needed)

### Modified Files
- `src/pywats_client/__main__.py` - Add 'service' subcommand
- `src/pywats_client/gui/app.py` - Remove service startup
- `src/pywats_client/gui/main_window.py` - Remove `_do_auto_start_async()`
- `src/pywats_client/gui/pages/connection.py` - Use IPC for status
- `src/pywats_client/app.py` - Add IPC server support
- `src/pywats_client/control/cli.py` - Enhance start/stop commands

### Configuration Changes
- Add: `service_ipc_name` to config (default: "pyWATS_Service")
- Separate: GUI instance lock from service instance lock

## Migration Path

### For Existing Users
1. Current behavior still works (GUI auto-starts services)
2. Add deprecation warning: "Auto-start will be removed in v0.2.0"
3. Provide migration instructions
4. Next release: Remove auto-start, require explicit service mode

### For New Users
- Document service + GUI pattern from start
- Provide Windows service installer
- Include systemd unit file for Linux

## Open Questions

1. **Should GUI be able to start/stop services?**
   - Pro: Convenient for users
   - Con: Defeats purpose of separation
   - Decision: Allow START but not auto-start

2. **Single config file or separate?**
   - Current: One config file
   - Keep it simple: Use same config for both modes

3. **How to handle service not running?**
   - Show clear message in GUI
   - Provide "Start Service" button
   - Or just display status and let user start manually

## Progress Tracking

- [x] Branch created: `feature/separate-service-gui-mode`
- [x] Architecture analysis complete
- [x] Design document created
- [ ] Phase 1.1: Service mode CLI
- [ ] Phase 1.2: Remove GUI auto-start
- [ ] Phase 1.3: IPC implementation
- [ ] Phase 1.4: GUI status updates
- [ ] Phase 2: Service control
- [ ] Phase 3: Testing & docs

## Notes

- Preserve backward compatibility where possible
- Use existing instance lock mechanism
- Leverage existing HeadlessService foundation
- Keep it simple: Don't over-engineer the IPC layer
