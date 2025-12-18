# REPORT Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and tailored for the `report` domain inside `pywats.domains.report`.

## 1. Service Functions
- **Overview:** `ReportService` is the orchestration layer for the report domain. It exposes factory methods (UUT/UUR creation), query helpers (serial, part no., date range, misc info), WSJF/WSXF submission/retrieval, attachment download, and certificate fetch. All heavy lifting is routed through `ReportRepository` so unit tests can focus on business rules.
- **Key Operations:**
  - `create_uut_report` – builds a `UUTReport`, resolves station metadata, and seeds operator/processCode details directly understood by WATS.
  - `create_uur_report` – supports three invocation patterns (UUT object, GUID + metadata, or PN + test operation), maintains the dual `repair_process_code` vs `test_operation_code` contract, and copies sub-units + failures to match WATS repair hierarchies.
  - Query helpers (`query_uut_headers`, `query_uur_headers`, `get_headers_by_*`) – wrap `ReportRepository.query_headers` with pre-built `WATSFilter` models so callers avoid crafting filter dictionaries manually.
  - Reporting operations (`submit_report`, `submit_report_xml`, `get_report`, `get_report_xml`, `get_attachment`, `get_all_attachments`, `get_certificate`) – provide concise service APIs for both JSON (WSJF) and XML (WSXF) report pipelines.
- **Open Questions:** Should the factory/query/attachment responsibilities be split into smaller services (e.g., `ReportSubmissionService`, `ReportQueryService`, `ReportAttachmentService`) to reduce the surface area of this 400-line class and make domain knowledge more discoverable?

## 2. Model Surface
- **Model Files:**
  - `models.py` – `WATSFilter`, `ReportHeader`, `Attachment` live here alongside a handful of mostly-wire-schema fields.
  - `report_models/report.py` – defines `Report` (extends `WATSBase`), the helper methods (`add_misc_info`, `add_sub_unit`, `add_asset`), and the `ReportStatus` enum used by UUT/UUR.
  - `report_models/wats_base.py` – shared base for report models that injects context defaults and configures Pydantic for alias-based serialization.
  - `report_models/uut/` – contains `UUTReport`, `UUTInfo`, `SequenceCall`, step definitions, etc.
  - `report_models/uur/` – houses `UURReport` (650+ lines), `UURInfo`, fail codes, failures, attachments, part info, misc info, `UURSubUnit`, and supporting helpers.
- **Class Summary:**
  - `WATSFilter`/`ReportHeader` – encapsulate query filters and listing payloads returned by WATS.
  - `Report` – base shared by UUT/UUR, enforces uuid/type/pn/sn/revision fields, keeps `start`/`start_utc` in sync, and contains helpers to add misc infos/assets/sub-units.
  - `UUTReport` – adds `.root` (`SequenceCall`) representing the step tree and `UUTInfo` metadata.
  - `UURReport` – contains complex logic for fail codes, part infos, attachments, and inherits `Report`; this class mirrors the WATS .NET UUR API to maximize compatibility.
- **Model Quality Notes:**
  - `models.py` and `report_models/report.py` currently group filters, headers, and base helpers into a single file; splitting them into `/models/filters.py`, `/models/headers.py`, and `/models/base.py` would keep each file focused and ready for reuse.
  - `UURReport` blends domain logic (fail code navigation, attachment bookkeeping) with schema definition and already exceeds 600 lines. Consider extracting behaviors (fail code helpers, part info management) into helper modules or service classes so the dataclass stays declarative.
  - The existing `/report_models/uut` and `/report_models/uur` directories are a good start, but we may want to reorganize the top-level `report_models` folder into a `/models/` package per module for consistency across domains.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
ReportService --> ReportRepository --> HttpClient (GET/POST/WSJF/WSXF/Attachment)
ReportService --> UUTReport / UURReport
Report --> WATSBase
UUTReport --> SequenceCall (root step tree) and UUTInfo
UURReport --> UURInfo, UURSubUnit, Failure, UURAttachment, MiscUURInfo
```

- **Refactor Ideas:**
  - `ReportService` could be split into smaller responsibility-based helpers (submission, querying, attachments). Each helper would keep domain knowledge about WATS expectations (dual process codes, `uurInfo` fields) in a more focused location.
  - Move `WATSFilter`, `ReportHeader`, and attachment helpers into a dedicated `/models/` package so every domain follows the same structure (e.g., `pywats/domains/report/models/filter.py`).
  - Extract the massive `UURReport` logic into submodules (`failures.py`, `part_info_manager.py`, `attachment_registry.py`) that can be tested and evolved independently.

## 4. Inline Documentation
- Added domain context to `_resolve_station` (station dimensions feed WATS analytics) and to `create_uut_report`/`create_uur_report` docstrings (links between `operation_type`, `repair_process_code`, and WATS processCode tables).
- Documented in `_copy_sub_units_to_uur` why idx/parentIdx matter for WATS repair hierarchies and clarified `ReportRepository.post_wsjf` about WSJF/uurInfo requirements, along with notes for `get_wsjf` on how the API signals repair vs test reports.

## 5. Acceptance Testing
- Created `tests/test_report_acceptance.py`.
  1. `test_create_uut_report_resolves_station` – verifies `ReportService` honors the station provider and embeds resolved values before submitting to WATS.
  2. `test_create_uur_report_from_uut_copies_sub_units` – ensures UUT sub-units copy into the resulting UUR, the repair `process_code` stays at 500, and `uur_info.test_operation_code` retains the failed operation.
  3. `test_submit_report_uses_repository` – exercises the WSJF submission pipeline with a stub repository to confirm `ReportService` hands the assembled `UUTReport` to `ReportRepository.post_wsjf` and returns the repository-provided ID.

## 6. Pending Work
- Next steps: expand acceptance tests to cover repository helpers (WSXF uploads, attachment downloads) using mocked `HttpClient` responses, and consider refactoring the UUR model logic into smaller helpers.
- Blockers: need to decide on the reorganization strategy for the massive `UURReport` file before splitting into `/models/` directories to avoid duplicate imports.
