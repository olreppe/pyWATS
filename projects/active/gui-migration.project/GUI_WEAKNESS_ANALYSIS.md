# Current GUI Weakness Analysis

**Date:** February 4, 2026  
**Analyzer:** GitHub Copilot  
**Purpose:** Identify reliability, data integrity, and stability issues in current GUI before migration  
**User Requirement:** "Fix any weaknesses, ensure reliability, NEVER lose customer data"

---

## 📊 Executive Summary

**Overall Assessment:** Current GUI is functional but has **CRITICAL DATA INTEGRITY GAPS** that violate the "never lose data" requirement.

**Severity Breakdown:**
- 🔴 **CRITICAL (3 issues):** Data loss risks, no offline queue, connection failures not handled
- 🟠 **HIGH (5 issues):** Error handling gaps, async safety, resource cleanup
- 🟡 **MEDIUM (4 issues):** Single-instance enforcement, retry logic missing, timeout handling
- 🟢 **LOW (2 issues):** UI polish, logging verbosity

**Migration Priority:** Fix CRITICAL and HIGH issues during migration, defer MEDIUM/LOW to post-migration.

---

## 🔴 CRITICAL Issues (Must Fix During Migration)

### C1: NO LOCAL QUEUE FOR FAILED OPERATIONS
**Location:** [connection.py](../../../src/pywats_client/gui/pages/connection.py#L346-L408)  
**Severity:** 🔴 CRITICAL - VIOLATES "NEVER LOSE DATA" REQUIREMENT

**Problem:**
```python
async def _run_send_uut_test(self) -> None:
    """Run test UUT send operation"""
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.post(f"{url}/api/Report/wats", json=test_report, headers=headers)
            
            if response.status_code in (200, 201):
                # SUCCESS - report sent
                pass
            else:
                # FAILURE - report is LOST FOREVER
                self._show_message("Test Report Failed", f"Server returned {response.status_code}", "warning")
                
    except httpx.ConnectError:
        # FAILURE - report is LOST FOREVER
        self._show_message("Connection Error", "Could not connect to server", "critical")
```

**Impact:**
- ❌ If server is down/unreachable, data is **LOST FOREVER**
- ❌ If connection times out, data is **LOST FOREVER**
- ❌ If authentication fails, data is **LOST FOREVER**
- ❌ No retry mechanism
- ❌ No local queue
- ❌ No "send later" option
- ❌ User sees error message and data is gone

**Fix Required:**
1. Create local queue directory (`pending/`, `failed/`, `sent/`)
2. Save report JSON to `pending/{timestamp}_{uuid}.json` BEFORE sending
3. Attempt send - if success, move to `sent/`
4. If failure, keep in `pending/` and retry later with exponential backoff
5. Background worker checks `pending/` folder every 30s and retries
6. User can view pending queue and manually retry/cancel
7. Failed reports after 10 retries move to `failed/` for manual review

**Affected Operations:**
- Test UUT send (connection page)
- All converter operations (if GUI adds upload feature)
- Any API operation that sends data to server

---

### C2: NO AUTO-RECONNECT MECHANISM
**Location:** [main_window.py](../../../src/pywats_client/gui/main_window.py#L200-L250)  
**Severity:** 🔴 CRITICAL - SERVICE CONNECTION NOT RESILIENT

**Problem:**
```python
async def _connect_to_service(self) -> bool:
    """Connect to the service via IPC"""
    max_retries = 5
    retry_delay = 1.0
    
    for attempt in range(max_retries):
        try:
            success = await self._ipc_client.connect()
            if success:
                self._service_connected = True
                return True
        except Exception as e:
            logger.warning(f"IPC connection attempt {attempt+1} failed: {e}")
        
        if attempt < max_retries - 1:
            await asyncio.sleep(retry_delay)
    
    # GIVES UP AFTER 5 ATTEMPTS - NO FURTHER RECONNECTION!
    self._service_connected = False
    return False
```

**Impact:**
- ❌ Tries 5 times at startup, then **GIVES UP FOREVER**
- ❌ If service crashes during session, **NO RECONNECTION ATTEMPT**
- ❌ User must manually restart GUI to reconnect
- ❌ Status timer (5s) only checks ping, doesn't trigger reconnect
- ❌ Operations fail silently if connection drops mid-session

**Fix Required:**
1. Background reconnection worker runs every 15s
2. If disconnected, attempt reconnect with exponential backoff (1s → 2s → 5s → 10s → 30s max)
3. Show reconnection UI banner: "Attempting to reconnect... (attempt 3/∞)"
4. When reconnected, trigger "connection restored" event
5. Pending operations in queue auto-retry on reconnection
6. User notification when connection lost/restored

---

### C3: NO OFFLINE MODE - GUI UNUSABLE WITHOUT CONNECTION
**Location:** Multiple pages  
**Severity:** 🔴 CRITICAL - BLOCKING OPERATIONS

**Problem:**
- Setup page: All fields disabled when disconnected ([setup.py](../../../src/pywats_client/gui/pages/setup.py#L623-L645))
- Connection page: Tests fail immediately if service offline
- Dashboard: No status if service offline
- Converters page: Likely unusable offline (needs verification)

**Impact:**
- ❌ User cannot configure client when service offline
- ❌ User cannot view/edit local settings
- ❌ User cannot prepare configuration for later deployment
- ❌ Terrible UX - GUI becomes useless when connection drops

**Fix Required:**
1. **Read-only offline mode:** Allow viewing all settings when offline
2. **Deferred save mode:** Allow editing settings, save locally, sync to service when online
3. **Local-first architecture:** Config saved to local file immediately, synced to service as secondary operation
4. **UI indicators:** Clear visual distinction between online/offline/syncing states
5. **Optimistic UI:** Show changes immediately, show sync status indicator

---

## 🟠 HIGH Issues (Fix During Migration)

### H1: ERROR HANDLING GAPS IN CONFIG SAVE OPERATIONS
**Location:** [setup.py](../../../src/pywats_client/gui/pages/setup.py#L685-L704), [api_settings.py](../../../src/pywats_client/gui/pages/api_settings.py#L342-L365)  
**Severity:** 🟠 HIGH - DATA INTEGRITY RISK

**Problem:**
```python
def save_config(self) -> None:
    """Save configuration"""
    self.config.instance_name = self._client_name_edit.text().strip()
    self.config.station_name = self._station_name_edit.text().strip()
    # ... more fields ...
    
    # Save to file
    if self.config._config_path:
        try:
            self.config.save()  # What if this fails?
        except Exception as e:
            print(f"Failed to save config: {e}")  # ONLY PRINTS TO CONSOLE!
```

**Impact:**
- ❌ User changes settings, clicks Apply
- ❌ Save fails (disk full, permissions, etc.)
- ❌ User sees no error dialog, assumes saved
- ❌ Changes are LOST when GUI closes
- ❌ No validation of saved values
- ❌ No rollback on partial failure

**Fix Required:**
1. Wrap ALL config saves in try/except with ERROR DIALOG
2. Validate config values before saving (non-empty required fields, valid ranges)
3. Atomic save pattern: Write to temp file → Validate → Rename to actual config
4. Show success toast notification: "Configuration saved successfully"
5. Log failures with full traceback
6. Disable Apply button only after CONFIRMED save success

---

### H2: CONVERTER FOLDER CREATION HAS NO ERROR HANDLING
**Location:** [converters.py](../../../src/pywats_client/gui/pages/converters.py#L200-L250)  
**Severity:** 🟠 HIGH - SYSTEM RELIABILITY

**Problem:**
```python
def create_default_converter_configs(self) -> None:
    """Create default watch folders and config files"""
    base_path = Path(self.config.converter_base_path)
    
    # Create folders for each system converter
    for converter_name in SYSTEM_CONVERTERS:
        watch_folder = base_path / converter_name / "watch"
        done_folder = base_path / converter_name / "done"
        error_folder = base_path / converter_name / "error"
        pending_folder = base_path / converter_name / "pending"
        
        # NO ERROR HANDLING - what if disk full, permissions denied, path too long?
        watch_folder.mkdir(parents=True, exist_ok=True)
        done_folder.mkdir(parents=True, exist_ok=True)
        error_folder.mkdir(parents=True, exist_ok=True)
        pending_folder.mkdir(parents=True, exist_ok=True)
```

**Impact:**
- ❌ Folder creation fails silently
- ❌ Converters expect folders to exist, crash when missing
- ❌ File watchers fail to start
- ❌ Reports pile up with no error notification
- ❌ Hard to diagnose in production

**Fix Required:**
1. Wrap folder creation in try/except
2. Check disk space before creating folders
3. Verify write permissions
4. Show error dialog if creation fails with actionable message:
   - "Failed to create converter folders at C:\path\to\converters"
   - "Reason: Permission denied"
   - "Solution: Run as administrator or choose different location"
5. Add "Verify Folders" button to check all folders exist and are writable
6. Automatically attempt fix (recreate missing folders) on GUI startup

---

### H3: ASYNC OPERATIONS WITHOUT EVENT LOOP GUARDS
**Location:** [connection.py](../../../src/pywats_client/gui/pages/connection.py#L250-L253), [main_window.py](../../../src/pywats_client/gui/main_window.py#L443)  
**Severity:** 🟠 HIGH - CRASH RISK

**Problem:**
```python
def _on_test_connection(self) -> None:
    """Handle test connection button click"""
    self._test_btn.setEnabled(False)
    self._test_btn.setText("Testing...")
    
    try:
        asyncio.create_task(self._run_connection_test(auto=False))  # CRASHES if event loop not ready!
    except RuntimeError as e:
        logger.warning(f"Could not start async test: {e}")
        self._test_btn.setEnabled(True)
        self._test_btn.setText("Run test")
        self.update_status("Error: No event loop")  # ONLY LOGS - NO USER NOTIFICATION!
```

**Impact:**
- ❌ If qasync event loop not fully initialized, task creation fails
- ❌ User clicks button, sees "Testing..." forever, no feedback
- ❌ Error only visible in logs, not in UI
- ❌ Happens during rapid startup actions (user clicks too fast)
- ❌ Confusing UX - button stuck in disabled state

**Fix Required:**
1. Add event loop check before all `asyncio.create_task()` calls:
   ```python
   loop = asyncio.get_event_loop()
   if not loop.is_running():
       QMessageBox.warning(self, "Not Ready", "Application still initializing. Please wait...")
       return
   ```
2. OR use ErrorHandlingMixin method that handles this gracefully
3. Show error dialog if event loop not ready
4. Add loading indicator during GUI startup ("Initializing event loop...")
5. Disable all async-requiring buttons until event loop confirmed running

---

### H4: NO RESOURCE CLEANUP ON WINDOW CLOSE
**Location:** [main_window.py](../../../src/pywats_client/gui/main_window.py)  
**Severity:** 🟠 HIGH - RESOURCE LEAK

**Problem:**
- No `closeEvent()` override to clean up resources
- IPC client connection not explicitly closed
- Async tasks not cancelled before shutdown
- Status timer (5s interval) not stopped
- Event subscriptions not unsubscribed

**Impact:**
- ❌ Background tasks keep running after window closed
- ❌ IPC connection stays open, holds server resources
- ❌ Status timer fires after GUI destroyed (potential crash)
- ❌ Memory leaks if GUI reopened multiple times in same process
- ❌ Clean shutdown not guaranteed

**Fix Required:**
```python
def closeEvent(self, event: QCloseEvent) -> None:
    """Clean up resources before closing"""
    try:
        # Stop status timer
        if self._status_timer:
            self._status_timer.stop()
        
        # Cancel all running async tasks
        if hasattr(self, '_pending_tasks'):
            for task in self._pending_tasks:
                if not task.done():
                    task.cancel()
        
        # Disconnect IPC client
        if self._ipc_client:
            asyncio.create_task(self._ipc_client.disconnect())
        
        # Unsubscribe from event bus
        if hasattr(self, '_event_subscriptions'):
            for unsub in self._event_subscriptions:
                unsub()
        
        # Call pages' cleanup if they have it
        for page in self._pages.values():
            if hasattr(page, 'cleanup'):
                page.cleanup()
        
        event.accept()
    except Exception as e:
        logger.exception("Error during cleanup")
        event.accept()  # Close anyway
```

---

### H5: SINGLE-INSTANCE ENFORCEMENT BLOCKS MULTI-INSTANCE USE
**Location:** [app.py](../../../src/pywats_client/gui/app.py#L58-L70)  
**Severity:** 🟠 HIGH - BLOCKS 60%+ USE CASES

**Problem:**
```python
# Check if another instance is already running
socket = QLocalSocket()
socket.connectToServer(server_name)

if socket.waitForConnected(500):
    # Another instance exists - activate it and exit
    socket.write(b"activate")
    socket.waitForBytesWritten()
    socket.close()
    sys.exit(0)  # KILLS THIS INSTANCE - CAN'T RUN MULTIPLE CONFIGURATORS!

# No existing instance - create local server to listen
server = QLocalServer()
QLocalServer.removeServer(server_name)
server.listen(server_name)
```

**Impact:**
- ❌ User cannot open multiple configurators for different client instances
- ❌ Blocks 60%+ deployments that use multiple services
- ❌ User must manually edit instance name in config before launching second GUI
- ❌ Poor UX for multi-instance workflows

**Fix Required (ALREADY APPROVED BY USER):**
1. **REMOVE** QLocalServer single-instance check entirely
2. Add instance selector dialog on startup (if no `--instance` CLI arg)
3. Dialog shows:
   - List of available instances (from config directory)
   - "Create New Instance" button
   - "Default Instance" checkbox for future launches
4. Each instance gets separate window title: "WATS Client - Instance 1 [Connected]"
5. Windows taskbar shows separate icons for each instance
6. Document multi-instance usage in installation guide

---

## 🟡 MEDIUM Issues (Fix Post-Migration)

### M1: NO RETRY LOGIC FOR CONNECTION TEST FAILURES
**Location:** [connection.py](../../../src/pywats_client/gui/pages/connection.py#L286-L304)  
**Severity:** 🟡 MEDIUM - UX ISSUE

**Problem:**
```python
async def _run_connection_test(self, auto: bool = False) -> None:
    """Run connection test asynchronously"""
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(test_url, headers=headers)
            
            if response.status_code == 200:
                self._show_test_result(True, "Online", auto)
            else:
                self._show_test_result(False, f"Server returned {response.status_code}", auto)
                # NO RETRY - one attempt only!
```

**Impact:**
- ⚠️ Transient network errors cause test to fail immediately
- ⚠️ User must manually click "Run test" again
- ⚠️ Auto-test on page show fails on temporary connection issues
- ⚠️ Annoying when starting GUI with flaky connection

**Fix Required:**
1. Add retry logic (3 attempts with 2s delay)
2. Show retry progress: "Testing... (attempt 2/3)"
3. Only fail after all retries exhausted
4. Log each attempt for diagnostics

---

### M2: STATUS TIMER INTERVAL TOO SLOW
**Location:** [main_window.py](../../../src/pywats_client/gui/main_window.py#L200)  
**Severity:** 🟡 MEDIUM - UX POLISH

**Problem:**
- Status timer checks connection every 5 seconds
- User disconnect takes up to 5s to show in UI
- Feels sluggish for connection monitoring

**Fix Required:**
1. Reduce interval to 2 seconds for faster feedback
2. OR use event-driven updates (IPC client emits disconnect event)
3. Show "Last checked: 2s ago" indicator

---

### M3: TIMEOUT CONFIGURATION NOT VALIDATED
**Location:** [settings_dialog.py](../../../src/pywats_client/gui/settings_dialog.py#L167-L176)  
**Severity:** 🟡 MEDIUM - CONFIG INTEGRITY

**Problem:**
- Timeout/retry settings use spinbox ranges (5-300s, 1-60s)
- No validation that retry_delay < timeout
- No validation that retry_attempts * retry_delay < reasonable time

**Fix Required:**
1. Add cross-field validation
2. Warn if retry_delay * max_attempts > timeout
3. Suggest optimal values based on network conditions

---

### M4: ERROR MESSAGES NOT USER-FRIENDLY
**Location:** Multiple locations  
**Severity:** 🟡 MEDIUM - UX POLISH

**Problem:**
```python
except Exception as e:
    self._show_message("Error", f"Error sending test report:\n{str(e)}", "critical")
```

**Impact:**
- Error messages show technical exceptions
- Users see: "Error: [Errno 111] Connection refused"
- Not actionable for non-technical users

**Fix Required:**
1. Create error message mapping:
   - `ConnectionRefusedError` → "Could not reach server. Check service address and ensure service is running."
   - `TimeoutError` → "Request timed out. Server may be slow or unreachable."
   - `AuthenticationError` → "Invalid API token. Check API Settings page."
2. Include "Show Details" button for technical error
3. Add "Help" link to troubleshooting guide

---

## 🟢 LOW Issues (Defer to Future)

### L1: VERBOSE LOGGING IN PRODUCTION
**Location:** Multiple files  
**Severity:** 🟢 LOW - OPERATIONAL POLISH

**Problem:**
- Many `logger.warning()` for expected errors (retry attempts, etc.)
- Clutters logs in production
- Makes real issues hard to find

**Fix Required:**
1. Reduce retry attempt logs to DEBUG level
2. Use INFO for state changes
3. Use WARNING only for unexpected errors
4. Use ERROR for critical failures

---

### L2: SETTINGS DIALOG LACKS "RESTORE DEFAULTS" BUTTON
**Location:** [settings_dialog.py](../../../src/pywats_client/gui/settings_dialog.py)  
**Severity:** 🟢 LOW - CONVENIENCE FEATURE

**Problem:**
- User configures settings incorrectly
- No easy way to restore defaults
- Must manually reset each field

**Fix Required:**
1. Add "Restore Defaults" button
2. Restores factory defaults for all settings
3. Requires confirmation before resetting

---

## 📋 Summary Statistics

| Severity | Count | Must Fix in Migration |
|----------|-------|----------------------|
| 🔴 CRITICAL | 3 | ✅ YES (data integrity) |
| 🟠 HIGH | 5 | ✅ YES (reliability) |
| 🟡 MEDIUM | 4 | ⏸️ DEFER (UX polish) |
| 🟢 LOW | 2 | ⏸️ DEFER (nice-to-have) |
| **TOTAL** | **14** | **8 must fix** |

---

## 🎯 Migration Fix Priority

### Phase 1: CRITICAL Fixes (Must Do - Data Integrity)
1. ✅ **C1: Local queue system** for failed operations (HIGHEST PRIORITY)
2. ✅ **C2: Auto-reconnect mechanism** with exponential backoff
3. ✅ **C3: Offline mode** - allow local config editing when disconnected

### Phase 2: HIGH Fixes (Must Do - Reliability)
4. ✅ **H1: Error handling for config saves** with user dialogs
5. ✅ **H2: Error handling for folder creation** with diagnostics
6. ✅ **H3: Event loop guards** for async operations
7. ✅ **H4: Resource cleanup** on window close
8. ✅ **H5: Remove single-instance enforcement** (add instance selector)

### Phase 3: MEDIUM Fixes (Defer to Post-Migration)
9. ⏸️ **M1-M4:** Retry logic, timeout validation, error messages, status timer

### Phase 4: LOW Fixes (Future Enhancement)
10. ⏸️ **L1-L2:** Logging levels, restore defaults

---

## 🔧 Implementation Recommendations

### Local Queue System (C1) - DETAILED DESIGN

**Directory Structure:**
```
%APPDATA%/pyWATS/instances/{instance_id}/queue/
├── pending/          # Reports waiting to send
│   ├── 20260204_143052_uuid123.json
│   └── 20260204_143055_uuid456.json
├── failed/           # Reports failed after 10 retries
│   └── 20260204_142000_uuid789.json
└── sent/             # Successfully sent (keep 7 days)
    └── 20260204_140000_uuid012.json
```

**Queue Manager Component:**
```python
class QueueManager(QObject):
    """Manages local queue of pending operations"""
    
    # Signals
    queue_changed = Signal(int)  # Emit when queue count changes
    send_success = Signal(str)   # Emit when item sent successfully
    send_failed = Signal(str, str)  # Emit when item fails (id, reason)
    
    def __init__(self, instance_id: str, ipc_client):
        self.queue_dir = Path(get_app_data_dir()) / "queue"
        self.pending_dir = self.queue_dir / "pending"
        self.failed_dir = self.queue_dir / "failed"
        self.sent_dir = self.queue_dir / "sent"
        self.ipc_client = ipc_client
        
        # Create directories
        for dir in [self.pending_dir, self.failed_dir, self.sent_dir]:
            dir.mkdir(parents=True, exist_ok=True)
        
        # Start background worker
        self.worker_timer = QTimer()
        self.worker_timer.timeout.connect(self.process_queue)
        self.worker_timer.start(30000)  # Check every 30s
    
    def enqueue(self, operation: dict) -> str:
        """Add operation to queue and attempt immediate send"""
        # Generate unique ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = f"{timestamp}_{uuid.uuid4().hex[:8]}"
        
        # Save to pending folder
        file_path = self.pending_dir / f"{unique_id}.json"
        with open(file_path, 'w') as f:
            json.dump({
                'id': unique_id,
                'operation': operation,
                'attempts': 0,
                'created': datetime.now().isoformat(),
                'last_attempt': None,
                'error': None
            }, f, indent=2)
        
        # Attempt immediate send (async)
        asyncio.create_task(self.send_item(unique_id))
        
        self.queue_changed.emit(self.get_queue_count())
        return unique_id
    
    async def send_item(self, item_id: str) -> bool:
        """Attempt to send a queued item"""
        file_path = self.pending_dir / f"{item_id}.json"
        if not file_path.exists():
            return False
        
        # Load item
        with open(file_path, 'r') as f:
            item = json.load(f)
        
        # Update attempt count
        item['attempts'] += 1
        item['last_attempt'] = datetime.now().isoformat()
        
        try:
            # Attempt send via IPC
            success = await self.ipc_client.send_operation(item['operation'])
            
            if success:
                # Move to sent folder
                sent_path = self.sent_dir / f"{item_id}.json"
                with open(sent_path, 'w') as f:
                    json.dump(item, f, indent=2)
                file_path.unlink()
                
                self.send_success.emit(item_id)
                self.queue_changed.emit(self.get_queue_count())
                return True
            else:
                raise Exception("IPC send failed")
                
        except Exception as e:
            # Save error
            item['error'] = str(e)
            
            # Move to failed after 10 attempts
            if item['attempts'] >= 10:
                failed_path = self.failed_dir / f"{item_id}.json"
                with open(failed_path, 'w') as f:
                    json.dump(item, f, indent=2)
                file_path.unlink()
                
                self.send_failed.emit(item_id, str(e))
                self.queue_changed.emit(self.get_queue_count())
                return False
            else:
                # Keep in pending for retry
                with open(file_path, 'w') as f:
                    json.dump(item, f, indent=2)
                return False
    
    def process_queue(self) -> None:
        """Background worker to retry pending items"""
        for file_path in self.pending_dir.glob("*.json"):
            item_id = file_path.stem
            asyncio.create_task(self.send_item(item_id))
    
    def get_queue_count(self) -> int:
        """Get count of pending items"""
        return len(list(self.pending_dir.glob("*.json")))
```

**UI Integration:**
- Status bar indicator: "📤 3 pending" (yellow if >0)
- Click indicator to open queue viewer dialog
- Queue viewer shows:
  - Pending items (with retry count, last attempt time)
  - Failed items (with error message, manual retry button)
  - "Clear Sent Items" button (deletes old sent files)

---

## ✅ Validation Checklist

Before considering migration complete, verify ALL CRITICAL/HIGH fixes:

- [ ] **C1:** Local queue working - operation fails → saved locally → retries automatically → shows in UI
- [ ] **C1:** Test manual queue retry - failed item → user clicks retry → succeeds → moved to sent
- [ ] **C2:** Auto-reconnect working - disconnect service → GUI shows reconnecting → service starts → auto-reconnects
- [ ] **C2:** Queue processes on reconnect - items pending → reconnects → items auto-send
- [ ] **C3:** Offline mode working - disconnect service → all settings still editable → saves locally
- [ ] **H1:** Config save errors shown - make file read-only → try save → see error dialog
- [ ] **H2:** Folder creation errors shown - point to protected path → see actionable error
- [ ] **H3:** Event loop guards working - rapid button clicks → no crashes → graceful degradation
- [ ] **H4:** Cleanup working - close window → no background tasks → resources freed
- [ ] **H5:** Multi-instance working - launch 2 GUIs → instance selector shown → separate windows

---

## 📝 Notes for Migration

**Good Design Patterns to Keep:**
- ✅ ErrorHandlingMixin - centralized error dialogs
- ✅ AsyncAPIRunner - composition-based async helper
- ✅ BasePage - loading states, async support
- ✅ IPC client architecture - clean separation
- ✅ Settings in separate dialog - reduces clutter
- ✅ Sidebar navigation - good UX

**Architecture Improvements:**
1. Add QueueManager as core component (alongside AsyncTaskRunner, EventBus)
2. Add ConnectionMonitor component (handles reconnection logic)
3. Add OfflineCapability mixin (enables offline editing for any page)
4. Add ValidationMixin (standardizes config validation)
5. Add cleanup() method to all pages (called on window close)

**Testing Requirements:**
- Unit tests for QueueManager (enqueue, retry, move to failed)
- Integration test: Full offline → online → queue drain workflow
- Stress test: 100 operations queued → all processed successfully
- Connection test: Service restart → auto-reconnect → operations resume
- Multi-instance test: 3 instances running simultaneously → no conflicts

---

**Analysis Complete:** February 4, 2026  
**Next Step:** Migrate pages with CRITICAL and HIGH fixes applied  
**Success Criteria:** All 8 critical/high validation checks pass
