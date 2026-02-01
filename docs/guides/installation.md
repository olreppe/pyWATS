# PyWATS Complete Installation Guide

A comprehensive guide covering all installation scenarios for pyWATS - from simple API usage to production service deployments.

**Last Updated:** February 1, 2026  
**Version:** 0.2.0+

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start Decision Tree](#quick-start-decision-tree)
3. [Basic Installations](#basic-installations)
   - [API Only (Python SDK)](#api-only-python-sdk)
   - [Client Service](#client-service)
   - [GUI Application](#gui-application)
4. [Platform-Specific Service Setup](#platform-specific-service-setup)
   - [Windows Service](#windows-service)
   - [Linux systemd Service](#linux-systemd-service)
   - [macOS launchd Service](#macos-launchd-service)
   - [Docker Deployment](#docker-deployment)
5. [Native Installers](#native-installers)
6. [Component Comparison](#component-comparison)

---

## Overview

### What is pyWATS?

pyWATS is a Python library and client service for integrating with WATS (Wired & Automated Test System). It provides:

- **Python SDK** - Direct API access for scripts and applications
- **Background Service** - Automated report processing with queuing and retry
- **Desktop GUI** - Monitoring and configuration interface
- **Converters** - Transform test equipment output to WATS format
- **Offline Support** - Queue reports when disconnected, upload when online

### Components

| Component | Description | Size | Use Case |
|-----------|-------------|------|----------|
| **API Only** | Python SDK for WATS integration | ~5 MB | Scripts, automation, server-side integrations |
| **Client Headless** | Background service without GUI | ~8 MB | Servers, Raspberry Pi, embedded systems |
| **Client + GUI** | Full desktop application | ~150 MB | Desktop test stations |

---

## Quick Start Decision Tree

```
What are you building?
│
├─► Python scripts/automation
│   └─ Install: pip install pywats-api
│   └─ Section: API Only
│
├─► Test station with queue/converters
│   │
│   ├─► With monitoring GUI
│   │   └─ Install: pip install pywats-api[client]
│   │   └─ Section: Client Service + GUI Application
│   │
│   └─► Headless/server
│       └─ Install: pip install pywats-api[client-headless]
│       └─ Section: Client Service
│
└─► Production deployment (auto-start on boot)
    └─ Choose your platform:
        ├─ Windows → Windows Service section
        ├─ Linux → Linux systemd Service section
        ├─ macOS → macOS launchd Service section
        └─ Docker → Docker Deployment section
```

---

## Basic Installations

### API Only (Python SDK)

Install the core pyWATS API library for direct integration with WATS from your Python applications.

#### What You Get

- Python SDK for all WATS domains (Report, Product, Production, Asset, etc.)
- Sync and async client support
- Data validation with Pydantic 2.0+
- No GUI dependencies

**Best for:** Scripts, automation, server-side integrations, custom applications.

#### Installation

```bash
pip install pywats-api
```

**Requirements:**
- Python 3.10+
- ~5 MB disk space

**Dependencies (automatically installed):**
- `httpx` - HTTP client
- `pydantic` - Data validation
- `python-dateutil` - Date utilities

#### Quick Start

**Basic Connection:**

```python
from pywats import pyWATS

# Initialize client
api = pyWATS(
    base_url="https://your-server.wats.com",
    token="your_base64_encoded_token"
)

# Test connection
if api.test_connection():
    print("Connected to WATS!")
```

**Using Environment Variables:**

Set credentials once, use everywhere:

```bash
# Windows
set PYWATS_SERVER_URL=https://your-server.wats.com
set PYWATS_API_TOKEN=your_base64_encoded_token

# Linux/macOS
export PYWATS_SERVER_URL=https://your-server.wats.com
export PYWATS_API_TOKEN=your_base64_encoded_token
```

Then in Python:

```python
from pywats import pyWATS

# Reads from environment automatically
api = pyWATS()
```

**Async Client:**

For high-performance applications:

```python
import asyncio
from pywats import pyWATS

async def main():
    async with pyWATS(async_mode=True) as api:
        products = await api.product.get_products()
        print(f"Found {len(products)} products")

asyncio.run(main())
```

#### API Domains

The API is organized into domain modules:

| Domain | Import | Use Case |
|--------|--------|----------|
| **Report** | `api.report` | Create/query test reports (UUT/UUR) |
| **Product** | `api.product` | Manage products, revisions, BOMs |
| **Production** | `api.production` | Serial numbers, unit lifecycle |
| **Asset** | `api.asset` | Equipment tracking, calibration |
| **Analytics** | `api.analytics` | Yield analysis, statistics |
| **Software** | `api.software` | Package distribution |
| **RootCause** | `api.rootcause` | Issue tracking, defects |
| **Process** | `api.process` | Operation types, processes |
| **SCIM** | `api.scim` | User provisioning |

**Example: Create a Test Report**

```python
from pywats import pyWATS
from pywats.report import UUTReport

api = pyWATS()

# Create report
report = UUTReport(
    part_number="PCB-001",
    serial_number="SN12345",
    operation_code="ICT",
    result="P"
)

# Add a numeric measurement
report.add_numeric_limit_step(
    name="Voltage Check",
    value=3.3,
    low_limit=3.0,
    high_limit=3.6,
    unit="V"
)

# Submit
result = api.report.submit_uut_report(report)
print(f"Report ID: {result.id}")
```

#### Authentication

**Token Generation:**

1. Log into WATS web interface
2. Navigate to **Settings → API Access**
3. Generate a new API token
4. Copy the base64-encoded token

**Token Format:**

The token is a base64-encoded string containing your credentials:

```python
import base64

# Create token from username:password
credentials = "username:password"
token = base64.b64encode(credentials.encode()).decode()
print(token)  # dXNlcm5hbWU6cGFzc3dvcmQ=
```

#### Configuration Options

**Client Initialization:**

```python
from pywats import pyWATS

api = pyWATS(
    base_url="https://your-server.wats.com",  # WATS server URL
    token="...",                               # Auth token
    timeout=30,                                # Request timeout (seconds)
    verify_ssl=True,                           # SSL certificate verification
    async_mode=False,                          # Use async client
)
```

**Environment Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `PYWATS_SERVER_URL` | WATS server base URL | Required |
| `PYWATS_API_TOKEN` | Base64-encoded auth token | Required |
| `PYWATS_TIMEOUT` | Request timeout (seconds) | 30 |
| `PYWATS_VERIFY_SSL` | Verify SSL certificates | true |
| `PYWATS_LOG_LEVEL` | Logging level | INFO |

#### Troubleshooting

**Import Errors:**

```bash
# Verify installation
pip show pywats-api

# Check Python version
python --version  # Should be 3.10+

# Reinstall
pip uninstall pywats-api
pip install pywats-api
```

**Connection Issues:**

```python
from pywats import pyWATS

api = pyWATS(
    base_url="https://your-server.wats.com",
    token="your_token"
)

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test connection
try:
    api.test_connection()
except Exception as e:
    print(f"Connection failed: {e}")
```

**SSL Certificate Errors:**

For development/testing only:

```python
api = pyWATS(
    base_url="https://...",
    token="...",
    verify_ssl=False  # ⚠️ Not for production!
)
```

---

### Client Service

The pyWATS Client Service is a background process that handles automated test report processing, queuing, and upload to WATS.

#### What You Get

- **Report Queue** - Reliable queuing with retry on failure
- **Offline Support** - Queue reports when disconnected, upload when online
- **Converters** - Transform test equipment output to WATS format
- **File Watching** - Auto-detect new reports in watch folders
- **Multi-Instance** - Run separate instances for different stations

**Best for:** Test station automation, production environments, embedded systems.

#### Installation

**With GUI (Desktop Stations):**

```bash
pip install pywats-api[client]
```

Includes desktop GUI for configuration and monitoring.

**Headless (Servers, Embedded):**

```bash
pip install pywats-api[client-headless]
```

No GUI dependencies - CLI and HTTP API only. Ideal for:
- Linux servers
- Raspberry Pi
- Embedded systems
- Docker containers

**Requirements:**
- Python 3.10+
- ~8 MB disk space (headless) / ~150 MB (with GUI)

#### Quick Start

**Start the Service:**

```bash
# Default instance
python -m pywats_client service

# Named instance
python -m pywats_client service --instance-id station1
```

**First-Time Configuration:**

Interactive setup:
```bash
pywats-client config init
```

Non-interactive:
```bash
pywats-client config init \
    --server-url https://wats.yourcompany.com \
    --username your-username \
    --password your-password \
    --station-name ICT-STATION-01 \
    --non-interactive
```

**Verify Connection:**

```bash
pywats-client status
```

#### Architecture

**Async-First Design (v1.4+):**

The client uses an **async-first architecture** with asyncio for efficient concurrent I/O:

| Component | Purpose | Concurrency |
|-----------|---------|-------------|
| **AsyncClientService** | Main service controller | Single asyncio event loop |
| **AsyncPendingQueue** | Report upload queue | 5 concurrent uploads |
| **AsyncConverterPool** | File conversion | 10 concurrent conversions |
| **File Watcher** | Detects new files in watch folders | Async events |
| **IPC Server** | GUI communication | Qt LocalSocket |

**Report Processing Flow:**

```
Test Equipment → [File Created] → [File Watcher]
                                       ↓
                          [AsyncConverterPool]
                           (10 concurrent)
                                       ↓
                          [AsyncPendingQueue]
                           (5 concurrent)
                                       ↓
                           [WATS Server]
```

**Benefits of async architecture:**
- **5x faster uploads** - Concurrent report submission
- **Lower memory** - Single thread vs multiple workers
- **Responsive GUI** - Non-blocking API calls
- **Efficient I/O** - asyncio multiplexing

#### File Organization

**Data Directories:**

**Windows (Production):**
```
C:\ProgramData\Virinco\pyWATS\
├── config.json              # Configuration
├── logs\                    # Service logs
├── queue\                   # Report queue
│   ├── pending\            # Waiting for upload
│   ├── processing\         # Currently uploading
│   ├── completed\          # Successfully uploaded
│   └── failed\             # Failed uploads
├── converters\              # Custom converters
└── data\                    # Software packages
```

**Windows (User Development):**
```
%APPDATA%\pyWATS_Client\
```

**Linux/macOS:**
```
~/.config/pywats_client/     # User
/var/lib/pywats/             # System service
```

**Queue Folder Contents:**

| Folder | Purpose | Auto-Cleanup |
|--------|---------|--------------|
| `pending/` | Reports waiting for upload | No |
| `processing/` | Currently uploading | No |
| `completed/` | Successfully uploaded | After 7 days |
| `failed/` | Failed uploads | After 30 days |

#### Configuration

**Configuration File (`config.json`):**

```json
{
  "server_url": "https://wats.yourcompany.com",
  "api_token": "...",
  "station_name": "ICT-STATION-01",
  "station_location": "Production Line A",
  
  "queue": {
    "watch_folders": ["C:\\TestReports"],
    "upload_interval": 10,
    "retry_attempts": 3,
    "retry_delay": 60
  },
  
  "converters": {
    "enabled": ["WATSStandardXMLConverter", "TeradyneICTConverter"],
    "auto_detect": true
  },
  
  "logging": {
    "level": "INFO",
    "max_size_mb": 10,
    "backup_count": 5
  }
}
```

**CLI Configuration:**

```bash
# View all settings
pywats-client config show

# Get specific value
pywats-client config get queue.upload_interval

# Set value
pywats-client config set queue.upload_interval 30

# Add watch folder
pywats-client config add-watch-folder "C:\TestReports\Station1"
```

**Environment Variables:**

Override config via environment:

| Variable | Description |
|----------|-------------|
| `PYWATS_SERVER_URL` | WATS server URL |
| `PYWATS_API_TOKEN` | Auth token |
| `PYWATS_STATION_NAME` | Station identifier |
| `PYWATS_LOG_LEVEL` | Logging level |
| `PYWATS_WATCH_FOLDERS` | Colon-separated paths |

#### Converters

Converters transform test equipment output into WATS format.

**Built-in Converters:**

**WATS Standard Formats:**

| Converter | Format | File Patterns |
|-----------|--------|---------------|
| `WATSStandardXMLConverter` | WSXF/WRML | `*.xml` |
| `WATSStandardJsonConverter` | WSJF | `*.json` |
| `WATSStandardTextConverter` | WSTF | `*.txt` |

**Industry Standards:**

| Converter | Standard | File Patterns | Notes |
|-----------|----------|---------------|-------|
| `ATMLConverter` | IEEE ATML (1671/1636.1) | `*.xml`, `*.atml` | ATML 2.02, 5.00, 6.01 + TestStand AddOn |

**Test Equipment:**

| Converter | Equipment | File Patterns |
|-----------|-----------|---------------|
| `TeradyneICTConverter` | Teradyne i3070 | `*.txt`, `*.log` |
| `TeradyneSpectrumICTConverter` | Teradyne Spectrum | `*.txt`, `*.log` |
| `SeicaXMLConverter` | Seica Flying Probe | `*.xml` |
| `KlippelConverter` | Klippel Audio/Acoustic | `*.txt` + data folder |
| `SPEAConverter` | SPEA ATE | `*.txt` |
| `XJTAGConverter` | XJTAG Boundary Scan | `*.zip` |

**Special:**

| Converter | Purpose |
|-----------|---------|
| `AIConverter` | Auto-detects file type and delegates to best matching converter |

**Custom Converters:**

Place custom converters in the converters folder:

```python
# converters/my_converter.py
from pywats_client.converters import BaseConverter, ConverterInfo
from pywats.report import UUTReport

class MyConverter(BaseConverter):
    @classmethod
    def get_info(cls) -> ConverterInfo:
        return ConverterInfo(
            name="MyConverter",
            description="Converts my test equipment output",
            file_patterns=["*.myext"],
            version="1.0.0"
        )
    
    def convert(self, file_path: str) -> UUTReport:
        # Parse file and create report
        report = UUTReport(
            part_number="...",
            serial_number="...",
            operation_code="TEST",
            result="P"
        )
        return report
```

#### Queue Management

**CLI Commands:**

```bash
# View queue status
pywats-client queue status

# List pending reports
pywats-client queue list

# Retry failed reports
pywats-client queue retry-failed

# Clear completed reports
pywats-client queue clear-completed

# Manual upload
pywats-client upload --file /path/to/report.xml
```

**Queue API:**

For programmatic access:

```python
from pywats_client.core.queue import ReportQueue

queue = ReportQueue(config_path)

# Add report
queue.add("path/to/report.xml")

# Get status
status = queue.get_status()
print(f"Pending: {status.pending_count}")

# Process queue
await queue.process_all()
```

#### Multi-Instance Support

Run separate instances for different stations:

```bash
# Instance 1
pywats-client --instance station1 config init
pywats-client --instance station1 service

# Instance 2
pywats-client --instance station2 config init  
pywats-client --instance station2 service
```

Each instance has separate:
- Configuration file
- Queue folder
- Log file
- Watch folders

#### Headless Mode

**CLI Control:**

```bash
# Start foreground
pywats-client start

# Start as daemon (Linux/macOS)
pywats-client start --daemon

# Check status
pywats-client status

# Stop daemon
pywats-client stop

# Restart
pywats-client restart
```

**HTTP API Control:**

```bash
# Start with HTTP API
pywats-client start --api --api-port 8765
```

Available endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Service status |
| `/queue` | GET | Queue status |
| `/queue/pending` | GET | List pending reports |
| `/restart` | POST | Restart service |
| `/stop` | POST | Stop service |
| `/config` | GET | View configuration |

```bash
# Examples
curl http://localhost:8765/status
curl http://localhost:8765/queue
curl -X POST http://localhost:8765/restart
```

#### Troubleshooting

**Service Won't Start:**

```bash
# Check Python version
python --version  # Should be 3.10+

# Check installation
pip show pywats-api

# View logs
cat ~/.config/pywats_client/pywats_client.log
```

**Reports Not Uploading:**

1. **Check connection:**
   ```bash
   pywats-client status
   ```

2. **Check queue:**
   ```bash
   pywats-client queue status
   ```

3. **Enable debug logging:**
   ```bash
   pywats-client config set logging.level DEBUG
   pywats-client restart
   ```

4. **Manual upload test:**
   ```bash
   pywats-client upload --file /path/to/report.xml --verbose
   ```

**Converter Not Detecting Files:**

1. **Check watch folders:**
   ```bash
   pywats-client config get queue.watch_folders
   ```

2. **Check file patterns:**
   ```bash
   pywats-client converters list
   ```

3. **Test converter manually:**
   ```bash
   pywats-client convert --file /path/to/file.txt --converter MyConverter
   ```

---

### GUI Application

The pyWATS GUI provides a desktop application for monitoring and configuring your WATS client service.

#### What You Get

- **Real-time Monitoring** - View queue status, upload progress, connection state
- **Configuration Interface** - Configure server, converters, and settings
- **Log Viewer** - Monitor application and service logs
- **Converter Management** - Enable/disable and configure converters

**Important:** The GUI is a companion application for the client service. The service handles the actual work (queue processing, uploads); the GUI provides visibility and configuration.

#### Installation

```bash
pip install pywats-api[client]
```

**Requirements:**
- Python 3.10+
- Display/monitor (X11/Wayland on Linux)
- ~150 MB disk space

**Dependencies (automatically installed):**
- `PySide6` - Qt6 GUI framework
- `watchdog` - File monitoring
- `aiofiles` - Async file operations
- Plus all API dependencies

#### Quick Start

**Starting the Service and GUI:**

The recommended workflow is to run the service first, then connect the GUI:

**Step 1: Start the service**
```bash
python -m pywats_client service --instance-id default
```

**Step 2: Launch GUI** (in another terminal)
```bash
python -m pywats_client gui --instance-id default
```

The GUI will connect to the running service via IPC.

**First-Time Setup:**

1. Launch the GUI
2. Go to **Setup** tab
3. Enter your WATS server details:
   - **Server URL**: `https://your-server.wats.com`
   - **Username**: Your WATS username
   - **Password**: Your WATS password
   - **Station Name**: Identifier for this test station
4. Click **Test Connection**
5. Click **Save**

#### GUI Tabs

**📊 Dashboard:**

Main overview showing:
- Connection status (connected/disconnected)
- Queue statistics (pending, processing, completed, failed)
- Recent uploads with timestamps
- Service health indicators

**⚙️ Setup:**

Configure WATS server connection:
- Server URL
- Credentials
- Station name and location
- Connection test button

**📁 Queue:**

View and manage the report queue:
- Pending reports waiting for upload
- Processing status
- Failed reports with error details
- Retry/delete options

**🔄 Converters:**

Manage report converters:
- View installed converters
- Enable/disable converters
- Configure converter settings
- View converter status and errors

**📋 Logs:**

Real-time log viewer:
- Filter by log level (DEBUG, INFO, WARNING, ERROR)
- Search functionality
- Auto-scroll toggle
- Export logs

**📦 Software:**

Software distribution panel (if enabled):
- Available packages
- Download status
- Version information

#### Configuration

**GUI Settings:**

The GUI stores its own settings separately from the service:

**Windows:**
```
%APPDATA%\pyWATS_Client\gui_settings.json
```

**Linux/macOS:**
```
~/.config/pywats_client/gui_settings.json
```

**Customizable Options:**

```json
{
  "window_geometry": {
    "width": 1200,
    "height": 800,
    "x": 100,
    "y": 100
  },
  "theme": "system",
  "log_viewer": {
    "max_lines": 10000,
    "auto_scroll": true,
    "show_timestamps": true
  },
  "refresh_interval": 1000,
  "notifications": {
    "upload_complete": true,
    "upload_failed": true,
    "connection_lost": true
  }
}
```

**Themes:**

The GUI supports system theme detection:

```bash
# Force light theme
python -m pywats_client gui --theme light

# Force dark theme  
python -m pywats_client gui --theme dark

# Use system preference (default)
python -m pywats_client gui --theme system
```

#### Command Line Options

```bash
python -m pywats_client gui [OPTIONS]

Options:
  --instance-id TEXT    Client instance to connect to (default: "default")
  --config-path PATH    Path to config file
  --theme TEXT          Theme: light, dark, system
  --minimized           Start minimized to system tray
  --help               Show help message
```

**Examples:**

```bash
# Connect to default instance
python -m pywats_client gui

# Connect to specific instance
python -m pywats_client gui --instance-id station2

# Start minimized
python -m pywats_client gui --minimized

# Custom config location
python -m pywats_client gui --config-path /path/to/config.json
```

#### System Tray

The GUI can minimize to the system tray:

- **Double-click** tray icon to restore window
- **Right-click** for context menu:
  - Show/Hide window
  - View status
  - Open logs folder
  - Exit

**Tray Notifications:**

When minimized, the GUI shows notifications for:
- Upload completed
- Upload failed
- Connection lost/restored
- Service stopped

Notifications can be disabled in settings.

#### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Q` | Quit application |
| `Ctrl+L` | Focus log search |
| `Ctrl+R` | Refresh all panels |
| `Ctrl+,` | Open settings |
| `F5` | Refresh queue |
| `F11` | Toggle fullscreen |
| `Ctrl+M` | Minimize to tray |

#### Troubleshooting

**GUI Won't Start:**

Check Qt installation:
```bash
python -c "from PySide6 import QtWidgets; print('Qt OK')"
```

If import fails:
```bash
pip uninstall PySide6
pip install PySide6
```

Linux: Check display server:
```bash
echo $DISPLAY  # Should show :0 or similar
```

**GUI Can't Connect to Service:**

1. **Verify service is running:**
   ```bash
   python -m pywats_client status --instance-id default
   ```

2. **Start service if needed:**
   ```bash
   python -m pywats_client service --instance-id default
   ```

3. **Check instance ID matches:**
   ```bash
   # Both must use same instance-id
   python -m pywats_client service --instance-id mystation
   python -m pywats_client gui --instance-id mystation
   ```

**Blank or Frozen UI:**

1. Check log file for errors:
   - Windows: `%APPDATA%\pyWATS_Client\pywats_client.log`
   - Linux: `~/.config/pywats_client/pywats_client.log`

2. Try resetting GUI settings:
   ```bash
   # Remove GUI settings (will use defaults)
   rm ~/.config/pywats_client/gui_settings.json
   ```

**High DPI Display Issues:**

```bash
# Force DPI scaling
export QT_AUTO_SCREEN_SCALE_FACTOR=1
python -m pywats_client gui

# Or set specific scale
export QT_SCALE_FACTOR=1.5
python -m pywats_client gui
```

---

## Platform-Specific Service Setup

For production deployments, install the client as a system service that auto-starts on boot.

### Windows Service

Install pyWATS Client as a Windows Service that auto-starts on system boot.

#### Overview

The pyWATS Client can run as a Windows Service in the background, automatically starting when Windows boots. This is the recommended setup for production environments.

**Folder Structure:**
- **Installation**: `C:\Program Files\Virinco\pyWATS\` (binaries)
- **Data/Config**: `C:\ProgramData\Virinco\pyWATS\` (configuration, logs, queues)
- **Service Name**: `pyWATS_Service` (appears in Task Manager/Services)

#### Prerequisites

**Required:**
- Windows 10/11 or Windows Server 2016+
- Python 3.10 or later
- Administrator privileges

**Recommended: NSSM (Non-Sucking Service Manager):**

NSSM provides the best Windows Service experience with:
- Easy service installation/removal
- Automatic log rotation
- Crash recovery
- Better process management

**Download NSSM:**
1. Visit: https://nssm.cc/download
2. Download the latest version (2.24+)
3. Extract `nssm.exe` to `C:\Program Files\NSSM\` or any PATH location

**Alternative:** The installer can use `sc.exe` (built into Windows), but this has limitations.

#### Installation

**Option 1: Using NSSM (Recommended)**

1. **Install pyWATS Client** (if not already installed):
   ```powershell
   pip install pywats-api[client]
   ```

2. **Install the service** (run as Administrator):
   ```powershell
   python -m pywats_client install-service
   ```

   This will:
   - Create service `pyWATS_Service`
   - Set auto-start on boot
   - Configure logging to `C:\ProgramData\Virinco\pyWATS\logs\`
   - Use default configuration

3. **Start the service**:
   ```powershell
   net start pyWATS_Service
   ```
   or
   ```powershell
   nssm start pyWATS_Service
   ```

**Option 2: Native Windows Service (Recommended for Enterprise)**

The native Windows service uses pywin32 and provides:
- **Appears in Task Manager** → Services tab
- **Automatic restart on failure** (5s/5s/30s delays)
- **Delayed auto-start** (waits for network services)
- **Windows Event Log integration** (events in Event Viewer)

```powershell
# Install native service (run as Administrator)
python -m pywats_client install-service --native

# Start the service
net start pyWATS_Service
```

**Features automatically configured:**
- Service recovery: restarts after 5s on first two failures, 30s thereafter
- Delayed start: waits for network to be ready before starting
- Event logging: service events written to Windows Event Log

**Option 3: Using sc.exe (Fallback)**

If NSSM is not available:

```powershell
python -m pywats_client install-service --use-sc
net start pyWATS_Service
```

**Note:** `sc.exe` has limitations (no automatic log rotation, limited crash recovery).

#### Multi-Instance Installation

For multi-station setups where you need multiple services (one per test station):

```powershell
# Install service for Station A
python -m pywats_client install-service --instance-id station_a --config "C:\ProgramData\Virinco\pyWATS\config_station_a.json"

# Install service for Station B
python -m pywats_client install-service --instance-id station_b --config "C:\ProgramData\Virinco\pyWATS\config_station_b.json"
```

Each instance will have:
- Service name: `pyWATS_Service_station_a`, `pyWATS_Service_station_b`
- Separate logs: `pyWATS_Service_station_a.log`, `pyWATS_Service_station_b.log`
- Independent configuration files

#### Service Management

**Check Service Status:**

```powershell
# Using sc.exe
sc query pyWATS_Service

# Using NSSM
nssm status pyWATS_Service

# Using services.msc GUI
services.msc
```

**Start/Stop/Restart:**

```powershell
# Start
net start pyWATS_Service

# Stop
net stop pyWATS_Service

# Restart
net stop pyWATS_Service && net start pyWATS_Service

# Or with NSSM
nssm restart pyWATS_Service
```

**View Logs:**

Logs are written to `C:\ProgramData\Virinco\pyWATS\logs\`:
- `pyWATS_Service.log` - Standard output
- `pyWATS_Service_error.log` - Error output

```powershell
# View latest logs
Get-Content "C:\ProgramData\Virinco\pyWATS\logs\pyWATS_Service.log" -Tail 50

# Monitor live
Get-Content "C:\ProgramData\Virinco\pyWATS\logs\pyWATS_Service.log" -Wait
```

**Uninstall Service:**

```powershell
# Stop and remove
python -m pywats_client uninstall-service

# For specific instance
python -m pywats_client uninstall-service --instance-id station_a
```

#### Configuration

**Default Configuration:**

The service uses configuration from:
- Default: `C:\ProgramData\Virinco\pyWATS\config.json`
- Custom: Specify with `--config` during installation

**Changing Configuration:**

**Option 1: Using GUI**
1. Run the pyWATS Client GUI
2. It will discover the running service
3. Make configuration changes in the GUI
4. Changes are sent via IPC to the service

**Option 2: Edit config.json**
1. Stop the service: `net stop pyWATS_Service`
2. Edit: `C:\ProgramData\Virinco\pyWATS\config.json`
3. Start the service: `net start pyWATS_Service`

**Option 3: Reinstall with new config**
```powershell
python -m pywats_client uninstall-service
python -m pywats_client install-service --config "C:\path\to\new\config.json"
net start pyWATS_Service
```

#### Troubleshooting

**Service Won't Start:**

1. **Check logs**:
   ```powershell
   Get-Content "C:\ProgramData\Virinco\pyWATS\logs\pyWATS_Service_error.log"
   ```

2. **Test service command manually**:
   ```powershell
   python -m pywats_client service --instance-id default
   ```
   
   This runs the service in foreground mode for debugging.

3. **Verify Python path**:
   ```powershell
   where python
   ```
   
   NSSM uses the Python executable from your PATH. Make sure it's correct.

**Permission Errors:**

The service runs under the SYSTEM account by default. If you need access to network shares or user-specific resources:

```powershell
# Change service account (NSSM)
nssm set pyWATS_Service ObjectName "DOMAIN\Username" "Password"

# Or use sc.exe
sc config pyWATS_Service obj= "DOMAIN\Username" password= "Password"
```

**Service Crashes:**

NSSM automatically restarts crashed services. Check logs for crash details:
```powershell
Get-Content "C:\ProgramData\Virinco\pyWATS\logs\pyWATS_Service_error.log" -Tail 100
```

To disable auto-restart (for debugging):
```powershell
nssm set pyWATS_Service AppExit Default Exit
```

**Multiple Instances Conflict:**

If you see errors about ports or IPC endpoints already in use:

1. Each instance needs a unique `--instance-id`
2. Check running services:
   ```powershell
   sc query type= service state= all | findstr "pyWATS"
   ```

3. Stop conflicting instances:
   ```powershell
   net stop pyWATS_Service
   net stop pyWATS_Service_station_a
   ```

#### Silent Installation (IT Deployment)

For scripted deployment via GPO, SCCM, or automation tools:

**Basic Silent Install:**

```powershell
# Install silently with native service
python -m pywats_client install-service --native --silent

# Check exit code
if ($LASTEXITCODE -ne 0) {
    Write-Error "Installation failed with exit code $LASTEXITCODE"
    exit 1
}
```

**Silent Install with Configuration:**

```powershell
python -m pywats_client install-service --native --silent `
    --server-url "https://wats.company.com" `
    --api-token "your-api-token" `
    --watch-folder "C:\TestReports"
```

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Missing requirements (Python version, pywin32) |
| 10 | Service already installed |
| 11 | Service not installed (uninstall) |
| 14 | Permission denied (need Administrator) |
| 41 | Server unreachable |

**Example Deployment Script:**

```powershell
# deploy_pywats.ps1 - Silent deployment script

param(
    [string]$ServerUrl = "https://wats.company.com",
    [string]$ApiToken,
    [string]$WatchFolder = "C:\TestReports"
)

# Ensure admin privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error "Administrator privileges required"
    exit 14
}

# Install Python package (if needed)
pip install pywats-api[client] --quiet

# Install service
python -m pywats_client install-service --native --silent `
    --server-url $ServerUrl `
    --api-token $ApiToken `
    --watch-folder $WatchFolder

if ($LASTEXITCODE -ne 0) {
    Write-Error "Service installation failed: exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

# Start service
net start pyWATS_Service
Write-Host "pyWATS Service installed and started successfully"
```

#### Event Log

When using `--native`, the service writes to Windows Event Log:

```powershell
# View pyWATS events in Event Viewer
Get-EventLog -LogName Application -Source "pyWATS" -Newest 20
```

Events include:
- Service installation/uninstallation
- Service start/stop
- Errors and warnings

---

### Linux systemd Service

Install pyWATS Client as a Linux systemd service that auto-starts on system boot.

#### Overview

The pyWATS Client can run as a systemd service in the background, automatically starting when Linux boots. This is the recommended setup for production environments.

**System Compatibility:**
- Ubuntu 16.04+ / Debian 8+
- RHEL/CentOS 7+
- Fedora 15+
- Any systemd-based Linux distribution

**Folder Structure:**
- **System-wide**: `/var/lib/pywats/` (configuration, logs, queues)
- **User-specific**: `~/.config/pywats_client/`
- **Service files**: `/etc/systemd/system/`

#### Prerequisites

**Required:**
- Linux with systemd (check: `systemctl --version`)
- Python 3.10 or later
- Root privileges (for system-wide installation)

**Check systemd:**
```bash
# Verify systemd is running
systemctl --version

# Should show systemd version (e.g., systemd 245)
```

#### Installation

**System-Wide Installation (Recommended):**

Installs service that runs at boot, before user login.

```bash
# Install pyWATS Client
pip install pywats-api[client]

# Install as systemd service (requires sudo)
sudo python -m pywats_client install-service

# Start the service
sudo systemctl start pywats-service

# Check status
sudo systemctl status pywats-service
```

This creates:
- Service: `pywats-service.service`
- Auto-start: Enabled
- Logs: `journalctl -u pywats-service`
- Data directory: `/var/lib/pywats/`

**User-Level Installation:**

Installs service that runs when specific user logs in.

```bash
# Install pyWATS Client
pip install pywats-api[client]

# Install as user service (specify your username)
sudo python -m pywats_client install-service --user $USER

# Start the service
sudo systemctl start pywats-service

# Check status
systemctl status pywats-service
```

This creates:
- Service runs as your user account
- Data directory: `~/.config/pywats_client/`
- User-specific permissions

#### Multi-Instance Installation

For multi-station setups where you need multiple services (one per test station):

```bash
# Create separate config files
sudo mkdir -p /var/lib/pywats
sudo cp config.json /var/lib/pywats/config_station_a.json
sudo cp config.json /var/lib/pywats/config_station_b.json

# Install service for Station A
sudo python -m pywats_client install-service \
    --instance-id station_a \
    --config /var/lib/pywats/config_station_a.json \
    --user pywats

# Install service for Station B
sudo python -m pywats_client install-service \
    --instance-id station_b \
    --config /var/lib/pywats/config_station_b.json \
    --user pywats

# Start both services
sudo systemctl start pywats-service@station_a
sudo systemctl start pywats-service@station_b
```

Each instance will have:
- Service name: `pywats-service@station_a.service`, `pywats-service@station_b.service`
- Separate configurations
- Independent logging

#### Service Management

**Check Service Status:**

```bash
# Status
sudo systemctl status pywats-service

# Check if enabled
systemctl is-enabled pywats-service

# Check if running
systemctl is-active pywats-service
```

**Start/Stop/Restart:**

```bash
# Start
sudo systemctl start pywats-service

# Stop
sudo systemctl stop pywats-service

# Restart
sudo systemctl restart pywats-service

# Reload configuration (without restart)
sudo systemctl reload pywats-service
```

**Enable/Disable Auto-Start:**

```bash
# Enable (auto-start on boot)
sudo systemctl enable pywats-service

# Disable (don't auto-start)
sudo systemctl disable pywats-service

# Check status
systemctl is-enabled pywats-service
```

**View Logs:**

systemd logs all service output to the journal:

```bash
# View all logs
sudo journalctl -u pywats-service

# Follow logs (live)
sudo journalctl -u pywats-service -f

# Last 50 lines
sudo journalctl -u pywats-service -n 50

# Since last boot
sudo journalctl -u pywats-service -b

# Last hour
sudo journalctl -u pywats-service --since "1 hour ago"

# With timestamps
sudo journalctl -u pywats-service -o short-iso
```

**Uninstall Service:**

```bash
# Stop and remove
sudo python -m pywats_client uninstall-service

# For specific instance
sudo python -m pywats_client uninstall-service --instance-id station_a

# Verify removal
systemctl list-units | grep pywats
```

#### Silent Installation (IT Deployment)

For automated deployment via Ansible, Puppet, Chef, or shell scripts, use silent mode with exit codes.

**Silent Mode Parameters:**

| Parameter | Description |
|-----------|-------------|
| `--silent` | Suppress all output (exit codes only) |
| `--server-url URL` | Pre-configure WATS server URL |
| `--api-token TOKEN` | Pre-configure API token |
| `--watch-folder PATH` | Pre-configure watch folder path |
| `--skip-preflight` | Skip connectivity checks |
| `--instance-id ID` | Create named instance |
| `--user USERNAME` | Run service as specific user |

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Missing requirements (systemd not available) |
| 10 | Service already installed |
| 11 | Service not installed (uninstall) |
| 14 | Permission denied (not running as root) |
| 20-22 | Configuration errors |
| 30 | Server unreachable |

**Bash Deployment Script:**

```bash
#!/bin/bash
# deploy_pywats.sh - Silent deployment for Ubuntu/Debian

set -e

WATS_SERVER="https://your-wats-server.com"
API_TOKEN="your-api-token"
WATCH_FOLDER="/data/reports"
SERVICE_USER="pywats"

# Create service user if not exists
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -m -d /var/lib/pywats -s /bin/false "$SERVICE_USER"
fi

# Create directories
mkdir -p /var/lib/pywats /var/log/pywats "$WATCH_FOLDER"
chown -R "$SERVICE_USER:$SERVICE_USER" /var/lib/pywats /var/log/pywats

# Install Python package
pip3 install pywats-api[client] --quiet

# Install service silently
python3 -m pywats_client install-service \
    --silent \
    --server-url "$WATS_SERVER" \
    --api-token "$API_TOKEN" \
    --watch-folder "$WATCH_FOLDER" \
    --user "$SERVICE_USER"

EXIT_CODE=$?

case $EXIT_CODE in
    0)  echo "Installation successful"
        systemctl start pywats-service
        ;;
    10) echo "Already installed, restarting..."
        systemctl restart pywats-service
        ;;
    14) echo "ERROR: Must run as root"
        exit 1
        ;;
    *)  echo "ERROR: Installation failed (code $EXIT_CODE)"
        exit 1
        ;;
esac

# Verify service is running
systemctl is-active pywats-service
```

**Ansible Playbook:**

```yaml
# deploy_pywats.yml
---
- name: Deploy pyWATS Client
  hosts: test_stations
  become: yes
  vars:
    wats_server: "https://wats.example.com"
    api_token: "{{ vault_api_token }}"
    watch_folder: "/data/reports"
    service_user: "pywats"

  tasks:
    - name: Create service user
      user:
        name: "{{ service_user }}"
        system: yes
        home: /var/lib/pywats
        shell: /bin/false
        create_home: yes

    - name: Create directories
      file:
        path: "{{ item }}"
        state: directory
        owner: "{{ service_user }}"
        group: "{{ service_user }}"
        mode: '0755'
      loop:
        - /var/lib/pywats
        - /var/log/pywats
        - "{{ watch_folder }}"

    - name: Install pyWATS
      pip:
        name: pywats-api[client]
        state: latest

    - name: Install service
      command: >
        python3 -m pywats_client install-service
        --silent
        --server-url {{ wats_server }}
        --api-token {{ api_token }}
        --watch-folder {{ watch_folder }}
        --user {{ service_user }}
      register: install_result
      changed_when: install_result.rc == 0
      failed_when: install_result.rc not in [0, 10]

    - name: Start service
      systemd:
        name: pywats-service
        state: started
        enabled: yes
```

#### Configuration

**Default Configuration:**

The service uses configuration from:
- System-wide: `/var/lib/pywats/config.json`
- User-specific: `~/.config/pywats_client/config.json`
- Custom: Specify with `--config` during installation

**Changing Configuration:**

**Option 1: Using GUI**
1. Run the pyWATS Client GUI
2. It will discover the running service
3. Make configuration changes in the GUI
4. Changes are sent via IPC to the service

**Option 2: Edit config.json**
```bash
# Stop the service
sudo systemctl stop pywats-service

# Edit configuration
sudo nano /var/lib/pywats/config.json

# Start the service
sudo systemctl start pywats-service

# Verify
sudo journalctl -u pywats-service -n 20
```

**Option 3: Reinstall with new config**
```bash
sudo python -m pywats_client uninstall-service
sudo python -m pywats_client install-service --config /path/to/new/config.json
sudo systemctl start pywats-service
```

#### Troubleshooting

**Service Won't Start:**

1. **Check logs**:
   ```bash
   sudo journalctl -u pywats-service -n 100 --no-pager
   ```

2. **Check service file**:
   ```bash
   sudo systemctl cat pywats-service
   ```

3. **Test service command manually**:
   ```bash
   # Run in foreground for debugging
   python -m pywats_client service --instance-id default
   ```

4. **Verify Python path**:
   ```bash
   which python
   python --version
   ```

5. **Check permissions**:
   ```bash
   ls -la /var/lib/pywats/
   sudo chown -R pywats:pywats /var/lib/pywats/
   ```

**Permission Errors:**

If the service can't access files:

```bash
# Create dedicated user
sudo useradd -r -s /bin/false pywats

# Set ownership
sudo chown -R pywats:pywats /var/lib/pywats/

# Reinstall with user
sudo python -m pywats_client uninstall-service
sudo python -m pywats_client install-service --user pywats
```

**Service Keeps Restarting:**

The service is configured to automatically restart on failure. Check why it's failing:

```bash
# View recent crashes
sudo journalctl -u pywats-service --since "10 minutes ago"

# Disable auto-restart temporarily
sudo systemctl edit pywats-service
# Add:
# [Service]
# Restart=no

sudo systemctl daemon-reload
sudo systemctl restart pywats-service
```

**Port Already in Use:**

If you see "Address already in use" errors:

```bash
# Check what's using the port
sudo netstat -tlnp | grep :8765

# Or with ss
sudo ss -tlnp | grep :8765

# Kill the conflicting process or change port in config
```

#### Advanced Configuration

**Custom User and Group:**

```bash
# Create dedicated user
sudo useradd -r -m -d /var/lib/pywats -s /bin/false pywats

# Install with custom user
sudo python -m pywats_client install-service --user pywats
```

**Environment Variables:**

Edit the service file:

```bash
sudo systemctl edit pywats-service --full
```

Add environment variables:
```ini
[Service]
Environment="PYTHONPATH=/custom/path"
Environment="PYWATS_LOG_LEVEL=DEBUG"
```

Then reload:
```bash
sudo systemctl daemon-reload
sudo systemctl restart pywats-service
```

**Resource Limits:**

The service unit file includes production-hardened defaults:

```ini
[Service]
# Memory and CPU limits
MemoryMax=512M
CPUQuota=80%
LimitNOFILE=65535
LimitNPROC=4096

# Watchdog (service health monitoring)
Type=notify
WatchdogSec=60s

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
PrivateDevices=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true

# Capability restrictions
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

# System call filtering
SystemCallArchitectures=native
SystemCallFilter=@system-service
```

---

### macOS launchd Service

Install pyWATS Client as a macOS launchd service that auto-starts on system boot.

#### Overview

The pyWATS Client can run as a launchd daemon/agent in the background, automatically starting when macOS boots or when you log in.

**Service Types:**
- **Launch Daemon**: Starts at boot (system-wide, requires sudo)
- **Launch Agent**: Starts at login (user-specific, no sudo required)

**Folder Structure:**
- **Daemons**: `/Library/LaunchDaemons/` (system-wide)
- **Agents**: `/Library/LaunchAgents/` (user-level)
- **Data (Daemon)**: `/var/lib/pywats/`
- **Data (Agent)**: `~/.config/pywats_client/`
- **Logs (Daemon)**: `/var/log/pywats/`
- **Logs (Agent)**: `~/Library/Logs/pyWATS/`

#### Prerequisites

**Required:**
- macOS 10.10 (Yosemite) or later
- Python 3.10 or later
- Administrator privileges (for Launch Daemon)

#### Installation

**Option 1: Launch Daemon (System-Wide, Recommended)**

Runs at boot, before any user logs in. Best for production test stations.

```bash
# Install pyWATS Client
pip3 install pywats-api[client]

# Install as Launch Daemon (requires sudo)
sudo python3 -m pywats_client install-service

# Service starts automatically after installation
# Or start manually:
sudo launchctl start com.wats.pywats.service
```

This creates:
- Plist: `/Library/LaunchDaemons/com.wats.pywats.service.plist`
- Auto-start: Enabled (runs at boot)
- Logs: `/var/log/pywats/pywats-service.log`
- Data: `/var/lib/pywats/`

**Option 2: Launch Agent (User-Level)**

Runs when you log in. Good for development.

```bash
# Install pyWATS Client
pip3 install pywats-api[client]

# Install as Launch Agent (no sudo needed)
python3 -m pywats_client install-service --user-agent

# Service starts automatically at login
# Or start manually:
launchctl start com.wats.pywats.service
```

This creates:
- Plist: `/Library/LaunchAgents/com.wats.pywats.service.plist`
- Auto-start: At login
- Logs: `~/Library/Logs/pyWATS/pywats-service.log`
- Data: `~/.config/pywats_client/`

#### Multi-Instance Installation

For multi-station setups where you need multiple services (one per test station):

```bash
# Create config files
sudo mkdir -p /var/lib/pywats
sudo cp config.json /var/lib/pywats/config_station_a.json
sudo cp config.json /var/lib/pywats/config_station_b.json

# Install service for Station A
sudo python3 -m pywats_client install-service \
    --instance-id station_a \
    --config /var/lib/pywats/config_station_a.json

# Install service for Station B
sudo python3 -m pywats_client install-service \
    --instance-id station_b \
    --config /var/lib/pywats/config_station_b.json
```

Each instance will have:
- Plist: `com.wats.pywats.service.station_a.plist`, `com.wats.pywats.service.station_b.plist`
- Separate configurations
- Independent logging

#### Service Management

**Check Service Status:**

```bash
# List all launchd services (system)
sudo launchctl list | grep pywats

# List user services
launchctl list | grep pywats

# Check specific service
sudo launchctl list com.wats.pywats.service
```

**Start/Stop:**

**Launch Daemon (system-wide):**
```bash
# Start
sudo launchctl start com.wats.pywats.service

# Stop
sudo launchctl stop com.wats.pywats.service

# Note: Service will auto-restart if killed
# To prevent restart, unload the plist
sudo launchctl unload /Library/LaunchDaemons/com.wats.pywats.service.plist
```

**Launch Agent (user-level):**
```bash
# Start
launchctl start com.wats.pywats.service

# Stop
launchctl stop com.wats.pywats.service

# Unload
launchctl unload /Library/LaunchAgents/com.wats.pywats.service.plist
```

**View Logs:**

**Launch Daemon logs:**
```bash
# View logs
sudo tail -f /var/log/pywats/pywats-service.log

# View errors
sudo tail -f /var/log/pywats/pywats-service-error.log

# View with Console.app
open -a Console /var/log/pywats/
```

**Launch Agent logs:**
```bash
# View logs
tail -f ~/Library/Logs/pyWATS/pywats-service.log

# View errors
tail -f ~/Library/Logs/pyWATS/pywats-service-error.log

# View with Console.app
open -a Console ~/Library/Logs/pyWATS/
```

**Uninstall Service:**

**Launch Daemon:**
```bash
# Stop and remove
sudo python3 -m pywats_client uninstall-service

# For specific instance
sudo python3 -m pywats_client uninstall-service --instance-id station_a

# Verify removal
sudo launchctl list | grep pywats
```

**Launch Agent:**
```bash
# Stop and remove
python3 -m pywats_client uninstall-service --user-agent

# Verify removal
launchctl list | grep pywats
```

#### Configuration

**Default Configuration:**

The service uses configuration from:
- Daemon: `/var/lib/pywats/config.json`
- Agent: `~/.config/pywats_client/config.json`
- Custom: Specify with `--config` during installation

**Changing Configuration:**

**Option 1: Using GUI**
1. Run the pyWATS Client GUI
2. It will discover the running service
3. Make configuration changes in the GUI
4. Changes are sent via IPC to the service

**Option 2: Edit config.json**
```bash
# Stop the service
sudo launchctl stop com.wats.pywats.service

# Edit configuration (Daemon)
sudo nano /var/lib/pywats/config.json

# Or for Agent
nano ~/.config/pywats_client/config.json

# Restart the service
sudo launchctl start com.wats.pywats.service
```

**Option 3: Reinstall with new config**
```bash
sudo python3 -m pywats_client uninstall-service
sudo python3 -m pywats_client install-service --config /path/to/new/config.json
```

#### Troubleshooting

**Service Won't Start:**

1. **Check if plist is loaded**:
   ```bash
   sudo launchctl list | grep pywats
   ```

2. **Check logs**:
   ```bash
   sudo tail -100 /var/log/pywats/pywats-service-error.log
   ```

3. **Test service command manually**:
   ```bash
   # Run in foreground for debugging
   python3 -m pywats_client service --instance-id default
   ```

4. **Verify Python path**:
   ```bash
   which python3
   python3 --version
   ```

5. **Check plist syntax**:
   ```bash
   plutil /Library/LaunchDaemons/com.wats.pywats.service.plist
   ```

**Permission Errors:**

If the service can't access files:

```bash
# Check ownership (Daemon)
ls -la /var/lib/pywats/

# Fix permissions
sudo chown -R root:wheel /var/lib/pywats/
sudo chmod -R 755 /var/lib/pywats/

# For Agent
ls -la ~/.config/pywats_client/
```

**Service Keeps Restarting:**

The service is configured to auto-restart on failure. Check why it's failing:

```bash
# View recent errors
sudo tail -100 /var/log/pywats/pywats-service-error.log

# Check system logs
log show --predicate 'subsystem == "com.apple.launchd"' --last 10m | grep pywats

# Disable auto-restart temporarily
sudo launchctl unload /Library/LaunchDaemons/com.wats.pywats.service.plist
```

**Port Already in Use:**

If you see "Address already in use" errors:

```bash
# Check what's using the port
sudo lsof -i :8765

# Kill the conflicting process or change port in config
```

**Service Doesn't Auto-Start at Boot:**

1. **Verify plist location**:
   ```bash
   ls -l /Library/LaunchDaemons/com.wats.pywats.service.plist
   ```

2. **Check RunAtLoad**:
   ```bash
   plutil -p /Library/LaunchDaemons/com.wats.pywats.service.plist | grep RunAtLoad
   # Should show: "RunAtLoad" => 1
   ```

3. **Reload plist**:
   ```bash
   sudo launchctl unload /Library/LaunchDaemons/com.wats.pywats.service.plist
   sudo launchctl load /Library/LaunchDaemons/com.wats.pywats.service.plist
   ```

#### Advanced Configuration

**Custom Environment Variables:**

Edit the plist file:

```bash
sudo nano /Library/LaunchDaemons/com.wats.pywats.service.plist
```

Add environment variables:
```xml
<key>EnvironmentVariables</key>
<dict>
    <key>PYTHONPATH</key>
    <string>/custom/path</string>
    <key>PYWATS_LOG_LEVEL</key>
    <string>DEBUG</string>
</dict>
```

Then reload:
```bash
sudo launchctl unload /Library/LaunchDaemons/com.wats.pywats.service.plist
sudo launchctl load /Library/LaunchDaemons/com.wats.pywats.service.plist
```

**Run on Schedule:**

Instead of continuous running, run periodically:

```xml
<key>StartCalendarInterval</key>
<dict>
    <key>Hour</key>
    <integer>8</integer>
    <key>Minute</key>
    <integer>0</integer>
</dict>
```

**Resource Limits:**

Add limits to prevent runaway processes:

```xml
<key>SoftResourceLimits</key>
<dict>
    <key>NumberOfFiles</key>
    <integer>1024</integer>
</dict>

<key>HardResourceLimits</key>
<dict>
    <key>NumberOfFiles</key>
    <integer>2048</integer>
</dict>
```

---

### Docker Deployment

Deploy pyWATS using Docker for containerized deployments.

#### Quick Start

**Prerequisites:**
- Docker 20.10+ and Docker Compose 2.0+
- WATS server credentials

**Initial Setup:**

```bash
# Clone the repository
git clone https://github.com/olreppe/pyWATS.git
cd pyWATS

# Create environment file
cp .env.example .env

# Edit .env and add your WATS credentials
nano .env
```

**Create Required Directories:**

```bash
mkdir -p watch output archive config
```

**Create Client Configuration:**

Create `config/client_config.json`:

```json
{
  "wats": {
    "base_url": "https://wats.yourcompany.com",
    "token": "your_base64_token"
  },
  "converters": {
    "enabled": ["csv", "json", "xml"],
    "watch_directory": "/app/watch",
    "output_directory": "/app/output",
    "archive_directory": "/app/archive"
  },
  "logging": {
    "level": "INFO",
    "file": "/app/logs/pywats_client.log"
  }
}
```

**Start the Client:**

```bash
# Start headless client
docker-compose up -d client

# View logs
docker-compose logs -f client

# Check status
docker-compose ps
```

#### Available Images

The Dockerfile provides multiple build targets:

**1. API Only (`api`)**

Minimal image with just the pyWATS API library.

```bash
# Build
docker build --target api -t pywats-api .

# Run Python with pyWATS
docker run -it pywats-api python
```

**Use Cases:**
- Python scripts that use pyWATS API
- Custom applications
- Lambda/serverless functions

**2. Headless Client (`client-headless`)**

Client without GUI for servers and embedded systems.

```bash
# Build
docker build --target client-headless -t pywats-client .

# Run with config
docker run -d \
  -v $(pwd)/config:/app/config:ro \
  -v $(pwd)/watch:/app/watch \
  -v $(pwd)/output:/app/output \
  -e WATS_BASE_URL=https://wats.example.com \
  -e WATS_TOKEN=your_token \
  pywats-client
```

**Use Cases:**
- Production test data ingestion
- Automated test report uploads
- Headless test stations
- Raspberry Pi deployments

**3. Development (`dev`)**

Full development environment with all dependencies.

```bash
# Start dev container
docker-compose --profile dev up -d dev

# Attach to container
docker-compose exec dev bash

# Run tests
docker-compose exec dev pytest

# Build docs
docker-compose exec dev sphinx-build docs/api docs/_build/html
```

#### Production Deployment

**Docker Compose (Recommended):**

```bash
# 1. Configure environment
cp .env.example .env
nano .env

# 2. Create config
mkdir -p config watch output archive
nano config/client_config.json

# 3. Start services
docker-compose up -d client

# 4. Verify
docker-compose logs client
docker-compose ps
```

**Kubernetes:**

Example deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pywats-client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pywats-client
  template:
    metadata:
      labels:
        app: pywats-client
    spec:
      containers:
      - name: client
        image: pywats-client:latest
        env:
        - name: WATS_BASE_URL
          valueFrom:
            secretKeyRef:
              name: pywats-secrets
              key: base-url
        - name: WATS_TOKEN
          valueFrom:
            secretKeyRef:
              name: pywats-secrets
              key: token
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
        - name: watch
          mountPath: /app/watch
        - name: output
          mountPath: /app/output
        - name: logs
          mountPath: /app/logs
        resources:
          requests:
            memory: "256Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "2"
      volumes:
      - name: config
        configMap:
          name: pywats-config
      - name: watch
        persistentVolumeClaim:
          claimName: pywats-watch
      - name: output
        persistentVolumeClaim:
          claimName: pywats-output
      - name: logs
        persistentVolumeClaim:
          claimName: pywats-logs
```

**Docker Swarm:**

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml pywats

# Scale service
docker service scale pywats_client=3

# View logs
docker service logs -f pywats_client
```

#### Configuration

**Environment Variables:**

**Required:**
- `WATS_BASE_URL` - WATS server URL
- `WATS_TOKEN` - Base64-encoded credentials

**Optional:**
- `PYWATS_LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
- `PYWATS_HEADLESS` - Run in headless mode (default: 1 in Docker)
- `PYWATS_CONFIG_DIR` - Configuration directory (default: /app/config)
- `PYWATS_DATA_DIR` - Data directory (default: /app/data)
- `PYWATS_LOG_DIR` - Log directory (default: /app/logs)

**Volume Mounts:**

| Mount Point | Purpose | Recommended |
|------------|---------|-------------|
| `/app/config` | Configuration files | Read-only in production |
| `/app/watch` | Incoming test data | Writable |
| `/app/output` | Converted reports | Writable |
| `/app/archive` | Processed files | Writable |
| `/app/logs` | Application logs | Persistent volume |
| `/app/data` | State/queue data | Persistent volume |

**Health Checks:**

All images include health checks:

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' pywats-client

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' pywats-client
```

#### Monitoring & Troubleshooting

**View Logs:**

```bash
# Real-time logs
docker-compose logs -f client

# Last 100 lines
docker-compose logs --tail=100 client

# Specific time range
docker-compose logs --since 2024-01-01T00:00:00 client
```

**Check Status:**

```bash
# Container status
docker-compose ps

# Resource usage
docker stats pywats-client

# Health status
docker inspect --format='{{.State.Health.Status}}' pywats-client
```

**Common Issues:**

**Container exits immediately:**

```bash
# Check logs
docker-compose logs client

# Common causes:
# 1. Missing WATS_BASE_URL or WATS_TOKEN
# 2. Invalid configuration in config/client_config.json
# 3. Permission issues on mounted directories
```

**Cannot connect to WATS server:**

```bash
# Test network connectivity
docker-compose exec client ping wats.yourcompany.com

# Test WATS API
docker-compose exec client python -c "
from pywats import pyWATS
api = pyWATS(base_url='https://wats.example.com', token='...')
print(api.test_connection())
"
```

**Permission denied errors:**

```bash
# Fix directory permissions (host)
chmod -R 777 watch output archive logs

# Or run with specific user ID
docker-compose run --user $(id -u):$(id -g) client
```

**Debugging:**

```bash
# Start interactive shell
docker-compose exec client bash

# Or start new container with shell
docker-compose run --rm client bash

# Run Python interactively
docker-compose exec client python
```

#### Advanced Usage

**Multi-Stage Builds:**

Build only what you need:

```bash
# API only (smallest)
docker build --target api -t pywats-api:latest .

# Headless client
docker build --target client-headless -t pywats-client:latest .

# Development (largest)
docker build --target dev -t pywats-dev:latest .
```

**Custom Configuration:**

Override defaults with `docker-compose.override.yml`:

```yaml
version: '3.8'
services:
  client:
    environment:
      PYWATS_LOG_LEVEL: DEBUG
    volumes:
      - /custom/watch:/app/watch
      - /custom/output:/app/output
```

**Resource Limits:**

Adjust in `docker-compose.yml`:

```yaml
deploy:
  resources:
    limits:
      cpus: '4'      # Max CPUs
      memory: 2G     # Max memory
    reservations:
      cpus: '1'      # Min CPUs
      memory: 512M   # Min memory
```

**Security Considerations:**

1. **Never commit `.env` files** - Use secrets management
2. **Use read-only config mounts** - Prevent container from modifying config
3. **Run as non-root** - All images use non-root user (uid 1000)
4. **Scan images** - `docker scan pywats-client`
5. **Use HTTPS** - Always use TLS for WATS connections
6. **Rotate credentials** - Update `WATS_TOKEN` regularly
7. **Network isolation** - Use Docker networks to restrict access

---

## Native Installers

Pre-built installers are available for systems without Python:

| Platform | Format | Download |
|----------|--------|----------|
| **Windows** | `.msi` | [GitHub Releases](https://github.com/olreppe/pyWATS/releases) |
| **macOS** | `.dmg` / `.pkg` | [GitHub Releases](https://github.com/olreppe/pyWATS/releases) |
| **Ubuntu/Debian** | `.deb` | [GitHub Releases](https://github.com/olreppe/pyWATS/releases) |
| **RHEL/Rocky/Alma** | `.rpm` | [GitHub Releases](https://github.com/olreppe/pyWATS/releases) |
| **Linux (any)** | AppImage | [GitHub Releases](https://github.com/olreppe/pyWATS/releases) |

**Building from source:** See [deployment/README.md](../../deployment/README.md)

---

## Component Comparison

### Quick Comparison

| Feature | API Only | Client Headless | Client + GUI |
|---------|----------|-----------------|--------------|
| **Size** | ~5 MB | ~8 MB | ~150 MB |
| **Python SDK** | ✓ | ✓ | ✓ |
| **Report Queue** | - | ✓ | ✓ |
| **Converters** | - | ✓ | ✓ |
| **File Watching** | - | ✓ | ✓ |
| **GUI** | - | - | ✓ |
| **Use Case** | Scripts | Servers, Pi | Desktop |

### Service Deployment Comparison

| Method | Auto-Start | Survives Reboot | Crash Recovery | Service Management |
|--------|------------|-----------------|----------------|-------------------|
| **Windows Service** | ✓ | ✓ | ✓ (NSSM) | services.msc, sc.exe |
| **Linux systemd** | ✓ | ✓ | ✓ | systemctl, journalctl |
| **macOS launchd** | ✓ | ✓ | ✓ | launchctl |
| **Docker** | ✓ | ✓ | ✓ | docker-compose, kubectl |
| **Manual (GUI)** | ✗ | ✗ | ✗ | Task Manager/Terminal |

---

## Next Steps

- **[Getting Started Guide](../getting-started.md)** - Comprehensive tutorial
- **[Client Architecture](../client-architecture.md)** - Architecture details
- **[LLM Converter Guide](../llm-converter-guide.md)** - Writing converters
- **[Quick Reference](../quick-reference.md)** - Common patterns and snippets
- **[Domain Documentation](../domains/)** - Detailed API reference
- **[Deployment README](../../deployment/README.md)** - Building native installers

---

## Support

- **Documentation:** https://github.com/olreppe/pyWATS/tree/main/docs
- **Issues:** https://github.com/olreppe/pyWATS/issues
- **Email:** support@virinco.com
