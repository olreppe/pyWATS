# pyWATS Core Architecture

This document describes the core functionality and architecture of the pyWATS system, excluding domain-specific features (like Process, Product, Analytics, etc.).

## Table of Contents

1. [System Overview](#system-overview)
2. [Three-Layer Architecture](#three-layer-architecture)
3. [pyWATS API (pywats)](#pywats-api-pywats)
4. [pyWATS Client (pywats_client)](#pywats-client-pywats_client)
5. [pyWATS Client GUI](#pywats-client-gui)
6. [Configuration Management](#configuration-management)
7. [File Watching and Converters](#file-watching-and-converters)
8. [Scheduled Tasks and Background Services](#scheduled-tasks-and-background-services)
9. [Data Synchronization and Persistence](#data-synchronization-and-persistence)
10. [Dependencies](#dependencies)

---

## System Overview

pyWATS is a three-layer system for connecting test stations to WATS (Web-based Automatic Test System) servers:

```
┌─────────────────────────────────────────────────────────────────┐
│                    pyWATS Client GUI                            │
│  (PySide6/Qt - Optional Desktop Application)                    │
│  - Login Window, Main Window, Settings Dialog                   │
│  - Page Navigation (Setup, Converters, S/N Handler, etc.)       │
│  - System Tray Integration                                      │
└─────────────────────────────────────────────────────────────────┘
                              │ Uses
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    pyWATS Client Service                        │
│  (pywats_client - Headless capable)                             │
│  - Connection Management & Monitoring                           │
│  - File Monitoring (Watchdog)                                   │
│  - Converter Processing                                         │
│  - Report Queue (Offline Storage)                               │
│  - Process Synchronization                                      │
│  - Instance Management (Multi-instance support)                 │
└─────────────────────────────────────────────────────────────────┘
                              │ Uses
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       pyWATS API                                │
│  (pywats - Core library)                                        │
│  - HTTP Client with Basic Auth                                  │
│  - Rate Limiting (500 req/min default)                          │
│  - Domain Services (Report, Product, Asset, etc.)               │
│  - Pydantic Models                                              │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP/REST
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      WATS Server                                │
│  (Cloud or On-Premise)                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Three-Layer Architecture

### Layer 1: pyWATS API (`src/pywats/`)

The foundation library providing HTTP communication with WATS servers.

**Responsibility:** REST API communication, authentication, models, rate limiting

### Layer 2: pyWATS Client (`src/pywats_client/`)

A service application that can run headless (no GUI) or with GUI.

**Responsibility:** Connection management, file watching, converters, offline queue, synchronization

### Layer 3: pyWATS Client GUI (`src/pywats_client/gui/`)

Optional Qt-based desktop application.

**Responsibility:** User interface, login flow, settings management, visual feedback

---

## pyWATS API (pywats)

**Location:** `src/pywats/`

### Core Components

#### HttpClient (`core/client.py`)

The central HTTP communication class:

```
┌─────────────────────────────────────────────┐
│               HttpClient                    │
├─────────────────────────────────────────────┤
│ Properties:                                 │
│ - base_url: str                             │
│ - token: str (Base64 encoded)               │
│ - timeout: float (default: 30s)             │
│ - verify_ssl: bool                          │
│ - rate_limiter: RateLimiter                 │
├─────────────────────────────────────────────┤
│ Methods:                                    │
│ - get(endpoint) → Response                  │
│ - post(endpoint, data) → Response           │
│ - put(endpoint, data) → Response            │
│ - patch(endpoint, data) → Response          │
│ - delete(endpoint) → Response               │
└─────────────────────────────────────────────┘
```

**Key Features:**
- Basic authentication via Authorization header
- Automatic URL path normalization
- Response wrapping with `Response` model
- No exception raising for HTTP errors (error handling delegated to repositories)
- Built-in rate limiting support

#### Response Model

```python
class Response(BaseModel):
    status_code: int
    data: Any           # Parsed JSON
    headers: Dict[str, str]
    raw: bytes
    
    # Computed properties
    is_success: bool    # 2xx
    is_error: bool      # 4xx or 5xx
    is_not_found: bool  # 404
    is_server_error: bool  # 5xx
    is_client_error: bool  # 4xx
    error_message: Optional[str]
```

#### Rate Limiter (`core/throttle.py`)

Thread-safe sliding window rate limiter:

```
┌─────────────────────────────────────────────┐
│              RateLimiter                    │
├─────────────────────────────────────────────┤
│ Configuration:                              │
│ - max_requests: int (default: 500)          │
│ - window_seconds: float (default: 60.0)     │
│ - enabled: bool                             │
├─────────────────────────────────────────────┤
│ Methods:                                    │
│ - acquire(timeout) → bool                   │
│ - wait_if_needed()                          │
├─────────────────────────────────────────────┤
│ Statistics:                                 │
│ - total_requests                            │
│ - total_wait_time                           │
│ - throttle_count                            │
└─────────────────────────────────────────────┘
```

**Usage:**
```python
from pywats.core.throttle import configure_throttling
configure_throttling(max_requests=500, window_seconds=60, enabled=True)
```

#### Retry Configuration (`core/retry.py`)

Automatic retry with exponential backoff for transient failures:

```
┌─────────────────────────────────────────────┐
│              RetryConfig                    │
├─────────────────────────────────────────────┤
│ Configuration:                              │
│ - enabled: bool (default: True)             │
│ - max_attempts: int (default: 3)            │
│ - base_delay: float (default: 1.0)          │
│ - max_delay: float (default: 30.0)          │
│ - jitter: bool (default: True)              │
│ - retry_methods: Set[str] (GET,PUT,DELETE)  │
│ - retry_status_codes: Set[int] (429,5xx)    │
├─────────────────────────────────────────────┤
│ Methods:                                    │
│ - should_retry_method(method) → bool        │
│ - should_retry_status(status) → bool        │
│ - calculate_delay(attempt) → float          │
│ - get_retry_after(response) → Optional[float]│
├─────────────────────────────────────────────┤
│ Statistics:                                 │
│ - total_retries                             │
│ - total_retry_time                          │
└─────────────────────────────────────────────┘
```

**Retries on:**
- `ConnectionError`, `TimeoutError` (network issues)
- HTTP 429 (Too Many Requests - respects Retry-After header)
- HTTP 500, 502, 503, 504 (server errors)

**Does NOT retry:**
- HTTP 400, 401, 403, 404, 409 (client errors)
- POST requests (not idempotent)

**Usage:**
```python
from pywats import pyWATS, RetryConfig

# Disable retry
api = pyWATS(..., retry_enabled=False)

# Custom configuration
config = RetryConfig(max_attempts=5, base_delay=2.0)
api = pyWATS(..., retry_config=config)

# Check statistics
print(api.retry_config.stats)
```

#### Station Concept (`core/station.py`)

Manages test station identity for reports:

```
┌─────────────────────────────────────────────┐
│                Station                      │
├─────────────────────────────────────────────┤
│ - name: str       (machineName in reports)  │
│ - location: str                             │
│ - purpose: str    (Production/Development) │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│            StationRegistry                  │
├─────────────────────────────────────────────┤
│ Manages multiple stations (hub mode):       │
│ - add(key, Station)                         │
│ - get(key) → Station                        │
│ - set_active(key)                           │
│ - get_active() → Station                    │
└─────────────────────────────────────────────┘
```

### Main API Class (`pywats.py`)

The `pyWATS` class is the primary entry point:

```python
from pywats import pyWATS

api = pyWATS(
    base_url="https://company.wats.com",
    token="your-api-token",
    station=Station("STATION-01", "Lab A", "Production")
)

# Access domain services
api.product      # ProductService
api.asset        # AssetService
api.production   # ProductionService
api.report       # ReportService
api.software     # SoftwareService
api.analytics    # AnalyticsService (also: api.app)
api.rootcause    # RootCauseService
```

### Architecture Pattern

Each domain follows a three-layer pattern:

```
Service (Business Logic)
    │
    ▼
Repository (Data Access)
    │
    ▼
HttpClient (HTTP Communication)
```

---

## pyWATS Client (pywats_client)

**Location:** `src/pywats_client/`

### Entry Point (`__main__.py`)

```bash
# GUI mode (default)
python -m pywats_client

# Headless mode
python -m pywats_client --no-gui

# CLI commands
pywats-client config show
pywats-client config init
pywats-client status
pywats-client start --daemon
```

### Core Application (`app.py`)

The `pyWATSApplication` class orchestrates all services:

```
┌───────────────────────────────────────────────────────────────┐
│                    pyWATSApplication                          │
├───────────────────────────────────────────────────────────────┤
│ Status: STOPPED | STARTING | RUNNING | STOPPING | ERROR       │
├───────────────────────────────────────────────────────────────┤
│ Services:                                                     │
│ ┌───────────────┐ ┌──────────────────┐ ┌──────────────────┐  │
│ │ConnectionSvc  │ │ProcessSyncSvc    │ │ReportQueueSvc    │  │
│ │               │ │                  │ │                  │  │
│ │- authenticate │ │- sync processes  │ │- queue reports   │  │
│ │- connect      │ │- sync levels     │ │- retry failed    │  │
│ │- health check │ │- sync prod grps  │ │- persist queue   │  │
│ │- reconnect    │ │- cache locally   │ │- upload online   │  │
│ └───────────────┘ └──────────────────┘ └──────────────────┘  │
│                                                               │
│ ┌───────────────────────────────────────────────────────────┐│
│ │                   ConverterManager                        ││
│ │ - Load Python converter modules                           ││
│ │ - Watch folders for new files (Watchdog)                  ││
│ │ - Process files through converters                        ││
│ │ - Submit to report queue                                  ││
│ └───────────────────────────────────────────────────────────┘│
├───────────────────────────────────────────────────────────────┤
│ Callbacks:                                                    │
│ - on_status_changed(ApplicationStatus)                        │
│ - on_error(ApplicationError)                                  │
└───────────────────────────────────────────────────────────────┘
```

### Core Client (`core/client.py`)

The `WATSClient` class provides a simpler alternative to `pyWATSApplication`:

```python
from pywats_client.core.client import WATSClient
from pywats_client.core.config import ClientConfig

config = ClientConfig.load("config.json")
client = WATSClient(config)

# Async usage
await client.start()
await client.stop()

# Or blocking mode
client.run()
```

### Services Layer (`services/`)

#### ConnectionService (`services/connection.py`)

Manages WATS server connection with persistent state:

```
┌─────────────────────────────────────────────────────────────┐
│                   ConnectionService                         │
├─────────────────────────────────────────────────────────────┤
│ Status: DISCONNECTED | CONNECTING | ONLINE | OFFLINE | ERROR│
├─────────────────────────────────────────────────────────────┤
│ Features:                                                   │
│ - Password-to-token authentication                          │
│ - Encrypted token storage (machine-specific key)            │
│ - Automatic health monitoring                               │
│ - Auto-reconnection when server comes back                  │
│ - Connection statistics tracking                            │
├─────────────────────────────────────────────────────────────┤
│ Methods:                                                    │
│ - authenticate(url, password, username)                     │
│ - connect() → bool                                          │
│ - disconnect()                                              │
│ - get_client() → pyWATS                                     │
├─────────────────────────────────────────────────────────────┤
│ Callbacks:                                                  │
│ - on_status_change(ConnectionStatus)                        │
└─────────────────────────────────────────────────────────────┘
```

**Connection States:**
- **NOT_CONNECTED**: No stored credentials
- **CONNECTED**: Authenticated and server reachable
- **OFFLINE**: Authenticated but server unreachable (credentials retained)

#### ProcessSyncService (`services/process_sync.py`)

Synchronizes reference data from WATS for offline access:

```
┌─────────────────────────────────────────────────────────────┐
│                  ProcessSyncService                         │
├─────────────────────────────────────────────────────────────┤
│ Syncs:                                                      │
│ - Processes (test operations)                               │
│ - Levels (test hierarchies)                                 │
│ - Product Groups                                            │
├─────────────────────────────────────────────────────────────┤
│ Features:                                                   │
│ - Periodic sync (configurable interval, default: 5 min)     │
│ - Local JSON cache in:                                      │
│   %APPDATA%\pyWATS_Client\cache\processes_cache.json        │
│ - Auto-sync when coming online                              │
├─────────────────────────────────────────────────────────────┤
│ Methods:                                                    │
│ - start() / stop()                                          │
│ - sync() → bool                                             │
│ - get_processes() → List[Dict]                              │
│ - get_levels() → List[Dict]                                 │
│ - get_product_groups() → List[Dict]                         │
└─────────────────────────────────────────────────────────────┘
```

#### ReportQueueService (`services/report_queue.py`)

Manages offline report storage and upload:

```
┌─────────────────────────────────────────────────────────────┐
│                  ReportQueueService                         │
├─────────────────────────────────────────────────────────────┤
│ Folders:                                                    │
│ - pending/    (awaiting upload)                             │
│ - failed/     (max retries exceeded)                        │
│ - completed/  (successfully uploaded)                       │
├─────────────────────────────────────────────────────────────┤
│ Features:                                                   │
│ - Queue reports when offline                                │
│ - Automatic upload when online                              │
│ - Retry with configurable attempts                          │
│ - Persistent queue (survives restarts)                      │
├─────────────────────────────────────────────────────────────┤
│ QueuedReport:                                               │
│ - report_id: UUID                                           │
│ - report_data: Dict (WSJF format)                           │
│ - status: PENDING | PROCESSING | FAILED | COMPLETED         │
│ - attempts: int                                             │
│ - error: str                                                │
├─────────────────────────────────────────────────────────────┤
│ Methods:                                                    │
│ - submit(report_data) → bool                                │
│ - get_pending_count() → int                                 │
│ - get_failed_reports() → List[QueuedReport]                 │
└─────────────────────────────────────────────────────────────┘
```

#### FileMonitor (`services/file_monitor.py`)

Watches folders for file system events:

```
┌─────────────────────────────────────────────────────────────┐
│                     FileMonitor                             │
├─────────────────────────────────────────────────────────────┤
│ Based on: watchdog library                                  │
├─────────────────────────────────────────────────────────────┤
│ MonitorRule:                                                │
│ - path: folder to watch                                     │
│ - converter_type: converter to use                          │
│ - recursive: watch subdirectories                           │
│ - delete_after_convert: auto-cleanup                        │
│ - auto_upload: submit to queue automatically                │
│ - file_pattern: glob pattern (e.g., "*.csv")                │
├─────────────────────────────────────────────────────────────┤
│ Events:                                                     │
│ - CREATED                                                   │
│ - MODIFIED                                                  │
│ - DELETED                                                   │
│ - MOVED                                                     │
├─────────────────────────────────────────────────────────────┤
│ Features:                                                   │
│ - Debouncing (avoid processing partial writes)              │
│ - Async operation                                           │
│ - Callback notifications                                    │
└─────────────────────────────────────────────────────────────┘
```

#### ConverterManager (`services/converter_manager.py`)

Manages file-to-report converters:

```
┌─────────────────────────────────────────────────────────────┐
│                   ConverterManager                          │
├─────────────────────────────────────────────────────────────┤
│ Uses: watchdog.Observer for file watching                   │
├─────────────────────────────────────────────────────────────┤
│ Converter Loading:                                          │
│ - Dynamic Python module loading                             │
│ - Modules must define ConverterBase subclass                │
│ - Arguments passed from config                              │
├─────────────────────────────────────────────────────────────┤
│ File Processing Flow:                                       │
│ 1. Watchdog detects file creation                           │
│ 2. Wait for file write completion (debounce)                │
│ 3. Check file patterns                                      │
│ 4. Call converter.convert(file_path)                        │
│ 5. Submit result to ReportQueueService                      │
│ 6. Move file to done/error folder                           │
└─────────────────────────────────────────────────────────────┘
```

### Instance Management (`core/instance_manager.py`)

Supports running multiple client instances on same machine:

```
┌─────────────────────────────────────────────────────────────┐
│                    InstanceLock                             │
├─────────────────────────────────────────────────────────────┤
│ File-based locking:                                         │
│ - Lock file: %TEMP%\pyWATS_Client\instance_{id}.lock        │
│ - Contains: instance_id, name, pid, started timestamp       │
│ - Stale lock detection (checks if PID still running)        │
├─────────────────────────────────────────────────────────────┤
│ Methods:                                                    │
│ - acquire(instance_name) → bool                             │
│ - release()                                                 │
│ - _is_process_running(pid) → bool                           │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   InstanceManager                           │
├─────────────────────────────────────────────────────────────┤
│ - get_running_instances() → List[Dict]                      │
│ - create_instance(name) → InstanceConfig                    │
└─────────────────────────────────────────────────────────────┘
```

### Encryption (`core/encryption.py`)

Machine-specific encryption for API tokens:

```
┌─────────────────────────────────────────────────────────────┐
│                      Encryption                             │
├─────────────────────────────────────────────────────────────┤
│ Uses: cryptography.fernet (symmetric encryption)            │
├─────────────────────────────────────────────────────────────┤
│ Machine ID Sources:                                         │
│ - Windows: HKLM\SOFTWARE\Microsoft\Cryptography\MachineGuid │
│ - Linux: /etc/machine-id                                    │
│ - Mac: IOPlatformUUID                                       │
├─────────────────────────────────────────────────────────────┤
│ Key Derivation:                                             │
│ - PBKDF2HMAC with SHA256                                    │
│ - Machine-specific salt                                     │
├─────────────────────────────────────────────────────────────┤
│ Functions:                                                  │
│ - encrypt_token(token) → encrypted_string                   │
│ - decrypt_token(encrypted) → token                          │
│ - get_machine_id() → str                                    │
└─────────────────────────────────────────────────────────────┘
```

**Security Note:** Tokens are encrypted with machine-specific keys, so encrypted tokens cannot be used on other machines.

---

## pyWATS Client GUI

**Location:** `src/pywats_client/gui/`

### Application Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   run_gui()     │───▶│  LoginWindow     │───▶│   MainWindow    │
│ (app.py)        │    │                  │    │                 │
│                 │    │ - URL input      │    │ - Sidebar nav   │
│ Check auth:     │    │ - Password input │    │ - Page stack    │
│ - Has token?    │    │ - Connect btn    │    │ - Status bar    │
│ - Valid state?  │    │                  │    │ - Tray icon     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### LoginWindow (`gui/login_window.py`)

Pre-authentication dialog:

```
┌─────────────────────────────────────────────────────────────┐
│                     LoginWindow                             │
├─────────────────────────────────────────────────────────────┤
│ Shown when:                                                 │
│ - First run (no stored credentials)                         │
│ - After logout                                              │
│ - Invalid stored credentials                                │
├─────────────────────────────────────────────────────────────┤
│ Fields:                                                     │
│ - Server URL (https://company.wats.com)                     │
│ - Password/API Token (masked)                               │
│ - Show password checkbox                                    │
│ - Remember connection checkbox                              │
│ - Instance selector (for multi-instance)                    │
├─────────────────────────────────────────────────────────────┤
│ Auth Flow:                                                  │
│ 1. Create ConnectionService with ConnectionConfig           │
│ 2. Call authenticate(url, password)                         │
│ 3. On success: encrypt token, save config, open MainWindow  │
└─────────────────────────────────────────────────────────────┘
```

### MainWindow (`gui/main_window.py`)

Main application window:

```
┌─────────────────────────────────────────────────────────────┐
│                      MainWindow                             │
├─────────────────────────────────────────────────────────────┤
│ Layout:                                                     │
│ ┌──────────┬──────────────────────────────────────────────┐ │
│ │ Sidebar  │              Content Area                    │ │
│ │          │         (QStackedWidget)                     │ │
│ │ - Setup  │                                              │ │
│ │ - Connect│    Pages loaded based on sidebar selection   │ │
│ │ - Convert│                                              │ │
│ │ - S/N    │                                              │ │
│ │ - Softw. │                                              │ │
│ │ - About  │                                              │ │
│ │ - Log    │                                              │ │
│ └──────────┴──────────────────────────────────────────────┘ │
│ ┌──────────────────────────────────────────────────────────┐│
│ │ Status Bar: Connection status, instance info             ││
│ └──────────────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────────────┤
│ Sidebar Modes:                                              │
│ - ADVANCED: All items visible                               │
│ - COMPACT: Essential items only                             │
│ - MINIMIZED: Icons only (narrow)                            │
├─────────────────────────────────────────────────────────────┤
│ Features:                                                   │
│ - System tray integration (minimize_to_tray config)         │
│ - Auto-start on startup                                     │
│ - Status refresh timer (5 seconds)                          │
└─────────────────────────────────────────────────────────────┘
```

### Pages (`gui/pages/`)

```
├── base.py          - BasePage (abstract base for all pages)
├── setup.py         - SetupPage (initial configuration)
├── connection.py    - ConnectionPage (server connection)
├── converters.py    - ConvertersPage (converter management)
├── converters_v2.py - ConvertersPageV2 (new converter UI)
├── sn_handler.py    - SNHandlerPage (serial number handling)
├── software.py      - SoftwarePage (software distribution)
├── about.py         - AboutPage (version info)
├── log.py           - LogPage (application logs)
├── asset.py         - AssetPage (asset management)
├── rootcause.py     - RootCausePage (ticketing)
├── production.py    - ProductionPage (unit management)
├── product.py       - ProductPage (product management)
├── proxy_settings.py- ProxySettingsPage
├── location.py      - LocationPage
└── general.py       - GeneralPage
```

### Settings Dialog (`gui/settings_dialog.py`)

Modal settings configuration.

### Styles (`gui/styles.py`)

Dark theme stylesheet (Qt CSS-like).

---

## Configuration Management

### ClientConfig (`core/config.py`)

Main configuration dataclass:

```
┌─────────────────────────────────────────────────────────────┐
│                      ClientConfig                           │
├─────────────────────────────────────────────────────────────┤
│ Instance Identification:                                    │
│ - instance_id: str (UUID-based)                             │
│ - instance_name: str                                        │
├─────────────────────────────────────────────────────────────┤
│ Server Connection:                                          │
│ - service_address: str                                      │
│ - api_token: str                                            │
│ - username: str                                             │
├─────────────────────────────────────────────────────────────┤
│ Station Identification:                                     │
│ - station_name: str                                         │
│ - location: str                                             │
│ - purpose: str                                              │
│ - station_name_source: "hostname" | "config" | "manual"     │
├─────────────────────────────────────────────────────────────┤
│ Multi-Station (Hub) Mode:                                   │
│ - multi_station_enabled: bool                               │
│ - station_presets: List[StationPreset]                      │
│ - active_station_key: str                                   │
├─────────────────────────────────────────────────────────────┤
│ Serial Number Handler:                                      │
│ - sn_mode: "Manual Entry" | "Auto-increment" |              │
│            "Barcode Scanner" | "External Source"            │
│ - sn_prefix, sn_start, sn_padding                           │
│ - sn_com_port, sn_terminator                                │
│ - sn_validate_format, sn_pattern                            │
│ - sn_check_duplicates                                       │
├─────────────────────────────────────────────────────────────┤
│ Proxy Settings:                                             │
│ - proxy_mode: "none" | "system" | "manual"                  │
│ - proxy_host, proxy_port                                    │
│ - proxy_auth, proxy_username, proxy_password                │
├─────────────────────────────────────────────────────────────┤
│ Sync Settings:                                              │
│ - sync_interval_seconds: int (default: 300)                 │
│ - process_sync_enabled: bool                                │
├─────────────────────────────────────────────────────────────┤
│ Offline Queue:                                              │
│ - reports_folder: str                                       │
│ - offline_queue_enabled: bool                               │
│ - max_retry_attempts: int (default: 5)                      │
│ - retry_interval_seconds: int (default: 60)                 │
├─────────────────────────────────────────────────────────────┤
│ Converters:                                                 │
│ - converters_folder: str                                    │
│ - converters: List[ConverterConfig]                         │
│ - converters_enabled: bool                                  │
├─────────────────────────────────────────────────────────────┤
│ GUI Tab Visibility:                                         │
│ - show_software_tab, show_sn_handler_tab, etc.              │
├─────────────────────────────────────────────────────────────┤
│ GUI Settings:                                               │
│ - start_minimized: bool                                     │
│ - minimize_to_tray: bool                                    │
├─────────────────────────────────────────────────────────────┤
│ Logging:                                                    │
│ - log_level: str                                            │
│ - log_file: str                                             │
└─────────────────────────────────────────────────────────────┘
```

### ConverterConfig

```
┌─────────────────────────────────────────────────────────────┐
│                    ConverterConfig                          │
├─────────────────────────────────────────────────────────────┤
│ Required:                                                   │
│ - name: str                                                 │
│ - module_path: str (Python module path)                     │
├─────────────────────────────────────────────────────────────┤
│ Watch Folders:                                              │
│ - watch_folder: str                                         │
│ - done_folder: str                                          │
│ - error_folder: str                                         │
│ - pending_folder: str                                       │
├─────────────────────────────────────────────────────────────┤
│ Converter Type:                                             │
│ - converter_type: "file" | "folder" | "scheduled"           │
├─────────────────────────────────────────────────────────────┤
│ Patterns:                                                   │
│ - file_patterns: List[str] (e.g., ["*.csv", "*.xml"])       │
│ - folder_patterns: List[str]                                │
├─────────────────────────────────────────────────────────────┤
│ Validation:                                                 │
│ - alarm_threshold: float (warn below this)                  │
│ - reject_threshold: float (reject below this)               │
├─────────────────────────────────────────────────────────────┤
│ Retry:                                                      │
│ - max_retries: int                                          │
│ - retry_delay_seconds: int                                  │
├─────────────────────────────────────────────────────────────┤
│ Scheduled Converter:                                        │
│ - schedule_interval_seconds: int                            │
│ - cron_expression: str                                      │
│ - run_on_startup: bool                                      │
├─────────────────────────────────────────────────────────────┤
│ Folder Converter:                                           │
│ - readiness_marker: str (e.g., "COMPLETE.marker")           │
│ - min_file_count: int                                       │
├─────────────────────────────────────────────────────────────┤
│ Post-Processing:                                            │
│ - post_action: "move" | "delete" | "archive" | "keep"       │
│ - archive_folder: str                                       │
├─────────────────────────────────────────────────────────────┤
│ Arguments:                                                  │
│ - arguments: Dict[str, Any] (passed to converter class)     │
└─────────────────────────────────────────────────────────────┘
```

### ConnectionConfig (`core/connection_config.py`)

Persistent connection state:

```
┌─────────────────────────────────────────────────────────────┐
│                   ConnectionConfig                          │
├─────────────────────────────────────────────────────────────┤
│ Server:                                                     │
│ - server_url: str                                           │
│ - username: str                                             │
│ - token_encrypted: str                                      │
├─────────────────────────────────────────────────────────────┤
│ State:                                                      │
│ - connection_state: "Not Connected"|"Connected"|"Offline"   │
│ - last_connected: datetime                                  │
│ - last_disconnected: datetime                               │
├─────────────────────────────────────────────────────────────┤
│ Health Monitoring:                                          │
│ - health_check_interval: int (default: 30)                  │
│ - health_check_timeout: int (default: 10)                   │
│ - auto_reconnect: bool                                      │
│ - max_reconnect_attempts: int                               │
│ - reconnect_delay: int                                      │
├─────────────────────────────────────────────────────────────┤
│ Statistics:                                                 │
│ - total_connections, total_disconnections                   │
│ - total_health_checks, failed_health_checks                 │
└─────────────────────────────────────────────────────────────┘
```

### Configuration File Locations

```
Windows:
  %APPDATA%\pyWATS_Client\
  ├── config.json                    # Main configuration
  ├── config_{instance_id}.json      # Per-instance configs
  ├── client.log                     # Application log
  ├── cache\
  │   └── processes_cache.json       # Synced reference data
  ├── reports\
  │   ├── pending\                   # Queued for upload
  │   ├── failed\                    # Failed uploads
  │   └── completed\                 # Archived uploads
  └── converters\                    # Custom converter modules

Linux/Mac:
  ~/.config/pywats_client/
  (same structure)
```

---

## File Watching and Converters

### Converter Types

1. **File Converter** (`converter_type: "file"`)
   - Triggered when files are created/modified in watch folder
   - One file = one report
   - Pattern matching via `file_patterns`

2. **Folder Converter** (`converter_type: "folder"`)
   - Triggered when folder is "ready"
   - Readiness determined by marker file (e.g., `COMPLETE.marker`)
   - Or minimum file count
   - Entire folder = one report

3. **Scheduled Converter** (`converter_type: "scheduled"`)
   - Runs on timer (`schedule_interval_seconds`)
   - Or cron expression (`cron_expression`)
   - Can run on startup (`run_on_startup`)

### File Processing Flow

```
┌────────────────┐
│   Watch Folder │
│   (Watchdog)   │
└───────┬────────┘
        │ File Created Event
        ▼
┌────────────────┐
│   Debounce     │  Wait for file write completion
│   (500ms)      │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│ Pattern Match  │  Check file_patterns
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Converter    │  Load and instantiate from module_path
│   Instance     │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Convert      │  converter.convert(file_path) → ConverterResult
└───────┬────────┘
        │
        ▼
┌────────────────┐
│   Validate     │  Check confidence > reject_threshold
└───────┬────────┘
        │
        ├───────────────────────┐
        │ Success               │ Failure
        ▼                       ▼
┌────────────────┐      ┌────────────────┐
│ Report Queue   │      │  Error Folder  │
│ (submit)       │      │                │
└───────┬────────┘      └────────────────┘
        │
        ▼
┌────────────────┐
│  Done Folder   │  (or delete, or archive per post_action)
└────────────────┘
```

### Converter Base Class

```python
from pywats_client.converters.base import ConverterBase, ConverterResult

class MyConverter(ConverterBase):
    def convert(self, file_path: Path) -> ConverterResult:
        # Parse file and create WATS report
        report = {...}  # WSJF format dict
        return ConverterResult(
            success=True,
            report=report,
            confidence=0.95,
            message="Converted successfully"
        )
    
    def validate(self, file_path: Path) -> float:
        # Return confidence score 0.0 - 1.0
        return 0.95
```

---

## Scheduled Tasks and Background Services

### Service Lifecycle

```
┌──────────────────────────────────────────────────────────────────┐
│                     Application Startup                          │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ 1. Acquire Instance Lock                                         │
│    - File: %TEMP%\pyWATS_Client\instance_{id}.lock               │
│    - Prevents duplicate instances                                │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ 2. Initialize Services                                           │
│    - ConnectionService                                           │
│    - ProcessSyncService (if process_sync_enabled)                │
│    - ReportQueueService (if offline_queue_enabled)               │
│    - ConverterManager (if converters_enabled)                    │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ 3. Start Background Tasks                                        │
│    - Connection health check loop                                │
│    - Process sync loop                                           │
│    - Report queue processing loop                                │
│    - File watchers (Watchdog observers)                          │
└───────────────────────────────┬──────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│ 4. Status: RUNNING                                               │
│    - GUI main loop (if GUI mode)                                 │
│    - Or async event loop (headless)                              │
└──────────────────────────────────────────────────────────────────┘
```

### Background Loops

| Service | Interval | Description |
|---------|----------|-------------|
| Connection Health | 30 seconds | Ping server, update status |
| Process Sync | 5 minutes (configurable) | Sync processes, levels, product groups |
| Report Queue | 60 seconds (configurable) | Retry pending uploads |
| File Monitor | Real-time (Watchdog) | Watch folders for new files |

### Async Architecture

All services use Python's `asyncio`:

```python
class Service:
    async def start(self):
        self._running = True
        self._task = asyncio.create_task(self._loop())
    
    async def stop(self):
        self._running = False
        if self._task:
            self._task.cancel()
    
    async def _loop(self):
        while self._running:
            await asyncio.sleep(self.interval)
            await self.do_work()
```

---

## Data Synchronization and Persistence

### What Gets Synced

| Data | Direction | Storage | Sync Frequency |
|------|-----------|---------|----------------|
| Processes | Server → Client | `cache/processes_cache.json` | On connect + every 5 min |
| Levels | Server → Client | `cache/processes_cache.json` | On connect + every 5 min |
| Product Groups | Server → Client | `cache/processes_cache.json` | On connect + every 5 min |
| Reports | Client → Server | `reports/pending/` → Server | On online + every 60 sec |

### What Gets Persisted Locally

| Data | File | Description |
|------|------|-------------|
| Configuration | `config.json` | All settings |
| Encrypted Token | In `config.json` | Machine-encrypted API token |
| Connection State | In `config.json` | Connected/Offline/Not Connected |
| Pending Reports | `reports/pending/*.json` | Queued for upload |
| Failed Reports | `reports/failed/*.json` | Max retries exceeded |
| Completed Reports | `reports/completed/*.json` | Archive (optional) |
| Process Cache | `cache/processes_cache.json` | Offline reference data |
| Instance Lock | `%TEMP%/instance_{id}.lock` | Running instance info |

### Offline Operation

```
┌────────────────────────────────────────────────────────────────┐
│                      ONLINE Mode                               │
├────────────────────────────────────────────────────────────────┤
│ - Reports uploaded immediately                                 │
│ - Process data synced periodically                             │
│ - Real-time status updates                                     │
└────────────────────────────────────────────────────────────────┘
                           │
                           │ Server unreachable
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                     OFFLINE Mode                               │
├────────────────────────────────────────────────────────────────┤
│ - Reports queued to pending/ folder                            │
│ - Cached process data used                                     │
│ - Credentials retained (encrypted)                             │
│ - Auto-reconnect attempts continue                             │
└────────────────────────────────────────────────────────────────┘
                           │
                           │ Server reachable again
                           ▼
┌────────────────────────────────────────────────────────────────┐
│                    Coming Back ONLINE                          │
├────────────────────────────────────────────────────────────────┤
│ 1. Process data synced                                         │
│ 2. Pending reports uploaded                                    │
│ 3. Status updated                                              │
└────────────────────────────────────────────────────────────────┘
```

---

## Dependencies

### Core API (`pywats`)

| Package | Version | Purpose |
|---------|---------|---------|
| httpx | >=0.24.0 | HTTP client (sync & async) |
| pydantic | >=2.0.0 | Data validation, models |
| python-dateutil | >=2.8.0 | Date/time parsing |
| attrs | >=22.0.0 | Class decorators |
| typing-extensions | >=4.8.0 | Backported typing (Python <3.11) |

### Client Service (`pywats_client`)

| Package | Version | Purpose |
|---------|---------|---------|
| watchdog | >=3.0.0 | File system monitoring |
| aiofiles | >=23.0.0 | Async file operations |
| cryptography | (bundled) | Token encryption |

### Client GUI

| Package | Version | Purpose |
|---------|---------|---------|
| PySide6 | >=6.4.0 | Qt GUI framework |

### Optional Installations

```bash
# Full client with GUI
pip install pywats-api[client]

# Headless client (servers, Raspberry Pi)
pip install pywats-api[client-headless]

# API only (library use)
pip install pywats-api

# MCP server (AI assistant integration)
pip install pywats-api[mcp]
```

---

## Summary

The pyWATS system provides a complete solution for connecting test stations to WATS servers:

1. **pyWATS API** - Low-level HTTP communication with built-in rate limiting and Pydantic models

2. **pyWATS Client** - Service layer handling:
   - Connection management with auto-reconnect
   - Offline report queuing with retry
   - File watching and converter processing
   - Reference data synchronization
   - Multi-instance support

3. **pyWATS Client GUI** - Optional Qt desktop application with:
   - Login/authentication flow
   - Page-based navigation
   - System tray integration
   - Settings management

All configuration is persisted to JSON files, with API tokens encrypted using machine-specific keys. The system supports both online and offline operation, automatically syncing when connectivity is restored.
