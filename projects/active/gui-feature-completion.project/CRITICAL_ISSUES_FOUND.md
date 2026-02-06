# Critical Issues Found in New GUI

**Date:** February 6, 2026  
**Status:** BLOCKING  
**Discovered During:** Config migration testing

---

## Summary

Multiple critical issues prevent the new GUI from functioning properly. Issues span configuration schema mismatches, converter migration bugs, and async/reliability component failures.

---

## 🔴 CRITICAL Issues

### 1. Config Schema Mismatches (CRITICAL)

GUI pages attempting to save fields that don't exist in `ClientConfig`:

**Missing Fields:**
- `client_id` - Used in setup.py:367
- `serial_number_handler` - Used in sn_handler.py:183  
- `api_tokens` - Used in api_settings.py:391
- `sw_dist_root` - Used in software.py:193

**Error Pattern:**
```python
KeyError: "Invalid config key: 'XXX'. Key not found in ClientConfig schema. Use only defined config fields."
```

**Impact:** Users cannot save page configurations. All settings are lost on GUI close.

**Root Cause:** GUI pages were built against Old GUI config schema which had different fields than new ClientConfig dataclass.

---

### 2. Converter Migration Type Bug (CRITICAL)

**Issue:** When migrating converters from old config, they're stored as plain `dict` objects instead of `ConverterConfig` dataclass instances.

**Error:**
```
AttributeError: 'dict' object has no attribute 'to_dict'
  File "src/pywats_client/core/config.py", line 962, in to_dict
    "converters": [c.to_dict() for c in self.converters],
```

**Impact:** Config cannot be saved when old converters are migrated. Affects all pages on close.

**Fix Required:** Convert dict to ConverterConfig objects during migration

---

### 3. ConnectionMonitor Missing Callback (HIGH)

**Error:**
```
ConnectionMonitor.__init__() missing 1 required positional argument: 'check_callback'
```

**File:** main_window.py - reliability components initialization  
**Impact:** Connection monitoring doesn't work, no reconnection attempts

---

### 4. Async Event Loop Issues (HIGH)

**Error 1:**
```
RuntimeError: There is no current event loop in thread 'MainThread'
```

**Error 2:**
```
RuntimeWarning: coroutine 'ConnectionPage._run_connection_test' was never awaited
```

**Impact:** Connection testing and async API operations don't work  
**Root Cause:** No qasync integration, Qt event loop doesn't support asyncio

---

## 📊 Testing Results

**Configurator GUI (Instance A):**
- ✅ Launches successfully
- ✅ Config migration attempted
- ❌ Cannot save any page configurations (schema mismatches)
- ❌ Connection monitoring fails (missing callback)
- ❌ Async operations fail (no event loop)
- ❌ Crashes on close (converter to_dict() error)

**Status:** PARTIALLY FUNCTIONAL (display only, cannot persist changes)

---

## 🔍 Affected Files

**Config Issues:**
- `src/pywats_ui/apps/configurator/pages/setup.py:367`
- `src/pywats_ui/apps/configurator/pages/sn_handler.py:183`
- `src/pywats_ui/apps/configurator/pages/api_settings.py:391`
- `src/pywats_ui/apps/configurator/pages/software.py:193`

**Migration Issues:**
- `run_client_a.py` - migrate_old_config()
- `run_client_b.py` - migrate_old_config()

**Reliability Issues:**
- `src/pywats_ui/apps/configurator/main_window.py` - ConnectionMonitor init
- `src/pywats_ui/apps/configurator/pages/connection.py` - async operations

---

## 💡 Required Fixes

### Priority 1 (IMMEDIATE - Blocking)
1. **Add missing fields to ClientConfig** or **update GUI pages to use correct fields**
2. **Fix converter migration** - convert dicts to ConverterConfig objects
3. **Fix ConnectionMonitor initialization** - provide check_callback

### Priority 2 (HIGH - Feature blocking)
4. **Integrate qasync** for async operation support
5. **Implement connection test** properly with event loop
6. **Complete QueueManager send callback** for report submission

---

## 📝 Analysis Required

These issues suggest that:
1. **GUI pages were copied from Old GUI** without adapting to new config schema
2. **No integration tests** exist for config save/load cycle
3. **Reliability components** were added but not fully integrated
4. **Async support** was planned but not implemented

**Recommendation:** Need full architecture audit to identify all schema/interface mismatches.

---

**Created:** February 6, 2026  
**Last Updated:** February 6, 2026 14:30
