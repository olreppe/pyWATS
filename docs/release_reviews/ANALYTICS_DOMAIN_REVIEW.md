# Analytics Domain - Deep Analysis & Review

**Date:** 2024  
**Scope:** `src/pywats/domains/analytics/`  
**Files Analyzed:**
- `__init__.py` (93 lines)
- `enums.py` (31 lines)
- `models.py` (1802 lines)
- `repository.py` (1004 lines)
- `repository_internal.py` (331 lines)
- `service.py` (829 lines)
- `service_internal.py` (517 lines)

---

## Executive Summary

| Category | Status | Notes |
|----------|--------|-------|
| Architecture Compliance | ✅ PASS | Service → Repository → HttpClient pattern followed |
| Exception Handling | ✅ PASS | Delegated to ErrorHandler, proper validation |
| Documentation Quality | ✅ PASS | Comprehensive docstrings with examples |
| Magic Numbers | ⚠️ MINOR | Default values are documented as parameters |
| Internal API Separation | ✅ PASS | Internal endpoints properly isolated |

---

## 1. Architecture Compliance

### Pattern: Service → Repository → HttpClient

The analytics domain correctly implements the three-layer architecture:

```
┌─────────────────────┐
│  AnalyticsService   │  Business logic, convenience methods
├─────────────────────┤
│ AnalyticsRepository │  Data access, HTTP calls to /api/App/*
├─────────────────────┤
│     HttpClient      │  Raw HTTP communication
└─────────────────────┘
```

**Findings:**

| Component | Compliance | Notes |
|-----------|------------|-------|
| `service.py` | ✅ | All methods delegate to repository |
| `repository.py` | ✅ | Uses `self._client` for HTTP calls |
| `service_internal.py` | ✅ | Uses internal repository for /api/internal/* |
| `repository_internal.py` | ✅ | Properly separated internal API access |

---

## 2. Function Evaluation - service.py (Public API)

| # | Function | Architecture | Exceptions | Documentation | Magic Numbers |
|---|----------|--------------|------------|---------------|---------------|
| 1 | `__init__` | ✅ | ✅ | ✅ | ✅ |
| 2 | `get_version` | ✅ | ✅ | ✅ Good docstring with example | ✅ |
| 3 | `get_processes` | ✅ | ✅ | ✅ Clear purpose and returns | ✅ |
| 4 | `get_levels` | ✅ | ✅ | ✅ Describes production levels | ✅ |
| 5 | `get_product_groups` | ✅ | ✅ | ✅ | ✅ |
| 6 | `get_dynamic_yield` | ✅ | ✅ | ✅ Comprehensive with example | ✅ |
| 7 | `get_dynamic_repair` | ✅ | ✅ | ✅ | ✅ |
| 8 | `get_volume_yield` | ✅ | ✅ | ✅ | ✅ |
| 9 | `get_worst_yield` | ✅ | ✅ | ✅ | ✅ |
| 10 | `get_high_volume` | ✅ | ✅ | ✅ | ✅ |
| 11 | `get_top_failed` | ✅ | ✅ | ✅ Clear model return type | ✅ |
| 12 | `get_test_step_analysis` | ✅ | ✅ | ✅ PREVIEW API noted | ✅ |
| 13 | `get_test_step_analysis_for_operation` | ✅ | ✅ ValueError | ✅ Convenience wrapper documented | ⚠️ See below |
| 14 | `get_related_repair_history` | ✅ | ✅ | ✅ | ✅ |
| 15 | `get_aggregated_measurements` | ✅ | ✅ | ✅ | ✅ |
| 16 | `get_measurements` | ✅ | ✅ | ✅ PREVIEW API noted | ✅ |
| 17 | `get_oee_analysis` | ✅ | ✅ | ✅ OEE formula explained | ✅ |
| 18 | `get_serial_number_history` | ✅ | ✅ | ✅ | ✅ |
| 19 | `get_uut_reports` | ✅ | ✅ | ✅ | ✅ |
| 20 | `get_uur_reports` | ✅ | ✅ | ✅ | ✅ |
| 21 | `get_yield_summary` | ✅ | ✅ | ✅ Helper method documented | ⚠️ `days=30` |
| 22 | `get_station_yield` | ✅ | ✅ | ✅ | ⚠️ `days=7` |

### Magic Number Analysis - service.py

| Function | Value | Assessment |
|----------|-------|------------|
| `get_test_step_analysis_for_operation` | `days=30, max_count=10000` | ✅ ACCEPTABLE - Documented default parameters, reasonable values |
| `get_yield_summary` | `days=30` | ✅ ACCEPTABLE - Documented parameter with sensible default |
| `get_station_yield` | `days=7` | ✅ ACCEPTABLE - Documented parameter, one week is intuitive |

**Verdict:** Default values are proper named parameters, not inline magic numbers.

---

## 3. Function Evaluation - repository.py (Data Access Layer)

| # | Function | Architecture | Exceptions | Documentation | Notes |
|---|----------|--------------|------------|---------------|-------|
| 1 | `__init__` | ✅ | ✅ | ✅ | Initializes HttpClient and ErrorHandler |
| 2 | `get_version` | ✅ | ✅ `handle_response` | ✅ | GET /api/App/Version |
| 3 | `get_processes` | ✅ | ✅ `handle_response` | ✅ | GET /api/App/Processes |
| 4 | `get_levels` | ✅ | ✅ `handle_response` | ✅ | GET /api/App/Levels |
| 5 | `get_product_groups` | ✅ | ✅ `handle_response` | ✅ | GET /api/App/ProductGroups |
| 6 | `get_dynamic_yield` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/DynamicYield |
| 7 | `get_dynamic_repair` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/DynamicRepair |
| 8 | `get_volume_yield` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/VolumeYield |
| 9 | `get_worst_yield` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/WorstYield |
| 10 | `get_high_volume` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/HighVolume |
| 11 | `get_top_failed` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/TopFailed |
| 12 | `get_test_step_analysis` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/TestStepAnalysis |
| 13 | `get_related_repair_history` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/RelatedRepairHistory |
| 14 | `get_aggregated_measurements` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/AggregatedMeasurements |
| 15 | `get_measurements` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/Measurements |
| 16 | `get_oee_analysis` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/OeeAnalysis |
| 17 | `get_serial_number_history` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/SNHistory |
| 18 | `get_uut_reports` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/UutReports |
| 19 | `get_uur_reports` | ✅ | ✅ `handle_response` | ✅ | POST /api/App/UurReports |
| 20 | `_normalize_measurement_path` | ✅ | N/A | ✅ | Static helper method |

**Exception Handling Pattern:**
All repository methods use:
```python
response = self._client.post("/api/App/...", json=params)
data = self._error_handler.handle_response(response, operation="...")
```

This properly delegates error handling to `ErrorHandler` which:
- Maps HTTP 4xx/5xx to appropriate `PyWATSError` subclasses
- Handles STRICT vs LENIENT modes
- Provides consistent error context

---

## 4. Function Evaluation - service_internal.py (Internal API)

| # | Function | Architecture | Exceptions | Documentation | Magic Numbers |
|---|----------|--------------|------------|---------------|---------------|
| 1 | `__init__` | ✅ | ✅ | ✅ | ✅ |
| 2 | `get_unit_flow` | ✅ | ✅ | ✅ ⚠️ INTERNAL API warning | ✅ |
| 3 | `get_flow_nodes` | ✅ | ✅ | ✅ | ✅ |
| 4 | `get_flow_links` | ✅ | ✅ | ✅ | ✅ |
| 5 | `get_flow_units` | ✅ | ✅ | ✅ | ✅ |
| 6 | `trace_serial_numbers` | ✅ | ✅ | ✅ Good usage example | ✅ |
| 7 | `split_flow_by` | ✅ | ✅ | ✅ | ✅ |
| 8 | `set_unit_order` | ✅ | ✅ | ✅ | ✅ |
| 9 | `show_operations` | ✅ | ✅ | ✅ | ✅ |
| 10 | `hide_operations` | ✅ | ✅ | ✅ | ✅ |
| 11 | `expand_operations` | ✅ | ✅ | ✅ | ✅ |
| 12 | `get_bottlenecks` | ✅ | ✅ | ✅ Example shows override | ⚠️ `min_yield_threshold=90.0` |
| 13 | `get_flow_summary` | ✅ | ✅ | ✅ | ⚠️ Inline `0.0` defaults |

### Magic Number Analysis - service_internal.py

| Location | Value | Assessment |
|----------|-------|------------|
| `get_bottlenecks(min_yield_threshold=90.0)` | `90.0` | ✅ ACCEPTABLE - Named parameter with documented purpose |
| `get_flow_summary` | `0.0` defaults | ✅ ACCEPTABLE - Safe fallback for empty yield calculations |

**Note:** The `90.0` threshold is a sensible industry standard default for "minimum acceptable yield". It's exposed as a parameter allowing users to override (as shown in the docstring example with `95.0`).

---

## 5. Function Evaluation - repository_internal.py (Internal Data Access)

| # | Function | Architecture | Exceptions | Documentation | Notes |
|---|----------|--------------|------------|---------------|-------|
| 1 | `__init__` | ✅ | ✅ | ✅ | Uses Referer header for internal API auth |
| 2 | `query_unit_flow` | ✅ | ✅ `handle_response` | ✅ | POST /api/internal/UnitFlow |
| 3 | `get_unit_flow_links` | ✅ | ✅ `handle_response` | ✅ | GET /api/internal/UnitFlow/Links |
| 4 | `get_unit_flow_nodes` | ✅ | ✅ `handle_response` | ✅ | GET /api/internal/UnitFlow/Nodes |
| 5 | `query_unit_flow_by_serial_numbers` | ✅ | ✅ `handle_response` | ✅ | POST /api/internal/UnitFlow/SN |
| 6 | `set_unit_flow_split_by` | ✅ | ✅ `handle_response` | ✅ | POST /api/internal/UnitFlow/SplitBy |
| 7 | `set_unit_flow_order` | ✅ | ✅ `handle_response` | ✅ | POST /api/internal/UnitFlow/UnitOrder |
| 8 | `get_unit_flow_units` | ✅ | ✅ `handle_response` | ✅ | GET /api/internal/UnitFlow/Units |
| 9 | `set_unit_flow_visibility` | ✅ | ✅ `handle_response` | ✅ | POST /api/internal/UnitFlow/SplitBy |

**All internal API calls correctly use the `/api/internal/*` endpoints.**

---

## 6. Model Evaluation - models.py

| Model | Documentation | Field Descriptions | Examples | Notes |
|-------|---------------|-------------------|----------|-------|
| `TopFailedStep` | ✅ | ✅ All fields documented | ✅ | Used for failure analysis |
| `RepairStatistics` | ✅ | ✅ | ✅ | Repair metrics |
| `RepairHistoryRecord` | ✅ | ✅ | ✅ | Historical repair data |
| `MeasurementData` | ✅ | ✅ | ✅ | PREVIEW API noted |
| `AggregatedMeasurement` | ✅ | ✅ | ✅ | Statistical aggregates |
| `OeeAnalysisResult` | ✅ | ✅ | ✅ | OEE formula in docstring |
| `YieldData` | ✅ | ✅ | ✅ | `extra="allow"` for forward compat |
| `ProcessInfo` | ✅ | ✅ | ✅ | Backward compat properties |
| `LevelInfo` | ✅ | ✅ | ✅ | Production levels |
| `ProductGroup` | ✅ | ✅ | ✅ | Product grouping |
| `StepAnalysisRow` | ✅ | Partial | ✅ | PREVIEW API noted |
| `UnitFlowNode` | ✅ | ✅ | ✅ | ⚠️ INTERNAL API warning |
| `UnitFlowLink` | ✅ | ✅ | ✅ | ⚠️ INTERNAL API warning |
| `UnitFlowUnit` | ✅ | ✅ | ✅ | ⚠️ INTERNAL API warning |
| `UnitFlowFilter` | ✅ | ✅ | ✅ | Filter parameters |
| `UnitFlowResult` | ✅ | ✅ | ✅ | Composite result |

**All models use:**
- `PyWATSModel` base class
- `AliasChoices` for camelCase/snake_case conversion
- Proper `Field()` definitions with `description`
- Examples in docstrings

---

## 7. Enum Evaluation - enums.py

| Enum | Values | Documentation |
|------|--------|---------------|
| `YieldDataType` | `FIRST_PASS=1`, `FINAL=2`, `ROLLED=3` | ✅ Clear naming |
| `ProcessType` | `TEST=1`, `REPAIR=2`, `CALIBRATION=3` | ✅ Clear naming |

---

## 8. Internal API Separation

**Verification:**

| Criterion | Status | Evidence |
|-----------|--------|----------|
| Internal endpoints in internal files | ✅ | All `/api/internal/*` calls in `repository_internal.py` |
| Internal service logic separated | ✅ | All Unit Flow logic in `service_internal.py` |
| Warning annotations | ✅ | `⚠️ INTERNAL API - SUBJECT TO CHANGE` in docstrings |
| Module exports | ✅ | `__init__.py` clearly separates public and internal exports |

---

## 9. Exception Handling Summary

### Exception Flow:
```
Repository Method
       │
       ▼
HttpClient.get/post()
       │
       ▼
ErrorHandler.handle_response()
       │
       ├─── HTTP 200 ──► Return data
       ├─── HTTP 404 ──► NotFoundError (STRICT) / None (LENIENT)
       ├─── HTTP 400 ──► ValidationError
       ├─── HTTP 401 ──► AuthenticationError
       ├─── HTTP 403 ──► AuthorizationError
       ├─── HTTP 409 ──► ConflictError
       └─── HTTP 5xx ──► ServerError
```

### Service Layer Validation:
```python
# From service.py - proper validation with clear error message
if not part_number or not part_number.strip():
    raise ValueError("part_number is required and cannot be empty")
if not test_operation or not test_operation.strip():
    raise ValueError("test_operation is required and cannot be empty")
```

---

## 10. Recommendations

### Minor Improvements (Low Priority)

1. **Consider extracting defaults to constants:**
   ```python
   # Instead of inline defaults:
   DEFAULT_DAYS_LOOKBACK = 30
   DEFAULT_MAX_RESULTS = 10000
   DEFAULT_MIN_YIELD_THRESHOLD = 90.0
   ```
   However, current implementation is acceptable as values are named parameters with documentation.

2. **StepAnalysisRow fields:** Some fields lack individual `description` parameter. Low priority as the class docstring covers them.

---

## 11. Overall Assessment

### Compliance Matrix

| Category | Rating | Score |
|----------|--------|-------|
| Architecture | Excellent | 10/10 |
| Exception Handling | Excellent | 10/10 |
| Documentation | Excellent | 9/10 |
| Magic Numbers | Good | 8/10 |
| Internal Separation | Excellent | 10/10 |

### Final Verdict: ✅ APPROVED

The analytics domain demonstrates excellent adherence to the pyWATS architecture patterns. All functions properly delegate through the Service → Repository → HttpClient layers, exception handling is consistently applied via the ErrorHandler, and documentation includes comprehensive docstrings with practical examples.

The use of default values for parameters like `days=30` or `min_yield_threshold=90.0` is acceptable as these are:
1. Named parameters (not inline literals)
2. Documented in docstrings
3. Overridable by users
4. Sensible industry-standard defaults

---

*Document generated from deep analysis of analytics domain source code.*
