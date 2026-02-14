# Task Checklist: GUI Cleanup for Beta

**Created:** February 14, 2026, 16:00  
**Last Updated:** February 14, 2026, 16:00

---

## Legend

- ✅ Completed
- 🚧 In Progress
- ⏸️ Blocked/Waiting
- ✗ Not Started
- ❌ Cancelled/Skipped

---

## Phase 1: Tab Management & File Menu

### 1.1 Update Navigation Items
- ✗ Update nav_items list to 7 tabs
- ✗ Reorder tabs (Connection before Converters)
- ✗ Remove: Software, Location, Proxy, API Settings

### 1.2 Update Pages Dictionary
- ✗ Remove page instances for removed tabs
- ✗ Match order with nav_items

### 1.3 Add File Menu
- ✗ Create _setup_menu_bar() method
- ✗ Add File menu with 4 items
- ✗ Add keyboard shortcuts
- ✗ Call from _setup_ui()

### 1.4 Implement Menu Actions
- ✗ _on_disconnect() method
- ✗ _on_minimize_to_tray() method
- ✗ Connect actions to methods

### 1.5 Verify System Tray
- ✗ Check system_tray.py integration
- ✗ Test minimize to tray functionality

---

## Phase 2: Scaling Fixes

### 2.1 Main Window Sizing
- ✗ Change minimum size to 800x600
- ✗ Change default size to 1000x700

### 2.2 Sidebar Width
- ✗ Change from fixed to min/max width
- ✗ Test sidebar resize behavior

### 2.3 Button Width Fixes
- ✗ Audit all pages for setFixedWidth()
- ✗ Replace with setMinimumWidth()
- ✗ Test button layout at various sizes

### 2.4 Test at Minimum Size
- ✗ Test Dashboard at 800x600
- ✗ Test Connection at 800x600
- ✗ Test Converters at 800x600
- ✗ Test Setup at 800x600
- ✗ Test Serial Numbers at 800x600
- ✗ Test Log at 800x600
- ✗ Test About at 800x600

---

## Phase 3: Dashboard Enhancements

### 3.1 Add Station Information Section
- ✗ Create station_group QGroupBox
- ✗ Add read-only labels for client/station info
- ✗ Add GPS checkbox
- ✗ Add "Edit Station Settings" button
- ✗ Position after service status section

### 3.2 Load Station Data
- ✗ Update load_config() method
- ✗ Load client_name, station_name, location, purpose
- ✗ Load location_services_enabled
- ✗ Update labels with config values

### 3.3 Add Event Handlers
- ✗ _on_gps_changed() method
- ✗ _on_edit_station() method
- ✗ Connect signals to handlers

### 3.4 Add Navigation Helper
- ✗ Add navigate_to_page() to MainWindow
- ✗ Update Dashboard parent reference
- ✗ Test navigation from Dashboard to Setup

### 3.5 Remove Location Page
- ✗ Remove LocationPage from __init__.py exports
- ✗ Keep file for reference

---

## Phase 4: Connection Page Simplification

### 4.1 Move API Settings to Advanced
- ✗ Review api_settings.py for fields
- ✗ Migrate missing fields to Connection Advanced
- ✗ Test field functionality

### 4.2 Move Proxy Settings to Advanced
- ✗ Review proxy_settings.py for fields
- ✗ Add proxy checkbox to Advanced
- ✗ Add proxy URL field to Advanced
- ✗ Add enable/disable logic

### 4.3 Update Save/Load Config
- ✗ Add proxy fields to save_config()
- ✗ Add proxy fields to load_config()
- ✗ Test config persistence

### 4.4 Remove Standalone Pages
- ✗ Remove APISettingsPage from exports
- ✗ Remove ProxySettingsPage from exports
- ✗ Keep files for reference

---

## Phase 5: Testing & Polish

### 5.1 Manual Testing - Navigation
- ✗ Launch → Dashboard is default
- ✗ Click each tab → Loads correctly
- ✗ Check console for errors

### 5.2 Manual Testing - File Menu
- ✗ File → Disconnect works
- ✗ File → Minimize to Tray works
- ✗ File → Exit works
- ✗ Keyboard shortcuts work

### 5.3 Manual Testing - Dashboard
- ✗ Station info displays
- ✗ GPS toggle saves
- ✗ Edit button navigates to Setup
- ✗ Service status updates

### 5.4 Manual Testing - Scaling
- ✗ Test at 800x600
- ✗ Test at 1920x1080
- ✗ Test dynamic resize
- ✗ All pages readable

### 5.5 Manual Testing - Connection
- ✗ Advanced options collapsed
- ✗ All settings in Advanced work
- ✗ Settings save/load correctly

### 5.6 Regression Testing
- ✗ Run pytest tests/client/
- ✗ No breaking changes

### 5.7 Documentation Updates
- ✗ Update CHANGELOG.md
- ✗ Update getting-started guide
- ✗ Update README if needed

### 5.8 Polish
- ✗ Review status messages
- ✗ Add missing tooltips
- ✗ Check error handling
- ✗ Final code review

---

**Total Tasks**: 70
**Estimated Time**: 8-10 hours
