# GUI Cleanup and Testing - Implementation Plan

**Project:** GUI Cleanup and Testing  
**Phase:** Implementation Planning  
**Date:** 2026-02-02

---

## Table of Contents

1. [Sprint Overview](#sprint-overview)
2. [Sprint 1: Acceptance Testing](#sprint-1-acceptance-testing)
3. [Sprint 2: Settings Dialog Updates](#sprint-2-settings-dialog-updates)
4. [Sprint 3: Converter GUI & Lifecycle](#sprint-3-converter-gui--lifecycle)
5. [Sprint 4: UI Polish & Final Testing](#sprint-4-ui-polish--final-testing)

---

## Sprint Overview

### Sprint Structure

**Total Duration:** 7 days (Feb 2-9, 2026)

| Sprint | Duration | Focus | Deliverables |
|--------|----------|-------|--------------|
| Sprint 1 | 2 days | Acceptance Testing & Documentation | Test report, issues list |
| Sprint 2 | 2 days | Settings Dialog (Cache, Metrics) | Performance & Observability panels |
| Sprint 3 | 1 day | Converter Priority & Lifecycle | Priority UI, clean shutdown |
| Sprint 4 | 2 days | UI Polish & Final Testing | Visual consistency, bug fixes |

---

## Sprint 1: Acceptance Testing (Days 1-2)

**Goal:** Test all existing GUI pages and document current state

### Phase 1.1: Test Infrastructure Setup (2 hours)

**Tasks:**
1. Create acceptance test checklist template
2. Setup test environment
3. Prepare test data (sample configs, test server)
4. Document test procedure

**Deliverables:**
- `testing/acceptance_test_template.md`
- Test environment ready

### Phase 1.2: Dashboard Testing (2 hours)

**Test Cases:**
1. Connection status display
   - Not connected state
   - Connecting state
   - Connected state (green indicator)
   - Error state (red indicator)
2. Quick stats widgets
   - Queue size display
   - Active converters count
   - Recent reports count
3. Recent activity log
   - Log scrolling
   - Timestamp formatting
   - Log levels (INFO, WARNING, ERROR)
4. Quick actions
   - Connect button functionality
   - Disconnect button functionality
   - Settings button functionality

**Deliverables:**
- Dashboard test report
- Screenshot collection
- Bug list

### Phase 1.3: Reports Page Testing (2 hours)

**Test Cases:**
1. Report list display
   - Column headers
   - Row data formatting
   - Sorting by column
2. Filtering and search
   - Filter by status
   - Search by serial number
   - Date range filter
3. Report details view
   - Click to view details
   - Details panel layout
   - Attachment display
4. Actions
   - Submit report
   - Retry failed report
   - Delete report
   - Export report

**Deliverables:**
- Reports page test report
- Bug list

### Phase 1.4: Converters Page Testing (2 hours)

**Test Cases:**
1. Converter list display
   - Name, type, status columns
   - Enable/disable toggle
   - Priority badge (if exists)
2. Add/Edit/Delete
   - Add new converter button
   - Edit converter button
   - Delete confirmation dialog
3. Converter status
   - Enabled/disabled state
   - Running/stopped indicator
   - Error state display
4. Converter controls
   - Start/stop individual converter
   - View converter logs
   - Refresh converter list

**Deliverables:**
- Converters page test report
- Current converter dialog structure
- Bug list

### Phase 1.5: Settings Dialog Testing (4 hours)

**Test Cases:**
1. Test all existing panels:
   - API General Settings
   - Product Domain
   - Report Domain
   - Production Domain
   - Process Domain
   - Software Domain
   - Asset Domain
   - RootCause Domain
2. Save/Cancel functionality
3. Validation errors
4. Panel switching
5. Data persistence

**Deliverables:**
- Settings dialog test report
- Missing features list
- Bug list

### Phase 1.6: Other Pages Testing (2 hours)

**Test Cases:**
1. Serial Number Handler
   - Mode selection
   - COM port detection
   - Format validation
2. Software Distribution
   - Software list display
   - Download functionality
3. Location Services
   - Location detection
   - Manual entry
4. Proxy Settings
   - Proxy mode selection
   - Authentication

**Deliverables:**
- Complete test report
- Consolidated bug list

### Phase 1.7: System Tray Testing (2 hours)

**Test Cases:**
1. Minimize to tray
2. Restore from tray
3. Tray menu
4. Exit from tray
5. Tray icon state
6. Platform testing (Windows)

**Deliverables:**
- System tray test report
- Platform-specific issues

**Sprint 1 Total:** ~16 hours (2 days)

---

## Sprint 2: Settings Dialog Updates (Days 3-4)

**Goal:** Add Performance and Observability panels to settings dialog

### Phase 2.1: Design & Planning (2 hours)

**Tasks:**
1. Review CONFIG_SETTINGS_REFERENCE.md
2. Design Performance panel layout
3. Design Observability panel layout
4. Create mockups/wireframes
5. Plan widget types (sliders, spinners, checkboxes)

**Deliverables:**
- Panel layout designs
- Widget specification

### Phase 2.2: Performance Panel Implementation (4 hours)

**Files to Modify:**
- `src/pywats_client/gui/settings_dialog.py`

**Components to Create:**

#### PerformancePanelWidget
```python
class PerformancePanelWidget(SettingsPanel):
    """Performance settings panel with cache and queue configuration"""
    
    def __init__(self, config: ClientConfig):
        # HTTP Cache Section
        self.enable_cache_cb = QCheckBox("Enable HTTP response caching")
        self.cache_ttl_slider = QSlider(Qt.Horizontal)  # 60-7200
        self.cache_ttl_label = QLabel()
        self.cache_size_slider = QSlider(Qt.Horizontal)  # 100-5000
        self.cache_size_label = QLabel()
        
        # Preset buttons
        self.ttl_preset_1min = QPushButton("1 min")
        self.ttl_preset_5min = QPushButton("5 min")
        self.ttl_preset_10min = QPushButton("10 min")
        self.ttl_preset_1hour = QPushButton("1 hour")
        
        # Cache statistics (read-only)
        self.cache_stats_group = QGroupBox("Cache Statistics")
        self.cache_hits_label = QLabel()
        self.cache_misses_label = QLabel()
        self.cache_hit_rate_label = QLabel()
        self.cache_current_size_label = QLabel()
        
        # Clear cache button
        self.clear_cache_btn = QPushButton("Clear Cache")
        
        # Queue Settings Section
        self.max_queue_size_spinner = QSpinBox()  # 0-100000
        self.max_concurrent_uploads_spinner = QSpinBox()  # 1-20
```

**Implementation Steps:**
1. Create PerformancePanelWidget class
2. Add cache enable/disable checkbox with signal
3. Add TTL slider with value label
4. Add preset buttons (1min, 5min, 10min, 1hour)
5. Add cache size slider with value label
6. Add cache statistics display (refresh timer)
7. Add clear cache button
8. Add queue size spinner
9. Add concurrent uploads spinner
10. Connect signals to config
11. Implement load_from_config()
12. Implement save_to_config()
13. Add to settings dialog tab widget

**Deliverables:**
- Performance panel fully functional
- Cache statistics refreshing (if connected)
- Settings persistence working

### Phase 2.3: Observability Panel Implementation (4 hours)

**Files to Modify:**
- `src/pywats_client/gui/settings_dialog.py`

**Components to Create:**

#### ObservabilityPanelWidget
```python
class ObservabilityPanelWidget(SettingsPanel):
    """Observability settings panel with metrics and health endpoints"""
    
    def __init__(self, config: ClientConfig):
        # Metrics Section
        self.enable_metrics_cb = QCheckBox("Enable Prometheus metrics")
        self.metrics_port_spinner = QSpinBox()  # 1024-65535
        self.metrics_endpoint_label = QLabel()  # Read-only preview
        self.open_metrics_btn = QPushButton("Open in Browser")
        
        # Health Endpoints Section
        self.health_check_interval_spinner = QSpinBox()  # 10-300
        self.health_endpoints_group = QGroupBox("Health Endpoints")
        self.health_endpoint_label = QLabel()
        self.ready_endpoint_label = QLabel()
        self.live_endpoint_label = QLabel()
        self.metrics_endpoint_label2 = QLabel()
```

**Implementation Steps:**
1. Create ObservabilityPanelWidget class
2. Add metrics enable/disable checkbox
3. Add metrics port spinner (1024-65535)
4. Add endpoint preview (auto-update on port change)
5. Add "Open in Browser" button
6. Add health check interval spinner
7. Add health endpoint URLs (read-only)
8. Connect signals to config
9. Implement load_from_config()
10. Implement save_to_config()
11. Add to settings dialog tab widget

**Deliverables:**
- Observability panel fully functional
- Metrics endpoint preview working
- Settings persistence working

### Phase 2.4: Integration & Testing (4 hours)

**Tasks:**
1. Add Performance panel to settings dialog
2. Add Observability panel to settings dialog
3. Update settings dialog tab order
4. Test save/load functionality
5. Test validation
6. Test with service running/stopped
7. Test cache statistics refresh
8. Test metrics endpoint opening

**Test Cases:**
- Toggle cache on/off (verify fields enable/disable)
- Adjust TTL slider (verify label updates)
- Click preset buttons (verify TTL changes)
- Adjust cache size slider
- View cache statistics (requires running service)
- Click clear cache button
- Toggle metrics on/off
- Change metrics port (verify endpoint preview updates)
- Click "Open in Browser" (requires running service)
- Save settings and reload
- Validate port range (1024-65535)
- Validate TTL range (60-7200)
- Validate cache size range (100-5000)

**Deliverables:**
- Settings dialog fully updated
- All v0.3.0 settings accessible
- Test report

**Sprint 2 Total:** ~14 hours (2 days)

---

## Sprint 3: Converter GUI & Lifecycle (Day 5)

**Goal:** Add priority to converter GUI and fix lifecycle issues

### Phase 3.1: Converter Dialog Updates (3 hours)

**Files to Modify:**
- `src/pywats_client/gui/converter_dialog.py`

**Components to Add:**

#### Priority Section
```python
class ConverterDialog(QDialog):
    def __init__(self, converter: ConverterConfig = None):
        # ... existing fields ...
        
        # Priority Section (NEW)
        self.priority_group = QGroupBox("Processing Priority")
        self.priority_slider = QSlider(Qt.Horizontal)
        self.priority_slider.setRange(1, 10)
        self.priority_slider.setTickPosition(QSlider.TicksBelow)
        self.priority_slider.setTickInterval(1)
        
        self.priority_value_label = QLabel("5")
        
        # Priority description
        self.priority_desc = QLabel(
            "1-2: Real-time, critical\n"
            "3-5: Normal (default=5)\n"
            "6-8: Batch processing\n"
            "9-10: Background tasks"
        )
```

**Implementation Steps:**
1. Add priority group box
2. Add priority slider (1-10)
3. Add priority value label
4. Add priority description label
5. Connect slider to value label
6. Add color-coding (1-2: red, 3-5: green, 6-10: gray)
7. Load priority from converter config
8. Save priority to converter config
9. Set default priority=5 for new converters

**Deliverables:**
- Converter dialog with priority slider
- Priority persisting correctly

### Phase 3.2: Converter List Updates (2 hours)

**Files to Modify:**
- `src/pywats_client/gui/converters_widget.py`

**Updates Needed:**
1. Add priority column to converter table
2. Show priority badge: `[P1]`, `[P5]`, etc.
3. Color-code priority badges
4. Add sort by priority option
5. Update converter model to include priority

**Deliverables:**
- Converter list showing priority
- Sort by priority working

### Phase 3.3: Lifecycle Fixes (3 hours)

**Files to Modify:**
- `src/pywats_client/gui/main_window.py`
- `src/pywats_client/service/async_client_service.py`

**Issues to Fix:**
1. **Clean Shutdown:**
   - Stop AsyncClientService properly
   - Wait for background tasks (max 5 seconds)
   - Close service connection
   - Save window state
   - Exit cleanly (no orphaned processes)

2. **System Tray:**
   - Fix minimize to tray
   - Fix restore from tray
   - Fix exit from tray menu
   - Update tray icon tooltip (connection status)

**Implementation Steps:**
1. Add shutdown handler in MainWindow
2. Implement graceful service shutdown
3. Add shutdown timeout (5 seconds)
4. Save config before exit
5. Save window geometry
6. Fix system tray minimize/restore
7. Update tray tooltip on connection change
8. Test all exit paths (X button, File→Exit, tray menu)

**Deliverables:**
- Clean shutdown (no orphaned processes)
- System tray working correctly
- Window state persisting

**Sprint 3 Total:** ~8 hours (1 day)

---

## Sprint 4: UI Polish & Final Testing (Days 6-7)

**Goal:** Visual consistency, bug fixes, and final validation

### Phase 4.1: Icon Audit & Updates (3 hours)

**Tasks:**
1. Audit all icons in application
2. Identify missing icons
3. Add system tray icon (multi-resolution)
4. Add menu icons (File, Edit, View, Tools, Help)
5. Add toolbar icons (Connect, Disconnect, Settings)
6. Ensure consistent icon style

**Deliverables:**
- Complete icon set
- Icons in multiple resolutions
- Icon resources integrated

### Phase 4.2: Menu Updates (2 hours)

**Files to Modify:**
- `src/pywats_client/gui/main_window.py`

**Menus to Add/Update:**

1. **File Menu**
   - Connect (Ctrl+C)
   - Disconnect (Ctrl+D)
   - ---
   - Settings (Ctrl+,)
   - ---
   - Exit (Ctrl+Q)

2. **Edit Menu**
   - Preferences (Ctrl+P)

3. **View Menu**
   - Show Dashboard
   - Show Reports
   - Show Converters
   - ---
   - Refresh (F5)

4. **Tools Menu**
   - Clear Cache
   - Open Metrics (Ctrl+M)
   - Test Connection
   - ---
   - View Logs

5. **Help Menu**
   - Documentation (F1)
   - About pyWATS
   - Check for Updates

**Deliverables:**
- Complete menu structure
- Keyboard shortcuts working
- Menu actions functional

### Phase 4.3: Layout & Spacing Fixes (3 hours)

**Tasks:**
1. Audit all pages for spacing issues
2. Fix alignment issues
3. Ensure consistent margins (10px standard)
4. Fix responsive resizing
5. Test on different screen sizes
6. Fix tab order for keyboard navigation

**Deliverables:**
- Consistent spacing throughout
- Proper widget alignment
- Responsive layouts

### Phase 4.4: Bug Fixes (4 hours)

**Process:**
1. Review all test reports
2. Prioritize bugs (critical, high, medium, low)
3. Fix critical bugs
4. Fix high priority bugs
5. Fix medium priority bugs (time permitting)
6. Document low priority bugs (future work)

**Deliverables:**
- All critical bugs fixed
- Most high priority bugs fixed
- Bug fix changelog

### Phase 4.5: Final Testing (4 hours)

**Test Plan:**
1. Run full acceptance test suite
2. Test all new features (cache, metrics, priority)
3. Test all lifecycle scenarios (startup, shutdown, tray)
4. Test on Windows (primary platform)
5. Test with real service connection
6. Performance test (check for UI lag)

**Test Scenarios:**
1. Fresh install
2. Upgrade from previous version (config migration)
3. Start with auto-connect
4. Start minimized
5. Long-running session (8+ hours)
6. Rapid connect/disconnect cycles
7. Settings changes while connected
8. Converter add/edit/delete
9. System tray operations
10. Forced shutdown (Ctrl+C)

**Deliverables:**
- Final test report
- Regression test results
- Performance metrics

### Phase 4.6: Documentation Updates (2 hours)

**Documents to Update:**
1. User guide (new settings panels)
2. Configuration reference (already done)
3. Screenshots (settings dialog, converter dialog)
4. Changelog entry

**Deliverables:**
- Updated user documentation
- Screenshot gallery
- Changelog entry

**Sprint 4 Total:** ~18 hours (2 days)

---

## Implementation Guidelines

### Code Style

**Python/Qt:**
```python
# Use descriptive widget names
self.cache_enabled_checkbox = QCheckBox("Enable cache")

# Connect signals explicitly
self.cache_enabled_checkbox.stateChanged.connect(self._on_cache_enabled_changed)

# Use layouts for flexible design
layout = QVBoxLayout()
layout.addWidget(self.cache_group)
layout.addStretch()  # Push to top

# Add tooltips for clarity
self.priority_slider.setToolTip("Processing priority (1=highest, 10=lowest)")
```

**Signal/Slot Naming:**
- Use `_on_widget_action` pattern
- Example: `_on_cache_enabled_changed`, `_on_ttl_slider_value_changed`

**Config Loading/Saving:**
```python
def load_from_config(self, config: ClientConfig):
    """Load settings from config"""
    self.enable_cache_cb.setChecked(config.enable_cache)
    self.cache_ttl_slider.setValue(int(config.cache_ttl_seconds))
    self.cache_size_slider.setValue(config.cache_max_size)

def save_to_config(self, config: ClientConfig):
    """Save settings to config"""
    config.enable_cache = self.enable_cache_cb.isChecked()
    config.cache_ttl_seconds = float(self.cache_ttl_slider.value())
    config.cache_max_size = self.cache_size_slider.value()
```

### Testing Checklist

**Before Committing:**
- [ ] Code runs without errors
- [ ] Settings save/load correctly
- [ ] UI looks correct (no overlapping widgets)
- [ ] Tooltips are accurate
- [ ] Validation works
- [ ] No console warnings/errors
- [ ] Clean shutdown works

**Before Merging:**
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Screenshots current
- [ ] Changelog updated
- [ ] No known critical bugs

---

## Success Criteria

### Sprint 1 Success
- ✅ All pages tested and documented
- ✅ Complete bug list created
- ✅ Current state documented

### Sprint 2 Success
- ✅ Performance panel functional
- ✅ Observability panel functional
- ✅ All v0.3.0 settings accessible
- ✅ Settings persist correctly

### Sprint 3 Success
- ✅ Converter priority UI working
- ✅ Priority persists correctly
- ✅ Clean shutdown (no orphaned processes)
- ✅ System tray working

### Sprint 4 Success
- ✅ All icons present and consistent
- ✅ Complete menu structure
- ✅ Consistent layouts and spacing
- ✅ All critical bugs fixed
- ✅ Documentation updated

---

## Deliverables Summary

### Code Deliverables
1. Updated `settings_dialog.py` (Performance + Observability panels)
2. Updated `converter_dialog.py` (Priority slider)
3. Updated `converters_widget.py` (Priority column/badges)
4. Updated `main_window.py` (Lifecycle fixes, menus)
5. Updated `system_tray.py` (Fixes)
6. New icons in `gui/resources/icons/`

### Documentation Deliverables
1. Acceptance test report (`testing/acceptance_tests.md`)
2. Settings dialog checklist (`testing/settings_dialog_checklist.md`)
3. Converter GUI tests (`testing/converter_gui_tests.md`)
4. Bug list and fixes changelog
5. Updated user guide (screenshots + new features)
6. CHANGELOG entry

### Test Deliverables
1. Acceptance test results
2. Regression test results
3. Performance test results
4. Platform compatibility report

---

**Plan Complete:** 2026-02-02  
**Next Phase:** Implementation (Sprint 1)
