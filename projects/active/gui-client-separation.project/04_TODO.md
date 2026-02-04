# TODO: GUI Framework + Template + AI Chat Pilot

**Updated:** February 4, 2026  
**Scope:** Framework + Configurator + Template + AI Chat (Phase 1 only)

---

## 🧠 Phase 0: Analysis & Research (Week 1)

### Configurator Research
- [ ] **Audit existing GUI code** - Review `src/pywats_client/gui/` (DO NOT MODIFY)
- [ ] **Map Configurator features** - Connection, station setup, service control
- [ ] **Identify reusable patterns** - Dialogs, widgets, layouts
- [ ] **Document current limitations** - Areas for improvement
- [ ] **Platform independence analysis** - How existing client handles cross-platform

### Qt/PySide6 Research
- [ ] **Qt app architecture patterns** - Best practices for framework design
- [ ] **Widget library design** - Research reusable component strategies
- [ ] **Dialog management** - Modal, modeless, stacked dialogs
- [ ] **Theme/styling** - QSS stylesheets and theme switching
- [ ] **MVC/MVP patterns** - Separation of concerns

### AI Chat Pilot Research
- [ ] **LLM integration options** - OpenAI API, Anthropic, local models (llama.cpp)
- [ ] **Data analysis requirements** - Process capability (Cp/Cpk), SPC, RCA
- [ ] **Chat UI patterns** - Message history, streaming responses, code snippets
- [ ] **Analytics visualization** - Charts for SPC, capability analysis
- [ ] **Security considerations** - API key management, data privacy

### Application Template Design
- [ ] **Template structure** - Folder layout, boilerplate files
- [ ] **Cookiecutter vs manual** - Evaluate scaffold tool options
- [ ] **Required components** - main.py, main_window.py, config, tests
- [ ] **Documentation strategy** - README template, code comments
- [ ] **Example customization** - How to extend template

### Architecture Design
- [ ] **Framework API specification** - Define BaseApplication, BaseMainWindow
- [ ] **Shared component catalog** - List all reusable dialogs/widgets
- [ ] **Configuration strategy** - Per-app settings, shared connection
- [ ] **Create ADR (Architecture Decision Record)** - Document chosen approach

---

## 🏗️ Phase 1: Framework Foundation (Week 2)

### Core Framework (`pywats_ui/framework/`)
- [ ] **Create package structure** - Set up `pywats_ui/framework/` folders
- [ ] **BaseApplication class** - App initialization, config, logging, API connection
- [ ] **BaseMainWindow class** - Menu bar, toolbar, status bar templates
- [ ] **Configuration management** - AppConfig class with JSON persistence
- [ ] **Logging integration** - Connect to `pywats.core.logging`
- [ ] **API connection helper** - Shared pyWATS client management
- [ ] **Error handling** - Consistent exception→UI feedback pattern

### Common Dialogs (`pywats_ui/framework/dialogs/`)
- [ ] **ConnectionDialog** - Server URL, credentials input with validation
- [ ] **SettingsDialog** - Extensible tabbed settings dialog
- [ ] **ProgressDialog** - Task execution with progress bar and cancel
- [ ] **ErrorDialog** - Formatted error display with traceback
- [ ] **ConfirmationDialog** - Standard yes/no/cancel with custom text
- [ ] **AboutDialog** - App name, version, credits

### Widget Library (`pywats_ui/framework/widgets/`)
- [ ] **ValidatedLineEdit** - Input validation with visual feedback (red border)
- [ ] **ConnectionStatusWidget** - Traffic light indicator (red/yellow/green)
- [ ] **LogViewerWidget** - Real-time log display with filtering
- [ ] **ProductSelector** - Dropdown/autocomplete for products (API-aware)
- [ ] **ProcessSelector** - Process type selection (ICT, FCT, EOL)
- [ ] **DateRangeSelector** - Start/end date picker with presets

### Theming (`pywats_ui/framework/themes/`)
- [ ] **ThemeManager** - Theme loading, switching, persistence
- [ ] **default.qss** - Default light theme stylesheet
- [ ] **dark.qss** - Dark theme stylesheet
- [ ] **Theme API** - `app.set_theme("dark")`

### Framework Tests
- [ ] **test_base_app.py** - BaseApplication initialization, config
- [ ] **test_base_window.py** - BaseMainWindow layout, menus
- [ ] **test_dialogs.py** - All dialog functionality
- [ ] **test_widgets.py** - Widget validation and behavior
- [ ] **test_themes.py** - Theme loading and switching

---

## 🔧 Phase 2: Client Configurator Refactor (Week 2-3)

### Migration to New Framework
- [ ] **Create `pywats_ui/apps/configurator/`** - New package structure
- [ ] **main.py** - Entry point using BaseApplication
- [ ] **main_window.py** - Refactor to extend BaseMainWindow
- [ ] **Connection tab** - Server URL, credentials (use ConnectionDialog)
- [ ] **Station tab** - Converter settings, test configuration
- [ ] **Service tab** - Start/stop/restart controls, status display
- [ ] **Logs tab** - Use LogViewerWidget for real-time logs
- [ ] **Settings** - Use framework SettingsDialog

### Testing
- [ ] **Unit tests** - Configurator-specific logic (settings persistence, etc.)
- [ ] **Integration tests** - End-to-end workflows (connect, configure, start service)
- [ ] **Comparison testing** - Feature parity with old GUI
- [ ] **Cross-platform** - Windows, Linux, macOS

### Deprecation
- [ ] **Add warnings to old GUI** - DeprecationWarning in `pywats_client.gui.__init__`
- [ ] **Migration banner** - In-app notice in old GUI
- [ ] **Update CLI** - New `pywats-configurator` command
- [ ] **Documentation** - Migration guide (`docs/guides/migration_gui.md`)

---

## 📋 Phase 3: Application Template (Week 3)

### Template Structure
```
template/
  {{app_name}}/
    __init__.py
    main.py                 # Entry point
    main_window.py          # Main window (extends BaseMainWindow)
    config.py               # App-specific configuration
    README.md               # Usage instructions
    tests/
      test_{{app_name}}.py  # Starter tests
```

### Template Implementation
- [ ] **Create template folder** - `pywats_ui/template/` with placeholders
- [ ] **main.py template** - Boilerplate BaseApplication setup
- [ ] **main_window.py template** - Basic window with menu/toolbar
- [ ] **config.py template** - Configuration class example
- [ ] **README.md template** - Instructions for customization
- [ ] **test template** - Basic test structure

### Template Generator (Optional - Manual Copy is Fine)
- [ ] **generator.py script** - Copy template with name replacement
- [ ] **CLI command** - `pywats-create-app <name>` (optional)
- [ ] **Interactive prompts** - App name, description, author (optional)

### Template Documentation
- [ ] **Template usage guide** - `docs/guides/creating_apps.md`
- [ ] **Customization examples** - Adding tabs, custom widgets
- [ ] **Best practices** - Code organization, testing
- [ ] **Example walkthrough** - Create "HelloWorld" app from template

---

## 🤖 Phase 4: AI Chat Pilot (Week 4)

### AI Chat Application (`pywats_ui/apps/aichat/`)
- [ ] **Create app structure** - Using application template
- [ ] **main_window.py** - Chat interface layout (input, history, results)
- [ ] **chat_widget.py** - Message display with bubbles (user/assistant)
- [ ] **input_widget.py** - Multi-line text input with send button
- [ ] **results_panel.py** - Visualization panel for analysis results

### LLM Integration
- [ ] **llm_service.py** - Abstract LLM interface (OpenAI, Anthropic, local)
- [ ] **openai_provider.py** - OpenAI API integration (GPT-4)
- [ ] **anthropic_provider.py** - Claude API integration (optional)
- [ ] **local_provider.py** - Local model support (llama.cpp, optional)
- [ ] **Streaming support** - Real-time token streaming for responses
- [ ] **API key management** - Secure credential storage

### Analytics Integration
- [ ] **process_capability.py** - Cp, Cpk, Pp, Ppk calculations (use pyWATS analytics)
- [ ] **spc_analysis.py** - Control charts, limits, violations
- [ ] **rca_prompts.py** - Pre-built prompts for root cause analysis
- [ ] **data_fetcher.py** - Query pyWATS API for test data
- [ ] **Chart widgets** - Capability histogram, SPC chart (use Qt Charts)

### Chat Features
- [ ] **Query types** - Process capability, SPC analysis, RCA, general questions
- [ ] **Context awareness** - Remember conversation history
- [ ] **Data visualization** - Generate charts based on analysis
- [ ] **Export results** - Save chat, export charts (PDF/PNG)
- [ ] **Preset queries** - Quick buttons ("Analyze last 100 units", "SPC for ICT")

### Testing
- [ ] **LLM mock tests** - Test chat logic without real API calls
- [ ] **Analytics tests** - Verify capability/SPC calculations
- [ ] **UI tests** - Chat widget functionality
- [ ] **Integration tests** - End-to-end with real API (optional, slow)

---

## 📚 Phase 5: Documentation & Examples (Week 5)

### User Documentation
- [ ] **docs/guides/gui_framework.md** - Framework overview and concepts
- [ ] **docs/guides/creating_apps.md** - Application template usage
- [ ] **docs/guides/configurator_guide.md** - User guide for Configurator
- [ ] **docs/guides/aichat_guide.md** - AI Chat pilot user guide
- [ ] **Application READMEs** - Per-app user instructions

### API Documentation
- [ ] **Sphinx docs for pywats_ui** - Auto-generated framework API reference
- [ ] **Framework examples** - Minimal app, custom widget, custom dialog
- [ ] **Code documentation** - Comprehensive docstrings for all public APIs

### Examples
- [ ] **examples/gui/minimal_app.py** - Simplest BaseApplication usage
- [ ] **examples/gui/custom_widget.py** - Creating reusable widgets
- [ ] **examples/gui/theme_demo.py** - Theme switching demonstration
- [ ] **examples/gui/llm_integration.py** - LLM provider usage (for AI Chat)

### Migration Guide
- [ ] **docs/guides/migration_gui.md** - Old GUI → New Configurator
- [ ] **Breaking changes** - Document import path changes
- [ ] **Feature comparison** - Old vs new feature matrix

---

## 🚀 Phase 6: Testing & Release (Week 5)

### Quality Assurance
- [ ] **Full test suite execution** - All apps + framework tests
- [ ] **Cross-platform testing** - Windows, Linux, macOS
- [ ] **Performance profiling** - App startup, LLM response times
- [ ] **Memory leak testing** - Long-running app stability
- [ ] **Code linting** - flake8, mypy type checking (if available)

### Release Preparation
- [ ] **Update CHANGELOG.md** - Framework, Configurator, Template, AI Chat
- [ ] **Migration guide finalization** - Breaking changes and upgrade path
- [ ] **pyproject.toml updates** - Entry points for apps
- [ ] **Package distribution** - `pip install pywats[gui]` with new apps
- [ ] **Version bump** - Semantic versioning (v0.3.0)
- [ ] **Git tag and release** - GitHub release with notes

### Cleanup
- [ ] **Remove unused code** - Clean up experimental code
- [ ] **Documentation review** - Ensure all docs are accurate
- [ ] **Example verification** - All examples run successfully

---

## 🚧 In Progress

(None - starting Phase 0)

---

## ✅ Completed

- ✅ Project scope defined (Framework + Configurator + Template + AI Chat)
- ✅ Transition strategy documented (old GUI coexists)
- ✅ Initial analysis and architecture options

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
