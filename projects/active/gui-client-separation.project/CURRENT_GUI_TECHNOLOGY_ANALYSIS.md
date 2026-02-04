# Current GUI Technology Analysis - src/pywats_client/gui

**Date:** February 4, 2026  
**Purpose:** Document what the current GUI actually uses (technology stack, patterns, shared components)

---

## 📊 Technology Stack (Current GUI)

### Core Technologies
- **PySide6 (Qt 6.x)** - Main GUI framework
- **qasync** - Qt-asyncio integration (bridges Qt event loop with asyncio)
- **asyncio** - For async API calls
- **QLocalSocket/QLocalServer** - Single-instance support
- **QSystemTrayIcon** - System tray integration (from service_tray.py)

### Key Libraries Used
```python
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QListWidget, QListWidgetItem, QLabel, QFrame, QPushButton,
    QMenu, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QSize, Signal, Slot, QTimer
from PySide6.QtGui import QAction, QCloseEvent, QIcon
```

---

## 🏗️ Architecture Patterns (Current GUI)

### 1. qasync Event Loop Integration
```python
# app.py - Uses qasync to bridge Qt and asyncio
import qasync
from PySide6.QtWidgets import QApplication

qt_app = QApplication(sys.argv)
loop = qasync.QEventLoop(qt_app)
asyncio.set_event_loop(loop)
```

**Implication**: New GUI apps SHOULD use qasync for async operations (already proven pattern).

---

### 2. Page-Based Navigation
```python
# main_window.py - Sidebar navigation + QStackedWidget
class MainWindow(QMainWindow):
    def __init__(self):
        self.sidebar = QListWidget()
        self.pages = QStackedWidget()
        
        # Pages: Dashboard, Setup, Connection, Converters, etc.
        self.pages.addWidget(DashboardPage())
        self.pages.addWidget(SetupPage())
```

**Implication**: New apps CAN use tabs OR pages (simpler apps might just use tabs).

---

### 3. AsyncAPIRunner (Composition Pattern)
```python
# async_api_runner.py - Bridges GUI and AsyncWATS API
class AsyncAPIRunner:
    def __init__(self, facade):
        self._facade = facade
    
    def run(
        self,
        api_call: Callable,
        on_success: Callable,
        on_error: Callable,
        task_name: str = "Loading..."
    ):
        # Runs async API calls from sync Qt slots
        # Shows loading indicator
        # Handles errors via ErrorHandlingMixin
```

**Pattern:**
- Page calls `self.async_api.run(lambda api: api.asset.get_assets(), ...)`
- Runner executes in background
- Callbacks fired on main thread
- Loading states managed automatically

**Implication**: New framework SHOULD provide similar async helper (but simpler for config/alarming apps).

---

### 4. ErrorHandlingMixin
```python
# error_mixin.py - Centralized error handling
class ErrorHandlingMixin:
    def handle_error(self, error: Exception, context: str = ""):
        # Shows appropriate QMessageBox based on exception type
        # - AuthenticationError → "Please log in again"
        # - ValidationError → "Invalid input: {details}"
        # - ConnectionError → "Cannot connect to server"
        # - ServerError → "Server error: {details}"
```

**Implication**: New framework SHOULD provide similar error handling utility.

---

### 5. BasePage (Abstract Page Class)
```python
# pages/base.py - Base class for all pages
class BasePage(QWidget):
    def __init__(self, config: ClientConfig, async_api_runner: AsyncAPIRunner):
        self.config = config
        self.async_api = async_api_runner
        self.setup_ui()
    
    def setup_ui(self):
        # Subclasses implement
        raise NotImplementedError
    
    def on_show(self):
        # Called when page becomes visible
        pass
```

**Implication**: New framework already has BaseMainWindow - consider adding BasePage for tabbed apps.

---

### 6. IPC Client Integration
```python
# main_window.py - Communicates with background service
class MainWindow(QMainWindow):
    def __init__(self, config):
        self._ipc_client = AsyncIPCClient(config.instance_id)
        self._service_connected = False
    
    async def _connect_to_service(self):
        await self._ipc_client.connect()
        status = await self._ipc_client.get_status()
```

**Implication**: New apps CAN use IPC client for service communication (platform-independent).

---

### 7. Dark Theme with QSS
```python
# styles.py - Qt StyleSheet
DARK_STYLESHEET = """
QMainWindow {
    background-color: #2b2b2b;
}
QPushButton {
    background-color: #3c3f41;
    color: #bbbbbb;
    border: 1px solid #555555;
}
...
"""

# Apply in app:
qt_app.setStyleSheet(DARK_STYLESHEET)
```

**Implication**: New framework CAN provide theme support (optional QSS files).

---

### 8. Single-Instance Support
```python
# app.py - Prevents multiple instances
server_name = f"pyWATS_Client_{instance_id}"
socket = QLocalSocket()
socket.connectToServer(server_name)

if socket.waitForConnected(500):
    # Another instance is running
    socket.write(b"ACTIVATE")
    return 0

# No existing instance - create server
server = QLocalServer()
server.listen(server_name)
```

**Implication**: New apps SHOULD support single-instance (prevent config conflicts).

---

## 🎯 Shared Components Available

### From pywats_client.gui (Current GUI)

1. **AsyncAPIRunner** - Async API call helper
2. **ErrorHandlingMixin** - Error dialog helper
3. **BasePage** - Page base class
4. **Styles** - Dark theme QSS
5. **SettingsDialog** - Settings dialog (reusable)
6. **LoginWindow** - Login dialog (reusable)
7. **Widgets** - ScriptEditor, NewConverterDialog

### From pywats_client.service

1. **AsyncIPCClient** - Service communication
2. **ClientConfig** - Configuration management
3. **ConnectionState** - Connection state tracking

### From pywats (API)

1. **AsyncWATS** - Async API client
2. **pyWATS** - Sync API client
3. **Exceptions** - Standard exceptions (AuthenticationError, etc.)

---

## ✅ What New Framework SHOULD Support

Based on current GUI analysis:

### 1. **qasync Integration** (CRITICAL)
- Bridge Qt event loop with asyncio
- Enables async API calls from Qt slots
- Already proven in production

```python
# BaseApplication should handle this
class BaseApplication(QApplication):
    def __init__(self, app_name: str, version: str):
        super().__init__(sys.argv)
        
        # Set up qasync event loop
        if HAS_QASYNC:
            self.loop = qasync.QEventLoop(self)
            asyncio.set_event_loop(self.loop)
```

### 2. **AsyncAPIRunner Equivalent** (HIGH PRIORITY)
- Simplified version for config/alarming apps
- Run async calls from sync slots
- Loading states
- Error handling

```python
# Framework helper
class AsyncHelper:
    def run_async(
        self, 
        coro: Coroutine, 
        on_success: Callable,
        on_error: Callable
    ):
        # Execute async coroutine from Qt slot
        # Call on_success(result) or on_error(exception)
```

### 3. **Error Handling** (HIGH PRIORITY)
- Reuse ErrorHandlingMixin or similar
- Standard error dialogs
- Context-aware messages

### 4. **Configuration Pattern** (ALREADY DONE ✅)
- `Path.home() / ".pywats" / {app_name}`
- JSON-based config
- Already implemented in ConfiguratorConfig

### 5. **IPC Client Access** (MEDIUM PRIORITY)
- For service communication
- Already abstracted in AsyncIPCClient
- New apps CAN use if needed

### 6. **Theme Support** (OPTIONAL)
- QSS stylesheet loading
- Dark/Light theme toggle
- Can copy from current GUI

### 7. **Single-Instance Support** (OPTIONAL)
- QLocalSocket/QLocalServer pattern
- Prevents config conflicts
- Can copy from current GUI

---

## 🚫 What New Framework Should NOT Do

Based on scope constraints:

1. ❌ **Advanced Data Grids** - Not needed for config/alarming
2. ❌ **Complex Charting** - Simple charts OK (matplotlib), advanced charting out of scope
3. ❌ **Real-time Monitoring** - Out of scope (simple status displays OK)
4. ❌ **Plugin System** - Out of scope
5. ❌ **Advanced Theming** - Simple QSS OK, theme engine out of scope

---

## 📋 Recommended Additions to Framework

### Minimal Additions (In Scope):

1. **AsyncHelper Class** - Simplified AsyncAPIRunner
   - Run async coroutines from Qt slots
   - Loading states (optional QProgressDialog)
   - Error handling (QMessageBox)

2. **ErrorDialog Utility** - Standard error display
   - Takes exception + context
   - Shows appropriate message
   - Logs error details

3. **Theme Support** - Basic QSS loading
   - `framework/themes/default.qss`
   - `framework/themes/dark.qss`
   - Load via `app.setStyleSheet()`

4. **Single-Instance Helper** - Prevent multiple instances
   - QLocalSocket/QLocalServer wrapper
   - Simple enable/disable flag

### Example Implementation:

```python
# framework/async_helper.py
from PySide6.QtCore import QObject, Signal, QThread
import asyncio

class AsyncWorker(QThread):
    finished = Signal(object)
    error = Signal(Exception)
    
    def __init__(self, coro):
        super().__init__()
        self.coro = coro
    
    def run(self):
        try:
            result = asyncio.run(self.coro)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(e)

class AsyncHelper:
    @staticmethod
    def run_async(coro, on_success, on_error):
        worker = AsyncWorker(coro)
        worker.finished.connect(on_success)
        worker.error.connect(on_error)
        worker.start()
        return worker
```

---

## 🎯 Summary for New Framework

**SHOULD Support (Already in Current GUI):**
- ✅ qasync event loop integration
- ✅ Async API calls from Qt slots (AsyncHelper)
- ✅ Error handling with context (ErrorDialog)
- ✅ Configuration management (Path.home()/.pywats/)
- ✅ IPC client access (AsyncIPCClient)
- ✅ Theme support (QSS loading)
- ✅ Single-instance support (QLocalSocket/QLocalServer)

**CAN Add (Reasonable Extensions):**
- ✅ Simplified AsyncHelper (simpler than AsyncAPIRunner)
- ✅ BasePage class for tabbed apps
- ✅ Common dialogs (Connection, Settings, About)
- ✅ Simple widgets (ValidatedLineEdit, StatusIndicator)

**Should NOT Add (Out of Scope):**
- ❌ Advanced data grids
- ❌ Complex charting libraries
- ❌ Real-time monitoring
- ❌ Plugin systems
- ❌ Advanced theme engines

---

**Conclusion**: The current GUI has everything we need. New framework should be a LIGHTER version of the same patterns, not a reinvention.

**Action**: Update agent instructions to reflect "same technology as current GUI + reasonable additions" rather than "minimalistic" (which was too vague).
