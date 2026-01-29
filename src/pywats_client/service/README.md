# pyWATS Client Service Architecture

**Architecture version**: v1.4.0 - Async-First Architecture

## Overview

The pyWATS Client uses an **async-first architecture** built on Python's `asyncio` for efficient concurrent I/O. The service and GUI are separated with IPC communication:

```
┌─────────────────────────────────────┐
│  Service Process (Background)        │
│  python -m pywats_client service    │
│                                      │
│  - AsyncClientService (controller)  │
│  - AsyncConverterPool (10 concurrent)│
│  - AsyncPendingQueue (5 concurrent) │
│  - IPC Server (GUI communication)   │
│                                      │
│  Runs independently, 24/7           │
│  Single asyncio event loop          │
└─────────────────────────────────────┘
              ⬍ IPC (Qt LocalSocket) ⬍
┌─────────────────────────────────────┐
│  GUI Process (Optional)              │
│  python -m pywats_client gui        │
│                                      │
│  - MainWindow (PySide6 UI)          │
│  - AsyncAPIRunner (composition) │
│  - IPC Client (service connection)  │
│  - Configuration & Monitoring       │
│                                      │
│  Can launch/exit freely             │
└─────────────────────────────────────┘
```

## Components

### Service Process (src/pywats_client/service/)

#### **async_client_service.py** - Main Async Service Controller
Main service controller using asyncio.

**Responsibilities:**
- Service lifecycle (start/stop) via asyncio tasks
- AsyncWATS API connection (non-blocking)
- Component coordination
- Timer management via asyncio.Task (not QTimer)
- Config file monitoring (hot-reload)
- IPC server for GUI communication

**Key Features:**
- Watchdog timer (60s) - Health checks for all components
- Ping timer (5min) - Server connectivity checks
- Registration timer (1hr) - Status updates to server
- Graceful shutdown with task cancellation
- Signal handling (SIGINT, SIGTERM)

**Usage:**
```bash
python -m pywats_client service --instance-id default
```

```python
from pywats_client.service import AsyncClientService

service = AsyncClientService()
asyncio.run(service.run())  # Blocks until shutdown
```

---

#### **async_converter_pool.py** - Concurrent File Conversion
Converts files using bounded concurrency with asyncio.Semaphore.

**Architecture:**
- **AsyncConverterPool**: Manages converters with semaphore-bounded concurrency
- **Converter**: Individual converter watching a folder
- **asyncio.Semaphore(10)**: Limits to 10 concurrent conversions

**Key Features:**
- **Bounded concurrency**: Up to 10 simultaneous conversions
- **Non-blocking I/O**: Uses aiofiles for file operations
- **File system watching**: Monitors input directories
- **Post-processing**: Move/Delete/Archive/Error handling

**Concurrency Model:**
```python
# Up to 10 files process simultaneously
# Additional files wait for semaphore
async with self._semaphore:  # Semaphore(10)
    result = await self._convert_file(file_path)
```

**State Machine:**
```
File arrives → PENDING → Semaphore acquired → PROCESSING
                            ↓
                    Success: Move to pending queue
                    Failure: Move to Error folder
```

---

#### **async_pending_queue.py** - Concurrent Report Upload Queue
Uploads reports to WATS with bounded concurrency.

**Architecture:**
- **AsyncPendingQueue**: Manages upload queue with semaphore
- **asyncio.Semaphore(5)**: Limits to 5 concurrent uploads
- **aiofiles**: Async file reading

**File-Based State Machine:**
- `.queued` - Ready to upload
- `.processing` - Currently uploading
- `.error` - Upload failed (retry after 5 min)
- `.completed` - Successfully uploaded

**Key Features:**
- **Bounded concurrency**: Up to 5 simultaneous uploads
- **File system watching**: Monitors for .queued files
- **Periodic checking**: Every 60 seconds
- **Timeout recovery**:
  - `.processing` > 30 min → back to `.queued`
  - `.error` > 5 min → retry as `.queued`
- **Atomic state transitions**: File rename = state change
- **Crash-proof**: State persisted in file system

**Concurrency Model:**
```python
async with self._semaphore:  # Semaphore(5)
    await self._submit_report(report_path)
```

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

#### **async_ipc_client.py** - Async IPC Client
Pure asyncio client for GUI to connect to service. No Qt dependency.

**Usage:**
```python
from pywats_client.service.async_ipc_client import AsyncIPCClient

async def check_service():
    client = AsyncIPCClient("default")
    if await client.connect():
        status = await client.get_status()
        print(f"Service status: {status.status}")
        print(f"Queue size: {status.pending_count}")
        await client.disconnect()
```

**Platform Support:**
- Windows: TCP localhost on deterministic port (50000-59999, derived from instance_id hash)
- Linux/macOS: Unix domain sockets at `/tmp/pywats_service_{instance_id}.sock`

---

### GUI Process (src/pywats_client/gui/)

The GUI has been **simplified** to only handle UI and configuration:
- **No embedded services** - Removed pyWATSApplication from GUI
- **Async IPC communication** - Connects to service via AsyncIPCClient
- **qasync integration** - Bridges Qt event loop with asyncio
- **AsyncAPIRunner** - Non-blocking API calls from GUI pages (composition)
- **Can launch/exit freely** - Doesn't affect background operations
- **Service discovery** - Finds running service instances

**Async GUI Integration:**
GUI pages use `AsyncAPIRunner` for non-blocking API calls:
```python
class ProductionPage(BasePage):
    def __init__(self, config, main_window=None, parent=None):
        super().__init__(config, parent, async_api_runner=getattr(main_window, 'async_api_runner', None))
    
    def _lookup_unit(self, part_number: str):
        if self.async_api:
            self.async_api.run(
                self,
                api_call=lambda api: api.production.lookup_production_unit(part_number),
                on_success=self._on_lookup_success,
                on_error=self._on_lookup_error
            )
```

**Migrated GUI Pages:**
- ✅ Production page (`production.py`)
- ✅ Asset page (`asset.py`)
- ✅ Product page (`product.py`)
- ✅ RootCause page (`rootcause.py`)

**Changes from old architecture:**
- ❌ Removed: `pyWATSApplication` instance in MainWindow
- ❌ Removed: `AppFacade` wrapper
- ❌ Removed: Embedded services (ConnectionService, etc.)
- ❌ Removed: ThreadPoolExecutor-based API calls
- ❌ Removed: Qt-based IPC (QLocalSocket/QLocalServer)
- ✅ Added: `AsyncIPCClient` for communication (pure asyncio)
- ✅ Added: `AsyncAPIRunner` for non-blocking API calls (composition)
- ✅ Added: `qasync` for Qt/asyncio integration
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

# GUI connects via async IPC
async def check_service():
    client = AsyncIPCClient(instance_id)
    await client.connect()
    status = await client.get_status()
    print(status)

# Benefits:
# - Service independent of GUI
# - Clean separation
# - No Qt dependency in service
# - Simple and reliable
```

---

## C# Equivalents (Naming Reference)

| Python (snake_case) | C# (PascalCase) | Purpose |
|---------------------|-----------------|---------|
| `ClientService` | `ClientSvc` | Sync entry point |
| `AsyncClientService` | N/A | THE async implementation |
| `AsyncConverterPool` | `Conversion` | Converter orchestration |
| `Converter` | `Converter` | Individual converter |
| `AsyncPendingQueue` | `PendingWatcher` | Report queue |
| `AsyncIPCServer` | `ClientIPC` / WCF | Service communication |

> **Note:** `ConverterPool` and `PendingQueue` are aliases to their async versions.

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
import asyncio
from pywats_client.service.async_ipc_client import AsyncIPCClient

async def test():
    client = AsyncIPCClient("default")
    connected = await client.connect()
    print(f"Connected: {connected}")
    if connected:
        status = await client.get_status()
        print(f"Status: {status}")

asyncio.run(test())
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
