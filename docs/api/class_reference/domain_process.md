# pywats.domains.process - Class Reference

Auto-generated class reference for `pywats.domains.process`.

---

## `process.async_repository`

### `AsyncProcessRepository`

_Async Process data access layer._

---

## `process.async_service`

### `AsyncProcessService`

_Async Process business logic layer with enhanced TTL caching._

**Class Variables:**
- `DEFAULT_CACHE_TTL`
- `DEFAULT_TEST_PROCESS_CODE`
- `DEFAULT_REPAIR_PROCESS_CODE`

**Properties:**
- `cache_stats`
- `cache_ttl`
- `last_refresh`
- `refresh_interval`

**Methods:**
- `refresh_interval(value: float) -> Any`

---

## `process.models`

### `FailureCodeInfo(NamedTuple)`

_Flattened failure code info for easy lookup._

**Class Variables:**
- `category: str`
- `code: str`
- `guid: UUID`
- `category_guid: UUID`

---

### `ProcessInfo(PyWATSModel)`

_Process/operation information._

**Class Variables:**
- `code: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`
- `is_test_operation: bool`
- `is_repair_operation: bool`
- `is_wip_operation: bool`
- `process_id: Optional[...]`
- `process_index: Optional[...]`
- `state: Optional[...]`
- `properties: Optional[...]`
- `model_config`

---

### `RepairCategory(PyWATSModel)`

_Repair category (fail code category)._

**Class Variables:**
- `guid: UUID`
- `description: str`
- `selectable: bool`
- `sort_order: int`
- `failure_type: int`
- `image_constraint: Optional[...]`
- `status: int`
- `fail_codes: List[...]`

---

### `RepairOperationConfig(PyWATSModel)`

_Repair operation configuration._

**Class Variables:**
- `description: str`
- `uut_required: int`
- `comp_ref_mask: Optional[...]`
- `comp_ref_mask_description: Optional[...]`
- `bom_constraint: Optional[...]`
- `bom_required: int`
- `vendor_required: int`
- `categories: List[...]`
- `misc_infos: List[...]`

**Properties:**
- `failure_codes`

**Methods:**
- `get_fail_code_by_name(category: str, code: str) -> Optional[...]`
- `validate_fail_code(category: str, code: str) -> tuple[...]`

---
