# GUI Cleanup and Testing - Task List

**Project:** GUI Cleanup and Testing  
**Last Updated:** 2026-02-02

---

## Legend
- ✅ Complete
- 🚧 In Progress
- ⏸️ Blocked
- ✗ Not Started

---

## Sprint 1: Acceptance Testing (Days 1-2)

### Phase 1.1: Test Infrastructure Setup
- ✗ Create acceptance test checklist template
- ✗ Setup test environment (test server, sample data)
- ✗ Prepare test configurations
- ✗ Document test procedure

### Phase 1.2: Dashboard Testing
- ✗ Test connection status display
- ✗ Test quick stats widgets
- ✗ Test recent activity log
- ✗ Test quick actions (Connect, Disconnect, Settings)
- ✗ Create dashboard test report
- ✗ Take screenshots
- ✗ Document bugs

### Phase 1.3: Reports Page Testing
- ✗ Test report list display
- ✗ Test filtering and search
- ✗ Test report details view
- ✗ Test report actions (Submit, Retry, Delete)
- ✗ Create reports test report
- ✗ Document bugs

### Phase 1.4: Converters Page Testing
- ✗ Test converter list display
- ✗ Test Add/Edit/Delete converters
- ✗ Test converter status indicators
- ✗ Test converter controls
- ✗ Document current converter dialog structure
- ✗ Create converters test report
- ✗ Document bugs

### Phase 1.5: Settings Dialog Testing
- ✗ Test API General Settings panel
- ✗ Test Product Domain panel
- ✗ Test Report Domain panel
- ✗ Test Production Domain panel
- ✗ Test Process Domain panel
- ✗ Test Software Domain panel
- ✗ Test Asset Domain panel
- ✗ Test RootCause Domain panel
- ✗ Test Save/Cancel functionality
- ✗ Test validation errors
- ✗ Document missing features (cache, metrics)
- ✗ Create settings dialog test report
- ✗ Document bugs

### Phase 1.6: Other Pages Testing
- ✗ Test Serial Number Handler
- ✗ Test Software Distribution
- ✗ Test Location Services
- ✗ Test Proxy Settings
- ✗ Create test reports
- ✗ Document bugs

### Phase 1.7: System Tray Testing
- ✗ Test minimize to tray
- ✗ Test restore from tray
- ✗ Test tray menu
- ✗ Test exit from tray
- ✗ Test tray icon state
- ✗ Test on Windows
- ✗ Create system tray test report
- ✗ Document platform-specific issues

### Sprint 1 Deliverables
- ✗ Complete acceptance test report
- ✗ Consolidated bug list
- ✗ Screenshot collection
- ✗ Current state documentation

---

## Sprint 2: Settings Dialog Updates (Days 3-4)

### Phase 2.1: Design & Planning
- ✗ Review CONFIG_SETTINGS_REFERENCE.md
- ✗ Design Performance panel layout
- ✗ Design Observability panel layout
- ✗ Create mockups/wireframes
- ✗ Plan widget types

### Phase 2.2: Performance Panel Implementation
- ✗ Create PerformancePanelWidget class
- ✗ Add cache enable/disable checkbox
- ✗ Add cache TTL slider (60-7200s)
- ✗ Add cache TTL value label
- ✗ Add TTL preset buttons (1min, 5min, 10min, 1hour)
- ✗ Add cache size slider (100-5000)
- ✗ Add cache size value label
- ✗ Add cache statistics display
- ✗ Add cache statistics refresh timer
- ✗ Add clear cache button
- ✗ Add queue max size spinner
- ✗ Add max concurrent uploads spinner
- ✗ Connect signals to config
- ✗ Implement load_from_config()
- ✗ Implement save_to_config()
- ✗ Add to settings dialog

### Phase 2.3: Observability Panel Implementation
- ✗ Create ObservabilityPanelWidget class
- ✗ Add metrics enable/disable checkbox
- ✗ Add metrics port spinner (1024-65535)
- ✗ Add metrics endpoint preview (read-only)
- ✗ Add "Open in Browser" button
- ✗ Add health check interval spinner
- ✗ Add health endpoint URLs display
- ✗ Connect signals to config
- ✗ Implement load_from_config()
- ✗ Implement save_to_config()
- ✗ Add to settings dialog

### Phase 2.4: Integration & Testing
- ✗ Add Performance panel to settings dialog tabs
- ✗ Add Observability panel to settings dialog tabs
- ✗ Update tab order
- ✗ Test save/load functionality
- ✗ Test validation (port range, TTL range, cache size range)
- ✗ Test with service running/stopped
- ✗ Test cache statistics refresh
- ✗ Test metrics endpoint opening
- ✗ Test preset buttons
- ✗ Test cache enable/disable (field dependencies)

### Sprint 2 Deliverables
- ✗ Performance panel fully functional
- ✗ Observability panel fully functional
- ✗ Settings dialog updated with v0.3.0 features
- ✗ Test report

---

## Sprint 3: Converter GUI & Lifecycle (Day 5)

### Phase 3.1: Converter Dialog Updates
- ✗ Add priority group box to converter dialog
- ✗ Add priority slider (1-10 range)
- ✗ Add priority value label
- ✗ Add priority description label
- ✗ Connect slider to value label
- ✗ Add color-coding (1-2: red, 3-5: green, 6-10: gray)
- ✗ Load priority from converter config
- ✗ Save priority to converter config
- ✗ Set default priority=5 for new converters

### Phase 3.2: Converter List Updates
- ✗ Add priority column to converter table
- ✗ Show priority badges ([P1], [P5], etc.)
- ✗ Color-code priority badges
- ✗ Add sort by priority option
- ✗ Update converter model

### Phase 3.3: Lifecycle Fixes
- ✗ Add shutdown handler in MainWindow
- ✗ Implement graceful service shutdown
- ✗ Add shutdown timeout (5 seconds)
- ✗ Save config before exit
- ✗ Save window geometry
- ✗ Fix system tray minimize/restore
- ✗ Update tray icon tooltip (connection status)
- ✗ Test all exit paths (X button, File→Exit, tray menu)
- ✗ Verify no orphaned processes

### Sprint 3 Deliverables
- ✗ Converter dialog with priority slider
- ✗ Converter list with priority badges
- ✗ Clean shutdown (no orphaned processes)
- ✗ System tray working correctly

---

## Sprint 4: UI Polish & Final Testing (Days 6-7)

### Phase 4.1: Icon Audit & Updates
- ✗ Audit all icons in application
- ✗ Identify missing icons
- ✗ Add system tray icon (multi-resolution)
- ✗ Add menu icons (File, Edit, View, Tools, Help)
- ✗ Add toolbar icons (Connect, Disconnect, Settings)
- ✗ Ensure consistent icon style

### Phase 4.2: Menu Updates
- ✗ Create File menu (Connect, Disconnect, Settings, Exit)
- ✗ Create Edit menu (Preferences)
- ✗ Create View menu (Show pages, Refresh)
- ✗ Create Tools menu (Clear cache, Open metrics, etc.)
- ✗ Create Help menu (Documentation, About)
- ✗ Add keyboard shortcuts
- ✗ Test all menu actions

### Phase 4.3: Layout & Spacing Fixes
- ✗ Audit all pages for spacing issues
- ✗ Fix alignment issues
- ✗ Ensure consistent margins (10px)
- ✗ Fix responsive resizing
- ✗ Test on different screen sizes
- ✗ Fix tab order for keyboard navigation

### Phase 4.4: Bug Fixes
- ✗ Review all test reports
- ✗ Prioritize bugs (critical, high, medium, low)
- ✗ Fix critical bugs
- ✗ Fix high priority bugs
- ✗ Fix medium priority bugs (time permitting)
- ✗ Document low priority bugs (future work)
- ✗ Create bug fix changelog

### Phase 4.5: Final Testing
- ✗ Run full acceptance test suite
- ✗ Test all new features (cache, metrics, priority)
- ✗ Test all lifecycle scenarios
- ✗ Test on Windows
- ✗ Test with real service connection
- ✗ Performance test (check for UI lag)
- ✗ Test fresh install scenario
- ✗ Test upgrade scenario (config migration)
- ✗ Test start with auto-connect
- ✗ Test start minimized
- ✗ Test long-running session (8+ hours)
- ✗ Create final test report

### Phase 4.6: Documentation Updates
- ✗ Update user guide (new settings panels)
- ✗ Update configuration reference (if needed)
- ✗ Take screenshots (settings dialog, converter dialog)
- ✗ Create CHANGELOG entry
- ✗ Update README (if needed)

### Sprint 4 Deliverables
- ✗ Complete icon set
- ✗ Updated menus with shortcuts
- ✗ Consistent layouts and spacing
- ✗ All critical bugs fixed
- ✗ Final test report
- ✗ Updated documentation
- ✗ CHANGELOG entry

---

## Project Completion

### Final Deliverables
- ✗ All GUI pages tested and documented
- ✗ Settings dialog with all v0.3.0 features
- ✗ Converter priority UI fully functional
- ✗ Clean startup/shutdown (no orphaned processes)
- ✗ System tray working correctly
- ✗ Consistent UI polish (icons, menus, layouts)
- ✗ All critical bugs fixed
- ✗ Complete documentation

### Completion Checklist
- ✗ All tests passing
- ✗ Move project tests to `tests/` suite (if applicable)
- ✗ Move examples to `examples/` (if applicable)
- ✗ Update CHANGELOG.md under [Unreleased]
- ✗ Create COMPLETION_SUMMARY.md
- ✗ Move project to `docs/internal_documentation/completed/2026-Q1/`
- ✗ Commit and push

---

## Summary

**Total Tasks:** ~110
**Completed:** 0 (0%)
**In Progress:** 0
**Blocked:** 0
**Not Started:** ~110

**Estimated Effort:** 56 hours (7 days)
**Actual Effort:** 0 hours

---

**Next Task:** Phase 1.1 - Create acceptance test checklist template
