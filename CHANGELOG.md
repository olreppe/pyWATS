# Changelog

All notable changes to PyWATS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

For detailed migration instructions, see [MIGRATION.md](MIGRATION.md).
For beta version history (b1-b38), see [CHANGELOG-BETA.md](CHANGELOG-BETA.md).

<!-- 
AGENT INSTRUCTIONS: See CONTRIBUTING.md for changelog management rules.
- Keep entries concise (one-liners, no code blocks)
- Add migration examples to MIGRATION.md, not here
- Link breaking changes to MIGRATION.md sections
-->

---

## [Unreleased]

### Added
- `AttachmentIO` class in `pywats_client.io` for file-based attachment operations
- `Step.add_attachment()` method for memory-only attachment handling
- `AttachmentMetadata` class (renamed from `Attachment` in models.py for clarity)
- `QueueItemStatus` enum for unified queue states
- `RetryHandler` class for unified retry execution
- Platform native installers (Windows MSI, macOS PKG/DMG, standalone executables)
- Multi-platform deployment infrastructure (systemd, launchd, Windows Service)
- Enhanced error messages with troubleshooting hints
- Layered event architecture (`pywats_events`, `pywats_cfx`)
- WATS 25.3 Asset module enhancements (calibration/maintenance, count management)
- Alarm and notification logs API

### Changed
- **File I/O architecture**: `pywats` is now memory-only; file operations in `pywats_client`
- Documentation reorganized into `docs/guides/`, `docs/reference/`, `docs/platforms/`, `docs/domains/`
- Core modules renamed: `batch` → `parallel`, `batching` → `coalesce`
- Terminology standardized: "Module" → "Domain"
- Test suite reorganized into domain-based structure
- Domain health grading upgraded to 60-point scale

### Removed (Breaking)
- `Attachment.from_file()` - Use `AttachmentIO.from_file()` ([migration](MIGRATION.md#v010b40---file-io-separation))
- `Step.attach_file()` - Use `AttachmentIO.from_file()` + `step.add_attachment()`
- `UURReport.attach_file()` - Use `attach_bytes()` instead
- `SimpleQueue` - Use `pywats_client.ClientService` for queuing
- `AsyncReportService` offline methods (`submit_offline`, `process_queue`, `offline_fallback`)
- Legacy UUR classes: `UURAttachment`, `Failure`, `UURPartInfo`, `FailCode`, `MiscUURInfo` ([migration](MIGRATION.md#v010b40---deprecated-uur-classes-removed))

### Deprecated
- UUR legacy classes marked for removal (now removed - see above)

---

## Beta Archive

All beta releases (0.1.0b1 through 0.1.0b38) have been archived to [CHANGELOG-BETA.md](CHANGELOG-BETA.md).

Key milestones from beta:
- **b38** - Report refactoring, type safety, queue architecture
- **b35** - Docker containerization, client test suite
- **b34** - Async-first architecture, batch operations, pagination
- **b32** - Unified API pattern (removed `*_internal` accessors)
- **b28** - Exception handling overhaul, ImportMode
- **b10** - Agent analysis tools
- **b1** - Initial release with all core domains
