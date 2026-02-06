# GUI Critical Issues - Fix Plan

**Date:** February 6, 2026 15:30  
**Based On:** [ARCHITECTURE_ANALYSIS.md](ARCHITECTURE_ANALYSIS.md)  
**Estimated Total Time:** 4-6 hours

---

## Executive Summary

**Root Cause:** Pages migrated from old GUI without schema adaptation. Old GUI used different field names and dict-based config; new uses dataclass with different structure.

**Strategy:** Fix in priority order - critical blockers first (1 hour), then schema mapping (2-3 hours), then reliability components (1 hour).

---

## Phase 1: Critical Blockers (Priority: P0, Time: 1 hour)

### C1: Fix Converter Migration Type Error ⏱️ 10 min

**File:** `run_client_a.py` line 48  
**Issue:** Converters copied as dicts instead of ConverterConfig objects  
**Error:** `AttributeError: 'dict' object has no attribute 'to_dict'`

**Fix:**
```python
# BEFORE:
new_config.converters = old_config['converters']

# AFTER:
from pywats_client.core.config import ConverterConfig
new_config.converters = [
    ConverterConfig.from_dict(c) for c in old_config.get('converters', [])
]
```

**Also Fix:** `run_client_b.py` (same issue)  
**Validation:** Launch GUI, modify converter, close → should save without error

---

### C3: Add ConnectionMonitor Callback ⏱️ 5 min

**File:** `src/pywats_ui/apps/configurator/main_window.py` line 268  
**Issue:** Missing required `check_callback` parameter  
**Error:** `TypeError: ConnectionMonitor.__init__() missing required argument`

**Fix:**
```python
# Add callback method:
def _check_connection(self) -> bool:
    """Check if service is reachable."""
    if not self._config.service_address:
        return False
    # Could ping service, or just check if configured
    return bool(self._config.api_token)

# Initialize with callback:
self._connection_monitor = ConnectionMonitor(
    check_callback=self._check_connection,
    check_interval=30
)
```

**Validation:** Launch GUI → no TypeError on ConnectionMonitor init

---

### C4: Integrate qasync for Event Loop ⏱️ 30 min

**Files:** `run_client_a.py`, `run_client_b.py`  
**Issue:** Async operations fail because no event loop  
**Error:** `RuntimeError: There is no current event loop in thread 'MainThread'`

**Fix:**
```python
# Add import:
import qasync
import asyncio

# Before app.exec():
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)

# Run with event loop:
with loop:
    loop.run_until_complete(main_window.initialize())  # If async init needed
    loop.run_forever()  # Or just app.exec() if qasync handles it
```

**Note:** qasync may need adding to requirements.txt: `qasync==0.27.1`

**Validation:** Test async operations (connection test, report send) work without RuntimeError

---

## Phase 2: Schema Mapping (Priority: P1, Time: 2-3 hours)

### C2: Map Old Schema Fields to New ⏱️ 2-3 hours

**Strategy:** Update each GUI page to use correct ClientConfig field names.

#### Setup Page (setup.py)

**Issues:**
- Line 411: Uses `client_id` (doesn't exist)
- Line 309: Uses `stations` instead of `station_presets`

**Fixes:**
```python
# Remove client_id references (line 411):
# self._client_id.setText(self._config.get("client_id", ""))
# OR if actually needed, add to ClientConfig schema

# Rename stations → station_presets (line 309):
stations = self._config.get("station_presets", [])  # Not "stations"
```

**Decision Needed:** Is `client_id` actually required? If yes, add to ClientConfig. If no, remove UI field.

---

#### Serial Number Handler Page (sn_handler.py)

**Issue:**
- Line 175: Expects nested dict `serial_number_handler: {type, batch_size, ...}`
- ClientConfig has flat fields: `sn_mode, sn_prefix, sn_start, ...`

**Fix:** Rewrite to use flat field access:
```python
# BEFORE (line 175):
sn_config = self._config.get("serial_number_handler", {})
sn_type = sn_config.get("type", "WATS Sequential")
batch_size = sn_config.get("batch_size", 10)

# AFTER:
sn_type = self._config.sn_mode  # Direct access
batch_size = 10  # Default (or add field to ClientConfig if needed)
```

**Mapping Table:**
| Old (nested) | New (flat) |
|-------------|-----------|
| `serial_number_handler['type']` | `sn_mode` |
| `serial_number_handler['batch_size']` | ❌ Add field or use constant |
| `serial_number_handler['fetch_threshold']` | ❌ Add field or use constant |
| `serial_number_handler['allow_reuse']` | ❌ Add field or use constant |

**Decision Needed:** Are batch_size, fetch_threshold, allow_reuse actually used? If yes, add to ClientConfig. If no, remove UI fields.

---

#### Software Page (software.py)

**Issue:**
- Line 223: Uses `sw_dist_root` (doesn't exist)
- Line 226: Uses `sw_dist_chunk_size` (doesn't exist)

**Fix Options:**
1. **Add fields to ClientConfig** if software distribution is supported
2. **Remove software page features** if deprecated
3. **Stub out** with placeholders and disable save

**Recommended:** Review if software distribution is still a feature. If yes, add fields. If no, hide tab via config flag.

---

#### All Pages: Use Direct Attribute Access

**Pattern Change:**
```python
# OLD (error-prone):
value = self._config.get("field_name", default)
self._config["field_name"] = value

# NEW (type-safe):
value = self._config.field_name or default  # Fails at dev time if wrong field
self._config.field_name = value
```

**Benefits:**
- IDE autocomplete works
- TypeError at dev time, not runtime
- Clear what fields exist

**Apply to:** All pages (Connection, Setup, SNHandler, Software, Location, Proxy, Converters, APISettings)

---

## Phase 3: Reliability Components (Priority: P2, Time: 1 hour)

### QueueManager Send Callback ⏱️ 30 min

**Issue:** QueueManager has incomplete send callback integration  
**Impact:** May not properly track report send success/failure

**Fix:** Review framework/reliability/queue_manager.py and ensure:
- Callbacks registered on send success/failure
- UI updates on queue state changes
- Retries work correctly

---

### AsyncAPIRunner Error Handling ⏱️ 30 min

**Issue:** Async operations may fail silently  
**Impact:** User doesn't know if connection test, report send, etc. succeeded

**Fix:**
- Add error signals to AsyncAPIRunner
- Connect to main window error handler
- Show user-friendly error dialogs

---

## Phase 4: Testing & Validation (Priority: P3, Time: 1-2 hours)

### Test Cases

**T1: Config Save/Load Cycle**
1. Launch GUI (client A)
2. Modify: service address, token, station name, converters
3. Close GUI
4. Check config file saved correctly
5. Re-launch GUI
6. Verify all settings persisted

**Expected:** No errors, all fields round-trip correctly

---

**T2: Migration from Old GUI**
1. Delete new config: `~/.pywats/instances/default/client_config.json`
2. Ensure old config exists: `~/.pywats/config.json`
3. Launch GUI (client A)
4. Verify migration success: service address, token, 8 converters visible
5. Close GUI
6. Verify new config file created with correct structure

**Expected:** Migration successful, converters are ConverterConfig objects

---

**T3: Multi-Instance**
1. Launch client A (instance "default")
2. Launch client B (instance "client_b")
3. Modify settings in each independently
4. Close both
5. Re-launch each
6. Verify settings isolated (A changes don't affect B)

**Expected:** Each instance maintains separate config

---

**T4: Async Operations**
1. Configure service address + token
2. Click "Test Connection" in Connection page
3. Send test UUT in Dashboard page
4. Monitor log for errors

**Expected:** No RuntimeError, operations complete, user sees success/failure dialogs

---

**T5: Offline Queue**
1. Configure correctly
2. Disconnect network
3. Send test UUT
4. Verify queued (not lost)
5. Reconnect network
6. Verify auto-sent

**Expected:** Report never lost, auto-syncs on reconnect

---

## Implementation Order

**Recommended sequence:**

1. ✅ **Phase 1.C1** - Converter migration fix (10 min)  
   → Unblocks config save

2. ✅ **Phase 1.C3** - ConnectionMonitor callback (5 min)  
   → Unblocks GUI launch

3. ✅ **Phase 1.C4** - qasync integration (30 min)  
   → Unblocks async operations

4. ✅ **Phase 2** - Schema mapping (2-3 hours)  
   → Fixes all page save errors
   → DECISION NEEDED: Which fields to add vs remove

5. ✅ **Phase 3** - Reliability components (1 hour)  
   → Completes feature parity

6. ✅ **Phase 4** - Testing (1-2 hours)  
   → Validates all fixes

**Total:** 4-6 hours (excluding decision time)

---

## Decision Points (Requires User Input)

**D1: client_id Field**
- **Question:** Is `client_id` still used for anything?
- **Options:**
  - A) Add to ClientConfig if yes
  - B) Remove from Setup page if no
- **Default:** Remove (likely deprecated from old GUI)

**D2: Serial Number Handler Fields**
- **Question:** Are batch_size, fetch_threshold, allow_reuse actually used?
- **Context:** Old GUI had these settings for serial number batching from server
- **Options:**
  - A) Add all fields to ClientConfig if feature is active
  - B) Remove from UI if feature deprecated
- **Default:** Check if WATS API actually supports SN reservation batching

**D3: Software Distribution**
- **Question:** Is software distribution feature still supported?
- **Context:** Old GUI had file distribution root and chunk size settings
- **Options:**
  - A) Add sw_dist_root, sw_dist_chunk_size to ClientConfig if yes
  - B) Hide Software tab if no
- **Default:** Check if domain/software service implements distribution

**D4: API Tokens (plural) vs Token (singular)**
- **Question:** Should multi-token support be added?
- **Context:** Old GUI may have supported multiple API tokens for different services
- **Options:**
  - A) Add api_tokens: List[str] to ClientConfig
  - B) Keep single api_token: str
- **Default:** Keep single token (multi-token likely over-engineering)

---

## Risk Assessment

**Low Risk Fixes:**
- C1 (Converter migration) - Simple type conversion
- C3 (ConnectionMonitor) - Just add callback parameter

**Medium Risk Fixes:**
- C4 (qasync) - Event loop integration can be tricky, needs testing
- Phase 2 (Schema mapping) - Many pages to update, risk of introducing new bugs

**High Risk:**
- None (all fixes are isolated, no breaking changes to other systems)

**Mitigation:**
- Test each fix individually before proceeding
- Keep git commits granular (one fix per commit)
- Can roll back any fix if issues found

---

## Success Criteria

**Minimum (Must Have):**
- ✅ GUI launches without errors
- ✅ Can save configuration without crashes
- ✅ Migration from old config works correctly
- ✅ Connection test works

**Target (Should Have):**
- ✅ All pages save/load correctly
- ✅ Multi-instance works
- ✅ Async operations work
- ✅ Offline queue never loses reports

**Stretch (Nice to Have):**
- ✅ All reliability components complete
- ✅ Integration tests pass
- ✅ Type-safe attribute access throughout

---

## Post-Fix Tasks

1. **Update CHANGELOG.md** under `[Unreleased]` → `Fixed` section:
   - Fixed GUI configuration save errors from schema mismatch
   - Fixed converter migration to use proper ConverterConfig objects
   - Fixed ConnectionMonitor initialization error
   - Integrated qasync for async UI operations

2. **Update BUG_TRACKING.md**:
   - Mark C1-C4 as FIXED
   - Close related issues

3. **Commit and push** with message:
   ```
   fix(gui): Resolve critical config save errors from schema mismatch
   
   - Fixed converter migration to create ConverterConfig objects (not dicts)
   - Added ConnectionMonitor check_callback parameter
   - Integrated qasync for async event loop
   - Updated pages to use correct ClientConfig field names
   - Tests: All 5 validation tests passing
   ```

4. **Close project** using `.agent_instructions.md` checklist

---

**Last Updated:** February 6, 2026 15:30
