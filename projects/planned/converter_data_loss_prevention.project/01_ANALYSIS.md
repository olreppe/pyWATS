# Converter Data Loss Prevention - Technical Analysis

**Created:** February 13, 2026  
**Purpose:** Deep-dive technical analysis of current state and proposed solution

---

## Table of Contents

1. [Current Architecture Analysis](#current-architecture-analysis)
2. [Gap Analysis](#gap-analysis)
3. [Proposed Architecture](#proposed-architecture)
4. [Data Models](#data-models)
5. [API Design](#api-design)
6. [Storage Strategy](#storage-strategy)
7. [Performance Considerations](#performance-considerations)
8. [Security & Compliance](#security--compliance)
9. [Migration Strategy](#migration-strategy)
10. [Risk Assessment](#risk-assessment)

---

## Current Architecture Analysis

### Converter Pipeline Flow

```python
# Current Flow (simplified)
1. FileSystemWatcher detects file in watch folder
2. Converter.validate() checks if can convert (confidence score)
3. Converter.convert() processes file → UUTReport/UURReport
4. API.submit() sends report to WATS server (or queues if offline)
5. PostProcessing based on PostProcessAction:
   - MOVE: source → Done folder
   - DELETE: source deleted
   - ZIP: source zipped → Done folder
   - KEEP: source stays in watch folder
6. on_success() or on_failure() lifecycle hooks called
7. File removed from watch folder (MOVE path)
```

### Current Post-Processing Actions

Located in `src/pywats_client/converters/models.py`:

```python
class PostProcessAction(Enum):
    DELETE = "delete"  # Delete the source file/folder
    MOVE = "move"      # Move to Done folder
    ZIP = "zip"        # Zip and move to Done folder
    KEEP = "keep"      # Keep file in place (no action)
```

**Current Implementation:**
- Post-processing handled by service layer after submission
- Done folder populated with source files (or zipped source files)
- No metadata tracking beyond filesystem timestamps
- No retention policies - Done folder grows indefinitely
- Manual cleanup required

### Existing Folder Structure

```
converter_base_path/
├── {converter_name}/
│   ├── watch/          # Input folder (FSWatcher monitors)
│   ├── Done/           # Successful conversions
│   ├── Error/          # Failed conversions
│   └── Pending/        # Suspended conversions (retry later)
```

### Configuration

From `src/pywats_client/core/config.py`:

```python
@dataclass
class ConverterConfig:
    name: str
    module_path: str              # "my_converter.CSVConverter"
    
    # Folders
    watch_folder: str
    done_folder: str
    error_folder: str
    pending_folder: str
    
    # Processing
    arguments: Dict[str, Any]     # Converter parameters
    priority: int = 5
    
    # Validation
    alarm_threshold: float = 0.5
    reject_threshold: float = 0.2
    
    # Retry
    max_retries: int = 3
    retry_delay_seconds: int = 60
    
    # Post-processing
    post_action: str = "move"
    archive_folder: str = ""      # <-- UNUSED currently!
```

**Key Finding:** `archive_folder` already exists but is NOT used!

---

## Gap Analysis

### Missing Capabilities

| Capability | Current State | Required State |
|-----------|---------------|----------------|
| **Source file retention** | Done folder only, manual cleanup | Automatic archiving with policies |
| **Conversion metadata** | None | Converter, version, params, timestamp |
| **Audit trail** | None | Queryable database of all conversions |
| **Reprocessing** | Manual file copy + reconvert | API to replay from date-time |
| **Output archiving** | .json files in Done, no compression | Compressed archive with retention |
| **Retention policies** | None | Time-based + size-based limits |
| **Archive browsing** | None | GUI to search/filter/view |
| **Space management** | Infinite growth | Automatic purging per policy |

### Critical Issues in Current Implementation

**Issue 1: Data Loss Risk**
- Source files moved to Done folder
- Users can manually delete Done folder contents
- No warning when disk space low
- **Impact:** Irreversible loss of source test data

**Issue 2: No Forensics**
- Can't determine what converter/params were used for a file
- Can't reproduce conversion results
- Troubleshooting requires guesswork
- **Impact:** Debugging conversion issues is extremely difficult

**Issue 3: Disk Space Exhaustion**
- Done folder grows unbounded
- Large binary source files never compressed
- .json output files accumulate
- **Impact:** Disk full errors stop conversions

**Issue 4: No Compliance Trail**
- No audit log of conversions
- Can't prove data integrity
- Can't export conversion history
- **Impact:** Regulatory compliance failures

---

## Proposed Architecture

### Enhanced Post-Processing Pipeline

```python
# NEW Flow with Archiving
1. FileSystemWatcher detects file in watch folder
2. [NEW] ArchiveInterceptor.pre_convert():
   - Copy source file to archive storage
   - Generate archive ID
   - Record metadata (timestamp, checksum, size)
   
3. Converter.validate() checks if can convert
4. Converter.convert() processes file → report
5. [NEW] ArchiveInterceptor.post_convert():
   - Update metadata with converter info
   - Store conversion parameters
   - Record conversion status
   
6. API.submit() sends report to server
7. [NEW] ArchiveInterceptor.post_submit():
   - Archive output .json report (if PostProcessAction.ARCHIVE)
   - Compress and store
   - Link to source archive ID
   
8. PostProcessing based on PostProcessAction:
   - MOVE: source → Done folder (as before)
   - DELETE: source deleted (as before)
   - ZIP: source zipped → Done folder (as before)
   - KEEP: source stays in watch folder (as before)
   - [NEW] ARCHIVE: source → archive storage, Done folder cleaned
   
9. [NEW] RetentionEngine.enforce_policy():
   - Check archive age vs. retention_days
   - Check archive size vs. max_size_gb
   - Purge old archives if limits exceeded
   - Log purge activity
```

### New Components

#### 1. Archive Storage Layer

```python
# src/pywats_client/converters/archive/storage.py

class ArchiveStorage:
    """
    Manages compressed storage of source files and output reports.
    
    Directory Structure:
        archive_root/
        ├── sources/
        │   └── {year}/
        │       └── {month}/
        │           └── {day}/
        │               └── {timestamp}_{checksum}.{ext}.gz
        ├── reports/
        │   └── {year}/
        │       └── {month}/
        │           └── {day}/
        │               └── {timestamp}_{archive_id}.json.gz
        └── metadata.db (SQLite)
    """
    
    async def archive_source(
        self,
        source_path: Path,
        converter_name: str,
        metadata: Dict[str, Any]
    ) -> str:
        """
        Archive a source file before conversion.
        
        Returns:
            archive_id: Unique ID for this archive entry
        """
    
    async def archive_report(
        self,
        report: Dict[str, Any],
        archive_id: str
    ) -> None:
        """Archive output report linked to source archive."""
    
    async def restore_source(
        self,
        archive_id: str,
        dest_folder: Path
    ) -> Path:
        """Restore archived source file to destination."""
    
    async def get_archives(
        self,
        from_date: datetime,
        to_date: datetime,
        converter_name: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[ArchiveEntry]:
        """Query archives within date range."""
    
    async def enforce_retention(
        self,
        policy: RetentionPolicy
    ) -> PurgeStatistics:
        """Purge old archives per retention policy."""
```

#### 2. Metadata Database

```sql
-- metadata.db schema

CREATE TABLE archive_entries (
    archive_id TEXT PRIMARY KEY,
    converter_name TEXT NOT NULL,
    converter_version TEXT,
    source_path TEXT NOT NULL,        -- Original file path
    source_checksum TEXT,              -- SHA256 of source
    source_size_bytes INTEGER,
    archived_path TEXT NOT NULL,       -- Path in archive storage
    compressed_size_bytes INTEGER,
   
    -- Conversion metadata
    conversion_timestamp DATETIME NOT NULL,
    conversion_parameters TEXT,        -- JSON of arguments
    conversion_status TEXT,            -- SUCCESS, FAILED, SUSPENDED
    conversion_error TEXT,             -- Error message if failed
    conversion_duration_ms INTEGER,
    
    -- Report metadata
    report_id TEXT,                    -- Report ID if submitted
    report_archived_path TEXT,         -- Path to archived report
    report_size_bytes INTEGER,
    
    -- Retention
    retention_until DATE,              -- Delete after this date
    purged_at DATETIME,                -- NULL if not purged
    
    -- Indexing
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_converter (converter_name, conversion_timestamp),
    INDEX idx_timestamp (conversion_timestamp),
    INDEX idx_status (conversion_status),
    INDEX idx_retention (retention_until, purged_at)
);

CREATE TABLE retention_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    converter_name TEXT UNIQUE NOT NULL,
    retention_days INTEGER NOT NULL DEFAULT 90,
    max_size_gb REAL NOT NULL DEFAULT 10.0,
    compression_level INTEGER DEFAULT 6,  -- 1-9 (gzip)
    enabled BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purge_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    purge_timestamp DATETIME NOT NULL,
    converter_name TEXT NOT NULL,
    archives_purged INTEGER,
    bytes_freed INTEGER,
    reason TEXT  -- "retention_days", "max_size_gb", "manual"
);
```

#### 3. Retention Policy Engine

```python
# src/pywats_client/converters/archive/retention.py

@dataclass
class RetentionPolicy:
    """Retention policy for a converter."""
    converter_name: str
    retention_days: int = 90        # Delete archives older than this
    max_size_gb: float = 10.0       # Delete oldest if total > this
    compression_level: int = 6      # 1 (fast) - 9 (best)
    enabled: bool = True

class RetentionEngine:
    """Enforces retention policies on archive storage."""
    
    async def enforce_policy(
        self,
        policy: RetentionPolicy
    ) -> PurgeStatistics:
        """
        Enforce retention policy:
        1. Delete archives older than retention_days
        2. If total size > max_size_gb, delete oldest until under limit
        
        Returns statistics on purged archives.
        """
    
    async def estimate_space_savings(
        self,
        policy: RetentionPolicy
    ) -> SpaceEstimate:
        """Calculate how much space would be freed by policy."""
    
    async def preview_purge(
        self,
        policy: RetentionPolicy
    ) -> List[ArchiveEntry]:
        """Show which archives would be purged (dry-run)."""
```

#### 4. Reprocessing API

```python
# src/pywats_client/converters/archive/reprocessing.py

class ReprocessingEngine:
    """Replays archived source files through converters."""
    
    async def reprocess_range(
        self,
        converter_name: str,
        from_date: datetime,
        to_date: datetime,
        use_current_converter: bool = True,
        use_current_parameters: bool = True,
        submit_to_server: bool = False,
        progress_callback: Optional[Callable] = None
    ) -> ReprocessingResult:
        """
        Reprocess archives within date range.
        
        Args:
            converter_name: Which converter's archives to reprocess
            from_date: Start of date range (inclusive)
            to_date: End of date range (inclusive)
            use_current_converter: Use current version or original?
            use_current_parameters: Use current args or original?
            submit_to_server: Submit reports or just convert?
            progress_callback: Called with (current, total, archive_id)
        
        Returns:
            Statistics on reprocessing run
        """
    
    async def reprocess_single(
        self,
        archive_id: str,
        **kwargs
    ) -> ConversionResult:
        """Reprocess a single archived file."""
    
    async def estimate_reprocessing_time(
        self,
        converter_name: str,
        from_date: datetime,
        to_date: datetime
    ) -> timedelta:
        """Estimate how long reprocessing would take."""
```

### Integration Points

#### Converter Lifecycle Hooks (Existing)

```python
# Current hooks we can leverage:
class FileConverter(ABC):
    def on_success(
        self, 
        source: ConverterSource, 
        result: ConverterResult,
        context: ConverterContext
    ) -> None:
        """Called after successful conversion and post-processing."""
        # [NEW] Archive here!
    
    def on_failure(
        self, 
        source: ConverterSource, 
        result: ConverterResult,
        context: ConverterContext
    ) -> None:
        """Called after failed conversion."""
        # [NEW] Archive with failure metadata!
```

**Problem:** Hooks called AFTER post-processing (file already moved)

**Solution:** Add new hooks OR intercept at service layer BEFORE post-processing.

#### Service Layer Integration

```python
# src/pywats_client/service/async_converter_pool.py

class AsyncConverterPool:
    async def _process_item(self, item: AsyncConversionItem) -> None:
        """Process conversion item."""
        
        # [NEW] Pre-convert archiving
        if self._archive_enabled:
            archive_id = await self._archive_storage.archive_source(
                source_path=item.file_path,
                converter_name=item.converter.name,
                metadata={
                    "arguments": item.converter.arguments,
                    "converter_version": item.converter.version
                }
            )
            item.archive_id = archive_id  # Track for later
        
        # Existing conversion logic
        result = await self._convert(item)
        
        # [NEW] Post-convert metadata update
        if self._archive_enabled and item.archive_id:
            await self._archive_storage.update_conversion_metadata(
                archive_id=item.archive_id,
                status=result.status,
                error=result.error,
                duration_ms=result.duration_ms
            )
        
        # Submit to server
        if result.success and result.report:
            await self._submit_report(result.report)
        
        # [NEW] Post-submit report archiving
        if self._archive_enabled and item.archive_id:
            if result.success and result.report:
                await self._archive_storage.archive_report(
                    report=result.report,
                    archive_id=item.archive_id
                )
        
        # Existing post-processing
        await self._post_process(item, result)
```

---

## Data Models

### ArchiveEntry

```python
@dataclass
class ArchiveEntry:
    """Represents a single archived conversion."""
    archive_id: str
    converter_name: str
    converter_version: str
    
    # Source file
    source_original_path: str
    source_archived_path: str
    source_checksum: str
    source_size_bytes: int
    compressed_size_bytes: int
    
    # Conversion
    conversion_timestamp: datetime
    conversion_parameters: Dict[str, Any]
    conversion_status: ConversionStatus
    conversion_error: Optional[str]
    conversion_duration_ms: int
    
    # Report
    report_id: Optional[str]
    report_archived_path: Optional[str]
    report_size_bytes: Optional[int]
    
    # Retention
    retention_until: date
    purged_at: Optional[datetime]
    
    # Metadata
    created_at: datetime


@dataclass
class ReprocessingResult:
    """Result of a reprocessing operation."""
    total_archives: int
    processed: int
    successful: int
    failed: int
    skipped: int
    duration: timedelta
    errors: List[Tuple[str, str]]  # (archive_id, error_msg)
```

---

## API Design

### Configuration Updates

```python
# Extend ConverterConfig
@dataclass
class ConverterConfig:
    # ... existing fields ...
    
    # Archive settings (NEW)
    archive_enabled: bool = False
    archive_folder: str = ""              # Already exists, now used!
    retention_days: int = 90
    max_archive_size_gb: float = 10.0
    compression_level: int = 6            # 1-9
    archive_source_files: bool = True     # Archive input files
    archive_output_reports: bool = True   # Archive .json outputs
```

### Client API

```python
# src/pywats/client/client.py

class Client:
    async def get_archive_entries(
        self,
        converter_name: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        status: Optional[ConversionStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ArchiveEntry]:
        """Query archived conversions."""
    
    async def reprocess_archives(
        self,
        converter_name: str,
        from_date: datetime,
        to_date: datetime,
        **kwargs
    ) -> ReprocessingResult:
        """Reprocess archived files."""
    
    async def get_retention_policy(
        self,
        converter_name: str
    ) -> RetentionPolicy:
        """Get retention policy for converter."""
    
    async def update_retention_policy(
        self,
        policy: RetentionPolicy
    ) -> None:
        """Update retention policy."""
    
    async def get_archive_statistics(
        self,
        converter_name: Optional[str] = None
    ) -> ArchiveStatistics:
        """Get statistics on archive storage."""
```

---

## Storage Strategy

### Directory Structure

```
{archive_root}/
├── sources/           # Compressed source files
│   └── {year}/        # 2026/
│       └── {month}/   # 02/
│           └── {day}/ # 13/
│              ├── 20260213_143022_a3f2d9.csv.gz
│              └── 20260213_143045_b8e1c4.xml.gz
│
├── reports/           # Compressed output .json files
│   └── {year}/
│       └── {month}/
│           └── {day}/
│               ├── 20260213_143022_a3f2d9.json.gz
│               └── 20260213_143045_b8e1c4.json.gz
│
└── metadata.db        # SQLite database
```

### File Naming Convention

```
{timestamp}_{archive_id}.{extension}.gz

Where:
- timestamp: YYYYMMDDHHmmss (sortable)
- archive_id: First 6 chars of SHA256(source_path + timestamp)
- extension: Original file extension (.csv, .xml, .json, etc.)
- .gz: Gzip compression
```

### Compression Strategy

**Gzip Compression Levels:**
- Level 1 (Fastest): ~2x compression, minimal CPU
- Level 6 (Default): ~5x compression, moderate CPU
- Level 9 (Best): ~6x compression, high CPU

**Recommendation:** Level 6 (good balance)

**Space Savings Estimate:**
- Text files (.csv, .txt, .xml): 5-10x compression
- JSON files: 3-5x compression
- Binary files (.bin, .dat): 1.5-2x compression (already compressed)

**Example:**
- 1 GB of CSV files → ~150 MB compressed
- 90 days * 1000 files/day * 10 KB/file = 900 MB → ~150 MB compressed

---

## Performance Considerations

### Archiving Overhead

**Pre-Convert Archiving:**
```python
# Worst case (10 MB file, compression level 6)
- Read file: ~20 ms (500 MB/s disk)
- Compress (gzip): ~100 ms (100 MB/s compression rate)
- Write compressed: ~5 ms
- Database insert: ~1 ms
Total: ~126 ms
```

**Post-Convert Archiving (Report):**
```python
# Typical .json report: ~50 KB
- Serialize to JSON: ~5 ms
- Compress: ~10 ms
- Write: ~1 ms
- Database update: ~1 ms
Total: ~17 ms
```

**Impact:** <150 ms added latency per conversion (acceptable)

### Query Performance

**SQLite with proper indexing:**
- Single archive lookup by ID: <1 ms
- Date range query (1 day): ~10 ms (hundreds of results)
- Date range query (90 days): ~50 ms (thousands of results)
- Full-text search on errors: ~100 ms

**Optimization:**
- Index on (converter_name, conversion_timestamp)
- Index on conversion_status for filtering
- Periodic VACUUM to reclaim space after purges

### Storage Growth

**Example Scenario:**
- 10 converters
- 1000 files/day average
- 10 KB average file size (before compression)
- 90-day retention

**Calculation:**
```
Uncompressed: 10 * 1000 * 10 KB * 90 = 9 GB
Compressed (5x): 9 GB / 5 = 1.8 GB

Plus metadata DB: ~50 MB (900,000 records * 50 bytes/record)

Total: ~2 GB for 90 days
```

**Capacity Planning:**
- Recommend 10 GB default max_size_gb per converter
- Monitor archive growth rate (bytes/day)
- Alert when approaching limit

---

## Security & Compliance

### Data Protection

**Checksums:**
- SHA256 hash of source file before compression
- Verify integrity on restore
- Detect corruption or tampering

**Access Control:**
- Archive folder permissions: Read/Write for client service only
- Database encryption: Optional (future enhancement)
- Audit log of archive access (future)

### Compliance Features

**Audit Trail:**
- Every conversion tracked with metadata
- Export archive manifest for compliance reports
- Tamper-evident via checksums

**Retention Policies:**
- Configurable per converter (21 CFR Part 11, GDPR, etc.)
- Automated enforcement
- Purge logs for verification

**Data Integrity:**
- Source file checksum verification
- Report to source linkage via archive_id
- Reproducibility: reprocess with original params

---

## Migration Strategy

### Phase 1: Opt-In (v0.3.0)

**Default:** Archiving disabled

**Enable per converter:**
```json
{
  "name": "CSV Converter",
  "archive_enabled": true,
  "archive_folder": "/var/pywats/archives/csv_converter",
  "retention_days": 90,
  "max_archive_size_gb": 10.0
}
```

**Backwards Compatibility:**
- All existing converters work unchanged
- No breaking API changes
- Archive code paths only execute if `archive_enabled=True`

### Phase 2: Default Enable (v0.4.0)

**After user adoption:**
- Default `archive_enabled=True` for new converters
- Existing converters remain opt-in
- Migration guide for enabling archiving

### Phase 3: Mandatory (v1.0)

**For compliance edition:**
- Archiving always enabled
- Configurable retention only
- Cannot disable (regulatory requirement)

---

## Risk Assessment

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Disk space exhaustion** | HIGH | MEDIUM | Size-based retention policies, monitoring, alerts |
| **Archive corruption** | MEDIUM | LOW | Checksums, verify on restore, graceful degradation |
| **Performance degradation** | MEDIUM | LOW | Async archiving, compression level tuning |
| **Database lock contention** | LOW | LOW | WAL mode for SQLite, batch inserts |
| **Reprocessing errors** | MEDIUM | MEDIUM | Dry-run mode, progress tracking, rollback |

### Operational Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Archive size explosion** | HIGH | MEDIUM | Default 10 GB limit, automatic purging |
| **Compliance audit failure** | HIGH | LOW | Comprehensive audit trail, export manifests |
| **User confusion (too many options)** | LOW | MEDIUM | Sane defaults, clear documentation, wizards |
| **Migration issues** | MEDIUM | LOW | Opt-in rollout, extensive testing |

### Data Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Archive vs source mismatch** | MEDIUM | LOW | Checksum verification |
| **Purge policy too aggressive** | MEDIUM | MEDIUM | Preview before purge, configurable limits |
| **Lost archiving (bugs)** | HIGH | LOW | Comprehensive unit/integration tests |
| **Report to source orphaning** | LOW | LOW | Foreign key constraints in DB |

---

## Open Design Questions

### 1. Archive Location

**Question:** Should archive_folder be:
- (A) Inside converter folder (e.g., `{converter}/Archive/`)
- (B) Separate global location (e.g., `/var/pywats/archives/`)
- (C) Configurable per converter

**Recommendation:** (C) Configurable - allows flexibility for different storage (network drives, separate disks)

### 2. Compression Algorithm

**Question:** Gzip vs. ZIP vs. LZMA?

**Comparison:**
| Algorithm | Compression Ratio | Speed | Random Access |
|-----------|------------------|--------|---------------|
| Gzip | 5x (good) | Fast | No |
| ZIP | 5x (good) | Fast | Yes (multi-file) |
| LZMA | 7x (best) | Slow | No |

**Recommendation:** Gzip - best for streaming individual files, widely supported

### 3. Database Choice

**Question:** SQLite vs. PostgreSQL vs. flat files (JSON)?

**Comparison:**
| Option | Pros | Cons |
|--------|------|------|
| SQLite | • No server<br>• Zero config<br>• Fast queries | • Single writer |
| PostgreSQL | • Multi-writer<br>• Advanced queries | • Requires server<br>• Complex setup |
| JSON files | • Simple<br>• Portable | • Slow queries<br>• No indexing |

**Recommendation:** SQLite - matches pyWATS architecture (no external dependencies)

### 4. Archive ID Generation

**Question:** UUID vs. SHA256(source) vs. Sequential?

**Recommendation:** Hybrid: `{timestamp_ms}_{sha256_first6}` for:
- Sortable by time
- Collision-resistant via checksum
- Human-readable timestamp

---

## References

### Existing Code

- `src/pywats_client/converters/models.py` - ConverterResult, PostProcessAction
- `src/pywats_client/core/config.py` - ConverterConfig
- `src/pywats_client/service/async_converter_pool.py` - Conversion pipeline
- `src/pywats_client/converters/file_converter.py` - Lifecycle hooks

### Standards

- ISO 27001 (Data retention)
- 21 CFR Part 11 (FDA electronic records)
- GDPR (Right to erasure vs. retention)

---

**Last Updated:** February 13, 2026  
**Next Steps:** Create implementation plan (02_IMPLEMENTATION_PLAN.md)
