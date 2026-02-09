# pywats.domains.rootcause - Class Reference

Auto-generated class reference for `pywats.domains.rootcause`.

---

## `rootcause.async_repository`

### `AsyncRootCauseRepository`

_Async RootCause (Ticketing) data access layer._

---

## `rootcause.async_service`

### `AsyncRootCauseService`

_Async RootCause (Ticketing) business logic layer._

---

## `rootcause.enums`

### `TicketPriority(IntEnum)`

_Ticket priority levels_

**Class Variables:**
- `LOW`
- `MEDIUM`
- `HIGH`

---

### `TicketStatus(IntFlag)`

_Ticket status flags._

**Class Variables:**
- `OPEN`
- `IN_PROGRESS`
- `ON_HOLD`
- `SOLVED`
- `CLOSED`
- `ARCHIVED`

---

### `TicketUpdateType(IntEnum)`

_Type of ticket update/history entry_

**Class Variables:**
- `CONTENT`
- `PROGRESS`
- `PROPERTIES`
- `NOTIFICATION`

---

### `TicketView(IntEnum)`

_Ticket view filter for listing tickets_

**Class Variables:**
- `ASSIGNED`
- `FOLLOWING`
- `ALL`

---

## `rootcause.models`

### `Ticket(PyWATSModel)`

_Represents a RootCause ticket in WATS._

**Class Variables:**
- `ticket_id: Optional[...]`
- `ticket_number: Optional[...]`
- `progress: Optional[...]`
- `owner: Optional[...]`
- `assignee: Optional[...]`
- `subject: Optional[...]`
- `status: Optional[...]`
- `priority: Optional[...]`
- `report_uuid: Optional[...]`
- `created_utc: Optional[...]`
- `updated_utc: Optional[...]`
- `team: Optional[...]`
- `origin: Optional[...]`
- `tags: Optional[...]`
- `history: Optional[...]`
- `update: Optional[...]`

---

### `TicketAttachment(PyWATSModel)`

_Represents an attachment in a RootCause ticket._

**Class Variables:**
- `attachment_id: Optional[...]`
- `filename: Optional[...]`

---

### `TicketUpdate(PyWATSModel)`

_Represents an update/history entry in a RootCause ticket._

**Class Variables:**
- `update_id: Optional[...]`
- `update_utc: Optional[...]`
- `update_user: Optional[...]`
- `content: Optional[...]`
- `update_type: Optional[...]`
- `attachments: Optional[...]`

---
