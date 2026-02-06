# Implementation Plan: GUI Feature Completion

**Project:** GUI Feature Completion  
**Created:** February 5, 2026  
**Timeline:** 1-2 days (9 hours)

---

## Phase 1: qasync Integration (2 hours)

### Step 1.1: Install and Configure qasync
**Duration:** 30 minutes  
**Files:** requirements.txt, pyproject.toml

**Tasks:**
1. Add `qasync` to requirements.txt
2. Add optional dependency `[gui]` extra
3. Install qasync in venv
4. Test basic qasync integration

**Validation:**
```python
import qasync
import asyncio
from PySide6.QtWidgets import QApplication

# Should create hybrid event loop
app = QApplication([])
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)
```

---

### Step 1.2: Update Main GUI Entry Point
**Duration:** 30 minutes  
**Files:** run_new_gui.py, run_new_gui_debug.py, src/pywats_ui/main.py

**Tasks:**
1. Replace standard event loop with qasync event loop
2. Update app.exec() to use asyncio.run()
3. Test GUI still launches normally

**Before:**
```python
app = QApplication(sys.argv)
# ...
sys.exit(app.exec())
```

**After:**
```python
app = QApplication(sys.argv)
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)

# ...
with loop:
    loop.run_forever()
```

**Validation:**
- GUI launches normally
- No event loop errors
- All pages still functional

---

### Step 1.3: Update ConnectionPage for Async Operations
**Duration:** 1 hour  
**Files:** src/pywats_ui/pages/connection.py

**Tasks:**
1. Add async slot decorators for button handlers
2. Update _run_connection_test to use qasync
3. Update _run_send_uut_test to use qasync
4. Add proper error handling

**Pattern:**
```python
from qasync import asyncSlot

@asyncSlot()
async def _on_test_connection_clicked(self) -> None:
    """Test connection button handler (async)"""
    self._test_connection_button.setEnabled(False)
    try:
        success = await self._run_connection_test()
        self._show_message(
            "Connection Test", 
            "Connected successfully!" if success else "Connection failed",
            "information" if success else "warning"
        )
    except Exception as e:
        self._show_message("Error", f"Test failed: {e}", "critical")
    finally:
        self._test_connection_button.setEnabled(True)
```

**Validation:**
- Button click doesn't freeze GUI
- Connection test runs asynchronously
- Error dialogs appear correctly
- Button re-enables after test

---

## Phase 2: Report Submission (4 hours)

### Step 2.1: QueueManager Send Callback Design
**Duration:** 1 hour  
**Files:** src/pywats_client/queue_manager.py (or create new file)

**Tasks:**
1. Review existing QueueManager interface
2. Design send callback pattern
3. Create mock implementation for testing

**Callback Pattern:**
```python
from typing import Callable, Optional

class QueueManager:
    def __init__(self, config, send_callback: Optional[Callable] = None):
        self._send_callback = send_callback
    
    async def send_report(self, report_data: dict) -> bool:
        """Send report to WATS API"""
        if self._send_callback:
            return await self._send_callback(report_data)
        else:
            # Default implementation
            return await self._default_send(report_data)
```

**Validation:**
- Callback can be None (fallback behavior)
- Callback receives report data
- Callback returns success/failure bool

---

### Step 2.2: Implement Default Send Logic
**Duration:** 1.5 hours  
**Files:** src/pywats_client/queue_manager.py

**Tasks:**
1. Implement _default_send method
2. Use AsyncAPIRunner or similar for API call
3. Add retry logic (3 attempts with exponential backoff)
4. Add error handling and logging

**Implementation:**
```python
async def _default_send(self, report_data: dict) -> bool:
    """Default send implementation using API"""
    max_retries = 3
    retry_delay = 1.0
    
    for attempt in range(max_retries):
        try:
            # Use API client to send report
            response = await self._api_client.post_report(report_data)
            if response.status_code in (200, 201):
                logger.info(f"Report sent successfully: {report_data.get('serial_number')}")
                return True
        except Exception as e:
            logger.warning(f"Send attempt {attempt+1} failed: {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
    
    logger.error(f"Report send failed after {max_retries} attempts")
    return False
```

**Validation:**
- Sends report to WATS API
- Retries on failure (max 3 times)
- Logs success/failure
- Returns bool result

---

### Step 2.3: Connect to ConnectionPage UI
**Duration:** 1.5 hours  
**Files:** src/pywats_ui/pages/connection.py

**Tasks:**
1. Get QueueManager reference in ConnectionPage
2. Create send callback or use default
3. Wire up "Send Test UUT" button
4. Add progress dialog during send
5. Show success/failure message

**Implementation:**
```python
@asyncSlot()
async def _on_send_uut_clicked(self) -> None:
    """Send test UUT button handler"""
    self._send_uut_button.setEnabled(False)
    
    # Show progress dialog
    progress = QProgressDialog("Sending test report...", "Cancel", 0, 0, self)
    progress.setWindowModality(Qt.WindowModal)
    progress.show()
    
    try:
        # Create test report data
        report_data = self._create_test_report()
        
        # Send via QueueManager
        success = await self._queue_manager.send_report(report_data)
        
        if success:
            self._show_message("Success", "Test report sent successfully!", "information")
        else:
            self._show_message("Failed", "Could not send test report. Check logs.", "warning")
    
    except Exception as e:
        self._show_message("Error", f"Send failed: {e}", "critical")
    
    finally:
        progress.close()
        self._send_uut_button.setEnabled(True)
```

**Validation:**
- Button sends test report
- Progress dialog shows during send
- Success/failure message appears
- Button re-enables after send
- Errors handled gracefully

---

## Phase 3: Connection Testing (3 hours)

### Step 3.1: API Connection Validation Logic
**Duration:** 1.5 hours  
**Files:** src/pywats_ui/pages/connection.py

**Tasks:**
1. Implement _run_connection_test method (currently stubbed)
2. Test API endpoint reachability
3. Test authentication
4. Test basic API operations (e.g., get server info)

**Implementation:**
```python
async def _run_connection_test(self) -> bool:
    """Run connection test against WATS API"""
    try:
        # Get connection details from form
        url = self._url_input.text()
        api_key = self._api_key_input.text()
        timeout = self._timeout_spinbox.value()
        
        # Create temporary API client
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            # Test 1: Server reachable
            response = await client.get(f"{url}/api/health")
            if response.status_code != 200:
                logger.warning(f"Health check failed: {response.status_code}")
                return False
            
            # Test 2: Authentication
            headers = {"Authorization": f"Bearer {api_key}"}
            response = await client.get(f"{url}/api/user/me", headers=headers)
            if response.status_code != 200:
                logger.warning(f"Authentication failed: {response.status_code}")
                return False
            
            # Test 3: Basic operation (get products)
            response = await client.get(f"{url}/api/products", headers=headers)
            if response.status_code != 200:
                logger.warning(f"Products query failed: {response.status_code}")
                return False
            
            logger.info("Connection test passed all checks")
            return True
    
    except httpx.ConnectError as e:
        logger.error(f"Connection error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error in connection test: {e}")
        return False
```

**Validation:**
- Tests server reachability
- Tests authentication
- Tests basic API operation
- Returns True/False result
- Handles all errors gracefully

---

### Step 3.2: Update UI Feedback
**Duration:** 1 hour  
**Files:** src/pywats_ui/pages/connection.py

**Tasks:**
1. Update connection status indicator (traffic light)
2. Show detailed test results in dialog
3. Add "Last Test" timestamp display
4. Save successful connection details to config

**Implementation:**
```python
@asyncSlot()
async def _on_test_connection_clicked(self) -> None:
    """Test connection button handler"""
    self._test_connection_button.setEnabled(False)
    self._connection_status.setText("Testing...")
    
    try:
        success = await self._run_connection_test()
        
        if success:
            # Update status indicator (green)
            self._connection_status.setText("✅ Connected")
            self._connection_status.setStyleSheet("color: green; font-weight: bold;")
            
            # Save connection details
            self._save_connection_settings()
            
            # Show success dialog
            self._show_message(
                "Connection Test Successful",
                "Successfully connected to WATS API!\n\n"
                "✓ Server reachable\n"
                "✓ Authentication verified\n"
                "✓ API operational",
                "information"
            )
        else:
            # Update status indicator (red)
            self._connection_status.setText("❌ Failed")
            self._connection_status.setStyleSheet("color: red; font-weight: bold;")
            
            # Show failure dialog
            self._show_message(
                "Connection Test Failed",
                "Could not connect to WATS API.\n\n"
                "Check:\n"
                "• Server URL is correct\n"
                "• API key is valid\n"
                "• Network connection\n"
                "• Firewall settings",
                "warning"
            )
        
        # Update last test timestamp
        from datetime import datetime
        self._last_test_label.setText(f"Last test: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    except Exception as e:
        self._connection_status.setText("❌ Error")
        self._connection_status.setStyleSheet("color: red; font-weight: bold;")
        self._show_message("Error", f"Test failed with error:\n{e}", "critical")
    
    finally:
        self._test_connection_button.setEnabled(True)
```

**Validation:**
- Status indicator updates (green/red)
- Detailed feedback in dialog
- Timestamp shows last test time
- Settings saved on success

---

### Step 3.3: Add Visual Indicators
**Duration:** 30 minutes  
**Files:** src/pywats_ui/pages/connection.py

**Tasks:**
1. Add traffic light icon/color to status label
2. Add "Last Test" timestamp label
3. Add progress spinner during test
4. Polish dialog messages

**Visual Enhancements:**
- 🟢 Green dot for successful connection
- 🔴 Red dot for failed connection
- 🟡 Yellow dot for "Testing..."
- Timestamp: "Last test: 2026-02-05 14:30:22"
- Spinner: Animated during test

**Validation:**
- UI updates reflect connection state
- Visual feedback is clear and intuitive
- No UI freezing during tests

---

## Phase 4: Testing & Documentation (1 hour - included in above)

### Step 4.1: Update Tests
**Duration:** 30 minutes  
**Files:** test_gui_stress.py, tests/client/test_queue_manager.py

**Tasks:**
1. Add tests for qasync integration
2. Add tests for QueueManager send callback
3. Add tests for connection validation
4. Update existing tests if needed

**Validation:**
- All existing tests still pass
- New async tests pass
- Coverage maintained/improved

---

### Step 4.2: Update Documentation
**Duration:** 30 minutes  
**Files:** GUI_MIGRATION_COMPLETE_SUMMARY.md, docs/client/gui-usage.md

**Tasks:**
1. Update "Deferred Work" section (mark as complete)
2. Add new features to user documentation
3. Update CHANGELOG.md

**Documentation Updates:**
- ✅ Async event loop integration - COMPLETE
- ✅ Report submission - COMPLETE
- ✅ Connection testing - COMPLETE

**Validation:**
- Documentation reflects new features
- CHANGELOG entry added
- Examples updated if needed

---

## 🎯 Acceptance Criteria

**Phase 1 (qasync):**
- [ ] qasync installed and configured
- [ ] GUI event loop uses qasync.QEventLoop
- [ ] GUI launches and runs normally
- [ ] Async slots work without freezing GUI

**Phase 2 (Report Submission):**
- [ ] QueueManager has send callback
- [ ] Default send logic implemented with retry
- [ ] "Send Test UUT" button functional
- [ ] Progress dialog shows during send
- [ ] Success/failure messages appear
- [ ] Errors logged and displayed

**Phase 3 (Connection Testing):**
- [ ] Connection test validates server, auth, API
- [ ] Status indicator updates (green/red)
- [ ] Detailed feedback in dialogs
- [ ] Timestamp shows last test time
- [ ] Connection settings saved on success
- [ ] All errors handled gracefully

**Phase 4 (Testing & Docs):**
- [ ] All tests pass (existing + new)
- [ ] Documentation updated
- [ ] CHANGELOG entry added
- [ ] No regressions introduced

---

## 📋 Risk Assessment

**Risk Level:** LOW

**Reasons:**
1. qasync is mature and well-tested library
2. Changes are isolated to ConnectionPage
3. QueueManager already designed for callbacks
4. Can revert to synchronous approach if issues

**Mitigations:**
1. Test qasync integration in isolation first
2. Keep synchronous fallback paths
3. Comprehensive error handling
4. Stress test after each phase

---

**Created:** February 5, 2026  
**Last Updated:** February 5, 2026
