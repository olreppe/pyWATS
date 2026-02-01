# Service/GUI Mode Separation - Architecture Refactor

**Branch:** `feature/separate-service-gui-mode`  
**Created:** 2026-01-23  
**Status:** In Progress

## Problem Statement

Currently, the pyWATS client auto-starts services every time the GUI is launched. This creates multiple service instances when the user just wants to open the GUI to change settings.

## Use Cases

### Use Case 1: Normal Installation (Single Station)
- **One service** runs continuously in background
- **One connection** (token + station config)
- **One set of converters** monitoring specific folders
- **GUI** opens to view status/change settings
- Service keeps running when GUI closes

### Use Case 2: Multi-Station Mode (PC Relay for Multiple Stations)
- **Multiple independent service instances** (one per simulated station)
- Each instance has:
  - Own config file (token, station info, paths)
  - Own connection to WATS server
  - Own converters and queue
  - Appears as separate test station to server
- **One GUI** that can:
  - Discover all running instances
  - Switch between instances
  - Configure each station individually
- All services keep running when GUI closes

### Use Case 3: Custom Implementations
- Developers using the client for custom scenarios
- May need programmatic access without GUI
- Service mode provides stable background process

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

#### 1. Service Mode (Background Daemon)
```bash
# Single station (default)
python -m pywats_client service
# Uses default config from ~/.pywats_client/config.json

# Multi-station (specify instance ID and config)
python -m pywats_client service --instance-id station1 --config station1.json
python -m pywats_client service --instance-id station2 --config station2.json
python -m pywats_client service --instance-id station3 --config station3.json
```

**Behavior:**
- Runs services without GUI
- Continues running until explicitly stopped
- Uses instance lock to prevent duplicate instances with same ID
- Each instance creates IPC endpoint: `pyWATS_Service_{instance_id}`
- Logs to file and/or console
- Can run as Windows service or systemd unit

#### 2. GUI Mode (Configuration Interface)
```bash
# Single station - connects to default instance
python -m pywats_client

# Multi-station - GUI discovers all running instances automatically
python -m pywats_client
```

**Behavior:**
- **Discovers all running service instances** by scanning IPC endpoints
- Shows instance selector (dropdown or sidebar list)
- Displays status from selected instance
- Allows configuration changes
- **Does NOT auto-start services**
- Shows "No services running" if no instances found
- Optional: "Start Service" button to launch default instance

### Multi-Instance Support

#### Instance Discovery
- GUI scans for IPC endpoints matching pattern `pyWATS_Service_*`
- Lists all discovered instances by instance_id
- Shows status indicator for each (running/connected/offline)

#### Instance Selector UI
**Option 1: Dropdown in header**
```
┌─────────────────────────────────────┐
│ [Station 1 ▼]  ●Running             │
├─────────────────────────────────────┤
│   Connection │ Analytics │ ...      │
│                                      │
│   Status: Connected                  │
│   Queue: 5 reports                   │
└─────────────────────────────────────┘
```

**Option 2: Sidebar list** (Recommended)
```
┌──────┬──────────────────────────────┐
│ Inst │  Connection │ Analytics      │
├──────┤                               │
│●Stn1 │  Status: Connected            │
│●Stn2 │  Queue: 5 reports             │
│○Stn3 │                               │
│      │                               │
└──────┴──────────────────────────────┘
```

#### Configuration per Instance
- Each instance has separate config file
- GUI saves config changes to instance-specific file
- Config includes:
  - Connection (URL, token)
  - Station info (name, ID)
  - Data paths (converters, queue, cache)
  - Service settings

### Communication Architecture

#### IPC Protocol (Named Pipes/Local Sockets)

**Service Side (ServiceStatusServer):**
- Creates named socket: `pyWATS_Service_{instance_id}`
- Listens for connections from GUI
- Responds to status queries
- Accepts configuration change commands

**GUI Side (ServiceStatusClient):**
- Scans for all `pyWATS_Service_*` sockets (discovery)
- Connects to selected instance's socket
- Polls for status updates
- Sends configuration changes

**Message Protocol (JSON over socket):**
```json
// GUI → Service: Get status
{"command": "get_status"}

// Service → GUI: Status response
{
  "status": "running",
  "connection": "connected",
  "instance_id": "station1",
  "config_file": "/path/to/station1.json",
  "services": {
    "connection": "online",
    "process_sync": "running",
    "report_queue": "running",
    "converter_manager": "running"
  },
  "stats": {
    "queue_size": 5,
    "uptime": 3600
  }
}

// GUI → Service: Get configuration
{"command": "get_config"}

// Service → GUI: Config response
{
  "config": { /* ClientConfig as JSON */ }
}

// GUI → Service: Update configuration
{
  "command": "update_config",
  "config": { /* partial or full config */ }
}

// GUI → Service: Control commands (optional)
{"command": "restart"}
{"command": "stop"}
```

**Benefits:**
- Built on existing QLocalServer/QLocalSocket infrastructure
- Simple JSON protocol
- Bidirectional communication
- Easy to extend with new commands
- No external dependencies

## Implementation Plan

### Phase 1: Core Service Mode

#### 1.1 Enhance Service Mode CLI ✓ (Partially exists)
- File: `src/pywats_client/__main__.py`
- Add: `service` as a proper subcommand (not just `--daemon`)
- Support: `--instance-id` and `--config` parameters
- Verify: `HeadlessService` in `control/service.py` works correctly

#### 1.2 Add IPC Server to Service
- File: `src/pywats_client/services/ipc.py` (new)
- Create: `ServiceIPCServer` class
  - Uses QLocalServer with name `pyWATS_Service_{instance_id}`
  - Handles JSON message protocol
  - Returns status, config, service states
  - Accepts config updates
- Integrate: Add IPC server to `pyWATSApplication.start()`

### Phase 2: GUI Instance Discovery & Selection

#### 2.1 Implement Instance Discovery
- File: `src/pywats_client/services/ipc.py`
- Create: `ServiceDiscovery` class
  - Scans for `pyWATS_Service_*` sockets
  - Returns list of running instances
  - Tests connectivity to each

#### 2.2 Create Instance Selector UI
- File: `src/pywats_client/gui/widgets/instance_selector.py` (new)
- Widget: Shows list of discovered instances
- Features:
  - Auto-refresh (scan every 5 seconds)
  - Status indicator (connected/offline)
  - "Start Service" button if none running
- Placement: Sidebar or header dropdown

#### 2.3 Remove GUI Auto-Start
- File: `src/pywats_client/gui/main_window.py`
- Remove: `_do_auto_start_async()` method
- Remove: Auto-start timer in `__init__`
- Keep: Status display logic (will now use IPC)

### Phase 3: GUI-Service Communication

#### 3.1 Implement IPC Client
- File: `src/pywats_client/services/ipc.py`
- Create: `ServiceIPCClient` class
  - Connects to specific instance's socket
  - Sends commands, receives responses
  - Handles connection errors gracefully

#### 3.2 Update GUI Status Display
- File: `src/pywats_client/gui/pages/connection.py`
- Change: Use IPC client instead of direct app status
- Show: Service status, connection state, queue size
- Handle: "Service not running" state

#### 3.3 Update Other Pages
- Files: All pages that check service/connection status
- Change: Use IPC client for status queries
- Examples: Analytics, Software, Report pages

### Phase 4: Multi-Instance Config Management

#### 4.1 Config File Naming
- Pattern: `~/.pywats_client/config_{instance_id}.json`
- Default: `~/.pywats_client/config.json` (for "default" instance)
- GUI: Loads/saves config for selected instance

#### 4.2 Instance Lock Separation
- Current: One instance lock per instance_id ✓ (already works)
- Verify: Multiple instances can run simultaneously
- Lock file pattern: `{temp}/pywats_client_{instance_id}.lock`

### Phase 5: Testing

#### 5.1 Single Station Mode
- Test: Start one service instance
- Test: GUI discovers and connects
- Test: Status updates appear in GUI
- Test: Config changes save correctly
- Test: Service keeps running when GUI closes

#### 5.2 Multi-Station Mode
- Test: Start 3 service instances (station1, station2, station3)
- Test: GUI discovers all 3 instances
- Test: Switch between instances in GUI
- Test: Each instance has separate config/queue/converters
- Test: All services keep running independently

#### 5.3 Edge Cases
- Test: GUI shows "No services running" when none exist
- Test: GUI handles service crash/disconnect gracefully
- Test: "Start Service" button launches default instance
- Test: Instance lock prevents duplicate instance_ids

### Phase 6: Documentation

#### 6.1 User Documentation
- Update: README with service vs GUI mode
- Create: Multi-station setup guide
- Document: Command-line options

#### 6.2 Developer Documentation
- Document: IPC protocol
- Document: Adding new IPC commands
- Document: Instance management

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

## Example Workflows

### Workflow 1: Single Station Setup

**Initial Setup:**
```bash
# Configure the client
python -m pywats_client
# Login, configure connection, converters, etc. in GUI
# Close GUI

# Start the service
python -m pywats_client service
# Service runs in background
```

**Ongoing Use:**
```bash
# Service is always running in background
# Open GUI only to check status or change settings
python -m pywats_client
# GUI shows: ●Station (Connected)
# Make changes, close GUI
# Service keeps running
```

### Workflow 2: Multi-Station Setup

**Initial Setup:**
```bash
# Create config for each station
cp config.json station1_config.json
cp config.json station2_config.json
cp config.json station3_config.json

# Edit each config (different tokens, station IDs, paths)

# Start services
python -m pywats_client service --instance-id station1 --config station1_config.json
python -m pywats_client service --instance-id station2 --config station2_config.json
python -m pywats_client service --instance-id station3 --config station3_config.json
```

**Ongoing Use:**
```bash
# All 3 services running in background
# Open GUI to manage them
python -m pywats_client

# GUI shows instance selector:
# ●station1 (Connected)
# ●station2 (Connected)
# ○station3 (Offline)

# Click station1 → see its status/config
# Click station2 → see its status/config
# Click station3 → see error details
```

### Workflow 3: Windows Service Installation (Future)

```powershell
# Install as Windows service (auto-start on boot)
pywats-client install-service
# or with nssm:
nssm install pyWATSClient "C:\...\python.exe" "-m pywats_client service"

# Start service
net start pyWATSClient

# Configure via GUI anytime
python -m pywats_client
```

## Open Questions

### RESOLVED:

1. **Should GUI be able to start/stop services?**
   - ✅ YES: GUI shows "Start Service" button if none running
   - ✅ YES: GUI can send stop/restart commands to running services
   - User-friendly for occasional users

2. **Single config file or separate?**
   - ✅ SEPARATE: Each instance has own config file
   - Pattern: `config_{instance_id}.json`
   - Allows different tokens, paths, station IDs per instance

3. **How to handle service not running?**
   - ✅ Show "No services running" with explanation
   - ✅ Provide "Start Default Service" button
   - ✅ Allow user to browse/select config and start specific instance

4. **Multi-instance GUI approach?**
   - ✅ OPTION C: GUI discovers all instances, shows selector
   - ✅ User switches between instances in GUI
   - ✅ Each instance maintains independent service process

### REMAINING:

5. **Instance selector UI placement?**
   - Option A: Dropdown in header (simpler)
   - Option B: Sidebar list (more visible, recommended for 3+ instances)
   - Decision: Start with sidebar, evaluate UX

6. **Config file management in GUI?**
   - Should GUI allow creating new instance configs?
   - Should GUI show file paths?
   - Or keep it simple: just show instance names?

7. **Error handling when instance disconnects?**
   - Auto-reconnect attempts?
   - Show stale data or clear display?
   - Notification to user?

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
