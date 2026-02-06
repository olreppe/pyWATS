# Full Stack Architecture Analysis (API → UI)

**Date:** February 6, 2026 14:35  
**Methodology:** Layered Architecture Analysis + Interface Contract Verification  
**Scope:** pyWATS API → Client Service → UI Framework  
**Source:** Code only (no assumptions)  
**Status:** ✅ COMPLETE

---

## Executive Summary

**Root Cause Identified:** GUI pages were migrated from old GUI without adapting to new ClientConfig schema. Pages use dict-like access (`config.get("key")`) expecting keys that don't exist in new schema, and migration code incorrectly passes raw dicts instead of ConverterConfig objects.

**Critical Findings:**
1. **Schema Mismatch**: Old GUI used different field names/structures than new ClientConfig
2. **Type Confusion**: Converters migrated as dicts, not ConverterConfig objects
3. **Missing Fields**: Pages access non-existent keys (client_id, serial_number_handler, sw_dist_root, api_tokens)
4. **Reliability Components**: ConnectionMonitor, AsyncAPIRunner, QueueManager have implementation gaps

**Impact:** Config save fails with KeyError and AttributeError, making GUI unusable for configuration management.

**Fix Complexity:** Medium (2-4 hours) - Requires systematic field mapping and converter migration fix.

---

## Layer 1: API Layer (src/pywats/)

### Architecture

**Core Classes:**
- `pyWATS` - Main synchronous API facade in [pywats.py](src/pywats/pywats.py#L232)
- `AsyncWATS` - Async API facade in [async_wats.py](src/pywats/async_wats.py#L34)
- `SyncServiceWrapper` - Wraps async services for sync calls

**Domain Services** (9 total):
- Report, Product, Production, Process, Asset, Software, RootCause, Analytics, SCIM
- Each has async service in `domains/{domain}/async_service.py`
- All inherit patterns from `shared/base_service.py`

**Authentication:**
- Token-based (parameter: `token`, Base64 encoded credentials)
- Changed from username/password on Jan 24-25, 2026
- Token format: `base64(username:password)`

**Data Models:**
- All models inherit from `PyWATSModel(BaseModel)` (Pydantic v2)
- Located in `shared/models/` and `domains/{domain}/models/`
- Schema validation via Pydantic

**Interface Contract:**
```python
api = pyWATS(
    token="base64_encoded_credentials",
    service_address="https://server.com",
    enable_cache=True,
    instance_id="default"
)
result = api.report.get_report(report_id=123)  # Returns Report model
```

### Health Status
- ✅ Well-defined interfaces
- ✅ Type hints throughout
- ✅ Pydantic validation
- ⚠️ Type stub (pywats.pyi) requires manual maintenance

---

## Layer 2: Client Service Layer (src/pywats_client/)

### Architecture

**Core Config Classes:**
- `ClientConfig` - Main config dataclass ([config.py](src/pywats_client/core/config.py#L213))
- `ConverterConfig` - Converter settings dataclass ([config.py](src/pywats_client/core/config.py#L29))
- `ProxyConfig` - Proxy settings dataclass ([config.py](src/pywats_client/core/config.py#L174))
- `ConfigManager` - File I/O for API settings ([config_manager.py](src/pywats_client/core/config_manager.py))

**ClientConfig Schema:**
```python
@dataclass
class ClientConfig:
    schema_version: str = "2.0"
    instance_id: str = "default"
    instance_name: str = "WATS Client"
    service_address: str = ""
    api_token: str = ""
    station_name: str = ""
    location: str = ""
    # Serial number handler fields (sn_mode, sn_prefix, etc.) - NOT "serial_number_handler"
    # Converters: List[ConverterConfig] - NOT List[dict]
    # NO fields: client_id, api_tokens, sw_dist_root
```

**Dict-Like Interface:**
```python
config.get("key", default)  # Returns getattr(config, key, default)
config["key"]  # Raises KeyError if not exists
config.to_dict()  # Serializes for save (calls .to_dict() on nested objects)
config.save()  # Atomic file write
```

**Service Classes:**
- `ClientService` - Report upload and sync service
- `AsyncClientService` - Async version
- `QueueManager` - Offline report queue (framework/reliability/)
- `ConnectionMonitor` - Connection status tracking (framework/reliability/)

### Interface Contract

```python
config = ClientConfig.load_or_create(Path("~/.pywats/instances/default/client_config.json"))
config.service_address = "https://server.com"
config.api_token = "base64_token"
config.converters = [ConverterConfig(...), ConverterConfig(...)]  # Must be objects!
config.save()
```

### Health Status
- ✅ Well-structured dataclass model
- ✅ Atomic file writes (SafeFileWriter)
- ✅ Forward-compatible (filters unknown fields)
- ❌ GUI pages expect different schema (old GUI format)
- ❌ Migration code creates type confusion (dicts vs objects)

---

## Layer 3: UI Framework (src/pywats_ui/)

### Architecture

**Base Classes:**
- `BaseMainWindow` - Main window base ([framework/__init__.py](src/pywats_ui/framework/__init__.py#L60))
- `BasePage` - Page base with async support ([framework/base_page.py](src/pywats_ui/framework/base_page.py#L38))
- `ErrorHandlingMixin` - Centralized error dialogs

**Configurator App:**
- `ConfiguratorMainWindow` - Sidebar navigation window
- **11 Pages:**
  - Dashboard, Setup, Connection, SerialNumbers, APISettings, Converters
  - Software, Location, Proxy, Log, About

**Reliability Components:**
- `QueueManager` - Never lose reports (offline queue)
- `ConnectionMonitor` - Track connection state
- `AsyncAPIRunner` - Run async operations without blocking UI

**Page Lifecycle:**
```python
page = ConnectionPage(config, queue_manager, parent)
page.load_config()  # Read from config into UI widgets
# User edits...
page.save_config()  # Write from UI widgets to config, then config.save()
```

### Health Status
- ✅ Clean separation of concerns (pages, framework, widgets)
- ✅ Centralized error handling
- ⚠️ Reliability components incomplete (ConnectionMonitor missing param, AsyncAPIRunner no qasync)
- ❌ **CRITICAL: Pages use old GUI schema expectations**

---

## Layer 4: Interface Contract Verification

### Layer 1 ↔ Layer 2 (API ↔ Client Service)

**Contract:** Client passes token and service address to API, receives Pydantic models back.

**Verification:** ✅ PASS
- ClientConfig.api_token → pyWATS(token=...)
- ClientConfig.service_address → pyWATS(service_address=...)
- API returns typed models (Report, Product, etc.)

### Layer 2 ↔ Layer 3 (Client Service ↔ UI)

**Contract:** UI pages read/write ClientConfig fields, save changes atomically.

**Verification:** ❌ FAIL - Multiple contract violations:

#### Issue 1: Missing Fields (KeyError on access)
Pages expect fields that don't exist in ClientConfig:

| Page | Expected Field | Actual Field | Line |
|------|---------------|--------------|------|
| Setup | `client_id` | ❌ Not in schema | [setup.py#L411](src/pywats_ui/apps/configurator/pages/setup.py#L411) |
| Setup | `stations` | `station_presets` | [setup.py#L309](src/pywats_ui/apps/configurator/pages/setup.py#L309) |
| SNHandler | `serial_number_handler` (dict) | `sn_*` fields (flat) | [sn_handler.py#L175](src/pywats_ui/apps/configurator/pages/sn_handler.py#L175) |
| Software | `sw_dist_root` | ❌ Not in schema | [software.py#L223](src/pywats_ui/apps/configurator/pages/software.py#L223) |
| Software | `sw_dist_chunk_size` | ❌ Not in schema | [software.py#L226](src/pywats_ui/apps/configurator/pages/software.py#L226) |

#### Issue 2: Type Confusion (AttributeError on save)
Converters migrated as dicts, but config.save() expects ConverterConfig objects:

```python
# Migration code (WRONG):
new_config.converters = old_config['converters']  # List[dict]

# ClientConfig.to_dict() tries:
"converters": [c.to_dict() for c in self.converters]  # ERROR: dict has no to_dict()
```

**Location:** [run_client_a.py#L48](run_client_a.py#L48)

#### Issue 3: Old GUI Schema vs New Schema

**Old GUI Schema** (`~/.pywats/config.json`):
```json
{
  "instance_id": "A",
  "serial_number_handler": {
    "type": "WATS Sequential",
    "batch_size": 10,
    "fetch_threshold": 5
  },
  "client_id": "some_guid",
  "sw_dist_root": "/path/to/software",
  "converters": [{"name": "CSV", ...}]  // Plain dicts
}
```

**New Schema** (`ClientConfig`):
```python
instance_id: str  # ✅ Same
sn_mode: str  # ❌ Not "serial_number_handler"
sn_prefix: str  # ❌ Flat, not nested
# ❌ No client_id field
# ❌ No sw_dist_root field
converters: List[ConverterConfig]  # ❌ Must be objects, not dicts
```

---

## Layer 5: Data Flow Analysis

### Configuration Save Flow

```
1. User edits field in GUI page (e.g., ConnectionPage)
2. Page.save_config() called
3. Page reads widget values: value = self._address_edit.text()
4. Page tries to set config: self._config.set("service_address", value)
   OR: self._config["service_address"] = value
5. ClientConfig.__setitem__ validates field exists
6. self._config.save() called
7. ClientConfig.to_dict() serializes:
   - Calls converter.to_dict() for each converter
   - ❌ FAILS if converter is dict (AttributeError)
8. SafeFileWriter.write_json_atomic() writes to file
```

**Break Points:**
- **Step 4:** KeyError if field doesn't exist in ClientConfig schema
- **Step 7:** AttributeError if converter is dict instead of ConverterConfig

### Configuration Load Flow

```
1. ClientConfig.load_or_create(path)
2. SafeFileReader.read_json_safe() reads file
3. ClientConfig.from_dict() filters to known fields
   - Unknown fields (client_id, sw_dist_root) dropped silently
4. Converters deserialized as dicts (from JSON)
   - ❌ Should be ConverterConfig.from_dict(d)
5. Config passed to GUI pages
6. Pages call config.get("key")
   - ❌ FAILS for dropped fields (returns None, then KeyError on dict ops)
```

**Break Points:**
- **Step 3:** Silent data loss (unknown fields dropped)
- **Step 4:** Type confusion (dicts instead of ConverterConfig)
- **Step 6:** KeyError when pages access non-existent fields

### Migration Flow (run_client_a.py)

```
1. Load old config: ~/.pywats/config.json
2. Load new config: ~/.pywats/instances/default/client_config.json
3. Migrate fields:
   new_config.service_address = old_config['service_address']  # ✅ Works
   new_config.api_token = old_config['api_token']  # ✅ Works
   new_config.converters = old_config['converters']  # ❌ WRONG TYPE
4. Save new config:
   - ❌ FAILS at save() because converters are dicts
```

**Break Point:** Step 3 - Should convert dicts to ConverterConfig objects

---

## Layer 6: Issue Cataloging

### Critical Issues (Blockers)

#### C1: Converter Migration Type Error
**Severity:** CRITICAL  
**Symptom:** `AttributeError: 'dict' object has no attribute 'to_dict'` (6 occurrences)  
**Root Cause:** Migration code assigns raw dicts from old config to ConverterConfig field  
**Location:** [run_client_a.py#L48](run_client_a.py#L48)  
**Fix:**
```python
# Current (WRONG):
new_config.converters = old_config['converters']

# Fixed:
new_config.converters = [
    ConverterConfig.from_dict(c) for c in old_config.get('converters', [])
]
```
**Complexity:** Low (10 minutes)

#### C2: Missing ClientConfig Fields
**Severity:** CRITICAL  
**Symptom:** `KeyError: 'client_id'`, `'serial_number_handler'`, `'sw_dist_root'`, etc.  
**Root Cause:** Pages expect fields from old GUI schema that don't exist in ClientConfig  
**Affected Pages:** Setup, SNHandler, Software  
**Fix Options:**
1. **Add fields to ClientConfig** (if actually needed)
2. **Remove page code** that uses non-existent fields
3. **Map to existing fields** (e.g., serial_number_handler → sn_* fields)

**Recommended Fix:** Option 3 (mapping)
```python
# SNHandler page - instead of:
sn_config = self._config.get("serial_number_handler", {})
sn_type = sn_config.get("type", "WATS Sequential")

# Use:
sn_type = self._config.sn_mode  # Direct attribute access
```
**Complexity:** Medium (1-2 hours, must review each page)

#### C3: ConnectionMonitor Missing Parameter
**Severity:** CRITICAL  
**Symptom:** `TypeError: ConnectionMonitor.__init__() missing required argument: 'check_callback'`  
**Root Cause:** ConnectionMonitor signature changed but main_window.py not updated  
**Location:** [main_window.py#L268](src/pywats_ui/apps/configurator/main_window.py#L268)  
**Fix:**
```python
self._connection_monitor = ConnectionMonitor(
    check_callback=self._check_connection,  # Add this
    check_interval=30
)
```
**Complexity:** Low (5 minutes)

#### C4: Missing Async Event Loop
**Severity:** CRITICAL  
**Symptom:** `RuntimeError: There is no current event loop in thread 'MainThread'`  
**Root Cause:** AsyncAPIRunner tries async operations but no qasync integration  
**Location:** [async_api_runner.py](src/pywats_ui/framework/async_api_runner.py)  
**Fix:** Integrate qasync in main window:
```python
import qasync
app = QApplication(sys.argv)
loop = qasync.QEventLoop(app)
asyncio.set_event_loop(loop)
```
**Complexity:** Medium (30 minutes + testing)

### High Issues (Major Functionality Loss)

#### H1: Serial Number Handler Schema Mismatch
**Pages:** SerialNumberHandlerPage  
**Expected:** Nested dict `serial_number_handler: {type, batch_size, ...}`  
**Actual:** Flat fields `sn_mode, sn_prefix, sn_start, ...`  
**Impact:** Cannot save serial number settings  
**Fix:** Rewrite page to use flat field access

#### H2: Software Distribution Missing Fields
**Pages:** SoftwarePage  
**Expected:** `sw_dist_root`, `sw_dist_chunk_size`  
**Actual:** ❌ Not in ClientConfig  
**Question:** Are these actually needed? Old GUI had them but maybe deprecated?  
**Fix:** Either add fields or remove page features

#### H3: Station Presets Naming Conflict
**Pages:** SetupPage  
**Expected:** `stations` (list)  
**Actual:** `station_presets` (list)  
**Impact:** Multi-station mode won't load/save  
**Fix:** Simple rename in page code

### Medium Issues (Cosmetic/Minor)

#### M1: Type Stub Maintenance
**Impact:** IDE shows wrong signatures  
**Fix:** Add to pre-release checklist

---

## Dependency Graph

### Layer Dependencies (Bottom-Up)

```
Layer 1 (API)
  ↑
Layer 2 (Client Service)
  └─ Depends on: pywats.core.config.APISettings
  └─ Depends on: pywats.PyWATS (for service operations)
  ↑
Layer 3 (UI Framework)
  └─ Depends on: pywats_client.core.config.ClientConfig
  └─ Depends on: pywats_client.service.ClientService (for IPC)
```

**No circular dependencies found.** ✅

### Key Imports

**UI → Client:**
- `from pywats_client.core.config import ClientConfig, ConverterConfig`
- `from pywats_client.core.config_manager import ConfigManager`
- `from pywats_ui.framework import BasePage, QueueManager`

**Client → API:**
- `from pywats import pyWATS, AsyncWATS`
- `from pywats.core.config import APISettings`

---

## Recommendations

### Immediate (Fix Critical Blockers)

1. **Fix Converter Migration** (10 min)
   - Change `run_client_a.py` line 48 to use `ConverterConfig.from_dict()`
   - Apply same fix to `run_client_b.py`

2. **Add ConnectionMonitor Callback** (5 min)
   - Add `check_callback` parameter in main_window.py

3. **Integrate qasync** (30 min)
   - Add to `run_client_a.py` and `run_client_b.py`
   - Test async operations work

### Short-Term (Fix Major Issues)

4. **Map Old Schema to New** (1-2 hours)
   - Create field mapping guide
   - Update all GUI pages to use new field names
   - Test each page's save/load cycle

5. **Add Missing Fields** (30 min - if needed)
   - Decide if `client_id`, `sw_dist_root` are actually required
   - Add to ClientConfig if yes, remove page code if no

### Long-Term (Architecture Improvements)

6. **Integration Tests** (4 hours)
   - Add tests for config save/load cycle
   - Test migration logic
   - Test GUI → Config → File → Config roundtrip

7. **Schema Versioning** (2 hours)
   - Use `schema_version` field for migrations
   - Auto-migrate old configs to new format
   - Never break existing configs

8. **Type Safety** (ongoing)
   - Remove dict-like interface from GUI code
   - Use direct attribute access: `config.service_address`
   - Catch errors at dev time, not runtime

---

## Conclusion

**Architecture Quality:** Solid foundation with clear layer separation. Well-designed dataclass-based config system.

**Migration Quality:** **Poor** - Copy-paste migration without schema adaptation caused critical failures.

**Root Cause:** Pages migrated from old GUI without updating for new ClientConfig schema. Assumed dict-based config would "just work" via dict-like interface, but:
1. Field names changed (stations → station_presets, serial_number_handler → sn_*)
2. Fields removed (client_id, sw_dist_root no longer exist)
3. Type expectations changed (List[dict] → List[ConverterConfig])

**Fix Strategy:** Systematic field mapping + converter migration fix + reliability component completion.

**Estimated Total Fix Time:** 4-6 hours (critical fixes: 1 hour, schema mapping: 2-3 hours, testing: 1-2 hours)

---

## Work Log

**14:35** - Started Layer 1 Analysis (API Layer)  
**14:42** - Analyzed Client Service Layer structure  
**14:48** - Examined UI Framework and pages  
**14:55** - Discovered schema mismatch root cause  
**15:02** - Analyzed old GUI config format  
**15:15** - Completed full stack data flow analysis  
**15:25** - Documented all issues and recommendations  
**15:30** - ✅ Analysis complete

