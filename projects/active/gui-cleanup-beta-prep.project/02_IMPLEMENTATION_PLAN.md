# GUI Cleanup - Implementation Plan

**Created:** February 14, 2026, 16:00  
**Last Updated:** February 14, 2026, 16:00  
**Status:** Ready for Implementation

---

## Overview

Implement GUI cleanup for beta release with 7-tab structure, improved scaling, and better UX.

**User Decisions**:
- ✅ Option 1: Moderate cleanup (7 tabs)
- ✅ Station info: Read-only on Dashboard (edit via Setup page)
- ✅ File menu: Disconnect, Minimize to Tray, Exit
- ✅ Multi-server: Manual instance selection (current approach)

**Estimated Effort**: 8-10 hours  
**Phases**: 5

---

## Phase 1: Tab Management & File Menu (2 hours)

### 1.1 Update Navigation Items

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Current** (line 174-186):
```python
nav_items = [
    "Dashboard",
    "Setup",
    "Connection",
    "Serial Numbers",
    "API Settings",
    "Converters",
    "Software",      # ❌ REMOVE
    "Location",      # ❌ REMOVE (GPS moved to Dashboard)
    "Proxy",         # ❌ REMOVE (move to Advanced in Connection)
    "Log",
    "About"
]
```

**Target**:
```python
nav_items = [
    "Dashboard",      # Default start page
    "Connection",     # Server connection
    "Converters",     # Core feature
    "Setup",          # Station configuration
    "Serial Numbers", # Converter-related
    "Log",            # Troubleshooting
    "About"           # Info
]
```

**Changes**:
- Remove: "Software", "Location", "Proxy"
- Remove: "API Settings" (integrated into Connection → Advanced)
- Reorder: Connection before Converters (logical flow)

### 1.2 Update Pages Dictionary

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Current** (line 229-241):
```python
self._pages: Dict[str, QWidget] = {
    "Dashboard": DashboardPage(self._config),
    "Setup": SetupPage(self._config),
    "Connection": ConnectionPage(self._config),
    "Serial Numbers": SerialNumberHandlerPage(self._config),
    "API Settings": APISettingsPage(self._config),
    "Converters": ConvertersPageV2(self._config, main_window=self),
    "Software": SoftwarePage(self._config),
    "Location": LocationPage(self._config),
    "Proxy": ProxySettingsPage(self._config),
    "Log": LogPage(self._config),
    "About": AboutPage(self._config),
}
```

**Target**:
```python
self._pages: Dict[str, QWidget] = {
    "Dashboard": DashboardPage(self._config),
    "Connection": ConnectionPage(self._config),
    "Converters": ConvertersPageV2(self._config, main_window=self),
    "Setup": SetupPage(self._config),
    "Serial Numbers": SerialNumberHandlerPage(self._config),
    "Log": LogPage(self._config),
    "About": AboutPage(self._config),
}
```

### 1.3 Add File Menu

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Location**: After `_setup_window()`, add new method `_setup_menu_bar()`

**Implementation**:
```python
def _setup_menu_bar(self) -> None:
    """Setup menu bar with File menu"""
    menu_bar = self.menuBar()
    
    # File menu
    file_menu = menu_bar.addMenu("&File")
    
    # Disconnect action
    disconnect_action = file_menu.addAction("&Disconnect")
    disconnect_action.setStatusTip("Disconnect from WATS server")
    disconnect_action.triggered.connect(self._on_disconnect)
    
    # Minimize to tray action
    minimize_action = file_menu.addAction("&Minimize to Tray")
    minimize_action.setStatusTip("Minimize window to system tray")
    minimize_action.triggered.connect(self._on_minimize_to_tray)
    
    file_menu.addSeparator()
    
    # Exit action
    exit_action = file_menu.addAction("E&xit")
    exit_action.setShortcut("Ctrl+Q")
    exit_action.setStatusTip("Exit application")
    exit_action.triggered.connect(self.close)
```

**Call in** `_setup_ui()` (line 122):
```python
def _setup_ui(self) -> None:
    """Setup main UI layout"""
    # Add menu bar first
    self._setup_menu_bar()
    
    # Central widget
    central_widget = QWidget()
    # ... rest of existing code
```

### 1.4 Implement Menu Actions

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Add methods**:
```python
def _on_disconnect(self) -> None:
    """Disconnect from server (File → Disconnect)"""
    from PySide6.QtWidgets import QMessageBox
    
    reply = QMessageBox.question(
        self,
        "Disconnect",
        "Disconnect from WATS server?\n\n"
        "This will stop the client service and clear the connection.",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    
    if reply == QMessageBox.StandardButton.Yes:
        try:
            # Stop service if running
            # TODO: Implement service stop logic
            
            # Update status
            self.statusBar().showMessage("Disconnected")
            logger.info("Disconnected from server")
            
        except Exception as e:
            logger.exception(f"Failed to disconnect: {e}")
            QMessageBox.warning(self, "Disconnect Error", f"Failed to disconnect:\n{e}")

def _on_minimize_to_tray(self) -> None:
    """Minimize to system tray (File → Minimize to Tray)"""
    # Check if system tray is available
    if hasattr(self, '_system_tray') and self._system_tray:
        self.hide()
        self._system_tray.showMessage(
            "pyWATS Configurator",
            "Application minimized to tray",
            2000  # 2 seconds
        )
        logger.debug("Minimized to system tray")
    else:
        # Fallback to regular minimize
        self.showMinimized()
        logger.debug("System tray not available, minimized to taskbar")
```

### 1.5 Verify System Tray Integration

**File**: `src/pywats_ui/framework/system_tray.py`

**Check**: Verify system tray implementation exists and is integrated

**If missing**: Basic implementation needed (defer to separate task if complex)

---

## Phase 2: Scaling Fixes (2 hours)

### 2.1 Main Window Sizing

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Current** (line 120-121):
```python
self.setMinimumSize(900, 650)
self.resize(1100, 800)
```

**Target**:
```python
self.setMinimumSize(800, 600)  # Industry standard minimum
self.resize(1000, 700)          # Comfortable default
```

### 2.2 Sidebar Width

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Current** (line 148):
```python
sidebar.setFixedWidth(200)
```

**Target**:
```python
sidebar.setMinimumWidth(180)
sidebar.setMaximumWidth(220)  # Allow slight resize
```

### 2.3 Button Width Fixes

**Files**: All page files

**Pattern to find**:
```python
button.setFixedWidth(XXX)
```

**Replace with**:
```python
button.setMinimumWidth(XXX)
```

**Affected files**:
- `connection.py` (line 74, 100, 117)
- `dashboard.py`
- Others (audit needed)

### 2.4 Test at Minimum Size

**Manual Test**:
1. Launch Configurator
2. Resize to 800x600
3. Check each page for:
   - Text readability
   - Button accessibility
   - Layout integrity
   - No horizontal/vertical scrolling needed for core content

---

## Phase 3: Dashboard Enhancements (3 hours)

### 3.1 Add Station Information Section

**File**: `src/pywats_ui/apps/configurator/pages/dashboard.py`

**Location**: After service status section, before statistics cards

**Implementation**:
```python
# === Station Information Section ===
station_group = QGroupBox("Station Information")
station_layout = QVBoxLayout(station_group)

# Info display (read-only)
info_form = QFormLayout()
info_form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)

self._client_name_label = QLabel("--")
self._client_name_label.setStyleSheet("color: #dcdcaa; font-weight: bold;")
info_form.addRow("Client Name:", self._client_name_label)

self._station_name_label = QLabel("--")
self._station_name_label.setStyleSheet("color: #dcdcaa; font-weight: bold;")
info_form.addRow("Station Name:", self._station_name_label)

self._station_location_label = QLabel("--")
self._station_location_label.setStyleSheet("color: #dcdcaa;")
info_form.addRow("Location:", self._station_location_label)

self._station_purpose_label = QLabel("--")
self._station_purpose_label.setStyleSheet("color: #dcdcaa;")
info_form.addRow("Purpose:", self._station_purpose_label)

station_layout.addLayout(info_form)

# GPS toggle
self._gps_enabled_cb = QCheckBox("Allow GPS location services")
self._gps_enabled_cb.setToolTip(
    "When enabled, the client includes geographical coordinates with test reports"
)
self._gps_enabled_cb.stateChanged.connect(self._on_gps_changed)
station_layout.addWidget(self._gps_enabled_cb)

# Edit button
edit_layout = QHBoxLayout()
self._edit_station_btn = QPushButton("Edit Station Settings")
self._edit_station_btn.setToolTip("Open Setup page to edit station information")
self._edit_station_btn.clicked.connect(self._on_edit_station)
edit_layout.addWidget(self._edit_station_btn)
edit_layout.addStretch()
station_layout.addLayout(edit_layout)

self._layout.addWidget(station_group)
```

### 3.2 Load Station Data

**File**: `src/pywats_ui/apps/configurator/pages/dashboard.py`

**Add to `load_config()` method**:
```python
def load_config(self) -> None:
    """Load configuration and station data"""
    try:
        # Existing code...
        
        # Load station information
        self._client_name_label.setText(
            self._config.get("client_name", "Not configured")
        )
        self._station_name_label.setText(
            self._config.get("station_name", "Not configured")
        )
        self._station_location_label.setText(
            self._config.get("location", "Not configured")
        )
        self._station_purpose_label.setText(
            self._config.get("purpose", "Not configured")
        )
        self._gps_enabled_cb.setChecked(
            self._config.get("location_services_enabled", False)
        )
        
        logger.debug("Station information loaded")
        
    except Exception as e:
        self.handle_error(e, "loading dashboard configuration")
```

### 3.3 Add Event Handlers

**File**: `src/pywats_ui/apps/configurator/pages/dashboard.py`

**Add methods**:
```python
def _on_gps_changed(self, state: int) -> None:
    """Handle GPS checkbox change"""
    try:
        enabled = state == Qt.CheckState.Checked.value
        self._config["location_services_enabled"] = enabled
        self._config.save()
        logger.info(f"GPS location services: {enabled}")
    except Exception as e:
        self.handle_error(e, "saving GPS setting")

def _on_edit_station(self) -> None:
    """Navigate to Setup page for editing station info"""
    # Need reference to main window navigation
    # Emit signal or use event bus
    if hasattr(self.parent(), 'navigate_to_page'):
        self.parent().navigate_to_page("Setup")
    else:
        # Fallback: Show info message
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Edit Station Settings",
            "Navigate to the 'Setup' page to edit station information."
        )
```

### 3.4 Add Navigation Helper to MainWindow

**File**: `src/pywats_ui/apps/configurator/main_window.py`

**Add method**:
```python
def navigate_to_page(self, page_name: str) -> None:
    """Navigate to specific page by name"""
    for i in range(self._nav_list.count()):
        item = self._nav_list.item(i)
        if item.data(Qt.ItemDataRole.UserRole) == page_name:
            self._nav_list.setCurrentRow(i)
            logger.debug(f"Navigated to page: {page_name}")
            return
    
    logger.warning(f"Page not found: {page_name}")
```

**Update Dashboard page creation** (line 229):
```python
"Dashboard": DashboardPage(self._config, parent=self),
```

### 3.5 Remove Location Page

**File**: `src/pywats_ui/apps/configurator/pages/__init__.py`

**Remove import**:
```python
from .location import LocationPage  # ❌ REMOVE
```

**Note**: Keep location.py file for now (may have code to reference)

---

## Phase 4: Connection Page Simplification (2 hours)

### 4.1 Move API Settings to Advanced

**File**: `src/pywats_ui/apps/configurator/pages/connection.py`

**Current Advanced options** (line 175-200):
- API Token (already there ✅)
- Sync interval (already there ✅)

**Check API Settings page** for additional fields to migrate:
```bash
# Review api_settings.py for fields
```

**If needed**: Add to Advanced group

### 4.2 Move Proxy Settings to Advanced

**File**: `src/pywats_ui/apps/configurator/pages/connection.py`

**Review** `proxy_settings.py` for fields:
- Proxy enabled checkbox
- Proxy URL
- Proxy authentication

**Add to Advanced group** (after sync interval):
```python
# Proxy settings
proxy_enabled_layout = QHBoxLayout()
self._proxy_enabled_cb = QCheckBox("Use proxy server")
self._proxy_enabled_cb.stateChanged.connect(self._on_proxy_enabled_changed)
proxy_enabled_layout.addWidget(self._proxy_enabled_cb)
advanced_layout.addLayout(proxy_enabled_layout)

proxy_url_layout = QHBoxLayout()
proxy_url_layout.addWidget(QLabel("Proxy URL:"))
self._proxy_url_edit = QLineEdit()
self._proxy_url_edit.setPlaceholderText("http://proxy.company.com:8080")
self._proxy_url_edit.textChanged.connect(self._emit_changed)
proxy_url_layout.addWidget(self._proxy_url_edit, 1)
advanced_layout.addLayout(proxy_url_layout)

# Enable/disable proxy URL based on checkbox
self._on_proxy_enabled_changed(self._proxy_enabled_cb.checkState())
```

### 4.3 Update Save/Load Config

**File**: `src/pywats_ui/apps/configurator/pages/connection.py`

**Add to `save_config()`**:
```python
# Proxy settings
self._config["proxy_enabled"] = self._proxy_enabled_cb.isChecked()
self._config["proxy_url"] = self._proxy_url_edit.text().strip()
```

**Add to `load_config()`**:
```python
# Proxy settings
self._proxy_enabled_cb.setChecked(self._config.get("proxy_enabled", False))
self._proxy_url_edit.setText(self._config.get("proxy_url", ""))
```

### 4.4 Remove Standalone Pages

**Files to keep** (for reference/migration):
- `api_settings.py` (review for missing fields)
- `proxy_settings.py` (review for missing fields)

**Remove from imports** in `__init__.py`:
```python
from .api_settings import APISettingsPage     # ❌ REMOVE from export
from .proxy_settings import ProxySettingsPage # ❌ REMOVE from export
```

---

## Phase 5: Testing & Polish (1 hour)

### 5.1 Manual Testing Checklist

**Navigation**:
- [ ] Launch Configurator → Dashboard is default page
- [ ] Click each tab → Page loads correctly
- [ ] No errors in console/log

**File Menu**:
- [ ] File → Disconnect → Confirmation dialog appears
- [ ] File → Disconnect → Service stops (if running)
- [ ] File → Minimize to Tray → Window hides (or minimizes if no tray)
- [ ] File → Exit → Application closes cleanly

**Dashboard**:
- [ ] Station information displays correctly
- [ ] GPS checkbox toggles and saves
- [ ] "Edit Station Settings" button navigates to Setup page
- [ ] Service status updates
- [ ] Converter health table populates

**Scaling**:
- [ ] Resize to 800x600 → All content readable
- [ ] Resize to 1920x1080 → No awkward stretching
- [ ] All pages tested at minimum size
- [ ] No layout breaks during dynamic resize

**Connection Page**:
- [ ] Service address editable
- [ ] Advanced options collapsed by default
- [ ] API Token, Sync Interval, Proxy settings in Advanced
- [ ] Settings save and load correctly

**Setup Page**:
- [ ] Station fields editable
- [ ] Changes save correctly
- [ ] Navigate to Dashboard → See updated values

### 5.2 Regression Testing

**Run existing tests**:
```bash
pytest tests/client/ -v
```

**Expected**: No breaking changes to backend logic

### 5.3 Documentation Updates

**Files to update**:
1. `README.md` - Update screenshots if GUI changed
2. `docs/guides/getting-started.md` - Update tab references
3. `CHANGELOG.md` - Add entry:
   ```markdown
   ### Changed
   - **GUI Cleanup**: Simplified Configurator navigation to 7 essential tabs
     - Removed: Software, Location, Proxy, API Settings pages
     - Integrated: GPS toggle, proxy, and API settings into Dashboard/Connection
     - Added: File menu with Disconnect, Minimize to Tray, Exit
     - Fixed: Scaling issues (minimum size now 800x600)
     - Improved: Dashboard now shows station information inline
   ```

### 5.4 Polish Items

**Status messages**:
- Update status bar messages to be clear
- Add tooltips where helpful

**Keyboard shortcuts**:
- Ctrl+Q → Exit (already in File menu)
- Consider: Ctrl+D → Disconnect, Ctrl+1-7 → Navigate tabs

**Error handling**:
- Verify all error dialogs are user-friendly
- Check log output is appropriate

---

## Implementation Order

1. **Phase 1** - Quick wins (tab removal, File menu)
2. **Phase 2** - Scaling fixes (test frequently)
3. **Phase 3** - Dashboard enhancements (station info)
4. **Phase 4** - Connection page simplification
5. **Phase 5** - Testing and polish

**Commit strategy**: One commit per phase for easy rollback

---

## Files Modified (Summary)

| File | Changes | Lines |
|------|---------|-------|
| `main_window.py` | Tab management, File menu, navigation helper | ~80 |
| `dashboard.py` | Station info section, GPS toggle, event handlers | ~120 |
| `connection.py` | Proxy/API settings integration | ~50 |
| `__init__.py` (pages) | Remove page exports | ~5 |
| `CHANGELOG.md` | Release notes | ~10 |
| Documentation | Tab reference updates | ~20 |

**Total**: ~285 lines modified/added

---

## Rollback Plan

**If issues arise**:
1. Each phase committed separately → Revert specific commits
2. Keep removed page files → Easy to restore if needed
3. Document breaking changes → Know what to fix

**Git strategy**:
```bash
# Phase 1
git add -u && git commit -m "GUI: Remove unnecessary tabs, add File menu"

# Phase 2
git add -u && git commit -m "GUI: Fix scaling issues (800x600 minimum)"

# Phase 3
git add -u && git commit -m "GUI: Add station info to Dashboard"

# Phase 4
git add -u && git commit -m "GUI: Integrate settings into Connection page"

# Phase 5
git add -u && git commit -m "GUI: Polish and documentation updates"
```

---

**Status**: Implementation plan complete, ready to execute.
