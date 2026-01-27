# pyWATS Client Service Architecture

**New architecture implemented**: Service/Client separation (like C# WATS Client)

## Overview

The pyWATS Client now follows a **clean service/GUI architecture** similar to the proven C# WATS Client design:

```
┌─────────────────────────────────────┐
│  Service Process (Background)        │
│  python -m pywats_client service    │
│                                      │
│  - ClientService (main controller)  │
│  - ConverterPool (worker threads)   │
│  - PendingWatcher (report queue)    │
│  - IPC Server (GUI communication)   │
│                                      │
│  Runs independently, 24/7           │
└─────────────────────────────────────┘
              ⬍ IPC (Qt LocalSocket) ⬍
┌─────────────────────────────────────┐
│  GUI Process (Optional)              │
│  python -m pywats_client gui        │
│                                      │
│  - MainWindow (PySide6 UI)          │
│  - IPC Client (service connection)  │
│  - Configuration & Monitoring       │
│                                      │
│  Can launch/exit freely             │
└─────────────────────────────────────┘
```

## Components

### Service Process (src/pywats_client/service/)

#### **client_service.py** - Main Service Controller
Equivalent to `ClientSvc.cs` in C# implementation.

**Responsibilities:**
- Service lifecycle (start/stop)
- API connection management
- Component coordination
- Timer management (watchdog, ping, registration)
- Config file monitoring (hot-reload)
- IPC server for GUI communication

**Key Features:**
- Watchdog timer (60s) - Health checks for all components
- Ping timer (5min) - Server connectivity checks
- Registration timer (1hr) - Status updates to server
- Graceful shutdown handling
- Signal handling (SIGINT, SIGTERM)

**Usage:**
```bash
python -m pywats_client service --instance-id default
```

---

#### **converter_pool.py** - Converter Pool with Auto-Scaling
Equivalent to `Conversion.cs` in C# implementation.

**Architecture:**
- **ConverterPool**: Manages converters and worker threads
- **Converter**: Individual converter watching a folder
- **ConverterWorkerClass**: Worker thread processing files
- **ConversionItem**: File queued for conversion

**Key Features:**
- **Auto-scaling worker pool**: 1 worker per 10 pending files
- **Max workers**: Configurable (default: 10, max: 50)
- **Auto-shutdown**: Workers terminate after 120s idle
- **Timeout recovery**: Reset items stuck >10 minutes
- **File system watching**: Per-converter folder monitoring
- **Post-processing**: Move/Delete/Archive/Error handling

**Worker Pool Behavior:**
```python
# Pending files: 0-10  -> 1 worker
# Pending files: 11-20 -> 2 workers
# Pending files: 21-30 -> 3 workers
# ... up to max_workers
```

**State Machine:**
```
File arrives → PENDING → Worker picks up → PROCESSING
                            ↓
                    Success: Post-process (move/delete)
                    Failure: Move to Error folder
```

---

#### **pending_watcher.py** - Offline Report Queue
Equivalent to `PendingWatcher.cs` in C# implementation.

**File-Based State Machine:**
- `.queued` - Ready to upload
- `.processing` - Currently uploading
- `.error` - Upload failed (retry after 5 min)
- `.completed` - Successfully uploaded

**Key Features:**
- **File system watching**: Monitors for .queued files
- **Periodic checking**: Every 5 minutes
- **Timeout recovery**:
  - `.processing` > 30 min → back to `.queued`
  - `.error` > 5 min → retry as `.queued`
- **Atomic state transitions**: File rename = state change
- **Crash-proof**: State persisted in file system

**Why file extensions for state?**
- Simple and reliable
- Survives crashes perfectly
- Atomic state transitions (file rename)
- Easy to inspect/debug (just look at files)
- No database or in-memory state needed

---

#### **ipc_server.py** - IPC Server
Simple IPC server for GUI↔Service communication.

**Protocol:** JSON over Qt LocalSocket
**Socket name:** `pyWATS_Service_{instance_id}`

**Supported Commands:**
- `get_status` - Get service status
- `get_config` - Get configuration
- `ping` - Check if alive
- `stop` - Stop service gracefully
- `restart` - Restart service (TODO)

**Example Response:**
```json
{
  "status": "Running",
  "api_status": "Online",
  "instance_id": "default",
  "converters": [
    {"name": "CSV Importer", "state": "Running", "pending_count": 5},
    ...
  ],
  "queue_size": 12
}
```

---

#### **ipc_client.py** - IPC Client
Client for GUI to connect to service.

**Usage:**
```python
from pywats_client.service.ipc_client import ServiceIPCClient

client = ServiceIPCClient("default")
if client.connect():
    status = client.get_status()
    print(f"Service status: {status['status']}")
    print(f"Queue size: {status['queue_size']}")
```

---

### GUI Process (src/pywats_client/gui/)

The GUI has been **simplified** to only handle UI and configuration:
- **No embedded services** - Removed pyWATSApplication from GUI
- **IPC communication only** - Connects to service via IPC
- **Can launch/exit freely** - Doesn't affect background operations
- **Service discovery** - Finds running service instances

**Changes from old architecture:**
- ❌ Removed: `pyWATSApplication` instance in MainWindow
- ❌ Removed: `AppFacade` wrapper
- ❌ Removed: Embedded services (ConnectionService, etc.)
- ✅ Added: `ServiceIPCClient` for communication
- ✅ Added: Service discovery and auto-connect
- ✅ Added: "Start Service" button if not running

---

## Usage

### Running the Service

**Foreground (for testing):**
```bash
python -m pywats_client service --instance-id default
```

**As Windows Service:**
```bash
# Install
python -m pywats_client install-service --instance-id default

# Start/Stop via Services app or:
sc start "pyWATS Client Service - default"
sc stop "pyWATS Client Service - default"
```

**As Linux systemd service:**
```bash
# Install
sudo python -m pywats_client install-service --instance-id default

# Start/Stop
sudo systemctl start pywats-client-default
sudo systemctl stop pywats-client-default
sudo systemctl status pywats-client-default
```

---

### Running the GUI

**Connect to existing service:**
```bash
python -m pywats_client gui --instance-id default
```

The GUI will:
1. Try to connect to service via IPC
2. If service not running, prompt to start it
3. Display real-time status from service
4. Allow configuration changes (sent to service via IPC)

---

### Multiple Instances

You can run multiple independent instances on the same machine:

```bash
# Terminal 1: Production station
python -m pywats_client service --instance-id production

# Terminal 2: Test station
python -m pywats_client service --instance-id test

# Terminal 3: GUI for production
python -m pywats_client gui --instance-id production

# Terminal 4: GUI for test
python -m pywats_client gui --instance-id test
```

Each instance has its own:
- Configuration file
- Report queue
- Converter settings
- IPC socket

---

## Configuration

### Configuration Files

**Location:**
- Windows: `%APPDATA%\pyWATS_Client\config_{instance_id}.json`
- Linux/Mac: `~/.config/pywats_client/config_{instance_id}.json`

**Structure:**
```json
{
  "version": "2.0",
  "instance_id": "default",
  "server": {
    "url": "https://company.wats.com",
    "token_encrypted": "..."
  },
  "station": {
    "name": "Station-1",
    "location": "Factory Floor",
    "purpose": "Production"
  },
  "service": {
    "max_converter_workers": 10,
    "watchdog_interval": 60,
    "ping_interval": 300,
    "register_interval": 3600
  },
  "converters": [...]
}
```

### Converter Configuration

Converters are defined in the main config or separate `converters.json`:

```json
{
  "name": "CSV Importer",
  "enabled": true,
  "watch_folder": "C:/TestData/CSV",
  "module_path": "~/.pywats/converters/csv_converter.py",
  "file_patterns": ["*.csv"],
  "arguments": {
    "delimiter": ",",
    "has_header": true
  },
  "post_action": "move",
  "done_folder": "C:/TestData/CSV/Done",
  "error_folder": "C:/TestData/CSV/Error"
}
```

---

## Architecture Benefits

### ✅ Service Independence
- Service runs 24/7 without GUI
- GUI can launch/exit without affecting background work
- Multiple GUIs can connect to one service
- Perfect for server deployments (no GUI needed)

### ✅ Reliability
- File-based queue survives crashes
- Automatic timeout recovery
- Worker auto-scaling for burst loads
- Graceful degradation on errors

### ✅ Performance
- Auto-scaling worker pool (1-50 workers)
- Efficient resource usage (workers idle out)
- Parallel file processing
- Minimal overhead when idle

### ✅ Maintainability
- Clean separation of concerns
- Simple IPC protocol
- File-based state (easy to debug)
- C# naming conventions (familiar to team)

### ✅ Cross-Platform
- Works on Windows, Linux, macOS
- Qt LocalSocket for IPC (cross-platform)
- Python standard library for service
- systemd/launchd/Windows Service support

---

## Comparison to Old Architecture

### Old (Broken) Architecture
```python
# GUI created embedded services
pywats_app = pyWATSApplication(config)  # Services inside!
window = MainWindow(config, pywats_app)

# Problems:
# - Closing GUI stops services
# - Can't run headless
# - IPC never actually used
# - Over-engineered facades
```

### New (Working) Architecture
```python
# Service runs independently
service = ClientService(instance_id)
service.start()  # Blocks, runs 24/7

# GUI connects via IPC
client = ServiceIPCClient(instance_id)
client.connect()
status = client.get_status()

# Benefits:
# - Service independent of GUI
# - Clean separation
# - Simple and reliable
```

---

## C# Equivalents (Naming Reference)

| Python (snake_case) | C# (PascalCase) | Purpose |
|---------------------|-----------------|---------|
| `ClientService` | `ClientSvc` | Main service controller |
| `ConverterPool` | `Conversion` | Converter orchestration |
| `Converter` | `Converter` | Individual converter |
| `ConverterWorkerClass` | `ConverterWorkerClass` | Worker thread |
| `ConversionItem` | `ConversionItem` | File to convert |
| `PendingWatcher` | `PendingWatcher` | Report queue |
| `IPCServer` | `ClientIPC` / WCF | Service communication |

---

## Migration from Old Code

### For Developers

The old `pyWATSApplication` class still exists but is **deprecated**. New code should:

1. **Run service separately:**
   ```bash
   python -m pywats_client service
   ```

2. **GUI uses IPC only:**
   ```python
   from pywats_client.service.ipc_client import ServiceIPCClient
   client = ServiceIPCClient("default")
   ```

3. **No embedded services:**
   - Don't create `pyWATSApplication` in GUI
   - Don't use `AppFacade`
   - Use `ServiceIPCClient` instead

### For Users

**Old way (deprecated):**
```bash
python -m pywats_client  # Launches GUI with embedded services
```

**New way (recommended):**
```bash
# Terminal 1: Start service
python -m pywats_client service

# Terminal 2: Launch GUI (connects to service)
python -m pywats_client gui
```

Or install as system service for automatic startup.

---

## Troubleshooting

### Service won't start

**Check logs:**
- Windows: `%APPDATA%\pyWATS_Client\service.log`
- Linux/Mac: `~/.config/pywats_client/service.log`

**Common issues:**
- Port/socket already in use (another instance running?)
- Config file errors
- Missing dependencies (pywats, PySide6, watchdog)

### GUI can't connect

**Check if service is running:**
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep pywats
```

**Test IPC connection:**
```python
from pywats_client.service.ipc_client import ServiceIPCClient
client = ServiceIPCClient("default")
print(client.connect())  # Should be True
```

### Converters not processing files

**Check converter status:**
- In GUI: Check Converters page
- Via IPC: `client.get_status()['converters']`
- Check error folder for failed files

**Common issues:**
- Watch folder doesn't exist
- File permissions
- Converter module not found
- Converter class errors (check logs)

---

## Future Enhancements

- [ ] HTTP REST API for remote control
- [ ] Web-based GUI (in addition to Qt)
- [ ] Distributed processing (multiple machines)
- [ ] Advanced monitoring/metrics
- [ ] Plugin marketplace for converters
- [ ] Docker containerization

---

## References

- Architecture: `docs/guides/client-architecture.md`
- Original pyWATS: `src/pywats/` (REST API wrapper)
