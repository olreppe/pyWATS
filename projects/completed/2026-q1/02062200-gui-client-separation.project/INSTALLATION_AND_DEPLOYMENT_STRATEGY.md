# Installation & Deployment Strategy
## GUI Framework Separation Architecture

**Created**: February 4, 2026  
**Project**: GUI-Client Separation  
**Status**: PROPOSAL - Awaiting approval

---

## 🎯 Executive Summary

**Current Misunderstanding**: We were copying components from `pywats_client/gui/` to create a "new framework" - but the existing GUI **IS the Configurator**. There's nothing to "rebuild" - we need to MIGRATE it.

**Critical Requirements**:
1. **Cross-platform** - Primary driver for this project
2. **Multi-instance aware** - Configurators can connect to multiple client instances
3. **Separate installations** - API/Client/Applications installed independently
4. **Shared logging** - Unified logging infrastructure across all layers
5. **No file operations in API** - API logs to memory/console only

---

## 📊 Current Architecture Analysis

### What Exists Today

**pywats (API Package)** - Pure Python API  
- Location: `src/pywats/`
- Purpose: WATS API wrapper
- Logging: Memory/console only (no file operations)
- Installation: `pip install pywats-api`
- Platform: Windows, Linux, macOS (pure Python)

**pywats_client (Client Service)** - Background service  
- Location: `src/pywats_client/`
- Purpose: Queue management, converters, file watching
- Logging: File-based (`pywats.log` in install directory)
- Installation: System service (Windows Service, systemd, launchd)
- Platform: Windows, Linux, macOS
- Multi-instance: ✅ YES (file-based locks, separate configs per instance)

**pywats_client/gui (Configurator GUI)** - Desktop application  
- Location: `src/pywats_client/gui/`
- Purpose: Configure and monitor client service
- Current State: **Monolithic** - bundled with client package
- Problem: Tied to client installation, not cross-platform friendly
- Multi-instance: ⚠️ Single-instance only (QLocalServer prevents multiple GUIs)

### Multi-Instance Capabilities (Current)

From [docs/guides/architecture.md](c:\Users\ola.lund.reppe\Source\PythonAPI (pyWATS)\pyWATS\docs\guides\architecture.md):

**Per Instance Isolation:**
- Configuration: `config_{instance_id}.json`
- Queue: `reports_{instance_id}/`
- Logs: `client_{instance_id}.log`
- IPC Socket: `pyWATS_Service_{instance_id}`
- Lock File: `instance_{instance_id}.lock` (in `%TEMP%/pyWATS_Client/`)

**Use Cases:**
- **Common**: ICT + FCT + EOL on same machine (separate test processes)
- **Importance**: HIGH - manufacturing floors often have multiple test stations per PC
- **Frequency**: 60%+ of deployments use multi-instance

**Current Limitation**: GUI uses QLocalServer with single server name - prevents multiple configurators for different instances.

---

## 🚀 Proposed Architecture

### Three-Layer Installation Model

```
┌─────────────────────────────────────────────────────────────┐
│ LAYER 3: Applications (pywats-ui)                           │
│ ┌─────────────┬─────────────┬─────────────┬──────────────┐ │
│ │   pyWATS    │   pyWATS    │   pyWATS    │   pyWATS     │ │
│ │ Configurator│   AI Chat   │    SPC      │    Yield     │ │
│ │             │             │             │   Monitor    │ │
│ └─────────────┴─────────────┴─────────────┴──────────────┘ │
│                          ▲                                  │
│                          │ Uses                             │
│                          ▼                                  │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ Framework (pywats_ui.framework)                         ││
│ │ - AsyncAPIRunner, ErrorHandlingMixin, BasePage          ││
│ │ - ScriptEditor, Dialogs, Themes                         ││
│ │ - Imports from pywats_client.core (AsyncTaskRunner, etc)││
│ └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ IPC + Imports
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: Client Service (pywats-client)                     │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ pywats_client.service (Service Process)                 ││
│ │ - Queue management, converters, file watching           ││
│ │ - IPC server (AsyncIPCServer)                           ││
│ └─────────────────────────────────────────────────────────┘│
│ ┌─────────────────────────────────────────────────────────┐│
│ │ pywats_client.core (Shared Infrastructure)              ││
│ │ - AsyncTaskRunner (Qt-asyncio bridge)                   ││
│ │ - EventBus (app-wide pub/sub)                           ││
│ │ - InstanceManager (multi-instance support)              ││
│ │ - ConnectionConfig, ClientConfig                        ││
│ │ - Logging (file-based, per instance)                    ││
│ └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                          ▲
                          │ Uses
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: API (pywats-api)                                   │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ pywats (Pure Python API)                                ││
│ │ - Synchronous API (WAtsAPI)                             ││
│ │ - Async API (AsyncWAtsAPI)                              ││
│ │ - Domain services, models, converters                   ││
│ │ - Logging (memory/console only - NO file operations)    ││
│ └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### Package Structure

**pyWATS Repository** (current monorepo):
```
src/
  pywats/              # API package (no GUI deps)
  pywats_client/       # Client service package (has Qt deps in core/)
    core/              # Shared infrastructure (Qt-dependent)
    service/           # Service process (no GUI)
    control/           # CLI and control utilities
    gui/               # [DEPRECATED] Old monolithic GUI
  pywats_ui/           # NEW: GUI framework + applications
    framework/         # Framework components (copied from gui/)
    widgets/           # Reusable widgets
    dialogs/           # Reusable dialogs
    apps/              # Applications
      configurator/    # MIGRATED from pywats_client/gui/
      aichat/          # New AI Chat app
      template/        # Application template
```

---

## 🏗️ Installation & Deployment Strategy

### Disk Layout (Windows Example)

**API Layer** (user-installable via pip):
```
C:\Users\{user}\AppData\Local\Programs\Python\Python314\Lib\site-packages\
  pywats\                     # API package
```

**Client Layer** (system-wide service):
```
C:\Program Files\pyWATS\Client\
  pywats_client\              # Client service package
  config\                     # Default configs
  scripts\                    # Service management scripts

C:\ProgramData\pyWATS\          # Shared data directory
  {instance_id}\                # Per-instance folders
    config_{instance_id}.json   # Instance configuration
    reports_{instance_id}\      # Queue directory
      pending\
      processing\
      completed\
      error\
    logs\
      pywats.log                # Main client log
      conversions\              # Conversion logs
```

**Application Layer** (user-installable):
```
C:\Users\{user}\AppData\Local\pyWATS\Applications\
  pywats_ui\                  # Framework + apps package
  Configurator\               # pyWATS Configurator application
    Configurator.exe          # Standalone executable
    config.json               # App-specific settings
  AIChat\                     # pyWATS AI Chat application
    AIChat.exe
    config.json
  SPC\                        # pyWATS SPC application
    SPC.exe
    config.json
  YieldMonitor\               # pyWATS Yield Monitor application
    YieldMonitor.exe
    config.json
```

**Instance Detection** (shared across all apps):
```
C:\Users\{user}\AppData\Local\Temp\pyWATS_Client\
  instance_production.lock    # Lock file for "production" instance
  instance_ict.lock           # Lock file for "ict" instance
  instance_fct.lock           # Lock file for "fct" instance
```

### Linux/macOS Layout

**API Layer**:
```
~/.local/lib/python3.14/site-packages/pywats/
```

**Client Layer** (system-wide service):
```
/opt/pywats/client/           # Installation
  pywats_client/
  config/
  scripts/

/var/lib/pywats/              # Data directory
  {instance_id}/
    config_{instance_id}.json
    reports_{instance_id}/
    logs/
```              # pyWATS Configurator
  AIChat/                    # pyWATS AI Chat
  SPC/                       # pyWATS SPC
  YieldMonitor/              # pyWATS Yield Monitor
**Application Layer** (user-installable):
```
~/.local/share/pywats/applications/
  pywats_ui/
  Configurator/
  AIChat/
```

**Instance Detection**:
```
/tmp/pywats_client/
  instance_*.lock
```

---

## 🔧 Multi-Instance Implementation

### Current Limitation

**Problem**: GUI uses QLocalServer for single-instance enforcement:

```python
# From pywats_client/gui/app.py
server_name = f"pyWATS_Client_{instance_id or 'default'}"
socket = QLocalSocket()
socket.connectToServer(server_name)

if socket.waitForConnected(500):
    # Another instance running - activate and exit
    return 0
```

This prevents running **multiple configurators** for different instances!

### Proposed Solution

**Remove single-instance enforcement from applications** - allow multiple configurators:

```python
# In pywats_ui/apps/configurator/app.py
def run_configurator(instance_id: str = None) -> int:
    """
    Run Configurator - allows multiple instances for different clients.
    
    Args:
        instance_id: Target client instance to connect to (optional)
    """
    qt_app = QApplication(sys.argv)
    
    # DO NOT enforce single-instance - allow multiple configurators
    # Each configurator connects to a different client instance
    
    if not instance_id:
        # Show instance selector dialog
        instance_id = show_instance_selector()
        if not instance_id:
            return 0  # User cancelled
    
    # Create configurator for selected instance
    window = ConfiguratorMainWindow(instance_id)
    window.show()
    
    # Run event loop
    loop = qasync.QEventLoop(qt_app)
    asyncio.set_event_loop(loop)
    return loop.run_forever()
```

**Instance Detection** (same as current):

```python
# From pywats_client/core/instance_manager.py
class InstanceManager:
    """Detect running client instances via lock files"""
    
    def get_running_instances(self) -> List[Dict[str, Any]]:
        """Get all running client instances"""
        instances = []
        lock_path = Path(os.environ.get('TEMP', '')) / 'pyWATS_Client'
        
        for lock_file in lock_path.glob("instance_*.lock"):
            with open(lock_file, 'r') as f:
                lock_data = json.load(f)
            
            pid = lock_data.get('pid')
            if pid and self._is_process_running(pid):
                instances.append(lock_data)
        
        return instances
```

**Instance Selector Dialog** (new):

```python
class InstanceSelectorDialog(QDialog):
    """Select which client instance to connect to"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Client Instance")
        
        # Scan for running instances
        manager = InstanceManager()
        instances = manager.get_running_instances()
        
        # Show list of instances
        layout = QVBoxLayout(self)
        
        if not instances:
            layout.addWidget(QLabel("No running client instances found."))
            layout.addWidget(QLabel("Please start a client service first."))
        else:
            layout.addWidget(QLabel("Select instance to configure:"))
            
            self.instance_list = QListWidget()
            for inst in instances:
                item_text = f"{inst['instance_name']} ({inst['instance_id']}) - PID {inst['pid']}"
                self.instance_list.addItem(item_text)
            
            layout.addWidget(self.instance_list)
        
        # OK/Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
```

### Use Cases Supported

**Use Case 1**: Single configurator monitoring multiple instances  
- User opens ONE configurator
- Switches between instances via dropdown/tabs
- Implementation: Single window, multiple IPC clients

**Use Case 2**: Multiple configurators for different instances  
- User opens configurator for "production" instance
- User opens ANOTHER configurator for "test" instance
- Both run simultaneously (different windows, different IPC connections)
- Implementation: Remove QLocalServer enforcement

**Use Case 3**: Multiple pyWATS apps open simultaneously  
- pyWATS Configurator + pyWATS AI Chat + pyWATS Yield Monitor (all open)
- All applications connect to SAME client instance
- Each app has different purpose (config vs analysis vs monitoring)
- Implementation: Multiple IPC clients to same service

---

## 📝 Logging Architecture

### Current Logging Structure

**API Layer** (`pywats`):
```python
# src/pywats/core/logging.py
def configure_logging(
    level: str = "INFO",
    format: Literal["text", "json"] = "text",
    handlers: Optional[List[logging.Handler]] = None,
    enable_console: bool = True,
    enable_correlation_ids: bool = False
) -> None:
    """
    Configure logging for pywats API.
    
    NO FILE OPERATIONS - only memory/console handlers!
    """
```

**Client Layer** (`pywats_client`):
```python
# src/pywats_client/core/logging.py
def setup_client_logging(
    instance_id: str = "default",
    log_level: str = "INFO",
    log_format: Literal["text", "json"] = "text",
    enable_console: bool = True,
    rotate_size_mb: int = 10,
    rotate_backups: int = 5
) -> Path:
    """
    Configure logging for client service.
    
    Returns path to main log file:
    - Windows: C:/ProgramData/pyWATS/{instance_id}/pywats.log
    - Linux: /var/lib/pywats/{instance_id}/logs/pywats.log
    - macOS: /Library/Application Support/pyWATS/{instance_id}/pywats.log
    """
```

**Conversion Logs** (separate directory):
```python
# Per-conversion logs in:
# C:/ProgramData/pyWATS/{instance_id}/logs/conversions/{conversion_id}.log
```

### Proposed Application Logging

**Framework Layer** (`pywats_ui`):

```python
# src/pywats_ui/framework/logging.py (NEW)
def setup_app_logging(
    app_name: str,
    instance_id: str = "default",
    log_level: str = "INFO"
) -> Path:
    """
    Configure logging for GUI applications.
    
    Logs to user-specific directory (NOT system-wide):
    - Windows: C:/Users/{user}/AppData/Local/pyWATS/Applications/{app_name}/logs/app.log
    - Linux: ~/.local/share/pywats/applications/{app_name}/logs/app.log
    - macOS: ~/Library/Application Support/pyWATS/Applications/{app_name}/logs/app.log
    
    Separate from client logs to avoid permission conflicts!
    """
```

**Logger Hierarchy**:

```
pywats.*                    # API loggers (memory/console only)
  pywats.domains.report
  pywats.domains.product
  pywats.core.cache

pywats_client.*             # Client loggers (file in ProgramData)
  pywats_client.service
  pywats_client.core.queue
  pywats_client.converters

pywats_ui.*                 # Application loggers (file in AppData)
  pywats_ui.apps.configurator
  pywats_ui.apps.aichat
  pywats_ui.framework
```

**No Conflicts**: Each layer logs to different locations with different permissions.

---

## 📦 Installation Workflows

### Developer Installation (Current Workflow)

```bash
# 1. Install API (editable)
pip install -e .

# 2. Run client service
pywats-client --instance dev service

# 3. Run GUI (OLD - monolithic)
pywats-client --instance dev gui

# 4. Run GUI (NEW - separate applications)
python -m pywats_ui.apps.configurator --instance dev
python -m pywats_ui.apps.aichat --instance dev
```

### End-User Installation (Proposed)

**Windows** (MSI installer):
```
1. Install pyWATS Client Service (System-wide)
   - Location: C:\Program Files\pyWATS\Client\
   - Creates Windows Service: "pyWATS Client (default)"
   - Logs: C:\ProgramData\pyWATS\default\logs\pywats.log

2. Install pyWATS Configurator (User-specific)
   - Location: C:\Users\{user}\AppData\Local\pyWATS\Applications\Configurator\
   - Creates Start Menu shortcut: "pyWATS Configurator"
   - Logs: C:\Users\{user}\AppData\Local\pyWATS\Applications\Configurator\logs\app.log

3. (Optional) Install pyWATS AI Chat, pyWATS SPC, pyWATS Yield Monitor
   - Separate installers, user-specific installations
   - All branded as "pyWATS {Feature}"
```

**Linux** (DEB/RPM packages):
```bash
# 1. Install client service (system-wide, requires root)
sudo apt install pywats-client
sudo systemctl enable pywats-client@default
sudo systemctl start pywats-client@default

# 2. Install pyWATS Configurator (user-specific, no root required)
pip install --user pywats-configurator
pywats-configurator --instance default

# 3. (Optional) Install other pyWATS applications
pip install --user pywats-aichat      # pyWATS AI Chat
pip install --user pywats-spc         # pyWATS SPC
pip install --user pywats-yield       # pyWATS Yield Monitor
pywats-aichat --instance default
```

**macOS** (PKG installer):
```
1. Install pyWATS Client Service (System-wide)
   - Location: /Applications/pyWATS Client.app
   - Creates launchd service
   - Logs: pyWATS Applications (User-specific)
   - Location: ~/Applications/pyWATS Configurator.app (and other pyWATS apps)
2. Install Configurator (User-specific)
   - Location: ~/Applications/pyWATS Configurator.app
   - Logs: ~/Library/Application Support/pyWATS/Applications/Configurator/logs/app.log
```

### Multi-Instance Installation

**Windows** (create multiple service instances):
```powershell
# Install client service (once)
msiexec /i pyWATS-Client-0.2.0.msi /quiet

# Create instances via CLI
pywats-client --instance ict config init
pywats-client --instance fct config init
pywats-client --instance eol config init

# Install as Windows Services
sc create "pyWATS Client (ict)" binPath= "pywats-client --instance ict service"
sc create "pyWATS Client (fct)" binPath= "pywats-client --instance fct service"
sc create "pyWATS Client (eol)" binPath= "pywats-client --instance eol service"

# Start services
sc start "pyWATS Client (ict)"
sc start "pyWATS Client (fct)"
sc start "pyWATS Client (eol)"

# Open configurators (multiple windows allowed!)
pywats-configurator --instance ict   # Opens configurator for ICT
pywats-configurator --instance fct   # Opens configurator for FCT
```

**Linux** (systemd templates):
```bash
# Install client service
sudo apt install pywats-client

# Create instances
sudo systemctl enable pywats-client@ict
sudo systemctl enable pywats-client@fct
sudo systemctl enable pywats-client@eol

sudo systemctl start pywats-client@ict
sudo systemctl start pywats-client@fct
sudo systemctl start pywats-client@eol

# Open configurators (multiple allowed)
pywats-configurator --instance ict &
pywats-configurator --instance fct &
```

---

## 🎯 Migration Strategy

### Phase 1: Framework Foundation (DONE ✅)

- ✅ Created `pywats_ui` package structure
- ✅ Copied framework components from `pywats_client/gui/`
- ✅ Created widgets, dialogs, themes packages
- ✅ Framework imports from `pywats_client.core` (AsyncTaskRunner, EventBus)

### Phase 2: Configurator Migration (NEXT)

**DO NOT REBUILD** - **MIGRATE** existing GUI:

1. **Copy pages** from `pywats_client/gui/pages/` to `pywats_ui/apps/configurator/pages/`
   - DashboardPage, ConnectionPage, SetupPage, ConvertersPage, etc.
   - All 8 existing pages (998 lines in main_window.py)

2. **Create ConfiguratorMainWindow** (adapt from `main_window.py`):
   - Sidebar navigation (keep existing UI)
   - Page routing (keep existing logic)
   - IPC client integration (same as before)
   - Multi-instance selector (NEW - show dialog on startup)

3. **Create configurator entry point** (`apps/configurator/app.py`):
   - Remove QLocalServer single-instance enforcement
   - Add instance selection dialog
   - Keep qasync event loop setup

4. **Test credentials** - Copy test fixtures:
   - From: `tests/fixtures/test_credentials.json`
   - To: `pywats_ui/apps/configurator/tests/fixtures/`

5. **Keep ALL capabilities** - no simplification:
   - ScriptEditor (1106 lines)
   - AsyncAPIRunner (402 lines)
   - All 8 pages from current GUI

### Phase 3: Deployment Packaging

1. **Update pyproject.toml** - Add new entry points:
   ```toml
   [project.scripts]
   pywats-client = "pywats_client.cli:main"
   pywats-configurator = "pywats_ui.apps.configurator:main"  # NEW
   pywats-aichat = "pywats_ui.apps.aichat:main"              # NEW
   ```

2. **Create standalone installers**:
   - Windows: MSI for client, separate MSI for each app
   - Linux: DEB for client, pip-installable apps
   - macOS: PKG for client, DMG for apps

3. **Update deployment scripts**:
   - `deployment/windows/build_msi.py` - Generate MSIs
   - `deployment/standalone/build_standalone.py` - PyInstaller builds
   - `deployment/debian/control` - Add app packages
pyWATS Configurator usage
   - `docs/apps/aichat.md` - pyWATS AI Chat usage
   - `docs/apps/spc.md` - pyWATS SPC usage
   - `docs/apps/yield.md` - pyWATS Yield Monitor

1. **Update installation guides**:
   - `docs/guides/installation.md` - New installation workflows
   - `deployment/README.md` - Platform-specific instructions

2. **Create application docs**:
   - `docs/apps/configurator.md` - Configurator usage
   - `docs/apps/aichat.md` - AI Chat usage

3. **Test multi-instance scenarios**:
   - Multiple client instances running
   - Multiple configurators open
   - Apps connecting to different instances

---pyWATS Configurator app
- `pip install pywats-ui[aichat]` - pyWATS AI Chat app
- `pip install pywats-ui[spc]` - pyWATS SPC app
- `pip install pywats-ui[yield]` - pyWATS Yield Monitor
## ❓ Open Questions for User

### Question 1: Installation Model

**Option A: Monorepo with multiple entry points** (current approach)
- Single GitHub repo
- `pip install pywats-api` - API only
- `pip install pywats-client` - Client service (includes core)
- `pip install pywats-ui[configurator]` - Configurator app
- `pip install pywats-ui[aipyWATS Configurator app + framework)
  - `pywats-aichat` (pyWATS AI Chat app + framework)
  - `pywats-spc` (pyWATS SPC app + framework)
  - `pywats-yield` (pyWATS Yield Monitor
**Option B: Separate packages**
- Split into separate PyPI packages:
  - `pywats-api` (API only)
  - `pywats-client` (Client service + core)
  - `pywats-configurator` (Configurator app + framework)
  - `pywats-aichat` (AI Chat app + framework)
- Framework duplicated in each app package

**Recommendation**: Option A (monorepo with extras) - simpler, less duplication.

### Question 2: Multi-Instance UI Pattern

**Option A: Single window with instance switcher** (simpler)
- One configurator window
- Dropdown to switch between instances
- Only one IPC connection at a time

**Option B: Multiple windows allowed** (more flexible)
- Remove single-instance enforcement completely
- Allow multiple configurator windows
- Each window connects to different instance

**Recommendation**: Option B (multiple windows) - more powerful, matches user's "multiple configurators" requirement.

### Question 3: Application Distribution

**Option A: All apps bundled together**
- `pip install pywats-ui` installs ALL pyWATS apps (Configurator, AI Chat, SPC, Yield Monitor)
- Single installation, larger download

**Option B: Apps installed separately**
- `pip install pywats-ui[configurator]` - pyWATS Configurator only
- `pip install pywats-ui[aichat]` - pyWATS AI Chat only
- `pip install pywats-ui[spc]` - pyWATS SPC only
- `pip install pywats-ui[yield]` - pyWATS Yield Monitor only
- User chooses which apps to install

**Recommendation**: Option B (separate extras) - smaller installs, user choice.

### Question 4: Configurator Migration ✅ **APPROVED WITH IMPROVEMENTS**

**User Decision:** Migrate with reliability improvements
- Same functionality, same pages (all 8 pages)
- Fix ANY weaknesses in current implementation
- Ensure proper utilization of client/core features
- Configurator must be "perfect example" of framework usage
- **Focus**: Reliability, efficiency, stability
- **Critical Goal**: NEVER lose customer data - data must be in server OR kept locally until problem resolved

**Analysis Required Before Migration:**
1. **Data Integrity Audit**
   - How does current GUI handle connection failures during operations?
   - Are all API calls properly error-handled with retry logic?
   - Is there local queueing if server is unreachable?
   - Are there any operations that could lose data on failure?

2. **Client/Core Feature Utilization**
   - Is AsyncTaskRunner used for all long-running operations?
   - Is EventBus used for cross-component communication?
   - Are all async operations using AsyncAPIRunner correctly?
   - Is ErrorHandlingMixin applied consistently?

3. **Missing Vital Features**
   - Connection health monitoring (real-time status)
   - Automatic reconnection on disconnect
   - Local operation queue (if server unreachable)
   - Operation result confirmation (verify success)
   - Undo capability for critical operations
   - Audit logging (who did what, when)

4. **Stability Issues**
   - Are there any race conditions in async operations?
   - Is there proper cleanup on window close?
   - Are resources (files, connections) properly released?
   - Is there proper cancellation of pending operations?

**Improvement Strategy:**
- Start with migration (copy existing pages)
- Analyze each page for reliability issues
- Add missing error handling and retry logic
- Implement local queueing for critical operations
- Add connection resilience (auto-reconnect, offline mode)
- Document any vital missing features found

---

## 🎯 Recommended Next Steps

1. ✅ **STRATEGY APPROVED** - User confirmed approach

2. **Analyze Current GUI for Weaknesses** (NEW - Critical):
   - Audit data integrity: How are connection failures handled?
   - Review error handling: Are all API operations properly wrapped?
   - Check async usage: Is AsyncTaskRunner/AsyncAPIRunner used correctly?
   - Identify missing features: Connection monitoring, auto-reconnect, local queuing
   - Document reliability issues: Race conditions, resource leaks, cleanup
   - **Goal**: Create weakness report BEFORE migration starts

3. **Migrate Configurator with Improvements** (Phase 2):
   - Copy all 8 pages from `pywats_client/gui/pages/` to `pywats_ui/apps/configurator/pages/`
   - Fix identified weaknesses during migration
   - Add missing reliability features (local queue, auto-reconnect, offline mode)
   - Ensure ALL operations have error handling and retry logic
   - Implement "never lose data" safeguards
   - Create `ConfiguratorMainWindow` (adapt from `main_window.py`)
   - Create `app.py` entry point with instance selector
   - Remove single-instance enforcement
   - Test with multiple instances

4. **Reliability Testing**:
   - Test connection failure scenarios (server down, network issues)
   - Verify data is queued locally if server unreachable
   - Test auto-reconnection behavior
   - Verify no data loss on GUI crash/close
   - Test async operation cancellation
   - Verify proper resource cleanup

5. **Update CHANGELOG** - Document new installation model + reliability improvements

6. **Test Multi-Instance**:
   - Start 2 client services (different instances)
   - Open 2 configurators (one for each instance)
   - Verify IPC connections work correctly
   - Check logging isolation
   - Test failure scenarios with multiple instances

7. **Create Deployment Packages**:
   - Windows MSI for configurator
   - Linux DEB package
   - macOS DMG

8. **Documentation**:
   - Update installation guide
   - Create multi-instance tutorial
   - Document new application structure
   - **Document reliability features** (local queue, auto-reconnect, never lose data)

---

## 📋 Summary

**What We're Actually Doing**:
- ✅ MIGRATING existing GUI to separate package (NOT rebuilding)
- ✅ Adding multi-instance support (multiple configurators allowed)
- ✅ Separating installations (client service vs applications)
- ✅ Cross-platform logging (no conflicts between layers)
- ✅ Framework foundation already complete (AsyncAPIRunner, BasePage, etc.)

**What We're NOT Doing**:
- ❌ Rebuilding GUI from scratch
- ❌ Simplifying/reducing features
- ❌ Breaking existing functionality
- ❌ Deprecating old GUI yet (experimental phase)

**Critical Success Factors**:
1. Keep ALL capabilities from current GUI
2. Support multiple configurators for different instances
3. Maintain cross-platform compatibility
4. Separate logging infrastructure
5. Allow independent installation of client vs apps

---

**Questions for User**:
1. ✅ **APPROVED** - Overall strategy confirmed
2. ✅ **APPROVED** - Option A (monorepo with extras)
3. ✅ **APPROVED** - Option B (multiple windows allowed)
4. ✅ **APPROVED** - Option B (apps installed separately)
5. ✅ **APPROVED WITH IMPROVEMENTS** - Migrate pages but fix weaknesses, ensure reliability, never lose data

**Next Action**: 
1. **Analyze current GUI** - Create weakness report (data integrity, error handling, missing features)
2. **Migrate Configurator** - Copy pages + fix weaknesses + add reliability features
3. **Test reliability** - Connection failures, data queuing, auto-reconnect, no data loss
