# pyWATS Development Roadmap

**Generated:** 2026-01-27  
**Last Updated:** 2026-01-27  
**Purpose:** Prioritized task list from to_do folder analysis

---

## Executive Summary

### Documentation Review Status

| Document | Status | Outcome |
|----------|--------|---------|
| `ASSET_MODULE_UPDATE.md` | ✅ **Complete** | Moved to `completed/` - All WATS 25.3 features implemented |
| `TARGET_PLATFORM_IMPLEMENTATION_PLAN.md` | ✅ **Complete** | Moved to `completed/` - All 4 deployment phases done |
| `TESTING_WITHOUT_HARDWARE.md` | 📚 **Reference** | Moved to `next_up/` - Comprehensive testing guide (not actionable tasks) |
| `PYWATS_DIFF_FROM_NET_CORE.md` | ⚠️ **3 Action Items** | Medium/Low priority enhancements |
| `IPC_CFX_ARCHITECTURE.md` | 💡 **Future Project** | Architecture study complete - separate project when needed |
| `ADDITIONAL_STANDARD_CONVERTERS.md` | ✅ **Complete** | All planned converters implemented |

### Completed Work

✅ **WATS 25.3 Asset Module Enhancements** (Fully Implemented)
- External calibration API (`record_calibration_external`)
- External maintenance API (`record_maintenance_external`)
- Direct count manipulation (`set_running_count`, `set_total_count`, `reset_running_count`)
- Documentation, tests, and examples complete

✅ **Platform Deployment** (All 4 Phases Complete)
- Phase 1: Windows Server/IoT hardening (service recovery, event log, pre-shutdown)
- Phase 2: Ubuntu LTS (DEB packages, systemd security hardening, health endpoint)
- Phase 3: Enterprise Linux (RPM packages, SELinux policy)
- Phase 4: Docker & VM (multi-arch containers, Packer templates, first-boot wizard)

✅ **Standard Converters**
- Keysight TestExec SL converter implemented
- STDF dropped (semiconductor only - out of scope)
- All industry-standard formats covered (ATML, Teradyne, SPEA, Seica, XJTAG, Klippel)

---

## Priority 1: Critical / High-Value

### No Critical Items

All critical features are implemented. No blocking issues identified.

---

## Priority 2: Medium - Enhanced Reliability

### 1. Client-Side Local Caching for Offline Resilience

**Status:** ⚠️ Not Implemented  
**Priority:** Medium  
**Effort:** 1-2 weeks  
**Source:** `PYWATS_DIFF_FROM_NET_CORE.md`

**Background:**
The .NET Core client caches key data locally for offline resilience:
- Process definitions (operation types, repair types)
- Station configuration
- Falls back to cache when server unavailable

**Current Gap:**
pyWATS client has no local cache - requires server connectivity for all operations.

**Implementation:**
```
src/pywats_client/core/cache.py
├── ProcessCache
│   ├── load_from_file()
│   ├── save_to_file()
│   └── get_with_fallback()
├── ConfigCache
│   ├── cache_station_info()
│   └── get_cached_config()
└── CacheManager
    ├── initialize()
    ├── refresh()
    └── get_cache_status()
```

**Benefits:**
- Client service continues during brief server outages
- Faster startup (no blocking API calls)
- Better offline queue handling

**Acceptance Criteria:**
- [ ] Cache process definitions on first connect
- [ ] Load from cache if server unavailable
- [ ] Auto-refresh cache periodically (configurable interval)
- [ ] Clear cache on API token change
- [ ] Cache location configurable
- [ ] Unit tests with mock server outages

**Related Files:**
- `.NET reference: referenced_code_net_core/Interface.TDM/Processes.cs`
- Implementation: `src/pywats_client/core/cache.py`
- Tests: `tests/client/test_cache.py`

---

## Priority 3: Low - Nice to Have

### 2. Verify `details` Parameter in `get_unit_reports()`

**Status:** ⚠️ Needs Verification  
**Priority:** Low  
**Effort:** 1-2 hours  
**Source:** `PYWATS_DIFF_FROM_NET_CORE.md`

**Background:**
.NET Core client has a `details` parameter in `GetUnitHistory()`:
```csharp
List<UnitHistory> GetUnitHistory(
    string serialNumber,
    string partNumber = null,
    bool details = false  // Include info/error messages
)
```

**Action Required:**
- [ ] Check if pyWATS `production.get_unit_reports()` supports `details` parameter
- [ ] If missing, add it with proper documentation
- [ ] Add integration test

**Files to Check:**
- `src/pywats/domains/production/async_service.py`
- `src/pywats/domains/production/async_repository.py`
- `docs/domains/production.md`

---

### 3. Strict Validation Mode Configuration Option

**Status:** ⚠️ Not Implemented  
**Priority:** Low  
**Effort:** 2-3 days  
**Source:** `PYWATS_DIFF_FROM_NET_CORE.md`

**Background:**
.NET Core client has two validation modes:
- **ThrowExceptions** (strict) - Current pyWATS behavior
- **TruncateAndContinue** (lenient) - Auto-truncates strings that exceed max length

**Current Behavior:**
pyWATS always throws exceptions on validation errors.

**Use Case:**
Converters processing messy data from legacy systems may benefit from auto-truncation
instead of failing entirely.

**Implementation:**
```python
# config.py
class WATSConfig:
    strict_validation: bool = True  # Default to strict
    
# models.py
class BaseModel(pydantic.BaseModel):
    def validate_string_length(self, value: str, max_length: int) -> str:
        if len(value) > max_length:
            if get_config().strict_validation:
                raise ValidationError(f"String exceeds max length {max_length}")
            else:
                return value[:max_length]  # Truncate silently
        return value
```

**Acceptance Criteria:**
- [ ] Add `strict_validation` config option
- [ ] Apply to string length validation
- [ ] Document behavior in converter guide
- [ ] Add tests for both modes

**Note:** Current strict mode is generally preferred. Only implement if specific customer need arises.

---

## Priority 4: Future Projects

### 4. IPC-CFX Integration (Separate Project)

**Status:** 💡 Architecture Study Complete  
**Priority:** Future (when customer demand exists)  
**Effort:** 6-9 weeks  
**Source:** `IPC_CFX_ARCHITECTURE.md`

**Background:**
IPC-CFX (IPC-2591) is a real-time factory connectivity standard for equipment-to-equipment
and equipment-to-MES communication via AMQP message broker.

**Key Finding:** CFX is NOT a file converter - it's a real-time event system.

**Recommended Approach:**
Create separate integration project: **pywats_cfx**

```
pywats_cfx/
├── amqp_client.py       # RabbitMQ/ActiveMQ connection
├── cfx_models.py        # CFX message schemas
├── handlers/
│   ├── report_handler.py    # UnitsTested → WATS Report
│   ├── asset_handler.py     # Maintenance → WATS Asset
│   └── product_handler.py   # MaterialsInstalled → WATS BOM
└── config.py
```

**Implementation Phases:**
1. **Phase 1:** Core AMQP infrastructure + TestHandler (2-3 weeks)
2. **Phase 2:** Domain handlers (Asset, Product, Production) (2-3 weeks)
3. **Phase 3:** Bidirectional integration (2-3 weeks)

**When to Implement:**
- Customer specifically requests CFX integration
- Multiple customers using CFX-compatible equipment
- Strategic partnership with CFX equipment vendor

**Documentation:** See `IPC_CFX_ARCHITECTURE.md` for complete analysis

---

### 5. Windows MSI Installer

**Status:** 💡 Planned (Stretch Goal)  
**Priority:** Future  
**Effort:** 2-3 weeks  
**Source:** `TARGET_PLATFORM_IMPLEMENTATION_PLAN.md`

**Background:**
IT departments prefer MSI packages for GPO deployment. Currently only pip install available.

**Options:**
- **cx_Freeze** - Bundle Python + pyWATS into single installer
- **PyInstaller** - Alternative bundler
- **WiX Toolset** - Create proper MSI with upgrade support
- **NSIS** - Lighter-weight installer option

**Scope:**
- [ ] Bundle Python 3.11 + pyWATS + dependencies
- [ ] Silent install support
- [ ] Service registration
- [ ] Upgrade handling (preserve config)
- [ ] Clean uninstall (optional config preservation)
- [ ] GPO deployment testing

**When to Implement:**
- Multiple enterprise customers request MSI
- Customer has GPO deployment mandate
- Security policies require signed installers

---

### 6. Windows IoT LTSC Field Testing

**Status:** 💡 Documentation Complete, Testing Pending  
**Priority:** Future  
**Effort:** 1-2 weeks  
**Source:** `TARGET_PLATFORM_IMPLEMENTATION_PLAN.md`

**Background:**
Full installation guide exists (`docs/platforms/windows-iot-ltsc.md`) but not field-tested
on actual Windows 10/11 IoT Enterprise LTSC hardware.

**Testing Needed:**
- [ ] Create IoT LTSC 2021 test VM
- [ ] Test with Write Filter (UWF) enabled
- [ ] Test with Embedded Lockdown Manager
- [ ] Test with AppLocker policies
- [ ] Verify service survives LTSC updates
- [ ] Document any additional workarounds

**When to Implement:**
- Customer deploys to IoT LTSC environment
- Pre-sales POC for IoT/embedded customer

---

## Recently Completed (Reference)

### ✅ WATS 25.3 Asset Module (Dec 2025 Release)

**Completed:** 2026-01-26  
**Effort:** ~2 days  
**Implementation:**

All new endpoints from WATS 25.3 release:
- `POST /api/Asset/Calibration/External` → `record_calibration_external()`
- `POST /api/Asset/Maintenance/External` → `record_maintenance_external()`
- `PUT /api/Asset/SetRunningCount` → `set_running_count()`
- `PUT /api/Asset/SetTotalCount` → `set_total_count()`
- `POST /api/Asset/ResetRunningCount` → `reset_running_count()`

**Files Created/Modified:**
- `src/pywats/domains/asset/async_repository.py` - Added 4 new endpoints
- `src/pywats/domains/asset/async_service.py` - Added service methods
- `src/pywats/domains/asset/service.py` - Added sync wrappers
- `src/pywats/domains/asset/enums.py` - Added `IntervalMode` enum
- `src/pywats/core/routes.py` - Added route constants
- `docs/domains/asset.md` - Updated with examples
- `examples/asset/calibration.py` - Added external calibration examples
- `examples/asset/maintenance.py` - Added external maintenance examples
- `tests/domains/asset/test_integration.py` - Added integration tests
- `CHANGELOG.md` - Documented changes

---

### ✅ Platform Deployment Infrastructure (Complete)

**Completed:** 2026-01-26  
**Total Effort:** ~6 weeks  

**Phase 1: Windows Server/IoT Hardening**
- Service recovery options
- Event Log integration
- Pre-shutdown notification
- Silent install mode
- Windows IoT LTSC documentation

**Phase 2: Ubuntu LTS**
- DEB package structure (`debian/` folder)
- systemd security hardening
- HTTP health endpoint for monitoring
- Headless mode verification

**Phase 3: Enterprise Linux**
- RPM spec file (`rpm/pywats.spec`)
- SELinux policy module (`selinux/`)
- RHEL 8/9 compatibility

**Phase 4: Docker & VM**
- Multi-architecture builds (amd64, arm64)
- GitHub Container Registry integration
- Packer templates for VM appliances
- First-boot configuration wizard
- Security scanning (Trivy)

**Files Created:**
- `deployment/debian/` - Full DEB package structure (8 files)
- `deployment/rpm/` - RPM spec and systemd units (3 files)
- `deployment/selinux/` - SELinux policy (3 files)
- `deployment/packer/` - VM appliance templates (5 files)
- `deployment/docker/` - Moved from root
- `.github/workflows/docker.yml` - Multi-arch CI/CD
- `docs/platforms/windows-iot-ltsc.md` - Installation guide
- `src/pywats_client/service/health_server.py` - HTTP health endpoint

---

### ✅ Keysight TestExec SL Converter

**Completed:** 2026-01-26  
**Effort:** ~2 days  

**Implementation:**
- File: `src/pywats_client/converters/standard/keysight_testexec_sl_converter.py`
- Lines: ~700
- Supports multiple XML root elements and namespaces
- Test mapping to `NumericLimitStep` and `PassFailStep`
- Configurable operation types and options

**Other Converter Decisions:**
- ❌ **STDF dropped** - Semiconductor wafer testing out of WATS scope
- ✅ **All industry formats covered** - ATML, Teradyne, SPEA, Seica, XJTAG, Klippel

---

## Development Guidelines

### When to Add to Roadmap

Add new items when:
- Customer specifically requests feature
- Multiple customers report same need
- Strategic value identified (competitive advantage, market expansion)
- Technical debt identified (performance, security, maintainability)

### Priority Levels

| Priority | Description | Typical Timeframe |
|----------|-------------|-------------------|
| **P1: Critical** | Blocking issue, data loss risk, security vulnerability | Immediate |
| **P2: High** | Customer-blocking, significant pain point | Next sprint |
| **P3: Medium** | Quality of life, reliability improvement | Next quarter |
| **P4: Low** | Nice to have, minor enhancement | Backlog |
| **Future** | Worthwhile but no immediate demand | When needed |

### Effort Estimates

| Estimate | Typical Scope |
|----------|---------------|
| Hours | Bug fix, small enhancement |
| Days | New feature, minor refactor |
| Weeks | Major feature, new domain |
| Months | New product, major architecture change |

---

## Related Documentation

### Completed Plans (Reference)
- [`completed/ASSET_MODULE_UPDATE_PLAN.md`](../completed/ASSET_MODULE_UPDATE_PLAN.md) - WATS 25.3 implementation
- [`completed/TARGET_PLATFORM_IMPLEMENTATION_PLAN.md`](../completed/TARGET_PLATFORM_IMPLEMENTATION_PLAN.md) - Deployment phases

### Reference Guides
- [`next_up/TESTING_WITHOUT_HARDWARE.md`](../next_up/TESTING_WITHOUT_HARDWARE.md) - Testing strategies
- [`IPC_CFX_ARCHITECTURE.md`](./IPC_CFX_ARCHITECTURE.md) - CFX integration design

### Gap Analysis
- [`PYWATS_DIFF_FROM_NET_CORE.md`](./PYWATS_DIFF_FROM_NET_CORE.md) - .NET Core comparison

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-27 | Initial roadmap created from to_do folder analysis | AI Assistant |
| 2026-01-27 | Moved ASSET_MODULE_UPDATE to completed | AI Assistant |
| 2026-01-27 | Moved TARGET_PLATFORM_IMPLEMENTATION_PLAN to completed | AI Assistant |
| 2026-01-27 | Moved TESTING_WITHOUT_HARDWARE to next_up | AI Assistant |

---

## Summary

### Current State

**✅ Strong Foundation:**
- All critical WATS 25.3 features implemented
- Comprehensive platform deployment support (Windows, Linux, Docker, VM)
- Full converter coverage for industry-standard formats
- Better than .NET Core in many areas (type safety, documentation, analytics)

**⚠️ Medium-Priority Enhancements:**
- Local caching for offline resilience (1-2 weeks)
- Validation mode configuration (2-3 days)
- Unit history details parameter verification (hours)

**💡 Future Projects (When Needed):**
- IPC-CFX integration (6-9 weeks, architecture complete)
- Windows MSI installer (2-3 weeks)
- Windows IoT LTSC field testing (1-2 weeks)

### Recommended Next Steps

1. **Immediate:** Nothing critical - all blocking issues resolved
2. **Next Quarter:** Consider local caching if customer offline scenarios increase
3. **When Requested:** IPC-CFX integration, MSI installer, IoT LTSC testing

### Health Assessment

🟢 **Excellent** - Production-ready with comprehensive feature set. All planned work complete.
Optional enhancements identified for future consideration based on customer demand.
