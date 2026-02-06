# Platform Independence Analysis - pywats_client

**Date:** February 4, 2026  
**Purpose:** Document existing platform-independent patterns to follow in GUI framework

---

## 📋 Executive Summary

The existing `pywats_client/` implementation demonstrates excellent platform independence through:
- **Abstraction layers** for OS-specific functionality
- **Async-first architecture** with sync wrappers
- **Configuration-driven** behavior (JSON files in user directories)
- **Service abstraction** (systemd, Windows Service, launchd handled separately)

**Key Takeaway**: GUI framework should follow these same patterns and NOT reinvent platform-specific code.

---

## 🏗️ Architecture Patterns Found

### 1. Service Layer (Async-First)

**Files:**
- `service/async_client_service.py` - Async source of truth
- `service/client_service.py` - Thin sync wrapper
- `service/windows_service.py` - Windows-specific wrapper
- `service/service_tray.py` - System tray (platform-agnostic via Qt)

**Pattern:**
```python
# Async implementation (source of truth)
class AsyncClientService:
    async def start(self): ...
    async def stop(self): ...
    async def run(self): ...

# Sync wrapper (convenience)
class ClientService:
    def __init__(self):
        self._async = AsyncClientService()
    
    def start(self):
        asyncio.run(self._async.start())
```

**GUI Implication**: Use async API calls, avoid blocking UI thread.

---

### 2. Configuration Management

**Files:**
- `core/config.py` - Platform-aware config paths
- Uses `~/.pywats/` on Linux/macOS
- Uses `%APPDATA%/pywats/` on Windows (likely via Path.home())

**Pattern:**
```python
from pathlib import Path

config_dir = Path.home() / ".pywats" / "client"
config_file = config_dir / "config.json"
```

**GUI Implication**: Already using this in `ConfiguratorConfig` - good!

---

### 3. IPC (Inter-Process Communication)

**Files:**
- `service/async_ipc_server.py` - IPC server
- `service/async_ipc_client.py` - IPC client
- `service/ipc_protocol.py` - Protocol definition

**Pattern:**
- Uses asyncio streams (platform-agnostic)
- JSON-based protocol
- Unix sockets on Linux/macOS, Named pipes on Windows (handled by asyncio)

**GUI Implication**: If GUI needs to talk to service, use IPC client (already abstracted).

---

### 4. Queue Management

**Files:**
- `queue/async_pending_queue.py` - Async queue operations
- Uses SQLite (platform-agnostic)
- File-based persistence

**Pattern:**
- SQLite for queue storage (works everywhere)
- File watchers for directory monitoring (platform-specific handled by watchdog library likely)

**GUI Implication**: No special handling needed - queue is abstracted.

---

### 5. Converter Framework

**Files:**
- `converters/` - File format conversion
- Runs in isolated process (subprocess)
- Platform-agnostic execution

**Pattern:**
```python
# Run converter in isolated process
result = subprocess.run([sys.executable, converter_script, input_file])
```

**GUI Implication**: Converters work as-is, no GUI changes needed.

---

## 🚫 What GUI Framework Should NOT Do

Based on existing patterns:

1. **DO NOT implement service control directly**
   - Use IPC to communicate with running service
   - Don't try to start/stop services from GUI
   - Let service manager handle OS-specific stuff

2. **DO NOT access queue database directly**
   - Use service IPC API to query queue status
   - Don't open SQLite files from GUI

3. **DO NOT handle platform-specific paths**
   - Use `Path.home()` and `.pywats/` pattern
   - Don't check `sys.platform` unless absolutely necessary

4. **DO NOT block UI thread with async operations**
   - Use QThread for long-running operations
   - Use Qt signals/slots for async completion

---

## ✅ What GUI Framework SHOULD Do

Based on analysis of existing code:

1. **Use IPC Client for Service Communication**
   ```python
   from pywats_client.service.async_ipc_client import AsyncIPCClient
   
   # In QThread worker:
   client = AsyncIPCClient(instance_id="default")
   status = await client.get_status()
   ```

2. **Follow Configuration Pattern**
   ```python
   # Already doing this:
   config_dir = Path.home() / ".pywats" / "configurator"
   config_file = config_dir / "config.json"
   ```

3. **Use Qt's Platform Abstraction**
   - File dialogs: `QFileDialog` (platform-native)
   - System tray: `QSystemTrayIcon` (works everywhere)
   - Notifications: Qt notifications (platform-aware)

4. **Keep Simple**
   - Config forms (text fields, dropdowns)
   - Status displays (labels, progress bars)
   - Log viewers (text widgets)
   - Simple charts (matplotlib/pyqtgraph embedded)

---

## 🎯 Recommended Implementation Strategy

### For Configurator GUI:

1. **Connection Tab** → Just edit config file (already doing this ✅)
2. **Station Tab** → Edit config file (already doing this ✅)
3. **Service Control** → Use IPC client to send commands to running service
4. **Logs Tab** → Read log file from `~/.pywats/client/client.log`

### For AI Chat:

1. **Data Queries** → Use pyWATS API (async calls in QThread)
2. **LLM Calls** → OpenAI API (async in QThread)
3. **Charts** → Matplotlib embedded in Qt widget

### General Pattern:

```python
# In main window:
class MainWindow(BaseMainWindow):
    def on_action(self):
        worker = Worker(self.do_async_work)
        worker.signals.finished.connect(self.on_complete)
        worker.start()
    
    async def do_async_work(self):
        # Use pyWATS API or IPC client
        result = await async_operation()
        return result
    
    def on_complete(self, result):
        # Update UI (on main thread)
        self.label.setText(str(result))
```

---

## 📊 Service Control - IPC Approach

**Instead of direct service control, use IPC:**

```python
# In service control tab (future implementation):
from pywats_client.service.async_ipc_client import AsyncIPCClient

class ServiceControlWorker(QThread):
    status_updated = Signal(dict)
    
    async def get_status(self):
        try:
            client = AsyncIPCClient(instance_id="default")
            status = await client.get_status()
            return status
        except Exception as e:
            return {"error": str(e)}
    
    def run(self):
        status = asyncio.run(self.get_status())
        self.status_updated.emit(status)
```

**Benefits:**
- No platform-specific code in GUI
- Service handles all OS differences
- GUI just displays status
- Clean separation of concerns

---

## 🚀 Action Items for GUI Framework

1. ✅ **Configuration** - Already using platform-agnostic paths
2. ✅ **Base Classes** - Already minimal (good!)
3. ⏸️ **Service Control** - Implement IPC client wrapper (future)
4. ⏸️ **Log Viewer** - Read from `~/.pywats/{app}/app.log` (future)
5. ❌ **Advanced Features** - Out of scope (simple GUIs only)

---

## 📝 Summary for Agent

**When implementing GUI features:**

1. Check if `pywats_client/` already has the functionality
2. Use IPC client to talk to service (don't reimplement)
3. Use `Path.home() / ".pywats"` for config
4. Use Qt abstractions (QFileDialog, QThread, etc.)
5. Keep it simple - forms, buttons, status displays
6. Don't touch service layer code

**Platform independence is already handled** - just don't break it!

---

**Reference Files:**
- `src/pywats_client/service/async_client_service.py` - Async service
- `src/pywats_client/service/async_ipc_client.py` - IPC communication
- `src/pywats_client/core/config.py` - Configuration patterns
- `src/pywats_client/service/service_tray.py` - Qt system tray example
