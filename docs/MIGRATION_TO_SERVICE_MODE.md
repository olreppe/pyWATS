# Migration Guide: Service/GUI Architecture

**Version**: 2.0  
**Date**: January 2026

## Overview

pyWATS Client has been redesigned to follow a clean **service/GUI separation** architecture, matching the proven C# WATS Client design. This guide helps you migrate from the old embedded architecture to the new IPC-based system.

## What Changed?

### Old Architecture (v1.x)
```
┌─────────────────────────────────┐
│  GUI Process                     │
│  ├─ MainWindow (UI)             │
│  └─ pyWATSApplication (embedded)│
│     ├─ Converters               │
│     ├─ Report Queue             │
│     └─ API Client               │
│                                  │
│  Problem: Closing GUI stops     │
│  all background operations!     │
└─────────────────────────────────┘
```

### New Architecture (v2.0)
```
┌─────────────────────────────────┐
│  Service Process (Background)    │
│  python -m pywats_client service│
│  ├─ ClientService               │
│  ├─ ConverterPool (auto-scale)  │
│  ├─ PendingWatcher (queue)      │
│  └─ IPC Server                  │
└─────────────────────────────────┘
              ⬍ IPC ⬍
┌─────────────────────────────────┐
│  GUI Process (Optional)          │
│  python -m pywats_client gui    │
│  ├─ MainWindow                  │
│  └─ IPC Client                  │
│                                  │
│  Can launch/exit freely!        │
└─────────────────────────────────┘
```

## Migration Steps

### For End Users

#### Before (v1.x)
```bash
# Start application
python -m pywats_client

# Closing GUI stops everything
```

#### After (v2.0)

**Step 1: Start service** (runs 24/7 in background)
```bash
python -m pywats_client service --instance-id default
```

**Step 2: Launch GUI** (optional, for configuration)
```bash
python -m pywats_client gui --instance-id default
```

Or install as Windows Service for automatic startup:
```bash
# Install service (runs automatically on boot)
python -m pywats_client install-service --instance-id default

# Start service
sc start "pyWATS Client Service - default"

# Launch GUI when needed
python -m pywats_client gui --instance-id default
```

### For Developers

#### Code Changes Required

**Before (v1.x)**: GUI created embedded services
```python
from pywats_client.app import pyWATSApplication
from pywats_client.gui.main_window import MainWindow

# Old: GUI owns the application
app = pyWATSApplication(config)
window = MainWindow(config, app)
window.show()
```

**After (v2.0)**: GUI connects via IPC
```python
from pywats_client.gui.main_window import MainWindow
from pywats_client.service.ipc_client import ServiceIPCClient

# New: GUI connects to independent service
window = MainWindow(config)  # No app parameter!
window.show()

# Service runs separately
# Access via IPC: window._ipc_client
```

#### Page Updates

**Before**: Pages received `facade` parameter
```python
class MyPage(BasePage):
    def __init__(self, config, parent, *, facade=None):
        super().__init__(config, parent, facade=facade)
        self.facade.api  # Access API via facade
```

**After**: Pages access service via IPC
```python
class MyPage(BasePage):
    def __init__(self, config, parent):
        super().__init__(config, parent)  # No facade!
        # Access service via parent window's IPC client
        ipc_client = self.parent()._ipc_client
        status = ipc_client.get_status()
```

## Key Differences

### Service Independence
- ✅ Service runs 24/7 without GUI
- ✅ GUI can launch/exit freely
- ✅ Crash-proof: file-based queue survives restarts
- ✅ Multiple GUIs can connect to one service

### Configuration
- Same config files (`%APPDATA%\pyWATS_Client\config_{instance}.json`)
- Config hot-reload: service detects changes automatically
- No migration of existing configs needed

### Converters
- Managed by service process
- Auto-scaling worker pool (1-50 workers)
- Workers auto-shutdown after idle time

### Reports
- File-based state machine (`.queued`, `.processing`, `.error`, `.completed`)
- Queue persists across crashes
- Automatic timeout recovery

### IPC Communication
- Protocol: JSON over Qt LocalSocket
- Socket name: `pyWATS_Service_{instance_id}`
- Commands: `get_status`, `get_config`, `ping`, `stop`

## Compatibility

### Deprecated (still works, but not recommended)

**Old command** (launches GUI with embedded services):
```bash
python -m pywats_client
```
⚠️ This still works for backward compatibility but is deprecated.

**Better**: Use separate service + GUI:
```bash
# Terminal 1: Service
python -m pywats_client service

# Terminal 2: GUI  
python -m pywats_client gui
```

### Removed Features

- ❌ `pyWATSApplication` in GUI process (use service instead)
- ❌ `AppFacade` wrapper (use IPC client)
- ❌ Auto-start on GUI launch (start service separately)

## Troubleshooting

### GUI shows "Service not running"

**Solution**: Start the service first
```bash
python -m pywats_client service --instance-id default
```

### Service won't start

**Check logs**:
- Windows: `%APPDATA%\pyWATS_Client\service.log`
- Linux: `~/.config/pywats_client/service.log`

**Common issues**:
- Another instance running on same socket
- Missing dependencies: `pip install pywats-api[client]`
- Config file errors

### GUI can't connect to service

**Verify service is running**:
```powershell
# Windows
Get-Process python | Where-Object {$_.CommandLine -like "*service*"}

# Or check socket
Test-Path "\\.\pipe\pyWATS_Service_default"  # Named pipe on Windows
```

**Try reconnecting**:
1. Close GUI
2. Restart service
3. Launch GUI again

### Converters not processing files

**Check service status via GUI**:
1. Open GUI
2. Check "Converters" tab
3. Verify converters are "Running"
4. Check error folder for failed files

**Check service logs**:
```bash
tail -f ~/.config/pywats_client/service.log  # Linux
Get-Content %APPDATA%\pyWATS_Client\service.log -Tail 50 -Wait  # Windows
```

## Benefits of New Architecture

### Reliability
- ✅ Service survives GUI crashes
- ✅ File-based queue survives service crashes  
- ✅ Automatic recovery from timeouts
- ✅ No lost reports

### Performance
- ✅ Auto-scaling workers (1-50)
- ✅ Efficient resource usage
- ✅ Parallel file processing
- ✅ Minimal overhead when idle

### Maintainability
- ✅ Clean separation of concerns
- ✅ Simple IPC protocol
- ✅ Easy to debug (file-based state)
- ✅ Matches proven C# architecture

### Deployment
- ✅ Windows Service support
- ✅ Linux systemd support
- ✅ macOS launchd support
- ✅ Docker-ready

## Rollback Plan

If you need to rollback to v1.x architecture:

1. **Stop new service**:
   ```bash
   # Send stop command via IPC
   python -c "from pywats_client.service.ipc_client import ServiceIPCClient; c=ServiceIPCClient('default'); c.connect(); c.stop_service()"
   ```

2. **Checkout previous version**:
   ```bash
   git checkout v1.x
   pip install -e .
   ```

3. **Launch old way**:
   ```bash
   python -m pywats_client  # Old embedded mode
   ```

## Support

- **Documentation**: `docs/service/README.md`
- **C# Reference**: `docs/CLIENT_ANALYSIS_REPORT.md`
- **Issues**: GitHub Issues
- **Architecture**: Service follows C# WATS Client patterns

---

**Questions?** Check the comprehensive architecture docs in `src/pywats_client/service/README.md`
