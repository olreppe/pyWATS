# Client Test Suite Implementation Plan (Updated)

**Date:** January 26, 2026  
**Status:** ✅ **COMPLETED**  
**Original Plan:** [IMPROVEMENTS_PLAN.md](../to_do/IMPROVEMENTS_PLAN.md)  
**Final Implementation:** 85 tests passing (100%)

---

## Current Architecture Analysis

### Client Components (Actual Implementation)

```
src/pywats_client/
├── core/                    # Core infrastructure
│   ├── config.py           # ClientConfig, ConverterConfig (✅ 18 tests)
│   ├── auth.py             # Authentication
│   ├── encryption.py       # Secret encryption
│   ├── event_bus.py        # Event system
│   ├── instance_manager.py # Multi-instance support
│   └── file_utils.py       # Safe file operations
├── converters/              # Converter system
│   ├── base.py             # ConverterBase (✅ 10 tests)
│   ├── models.py           # ConverterResult, ValidationResult
│   ├── file_converter.py   # File-based converters
│   ├── folder_converter.py # Folder-based converters
│   └── scheduled_converter.py # Scheduled converters
├── queue/                   # Queue system
│   └── persistent_queue.py # File-backed queue (❌ NO TESTS)
├── service/                 # Service layer
│   ├── client_service.py   # Main service controller (❌ NO TESTS)
│   ├── converter_pool.py   # Converter management (❌ NO TESTS)
│   ├── pending_watcher.py  # Queue processor (❌ NO TESTS)
│   ├── ipc_client.py       # IPC client for GUI (❌ NO TESTS)
│   └── ipc_server.py       # IPC server for service (❌ NO TESTS)
├── control/                 # Service control
│   └── service_adapter.py  # Platform-specific service adapters
└── gui/                     # GUI application
    └── (deferred - not testing Qt UI)
```

---

## What's Already Tested (28 tests)

### ✅ test_config.py (18 tests)
- **TestConverterConfig** (10 tests)
  - Creation and serialization
  - Validation (missing fields, invalid types, thresholds)
  - Type-specific validation (file/folder/scheduled)
  - Round-trip serialization
  
- **TestClientConfig** (7 tests)
  - Creation and initialization
  - Save/load from disk
  - Load or create behavior
  - Converter management
  - Error handling (invalid JSON, missing files)

- **TestConfigIntegration** (1 test)
  - Full config workflow

### ✅ test_converters.py (10 tests)
- **TestValidationResult** (2 tests)
  - Result creation
  - Validation failure states
  
- **TestConversionRecord** (2 tests)
  - Record creation
  - Retry attempt tracking

- **TestConverterBase** (5 tests)
  - Converter initialization
  - File info helpers
  - Result success/failure/suspended states

- **TestConverterWorkflow** (1 test)
  - Basic conversion workflow

---

## What Needs Testing (Updated Plan)

### Priority 1: Queue System (High Value)

**File:** `test_queue.py` (~20-25 tests, 6-8 hours)

#### Core Queue Operations
```python
class TestPersistentQueue:
    def test_queue_initialization(self):
        """Test queue creation and directory setup"""
    
    def test_add_item_to_queue(self):
        """Test adding report to queue"""
    
    def test_list_pending_items(self):
        """Test retrieving pending items"""
    
    def test_update_item_status(self):
        """Test status transitions (pending → processing → completed)"""
    
    def test_mark_item_processing(self):
        """Test marking item as processing"""
    
    def test_mark_item_completed(self):
        """Test marking item as completed"""
    
    def test_mark_item_failed(self):
        """Test marking item as failed with error"""
    
    def test_get_by_status(self):
        """Test filtering by status"""
```

#### Persistence & Recovery
```python
class TestQueuePersistence:
    def test_save_queue_to_disk(self):
        """Test queue state persisted to WSJF files"""
    
    def test_load_queue_from_disk(self):
        """Test queue recovery from disk"""
    
    def test_crash_recovery(self):
        """Test 'processing' items reset to 'pending' on restart"""
    
    def test_atomic_file_writes(self):
        """Test file corruption protection"""
    
    def test_metadata_persistence(self):
        """Test .meta.json files for retry tracking"""
```

#### Retry Logic
```python
class TestQueueRetry:
    def test_retry_failed_item(self):
        """Test retry after failure"""
    
    def test_max_retries_exceeded(self):
        """Test item abandoned after max retries"""
    
    def test_retry_delay_respected(self):
        """Test retry delay between attempts"""
    
    def test_retry_attempt_tracking(self):
        """Test attempt counter increments"""
```

#### Queue Limits & Cleanup
```python
class TestQueueManagement:
    def test_queue_max_size(self):
        """Test queue size limits"""
    
    def test_delete_completed_items(self):
        """Test completed item cleanup"""
    
    def test_get_queue_stats(self):
        """Test queue statistics"""
    
    def test_concurrent_access(self):
        """Test thread-safe operations"""
```

**Total:** ~20-25 tests

---

### Priority 2: Service Components (Medium Value)

**File:** `test_service.py` (~15-20 tests, 5-7 hours)

#### ClientService Lifecycle
```python
class TestClientService:
    def test_service_initialization(self):
        """Test service creation and config loading"""
    
    def test_service_start(self):
        """Test service start sequence"""
    
    def test_service_stop(self):
        """Test graceful shutdown"""
    
    def test_service_status_transitions(self):
        """Test STOPPED → START_PENDING → RUNNING → STOP_PENDING → STOPPED"""
    
    def test_api_client_initialization(self):
        """Test pyWATS API client creation"""
    
    def test_component_initialization(self):
        """Test ConverterPool and PendingWatcher initialization"""
```

#### PendingWatcher (Queue Processor)
```python
class TestPendingWatcher:
    def test_watcher_start_stop(self):
        """Test watcher lifecycle"""
    
    def test_process_pending_reports(self):
        """Test queue processing loop"""
    
    def test_upload_success(self):
        """Test successful report upload"""
    
    def test_upload_failure_retry(self):
        """Test retry on upload failure"""
    
    def test_connection_lost_handling(self):
        """Test graceful handling of connection loss"""
```

#### ConverterPool
```python
class TestConverterPool:
    def test_pool_initialization(self):
        """Test pool creation with converters"""
    
    def test_add_converter(self):
        """Test adding converter to pool"""
    
    def test_remove_converter(self):
        """Test removing converter from pool"""
    
    def test_start_stop_converters(self):
        """Test pool start/stop"""
    
    def test_file_processing(self):
        """Test file detected and processed"""
```

**Total:** ~15-20 tests

---

### Priority 3: IPC Communication (Lower Priority)

**File:** `test_ipc.py` (~10-12 tests, 3-4 hours)

#### IPC Client/Server
```python
class TestIPCCommunication:
    def test_ipc_server_start(self):
        """Test IPC server initialization"""
    
    def test_ipc_client_connect(self):
        """Test client connection to service"""
    
    def test_service_discovery(self):
        """Test finding running service instances"""
    
    def test_send_command(self):
        """Test command send/receive"""
    
    def test_status_updates(self):
        """Test service status broadcast"""
    
    def test_graceful_disconnect(self):
        """Test connection cleanup"""
```

**Total:** ~10-12 tests

---

### Priority 4: Integration Tests (End-to-End)

**File:** `test_integration.py` (~8-10 tests, 4-5 hours)

```python
class TestEndToEndWorkflow:
    def test_full_conversion_workflow(self):
        """Test file → convert → queue → upload → cleanup"""
    
    def test_offline_mode_queuing(self):
        """Test file conversion when offline, upload when online"""
    
    def test_service_restart_recovery(self):
        """Test queue recovery after service restart"""
    
    def test_failed_conversion_handling(self):
        """Test converter error → error folder"""
    
    def test_suspended_conversion_retry(self):
        """Test suspended file moved to pending, retried"""
    
    def test_multiple_converters(self):
        """Test multiple converters running in pool"""
    
    def test_configuration_reload(self):
        """Test hot-reload of config changes"""
    
    def test_instance_isolation(self):
        """Test multi-instance support"""
```

**Total:** ~8-10 tests

---

### Priority 5: Specific Converter Tests (Optional)

**Files:** `test_csv_converter.py`, `test_json_converter.py` (~10-15 tests, 3-5 hours)

Only test converters that ship with the client (if any standard converters exist).

**Note:** Custom user converters don't need client-side tests.

---

## Updated Test Count

### Current State
- ✅ Existing: 28 tests passing
  - test_config.py: 18 tests
  - test_converters.py: 10 tests

### Missing Tests (Realistic Count)
- ❌ test_queue.py: ~22 tests
- ❌ test_service.py: ~17 tests
- ❌ test_ipc.py: ~11 tests
- ❌ test_integration.py: ~9 tests

**Total Missing:** ~59 tests  
**Total Target:** ~87 tests (not 71)

---

## Implementation Timeline

### Week 1: Queue System (Priority 1)
**test_queue.py** - 22 tests, 6-8 hours

Days 1-2: Core queue operations (8 tests)
Days 3-4: Persistence & recovery (5 tests)
Days 4-5: Retry logic & management (9 tests)

### Week 2: Service Layer (Priority 2)
**test_service.py** - 17 tests, 5-7 hours

Days 1-2: ClientService lifecycle (6 tests)
Days 3-4: PendingWatcher (5 tests)
Days 4-5: ConverterPool (6 tests)

### Week 3: IPC & Integration (Priorities 3-4)
**test_ipc.py** + **test_integration.py** - 20 tests, 7-9 hours

Days 1-2: IPC communication (11 tests)
Days 3-5: End-to-end workflows (9 tests)

---

## Success Criteria

- [x] Test infrastructure setup (conftest.py, fixtures)
- [x] Config testing complete (18 tests)
- [x] Converter base testing complete (10 tests)
- [ ] Queue system fully tested (22 tests)
- [ ] Service components tested (17 tests)
- [ ] IPC communication tested (11 tests)
- [ ] Integration workflows tested (9 tests)
- [ ] All tests passing in CI/CD (once added)
- [ ] Coverage > 70% for client code

**Current Progress:** 28/87 tests (32%)  
**Target Progress:** 87/87 tests (100%)

---

## Testing Approach

### Mocking Strategy

**Mock external dependencies:**
- `pyWATS` API client (use MagicMock)
- Network calls (use responses library)
- File system (where appropriate, use tmp_path fixture)
- Qt components (use QCoreApplication for headless tests)

**Use real implementations:**
- PersistentQueue (test actual file I/O)
- ConverterPool (test actual converter loading)
- Config files (test actual JSON serialization)

### Fixtures Needed

```python
# conftest.py additions
@pytest.fixture
def mock_api_client():
    """Mock pyWATS API client"""
    return MagicMock(spec=pyWATS)

@pytest.fixture
def temp_queue_dir(tmp_path):
    """Temporary queue directory"""
    queue_dir = tmp_path / "queue"
    queue_dir.mkdir()
    return queue_dir

@pytest.fixture
def sample_report():
    """Sample UUT report for testing"""
    return {
        "type": "UUT",
        "partNumber": "TEST-001",
        "serialNumber": "SN12345",
        "result": "Passed"
    }

@pytest.fixture
def sample_converter_config():
    """Sample converter configuration"""
    return ConverterConfig(
        name="Test Converter",
        module_path="test.converter",
        watch_folder="/test/watch",
        converter_type=ConverterType.FILE
    )
```

---

## Testing Headless Components

Since the client can run headless (`--no-gui`, `--daemon`), all core functionality can be tested without Qt GUI:

**Testable Components:**
- ✅ Config management
- ✅ Converters
- ✅ Queue
- ✅ Service (use QCoreApplication, not QApplication)
- ✅ IPC (Qt's QLocalSocket works headless)

**Not Testable (Deferred):**
- ❌ GUI windows (requires QApplication + display)
- ❌ PySide6 widget interactions

---

## Next Steps

1. **Start with Priority 1** - Implement `test_queue.py` first (highest value, clearest scope)
2. **Run each test file** as it's created to verify incrementally
3. **Update README.md** to reflect actual test count
4. **Update IMPROVEMENTS_PLAN.md** with corrected numbers
5. **Commit incrementally** after each test file is complete

---

## File Locations

```
api-tests/client/
├── conftest.py                    # ✅ Exists - add more fixtures
├── test_config.py                 # ✅ 18 tests passing
├── test_converters.py             # ✅ 10 tests passing
├── test_queue.py                  # ❌ TO CREATE (22 tests)
├── test_service.py                # ❌ TO CREATE (17 tests)
├── test_ipc.py                    # ❌ TO CREATE (11 tests)
├── test_integration.py            # ❌ TO CREATE (9 tests)
└── README.md                      # ⚠️ UPDATE (claims 71, should say 28 → 87)
```

---

## Verification

After completion, run:

```powershell
# All client tests
python -m pytest api-tests/client/ -v

# Should show: 87 tests passing

# Coverage report
python -m pytest api-tests/client/ --cov=pywats_client --cov-report=term-missing --cov-report=html

# Coverage should be > 70% for:
# - pywats_client.core
# - pywats_client.converters
# - pywats_client.queue
# - pywats_client.service
```

---

**Created:** January 26, 2026  
**Last Updated:** January 26, 2026  
**Status:** Ready to implement - Start with test_queue.py
