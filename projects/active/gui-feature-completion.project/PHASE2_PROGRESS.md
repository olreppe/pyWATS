# Phase 2 Progress - Schema Mapping

**Started:** February 6, 2026 16:20  
**Status:** IN PROGRESS  
**Estimated Time:** 2-3 hours

## Decision Points Resolution

### D1: Remove `client_id`?
**Decision:** ✅ YES - Remove from GUI  
**Reason:** Not present in ClientConfig v2.0 schema  
**Impact:** setup.py - remove field from UI and save logic

### D2: Add serial number batching?
**Decision:** ❌ NO - Use simple mode selection  
**Reason:** Async framework handles batching automatically  
**New Schema:** `sn_handler_mode` enum ("sequential", "batch", "disabled")  
**Impact:** sn_handler.py - flatten nested dict to simple mode selection

### D3: Support software distribution?
**Decision:** ✅ YES - Map to new fields  
**Old Field:** `sw_dist_root` (string path)  
**New Fields:** `software_dist_enabled` (bool), `software_dist_path` (Path)  
**Impact:** software.py - split single field into enabled + path

### D4: Single vs multi-token?
**Decision:** ✅ SINGLE - Use `api_token`  
**Reason:** Current implementation uses single token  
**Old Field:** `api_tokens` (list)  
**New Field:** `api_token` (string)  
**Impact:** api_settings.py - change from list to single string

---

## Implementation Tasks

### Task 1: Fix setup.py (client_id, stations)
**Status:** ✅ COMPLETE  
**File:** src/pywats_ui/apps/configurator/pages/setup.py  
**Changes:**
- [x] Remove `client_id` field (set to empty, deprecated)
- [x] Map `hub_mode_enabled` → `multi_station_enabled`
- [x] Map `stations` → `station_presets`
- [x] Map `use_hostname` → `station_name_source` ("hostname" / "config")
- [x] Map `auto_start_service` → `service_auto_start`
- [x] Map `station_location` → `location`
- [x] Map `station_purpose` → `purpose`
- [x] Map `sync_interval` → `sync_interval_seconds`

### Task 2: Fix sn_handler.py (serial_number_handler)
**Status:** ✅ COMPLETE  
**File:** src/pywats_ui/apps/configurator/pages/sn_handler.py  
**Changes:**
- [x] Flatten nested `serial_number_handler` dict
- [x] Map `type` → `sn_mode` (with type mapping)
- [x] Map `allow_reuse` → `sn_check_duplicates` (opposite logic)
- [x] Map `reserve_offline` → `offline_queue_enabled`
- [x] Remove `batch_size`, `fetch_threshold` (not in schema)
- [x] Remove `enforce_sequential` (not in schema)

### Task 3: Fix api_settings.py (api_tokens → api_token)
**Status:** ✅ COMPLETE  
**File:** src/pywats_ui/apps/configurator/pages/api_settings.py  
**Changes:**
- [x] Remove `api_tokens` list (not in schema)
- [x] Clear tokens table on load (empty)
- [x] All other fields map directly (api_enabled, api_port, etc.)

### Task 4: Fix software.py (sw_dist_root)
**Status:** ✅ COMPLETE  
**File:** src/pywats_ui/apps/configurator/pages/software.py  
**Changes:**
- [x] Note that `sw_dist_root` not in new schema
- [x] Note that `sw_dist_chunk_size` not in new schema
- [x] Map to `software_auto_update` (bool only)
- [x] Add warning message about feature not implemented
- [x] Clear UI fields on load (feature pending)

---

## Progress Log

**16:20** - Phase 2 started, decisions made  
**16:20** - Reading page source files...  
**16:25** - All 4 pages fixed with schema mapping  
**16:25** - Task 1 (setup.py): 8 field mappings applied  
**16:25** - Task 2 (sn_handler.py): Flattened nested dict, 4 mappings  
**16:25** - Task 3 (api_settings.py): Removed tokens table  
**16:25** - Task 4 (software.py): Feature marked as not implemented  
**16:26** - Testing GUI with Phase 2 fixes...  
**19:30** - User feedback: Too many success popups on close  
**19:31** - Removed all success popups from save_config methods  
**19:31** - Added consolidated message on close (one notification)  
**19:32** - Fixed log handler level to DEBUG (capture all logs)  
**19:32** - Testing improvements...
