# pyWATS Client Architecture

**Version:** 1.3.0 (Service/GUI Separation)  
**Last Updated:** January 2026  
**Audience:** Client developers, advanced users, troubleshooters

---

## Overview

The pyWATS Client is a **background service** with optional **GUI frontend** for managing test station automation. Starting with v1.3.0, the client uses a **separate service and GUI architecture** with inter-process communication (IPC), enabling true headless operation and better reliability.

**Key Features:**
- **Headless operation:** Service runs independently without GUI
- **IPC communication:** GUI communicates with service via Qt LocalSocket
- **Multi-instance:** Run multiple isolated clients on same machine
- **Crash resilience:** Service continues running even if GUI crashes
- **Platform support:** Windows, Linux, macOS, Docker

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Service Components](#service-components)
3. [Async Architecture](#async-architecture) *(NEW)*
4. [IPC Communication](#ipc-communication)
5. [Queue System](#queue-system)
6. [Converter System](#converter-system)
7. [File Monitoring](#file-monitoring)
8. [Instance Management](#instance-management)
9. [Configuration System](#configuration-system)
10. [Service Modes](#service-modes)
11. [Testing Architecture](#testing-architecture)

---

## Architecture Overview

### Layered Design

```
┌────────────────────────────────────────────────────────────┐
│                     GUI Process (Optional)                 │
│  • PySide6/Qt application                                  │
│  • ServiceIPCClient                                        │
│  • Sends commands, receives updates                        │
└────────────────────────────────────────────────────────────┘
                         ↕ IPC (LocalSocket)
┌────────────────────────────────────────────────────────────┐
│                    Service Process                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              ClientService                           │  │
│  │  • ServiceStatus management                          │  │
│  │  • Lifecycle coordination                            │  │
│  │  • pyWATS API client                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │PendingWatcher│  │ConverterPool │  │PersistentQueue │  │
│  │              │  │              │  │                │  │
│  │• File monitor│  │• Worker mgmt │  │• SQLite DB     │  │
│  │• Periodic    │  │• 1-50 workers│  │• Crash recovery│  │
│  │• Submit queue│  │• Converters  │  │• Retry logic   │  │
│  └──────────────┘  └──────────────┘  └────────────────┘  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              IPCServer                               │  │
│  │  • Qt LocalSocket server                             │  │
│  │  • Socket: pyWATS_Service_{instance_id}              │  │
│  │  • JSON command/response protocol                    │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Component Interactions

```
GUI                Service           Queue              WATS
 │                    │                │                  │
 │──Start Command────▶│                │                  │
 │                    │──Initialize───▶│                  │
 │                    │                │                  │
 │                    │◀─Queue Ready───│                  │
 │◀─Status Update────│                │                  │
 │                    │                │                  │
 │                    │   [File appears in watch folder]   │
 │                    │                │                  │
 │                    │──Add Report───▶│                  │
 │◀─File Processed───│                │                  │
 │                    │                │                  │
 │                    │                │──Submit Report──▶│
 │                    │                │◀─Success─────────│
 │                    │◀─Complete──────│                  │
 │◀─Status Update────│                │                  │
```

---

## Service Components

### ClientService

**Purpose:** Main service controller and lifecycle manager

**Location:** `src/pywats_client/service/client_service.py`

**ServiceStatus States:**
- `STOPPED` - Not running
- `START_PENDING` - Initializing
- `RUNNING` - Active and operational
- `STOP_PENDING` - Shutting down
- `PAUSED` - Temporarily paused (reserved for future use)

**Key Responsibilities:**
1. Initialize and coordinate all components
2. Manage service lifecycle
3. Provide pyWATS API client access
4. Track connection status
5. Handle start/stop/pause commands

**Code Structure:**
```python
class ClientService:
    def __init__(self, config: ClientConfig):
        self.config = config
        self.status = ServiceStatus.STOPPED
        self._api_client: Optional[pyWATS] = None
        self._pending_watcher: Optional[PendingWatcher] = None
        self._converter_pool: Optional[ConverterPool] = None
    
    async def start(self):
        """Start the service and all components"""
        self.status = ServiceStatus.START_PENDING
        
        # Initialize API client
        self._api_client = self._create_api_client()
        
        # Start queue watcher
        self._pending_watcher = PendingWatcher(...)
        await self._pending_watcher.async_init()
        
        # Start converter pool
        self._converter_pool = ConverterPool(...)
        
        self.status = ServiceStatus.RUNNING
    
    async def stop(self):
        """Stop the service gracefully"""
        self.status = ServiceStatus.STOP_PENDING
        
        # Stop components in reverse order
        if self._pending_watcher:
            await self._pending_watcher.dispose()
        
        self.status = ServiceStatus.STOPPED
```

**API Status Tracking:**
```python
def get_api_status(self) -> str:
    """Get current API connection status"""
    if not self._api_client:
        return "Disconnected"
    
    try:
        # Test connection with quick API call
        version = self._api_client.app.get_version()
        return "Online"
    except Exception:
        return "Offline"
```

### PendingWatcher

**Purpose:** Monitor and submit queued reports

**Location:** `src/pywats_client/service/pending_watcher.py`

**Key Features:**
1. **File system monitoring:** Watches pending reports directory
2. **Periodic checking:** Timer-based check every 5 minutes
3. **Submission lock:** Prevents concurrent uploads
4. **Async initialization:** Non-blocking startup

**Workflow:**
```
┌─────────────────────┐
│ Pending Directory   │
│ - report1.json      │
│ - report2.json      │
└─────────────────────┘
          │
          ▼
┌─────────────────────┐      ┌──────────────────┐
│  File System Event  │─────▶│ Submission Lock  │
│  or Periodic Timer  │      │ (Prevent overlap)│
└─────────────────────┘      └──────────────────┘
          │                           │
          ▼                           ▼
┌─────────────────────┐      ┌──────────────────┐
│ Read Report JSON    │      │  Submit to WATS  │
└─────────────────────┘      └──────────────────┘
          │                           │
          ▼                           ▼
┌─────────────────────┐      ┌──────────────────┐
│ Move to Processing  │─────▶│  On Success:     │
│                     │      │  Move to Complete│
└─────────────────────┘      └──────────────────┘
```

**Code Structure:**
```python
class PendingWatcher:
    def __init__(self, queue_dir: Path, api_client: pyWATS):
        self.queue_dir = queue_dir
        self.api_client = api_client
        self._timer = None
        self._submission_lock = asyncio.Lock()
        self._disposed = False
    
    async def async_init(self):
        """Initialize file watcher and start timer"""
        # Set up file system watcher
        self._observer = Observer()
        self._observer.schedule(
            self._event_handler,
            str(self.queue_dir / "pending"),
            recursive=False
        )
        self._observer.start()
        
        # Start periodic check
        self._timer = asyncio.create_task(self._periodic_check())
    
    async def _periodic_check(self):
        """Check for pending reports every 5 minutes"""
        while not self._disposed:
            await asyncio.sleep(300)  # 5 minutes
            await self._submit_pending_reports()
    
    async def _submit_pending_reports(self):
        """Submit all pending reports with lock"""
        async with self._submission_lock:
            # Process pending reports...
            pass
    
    async def dispose(self):
        """Clean shutdown"""
        self._disposed = True
        if self._observer:
            self._observer.stop()
            self._observer.join()
```

### ConverterPool

**Purpose:** Manage converter workers and execution

**Location:** `src/pywats_client/service/converter_pool.py`

**Configuration:**
- `max_converter_workers`: 1-50 (default: 10)
- Worker count bounded to prevent resource exhaustion

**Responsibilities:**
1. Manage worker threads/processes
2. Distribute converter tasks
3. Maintain converter registry
4. Handle pending conversion queue

**Code Structure:**
```python
class ConverterPool:
    def __init__(self, max_workers: int = 10):
        self.max_workers = max(1, min(50, max_workers))
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self._converters: List[Converter] = []
        self._pending_queue: Queue = Queue()
        self._dispose_flag = False
    
    def add_converter(self, converter: Converter):
        """Register a converter"""
        self._converters.append(converter)
    
    def submit_conversion(self, file_path: Path, converter: Converter):
        """Submit file for conversion"""
        future = self._executor.submit(
            self._convert_file,
            file_path,
            converter
        )
        return future
    
    def _convert_file(self, file_path: Path, converter: Converter):
        """Execute conversion (runs in worker thread)"""
        try:
            source = ConverterSource(file_path)
            result = converter.convert(source, context={})
            return result
        except Exception as e:
            return ConverterResult.failure(str(e))
    
    def dispose(self):
        """Shutdown pool"""
        self._dispose_flag = True
        self._executor.shutdown(wait=True)
```

---

## Async Architecture

Starting with v1.4.0, pyWATS Client includes an **async-first architecture** as an alternative to the traditional threading-based approach. The async architecture uses Python's `asyncio` for efficient concurrent I/O with a single thread.

### Benefits

| Aspect | Threading (Traditional) | Asyncio (New) |
|--------|------------------------|---------------|
| Concurrency | Thread pool (1-50 workers) | Single thread, async tasks |
| API Calls | Blocking, one per thread | Non-blocking, multiplexed |
| Resource Usage | Higher (thread overhead) | Lower (coroutines are lightweight) |
| Complexity | Race conditions, locks | Event loop, no locks |
| GUI Integration | QThread signals | qasync event loop |

### Async Components

#### AsyncClientService

**Location:** `src/pywats_client/service/async_client_service.py`

The main async service controller, replacing `ClientService` for async-first deployments.

```python
from pywats_client.service import AsyncClientService

# Create and run the async service
service = AsyncClientService()
await service.run()  # Blocks until shutdown
```

**Key Features:**
- Uses `AsyncWATS` instead of `pyWATS` for non-blocking API calls
- All timers run as `asyncio.Task` instead of `QTimer`
- Configuration hot-reload via async file watcher
- Graceful shutdown with task cancellation

#### AsyncPendingQueue

**Location:** `src/pywats_client/service/async_pending_queue.py`

Concurrent report upload queue with bounded parallelism.

```python
from pywats_client.service import AsyncPendingQueue

queue = AsyncPendingQueue(
    api=async_wats,
    reports_dir=Path("/var/lib/pywats/pending"),
    max_concurrent=5  # 5 concurrent uploads
)
await queue.run()
```

**Concurrency Model:**
```
┌─────────────────────────────────────────────────────────┐
│                  AsyncPendingQueue                       │
│                                                          │
│  ┌───────────────┐   ┌─────────────────────────────┐    │
│  │ File Watcher  │──▶│  asyncio.Semaphore(5)       │    │
│  │ (watchfiles)  │   │                              │    │
│  └───────────────┘   │  Task 1: submit_report()    │    │
│                      │  Task 2: submit_report()    │────▶│ WATS
│  ┌───────────────┐   │  Task 3: submit_report()    │    │  API
│  │ Periodic Scan │──▶│  Task 4: submit_report()    │    │
│  │ (60s timer)   │   │  Task 5: submit_report()    │    │
│  └───────────────┘   └─────────────────────────────┘    │
│                                                          │
│  [waiting]: report6.json, report7.json, ...              │
└─────────────────────────────────────────────────────────┘
```

#### AsyncConverterPool

**Location:** `src/pywats_client/service/async_converter_pool.py`

Concurrent file conversion with semaphore-limited workers.

```python
from pywats_client.service import AsyncConverterPool

pool = AsyncConverterPool(
    config=client_config,
    api=async_wats,
    max_concurrent=10  # 10 concurrent conversions
)
await pool.run()
```

**Features:**
- Watches input directories for new files
- Runs converters concurrently (up to max_concurrent)
- Auto-moves converted files to pending queue
- Supports all converter types (Python, DLL, process)

### GUI Integration (qasync)

For GUI mode, the async service integrates with Qt using `qasync`:

```python
import qasync
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)

# Run async service alongside Qt
async def main():
    service = AsyncClientService()
    await service.run()

with loop:
    loop.run_until_complete(main())
```

#### AsyncAPIMixin

Helper mixin for GUI pages to make async API calls without blocking the UI:

```python
from pywats_client.gui.async_api_mixin import AsyncAPIPageMixin

class ProductionPage(AsyncAPIPageMixin, BasePage):
    def _lookup_unit(self, part_number: str):
        # Automatically handles async/sync detection
        self.run_api_call(
            api_call=lambda api: api.production.lookup_production_unit(part_number),
            on_success=self._on_lookup_success,
            on_error=self._on_lookup_error
        )
```

### Migration Path

To migrate from sync to async architecture:

1. **Replace imports:**
   ```python
   # Before
   from pywats import pyWATS
   from pywats_client.service import ClientService
   
   # After
   from pywats import AsyncWATS
   from pywats_client.service import AsyncClientService
   ```

2. **Update entry point:**
   ```python
   # Before (threading)
   service = ClientService()
   service.start()
   
   # After (asyncio)
   service = AsyncClientService()
   asyncio.run(service.run())
   ```

3. **GUI pages:** Use `AsyncAPIPageMixin` for non-blocking API calls

### Migrated GUI Pages

The following GUI pages now use `AsyncAPIPageMixin` for non-blocking API calls:

| Page | File | Status |
|------|------|--------|
| Production | `production.py` | ✅ Fully async |
| Asset | `asset.py` | ✅ Uses mixin |
| Product | `product.py` | ✅ Uses mixin |
| RootCause | `rootcause.py` | ✅ Uses mixin |

Pages that don't make API calls (settings pages, dashboard, etc.) don't need async migration.

### When to Use Async

| Use Case | Recommendation |
|----------|---------------|
| Headless service | ✅ AsyncClientService |
| High-volume uploads | ✅ AsyncPendingQueue (5 concurrent) |
| Many converters | ✅ AsyncConverterPool |
| GUI application | ✅ With qasync |
| Legacy integration | Consider traditional ClientService |

---

## IPC Communication

### Protocol Overview

**Transport:** Qt LocalSocket (named pipe on Windows, Unix socket on Linux/Mac)

**Socket Name:** `pyWATS_Service_{instance_id}`
- Example: `pyWATS_Service_default`
- Example: `pyWATS_Service_production`

**Message Format:** JSON

### Command Structure

**Request (GUI → Service):**
```json
{
  "command": "get_status",
  "request_id": "uuid-here",
  "args": {
    "param1": "value1"
  }
}
```

**Response (Service → GUI):**
```json
{
  "success": true,
  "data": {
    "status": "RUNNING",
    "api_status": "Online",
    "pending_count": 5
  },
  "error": null,
  "request_id": "uuid-here"
}
```

### Supported Commands

| Command | Args | Response | Purpose |
|---------|------|----------|---------|
| `get_status` | None | ServiceStatus, API status | Check service state |
| `get_config` | None | ClientConfig | Get current configuration |
| `start` | None | Success/error | Start service |
| `stop` | None | Success/error | Stop service gracefully |
| `restart` | None | Success/error | Restart service |
| `ping` | None | "pong" | Health check |
| `get_queue_stats` | None | Pending/failed counts | Queue status |

### IPCServer Implementation

**Location:** `src/pywats_client/service/ipc_server.py`

**Code Structure:**
```python
class IPCServer(QObject):
    def __init__(self, instance_id: str, service: ClientService):
        super().__init__()
        self.instance_id = instance_id
        self.service = service
        self._server = QLocalServer()
        self._clients: List[QLocalSocket] = []
    
    def start(self) -> bool:
        """Start IPC server"""
        socket_name = f"pyWATS_Service_{self.instance_id}"
        
        # Remove stale socket
        QLocalServer.removeServer(socket_name)
        
        # Start listening
        if not self._server.listen(socket_name):
            return False
        
        self._server.newConnection.connect(self._on_new_connection)
        return True
    
    def _on_new_connection(self):
        """Handle new client connection"""
        client = self._server.nextPendingConnection()
        client.readyRead.connect(lambda: self._on_data_ready(client))
        self._clients.append(client)
    
    def _on_data_ready(self, client: QLocalSocket):
        """Process incoming command"""
        data = client.readAll().data().decode('utf-8')
        request = json.loads(data)
        
        # Dispatch command
        response = self._handle_command(request)
        
        # Send response
        client.write(json.dumps(response).encode('utf-8'))
        client.flush()
    
    def _handle_command(self, request: dict) -> dict:
        """Execute command and return response"""
        command = request.get("command")
        
        if command == "get_status":
            return {
                "success": True,
                "data": {
                    "status": self.service.status.name,
                    "api_status": self.service.get_api_status()
                },
                "request_id": request.get("request_id")
            }
        
        elif command == "ping":
            return {
                "success": True,
                "data": "pong",
                "request_id": request.get("request_id")
            }
        
        # ... other commands
```

### ServiceIPCClient (GUI Side)

**Location:** `src/pywats_client/gui/ipc_client.py`

**Code Structure:**
```python
class ServiceIPCClient(QObject):
    status_changed = Signal(str)
    
    def __init__(self, instance_id: str):
        super().__init__()
        self.instance_id = instance_id
        self._socket = QLocalSocket()
    
    def connect_to_service(self) -> bool:
        """Connect to service IPC socket"""
        socket_name = f"pyWATS_Service_{self.instance_id}"
        self._socket.connectToServer(socket_name)
        
        if not self._socket.waitForConnected(5000):
            return False
        
        self._socket.readyRead.connect(self._on_data_ready)
        return True
    
    def send_command(self, command: str, args: dict = None) -> dict:
        """Send command and wait for response"""
        request = {
            "command": command,
            "request_id": str(uuid.uuid4()),
            "args": args or {}
        }
        
        # Send request
        data = json.dumps(request).encode('utf-8')
        self._socket.write(data)
        self._socket.flush()
        
        # Wait for response
        if not self._socket.waitForReadyRead(10000):
            raise TimeoutError("No response from service")
        
        response_data = self._socket.readAll().data().decode('utf-8')
        return json.loads(response_data)
    
    def get_status(self) -> dict:
        """Get service status"""
        return self.send_command("get_status")
```

---

## Queue System

### PersistentQueue Architecture

**Purpose:** SQLite-backed report queue with crash recovery

**Location:** `src/pywats_client/queue/persistent_queue.py`

**Database Schema:**
```sql
CREATE TABLE reports (
    id TEXT PRIMARY KEY,
    report_data TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    attempts INTEGER DEFAULT 0,
    error TEXT,
    CHECK(status IN ('pending', 'processing', 'completed', 'failed'))
);

CREATE INDEX idx_status ON reports(status);
CREATE INDEX idx_created_at ON reports(created_at);
```

### Queue States

```
┌────────────┐
│  pending   │  Initial state, awaiting upload
└─────┬──────┘
      │
      ▼
┌────────────┐
│processing  │  Currently being uploaded
└─────┬──────┘
      │
      ├─Success─────▶┌───────────┐
      │              │ completed │  Successfully uploaded
      │              └───────────┘
      │
      └─Failure─────▶┌───────────┐
                     │  pending  │  Retry (if attempts < max)
                     └─────┬─────┘
                           │
                           └─Max retries───▶┌────────┐
                                            │ failed │  Permanent failure
                                            └────────┘
```

### Crash Recovery

**On service startup:**
1. Scan database for reports in `processing` state
2. Reset to `pending` state (interrupted uploads)
3. Increment attempt counter
4. Add to retry queue

**Implementation:**
```python
class PersistentQueue:
    def __init__(self, queue_dir: Path):
        self.queue_dir = queue_dir
        self.db_path = queue_dir / "queue.db"
        self._init_database()
        self._recover_crashed_reports()
    
    def _recover_crashed_reports(self):
        """Reset processing reports to pending on startup"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE reports 
            SET status = 'pending',
                attempts = attempts + 1,
                updated_at = ?
            WHERE status = 'processing'
        """, (datetime.now(),))
        
        recovered = cursor.rowcount
        conn.commit()
        conn.close()
        
        if recovered > 0:
            logger.info(f"Recovered {recovered} crashed reports")
    
    def add(self, report_data: dict) -> str:
        """Add report to queue"""
        report_id = str(uuid.uuid4())
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO reports (id, report_data, status, created_at, updated_at)
            VALUES (?, ?, 'pending', ?, ?)
        """, (report_id, json.dumps(report_data), datetime.now(), datetime.now()))
        
        conn.commit()
        conn.close()
        
        return report_id
    
    def get_pending(self, limit: int = 10) -> List[QueuedReport]:
        """Get pending reports for upload"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, report_data, attempts
            FROM reports
            WHERE status = 'pending'
            ORDER BY created_at
            LIMIT ?
        """, (limit,))
        
        reports = [
            QueuedReport(
                id=row[0],
                report_data=json.loads(row[1]),
                attempts=row[2]
            )
            for row in cursor.fetchall()
        ]
        
        conn.close()
        return reports
    
    def mark_processing(self, report_id: str):
        """Mark report as being uploaded"""
        self._update_status(report_id, 'processing')
    
    def mark_completed(self, report_id: str):
        """Mark report as successfully uploaded"""
        self._update_status(report_id, 'completed')
    
    def mark_failed(self, report_id: str, error: str, max_attempts: int = 3):
        """Mark report as failed, retry if attempts < max"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE reports
            SET status = CASE
                    WHEN attempts >= ? THEN 'failed'
                    ELSE 'pending'
                END,
                error = ?,
                attempts = attempts + 1,
                updated_at = ?
            WHERE id = ?
        """, (max_attempts, error, datetime.now(), report_id))
        
        conn.commit()
        conn.close()
```

### Retry Logic

**Configuration:**
- `max_retry_attempts`: Default 3
- `retry_interval_seconds`: Default 60

**Exponential Backoff:**
```python
def calculate_retry_delay(attempt: int) -> int:
    """Calculate delay with exponential backoff"""
    base_delay = 60  # 1 minute
    max_delay = 3600  # 1 hour
    
    delay = min(base_delay * (2 ** attempt), max_delay)
    return delay
```

---

## Converter System

### Converter Lifecycle

```
1. Configuration Load
   ↓
2. Module Import (dynamic)
   ↓
3. Class Instantiation
   ↓
4. File Pattern Registration
   ↓
5. Watch Folder Setup
   ↓
[File appears in watch folder]
   ↓
6. Event Triggered
   ↓
7. Debounce Wait (500ms)
   ↓
8. Pattern Match Check
   ↓
9. Converter.convert() Call
   ↓
10. Result Validation
   ↓
11. Queue Submission or Direct Upload
   ↓
12. Post-Processing (move/delete/archive)
```

### FileConverter Base Class

**Location:** `src/pywats_client/converters/file_converter.py`

**Abstract Methods:**
```python
class FileConverter(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Converter display name"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Converter version"""
        return "1.0.0"
    
    @property
    @abstractmethod
    def file_patterns(self) -> List[str]:
        """File patterns to match (glob)"""
        pass
    
    @abstractmethod
    def convert(self, source: ConverterSource, context: dict) -> ConverterResult:
        """Convert file to report"""
        pass
```

### Converter Configuration

```json
{
  "converters": [{
    "name": "CSV Converter",
    "module_path": "converters.csv_converter.CSVConverter",
    "watch_folder": "C:\\TestData\\Incoming",
    "done_folder": "C:\\TestData\\Done",
    "error_folder": "C:\\TestData\\Error",
    "file_patterns": ["*.csv"],
    "post_action": "move",
    "enabled": true,
    "arguments": {
      "delimiter": ",",
      "encoding": "utf-8"
    }
  }]
}
```

### Dynamic Loading

```python
def load_converter(module_path: str, arguments: dict) -> Converter:
    """Dynamically load converter class"""
    # Parse module path
    module_name, class_name = module_path.rsplit('.', 1)
    
    # Import module
    module = importlib.import_module(module_name)
    
    # Get class
    converter_class = getattr(module, class_name)
    
    # Instantiate with arguments
    converter = converter_class(**arguments)
    
    return converter
```

---

## File Monitoring

### Watchdog Integration

**Library:** `watchdog` (cross-platform file system events)

**Event Types:**
- `FileCreatedEvent` - New file appears
- `FileModifiedEvent` - File content changed
- `FileDeletedEvent` - File removed
- `FileMovedEvent` - File renamed/moved

### Debouncing

**Problem:** File system events fire multiple times during file write

**Solution:** Wait for write completion before processing

```python
class DebouncingEventHandler(FileSystemEventHandler):
    def __init__(self, callback, delay=0.5):
        self.callback = callback
        self.delay = delay  # 500ms
        self._timers = {}
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        # Cancel previous timer
        if event.src_path in self._timers:
            self._timers[event.src_path].cancel()
        
        # Start new timer
        timer = Timer(self.delay, self._process_file, [event.src_path])
        self._timers[event.src_path] = timer
        timer.start()
    
    def _process_file(self, file_path):
        """Called after debounce delay"""
        self.callback(file_path)
        if file_path in self._timers:
            del self._timers[file_path]
```

---

## Instance Management

### Multi-Instance Support

**Use Case:** Multiple test processes on same machine

**Example:**
- Instance "ict" - ICT testing
- Instance "fct" - Functional testing
- Instance "eol" - End-of-line testing

### Instance Isolation

**Separate per instance:**
- Configuration file: `config_{instance_id}.json`
- Queue directory: `reports_{instance_id}/`
- Log file: `client_{instance_id}.log`
- IPC socket: `pyWATS_Service_{instance_id}`
- Lock file: `instance_{instance_id}.lock`

### Lock File Mechanism

**Location:** `%TEMP%\pyWATS_Client\instance_{id}.lock`

**Content:**
```json
{
  "instance_id": "production",
  "instance_name": "Production Station",
  "pid": 12345,
  "started": "2026-01-26T10:30:00Z"
}
```

**Stale Lock Detection:**
```python
def _is_process_running(pid: int) -> bool:
    """Check if PID is still alive"""
    try:
        if sys.platform == "win32":
            # Windows: Check with tasklist
            output = subprocess.check_output(
                ["tasklist", "/FI", f"PID eq {pid}"],
                text=True
            )
            return str(pid) in output
        else:
            # Unix: Send signal 0
            os.kill(pid, 0)
            return True
    except (subprocess.CalledProcessError, OSError):
        return False
```

---

## Configuration System

See [Configuration Management](architecture.md#configuration-management) in main architecture doc.

**Key Points:**
- JSON-based configuration
- Machine-specific encryption for API tokens
- Environment variable overrides
- Multi-instance support

---

## Service Modes

### 1. GUI Mode (Default)
```bash
python -m pywats_client gui
```
- Service + GUI in same process (legacy)
- Full user interface
- Best for: Development, troubleshooting

### 2. Service Mode (Headless)
```bash
python -m pywats_client service --daemon
```
- Service only, no GUI
- Runs in background
- Best for: Production, servers

### 3. Separate Service + GUI
```bash
# Terminal 1: Start service
python -m pywats_client service

# Terminal 2: Start GUI (connects to service)
python -m pywats_client gui --connect
```
- Service and GUI in separate processes
- GUI can crash without affecting service
- Best for: Reliability, debugging

### 4. Windows Service
```powershell
pywats-client install-service --instance-id production
Start-Service pyWATS-Client-production
```
- Installed as Windows service
- Auto-start on boot
- Best for: Production Windows stations

### 5. Linux systemd
```bash
sudo systemctl enable pywats-client@production
sudo systemctl start pywats-client@production
```
- Managed by systemd
- Auto-restart on failure
- Best for: Production Linux stations

### 6. Docker Container
```bash
docker run -d ghcr.io/olreppe/pywats:client-headless
```
- Containerized deployment
- Reproducible environment
- Best for: Cloud, Kubernetes, server racks

---

## Testing Architecture

### Test Suite Overview

**Location:** `api-tests/client/`

**Coverage:** 85 tests (100% passing)

**Test Categories:**
1. **Configuration (18 tests)** - Config validation, serialization, lifecycle
2. **Converters (10 tests)** - Base classes, validation, results
3. **Queue (21 tests)** - Persistence, crash recovery, retry
4. **Service (17 tests)** - ClientService, PendingWatcher, ConverterPool
5. **IPC (10 tests)** - Communication, protocols, commands
6. **Integration (9 tests)** - End-to-end workflows

### Test Philosophy

**Principles:**
- Minimal mocking (use actual components where possible)
- Mock PySide6 at module level (avoid Qt runtime)
- Test business logic, not implementation details
- Focus on public interfaces

**Example Test:**
```python
def test_persistent_queue_crash_recovery(tmp_path):
    """Test that processing reports are recovered on restart"""
    queue = PersistentQueue(tmp_path)
    
    # Add report and mark as processing
    report_id = queue.add({"data": "test"})
    queue.mark_processing(report_id)
    
    # Simulate crash (create new queue instance)
    queue2 = PersistentQueue(tmp_path)
    
    # Verify report reset to pending
    pending = queue2.get_pending()
    assert len(pending) == 1
    assert pending[0].id == report_id
    assert pending[0].attempts == 1  # Incremented
```

### Running Tests

```bash
# Run all client tests
pytest api-tests/client/ -v

# Run specific category
pytest api-tests/client/test_service.py -v

# Run with coverage
pytest api-tests/client/ --cov=pywats_client --cov-report=html
```

---

## Troubleshooting

### Service Won't Start

**Check lock file:**
```bash
# Windows
dir "%TEMP%\pyWATS_Client\*.lock"

# Linux
ls /tmp/pyWATS_Client/*.lock
```

**Remove stale lock:**
```bash
python -m pywats_client unlock --instance-id production
```

### GUI Can't Connect to Service

**Verify service running:**
```bash
python -m pywats_client status --instance-id production
```

**Check socket name:**
```python
# Should be: pyWATS_Service_{instance_id}
# Windows: \\.\pipe\pyWATS_Service_production
# Linux: /tmp/pyWATS_Service_production
```

**Test IPC manually:**
```python
from pywats_client.gui.ipc_client import ServiceIPCClient

client = ServiceIPCClient("production")
if client.connect_to_service():
    response = client.send_command("ping")
    print(response)  # Should be "pong"
```

### Queue Growing Too Large

**Check failed reports:**
```bash
python -m pywats_client queue stats --instance-id production
```

**Retry failed:**
```bash
python -m pywats_client queue retry --instance-id production
```

**Clear completed:**
```bash
python -m pywats_client queue clean --instance-id production
```

---

## See Also

- **[Architecture Overview](architecture.md)** - System-wide architecture
- **[Integration Patterns](integration-patterns.md)** - Common workflows
- **[Client Installation](installation/client.md)** - Installation guide
- **[Service Deployment](installation/windows-service.md)** - Service setup

---

**Last Updated:** January 26, 2026  
**Version:** 1.3.0 (Separate Service/GUI Architecture)
