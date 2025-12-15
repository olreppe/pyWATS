# PyWATS Client Architecture - Service & Client Refactoring

## Overview

The PyWATS Client has been refactored into a layered architecture that separates:

1. **Base Application Layer** (`pyWATSApplication`) - Core service without GUI
2. **GUI Layer** (`PySide6`) - Optional Qt-based interface
3. **Services Layer** - Specialized services (connection, sync, queue, converters)
4. **Settings & Configuration** - Persistent settings management
5. **Serial Number Management** - Offline serial reservation
6. **File Monitoring** - Automatic file detection and conversion

## Architecture Layers

### 1. Core Application (No GUI)

**File:** `src/pywats_client/app.py`

The `pyWATSApplication` class is the main orchestrator that runs without any UI:

```python
from pywats_client import pyWATSApplication, ApplicationStatus
from pywats_client import ClientConfig

# Load configuration
config = ClientConfig.load("config.json")

# Create application
app = pyWATSApplication(config)

# Add callbacks for status changes
app.on_status_changed(lambda status: print(f"Status: {status.value}"))
app.on_error(lambda error: print(f"Error: {error}"))

# Start all services
await app.start()

# Use services
if app.is_online():
    report = app.wats_client.reports.get_by_id(123)
    
    # Check offline queue
    queue_status = app.get_queue_status()
    print(f"Pending reports: {queue_status['pending_reports']}")

# Stop gracefully
await app.stop()
```

**Features:**
- Service lifecycle management (start, stop, restart)
- Connection monitoring
- Status tracking and callbacks
- Error handling with callbacks
- Access to all sub-services
- Multi-instance locking (single instance per config)

**Status Flow:**
```
STOPPED -> STARTING -> RUNNING -> STOPPING -> STOPPED
   |                      |
   +------- ERROR --------+
```

### 2. Services Layer

#### ConnectionService
**File:** `src/pywats_client/services/connection.py`

Manages server connectivity with automatic reconnection:

```python
# Access from application
connection = app.connection

# Check status
if connection.status == ConnectionStatus.ONLINE:
    print("Connected to server")

# Register for status changes
connection.on_status_changed(
    lambda status: print(f"Connection: {status.value}")
)

# Get last error
last_error = connection.last_error
```

**Status Enum:**
- `DISCONNECTED` - Initial state
- `CONNECTING` - Attempting connection
- `ONLINE` - Successfully connected
- `OFFLINE` - Lost connection
- `ERROR` - Persistent connection error

#### ProcessSyncService
**File:** `src/pywats_client/services/process_sync.py`

Synchronizes process and product data from server:

```python
process_sync = app.process_sync

# Data is automatically synced from server
# Access synchronized data
data = process_sync.get_cached_data("processes")
```

#### ReportQueueService
**File:** `src/pywats_client/services/report_queue.py`

Manages offline report storage and automatic upload:

```python
report_queue = app.report_queue

# Get pending reports count
pending = len(report_queue.queue)

# Queue status
print(f"Pending reports: {pending}")
print(f"Pending files: {len(report_queue.pending_files)}")

# Reports automatically upload when online
```

#### ConverterManager
**File:** `src/pywats_client/services/converter_manager.py`

Manages file format converters:

```python
converter_mgr = app.converter_manager

# Convert a file
result = await converter_mgr.convert("data.csv", converter_type="csv")

if result.success:
    report = result.report
    # Can queue for upload
```

### 3. Settings Management

**File:** `src/pywats_client/services/settings_manager.py`

Persistent settings storage and management:

```python
from pywats_client import SettingsManager, MonitorFolder, ConverterConfig

# Create settings manager
settings_mgr = SettingsManager(config_dir=Path("./config"))

# Load settings
settings = settings_mgr.load()

# Modify settings
settings.server_url = "https://new-server.com"
settings.log_level = "DEBUG"

# Add a monitor folder
folder = MonitorFolder(
    path="./uploads",
    converter_type="csv",
    auto_upload=True,
    delete_after_convert=True
)
settings_mgr.add_monitor_folder(folder)

# Save settings
settings_mgr.save(settings)

# Listen for external changes
settings_mgr.on_settings_changed(lambda s: reload_config(s))
```

**Settings Structure:**
```json
{
  "server_url": "https://python.wats.com",
  "api_token": "...",
  "connection_check_interval": 30,
  "auto_upload_reports": true,
  "auto_upload_interval": 60,
  "log_level": "INFO",
  "auto_reserve_serials": true,
  "reserve_count": 10,
  "monitor_folders": [
    {
      "path": "./uploads",
      "enabled": true,
      "converter_type": "csv",
      "recursive": false,
      "delete_after_convert": true,
      "auto_upload": true
    }
  ]
}
```

### 4. Serial Number Management

**File:** `src/pywats_client/services/serial_manager.py`

Persistent pool of reserved serial numbers for offline use:

```python
from pywats_client import SerialNumberManager

# Create manager
serial_mgr = SerialNumberManager(storage_path=Path("./serials.json"))

# Get pool status
status = serial_mgr.get_pool_status()
print(f"Available serials: {status['unused']}")

# Get a serial for offline use
serial = serial_mgr.get_reserved_serial()

if serial:
    # Use serial for test...
    # After test completes
    serial_mgr.mark_used(serial, test_id="test_123")

# Get recommendations
recommendations = serial_mgr.get_recommendations()

# Used serials can be synced back when online
used = serial_mgr.get_used_serials()
# ... sync back to server ...
serial_mgr.clear_used_serials()
```

**Pool Management:**
- Auto-replenish when online
- Persist used serials offline
- Track serial usage
- Clear after syncing with server

### 5. File Monitoring

**File:** `src/pywats_client/services/file_monitor.py`

Watches folders for files and auto-converts/uploads them:

```python
from pywats_client import FileMonitor, MonitorRule, FileEventType

# Create monitor
file_monitor = FileMonitor(check_interval=2)  # Check every 2 seconds

# Add monitoring rule
rule = MonitorRule(
    path="./uploads",
    converter_type="csv",
    recursive=False,
    delete_after_convert=True,
    auto_upload=True,
    file_pattern="*.csv"
)
file_monitor.add_rule(rule)

# Handle file events
async def on_file_event(event):
    print(f"File {event['type'].value}: {event['path'].name}")
    # Trigger conversion...
    
file_monitor.on_file_event(on_file_event)

# Start monitoring
await file_monitor.start()

# Get status
status = file_monitor.get_status()
print(f"Monitoring {status['rules_count']} folders")
```

## Integration: Complete Application Example

```python
import asyncio
from pathlib import Path
from pywats_client import (
    pyWATSApplication,
    ClientConfig,
    SettingsManager,
    SerialNumberManager,
    FileMonitor,
    MonitorRule,
    ApplicationStatus,
)

async def main():
    # Load configuration
    config = ClientConfig.load("config.json")
    
    # Create application
    app = pyWATSApplication(config)
    
    # Setup settings
    settings_mgr = SettingsManager(config_dir=Path("./config"))
    settings = settings_mgr.load()
    
    # Setup serial management
    serial_mgr = SerialNumberManager(storage_path=Path("./serials.json"))
    
    # Setup file monitoring
    file_monitor = FileMonitor()
    for folder_config in settings.monitor_folders:
        rule = MonitorRule(
            path=folder_config["path"],
            converter_type=folder_config.get("converter_type", ""),
            auto_upload=folder_config.get("auto_upload", True),
        )
        file_monitor.add_rule(rule)
    
    # Handle file events
    async def on_file_event(event):
        converter_type = event["converter_type"]
        file_path = event["path"]
        
        # Convert file
        converter_mgr = app.converter_manager
        result = await converter_mgr.convert(
            str(file_path),
            converter_type=converter_type
        )
        
        if result.success:
            # Queue report
            report = result.report
            app.report_queue.queue.append(report)
            
            # Delete file if configured
            if event["delete_after_convert"]:
                file_path.unlink()
    
    file_monitor.on_file_event(on_file_event)
    
    # Handle status changes
    def on_status_changed(status):
        print(f"App status: {status.value}")
        
        if status == ApplicationStatus.RUNNING:
            # When online, sync data
            if app.connection.status.value == "Online":
                # Replenish serial pool
                if serial_mgr.is_depleted():
                    print("Serial pool low, reserving more when online...")
                
                # Sync used serials back to server
                used = serial_mgr.get_used_serials()
                if used:
                    print(f"Syncing {len(used)} used serials to server...")
    
    app.on_status_changed(on_status_changed)
    
    # Start everything
    await app.start()
    await file_monitor.start()
    
    try:
        # Keep running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        await file_monitor.stop()
        await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
```

## GUI Layer (Optional)

**File:** `src/pywats_client/gui/app.py`

The GUI runs on top of the base application:

```python
from pywats_client.gui.app import run_gui, run_headless

# For GUI mode
run_gui()

# For headless/service mode
run_headless()
```

The GUI:
- Uses `pyWATSApplication` for all business logic
- Provides status visualization
- Allows settings configuration
- Shows offline queue status
- Manages file monitoring rules
- No business logic duplication

## Deployment Scenarios

### 1. GUI Application
```bash
python -m pywats_client.gui.app
```
Runs the full PySide6 GUI application.

### 2. Headless Service
```bash
python -m pywats_client.gui.app --headless
```
Runs without GUI (systemd service, Windows service, etc).

### 3. Custom Application
```python
from pywats_client import pyWATSApplication, ClientConfig

config = ClientConfig.load("config.json")
app = pyWATSApplication(config)
await app.start()
# ... use app ...
await app.stop()
```

### 4. Windows Service
Wrapper for running as Windows Service:
```python
import servicemanager
from pywats_client.services.windows_service import WATSClientService

if __name__ == '__main__':
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(WATSClientService)
    servicemanager.StartServiceCtrlDispatcher()
```

## File Structure

```
pywats_client/
├── app.py                          # Base application (no GUI)
├── __init__.py                     # Package exports
├── core/
│   ├── client.py                   # WATSClient (orchestrator)
│   ├── config.py                   # ClientConfig
│   └── instance_manager.py         # Single instance lock
├── gui/
│   ├── app.py                      # GUI entry point
│   ├── main_window.py              # Main window
│   └── pages/                      # GUI pages/views
├── services/
│   ├── connection.py               # Server connection
│   ├── process_sync.py             # Data synchronization
│   ├── report_queue.py             # Offline queue
│   ├── converter_manager.py        # File converters
│   ├── windows_service.py          # Windows integration
│   ├── settings_manager.py         # Settings persistence [NEW]
│   ├── serial_manager.py           # Serial management [NEW]
│   └── file_monitor.py             # File monitoring [NEW]
├── converters/
│   ├── base.py                     # Base converter class
│   └── example_csv.py              # Example CSV converter
└── tools/
    └── test_uut.py                 # Testing utilities
```

## Key Design Principles

1. **Separation of Concerns**
   - Base app (`pyWATSApplication`) has no GUI dependencies
   - Services are independent and pluggable
   - GUI is a consumer of the base app

2. **Async First**
   - All I/O operations are async
   - Proper task cleanup on shutdown
   - Non-blocking event loops

3. **Persistent State**
   - Settings stored in JSON
   - Serial numbers stored locally
   - Offline queue in local storage

4. **Error Resilience**
   - Automatic reconnection
   - Graceful degradation when offline
   - Detailed error tracking

5. **Extensibility**
   - Pluggable converter framework
   - Custom monitoring rules
   - Callback-based event system

## Next Steps

1. ✅ Base application layer
2. ✅ Settings management
3. ✅ Serial number management
4. ✅ File monitoring
5. ⚠️ Update error handling to use WATS API ErrorHandler
6. ⚠️ Create installable package configuration
7. ⚠️ Update GUI to use new architecture
8. ⚠️ System service integration (Windows/systemd)
