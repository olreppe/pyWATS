# TODO: Multi-Application GUI Framework

**Updated:** February 4, 2026  
**Scope:** 4 applications + shared framework

---

## 🧠 Phase 0: Analysis & Research (Week 1-2)

### C# Application Research
- [ ] **Study Client Configurator** (C# codebase) - Features, workflows, dialogs
- [ ] **Study Yield Monitor** - Dashboards, charts, alerting logic
- [ ] **Study Software Package Manager** - Upload workflow, review process
- [ ] **Study Client Monitor** - Health monitoring, metrics display
- [ ] **Map shared components** - Identify common UI patterns across apps
- [ ] **Document feature matrix** - Create comparison table of all 4 apps

### Qt/PySide6 Research
- [ ] **Review existing GUI code** - Audit `src/pywats_client/gui/`
- [ ] **Qt app architecture patterns** - Best practices for multi-app structure
- [ ] **Widget library design** - Research reusable component strategies
- [ ] **IPC mechanisms** - Evaluate QLocalSocket, message bus, shared memory
- [ ] **Chart libraries** - Evaluate Qt Charts, PyQtGraph, Matplotlib integration
- [ ] **Theme/styling** - Research QSS stylesheets and theme management

### Architecture Design
- [ ] **Framework API specification** - Define BaseApplication, BaseMainWindow, etc.
- [ ] **Message bus schema** - Define event types and message format
- [ ] **Shared widget interfaces** - Design ProductSelector, ChartWidget, etc.
- [ ] **Configuration strategy** - Per-app settings, shared connection info
- [ ] **Create ADR (Architecture Decision Record)** - Document chosen approach
- [ ] **Stakeholder review** - Present design for approval

---

## 🏗️ Phase 1: Framework Foundation (Week 3)

### Core Framework (`pywats_ui/framework/`)
- [ ] **Create package structure** - Set up `pywats_ui/framework/` folders
- [ ] **BaseApplication class** - App initialization, config, logging
- [ ] **BaseMainWindow class** - Menu bar, toolbar, status bar templates
- [ ] **Configuration management** - AppConfig, SharedConfig classes
- [ ] **Logging integration** - Connect to pywats.core.logging
- [ ] **API connection helper** - Shared pyWATS client management
- [ ] **Error handling** - Consistent exception→UI feedback pattern

### Common Dialogs (`pywats_ui/framework/dialogs/`)
- [ ] **ConnectionDialog** - Server URL, credentials input
- [ ] **SettingsDialog** - Extensible settings with tabs
- [ ] **ProgressDialog** - Task execution with cancel support
- [ ] **ErrorDialog** - Formatted error display with details
- [ ] **ConfirmationDialog** - Standard yes/no/cancel

### Widget Library (`pywats_ui/framework/widgets/`)
- [ ] **ValidatedLineEdit** - Input validation with visual feedback
- [ ] **ConnectionStatusWidget** - Connection indicator for status bar
- [ ] **LogViewerWidget** - Real-time log display with filtering
- [ ] **ProductSelector** - Dropdown/autocomplete for products
- [ ] **ProcessSelector** - Process type selection
- [ ] **DateRangeSelector** - Start/end date picker

### IPC Layer (`pywats_ui/framework/ipc/`)
- [ ] **MessageBus** - Event publish/subscribe across apps
- [ ] **SharedConfig** - File-based shared configuration
- [ ] **IPC protocol** - Define message schema and transport (QLocalSocket)

### Theming (`pywats_ui/framework/themes/`)
- [ ] **ThemeManager** - Theme loading and switching
- [ ] **default.qss** - Default stylesheet
- [ ] **dark.qss** - Dark theme stylesheet

### Framework Tests
- [ ] **test_base_app.py** - BaseApplication tests
- [ ] **test_dialogs.py** - Dialog functionality
- [ ] **test_widgets.py** - Widget validation
- [ ] **test_ipc.py** - Message bus and shared config

---

## 🔧 Phase 2: Client Configurator (Week 4)

### Migration to New Framework
- [ ] **Create `pywats_ui/apps/configurator/`** - New package structure
- [ ] **Port main_window.py** - Refactor to use BaseMainWindow
- [ ] **Port dialogs** - Use framework dialogs where possible
- [ ] **Port custom widgets** - Integrate with framework widgets
- [ ] **Update entry point** - Create `main.py` using BaseApplication
- [ ] **CLI integration** - Update `pywats-client gui` command
- [ ] **Backward compatibility** - Deprecation warnings for old imports

### Testing
- [ ] **Unit tests** - Configurator-specific logic
- [ ] **Integration tests** - End-to-end workflows
- [ ] **Cross-platform testing** - Windows, Linux, macOS

---

## 📊 Phase 3: Yield Monitor (Week 5-6)

### Dashboard Components (`pywats_ui/apps/yield_monitor/dashboards/`)
- [ ] **ProcessDashboard** - Yield by process (ICT, FCT, EOL)
- [ ] **TrendDashboard** - Historical yield trends
- [ ] **FailureDashboard** - Top failure analysis

### Chart Components (`pywats_ui/apps/yield_monitor/charts/`)
- [ ] **YieldChart** - Real-time yield visualization
- [ ] **FailureChart** - Pareto chart for failures
- [ ] **TrendChart** - Time-series trend lines
- [ ] **Chart library integration** - Qt Charts or PyQtGraph

### Main Window
- [ ] **Create main_window.py** - Dashboard container with tabs
- [ ] **Toolbar actions** - Refresh, time range, export
- [ ] **Status bar** - Last update time, connection status
- [ ] **Menu bar** - File, View, Settings, Help

### Data Integration
- [ ] **Analytics service integration** - Use `api.analytics` endpoints
- [ ] **Real-time updates** - Polling or WebSocket for live data
- [ ] **Caching strategy** - Reduce API calls, improve performance

### Testing
- [ ] **Chart rendering tests** - Verify visualization accuracy
- [ ] **Data refresh tests** - Polling and updates
- [ ] **Performance tests** - Large dataset handling

---

## 📦 Phase 4: Software Package Manager (Week 7)

### Views (`pywats_ui/apps/package_manager/views/`)
- [ ] **PackageListView** - Browse available packages
- [ ] **PackageDetailView** - Package metadata and files

### Upload Workflow (`pywats_ui/apps/package_manager/upload/`)
- [ ] **UploadDialog** - ZIP file selection and metadata
- [ ] **ReviewDialog** - Review and approve workflow
- [ ] **ProgressWidget** - Upload progress tracking

### Main Window
- [ ] **Create main_window.py** - List/detail layout
- [ ] **Toolbar actions** - Upload, refresh, review, release
- [ ] **Search/filter** - Package search and filtering

### Data Integration
- [ ] **Software service integration** - Use `api.software` endpoints
- [ ] **File upload handling** - Large file upload with progress
- [ ] **Validation** - Package validation before upload

### Testing
- [ ] **Upload workflow tests** - End-to-end upload
- [ ] **Review process tests** - Approval workflow
- [ ] **File handling tests** - Large file uploads

---

## 🖥️ Phase 5: Client Monitor (Week 8)

### Monitors (`pywats_ui/apps/client_monitor/monitors/`)
- [ ] **HealthMonitor** - Service health dashboard
- [ ] **PerformanceMonitor** - CPU, memory, disk metrics
- [ ] **ConnectionMonitor** - API connection status

### Alarms (`pywats_ui/apps/client_monitor/alarms/`)
- [ ] **AlarmViewer** - Real-time alarm list
- [ ] **AlarmDetailDialog** - Alarm details and actions
- [ ] **Alarm filtering** - By severity, time, source

### Main Window
- [ ] **Create main_window.py** - Multi-panel dashboard
- [ ] **Real-time updates** - Service status polling
- [ ] **Alert notifications** - System tray or toast notifications

### Data Integration
- [ ] **Client service API** - Health check endpoints
- [ ] **Alarm service integration** - Use alarm_monitor.py
- [ ] **Performance metrics** - System resource monitoring

### Testing
- [ ] **Real-time update tests** - Polling and data refresh
- [ ] **Alarm handling tests** - Notification and acknowledgment
- [ ] **Performance tests** - Resource monitoring accuracy

---

## 📚 Phase 6: Documentation & Examples (Week 9)

### User Documentation
- [ ] **docs/guides/gui_framework.md** - Framework overview and concepts
- [ ] **docs/guides/building_apps.md** - Developer guide for new apps
- [ ] **docs/guides/app_communication.md** - IPC and message bus usage
- [ ] **Application READMEs** - User guide for each app

### API Documentation
- [ ] **Sphinx docs for pywats_ui** - Auto-generated API reference
- [ ] **Framework examples** - Minimal app, custom widget, etc.
- [ ] **Code documentation** - Comprehensive docstrings

### Examples
- [ ] **examples/gui/minimal_app.py** - Simplest BaseApplication usage
- [ ] **examples/gui/custom_widget.py** - Creating custom widgets
- [ ] **examples/gui/ipc_demo.py** - Message bus communication

---

## 🚀 Phase 7: Testing & Release (Week 10)

### Quality Assurance
- [ ] **Full test suite execution** - All 4 apps + framework
- [ ] **Cross-platform testing** - Windows, Linux, macOS
- [ ] **Performance profiling** - App startup, dashboard updates
- [ ] **Memory leak testing** - Long-running app stability
- [ ] **Code linting** - flake8, mypy type checking

### Release Preparation
- [ ] **Update CHANGELOG.md** - All new features and changes
- [ ] **Migration guide** - Breaking changes and upgrade path
- [ ] **pyproject.toml updates** - Entry points for all 4 apps
- [ ] **Package distribution** - `pip install pywats[gui]`
- [ ] **Version bump** - Semantic versioning for release
- [ ] **Git tag and release** - GitHub release with binaries

---

## 🚧 In Progress

(Currently empty - starting fresh with Phase 0)

---

## ✅ Completed

(None yet - project just starting)

---

## ✅ Completed

- [✅] Project structure created - `gui-client-separation.project/`
- [✅] README.md drafted
- [✅] 01_ANALYSIS.md - Initial draft complete
- [✅] 02_IMPLEMENTATION_PLAN.md - Phased approach outlined
- [✅] 03_PROGRESS.md - Session tracking established
- [✅] 04_TODO.md (this file) - Task breakdown created

---

## ⏸️ Blocked

*None currently*

---

## 🔍 Research Tasks

- [ ] **Survey existing GUI frameworks** - Review how other Python projects handle multi-app GUI architectures
- [ ] **Qt application lifecycle** - Best practices for managing multiple windows/apps
- [ ] **IPC patterns** - Optimal GUI-to-service communication patterns
- [ ] **Theme/styling** - QSS (Qt Style Sheets) or other theming approaches
- [ ] **Distribution strategy** - How to package optional GUI dependencies

---

## 📋 Quick Actions

### Before Starting Implementation
1. Read through analysis document completely
2. Review current `pywats_client/gui/` code structure
3. Test current GUI functionality as baseline
4. Make architecture decision
5. Get stakeholder sign-off

### When Starting Implementation
1. Create feature branch: `git checkout -b feature/gui-client-separation`
2. Mark first TODO item with 🚧
3. Update PROGRESS.md with session start
4. Proceed with Phase 1 tasks

---

## 🎯 Success Tracking

**Definition of Done for Each Phase:**

✅ **Phase 0:** ADR approved, implementation plan finalized  
✅ **Phase 1:** Framework package functional, tests passing  
✅ **Phase 2:** Configurator migrated, all existing tests pass  
✅ **Phase 3:** Documentation complete, example app works  
✅ **Phase 4:** Release tagged, CHANGELOG updated  

---

*Last Updated: February 3, 2026*  
*Total Tasks: 35+*  
*Completed: 6*  
*In Progress: 2*  
*Blocked: 0*
