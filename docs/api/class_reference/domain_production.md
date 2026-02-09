# pywats.domains.production - Class Reference

Auto-generated class reference for `pywats.domains.production`.

---

## `production.async_repository`

### `AsyncProductionRepository`

_Async Production data access layer._

---

## `production.async_service`

### `AsyncProductionService`

_Async Production business logic._

---

## `production.enums`

### `SerialNumberIdentifier(IntEnum)`

_Serial number identifier type._

**Class Variables:**
- `SERIAL_NUMBER`
- `MAC_ADDRESS`
- `IMEI`

---

### `UnitPhaseFlag(IntFlag)`

_Unit phase flags representing lifecycle states._

**Class Variables:**
- `UNKNOWN`
- `UNDER_PRODUCTION`
- `PRODUCTION_REPAIR`
- `SERVICE_REPAIR`
- `FINALIZED`
- `SCRAPPED`
- `EXTENDED_TEST`
- `CUSTOMIZATION`
- `REPAIRED`
- `MISSING`
- `IN_STORAGE`
- `SHIPPED`

---

## `production.models`

### `ProductionBatch(PyWATSModel)`

_Represents a production batch._

**Class Variables:**
- `batch_number: Optional[...]`
- `batch_size: Optional[...]`

---

### `SerialNumberType(PyWATSModel)`

_Represents a serial number type configuration._

**Class Variables:**
- `name: Optional[...]`
- `description: Optional[...]`
- `format: Optional[...]`
- `reg_ex: Optional[...]`
- `identifier: SerialNumberIdentifier`
- `identifier_name: Optional[...]`

---

### `Unit(PyWATSModel)`

_Represents a production unit in WATS._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `parent_serial_number: Optional[...]`
- `batch_number: Optional[...]`
- `serial_date: Optional[...]`
- `current_location: Optional[...]`
- `xml_data: Optional[...]`
- `unit_phase_id: Optional[...]`
- `unit_phase: Optional[...]`
- `process_code: Optional[...]`
- `tags: List[...]`
- `product_revision: Optional[...]`
- `product: Optional[...]`
- `sub_units: List[...]`

---

### `UnitChange(PyWATSModel)`

_Represents a unit change record._

**Class Variables:**
- `id: Optional[...]`
- `unit_serial_number: Optional[...]`
- `new_parent_serial_number: Optional[...]`
- `new_part_number: Optional[...]`
- `new_revision: Optional[...]`
- `new_unit_phase_id: Optional[...]`

---

### `UnitPhase(PyWATSModel)`

_Represents a unit phase in WATS._

**Class Variables:**
- `phase_id: int`
- `code: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`

---

### `UnitVerification(PyWATSModel)`

_Represents unit verification result for a single process._

**Class Variables:**
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `process_index: Optional[...]`
- `status: Optional[...]`
- `start_utc: Optional[...]`
- `station_name: Optional[...]`
- `total_count: Optional[...]`
- `non_passed_count: Optional[...]`
- `repair_count: Optional[...]`

---

### `UnitVerificationGrade(PyWATSModel)`

_Represents complete unit verification grade result._

**Class Variables:**
- `status: Optional[...]`
- `grade: Optional[...]`
- `all_processes_executed_in_correct_order: bool`
- `all_processes_passed_first_run: bool`
- `all_processes_passed_any_run: bool`
- `all_processes_passed_last_run: bool`
- `no_repairs: bool`
- `results: List[...]`

---
