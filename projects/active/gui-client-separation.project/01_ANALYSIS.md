# Analysis: Multi-Application GUI Framework

**Date:** February 4, 2026  
**Type:** Architecture Analysis  
**Updated:** Expanded scope to 4 applications + shared framework

---

## 🎯 Problem Statement

The current pyWATS architecture has a single tightly-coupled GUI (Client Configurator). The C# reference implementation has **4 separate GUI applications** that need to be implemented in Python:

1. **Client Configurator** - Service configuration and management (exists, needs refactoring)
2. **Yield Monitor** - Real-time yield/analytics dashboard (NEW)
3. **Software Package Manager** - Package distribution and deployment (NEW)
4. **Client Monitor** - Service health and diagnostics (NEW)

**Current Issues:**
1. **No shared framework** - Would lead to massive code duplication
2. **Tight coupling** - Existing configurator mixed with client service
3. **No communication** - Apps can't talk to each other (optional requirement)
4. **Monolithic structure** - Each new app would start from scratch

**Goal:** Create a shared UI framework (`pywats_ui`) that:
- Maximizes code reuse across 4+ applications
- Allows apps to run independently
- Enables optional inter-app communication
- Provides consistent look & feel
- Supports future applications and name changes

---

## 📋 Requirements

### Application Requirements

**1. Client Configurator** (Refactor existing)
- Service configuration (connection, credentials)
- Station setup (converters, settings)
- Test connection and validation
- Service start/stop/restart
- Log viewer integration

**2. Yield Monitor** (NEW - High Priority)
- Real-time yield dashboards
- Process analytics (ICT, FCT, EOL)
- Trend charts and visualizations
- Configurable time ranges
- Alert thresholds
- Export reports

**3. Software Package Manager** (NEW)
- Browse available packages
- Upload new packages (ZIP files)
- Review/approve workflow
- Release management
- Version tracking
- Deployment status

**4. Client Monitor** (NEW)
- Service health dashboard
- Real-time status monitoring
- Alarm viewer and management
- Performance metrics
- Log aggregation
- Service restart/control

### Shared Framework Requirements

**Must Have:**
- Base application class (initialization, config, shutdown)
- Common main window template (menu bar, status bar, toolbar)
- Dialog library (connection, authentication, alerts, progress)
- Widget library (styled controls, validators)
- Configuration management (per-app settings)
- Logging integration (structured logs)
- API/Client access (shared connection pool)
- Theme/styling system (consistent look & feel)

**Should Have:**
- Inter-app communication (IPC via message bus or QLocalSocket)
- Plugin architecture (extensible apps)
- Shared data models and validators
- Common error handling and user feedback
- Session management (user authentication state)

**Nice to Have:**
- Hot reload for development
- Built-in debugger/inspector
- Accessibility support
- Internationalization (i18n)

### Non-Functional Requirements

**Performance:**
- App startup time < 2 seconds
- Dashboard updates < 500ms latency
- Responsive UI (no blocking on API calls)

**Maintainability:**
- 60%+ code reuse via shared framework
- Clear module boundaries
- Documented framework API
- Easy to add new applications

**Compatibility:**
- Python 3.8+ support
- PySide6 (Qt 6.x)
- Cross-platform (Windows, Linux, macOS)
- Optional GUI dependencies: `pip install pywats[gui]`

---

## 🔒 Constraints

### Technical Constraints

1. **Qt Framework:** PySide6 (Qt 6.x) - primary UI framework
2. **Python Version:** 3.8+ (current target)
3. **Package Distribution:** Optional GUI via `pip install pywats[gui]`
4. **API Access:** All apps use same pyWATS API and client service
5. **IPC Protocol:** If implementing, must be cross-platform

### Time Constraints

- Analysis phase: 1-2 weeks (research C# apps, design framework)
- Design/decision: 1 week (architecture, API contracts)
- Implementation: 4-6 weeks (framework + 4 applications)
  - Phase 1: Framework foundation (1 week)
  - Phase 2: Configurator refactor (1 week)
  - Phase 3: Yield Monitor (2 weeks)
  - Phase 4: Package Manager (1 week)
  - Phase 5: Client Monitor (1 week)

### Breaking Changes

**Acceptable:**
- GUI import paths (`pywats_client.gui` → `pywats_ui.apps.configurator`)
- Internal GUI structure and class names
- Application entry points

**Not Acceptable:**
- CLI interface (`pywats-client` command)
- Client service API
- Configuration file formats (backward compatible migrations only)

---

## 🏗️ Architecture Options

### Current Structure
```
src/
  pywats_client/
    gui/                    # Single tightly coupled app
      main_window.py
      config_dialog.py
    cli.py
    service.py
```

### Proposed: Separate UI Package

**Recommended Structure:**
```
src/
  pywats_client/           # Headless service (no GUI deps)
    service/
    cli.py
    
  pywats_ui/               # NEW: Shared UI framework
    framework/             # Reusable base classes
      base_app.py          # BaseApplication
      base_window.py       # BaseMainWindow
      dialogs/             # Common dialogs
      widgets/             # Custom widgets
      themes/              # Styling system
      ipc/                 # Inter-app communication
      
    apps/                  # Applications
      configurator/        # Client Configurator
        main.py
        windows/
        dialogs/
        
      yield_monitor/       # NEW: Yield Monitor
        main.py
        dashboards/
        charts/
        
      package_manager/     # NEW: Software Package Manager
        main.py
        views/
        upload/
        
      client_monitor/      # NEW: Client Monitor
        main.py
        monitors/
        alarms/
```

**Entry Points (pyproject.toml):**
```toml
[project.scripts]
pywats-configurator = "pywats_ui.apps.configurator.main:main"
pywats-yield-monitor = "pywats_ui.apps.yield_monitor.main:main"
pywats-package-manager = "pywats_ui.apps.package_manager.main:main"
pywats-client-monitor = "pywats_ui.apps.client_monitor.main:main"
```

### Alternative: Monorepo with Separate Packages

```
packages/
  pywats-api/              # Core API
  pywats-client/           # Headless service
  pywats-ui-framework/     # Shared framework
  pywats-configurator/     # App 1
  pywats-yield-monitor/    # App 2
  pywats-package-manager/  # App 3
  pywats-client-monitor/   # App 4
```

**Pros:**
- Independent versioning
- Can install apps separately
- Clear dependency boundaries

**Cons:**
- Complex build/release process
- Harder to maintain version compatibility
- More repository overhead

### Impact Analysis

**Recommended: Single Package with Submodules**
- ✅ Simpler distribution (`pip install pywats[gui]`)
- ✅ Version synchronization
- ✅ Easier development workflow
- ✅ All apps share same framework version
- ❌ Larger package size (but GUI is optional)

---

## 🎨 C# Reference Application Analysis

### Identified Components

From C# codebase enumeration:
```csharp
public enum Modules { 
    Database = 1, 
    TransferAgent = 2, 
    Datacenter = 3, 
    Controlpanel = 4,          // Control Panel (UI)
    Clientmonitor = 5,         // ✅ Client Monitor (Target App #4)
    ServerConfigurator = 6,     // ✅ Configurator (Target App #1)
    TestStation = 7, 
    Core = 8, 
    MESDatabase = 9 
}

public enum ServiceTypes {
    S_EmailBasedYieldMonitor = 14,  // ✅ Yield Monitor (Target App #2)
    // ... other services
}
```

### Application Feature Mapping

**1. Client Configurator** (ServerConfigurator)
- Connection settings (URL, credentials)
- Converter configuration
- Test station setup
- Service control (start/stop/restart)
- Validation and testing
- **Status:** Exists in Python, needs refactoring

**2. Yield Monitor** (EmailBasedYieldMonitor service + UI)
- Real-time yield statistics
- Process-specific dashboards (ICT, FCT, EOL)
- Email alerts for thresholds
- Trend analysis
- **Status:** Service exists (alarm_monitor.py), needs UI

**3. Software Package Manager** (TBD - research needed)
- Package browsing and search
- Upload workflow
- Review/approval process
- Release management
- **Status:** NEW - needs full implementation

**4. Client Monitor** (Clientmonitor)
- Service health dashboard
- Connection status
- Performance metrics
- Alarm viewing
- **Status:** NEW - needs full implementation

### Shared Framework Requirements (Derived from C#)

**Common UI Patterns:**
1. **Connection Management** - All apps need server connection
2. **Authentication** - Shared credential handling
3. **Settings Dialog** - Per-app configuration
4. **Status Bar** - Connection status, service status
5. **Menu Bar** - File, Edit, View, Tools, Help
6. **Toolbar** - Common actions (refresh, settings, etc.)
7. **Dialogs** - Error handling, confirmation, progress

**Common Data Patterns:**
1. **API Client** - Shared pyWATS API instance
2. **Configuration** - App-specific settings storage
3. **Logging** - Unified logging infrastructure
4. **Error Handling** - Consistent user feedback

---

## 🔌 Inter-App Communication Options

### Option 1: Message Bus (Recommended)
```python
# Centralized event bus
from pywats_ui.framework.ipc import MessageBus

# App 1 publishes
bus.publish("connection.changed", {"url": "...", "status": "connected"})

# App 2 subscribes
bus.subscribe("connection.changed", on_connection_changed)
```

**Pros:**
- Decoupled communication
- Easy to extend (new apps can listen)
- Works across process boundaries (QLocalSocket backend)

**Cons:**
- Adds complexity
- Need to manage message schemas

### Option 2: Shared Configuration
```python
# Apps monitor shared config file
from pywats_ui.framework.config import SharedConfig

config = SharedConfig.instance()
config.watch("connection.url", on_url_changed)
```

**Pros:**
- Simple implementation
- Persistence built-in

**Cons:**
- File-based (slower)
- Limited to configuration data

### Option 3: REST API (pyWATS Client Service)
```python
# Apps call client service endpoints
client_service.get_status()
client_service.subscribe_alarms(callback)
```

**Pros:**
- Already exists
- Well-defined API

**Cons:**
- Requires service running
- Network overhead (even local)

**Recommendation:** Hybrid approach:
- **Configuration:** SharedConfig for settings
- **Events:** MessageBus for real-time updates
- **Data:** pyWATS API for all data operations

---

## 🎯 Shared Framework API Design

### Base Classes

**BaseApplication:**
```python
class BaseApplication(QApplication):
    """Base class for all pyWATS GUI applications."""
    
    def __init__(self, app_name: str, app_version: str):
        """Initialize application with name and version."""
        
    def setup_logging(self) -> None:
        """Configure application logging."""
        
    def load_config(self) -> AppConfig:
        """Load application configuration."""
        
    def connect_to_api(self) -> pyWATS:
        """Establish connection to pyWATS API."""
```

**BaseMainWindow:**
```python
class BaseMainWindow(QMainWindow):
    """Base class for main application windows."""
    
    def __init__(self, app: BaseApplication):
        """Initialize main window."""
        
    def create_menu_bar(self) -> None:
        """Create standard menu bar."""
        
    def create_toolbar(self) -> None:
        """Create standard toolbar."""
        
    def create_status_bar(self) -> None:
        """Create status bar with connection indicator."""
        
    def show_error(self, title: str, message: str) -> None:
        """Display error dialog."""
        
    def show_progress(self, title: str, task: Callable) -> Any:
        """Execute task with progress dialog."""
```

### Common Dialogs

```python
# Connection dialog (used by all apps)
from pywats_ui.framework.dialogs import ConnectionDialog

dialog = ConnectionDialog(parent=self)
if dialog.exec():
    url, token = dialog.get_connection_info()
    
# Settings dialog (customizable)
from pywats_ui.framework.dialogs import SettingsDialog

dialog = SettingsDialog(parent=self)
dialog.add_section("General", general_widget)
dialog.add_section("Logging", logging_widget)
```

### Widget Library

```python
# Styled inputs with validation
from pywats_ui.framework.widgets import (
    ValidatedLineEdit,
    ConnectionStatusWidget,
    LogViewerWidget,
    ChartWidget,
)

# API-aware widgets
from pywats_ui.framework.widgets import (
    ProductSelector,
    ProcessSelector,
    DateRangeSelector,
)
```

---

## 📐 Recommended Architecture

### Package Structure (Final Recommendation)

```
src/pywats_ui/
    __init__.py
    
    framework/                      # Shared framework (60%+ code reuse)
        __init__.py
        base_app.py                 # BaseApplication
        base_window.py              # BaseMainWindow
        
        dialogs/                    # Common dialogs
            __init__.py
            connection.py           # ConnectionDialog
            settings.py             # SettingsDialog
            progress.py             # ProgressDialog
            error.py                # ErrorDialog
            
        widgets/                    # Reusable widgets
            __init__.py
            validated_inputs.py     # ValidatedLineEdit, etc.
            status.py               # ConnectionStatusWidget
            log_viewer.py           # LogViewerWidget
            charts.py               # ChartWidget (for Yield Monitor)
            api_widgets.py          # ProductSelector, etc.
            
        ipc/                        # Inter-app communication
            __init__.py
            message_bus.py          # Event bus implementation
            shared_config.py        # Shared configuration
            
        themes/                     # Styling
            __init__.py
            default.qss             # Default stylesheet
            dark.qss                # Dark theme
            theme_manager.py        # Theme switching
            
        utils/                      # Utilities
            __init__.py
            validators.py           # Input validation
            formatters.py           # Data formatting
            
    apps/                           # Applications (40% app-specific)
        __init__.py
        
        configurator/               # ✅ App #1: Client Configurator
            __init__.py
            main.py                 # Entry point
            main_window.py          # Main window
            windows/                # Additional windows
            dialogs/                # App-specific dialogs
            
        yield_monitor/              # ✅ App #2: Yield Monitor
            __init__.py
            main.py
            main_window.py
            dashboards/             # Dashboard components
                process_dashboard.py
                trend_dashboard.py
            charts/                 # Chart components
                yield_chart.py
                failure_chart.py
                
        package_manager/            # ✅ App #3: Software Package Manager
            __init__.py
            main.py
            main_window.py
            views/                  # List/detail views
                package_list.py
                package_detail.py
            upload/                 # Upload workflow
                upload_dialog.py
                review_dialog.py
                
        client_monitor/             # ✅ App #4: Client Monitor
            __init__.py
            main.py
            main_window.py
            monitors/               # Monitoring components
                health_monitor.py
                performance_monitor.py
            alarms/                 # Alarm management
                alarm_viewer.py
                alarm_detail.py
```

### Dependency Graph

```
┌─────────────────────────────────────────┐
│          pywats (Core API)              │
│  - Product, Report, Analytics, etc.     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       pywats_client (Service)           │
│  - Background service                   │
│  - Alarm monitoring                     │
│  - Converter execution                  │
└─────────────────┬───────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
┌────────▼──────┐  ┌───────▼──────────────┐
│ pywats_ui/    │  │  CLI (Headless)      │
│ framework     │  │  - Service control   │
│ (Shared 60%)  │  │  - No GUI deps       │
└────────┬──────┘  └──────────────────────┘
         │
   ┌─────┴─────┬──────────┬──────────┐
   │           │          │          │
┌──▼──┐   ┌───▼────┐ ┌───▼────┐ ┌───▼────┐
│ App1│   │ App2   │ │ App3   │ │ App4   │
│Conf │   │Yield   │ │Package │ │Monitor │
└─────┘   └────────┘ └────────┘ └────────┘
```

---

## 🚦 Next Steps

1. **Research Phase** (2-3 days)
   - Review existing GUI code (`pywats_client/gui/`)
   - Study C# application features in detail
   - Identify Qt/PySide6 best practices
   - Research IPC options (QLocalSocket, message bus libraries)

2. **Design Phase** (3-5 days)
   - Create detailed framework API specification
   - Design message bus schema
   - Define shared widget interfaces
   - Plan migration path for existing configurator

3. **Prototype Phase** (1 week)
   - Build framework foundation
   - Port one dialog to new framework (proof of concept)
   - Test IPC communication between dummy apps
   - Validate performance and usability

4. **Implementation Phase** (4-6 weeks)
   - See Implementation Plan for detailed roadmap

---

## 🎓 Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Framework over-engineering | High | Medium | Start simple, iterate based on needs |
| Qt version compatibility | Medium | Low | Use PySide6 stable APIs only |
| IPC complexity | Medium | Medium | Make IPC optional, apps work standalone |
| Performance overhead | Medium | Low | Profile early, optimize critical paths |
| Code duplication creep | High | Medium | Enforce framework usage via code reviews |
| Migration breaks existing GUI | High | Low | Extensive testing, gradual rollout |

---

## 📚 Research References

**Qt/PySide6:**
- Qt Application Architecture: https://doc.qt.io/qt-6/application-architecture.html
- Model/View Programming: https://doc.qt.io/qt-6/model-view-programming.html
- Inter-Process Communication: https://doc.qt.io/qt-6/ipc.html

**Python GUI Frameworks:**
- PySide6 Documentation: https://doc.qt.io/qtforpython-6/
- Qt Style Sheets: https://doc.qt.io/qt-6/stylesheet.html

**Architecture Patterns:**
- MVP (Model-View-Presenter) for testability
- Signal/Slot for decoupled communication
- Repository pattern for data access

---

**Analysis Status:** ✅ Complete  
**Next Document:** [02_IMPLEMENTATION_PLAN.md](02_IMPLEMENTATION_PLAN.md)
- ❌ Less clear separation
- ❌ Client still has GUI code (just organized differently)

**Option 3 (Monorepo):**
- ✅ Maximum separation and reusability
- ✅ Independent versioning
- ❌ Most complex to set up and maintain
- ❌ Requires monorepo tooling

---

## ⚠️ Risk Assessment

### HIGH Risk
- **Breaking existing workflows:** Users expect `pywats-client gui` to work
  - *Mitigation:* Maintain command compatibility, deprecate gracefully
  
- **Increased complexity:** More packages/modules to maintain
  - *Mitigation:* Clear documentation, automated tests

### MEDIUM Risk
- **Dependency management:** Qt dependencies need careful handling
  - *Mitigation:* Optional dependencies, clear install instructions

- **IPC changes:** GUI-service communication might need refactoring
  - *Mitigation:* Version IPC protocol, maintain backward compatibility

### LOW Risk
- **Performance impact:** Separation might add overhead
  - *Mitigation:* Measure before/after, optimize if needed

- **Learning curve:** Contributors need to understand new structure
  - *Mitigation:* Architecture documentation, contribution guide

---

## 🔍 Additional Considerations

### Reusable Framework Components

**What should be shared:**
1. **Core UI Framework:**
   - Application base class
   - Window management
   - Dialog utilities
   - Event handling patterns

2. **Common Widgets:**
   - Connection status indicator
   - Log viewer component
   - Settings panel
   - Progress dialogs

3. **Client Integration:**
   - IPC client wrapper
   - Authentication handling
   - Configuration management
   - Error handling patterns

4. **Utilities:**
   - Theme/styling
   - Icon management
   - Layout helpers
   - Validation patterns

### Future Applications

**Potential standalone tools:**
- Log Viewer (read client/WATS logs)
- Report Analyzer (visualize test data)
- Configuration Manager (edit configs without full client)
- Health Monitor (lightweight status dashboard)
- Converter Sandbox Manager (test/debug converters)

---

## 📊 Comparison Matrix

| Aspect | Option 1: Separate Pkg | Option 2: Subpackage | Option 3: Monorepo |
|--------|----------------------|---------------------|-------------------|
| Separation Clarity | ★★★★★ | ★★★☆☆ | ★★★★★ |
| Ease of Maintenance | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ |
| Distribution Complexity | ★★★☆☆ | ★★★★★ | ★★☆☆☆ |
| Reusability | ★★★★★ | ★★★☆☆ | ★★★★★ |
| Migration Effort | ★★★☆☆ | ★★★★☆ | ★★☆☆☆ |
| **Overall** | **17/25** | **18/25** | **16/25** |

---

## 🎯 Recommendation (TBD)

*To be filled after stakeholder discussion*

**Preferred Option:** TBD  
**Rationale:** TBD  
**Trade-offs Accepted:** TBD
