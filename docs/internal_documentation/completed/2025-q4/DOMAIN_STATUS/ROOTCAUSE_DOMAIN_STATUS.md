# ROOTCAUSE Domain Status

> Based on `TEMPLATE_DOMAIN_STATUS.md` and updated for `pywats.domains.rootcause`.

## 1. Service Functions
- **Overview:** `RootCauseService` is the high-level ticketing API that hides `RootCauseRepository` details and accepts either a repository or `HttpClient` for backward compatibility.
- **Key Operations:**
  - Ticket lifecycle helpers (`get_ticket`, `get_tickets`, `get_open_tickets`, `get_active_tickets`, `create_ticket`, `update_ticket`).
  - Workflow helpers (`add_comment`, `change_status`, `assign_ticket`, `archive_tickets`) that build minimal `Ticket` payloads before delegating to `update_ticket`/`archive_tickets`.
  - Attachment helpers (`get_attachment`, `upload_attachment`) for fetching and uploading related files.
- **Open Questions:** Should we split offline ticket mutations (`create_ticket`, `add_comment`, `assign_ticket`) into a `RootCauseCommandService` and leave reads on a `RootCauseQueryService` to better match CQRS patterns?

## 2. Model Surface
- **Model Files:**
  - `models.py` – defines `Ticket`, `TicketUpdate`, and `TicketAttachment` with `pywats.shared` helpers for aliasing and UTC timestamps.
- **Class Summary:**
  - `Ticket` – the aggregate root capturing status, priority, ownership, metadata, history, and pending updates.
  - `TicketUpdate` – nested entries representing history + attachments.
  - `TicketAttachment` – simple DTO describing uploaded files (ID + filename).
- **Model Quality Notes:** The `Ticket` model mixes optional lists (`tags`, `history`) with nearly required workflow metadata; consider splitting the write model (`TicketUpdate`) from the read model to reduce ambiguity about which fields the API requires.

## 3. Architecture & Diagrams
- **Class Relationships:**

```
RootCauseService --> RootCauseRepository --> HttpClient
RootCauseService --> Ticket / TicketUpdate models
```

- **Refactor Ideas:** Introduce a `RootCauseCommandService` for writes and keep the existing service for reads to reduce the need to construct partial `Ticket` objects in both command and query paths.

## 4. Inline Documentation
- **Domain Knowledge Additions:** Docstrings clarify that `TicketStatus` flags are bitmasks and note that only solved tickets can be archived.
- **Doc Gaps:** The attachment helpers could use more detail on supported file sizes/content types to educate callers when uploads will be rejected by the server.

## 5. Acceptance Testing
- **Test Scenarios:**
  1. `test_create_ticket_routes_to_repository` – verifies `create_ticket` builds a `Ticket` (with optional report UUID) and saves it via the repository stub.
  2. `test_assign_ticket_updates_assignee` – confirms `assign_ticket` reuses `update_ticket` and that the repository receives the `assignee` field.
  Both tests are in [tests/acceptance/rootcause/test_rootcause_acceptance.py](tests/acceptance/rootcause/test_rootcause_acceptance.py).
- **Data Setup Notes:** The stub repository captures created/updated tickets and returns placeholder entries for reads.
- **Verification Steps:** Check the stub’s `created` and `updated` attributes for expected subjects and assignees.

## 6. Pending Work
- **Next Steps:** Add acceptance coverage for `archive_tickets` and attachment upload/download flows, including rejection paths when files are missing.
- **Blockers:** Need reproducible ticket IDs and file fixture data from the RootCause UI team before automating attachment scenarios.