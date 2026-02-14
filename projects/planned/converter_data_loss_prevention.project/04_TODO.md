# TODO Checklist: Converter Data Loss Prevention & Archive System

**Project:** Converter Data Loss Prevention & Archive System  
**Last Updated:** February 13, 2026  
**Status Key:** ✅ Complete | 🚧 In Progress | ⏸️ Blocked | ✗ Not Started

---

## Phase 0: Analysis & Planning

- ✅ Create project structure
- ✅ Create README.md with executive summary
- ✅ Perform codebase analysis (converter architecture)
- ✅ Create 01_ANALYSIS.md technical document
- ✅ Design 4-component architecture
- ✅ Define database schema (SQLite)
- ✅ Design storage strategy
- ✅ Analyze performance impact
- ✅ Create 02_IMPLEMENTATION_PLAN.md
- ✅ Define 4-phase implementation approach
- ✅ Create 03_PROGRESS.md
- ✅ Create 04_TODO.md (this file)
- ✗ Get stakeholder approval to proceed

---

## Phase 1: Core Archive Infrastructure (Week 1)

### Task 1.1: Create Archive Storage Module (⏱️ 8 hours)

- ✗ Create `src/pywats_client/converters/archive/__init__.py`
- ✗ Create `src/pywats_client/converters/archive/models.py`
  - ✗ Define ArchiveEntry dataclass
  - ✗ Define RetentionPolicy dataclass
  - ✗ Define PurgeStatistics dataclass
- ✗ Create `src/pywats_client/converters/archive/storage.py`
  - ✗ Implement ArchiveStorage class
  - ✗ Implement `__init__` (create directory structure)
  - ✗ Implement `_init_database()` (create schema)
  - ✗ Implement `archive_source()` async method
  - ✗ Implement `archive_report()` async method
  - ✗ Implement `get_archive()` async method
  - ✗ Implement `query_archives()` async method
- ✗ Create `tests/client/converters/archive/test_storage.py`
  - ✗ Test archive source file
  - ✗ Test archive report
  - ✗ Test query archives (filters)
  - ✗ Test invalid inputs (error handling)
  - ✗ Achieve 100% coverage for storage.py

### Task 1.2: Implement Database Layer (⏱️ 4 hours)

- ✗ Create `src/pywats_client/converters/archive/database.py`
  - ✗ Implement ArchiveDatabase class
  - ✗ Implement `_init_schema()` (CREATE TABLE statements)
  - ✗ Implement `insert_archive()` async method
  - ✗ Implement `update_conversion_metadata()` async method
  - ✗ Implement `update_report_metadata()` async method
  - ✗ Implement `query()` async method
  - ✗ Create indexes for performance (converter_name, conversion_timestamp)
  - ✗ Enable WAL mode for concurrency
- ✗ Create `tests/client/converters/archive/test_database.py`
  - ✗ Test insert archive entry
  - ✗ Test update operations
  - ✗ Test query with filters
  - ✗ Test pagination (limit/offset)
  - ✗ Test concurrent writes (WAL mode)
  - ✗ Achieve 100% coverage for database.py

### Task 1.3: Add Compression Utilities (⏱️ 3 hours)

- ✗ Create `src/pywats_client/converters/archive/compression.py`
  - ✗ Implement CompressionHandler class
  - ✗ Implement `compress_file()` static async method
  - ✗ Implement `decompress_file()` static async method
  - ✗ Implement `calculate_checksum()` static method (SHA256)
  - ✗ Use asyncio.to_thread for blocking I/O
- ✗ Create `tests/client/converters/archive/test_compression.py`
  - ✗ Test compress file (verify size reduction)
  - ✗ Test decompress file (verify exact restoration)
  - ✗ Test checksum calculation (deterministic)
  - ✗ Test compress/decompress round-trip
  - ✗ Test compression levels (1-9)
  - ✗ Test with large files (10 MB+)
  - ✗ Achieve 100% coverage for compression.py

### Task 1.4: Update ConverterConfig Schema (⏱️ 2 hours)

- ✗ Modify `src/pywats_client/core/config.py`
  - ✗ Add `archive_enabled: bool = False`
  - ✗ Document existing `archive_folder: str = ""`
  - ✗ Add `retention_days: int = 90`
  - ✗ Add `max_archive_size_gb: float = 10.0`
  - ✗ Add `compression_level: int = 6`
  - ✗ Add `archive_source_files: bool = True`
  - ✗ Add `archive_output_reports: bool = True`
  - ✗ Add validation for compression_level (1-9)
- ✗ Update config serialization/deserialization
- ✗ Test backward compatibility with existing configs
- ✗ Update `tests/client/core/test_config.py`
  - ✗ Test new fields load with defaults
  - ✗ Test config save/load round-trip
  - ✗ Test validation (invalid compression_level)

---

## Phase 2: Retention & Post-Processing (Week 2)

### Task 2.1: Create Retention Policy Engine (⏱️ 6 hours)

- ✗ Create `src/pywats_client/converters/archive/retention.py`
  - ✗ Implement RetentionEngine class
  - ✗ Implement `enforce_policy()` async method
  - ✗ Implement `estimate_space_savings()` async method
  - ✗ Implement `preview_purge()` async method (dry-run)
  - ✗ Implement `get_archive_statistics()` async method
  - ✗ Add time-based retention logic (older than X days)
  - ✗ Add size-based retention logic (purge oldest until under limit)
  - ✗ Add purge history logging
- ✗ Create `tests/client/converters/archive/test_retention.py`
  - ✗ Test time-based retention
  - ✗ Test size-based retention
  - ✗ Test combined retention (time AND size)
  - ✗ Test preview mode (no deletion)
  - ✗ Test archive statistics accuracy
  - ✗ Test transactional purge (all or nothing)
  - ✗ Achieve 100% coverage for retention.py

### Task 2.2: Add PostProcessAction.ARCHIVE (⏱️ 4 hours)

- ✗ Modify `src/pywats_client/converters/models.py`
  - ✗ Add `ARCHIVE = "archive"` to PostProcessAction enum
  - ✗ Update docstring with ARCHIVE behavior
- ✗ Modify `src/pywats_client/service/async_converter_pool.py`
  - ✗ Add ARCHIVE case to `_post_process_file()` method
  - ✗ Delete source file from watch folder after archiving
  - ✗ Clean Done folder (.json files)
- ✗ Update tests for new post-process action
  - ✗ Test ARCHIVE action deletes source
  - ✗ Test ARCHIVE action cleans Done folder
  - ✗ Test ARCHIVE works with existing actions

### Task 2.3: Integrate Archiving into Conversion Pipeline (⏱️ 8 hours)

- ✗ Modify `src/pywats_client/service/async_converter_pool.py`
  - ✗ Add `_archive_storage: Optional[ArchiveStorage]` field
  - ✗ Initialize ArchiveStorage in `__init__` if archive_root configured
  - ✗ Implement `_should_archive()` method
  - ✗ Implement `_archive_source()` method (pre-convert)
  - ✗ Implement `_update_archive_failure()` method
  - ✗ Implement `_update_archive_success()` method
  - ✗ Implement `_archive_report()` method
  - ✗ Implement `_enforce_retention_async()` background task
  - ✗ Integrate archiving into `_process_item()` pipeline
  - ✗ Add error handling (archiving failures don't break conversions)
- ✗ Create integration tests
  - ✗ Test end-to-end: file arrives → archived → converted → report archived
  - ✗ Test archiving disabled → no overhead
  - ✗ Test conversion failure → archive marked as failed
  - ✗ Test retention triggered after archiving
  - ✗ Test concurrent conversions with archiving

### Task 2.4: Add Configuration UI for Archive Settings (⏱️ 4 hours)

- ✗ Modify `src/pywats_ui/apps/configurator/pages/converters.py`
  - ✗ Add `_create_archive_section()` method to ConverterSettingsDialogV2
  - ✗ Add archive enabled checkbox
  - ✗ Add archive folder browser
  - ✗ Add retention days spinner (1-3650)
  - ✗ Add max size spinner (0.1-1000 GB)
  - ✗ Add compression level spinner (1-9)
  - ✗ Add source/report archiving checkboxes
  - ✗ Connect controls to config save/load
  - ✗ Add validation (archive folder must exist)
- ✗ Test UI changes
  - ✗ Test settings save/load correctly
  - ✗ Test folder browser works
  - ✗ Test validation prevents invalid inputs

---

## Phase 3: Reprocessing Capabilities (Week 3)

### Task 3.1: Create Reprocessing Engine (⏱️ 10 hours)

- ✗ Create `src/pywats_client/converters/archive/reprocessing.py`
  - ✗ Define ReprocessingOptions dataclass
  - ✗ Define ReprocessingResult dataclass
  - ✗ Implement ReprocessingEngine class
  - ✗ Implement `reprocess_range()` async method
  - ✗ Implement `reprocess_single()` async method
  - ✗ Implement `_restore_to_temp()` helper
  - ✗ Implement `_get_converter()` helper (current vs. original version)
  - ✗ Implement `_convert_file()` helper
  - ✗ Implement `_submit_report()` helper
  - ✗ Implement `_cleanup_temp()` helper
  - ✗ Add progress callback support
  - ✗ Add error handling (skip vs. abort)
- ✗ Create `tests/client/converters/archive/test_reprocessing.py`
  - ✗ Test reprocess single archive
  - ✗ Test reprocess date range
  - ✗ Test use current converter/parameters
  - ✗ Test use original converter/parameters
  - ✗ Test progress callback fires
  - ✗ Test skip_on_error=True continues
  - ✗ Test skip_on_error=False aborts
  - ✗ Test statistics accuracy
  - ✗ Achieve 100% coverage for reprocessing.py

### Task 3.2: Add Reprocessing API to Client (⏱️ 3 hours)

- ✗ Modify `src/pywats/client/client.py`
  - ✗ Add `reprocess_archives()` async method
  - ✗ Add `get_archive_entries()` async method
  - ✗ Add type hints and docstrings
- ✗ Modify `src/pywats_client/service/client_service.py`
  - ✗ Implement `reprocess_archives()` service method
  - ✗ Implement `get_archive_entries()` service method
  - ✗ Wire up to ReprocessingEngine
- ✗ Update API tests
  - ✗ Test client.reprocess_archives() calls service
  - ✗ Test client.get_archive_entries() returns data
  - ✗ Test error propagation

### Task 3.3: Create Reprocessing CLI Tool (⏱️ 4 hours)

- ✗ Create `src/pywats_dev/cli/reprocess.py`
  - ✗ Implement `pywats-reprocess` command
  - ✗ Add --converter option (required)
  - ✗ Add --from-date option (required)
  - ✗ Add --to-date option (required)
  - ✗ Add --current-converter/--original-converter flag
  - ✗ Add --current-params/--original-params flag
  - ✗ Add --submit/--no-submit flag
  - ✗ Add --dry-run flag (preview mode)
  - ✗ Implement preview logic (show archives)
  - ✗ Implement reprocessing with progress bar
  - ✗ Add error reporting
- ✗ Register command in `pyproject.toml` [project.scripts]
- ✗ Test CLI tool
  - ✗ Test dry-run mode
  - ✗ Test actual reprocessing
  - ✗ Test progress bar updates
  - ✗ Test error handling

---

## Phase 4: GUI & User Experience (Week 4)

### Task 4.1: Create Archive Browser Widget (⏱️ 8 hours)

- ✗ Create `src/pywats_ui/widgets/archive_browser.py`
  - ✗ Implement ArchiveBrowserWidget class
  - ✗ Create filter controls (converter, date range, status)
  - ✗ Create archive table (8 columns)
  - ✗ Implement `_on_search()` async method
  - ✗ Implement `_populate_table()` method
  - ✗ Implement `_show_actions()` context menu
  - ✗ Implement `_view_details()` action
  - ✗ Implement `_restore_file()` action
  - ✗ Implement `_reprocess_single()` action
  - ✗ Add table sorting
  - ✗ Add pagination controls
  - ✗ Add statistics label (total count, size)
- ✗ Test archive browser widget
  - ✗ Test filters work correctly
  - ✗ Test table populates
  - ✗ Test action menu appears
  - ✗ Test performance with 1000+ rows

### Task 4.2: Create Reprocessing Dialog (⏱️ 6 hours)

- ✗ Create `src/pywats_ui/widgets/reprocess_dialog.py`
  - ✗ Implement ReprocessDialog class (inherit ErrorHandlingMixin)
  - ✗ Create date range controls
  - ✗ Create options checkboxes (converter, params, submit)
  - ✗ Create preview button
  - ✗ Create preview text area
  - ✗ Create progress bar
  - ✗ Implement `_on_preview()` async method (dry-run)
  - ✗ Implement `_on_reprocess()` async method
  - ✗ Add progress callback (update progress bar)
  - ✗ Add success/error dialogs
  - ✗ Keep UI responsive during reprocessing
- ✗ Test reprocessing dialog
  - ✗ Test dialog opens with pre-filled values
  - ✗ Test preview works (dry-run)
  - ✗ Test reprocessing executes
  - ✗ Test progress bar updates
  - ✗ Test error handling

### Task 4.3: Add Archive Stats Dashboard (⏱️ 4 hours)

- ✗ Create `src/pywats_ui/widgets/archive_stats.py`
  - ✗ Implement ArchiveStatsWidget class
  - ✗ Create stat cards layout (grid)
  - ✗ Implement `_create_stat_card()` helper
  - ✗ Add "Total Archives" card
  - ✗ Add "Total Size" card
  - ✗ Add "Space Saved" card (compression)
  - ✗ Add "Oldest Archive" card
  - ✗ Fetch live data from archive storage
  - ✗ Add auto-refresh (every 30 seconds)
  - ✗ Add styling (consistent with app theme)
- ✗ Test archive stats widget
  - ✗ Test stats display correctly
  - ✗ Test auto-refresh updates values
  - ✗ Test styling is consistent

---

## Documentation

### Developer Documentation

- ✗ Create `docs/guides/converter-archiving.md`
  - ✗ How to enable archiving
  - ✗ Configuring retention policies
  - ✗ Using reprocessing APIs
  - ✗ Troubleshooting archive issues
- ✗ Create `docs/api/archive-api.rst` (Sphinx)
  - ✗ ArchiveStorage reference
  - ✗ RetentionEngine reference
  - ✗ ReprocessingEngine reference
  - ✗ API examples
- ✗ Create `examples/converters/archived_converter.py`
  - ✗ Example converter with archiving enabled
  - ✗ Comment explaining each configuration option
  - ✗ Show how to query archives
  - ✗ Show how to reprocess
- ✗ Create `examples/converters/reprocessing_example.py`
  - ✗ Demonstrate reprocessing API usage
  - ✗ Show date-range reprocessing
  - ✗ Show single archive reprocessing

### User Documentation

- ✗ Create `docs/guides/data-retention.md`
  - ✗ Why archiving is important (compliance, forensics)
  - ✗ Recommended retention settings by industry
  - ✗ Storage requirements calculator
  - ✗ Legal considerations
- ✗ Create `docs/guides/reprocessing-guide.md`
  - ✗ When to reprocess archives
  - ✗ How to browse archives in GUI
  - ✗ How to reprocess using CLI
  - ✗ How to reprocess using GUI
  - ✗ Best practices

### CHANGELOG

- ✗ Update `CHANGELOG.md` under `[Unreleased]`
  - ✗ Add "Added" section with archiving features
  - ✗ Describe PostProcessAction.ARCHIVE
  - ✗ Describe retention policies
  - ✗ Describe reprocessing capabilities
  - ✗ Describe new GUI components
  - ✗ List new API methods
  - ✗ Include migration notes

---

## Testing

### Unit Tests

- ✗ Create `tests/client/converters/archive/test_storage.py` - See Task 1.1
- ✗ Create `tests/client/converters/archive/test_database.py` - See Task 1.2
- ✗ Create `tests/client/converters/archive/test_compression.py` - See Task 1.3
- ✗ Create `tests/client/converters/archive/test_retention.py` - See Task 2.1
- ✗ Create `tests/client/converters/archive/test_reprocessing.py` - See Task 3.1
- ✗ Update existing tests for new config fields
- ✗ Achieve 90%+ test coverage across all new modules

### Integration Tests

- ✗ Create `tests/integration/test_archive_pipeline.py`
  - ✗ Test end-to-end archiving flow
  - ✗ Test conversion failure → archive marked failed
  - ✗ Test retention enforcement
  - ✗ Test reprocessing restores and reconverts
- ✗ Run all existing tests to verify no regressions

### Performance Tests

- ✗ Benchmark archiving 1000 files (10 KB each)
  - ✗ Target: <150 ms per file
- ✗ Benchmark querying 10,000 archives with filters
  - ✗ Target: <100 ms
- ✗ Benchmark reprocessing 100 archives
  - ✗ Measure throughput
- ✗ Benchmark retention purge of 1000 archives
  - ✗ Target: <5 seconds
- ✗ Memory leak testing (long-running archiving)

---

## Migration & Rollout

### Internal Beta (Week 1-2)

- ✗ Enable archiving for 1-2 internal converters
- ✗ Monitor disk usage daily
- ✗ Verify metadata accuracy (spot checks)
- ✗ Test retention policy enforcement
- ✗ Collect performance metrics
- ✗ Document any issues found

### Limited Release (Week 3)

- ✗ Enable for select customers (opt-in)
- ✗ Provide reprocessing CLI tool
- ✗ Monitor usage and errors
- ✗ Collect user feedback
- ✗ Create FAQ based on support questions
- ✗ Update documentation based on feedback

### General Availability (Week 4+)

- ✗ Include in v0.3.0 release
- ✗ Update user documentation
- ✗ Create training materials (videos, guides)
- ✗ Announce feature (release notes, blog post)
- ✗ Provide migration guide for existing users
- ✗ Monitor adoption rates

---

## Success Criteria Validation

### Technical Validation

- ✗ All unit tests passing (90%+ coverage)
- ✗ All integration tests passing
- ✗ Performance benchmarks met
- ✗ No memory leaks detected
- ✗ Archiving adds <10% overhead to conversion pipeline
- ✗ Database queries <100 ms for typical use
- ✗ Compression ratios >4x for text files

### Business Validation

- ✗ 50%+ of converters enable archiving (adoption)
- ✗ 5x compression ratio achieved (space savings)
- ✗ 10+ reprocessing runs per month (usage)
- ✗ Positive feedback from beta testers
- ✗ <5 archiving-related support tickets per month
- ✗ No data loss incidents reported

---

## Completion Checklist

Before moving project to `docs/internal_documentation/completed/`:

- ✗ All tests passing
- ✗ Move project tests to `tests/` directory
- ✗ Move examples to `examples/converters/`
- ✗ Update `CHANGELOG.md` under `[Unreleased]`
- ✗ Create `COMPLETION_SUMMARY.md`
- ✗ Regenerate Sphinx docs
- ✗ Run pre-release check script
- ✗ Code review completed
- ✗ User documentation reviewed
- ✗ Commit and push all changes
- ✗ Create pull request
- ✗ Get PR approved
- ✗ Merge to main
- ✗ Tag release (if applicable)
- ✗ Archive project to completed folder

---

**Last Updated:** February 13, 2026  
**Estimated Completion:** March 13, 2026 (4 weeks)  
**Current Status:** Planning Complete, Ready for Implementation
