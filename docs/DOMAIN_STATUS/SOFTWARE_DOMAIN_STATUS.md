# SOFTWARE Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and updated for `pywats.domains.software`.

## 1. Service Functions
- **Overview:** `SoftwareService` manages software distribution packages, exposing CRUD operations, status transitions (Draft ⇄ Pending ⇄ Released ⇄ Revoked), file uploads, and virtual folder queries while hiding the HTTP plumbing of `SoftwareRepository`.
- **Key Operations:**
  - Package lifecycle helpers (`get_packages`, `get_package`, `create_package`, `update_package`, `delete_package`, `delete_package_by_name`).
  - Status transition helpers (`submit_for_review`, `return_to_draft`, `release_package`, `revoke_package`) that reuse `update_package_status` for clarity.
  - File/virtual folder helpers (`get_package_files`, `upload_zip`, `update_file_attribute`, `get_virtual_folders`).
- **Open Questions:** Should the zip upload flow be split into a dedicated `PackageFileService` so the core service stays focused on metadata and the upload details live near `PackageFile` models?

## 2. Model Surface
- **Model Files:**
  - `models.py` – defines `Package`, `PackageFile`, `PackageTag`, and `VirtualFolder`, all backing the `SoftwareRepository` payloads.
- **Class Summary:**
  - `Package` – root entity with versioning, status enum, root path, tags, and optional file listings.
  - `PackageFile` – describes each uploaded file with aliases for JSON fields and optional checksum/attributes.
  - `PackageTag`/`VirtualFolder` – metadata helpers for filtering and browsing packages.
- **Model Quality Notes:** `PackageFile` stores multiple alias combinations (fileId/id, filename/name) to stay compatible with different API versions; keep these alias rules documented for any future schema cleanup.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
SoftwareService --> SoftwareRepository --> HttpClient
SoftwareService --> Package / PackageFile models
``` 

- **Refactor Ideas:** Consider introducing `PackageStatusService` for status transitions and a `PackageFileService` for uploads so each class can be smaller and more focused.

## 4. Inline Documentation
- **Domain Knowledge Additions:** Many docstrings now mention which statuses can transition (e.g., Draft → Pending, Pending → Released) so callers do not accidentally attempt invalid moves.
- **Doc Gaps:** `upload_zip` could note the server limits on zip size and the requirement that files must be inside a folder (no root-level files) to align with API constraints.

## 5. Acceptance Testing
- **Test Scenarios:**
  1. `test_create_package_calls_repository` – ensures the service builds `Package` metadata (including tags) and hands it to `SoftwareRepository.create_package`.
  2. `test_submit_for_review_updates_status` – confirms `submit_for_review` flips the status to `PackageStatus.PENDING` via `update_package_status`.
  Tests live in [tests/acceptance/software/test_software_acceptance.py](tests/acceptance/software/test_software_acceptance.py).
- **Data Setup Notes:** A dummy repository records the created package, status updates, and deleted IDs so the tests can assert the flows without hitting HTTP.
- **Verification Steps:** Validate the stub’s captured calls rather than hitting real endpoints.

## 6. Pending Work
- **Next Steps:** Extend acceptance coverage for file uploads (`upload_zip`) and status rollbacks (`return_to_draft`, `release_package`) including failure handling.
- **Blockers:** Need sample binary fixtures (zip blobs) before writing deterministic upload tests.