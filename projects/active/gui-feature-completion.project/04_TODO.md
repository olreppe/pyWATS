# TODO: GUI Feature Completion

**Updated:** February 5, 2026  
**Scope:** Short-term deferred GUI features (9 hours)

---

## 📋 Phase 1: qasync Integration (2 hours)

### Setup
- [ ] **Install qasync** - Add to requirements.txt and pyproject.toml
- [ ] **Test basic integration** - Verify qasync works with PySide6

### Main GUI Entry Point
- [ ] **Update run_new_gui.py** - Replace event loop with qasync.QEventLoop
- [ ] **Update run_new_gui_debug.py** - Same qasync integration
- [ ] **Update src/pywats_ui/main.py** - If separate entry point
- [ ] **Test GUI launch** - Verify no regressions

### ConnectionPage Updates
- [ ] **Add asyncSlot decorator** - Import from qasync
- [ ] **Update _on_test_connection_clicked** - Make async slot
- [ ] **Update _on_send_uut_clicked** - Make async slot
- [ ] **Add error handling** - Try/except with finally for button re-enable
- [ ] **Test button clicks** - Verify no GUI freezing

**Validation:**
- [ ] GUI launches normally
- [ ] All pages still functional
- [ ] Async operations don't freeze GUI
- [ ] Error dialogs appear correctly

---

## 📋 Phase 2: Report Submission (4 hours)

### QueueManager Design
- [ ] **Review existing QueueManager** - Understand current interface
- [ ] **Design send callback pattern** - Callable signature
- [ ] **Create mock implementation** - For testing
- [ ] **Document callback contract** - Expected behavior

### Default Send Implementation
- [ ] **Implement _default_send** - Use API client for sending
- [ ] **Add retry logic** - 3 attempts with exponential backoff
- [ ] **Add error handling** - Log failures
- [ ] **Add logging** - Success/failure messages
- [ ] **Test send logic** - Unit tests

### ConnectionPage Integration
- [ ] **Get QueueManager reference** - From main window or create
- [ ] **Wire up "Send Test UUT" button** - Connect to handler
- [ ] **Create _create_test_report** - Generate test data
- [ ] **Add progress dialog** - Show during send
- [ ] **Add success/failure messages** - User feedback
- [ ] **Test full flow** - Send → Progress → Result

**Validation:**
- [ ] Button sends test report
- [ ] Progress dialog shows during send
- [ ] Success message on successful send
- [ ] Failure message with details on error
- [ ] Button re-enables after operation
- [ ] Errors logged appropriately

---

## 📋 Phase 3: Connection Testing (3 hours)

### Connection Test Logic
- [ ] **Implement _run_connection_test** - Full validation logic
- [ ] **Test 1: Server reachable** - GET /api/health
- [ ] **Test 2: Authentication** - GET /api/user/me with API key
- [ ] **Test 3: Basic operation** - GET /api/products
- [ ] **Add error handling** - ConnectError, timeout, auth failure
- [ ] **Add logging** - Log each test step
- [ ] **Test validation logic** - Unit tests

### UI Feedback
- [ ] **Update connection status indicator** - Green/red/yellow
- [ ] **Add "Last Test" timestamp** - Display when last tested
- [ ] **Create detailed result dialog** - Show what passed/failed
- [ ] **Save connection settings** - On successful test
- [ ] **Add CSS styling** - Color code status (green=success, red=fail)

### Visual Polish
- [ ] **Add traffic light icons** - 🟢 🟡 🔴 or equivalent
- [ ] **Add progress spinner** - During test execution
- [ ] **Polish dialog messages** - Clear, actionable text
- [ ] **Add tooltips** - Explain what test does
- [ ] **Test UI updates** - Verify all states work

**Validation:**
- [ ] Connection test validates all 3 steps
- [ ] Status indicator updates correctly
- [ ] Detailed feedback shows in dialog
- [ ] Timestamp updates after each test
- [ ] Settings saved on success only
- [ ] All errors handled gracefully
- [ ] UI is responsive and clear

---

## 📋 Phase 4: Testing & Documentation (Integrated)

### Tests
- [ ] **Add qasync tests** - Test event loop integration
- [ ] **Add QueueManager tests** - Test send callback
- [ ] **Add connection test tests** - Test validation logic
- [ ] **Update existing tests** - Fix any broken tests
- [ ] **Run full test suite** - Ensure no regressions
- [ ] **Run stress tests** - test_gui_stress.py

### Documentation
- [ ] **Update GUI_MIGRATION_COMPLETE_SUMMARY.md** - Mark deferred items complete
- [ ] **Update docs/client/gui-usage.md** - Document new features
- [ ] **Add CHANGELOG entry** - Under [Unreleased] section
- [ ] **Update README** - If needed
- [ ] **Add code examples** - For new features if applicable

**Validation:**
- [ ] All tests passing
- [ ] Documentation complete and accurate
- [ ] CHANGELOG entry added
- [ ] No broken links in docs

---

## 🎉 Completion Checklist

### Technical Completion
- [ ] qasync integrated and working
- [ ] Connection test fully functional
- [ ] Report submission fully functional
- [ ] All tests passing
- [ ] No regressions introduced
- [ ] Error handling comprehensive

### Documentation Completion
- [ ] All docs updated
- [ ] CHANGELOG entry added
- [ ] Code examples added where needed
- [ ] Deferred work section updated

### Quality Gates
- [ ] No new errors or warnings
- [ ] GUI launches cleanly
- [ ] All async operations work
- [ ] User feedback is clear
- [ ] Code is well-commented

---

**Created:** February 5, 2026  
**Last Updated:** February 5, 2026
