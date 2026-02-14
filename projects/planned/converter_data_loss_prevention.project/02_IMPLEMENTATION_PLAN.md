# Implementation Plan: Converter Data Loss Prevention & Archive System

**Created:** February 13, 2026  
**Estimated Duration:** 3-4 weeks  
**Target Release:** v0.3.0

---

## Overview

This document outlines the step-by-step execution plan for implementing the Converter Data Loss Prevention & Archive System.

**Approach:** Incremental delivery in 4 phases
- Phase 1: Core infrastructure (archiving layer)
- Phase 2: Retention & post-processing
- Phase 3: Reprocessing capabilities
- Phase 4: GUI & user experience

---

## Prerequisites

### Technical Requirements
- ✅ Python 3.8+ installed
- ✅ SQLite3 available (Python standard library)
- ✅ Disk space for archives (recommend 50+ GB)
- ✅ Existing converter infrastructure working

### Code Dependencies
- ✅ `pywats` core library (domains, exceptions, logging)
- ✅ `pywats_client` service layer
- ✅ `pywats_ui` for GUI components
- ⏳ NEW: `gzip` module for compression (standard library)
- ⏳ NEW: `sqlite3` module for database (standard library)

### Knowledge Requirements
- Understanding of converter lifecycle
- Familiarity with async/await patterns
- SQLite database basics
- File compression concepts

---

## Phase 1: Core Archive Infrastructure (Week 1)

**Goal:** Implement foundational archive storage layer with metadata database

### Task 1.1: Create Archive Storage Module ⏱️ 8 hours

**Priority:** CRITICAL  
**Files:**
- `src/pywats_client/converters/archive/__init__.py` (new)
- `src/pywats_client/converters/archive/storage.py` (new)
- `src/pywats_client/converters/archive/models.py` (new)

**Implementation:**
```python
# storage.py structure
class ArchiveStorage:
    """Manages compressed file storage and metadata."""
    
    def __init__(self, archive_root: Path):
        self.archive_root = archive_root
        self.sources_dir = archive_root / "sources"
        self.reports_dir = archive_root / "reports"
        self.db_path = archive_root / "metadata.db"
        self._init_database()
    
    def _init_database(self) -> None:
        """Create database schema if not exists."""
        # Execute SQL from analysis doc
    
    async def archive_source(
        self,
        source_path: Path,
        converter_name: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Archive source file with compression."""
        # 1. Generate archive_id
        # 2. Calculate checksum
        # 3. Compress with gzip
        # 4. Save to dated folder
        # 5. Insert metadata row
        # 6. Return archive_id
    
    async def archive_report(
        self,
        report: Dict[str, Any],
        archive_id: str
    ) -> None:
        """Archive output report."""
        # 1. Serialize to JSON
        # 2. Compress
        # 3. Save to dated folder
        # 4. Update metadata row
    
    async def get_archive(
        self,
        archive_id: str
    ) -> Optional[ArchiveEntry]:
        """Retrieve archive metadata by ID."""
    
    async def query_archives(
        self,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        converter_name: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[ArchiveEntry]:
        """Query archives with filters."""
```

**Success Criteria:**
- ✅ Database schema created correctly
- ✅ Files compressed and stored in dated folders
- ✅ Metadata inserted to database
- ✅ Archives queryable by date/converter/status
- ✅ Unit tests pass (100% coverage)

**Testing:**
```python
# tests/client/converters/archive/test_storage.py
async def test_archive_source():
    storage = ArchiveStorage(temp_dir)
    archive_id = await storage.archive_source(
        source_path=Path("test.csv" ),
        converter_name="CSV Converter",
        metadata={"version": "1.0.0"}
    )
    
    assert archive_id is not None
    entry = await storage.get_archive(archive_id)
    assert entry.converter_name == "CSV Converter"
    assert entry.source_checksum is not None
```

### Task 1.2: Implement Database Layer ⏱️ 4 hours

**Priority:** CRITICAL  
**Files:**
-  `src/pywats_client/converters/archive/database.py` (new)

**Implementation:**
```python
class ArchiveDatabase:
    """SQLite database operations for archive metadata."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_schema()
    
    def _init_schema(self) -> None:
        """Create tables and indexes."""
        # Execute CREATE TABLE statements from analysis
    
    async def insert_archive(
        self,
        entry: ArchiveEntry
    ) -> None:
        """Insert new archive entry."""
    
    async def update_conversion_metadata(
        self,
        archive_id: str,
        status: str,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None
    ) -> None:
        """Update after conversion completes."""
    
    async def update_report_metadata(
        self,
        archive_id: str,
        report_id: str,
        report_path: str,
        report_size: int
    ) -> None:
        """Update after report archived."""
    
    async def query(
        self,
        filters: Dict[str, Any],
        order_by: str = "conversion_timestamp DESC",
        limit: int = 100,
        offset: int = 0
    ) -> List[ArchiveEntry]:
        """Flexible query with filters."""
```

**Success Criteria:**
- ✅ All CRUD operations working
- ✅ Indexes created for performance
- ✅ Parameterized queries (SQL injection safe)
- ✅ Connection pooling for async
- ✅ WAL mode enabled for concurrency

### Task 1.3: Add Compression Utilities ⏱️ 3 hours

**Priority:** HIGH  
**Files:**
- `src/pywats_client/converters/archive/compression.py` (new)

**Implementation:**
```python
class CompressionHandler:
    """Handles file compression/decompression."""
    
    @staticmethod
    async def compress_file(
        source_path: Path,
        dest_path: Path,
        compression_level: int = 6
    ) -> int:
        """
        Compress file with gzip.
        
        Returns:
            Compressed file size in bytes
        """
        # Use asyncio.to_thread for blocking I/O
        def _compress():
            with open(source_path, 'rb') as f_in:
                with gzip.open(dest_path, 'wb', compresslevel=compression_level) as f_out:
                    shutil.copyfileobj(f_in, f_out)
            return dest_path.stat().st_size
        
        return await asyncio.to_thread(_compress)
    
    @staticmethod
    async def decompress_file(
        compressed_path: Path,
        dest_path: Path
    ) -> int:
        """Decompress gzipped file."""
    
    @staticmethod
    def calculate_checksum(file_path: Path) -> str:
        """Calculate SHA256 checksum."""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
```

**Success Criteria:**
- ✅ Files compressed successfully
- ✅ Compression ratios measured (5x+ for text)
- ✅ Decompression restores original exactly
- ✅ Checksums match before/after
- ✅ Async operations don't block event loop

### Task 1.4: Update ConverterConfig Schema ⏱️ 2 hours

**Priority:** HIGH  
**Files:**
- `src/pywats_client/core/config.py` (modify)

**Changes:**
```python
@dataclass
class ConverterConfig:
    # ... existing fields ...
    
    # Archive settings (NEW)
    archive_enabled: bool = False
    archive_folder: str = ""  # Already exists, now documented!
    retention_days: int = 90
    max_archive_size_gb: float = 10.0
    compression_level: int = 6  # 1-9
    archive_source_files: bool = True
    archive_output_reports: bool = True
```

**Migration:**
- Add default values for new fields
- Existing configs load without errors
- Update config serialization/deserialization

**Success Criteria:**
- ✅ New fields added with defaults
- ✅ Existing configs backward compatible
- ✅ Config save/load works
- ✅ Validation prevents invalid values (compression_level 1-9)

---

## Phase 2: Retention & Post-Processing (Week 2)

**Goal:** Implement retention policies and archive post-processing

### Task 2.1: Create Retention Policy Engine ⏱️ 6 hours

**Priority:** HIGH  
**Files:**
- `src/pywats_client/converters/archive/retention.py` (new)

**Implementation:**
```python
@dataclass
class RetentionPolicy:
    converter_name: str
    retention_days: int = 90
    max_size_gb: float = 10.0
    compression_level: int = 6
    enabled: bool = True

@dataclass
class PurgeStatistics:
    archives_purged: int
    bytes_freed: int
    oldest_purged: datetime
    newest_purged: datetime
    reason: str  # "retention_days", "max_size_gb", "manual"

class RetentionEngine:
    """Enforces retention policies."""
    
    async def enforce_policy(
        self,
        policy: RetentionPolicy
    ) -> PurgeStatistics:
        """
        Enforce retention policy:
        1. Find archives older than retention_days
        2. Find oldest archives if total size > max_size_gb
        3. Purge identified archives
        4. Update database (purged_at timestamp)
        5. Delete compressed files
        6. Return statistics
        """
    
    async def estimate_space_savings(
        self,
        policy: RetentionPolicy
    ) -> int:
        """Calculate bytes that would be freed."""
    
    async def preview_purge(
        self,
        policy: RetentionPolicy
    ) -> List[ArchiveEntry]:
        """Dry-run: show what would be purged."""
    
    async def get_archive_statistics(
        self,converter_name: str
    ) -> Dict[str, Any]:
        """Get current archive stats (count, size, oldest, newest)."""
```

**Success Criteria:**
- ✅ Time-based retention works (archives older than X days deleted)
- ✅ Size-based retention works (oldest deleted until under limit)
- ✅ Purge is transactional (all or nothing)
- ✅ Statistics accurate
- ✅ Preview mode doesn't delete anything

### Task 2.2: Add PostProcessAction.ARCHIVE ⏱️ 4 hours

**Priority:** HIGH  
**Files:**
- `src/pywats_client/converters/models.py` (modify)
- `src/pywats_client/service/async_converter_pool.py` (modify)

**Changes:**
```python
# models.py
class PostProcessAction(Enum):
    DELETE = "delete"
    MOVE = "move"
    ZIP = "zip"
    KEEP = "keep"
    ARCHIVE = "archive"  # NEW

# async_converter_pool.py
async def _post_process_file(
    self,
    item: AsyncConversionItem,
    result: ConverterResult
) -> None:
    """Handle post-processing."""
    
    if result.post_action == PostProcessAction.ARCHIVE:
        # Already archived in pre-convert phase
        # Just delete from watch folder
        await self._delete_source_file(item.file_path)
        
        # Clean Done folder (delete .json if exists)
        if self._done_folder:
            json_file = self._done_folder / f"{item.file_path.stem}.json"
            if json_file.exists():
                await self._delete_file(json_file)
    
    elif result.post_action == PostProcessAction.MOVE:
        # Existing logic...
    
    # ... other actions ...
```

**Success Criteria:**
- ✅ ARCHIVE action available in enum
- ✅ Source file deleted after archiving
- ✅ Done folder cleaned
- ✅ Works with existing actions

### Task 2.3: Integrate Archiving into Conversion Pipeline ⏱️ 8 hours

**Priority:** CRITICAL  
**Files:**
- `src/pywats_client/service/async_converter_pool.py` (modify)

**Implementation:**
```python
class AsyncConverterPool:
    def __init__(self, ...):
        # ... existing init ...
        
        # NEW: Archive storage
        self._archive_storage: Optional[ArchiveStorage] = None
        if self._config.archive_root:
            self._archive_storage = ArchiveStorage(
                Path(self._config.archive_root)
            )
    
    async def _process_item(
        self,
        item: AsyncConversionItem
    ) -> None:
        """Process conversion with archiving."""
        
        archive_id: Optional[str] = None
        
        # STEP 1: Pre-convert archiving (if enabled)
        if self._should_archive(item.converter):
            archive_id = await self._archive_source(item)
            item.archive_id = archive_id
        
        # STEP 2: Existing conversion logic
        try:
            result = await self._convert_item(item)
        except Exception as e:
            # Update archive with failure
            if archive_id:
                await self._update_archive_failure(archive_id, str(e))
            raise
        
        # STEP 3: Update archive with success metadata
        if archive_id and result.success:
            await self._update_archive_success(
                archive_id=archive_id,
                status=result.status,
                duration_ms=result.duration_ms
            )
        
        # STEP 4: Submit report
        if result.success and result.report:
            report_id = await self._submit_report(result.report)
            
            # STEP 5: Archive output report
            if archive_id and self._should_archive_reports(item.converter):
                await self._archive_report(archive_id, result.report, report_id)
        
        # STEP 6: Post-processing
        await self._post_process(item, result)
        
        # STEP 7: Enforce retention (async background task)
        if self._archive_storage:
            asyncio.create_task(
                self._enforce_retention_async(item.converter.name)
            )
    
    def _should_archive(self, converter: Converter) -> bool:
        """Check if archiving enabled for converter."""
        config = converter.config
        return (
            config.archive_enabled 
            and config.archive_source_files
            and self._archive_storage is not None
        )
    
    async def _archive_source(
        self,
        item: AsyncConversionItem
    ) -> str:
        """Archive source file before conversion."""
        return await self._archive_storage.archive_source(
            source_path=item.file_path,
            converter_name=item.converter.name,
            metadata={
                "converter_version": item.converter.version,
                "arguments": item.converter.arguments,
                "priority": item.converter.priority
            }
        )
```

**Success Criteria:**
- ✅ Archiving integrated without breaking existing flow
- ✅ Source archived before conversion
- ✅ Metadata updated after conversion
- ✅ Report archived after submission
- ✅ Retention enforced asynchronously
- ✅ No archiving when disabled
- ✅ All tests pass

### Task 2.4: Add Configuration UI for Archive Settings ⏱️ 4 hours

**Priority:** MEDIUM  
**Files:**
- `src/pywats_ui/apps/configurator/pages/converters.py` (modify)

**Changes:**
```python
# Add archive settings section to ConverterSettingsDialogV2
class ConverterSettingsDialogV2(QDialog, ErrorHandlingMixin):
    def _create_archive_section(self) -> QGroupBox:
        """Create archive settings section."""
        group = QGroupBox("Archive & Retention")
        layout = QFormLayout()
        
        # Enable archiving checkbox
        self._archive_enabled = QCheckBox("Enable archiving")
        layout.addRow("", self._archive_enabled)
        
        # Archive folder
        self._archive_folder = QLineEdit()
        self._browse_archive_btn = QPushButton("Browse...")
        archive_layout = QHBoxLayout()
        archive_layout.addWidget(self._archive_folder)
        archive_layout.addWidget(self._browse_archive_btn)
        layout.addRow("Archive Folder:", archive_layout)
        
        # Retention days
        self._retention_days = QSpinBox()
        self._retention_days.setRange(1, 3650)  # 1 day - 10 years
        self._retention_days.setValue(90)
        layout.addRow("Retention (days):", self._retention_days)
        
        # Max size
        self._max_size = QDoubleSpinBox()
        self._max_size.setRange(0.1, 1000.0)  # 100 MB - 1 TB
        self._max_size.setValue(10.0)
        self._max_size.setSuffix(" GB")
        layout.addRow("Max Archive Size:", self._max_size)
        
        # Compression level
        self._compression_level = QSpinBox()
        self._compression_level.setRange(1, 9)
        self._compression_level.setValue(6)
        layout.addRow("Compression Level:", self._compression_level)
        
        group.setLayout(layout)
        return group
```

**Success Criteria:**
- ✅ Archive settings UI added to converter config dialog
- ✅ Settings save/load correctly
- ✅ Folder browser works
- ✅ Validation on input values

---

## Phase 3: Reprocessing Capabilities (Week 3)

**Goal:** Enable reprocessing of archived files

### Task 3.1: Create Reprocessing Engine ⏱️ 10 hours

**Priority:** HIGH  
**Files:**
- `src/pywats_client/converters/archive/reprocessing.py` (new)

**Implementation:**
```python
@dataclass
class ReprocessingOptions:
    """Options for reprocessing."""
    use_current_converter: bool = True
    use_current_parameters: bool = True
    submit_to_server: bool = False
    skip_on_error: bool = True

@dataclass
class ReprocessingResult:
    total_archives: int
    processed: int
    successful: int
    failed: int
    skipped: int
    duration: timedelta
    errors: List[Tuple[str, str]]

class ReprocessingEngine:
    """Replays archived files through converters."""
    
    def __init__(
        self,
        archive_storage: ArchiveStorage,
        converter_pool: AsyncConverterPool
    ):
        self._storage = archive_storage
        self._pool = converter_pool
    
    async def reprocess_range(
        self,
        converter_name: str,
        from_date: datetime,
        to_date: datetime,
        options: ReprocessingOptions = ReprocessingOptions(),
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> ReprocessingResult:
        """
        Reprocess archives in date range.
        
        Algorithm:
        1. Query archives in date range
        2. For each archive:
           a. Restore source file to temp location
           b. Load converter (current or original version)
           c. Load parameters (current or original)
           d. Run conversion
           e. Submit report (if options.submit_to_server)
           f. Update progress callback
           g. Cleanup temp file
        3. Return statistics
        """
        archives = await self._storage.query_archives(
            from_date=from_date,
            to_date=to_date,
            converter_name=converter_name
        )
        
        total = len(archives)
        processed = 0
        successful = 0
        failed = 0
        errors = []
        
        start_time = datetime.now()
        
        for archive in archives:
            try:
                # Progress callback
                if progress_callback:
                    progress_callback(processed, total, archive.archive_id)
                
                # Restore source file
                temp_file = await self._restore_to_temp(archive)
                
                # Get converter
                converter = await self._get_converter(
                    converter_name,
                    use_current=options.use_current_converter,
                    original_version=archive.converter_version
                )
                
                # Get parameters
                if options.use_current_parameters:
                    params = converter.arguments
                else:
                    params = archive.conversion_parameters
                
                # Convert
                result = await self._convert_file(
                    converter=converter,
                    file_path=temp_file,
                    arguments=params
                )
                
                if result.success:
                    successful += 1
                    
                    # Submit if requested
                    if options.submit_to_server and result.report:
                        await self._submit_report(result.report)
                else:
                    failed += 1
                    errors.append((archive.archive_id, result.error or "Unknown error"))
                
                # Cleanup
                await self._cleanup_temp(temp_file)
                
            except Exception as e:
                failed += 1
                errors.append((archive.archive_id, str(e)))
                
                if not options.skip_on_error:
                   raise
            
            finally:
                processed += 1
        
        duration = datetime.now() - start_time
        
        return ReprocessingResult(
            total_archives=total,
            processed=processed,
            successful=successful,
            failed=failed,
            skipped=total - processed,
            duration=duration,
            errors=errors
        )
    
    async def reprocess_single(
        self,
        archive_id: str,
        options: ReprocessingOptions = ReprocessingOptions()
    ) -> ConverterResult:
        """Reprocess a single archive."""
        # Similar to above but for one archive
```

**Success Criteria:**
- ✅ Can reprocess date ranges
- ✅ Can use current or original converter/params
- ✅ Progress callback works
- ✅ Error handling robust (skip vs. abort)
- ✅ Statistics accurate
- ✅ Temp files cleaned up

### Task 3.2: Add Reprocessing API to Client ⏱️ 3 hours

**Priority:** HIGH  
**Files:**
- `src/pywats/client/client.py` (modify)
- `src/pywats_client/service/client_service.py` (modify)

**Implementation:**
```python
# client.py
class Client:
    async def reprocess_archives(
        self,
        converter_name: str,
        from_date: datetime,
        to_date: datetime,
        use_current_converter: bool = True,
        use_current_parameters: bool = True,
        submit_to_server: bool = False,
        skip_on_error: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Reprocess archived conversions."""
        return await self._service.reprocess_archives(...)
    
    async def get_archive_entries(
        self,
        converter_name: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Query archived conversions."""
        return await self._service.get_archive_entries(...)
```

**Success Criteria:**
- ✅ Client API added
- ✅ Service layer integration
- ✅ Type hints correct
- ✅ Docstrings complete

### Task 3.3: Create Reprocessing CLI Tool ⏱️ 4 hours

**Priority:** MEDIUM  
**Files:**
- `src/pywats_dev/cli/reprocess.py` (new)

**Implementation:**
```python
# CLI: pywats-reprocess

@click.command()
@click.option('--converter', required=True, help='Converter name')
@click.option('--from-date', required=True, type=click.DateTime(), help='Start date (YYYY-MM-DD)')
@click.option('--to-date', required=True, type=click.DateTime(), help='End date (YYYY-MM-DD)')
@click.option('--current-converter/--original-converter', default=True, help='Use current or original converter')
@click.option('--current-params/--original-params', default=True, help='Use current or original parameters')
@click.option('--submit/--no-submit', default=False, help='Submit reports to server')
@click.option('--dry-run', is_flag=True, help='Preview without reprocessing')
async def reprocess(
    converter: str,
    from_date: datetime,
    to_date: datetime,
    current_converter: bool,
    current_params: bool,
    submit: bool,
    dry_run: bool
):
    """Reprocess archived converter files."""
    
    client = await get_client()
    
    if dry_run:
        # Preview what would be reprocessed
        archives = await client.get_archive_entries(
            converter_name=converter,
            from_date=from_date,
            to_date=to_date
        )
        
        click.echo(f"Would reprocess {len(archives)} archives:")
        for archive in archives[:10]:  # Show first 10
            click.echo(f"  - {archive['archive_id']}: {archive['source_original_path']}")
        
        if len(archives) > 10:
            click.echo(f"  ... and {len(archives) - 10} more")
    
    else:
        # Actual reprocessing with progress bar
        with click.progressbar(length=100, label='Reprocessing') as bar:
            def progress_callback(current, total, archive_id):
                bar.update(int((current / total) * 100) - bar.pos)
            
            result = await client.reprocess_archives(
                converter_name=converter,
                from_date=from_date,
                to_date=to_date,
                use_current_converter=current_converter,
                use_current_parameters=current_params,
                submit_to_server=submit,
                progress_callback=progress_callback
            )
        
        click.echo(f"\nReprocessing complete!")
        click.echo(f"  Processed: {result['processed']}/{result['total_archives']}")
        click.echo(f"  Successful: {result['successful']}")
        click.echo(f"  Failed: {result['failed']}")
        click.echo(f"  Duration: {result['duration']}")
        
        if result['errors']:
            click.echo("\nErrors:")
            for archive_id, error in result['errors'][:5]:
                click.echo(f"  - {archive_id}: {error}")
```

**Success Criteria:**
- ✅ CLI command works
- ✅ Dry-run mode previews accurately
- ✅ Progress bar updates correctly
- ✅ Error reporting clear

---

## Phase 4: GUI & User Experience (Week 4)

**Goal:** Build user-friendly GUI for archive management

### Task 4.1: Create Archive Browser Widget ⏱️ 8 hours

**Priority:** HIGH  
**Files:**
- `src/pywats_ui/widgets/archive_browser.py` (new)

**Implementation:**
```python
class ArchiveBrowserWidget(QWidget):
    """Widget for browsing and filtering archived conversions."""
    
    def __init__(self, client: Client, parent=None):
        super().__init__(parent)
        self._client = client
        self._archives: List[Dict[str, Any]] = []
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # Filters
        filter_group = self._create_filters()
        layout.addWidget(filter_group)
        
        # Archive table
        self._table = QTableWidget()
        self._table.setColumnCount(8)
        self._table.setHorizontalHeaderLabels([
            "Archive ID",
            "Converter",
            "Source File",
            "Date/Time",
            "Status",
            "Size",
            "Compressed",
            "Actions"
        ])
        layout.addWidget(self._table)
        
        # Statistics
        stats_label = QLabel()
        layout.addWidget(stats_label)
        
        self.setLayout(layout)
    
    def _create_filters(self) -> QGroupBox:
        """Create filter controls."""
        group = QGroupBox("Filters")
        layout = QFormLayout()
        
        # Converter dropdown
        self._converter_combo = QComboBox()
        layout.addRow("Converter:", self._converter_combo)
        
        # Date range
        self._from_date = QDateEdit()
        self._from_date.setCalendarPopup(True)
        self._to_date = QDateEdit()
        self._to_date.setCalendarPopup(True)
        layout.addRow("From Date:", self._from_date)
        layout.addRow("To Date:", self._to_date)
        
        # Status filter
        self._status_combo = QComboBox()
        self._status_combo.addItems(["All", "Success", "Failed", "Suspended"])
        layout.addRow("Status:", self._status_combo)
        
        # Search button
        self._search_btn = QPushButton("Search")
        self._search_btn.clicked.connect(self._on_search)
        layout.addRow("", self._search_btn)
        
        group.setLayout(layout)
        return group
    
    async def _on_search(self):
        """Search archives with filters."""
        archives = await self._client.get_archive_entries(
            converter_name=self._converter_combo.currentText(),
            from_date=self._from_date.dateTime().toPython(),
            to_date=self._to_date.dateTime().toPython(),
            status=self._status_combo.currentText() if self._status_combo.currentText() != "All" else None
        )
        
        self._populate_table(archives)
    
    def _populate_table(self, archives: List[Dict[str, Any]]):
        """Populate table with archive entries."""
        self._table.setRowCount(len(archives))
        
        for row, archive in enumerate(archives):
            # Archive ID
            self._table.setItem(row, 0, QTableWidgetItem(archive['archive_id'][:8]))
            
            # Converter
            self._table.setItem(row, 1, QTableWidgetItem(archive['converter_name']))
            
            # Source file
            self._table.setItem(row, 2, QTableWidgetItem(
                Path(archive['source_original_path']).name
            ))
            
            # Date/Time
            dt = datetime.fromisoformat(archive['conversion_timestamp'])
            self._table.setItem(row, 3, QTableWidgetItem(
                dt.strftime("%Y-%m-%d %H:%M:%S")
            ))
            
            # Status
            st status_item = QTableWidgetItem(archive['conversion_status'])
            if archive['conversion_status'] == 'SUCCESS':
                status_item.setBackground(QColor(200, 255, 200))
            elif archive['conversion_status'] == 'FAILED':
                status_item.setBackground(QColor(255, 200, 200))
            self._table.setItem(row, 4, status_item)
            
            # Size
            self._table.setItem(row, 5, QTableWidgetItem(
                self._format_bytes(archive['source_size_bytes'])
            ))
            
            # Compressed
            self._table.setItem(row, 6, QTableWidgetItem(
                self._format_bytes(archive['compressed_size_bytes'])
            ))
            
            # Actions button
            actions_btn = QPushButton("⋮")
            actions_btn.clicked.connect(
                lambda checked, aid=archive['archive_id']: self._show_actions(aid)
            )
            self._table.setCellWidget(row, 7, actions_btn)
        
        self._table.resizeColumnsToContents()
    
    def _show_actions(self, archive_id: str):
        """Show action menu for archive."""
        menu = QMenu(self)
        
        view_action = menu.addAction("View Details")
        view_action.triggered.connect(lambda: self._view_details(archive_id))
        
        restore_action = menu.addAction("Restore File")
        restore_action.triggered.connect(lambda: self._restore_file(archive_id))
        
        reprocess_action = menu.addAction("Reprocess")
        reprocess_action.triggered.connect(lambda: self._reprocess_single(archive_id))
        
        menu.exec_(QCursor.pos())
    
    @staticmethod
    def _format_bytes(bytes_val: int) -> str:
        """Format bytes as human-readable."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024.0:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024.0
        return f"{bytes_val:.1f} TB"
```

**Success Criteria:**
- ✅ Archive table displays correctly
- ✅ Filters work (converter, date, status)
- ✅ Action menu appears on row click
- ✅ Performance acceptable for 1000+ rows
- ✅ Sorting by columns works

### Task 4.2: Create Reprocessing Dialog ⏱️ 6 hours

**Priority:** MEDIUM  
**Files:**
- `src/pywats_ui/widgets/reprocess_dialog.py` (new)

**Implementation:**
```python
class ReprocessDialog(QDialog, ErrorHandlingMixin):
    """Dialog for configuring and running reprocessing."""
    
    def __init__(
        self,
        client: Client,
        converter_name: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        parent=None
    ):
        super().__init__(parent)
        self._client = client
        self._setup_ui()
        
        if converter_name:
            self._converter_combo.setCurrentText(converter_name)
        if from_date:
            self._from_date.setDateTime(from_date)
        if to_date:
            self._to_date.setDateTime(to_date)
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # Date range
        form = QFormLayout()
        self._converter_combo = QComboBox()
        self._from_date = QDateTimeEdit()
        self._to_date = QDateTimeEdit()
        form.addRow("Converter:", self._converter_combo)
        form.addRow("From Date:", self._from_date)
        form.addRow("To Date:", self._to_date)
        layout.addLayout(form)
        
        # Options
        options_group = QGroupBox("Reprocessing Options")
        options_layout = QVBoxLayout()
        
        self._current_converter_check = QCheckBox("Use current converter version")
        self._current_converter_check.setChecked(True)
        
        self._current_params_check = QCheckBox("Use current parameters")
        self._current_params_check.setChecked(True)
        
        self._submit_check = QCheckBox("Submit reports to server")
        self._submit_check.setChecked(False)
        
        options_layout.addWidget(self._current_converter_check)
        options_layout.addWidget(self._current_params_check)
        options_layout.addWidget(self._submit_check)
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Preview button
        self._preview_btn = QPushButton("Preview (Dry Run)")
        self._preview_btn.clicked.connect(self._on_preview)
        layout.addWidget(self._preview_btn)
        
        # Preview results
        self._preview_text = QTextEdit()
        self._preview_text.setReadOnly(True)
        self._preview_text.setMaximumHeight(150)
        layout.addWidget(self._preview_text)
        
        # Progress bar
        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        layout.addWidget(self._progress_bar)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_reprocess)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        self.setWindowTitle("Reprocess Archives")
        self.resize(600, 500)
    
    async def _on_preview(self):
        """Preview what archives would be reprocessed."""
        archives = await self._client.get_archive_entries(
            converter_name=self._converter_combo.currentText(),
            from_date=self._from_date.dateTime().toPython(),
            to_date=self._to_date.dateTime().toPython()
        )
        
        preview = f"Found {len(archives)} archives to reprocess:\n\n"
        for archive in archives[:20]:  # Show first 20
            preview += f"  - {archive['archive_id']}: {Path(archive['source_original_path']).name}\n"
        
        if len(archives) > 20:
            preview += f"\n... and {len(archives) - 20} more archives"
        
        self._preview_text.setPlainText(preview)
    
    async def _on_reprocess(self):
        """Run reprocessing."""
        self._progress_bar.setVisible(True)
        self._progress_bar.setValue(0)
        
        def progress_callback(current, total, archive_id):
            self._progress_bar.setValue(int((current / total) * 100))
            QApplication.processEvents()  # Keep UI responsive
        
        try:
            result = await self._client.reprocess_archives(
                converter_name=self._converter_combo.currentText(),
                from_date=self._from_date.dateTime().toPython(),
                to_date=self._to_date.dateTime().toPython(),
                use_current_converter=self._current_converter_check.isChecked(),
                use_current_parameters=self._current_params_check.isChecked(),
                submit_to_server=self._submit_check.isChecked(),
                progress_callback=progress_callback
            )
            
            self.show_success(
                f"Reprocessing complete!\n\n"
                f"Processed: {result['processed']}/{result['total_archives']}\n"
                f"Successful: {result['successful']}\n"
                f"Failed: {result['failed']}\n"
                f"Duration: {result['duration']}",
                "Reprocessing Complete"
            )
            
            self.accept()
            
        except Exception as e:
            self.handle_error(e, "reprocessing archives")
```

**Success Criteria:**
- ✅ Dialog configures all options
- ✅ Preview works (dry run)
- ✅ Progress bar updates during reprocess
- ✅ Success/error dialogs shown
- ✅ UI remains responsive

### Task 4.3: Add Archive Stats Dashboard ⏱️ 4 hours

**Priority:** LOW  
**Files:**
- `src/pywats_ui/widgets/archive_stats.py` (new)

**Implementation:**
```python
class ArchiveStatsWidget(QWidget):
    """Dashboard showing archive statistics."""
    
    def _setup_stats_cards(self):
        """Create stat cards layout."""
        layout = QGridLayout()
        
        # Total archives card
        total_card = self._create_stat_card(
            title="Total Archives",
            value="1,234",
            icon="📦"
        )
        layout.addWidget(total_card, 0, 0)
        
        # Total size card
        size_card = self._create_stat_card(
            title="Total Size",
            value="8.5 GB",
            icon="💾"
        )
        layout.addWidget(size_card, 0, 1)
        
        # Space saved card
        saved_card = self._create_stat_card(
            title="Space Saved",
            value="42.3 GB",
            subtitle="(83% compression)",
            icon="📊"
        )
        layout.addWidget(saved_card, 0, 2)
        
        # Oldest archive card
        oldest_card = self._create_stat_card(
            title="Oldest Archive",
            value="45 days ago",
            icon="📅"
        )
        layout.addWidget(oldest_card, 0, 3)
        
        return layout
    
    def _create_stat_card(
        self,
        title: str,
        value: str,
        icon: str = "",
        subtitle: str = ""
    ) -> QFrame:
        """Create a stat card widget."""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 32px;")
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; color: #666;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("font-size: 10px; color: #999;")
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(subtitle_label)
        
        card.setLayout(layout)
        return card
```

**Success Criteria:**
- ✅ Stats cards display key metrics
- ✅ Values update from live data
- ✅ Styling consistent with app theme
- ✅ Responsive layout

---

## Testing Strategy

### Unit Tests

**Coverage Target:** 90%+

**Key Test Files:**
- `tests/client/converters/archive/test_storage.py` - Archive storage operations
- `tests/client/converters/archive/test_database.py` - Database CRUD operations
- `tests/client/converters/archive/test_compression.py` - Compression/decompression
- `tests/client/converters/archive/test_retention.py` - Retention policy enforcement
- `tests/client/converters/archive/test_reprocessing.py` - Reprocessing engine

**Test Scenarios:**
- Archive source file (compress, store, metadata)
- Archive report (serialize, compress, link to source)
- Query archives (filters, pagination, ordering)
- Enforce retention (time-based, size-based, combined)
- Reprocess single archive
- Reprocess date range with failures
- Handle corrupted archives gracefully
- Concurrent archiving (thread safety)

### Integration Tests

**Test Scenarios:**
- End-to-end: File arrives → converted → archived → queried → restored → reprocessed
- Archiving disabled → no overhead
- Archiving enabled → files compressed and metadata stored
- Retention exceeded → oldest archives purged
- Reprocessing updates metadata correctly

### Performance Tests

**Benchmarks:**
- Archive 1000 files (10 KB each) → measure duration
- Query 10,000 archives with filters → <100 ms
- Reprocess 100 archives → measure throughput
- Retention purge of 1000 archives → <5 seconds

**Acceptance Criteria:**
- Archiving adds <150 ms per conversion
- Database queries <100 ms for typical use
- No memory leaks during long-running operations

---

## Documentation

### Developer Documentation

**Files to Create:**
- `docs/guides/converter-archiving.md` - User guide for archiving features
- `docs/api/archive-api.rst` - Sphinx API reference
- `examples/converters/archived_converter.py` - Example with archiving enabled

**Content:**
- How to enable archiving
- Configuring retention policies
- Using reprocessing APIs
- Troubleshooting archive issues
-  CLI tool reference

### User Documentation

**Files to Create:**
- `docs/guides/data-retention.md` - Data retention guide for compliance
- `docs/guides/reprocessing-guide.md` - How to reprocess archived data

**Content:**
- Why archiving is important
- Recommended retention settings
- How to browse archives
- How to reprocess conversions
- Storage requirements

---

## Migration & Rollout

### Phase 1: Internal Beta (Week 1-2)

**Scope:** Core archiving only
- Enable for 1-2 converters internally
- Monitor disk usage
- Verify metadata accuracy
- Test retention policies

**Rollback Plan:**
- Disable archiving in config
- Archive storage remains on disk (no data loss)

### Phase 2: Limited Release (Week 3)

**Scope:** Add reprocessing
- Enable for select customers
- Provide reprocessing CLI tool
- Monitor usage and errors
- Collect feedback

### Phase 3: General Availability (Week 4+)

**Scope:** Full release with GUI
- Include in v0.3.0 release
- Update documentation
- Training materials
- Announce feature

---

## Success Metrics

### Technical Metrics
- ✅ Archive storage implementation complete (100% of planned features)
- ✅ Retention policies enforced correctly (100% accuracy)
- ✅ Reprocessing works for all converter types
- ✅ Performance impact <10% on conversion pipeline
- ✅ Unit test coverage >90%
- ✅ No data loss in production

### Business Metrics
- 🎯 Adoption: 50%+ of converters enable archiving
- 🎯 Space savings: 5x compression ratio achieved
- 🎯 Reprocessing usage: 10+ reprocessing runs per month
- 🎯 User satisfaction: Positive feedback from beta testers
- 🎯 Support tickets: <5 archiving-related issues per month

---

## Risks & Mitigation

### High Risks

**Risk:** Disk space exhaustion crashes conversions  
**Mitigation:** Size-based retention policies, disk usage monitoring, alerts

**Risk:** Archive corruption causes data loss  
**Mitigation:** Checksums verify integrity, graceful degradation if archive missing

**Risk:** Performance degradation slows conversions  
**Mitigation:** Async archiving, compression level tuning, benchmarking

### Medium Risks

**Risk:** Retention policies too aggressive (purge needed data)  
**Mitigation:** Preview before purge, configurable limits, audit logs

**Risk:** Reprocessing floods server with duplicate reports  
**Mitigation:** submit_to_server flag defaults to False, confirmation dialogs

**Risk:** Database lock contention blocks conversions  
**Mitigation:** SQLite WAL mode, batch inserts, separate database per converter

---

## Next Steps

1. ✅ Review implementation plan with team
2. ✅ Get stakeholder approval
3. ⏳ Start Phase 1 (Archive Infrastructure) - Week 1
4. ⏳ Regular progress updates in [03_PROGRESS.md](03_PROGRESS.md)
5. ⏳ Update [04_TODO.md](04_TODO.md) as tasks complete

---

**Last Updated:** February 13, 2026  
**Estimated Completion:** March 13, 2026 (4 weeks)  
**Owner:** Development Team
