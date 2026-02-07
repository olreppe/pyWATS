# VTE → WATS Integration - TODO

**Legend:** ✅ Done | 🚧 In Progress | ✗ Not Started | ⏸️ Blocked | 🔄 Needs Review

---

## Phase 1: VTE Schema Analysis & Validation

### Database Setup
- [ ] ✗ Obtain VTE 9_3 database copy (sanitized)
- [ ] ✗ Restore to local SQL Server instance
- [ ] ✗ Create read-only login: `vte_adapter_readonly`
- [ ] ✗ Test connectivity via SSMS
- [ ] ✗ Document connection string format

### Schema Analysis
- [ ] ✗ Generate ER diagram using SSMS
- [ ] ✗ Compare with provided ERD (21 tables)
- [ ] ✗ Verify IndexData, UutData, TestData* tables
- [ ] ✗ Identify primary keys and foreign keys
- [ ] ✗ Document any schema differences from 9.31.1 baseline

### Query Development
- [ ] ✗ Write extraction query: IndexData + UutData
- [ ] ✗ Join TestDataNumeric, TestDataText, TestDataOther
- [ ] ✗ Add timestamp filter: `WHERE Timestamp > @Watermark`
- [ ] ✗ Test batching: `ORDER BY Timestamp OFFSET @Skip ROWS FETCH NEXT 1000`
- [ ] ✗ Profile query performance (execution plan)

### Sample Data
- [ ] ✗ Extract 100 real test runs to CSV
- [ ] ✗ Analyze pass/fail distribution
- [ ] ✗ Check for NULLs in Serial, ProductName, TestplanName
- [ ] ✗ Document field value ranges (timestamps, limits)
- [ ] ✗ Identify data quality issues

---

## Phase 2: .NET Data Access Library

### Project Setup
- [ ] ✗ Create .NET 8 console app: `VteWatsAdapter`
- [ ] ✗ Add NuGet: Dapper, Microsoft.Data.SqlClient, Serilog
- [ ] ✗ Create solution structure: DataAccess, Models, Services
- [ ] ✗ Configure logging (Serilog: console + file)
- [ ] ✗ Add .gitignore for .NET projects

### Data Models
- [ ] ✗ Create `VteTestRun` class (IndexData + UutData fields)
- [ ] ✗ Create `VteStepResult` class (TestData union)
- [ ] ✗ Create `VteProduct`, `VteTestplan` classes
- [ ] ✗ Add data annotations for required fields
- [ ] ✗ Add ToString() overrides for debugging

### Repository Implementation
- [ ] ✗ Create `IVteRepository` interface
- [ ] ✗ Implement `GetTestRunsSinceAsync(DateTime watermark)`
- [ ] ✗ Implement `GetTestRunByIdAsync(Guid indexGuid)`
- [ ] ✗ Implement step results normalization (UNION ALL query)
- [ ] ✗ Add IAsyncEnumerable for streaming results
- [ ] ✗ Configure connection pooling

### Configuration
- [ ] ✗ Create `appsettings.json` schema
- [ ] ✗ Add `VteDbOptions` class (ConnectionString, Schema)
- [ ] ✗ Add `WatsApiOptions` class (Endpoint, ApiKey)
- [ ] ✗ Add `SyncOptions` class (Interval, BatchSize)
- [ ] ✗ Implement configuration validation on startup

### Watermark Persistence
- [ ] ✗ Create `WatermarkStore` class (JSON file-based)
- [ ] ✗ Store last sync timestamp: `{ "lastSync": "2026-02-02T10:00:00Z" }`
- [ ] ✗ Add guard band logic (re-read last 10 minutes)
- [ ] ✗ Handle first-run: use configured initial date
- [ ] ✗ Add thread-safe read/write

### Error Handling
- [ ] ✗ Add Polly NuGet package
- [ ] ✗ Implement retry policy (3 attempts, exponential backoff)
- [ ] ✗ Detect transient SQL errors (timeout, connection reset)
- [ ] ✗ Add structured logging for failures
- [ ] ✗ Create dead letter queue (failed runs to JSON file)

### Unit Tests
- [ ] ✗ Create `VteWatsAdapter.Tests` project
- [ ] ✗ Mock SqlConnection for repository tests
- [ ] ✗ Test watermark persistence (read, write, guard band)
- [ ] ✗ Test configuration validation (missing required fields)
- [ ] ✗ Test retry logic (simulate SQL timeout)
- [ ] ✗ Achieve 80%+ code coverage

---

## Phase 3: WATS Mapping & Upload

### pyWATS Setup
- [ ] ✗ Install pyWATS in Python venv
- [ ] ✗ Configure WATS API credentials (test environment)
- [ ] ✗ Test sample report upload: `client.report.submit_report(...)`
- [ ] ✗ Document authentication flow (API key vs OAuth)

### Mapper Implementation
- [ ] ✗ Create `WatsReportMapper` class
- [ ] ✗ Map `VteTestRun.IndexGuid` → `source_id="VTE:{guid}"`
- [ ] ✗ Map product, process, station from VTE master data
- [ ] ✗ Map step results: numeric with limits, text results
- [ ] ✗ Handle pass/fail status
- [ ] ✗ Map timestamp (timezone conversion if needed)
- [ ] ✗ Handle optional fields (operator, testplan revision)

### Idempotency
- [ ] ✗ Query WATS for existing report by source_id
- [ ] ✗ Skip upload if already exists
- [ ] ✗ Log: "Run {IndexGuid} already uploaded, skipping"
- [ ] ✗ Add force-reupload flag (override idempotency)

### Upload Service
- [ ] ✗ Create `WatsUploadService` class
- [ ] ✗ Implement batch upload (100 reports per batch)
- [ ] ✗ Add retry logic on WATS API errors (429, 503)
- [ ] ✗ Update watermark after successful batch
- [ ] ✗ Rollback watermark on batch failure

### pyWATS Integration
- [ ] ✗ Decide: subprocess (Python script) vs HTTP client
- [ ] ✗ Serialize VteTestRun to JSON
- [ ] ✗ Call pyWATS upload endpoint
- [ ] ✗ Parse response (success, error, validation issues)
- [ ] ✗ Handle rate limiting (backoff, retry)

### End-to-End Workflow
- [ ] ✗ Implement main loop: Extract → Map → Upload → Watermark
- [ ] ✗ Add progress reporting (runs processed, uploaded, skipped)
- [ ] ✗ Add dry-run mode (`--dry-run` flag, no upload)
- [ ] ✗ Add backfill mode (`--start-date`, `--end-date`)

### Integration Tests
- [ ] ✗ Test full pipeline with sample VTE data
- [ ] ✗ Verify reports in WATS test environment
- [ ] ✗ Test idempotency (re-run should skip existing)
- [ ] ✗ Test error recovery (WATS down, network failure)
- [ ] ✗ Test backfill mode (historical data)

---

## Phase 4: Production Features

### Sync Scheduler
- [ ] ✗ Add configurable interval (default: 5 minutes)
- [ ] ✗ Implement timer-based execution (System.Threading.Timer)
- [ ] ✗ Add graceful shutdown (CancellationToken)
- [ ] ✗ Add manual trigger (run-now command)

### Health Monitoring
- [ ] ✗ Expose HTTP health endpoint: `/health`
- [ ] ✗ Report: last sync time, runs processed, error count
- [ ] ✗ Add metrics: runs/minute, upload latency
- [ ] ✗ Write health status to log file

### Alerting
- [ ] ✗ Detect sync failures (no progress for 1 hour)
- [ ] ✗ Send email on error threshold (configure SMTP)
- [ ] ✗ Add VTE DB connectivity check (on startup, periodic)
- [ ] ✗ Add WATS API connectivity check

### Performance Optimization
- [ ] ✗ Profile SQL queries with SQL Server Profiler
- [ ] ✗ Test with 10,000+ run backlog
- [ ] ✗ Benchmark batch sizes: 100, 500, 1000
- [ ] ✗ Add parallel upload if beneficial (SemaphoreSlim)

### Documentation
- [ ] ✗ Write installation guide (prerequisites, setup steps)
- [ ] ✗ Document appsettings.json schema
- [ ] ✗ Create troubleshooting guide (common errors, solutions)
- [ ] ✗ Add architecture diagram (VTE → Adapter → WATS)
- [ ] ✗ Document timezone handling

### Deployment Package
- [ ] ✗ Publish self-contained: `dotnet publish -c Release -r win-x64`
- [ ] ✗ Include sample appsettings.json
- [ ] ✗ Create Windows Task Scheduler XML template
- [ ] ✗ Add README with quick start instructions
- [ ] ✗ Package as ZIP: `VteWatsAdapter-v1.0.0.zip`

---

## Phase 5: Testing & Validation

### Customer Site Testing
- [ ] ✗ Deploy to customer test environment
- [ ] ✗ Configure with production VTE DB (read-only)
- [ ] ✗ Run initial backfill (last 7 days)
- [ ] ✗ Monitor logs for errors
- [ ] ✗ Verify WATS test environment receives reports

### Data Validation
- [ ] ✗ Compare VTE vs WATS (sample 100 runs)
- [ ] ✗ Verify step results match (values, limits)
- [ ] ✗ Verify pass/fail status matches
- [ ] ✗ Check timestamp accuracy (timezone)
- [ ] ✗ Verify product/process mapping

### Performance Testing
- [ ] ✗ Measure throughput (runs/hour)
- [ ] ✗ Identify bottlenecks (SQL query, WATS upload)
- [ ] ✗ Tune batch size based on results
- [ ] ✗ Test with peak load (1000 runs at once)

### Bug Fixes
- [ ] ✗ Fix issues found in testing
- [ ] ✗ Add missing error handling
- [ ] ✗ Improve logging clarity
- [ ] ✗ Update documentation

### User Acceptance Testing
- [ ] ✗ Customer reviews WATS reports
- [ ] ✗ Validate data completeness
- [ ] ✗ Test restart/recovery (stop adapter, restart)
- [ ] ✗ Customer sign-off on deployment

### Production Deployment
- [ ] ✗ Deploy to production server
- [ ] ✗ Configure Windows Task Scheduler (every 5 min)
- [ ] ✗ Set up monitoring/alerting
- [ ] ✗ Hand off to customer operations team
- [ ] ✗ Schedule 1-week follow-up review

---

## Documentation & Finalization

### CHANGELOG
- [ ] ✗ Add entry under [Unreleased] → Added
- [ ] ✗ Entry: "VTE → WATS integration adapter"
- [ ] ✗ Include version, deployment date

### Completion
- [ ] ✗ Create COMPLETION_SUMMARY.md
- [ ] ✗ Move project to `docs/internal_documentation/completed/`
- [ ] ✗ Archive .NET code to separate repository
- [ ] ✗ Update project status in active README

---

## Blockers

_None currently - waiting for approval to start_

---

## Notes

- Project created from VTE integration analysis and .NET skeleton
- Targeting Q2 2026 completion (7 weeks)
- Requires VTE DB access and WATS API credentials to begin
- Consider Python-only implementation as alternative (pyodbc + pyWATS)

---

**Last Updated:** 2026-02-02
