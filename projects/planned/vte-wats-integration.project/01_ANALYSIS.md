# VTE → WATS Integration - Analysis

**Date:** 2026-02-02  
**Author:** Integration Team

---

## Problem Statement

Manufacturing sites using **Keysight VTE** (VEE Test Executive) for production testing need automated upload of test results to WATS. Currently:
- VTE stores results in SQL Server (21 tables, complex schema)
- No official WATS integration exists for VTE
- Sites manually export or build custom, fragile scripts
- Result data fragmented across TestDataNumeric, TestDataText, TestDataOther tables

**Goal:** Build a supported, production-ready VTE → WATS adapter.

---

## Requirements

### Functional Requirements

1. **Data Extraction**
   - Connect to VTE 9.3x SQL Server database (Windows Auth or SQL Auth)
   - Extract test runs from `IndexData` table (execution header)
   - Join with `UutData`, `TestData*`, optionally `RepairData`
   - Support incremental sync via `IndexData.Timestamp`

2. **Data Mapping**
   - Map VTE entities to WATS model:
     - `Products` → WATS Product
     - `Testplans` + `TestplanRevisions` → WATS Process + Version
     - `IndexData` → WATS Report (UUT)
     - `TestDataNumeric/Text/Other` → WATS Step Results
     - `UutData.Serial` → WATS Unit Serial Number
   - Handle pass/fail status from VTE results
   - Preserve test execution timestamp (timezone-aware)

3. **Idempotency**
   - Use `IndexData.Index_GUID` as unique key
   - Store mapping in WATS (source="VTE", source_id=Index_GUID)
   - Skip re-upload of already-processed runs

4. **Repair Data (Optional)**
   - Extract repair sessions from `RepairData`, `RepairActions`
   - Map to WATS UUR (Unit Under Repair) if applicable
   - Include repair codes, actions, syndromes

5. **Deployment**
   - Run as Windows Service or scheduled task
   - Configuration file (DB connection, WATS API endpoint)
   - Logging to file + console
   - Health check endpoint or status reporting

### Non-Functional Requirements

- **Performance:** Process 1000+ test runs per hour
- **Reliability:** Automatic retry on transient failures
- **Security:** Read-only DB access, never export VTE user passwords
- **Maintainability:** Clear logging, error messages, configuration validation
- **Compatibility:** Support VTE 9.3x (9.31.1 tested), potentially 9.2x with schema checks

---

## Constraints

1. **Schema Variations:** VTE schema may differ across installations (9.3x vs 9.2x)
2. **Database Access:** Requires SQL Server permissions (read-only sufficient)
3. **WATS API:** Must use pyWATS or direct WATS REST API
4. **Timezone:** VTE timestamps may be local server time, need clarification
5. **Large Data:** Some sites may have millions of historical rows

---

## Technical Approach

### Architecture: .NET Service + pyWATS Upload

**Option A: .NET Adapter (Recommended)**
- **Pros:** Native SQL Server integration, Dapper for performance, Windows Service deployment
- **Cons:** Separate codebase from pyWATS

**Option B: Python + pyodbc**
- **Pros:** Single-language stack with pyWATS
- **Cons:** pyodbc/Windows drivers can be brittle, slower than native .NET

**Decision:** Use **.NET 8 console app** for extraction + **pyWATS** for upload.

```
VTE SQL Server → .NET Adapter (Dapper) → JSON/HTTP → pyWATS → WATS API
```

### Data Model

**VTE Entities (Source):**
```csharp
public class VteTestRun
{
    public Guid IndexGuid { get; set; }           // Unique key
    public DateTime Timestamp { get; set; }       // Execution time
    public string Serial { get; set; }            // UUT serial
    public string ProductName { get; set; }
    public string TestplanName { get; set; }
    public string TestplanRevision { get; set; }
    public string TestsystemName { get; set; }
    public string OperatorName { get; set; }
    public bool Passed { get; set; }
    
    public List<VteStepResult> StepResults { get; set; }
}

public class VteStepResult
{
    public string StepName { get; set; }
    public string StepType { get; set; }  // Numeric, Text, Other
    public double? NumericValue { get; set; }
    public double? LowerLimit { get; set; }
    public double? UpperLimit { get; set; }
    public string TextValue { get; set; }
    public bool Passed { get; set; }
}
```

**WATS Mapping:**
- `VteTestRun` → `Report` (UUT report)
- `VteStepResult` → `StepResult` with appropriate limits/values
- Product/Process from VTE master tables

### Extraction Strategy

**Incremental Sync:**
```sql
SELECT *
FROM IndexData i
JOIN UutData u ON i.Uut_GUID = u.Uut_GUID
WHERE i.Timestamp > @LastSyncTimestamp
ORDER BY i.Timestamp ASC
```

**Watermark Persistence:**
- Store last sync timestamp in local config file or database
- Use guard band (re-read last 10 minutes) to handle late-arriving data

**Batching:**
- Process 100-1000 runs per batch
- Commit watermark after successful WATS upload

### Idempotency Implementation

**In .NET Adapter:**
1. Query IndexData with timestamp filter
2. For each run, generate stable ID: `VTE:{Index_GUID}`
3. Before upload, check if already in WATS (via source_id)
4. Skip if exists, upload if new

**In WATS:**
- Store `source="VTE"`, `source_id="{Index_GUID}"` in report metadata
- Use WATS API search/query to check existence

### Step Results Normalization

VTE stores results across 3 tables:
- `TestDataNumeric`: measured values + limits
- `TestDataText`: string results
- `TestDataOther`: binary/unknown

**Normalization Query:**
```sql
-- Get all step results for a run
SELECT 
    'Numeric' AS StepType,
    StepName,
    MeasuredValue,
    LowerLimit,
    UpperLimit,
    NULL AS TextValue
FROM TestDataNumeric
WHERE Index_GUID = @IndexGuid

UNION ALL

SELECT
    'Text' AS StepType,
    StepName,
    NULL,
    NULL,
    NULL,
    TextResult
FROM TestDataText
WHERE Index_GUID = @IndexGuid

UNION ALL

SELECT
    'Other' AS StepType,
    StepName,
    NULL,
    NULL,
    NULL,
    CONVERT(VARCHAR(MAX), OtherData)
FROM TestDataOther
WHERE Index_GUID = @IndexGuid

ORDER BY StepName
```

### Repair Data Handling (Phase 2)

**Tables:**
- `RepairData` - Repair session header
- `RepairActions` - Actions taken (codes + descriptions)
- `RepairSyndromes` / `RepairSyndromeCauses` - Failure taxonomy

**Mapping to WATS:**
- Create UUR (Unit Under Repair) report
- Include repair codes as custom fields
- Link to original UUT report via serial number

---

## Dependencies

### External Systems
- **VTE SQL Server** - Read-only access required
- **WATS API** - Upload endpoint (REST or pyWATS)
- **Windows Server** - Deployment target (for .NET service)

### Libraries
- **.NET 8 SDK** - Runtime environment
- **Dapper** - Micro-ORM for SQL queries
- **Microsoft.Data.SqlClient** - SQL Server driver
- **Serilog** - Structured logging
- **pyWATS** - WATS API client (via subprocess or HTTP)

### Configuration
- Connection string (SQL Server)
- WATS API endpoint + credentials
- Sync interval (e.g., every 5 minutes)
- Batch size (default 500 runs)
- Watermark file path

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| VTE schema differs across versions | High | High | Introspect schema on startup, validate required tables/columns |
| Timestamp timezone mismatch | Medium | High | Document timezone assumptions, add configuration option |
| Large historical backlog | Medium | Medium | Support initial sync with date range filter |
| TestDataOther format unknown | Low | Medium | Log as text, document limitation, defer complex parsing |
| WATS API rate limiting | Low | Medium | Add retry logic with exponential backoff |
| VTE DB downtime | Medium | Medium | Retry connection, log errors, continue on next cycle |

---

## Alternatives Considered

1. **Python-Only Adapter** ❌
   - Slower than .NET for SQL Server
   - pyodbc setup complexity on Windows
   - Decision: Use .NET for extraction, Python for upload

2. **Direct WATS REST API (No pyWATS)** ❌
   - Reinvents authentication, report building
   - Decision: Use pyWATS for maintainability

3. **VTE Export Files Instead of DB** ❌
   - VTE can export XML/CSV, but inconsistent formats
   - Decision: Database is source of truth

4. **Real-Time Integration (Hook VTE Events)** ❌
   - VTE may not expose event hooks
   - Decision: Polling-based incremental sync

---

## Open Questions

1. **Timezone Handling:** Are VTE timestamps in local server time or UTC?
   - **Action:** Query VTE DB admin, document in config

2. **Repair Data Priority:** Should repair data be in Phase 1 or Phase 2?
   - **Decision:** Phase 2 (optional feature)

3. **Historical Data:** Should adapter support one-time backfill?
   - **Decision:** Yes, with date range configuration

4. **Deployment:** Windows Service or console app + Task Scheduler?
   - **Decision:** Console app + Task Scheduler (simpler deployment)

5. **Multi-Site Support:** Single adapter instance or per-site deployment?
   - **Decision:** Per-site deployment with site-specific config

---

## Success Metrics

- **Extraction Performance:** Extract 1000 runs in <30 seconds
- **Upload Performance:** Upload 1000 runs to WATS in <5 minutes
- **Data Quality:** 100% of VTE runs appear in WATS with correct pass/fail
- **Idempotency:** Zero duplicate uploads after restart
- **Reliability:** <1% failure rate on transient errors

---

## Next Steps

1. Set up VTE 9.31.1 test database (copy from production)
2. Analyze schema using SQL Server Management Studio
3. Validate .NET Dapper skeleton against real data
4. Design WATS mapping schema
5. Build Phase 1 prototype (extraction + single upload)

---

**Status:** Analysis complete, ready for implementation planning
