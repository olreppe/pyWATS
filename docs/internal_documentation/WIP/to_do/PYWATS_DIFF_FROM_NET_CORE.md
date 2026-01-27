# pyWATS vs .NET Core Client Comparison

**Date:** 2026-01-26  
**Last Reviewed:** 2026-01-27  
**Status:** ✅ Reviewed - 3 Low/Medium Priority Action Items  
**Reference:** `referenced_code_net_core/` folder

---

## Status Summary (2026-01-27)

**Review Complete:** pyWATS is well-aligned with modern .NET Core client.

**Key Findings:**
- ✅ **Architecture aligned** - REST, async, domain structure all match
- ✅ **pyWATS is better** in type safety, documentation, error handling, and analytics
- ⚠️ **3 Optional enhancements identified** - See Action Items section below
- ❌ **Workflow module** - Deprecated in .NET, will not implement

**Action Items:** See ROADMAP.md for prioritized implementation plan

---

## Overview

This document compares the current pyWATS Python implementation against the modern .NET Core WATS Client (`referenced_code_net_core/`). The .NET Core client represents the latest C# implementation and has fully migrated from WCF to REST.

---

## Architecture Alignment

### REST API Migration ✅ ALIGNED

The .NET Core version has fully migrated from WCF to REST:
- `WatsRestAPI.cs` is auto-generated from Swagger/NSwag (8598 lines)
- Uses `HttpClient` with JSON serialization everywhere
- Old WCF config files marked as deprecated/obsolete

**pyWATS Status:** ✅ Already REST-based from the start

---

### Async-First Design ✅ ALIGNED

The .NET Core client uses `async/await` throughout:
```csharp
public async Task<string> VersionAsync(CancellationToken cancellationToken)
```

**pyWATS Status:** ✅ We have both sync and async versions (`AsyncWATS`, `pyWATS`) plus `run_sync()` utility

---

### Domain Structure ✅ ALIGNED

.NET Core `MesInterface` structure maps to pyWATS domains:

| .NET Core | pyWATS |
|-----------|--------|
| `Production` | `production` domain |
| `Product` | `product` domain |
| `Software` | `software` domain |
| `Asset` (AssetHandler) | `asset` domain |
| `Workflow` | ❌ Deprecated - not migrating |

---

## Gaps to Address

### 1. Local Caching Pattern ⚠️ CONSIDER

**What .NET Core Does:**

The .NET client caches key data locally for offline resilience:

```csharp
// Processes.cs
internal const string processesFilename = "Processes.json";

internal void Load() 
{
    // Load from local cache file
    using (var txtreader = new StreamReader(Path.Combine(_api.DataDir, processesFilename)))
    {
        var reader = new JsonTextReader(txtreader);
        _processes = serializer.Deserialize<Process[]>(reader).ToDictionary(p => p.Code);
    }
}

internal void Get(bool save = true) 
{
    // Get from server, then save to cache
    _processes = proxy.GetJson<Process[]>(cApiGetProcesses);
    if (save) Save();
}
```

Cached files:
- `Processes.json` - Operation types, repair types
- `ClientInfo.json` - Station info, site codes

**pyWATS Status:** ❌ Not implemented

**Recommendation:**
- Add to `pywats_client` for offline scenarios
- Cache processes/operations on first connection
- Use cached data when server unavailable
- Priority: **MEDIUM** - valuable for client service reliability

**Implementation Location:** `src/pywats_client/core/cache.py`

---

### 2. ValidationMode Setting ⚠️ CONSIDER

**What .NET Core Does:**

```csharp
public ValidationModeType ValidationMode { get; set; }

internal string SetPropertyValidated<Type>(string propertyName, string newValue, ...)
{            
    int maxLen = Utilities.GetMaxLengthFromAttribute<Type>(propertyName);
    if (maxLen > 0 && newValue.Length > maxLen)
    {
        if (ValidationMode == ValidationModeType.ThrowExceptions)
            throw new ArgumentException(...);
        else
            newValue = newValue.Substring(0, maxLen);  // Truncate silently
    }
    return newValue;
}
```

Two modes:
- `ThrowExceptions` - Strict, throws on invalid data
- `TruncateAndContinue` - Lenient, auto-truncates strings

**pyWATS Status:** ❌ Always strict (throws)

**Recommendation:**
- Add `strict_validation: bool = True` config option
- When `False`, truncate strings instead of throwing
- Useful for converters processing messy data
- Priority: **LOW** - current strict mode is generally preferred

**Implementation Location:** `src/pywats/core/config.py`

---

### 3. Unit History Details Flag ⚠️ VERIFY

**What .NET Core Does:**

```csharp
public List<UnitHistory> GetUnitHistory(
    string serialNumber, 
    string partNumber = null, 
    bool details = false  // Include info/error messages
)
```

**pyWATS Status:** ⚠️ May be missing the `details` parameter

**Action:** Verify `production.get_unit_reports()` supports the `details` parameter

---

## Already Better in pyWATS ✅

### 1. Type Safety
- Full Pydantic models with validation
- .NET Core uses loose dictionaries in many places
- AliasChoices for camelCase/snake_case compatibility

### 2. Documentation
- Comprehensive docstrings with Args/Returns/Raises/Examples
- .NET Core has basic XML comments

### 3. Error Handling
- Unified `ErrorHandler` pattern across all domains
- Custom exception hierarchy (`WATSError`, `ValidationError`, etc.)
- .NET Core has ad-hoc try/catch patterns

### 4. Analytics Domain
- Much richer than .NET client's basic `Statistics` classes
- OEE analysis, dynamic yield, measurement statistics
- Alarm logs API (recently added)

### 5. Async Support
- `run_sync()` utility for mixed sync/async code
- Context managers for both sync and async
- .NET Core async is more basic

### 6. Report Models
- UUTReport and UURReport with full validation
- Step builders with fluent API
- Recent UURReport refactoring (644→426 lines)

---

## No Changes Needed ✅

| Feature | Status | Notes |
|---------|--------|-------|
| REST transport | ✅ Aligned | Both use HTTP/JSON |
| Asset module | ✅ Better | pyWATS has 25.3 additions |
| Report submission | ✅ Aligned | Online/offline/automatic modes |
| Software distribution | ✅ Aligned | Core API covered, GUI is desktop-specific |
| Production tracking | ✅ Aligned | Unit lifecycle, serial numbers |
| Process configuration | ✅ Aligned | Operation types, repair types |

---

## Deprecated - Not Migrating ❌

### Workflow Module

The .NET Core client has a `Workflow` module:
```csharp
public WorkflowResponse StartTest(...)
public WorkflowResponse EndTest(...)
public WorkflowResponse Validate(...)
public WorkflowResponse Initialize(...)
public WorkflowResponse CheckIn(...)
```

**Decision:** ❌ **DEPRECATED** - Will not be migrated to pyWATS

---

## Action Items

### High Priority
- [ ] None identified

### Medium Priority
- [ ] Investigate local caching for `pywats_client` offline scenarios
- [ ] Verify `details` parameter in `get_unit_history()` / `get_unit_reports()`

### Low Priority
- [ ] Consider `strict_validation` config option for lenient mode

---

## Reference Files

Key .NET Core files reviewed:

| File | Purpose |
|------|---------|
| `Interface.TDM/TDM.cs` | Main TDM API class (2096 lines) |
| `Interface.TDM/MES.cs` | MES interface facade |
| `Interface.MES/WatsRestAPI.cs` | Auto-generated REST client (8598 lines) |
| `Interface.MES/Asset/AssetHandler.cs` | Asset management (469 lines) |
| `Interface.MES/Production/Production.cs` | Production tracking (560 lines) |
| `Interface.MES/Software/Software.cs` | Software distribution (957 lines) |
| `Interface.TDM/Processes.cs` | Process caching pattern |
| `Interface.TDM/UUTClasses/UUTReport.cs` | UUT report builder (573 lines) |
| `Interface.TDM/UURClasses/UURReport.cs` | UUR report builder (374 lines) |
| `Contract.MES/*.cs` | Service contracts and entities |

---

## Conclusion

The pyWATS implementation is well-aligned with the modern .NET Core client. Key differences are:

1. **pyWATS is better** in type safety, documentation, error handling, and analytics
2. **Consider adding** local caching for offline resilience in pywats_client
3. **Workflow is deprecated** and will not be implemented
4. **No major gaps** in core functionality

The .NET Core reference validates our architecture choices and confirms we're on the right track.

---

**Last Updated:** 2026-01-26  
**Reviewer:** AI Assistant
