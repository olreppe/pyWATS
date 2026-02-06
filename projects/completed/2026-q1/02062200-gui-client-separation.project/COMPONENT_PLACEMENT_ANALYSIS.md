# Component Placement Analysis - Where Should Code Live?

**Date:** February 4, 2026  
**Question:** Should GUI components be in `pywats_client.core/`, `pywats_ui.framework/`, or app-specific?

---

## 🔍 Key Question: What Belongs Where?

### Three Potential Locations:

1. **`pywats_client.core/`** - Client infrastructure (shared between GUI, CLI, service)
2. **`pywats_ui.framework/`** - GUI framework (shared across all GUI apps)
3. **`pywats_ui.apps.{app}/`** - App-specific implementations

---

## 📊 Current `pywats_client.core/` Analysis

### What's Already in Core:

| Component | Qt Dependencies? | Used By |
|-----------|------------------|---------|
| **AsyncTaskRunner** | ✅ YES (QObject, Signal) | GUI only |
| **EventBus** | ✅ YES (QObject, Signal) | GUI + Service |
| **InstanceManager** | ❌ NO (file-based) | GUI + Service |
| **ConnectionConfig** | ❌ NO (dataclass) | GUI + Service |
| **ClientConfig** | ❌ NO (dataclass) | GUI + Service |
| **Encryption/Security** | ❌ NO | GUI + Service |
| **Logging** | ❌ NO | GUI + Service |
| **FileUtils** | ❌ NO | GUI + Service |

### CRITICAL FINDING: AsyncTaskRunner has Qt dependencies!

```python
# pywats_client/core/async_runner.py
from PySide6.QtCore import QObject, Signal, QThread

class AsyncTaskRunner(QObject):
    task_completed = Signal(object)
    task_error = Signal(Exception)
```

**Question:** If AsyncTaskRunner is Qt-specific, why is it in `core/`?

**Answer:** Because `pywats_client.core/` is "client infrastructure" NOT "platform-independent infrastructure"
- The "client" package includes GUI support
- Having Qt in `core/` is acceptable for client-specific infrastructure
- Service doesn't import from `pywats_client.core.async_runner`

---

## 🎯 Component-by-Component Analysis

### 1. AsyncAPIRunner (402 lines - `gui/async_api_runner.py`)

**Current Location:** `src/pywats_client/gui/async_api_runner.py`  
**Qt Dependencies:** YES (uses AsyncTaskRunner which has Qt signals)  
**Used By:** All GUI pages (wraps API calls)

**Options:**
- A) Leave in `pywats_client.core/` (alongside AsyncTaskRunner) ❓
- B) Move to `pywats_ui.framework/` (GUI framework) ✅
- C) Keep app-specific ❌

**Recommendation:** **B) pywats_ui.framework/**
- It's a GUI-specific wrapper around API calls
- Every GUI app will need it
- It's framework-level, not core-level
- **Core should be lower-level** (AsyncTaskRunner, EventBus)
- **Framework is higher-level** (AsyncAPIRunner uses AsyncTaskRunner)

---

### 2. ErrorHandlingMixin (~200 lines - `gui/error_mixin.py`)

**Current Location:** `src/pywats_client/gui/error_mixin.py`  
**Qt Dependencies:** YES (QMessageBox, QWidget)  
**Used By:** All GUI pages (error dialogs)

**Options:**
- A) Move to `pywats_client.core/` ❌ (Qt-specific)
- B) Move to `pywats_ui.framework/` ✅
- C) Keep app-specific ❌

**Recommendation:** **B) pywats_ui.framework/**
- Every GUI app needs error handling
- It's pure Qt (QMessageBox)
- Framework-level utility

---

### 3. BasePage (351 lines - `gui/pages/base.py`)

**Current Location:** `src/pywats_client/gui/pages/base.py`  
**Qt Dependencies:** YES (QWidget, QVBoxLayout, etc.)  
**Used By:** All page-based GUI apps

**Options:**
- A) Move to `pywats_client.core/` ❌ (Qt-specific)
- B) Move to `pywats_ui.framework/` ✅
- C) Keep app-specific ❌

**Recommendation:** **B) pywats_ui.framework/**
- Base class for all pages
- Framework-level abstraction
- Shared across all page-based apps

---

### 4. Styles / Dark Theme (405 lines - `gui/styles.py`)

**Current Location:** `src/pywats_client/gui/styles.py`  
**Qt Dependencies:** YES (QSS stylesheets)  
**Used By:** All GUI apps (consistent look)

**Options:**
- A) Move to `pywats_client.core/` ❌ (Qt-specific)
- B) Move to `pywats_ui.framework/themes/` ✅
- C) Keep app-specific ❌

**Recommendation:** **B) pywats_ui.framework/themes/**
- Every app needs consistent styling
- Framework-level resource
- Could have multiple themes (dark, light)

---

### 5. ScriptEditor (1106 lines - `gui/widgets/script_editor.py`)

**Current Location:** `src/pywats_client/gui/widgets/script_editor.py`  
**Qt Dependencies:** YES (complex Qt widget)  
**Used By:** Configurator (converter editing), possibly AI Chat (show/edit code)

**Options:**
- A) Move to `pywats_client.core/` ❌ (Qt-specific)
- B) Move to `pywats_ui.widgets/` ✅ (reusable widget library)
- C) Keep in `pywats_ui.apps.configurator/` ❓ (app-specific)

**Recommendation:** **B) pywats_ui.widgets/**
- It's a reusable component (could be used by multiple apps)
- Too large/complex to duplicate
- Widget library is the right level of abstraction
- **Even if only Configurator uses it now**, AI Chat might want to show/edit Python code

---

### 6. StatusIndicator (~50 lines - `gui/pages/dashboard.py`)

**Current Location:** Embedded in `src/pywats_client/gui/pages/dashboard.py`  
**Qt Dependencies:** YES (QFrame)  
**Used By:** Dashboard, Station Monitoring, Service Control

**Options:**
- A) Move to `pywats_client.core/` ❌ (Qt-specific)
- B) Move to `pywats_ui.widgets/` ✅ (reusable widget library)
- C) Keep app-specific ❌ (multiple apps need it)

**Recommendation:** **B) pywats_ui.widgets/**
- Simple, reusable widget (colored status circle)
- Multiple apps will need status indicators
- Extract from dashboard.py to standalone widget

---

### 7. LoginWindow (`gui/login_window.py`)

**Current Location:** `src/pywats_client/gui/login_window.py`  
**Qt Dependencies:** YES (QDialog)  
**Used By:** All apps that need authentication

**Options:**
- A) Move to `pywats_client.core/` ❌ (Qt-specific)
- B) Move to `pywats_ui.framework/` ✅ OR `pywats_ui.dialogs/` ✅
- C) Keep app-specific ❌

**Recommendation:** **B) pywats_ui.dialogs/** (or framework/)
- Reusable dialog
- Most apps need authentication
- Dialog library is appropriate

---

### 8. SettingsDialog (`gui/settings_dialog.py`)

**Current Location:** `src/pywats_client/gui/settings_dialog.py`  
**Qt Dependencies:** YES (QDialog)  
**Used By:** All apps (app settings)

**Options:**
- A) Move to `pywats_client.core/` ❌ (Qt-specific)
- B) Move to `pywats_ui.framework/` ✅ OR `pywats_ui.dialogs/` ✅
- C) Keep app-specific ❌

**Recommendation:** **B) pywats_ui.dialogs/** (or framework/)
- Reusable dialog
- Every app has settings
- Dialog library is appropriate

---

## ✅ Final Recommendations

### Keep in `pywats_client.core/` (IMPORT - no changes):
- ✅ **AsyncTaskRunner** - Qt-based async infrastructure (already there, works fine)
- ✅ **EventBus** - Qt-based pub/sub (already there, works fine)
- ✅ **InstanceManager** - File-based locking (platform-independent)
- ✅ **ConnectionConfig** - Connection state (platform-independent)
- ✅ **ClientConfig** - Configuration (platform-independent)
- ✅ **Encryption, Security, Logging, FileUtils** - Platform-independent utilities

**Reasoning:** These are client infrastructure, shared by GUI and service. Qt dependencies are acceptable in `pywats_client.core/` because it's client-specific, not a general-purpose library.

---

### Move to `pywats_ui.framework/`:
- ✅ **AsyncAPIRunner** - Higher-level GUI helper (uses AsyncTaskRunner)
- ✅ **ErrorHandlingMixin** - Qt error dialogs
- ✅ **BasePage** - Page base class
- ✅ **BaseApplication** - App setup (qasync, single-instance)
- ✅ **BaseMainWindow** - Main window base class
- ✅ **Styles/Themes** - QSS stylesheets

**Reasoning:** Framework-level GUI infrastructure, shared across all apps.

---

### Move to `pywats_ui.widgets/`:
- ✅ **ScriptEditor** - Reusable Python editor widget
- ✅ **StatusIndicator** - Reusable status display widget
- ✅ **Other widgets** - Any reusable Qt widgets

**Reasoning:** Widget library for reusable components.

---

### Move to `pywats_ui.dialogs/`:
- ✅ **LoginWindow** - Authentication dialog
- ✅ **SettingsDialog** - Settings dialog
- ✅ **ConnectionDialog** - Connection config dialog
- ✅ **Other dialogs** - Any reusable Qt dialogs

**Reasoning:** Dialog library for reusable modal/modeless dialogs.

---

### Keep in `pywats_ui.apps.{app}/`:
- ✅ **App main window** - App-specific main window
- ✅ **App pages** - App-specific pages
- ✅ **App logic** - App-specific business logic

**Reasoning:** App-specific implementations.

---

## 🏗️ Proposed Package Structure

```
pywats_client/
├── core/                           # Client infrastructure (GUI + Service)
│   ├── async_runner.py            # ✅ KEEP (Qt-based, already here)
│   ├── event_bus.py               # ✅ KEEP (Qt-based, already here)
│   ├── instance_manager.py        # ✅ KEEP (platform-independent)
│   ├── connection_config.py       # ✅ KEEP (platform-independent)
│   ├── config.py                  # ✅ KEEP (ClientConfig)
│   ├── encryption.py              # ✅ KEEP
│   ├── security.py                # ✅ KEEP
│   ├── logging.py                 # ✅ KEEP
│   └── file_utils.py              # ✅ KEEP
│
├── gui/                           # OLD GUI (keep as-is, no deprecation)
│   └── ... (unchanged)
│
└── service/                       # Service layer (unchanged)
    └── ...

pywats_ui/
├── framework/                     # GUI framework (shared infrastructure)
│   ├── __init__.py               # Export: BaseApplication, BaseMainWindow, etc.
│   ├── base_application.py       # ✅ COPY from gui/app.py patterns
│   ├── base_main_window.py       # ✅ COPY from gui/main_window.py patterns
│   ├── base_page.py              # ✅ COPY from gui/pages/base.py
│   ├── async_api_runner.py       # ✅ COPY from gui/async_api_runner.py
│   ├── error_mixin.py            # ✅ COPY from gui/error_mixin.py
│   └── themes/
│       ├── dark.qss              # ✅ COPY from gui/styles.py
│       └── light.qss             # Optional
│
├── widgets/                       # Reusable widget library
│   ├── __init__.py
│   ├── script_editor.py          # ✅ COPY from gui/widgets/script_editor.py
│   ├── status_indicator.py       # ✅ EXTRACT from gui/pages/dashboard.py
│   └── ... (other reusable widgets)
│
├── dialogs/                       # Reusable dialog library
│   ├── __init__.py
│   ├── login_window.py           # ✅ COPY from gui/login_window.py
│   ├── settings_dialog.py        # ✅ COPY from gui/settings_dialog.py
│   └── ... (other dialogs)
│
├── apps/                          # Applications
│   ├── configurator/             # Configurator app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── main_window.py
│   │   └── pages/
│   │       ├── connection.py     # ✅ COPY from gui/pages/connection.py
│   │       ├── setup.py          # ✅ COPY from gui/pages/setup.py
│   │       ├── converters.py     # ✅ COPY from gui/pages/converters.py
│   │       └── ...
│   │
│   ├── aichat/                   # AI Chat app
│   │   └── ...
│   │
│   └── template/                 # Template for new apps
│       └── ...
│
└── __init__.py
```

---

## 🎯 Key Design Principles

### 1. Core vs Framework Distinction:
- **`pywats_client.core/`** = Low-level client infrastructure (can have Qt)
- **`pywats_ui.framework/`** = High-level GUI framework (uses core)
- Framework IMPORTS from core, builds on top

### 2. Layering:
```
pywats_ui.apps.{app}              # App layer (uses framework)
    ↓ imports
pywats_ui.framework               # Framework layer (uses core + Qt)
    ↓ imports
pywats_client.core                # Core layer (Qt + platform-independent)
    ↓ imports
pywats                            # API layer
```

### 3. Reusability:
- Framework = shared across ALL apps
- Widgets/Dialogs = shared where needed
- Apps = app-specific logic

---

## 🚫 What Should NOT Go in Core

Components that should NOT be in `pywats_client.core/`:

1. ❌ **AsyncAPIRunner** - Too high-level, GUI-specific wrapper
2. ❌ **ErrorHandlingMixin** - GUI-specific (QMessageBox)
3. ❌ **BasePage** - GUI-specific (QWidget)
4. ❌ **ScriptEditor** - GUI widget, not infrastructure
5. ❌ **Styles** - GUI styling, not infrastructure

**Reasoning:** Core should be foundational (AsyncTaskRunner, EventBus, config). Framework should be structural (base classes, helpers).

---

## ✅ Summary

### Question: Should components be in core?
**Answer:** NO - AsyncAPIRunner, ErrorHandlingMixin, BasePage should be in `pywats_ui.framework/`

### Why keep AsyncTaskRunner in core?
**Answer:** It's already there, it's low-level infrastructure, and it works fine. Qt dependencies in `pywats_client.core/` are acceptable for client-specific infrastructure.

### Structure:
```
IMPORT from core:     AsyncTaskRunner, EventBus, InstanceManager, Config
COPY to framework:    AsyncAPIRunner, ErrorHandlingMixin, BasePage, Styles
COPY to widgets:      ScriptEditor, StatusIndicator
COPY to dialogs:      LoginWindow, SettingsDialog
COPY to apps:         App-specific pages and logic
```

---

**Bottom Line:** The original plan was mostly correct. Nothing needs to move to `pywats_client.core/` - the framework/widgets/dialogs separation is the right approach.
