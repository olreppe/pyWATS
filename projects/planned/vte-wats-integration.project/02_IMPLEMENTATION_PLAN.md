# VTE → WATS Integration - Implementation Plan

**Created:** 2026-02-02  
**Phases:** 5  
**Total Duration:** 7 weeks

---

## Phase 1: VTE Schema Analysis & Validation (Week 1)

### Objectives
- Validate VTE 9.31.1 schema against provided documentation
- Identify required tables, columns, relationships
- Test SQL queries for extraction

### Tasks

1. **Set up VTE test database** (4 hours)
   - Obtain sanitized copy of VTE 9_3 database
   - Restore to local SQL Server instance
   - Create read-only login for adapter
   - Verify connectivity via SSMS

2. **Schema introspection** (4 hours)
   - Generate ER diagram using SSMS
   - Compare with provided ERD
   - Document any schema differences
   - Identify primary keys, foreign keys, indexes

3. **Query validation** (8 hours)
   - Test extraction query for IndexData + UutData
   - Join TestDataNumeric, TestDataText, TestDataOther
   - Verify timestamp filtering works
   - Test batching/paging (TOP 1000, OFFSET/FETCH)
   - Profile query performance on large dataset

4. **Sample data analysis** (4 hours)
   - Extract 100 real test runs
   - Analyze pass/fail distribution
   - Check for NULLs in critical fields
   - Identify data quality issues
   - Document field value ranges

**Deliverables:**
- VTE schema documentation (tables, columns, relationships)
- Validated SQL extraction queries
- Sample dataset (100 runs) for mapping tests
- Performance baseline (query execution times)

**Success Criteria:**
- All required tables exist with expected columns
- Extraction query returns complete test runs
- Query executes in <5 seconds for 1000 runs

---

## Phase 2: .NET Data Access Library (Weeks 2-3)

### Objectives
- Build production-ready Dapper-based VTE repository
- Implement incremental sync logic
- Add configuration, logging, error handling

### Tasks

1. **Project setup** (2 hours)
   - Create .NET 8 console app: `VteWatsAdapter`
   - Add NuGet packages: Dapper, Microsoft.Data.SqlClient, Serilog
   - Configure solution structure (DataAccess, Models, Services)
   - Set up logging (console + file)

2. **Data models** (4 hours)
   - Create `VteTestRun` class (IndexData + UutData)
   - Create `VteStepResult` class (union of TestData tables)
   - Create `VteProduct`, `VteTestplan`, etc. (master data)
   - Add data annotations for validation

3. **VteRepository implementation** (12 hours)
   - Implement `GetTestRunsSinceAsync(DateTime watermark)`
   - Implement `GetTestRunByIdAsync(Guid indexGuid)`
   - Implement step results normalization query
   - Add batching logic (yield return IAsyncEnumerable)
   - Add connection pooling configuration

4. **Configuration management** (4 hours)
   - Create `appsettings.json` schema
   - Add VteDbOptions class
   - Add WatsApiOptions class
   - Implement configuration validation
   - Add secrets management (connection strings)

5. **Watermark persistence** (4 hours)
   - Create `WatermarkStore` class (JSON file)
   - Store last sync timestamp per site
   - Add guard band logic (re-read last 10 min)
   - Handle first-run scenario (initial backfill)

6. **Error handling** (4 hours)
   - Add retry logic with Polly
   - Transient failure detection (SQL timeout, connection reset)
   - Dead letter queue for failed runs
   - Structured error logging

7. **Unit tests** (6 hours)
   - Mock SqlConnection with Dapper
   - Test VteRepository methods
   - Test watermark persistence
   - Test configuration validation
   - Test error handling paths

**Deliverables:**
- `Vte.DataAccess` class library
- `VteWatsAdapter` console app skeleton
- Unit tests (80%+ coverage)
- Configuration documentation

**Success Criteria:**
- Repository extracts test runs with all step results
- Incremental sync works (watermark tracking)
- Unit tests pass, no SQL injection risks

---

## Phase 3: WATS Mapping & Upload (Weeks 4-5)

### Objectives
- Map VTE data model to WATS reports
- Integrate with pyWATS library
- Implement idempotency checks

### Tasks

1. **pyWATS integration setup** (4 hours)
   - Install pyWATS in Python venv
   - Configure WATS API credentials
   - Test report upload with sample data
   - Document authentication flow

2. **VTE → WATS mapper** (12 hours)
   - Create `WatsReportMapper` class
   - Map `VteTestRun` → WATS `Report`
   - Map product/process/station from VTE master data
   - Map step results with limits
   - Handle pass/fail status
   - Handle missing/optional fields

3. **Idempotency implementation** (6 hours)
   - Query WATS for existing reports by source_id
   - Skip upload if `VTE:{Index_GUID}` exists
   - Log skip reason (already uploaded)
   - Add force-reupload option (override)

4. **Upload service** (8 hours)
   - Create `WatsUploadService` class
   - Batch upload (100 reports per batch)
   - Retry logic on WATS API errors
   - Update watermark after successful batch
   - Rollback watermark on failure

5. **Integration with pyWATS** (8 hours)
   - **Option A:** Call pyWATS via subprocess (Python script)
   - **Option B:** HTTP client to pyWATS REST endpoints
   - Serialize VTE runs to JSON
   - Pass to pyWATS for upload
   - Handle response errors

6. **End-to-end workflow** (4 hours)
   - Main loop: Extract → Map → Upload → Update watermark
   - Add progress reporting (runs processed, uploaded, skipped)
   - Add dry-run mode (no upload)
   - Add backfill mode (custom date range)

7. **Integration tests** (6 hours)
   - Test full pipeline with sample VTE data
   - Verify reports appear in WATS (test environment)
   - Test idempotency (re-run should skip)
   - Test error recovery (WATS down, network failure)

**Deliverables:**
- `WatsReportMapper` class
- `WatsUploadService` class
- Integration tests
- pyWATS integration documentation

**Success Criteria:**
- VTE test runs upload to WATS correctly
- Idempotency prevents duplicates
- Upload rate: 1000 runs in <5 minutes

---

## Phase 4: Incremental Sync & Production Features (Week 6)

### Objectives
- Finalize incremental sync behavior
- Add monitoring, health checks
- Prepare for deployment

### Tasks

1. **Sync scheduler** (4 hours)
   - Add configurable sync interval (default: 5 minutes)
   - Implement timer-based execution
   - Add graceful shutdown (finish current batch)
   - Add manual trigger (run-now command)

2. **Health monitoring** (4 hours)
   - Expose health check endpoint (HTTP /health)
   - Report: last sync time, runs processed, errors
   - Add metrics: runs/minute, upload latency
   - Write health status to log

3. **Alerting** (4 hours)
   - Detect sync failures (no progress for 1 hour)
   - Send email/webhook on error threshold
   - Add WATS API connectivity check
   - Add VTE DB connectivity check

4. **Performance optimization** (6 hours)
   - Profile SQL queries, add indexes if needed
   - Test with 10,000+ run backlog
   - Optimize batch size (benchmark)
   - Add parallel upload if beneficial

5. **Documentation** (6 hours)
   - Installation guide (prerequisites, setup)
   - Configuration reference (appsettings.json)
   - Troubleshooting guide (common errors)
   - API/architecture documentation

6. **Deployment package** (4 hours)
   - Create self-contained .NET publish
   - Include sample appsettings.json
   - Create Windows Task Scheduler template
   - Add README with quick start

**Deliverables:**
- Production-ready adapter executable
- Health monitoring endpoints
- Installation guide
- Deployment package (ZIP)

**Success Criteria:**
- Adapter runs continuously without manual intervention
- Health checks report accurate status
- Documentation allows customer self-deployment

---

## Phase 5: Testing & Validation (Week 7)

### Objectives
- Test adapter with real VTE data at customer site
- Validate data accuracy in WATS
- Fix bugs, tune performance

### Tasks

1. **Customer site testing** (8 hours)
   - Deploy adapter to test environment
   - Configure with production VTE database (read-only)
   - Run initial backfill (last 7 days)
   - Monitor for errors, data quality issues

2. **Data validation** (6 hours)
   - Compare VTE results with WATS reports (sample 100)
   - Verify step results, limits, pass/fail
   - Check timestamps (timezone correctness)
   - Verify product/process mapping

3. **Performance tuning** (4 hours)
   - Measure actual throughput (runs/hour)
   - Identify bottlenecks (DB query, WATS upload)
   - Tune batch size, concurrency
   - Test with peak load scenario

4. **Bug fixes** (8 hours)
   - Fix issues found during testing
   - Add missing error handling
   - Improve logging clarity
   - Update documentation

5. **User acceptance testing** (4 hours)
   - Customer reviews reports in WATS
   - Verify data completeness
   - Test restart/recovery scenarios
   - Sign-off on deployment

6. **Production deployment** (4 hours)
   - Deploy to production server
   - Configure Windows Task Scheduler
   - Set up monitoring/alerting
   - Hand off to customer operations team

**Deliverables:**
- Validated adapter (customer sign-off)
- Test report (data accuracy, performance)
- Production deployment
- Operations runbook

**Success Criteria:**
- 100% of VTE runs uploaded to WATS correctly
- Zero data quality issues
- Adapter runs reliably for 1 week without intervention

---

## Risk Mitigation Strategies

### Risk: VTE schema differences across sites
- **Mitigation:** Add schema validation on startup
- **Fallback:** Support configuration overrides for column names

### Risk: Timezone mismatches cause duplicate uploads
- **Mitigation:** Document timezone assumptions, add config option
- **Fallback:** Use guard band (re-read last hour)

### Risk: WATS API rate limiting
- **Mitigation:** Add exponential backoff retry
- **Fallback:** Reduce batch size, increase interval

### Risk: Large historical backlog overwhelms adapter
- **Mitigation:** Add backfill mode with date range
- **Fallback:** Manual batching (run multiple times with different ranges)

---

## Dependencies & Prerequisites

**Before Starting:**
- VTE 9.31.1 database access (read-only)
- WATS API credentials (test + production)
- .NET 8 SDK installed
- pyWATS library installed in Python venv
- SQL Server Management Studio (for schema analysis)

**External Services:**
- VTE SQL Server (customer-hosted)
- WATS API (cloud or on-premise)
- Windows Server for deployment

---

## Testing Strategy

### Unit Testing
- Repository methods (mocked DB)
- Mapper logic (VTE → WATS)
- Watermark persistence
- Configuration validation

### Integration Testing
- Full pipeline with sample data
- WATS upload (test environment)
- Idempotency verification
- Error recovery scenarios

### Performance Testing
- Extract 10,000 runs, measure time
- Upload 10,000 runs, measure time
- Stress test with concurrent sync

### User Acceptance Testing
- Customer reviews WATS reports
- Validates data accuracy
- Tests operational procedures

---

## Rollback Plan

If adapter causes issues in production:
1. Stop Windows Task Scheduler job
2. Revert watermark to last known good timestamp
3. Investigate errors in logs
4. Fix and redeploy, or fall back to manual export

---

## Timeline Summary

| Phase | Duration | Dependencies |
|-------|----------|--------------|
| 1. Schema Analysis | 1 week | VTE DB access |
| 2. Data Access Library | 2 weeks | Phase 1 complete |
| 3. WATS Mapping | 2 weeks | Phase 2 complete, pyWATS setup |
| 4. Production Features | 1 week | Phase 3 complete |
| 5. Testing & Deployment | 1 week | Customer site access |

**Total:** 7 weeks

---

## Next Steps

1. Obtain VTE database access credentials
2. Set up development environment (.NET 8 + SQL Server)
3. Create Phase 1 tasks in TODO.md
4. Schedule kickoff meeting with customer stakeholders

**Status:** Implementation plan ready for approval
