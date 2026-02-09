# pywats.shared - Class Reference

Auto-generated class reference for `pywats.shared`.

---

## `shared.base_model`

### `PyWATSModel(BaseModel)`

_Base class for all pyWATS models._

**Class Variables:**
- `model_config`

---

## `shared.common_types`

### `ChangeType(IntEnum)`

_Change type for settings._

**Class Variables:**
- `NONE`
- `ADD`
- `UPDATE`
- `DELETE`
- `UNKNOWN_4`
- `UNKNOWN_5`
- `UNKNOWN_6`

---

### `Setting(PyWATSModel)`

_Key-value setting used for tags/custom data._

**Class Variables:**
- `key: str`
- `value: Optional[...]`
- `change: Optional[...]`

---

## `shared.enums`

### `CompOp(str, Enum)`

_Comparison operators for numeric limit steps._

**Class Variables:**
- `LOG`
- `EQ`
- `EQT`
- `NE`
- `LT`
- `LE`
- `GT`
- `GE`
- `CASESENSIT`
- `IGNORECASE`
- `GTLT`
- `GTLE`
- `GELT`
- `GELE`
- `LTGT`
- `LTGE`
- `LEGT`
- `LEGE`

**Methods:**
- `evaluate(value: Any, low_limit: Any, high_limit: Any) -> bool`
- `get_limits_requirement() -> tuple[...]`
- `validate_limits(low_limit: Any, high_limit: Any) -> bool`

---

### `QueueItemStatus(str, Enum)`

_Unified status for queue items across all queue implementations._

**Class Variables:**
- `PENDING`
- `PROCESSING`
- `COMPLETED`
- `FAILED`
- `SUSPENDED`

**Properties:**
- `can_process`
- `is_active`
- `is_terminal`

---

### `RunFilter(IntEnum)`

_Run filter for step/measurement analysis._

**Class Variables:**
- `FIRST`
- `SECOND`
- `THIRD`
- `LAST`
- `ALL`

---

### `SortDirection(str, Enum)`

_Sort direction for dimension queries._

**Class Variables:**
- `ASC`
- `DESC`

---

### `StatusFilter(str, Enum)`

_Status filter values for querying reports with flexible string conversion._

**Class Variables:**
- `PASSED`
- `FAILED`
- `ERROR`
- `TERMINATED`
- `DONE`
- `SKIPPED`

**Properties:**
- `full_name`
- `is_failure`
- `is_passing`

---

### `StepType(str, Enum)`

_Test step types in WATS._

**Class Variables:**
- `SEQUENCE_CALL`
- `NUMERIC_LIMIT`
- `STRING_VALUE`
- `PASS_FAIL`
- `MULTIPLE_NUMERIC`
- `ACTION`
- `MESSAGE_POPUP`
- `CALL_EXECUTABLE`
- `LABEL`
- `GOTO`
- `FLOW_CONTROL`
- `STATEMENT`
- `PROPERTY_LOADER`
- `GENERIC`
- `UNKNOWN`

---

## `shared.odata`

### `ODataFilterBuilder`

_Fluent builder for constructing OData filter expressions._

**Methods:**
- `build() -> str`
- `contains(value: str) -> Any`
- `endswith(value: str) -> Any`
- `eq(value: Any) -> Any`
- `field(name: str) -> Any`
- `ge(value: Any) -> Any`
- `gt(value: Any) -> Any`
- `in_list(values: List[...]) -> Any`
- `is_not_null() -> Any`
- `is_null() -> Any`
- `le(value: Any) -> Any`
- `lt(value: Any) -> Any`
- `ne(value: Any) -> Any`
- `or_group(builder: Any) -> Any`
- `raw(expression: str) -> Any`
- `startswith(value: str) -> Any`
- `use_and() -> Any`
- `use_or() -> Any`

---

## `shared.paths`

### `MeasurementPath(StepPath)`

_Represents a measurement path in WATS._

**Properties:**
- `measurement_name`
- `step_path`

---

### `StepPath`

_Represents a test step path in WATS._

**Properties:**
- `api_format`
- `display`
- `name`
- `parent`
- `parts`

**Methods:**
- `from_parts(cls) -> Any`

---

## `shared.result`

### `ErrorCode(str, Enum)`

_Standard error codes for pyWATS operations._

**Class Variables:**
- `INVALID_INPUT`
- `MISSING_REQUIRED_FIELD`
- `INVALID_FORMAT`
- `VALUE_OUT_OF_RANGE`
- `NOT_FOUND`
- `ALREADY_EXISTS`
- `CONFLICT`
- `OPERATION_FAILED`
- `SAVE_FAILED`
- `DELETE_FAILED`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `CONNECTION_ERROR`
- `TIMEOUT`
- `API_ERROR`
- `UNKNOWN_ERROR`

---

### `Failure(BaseModel)`

_Represents a failed operation with structured error information._

**Class Variables:**
- `model_config`
- `error_code: str`
- `message: str`
- `details: Dict[...]`
- `suggestions: List[...]`

**Properties:**
- `is_failure`
- `is_success`
- `value`

---

### `Success(BaseModel, Unknown)`

_Represents a successful operation with a value._

**Class Variables:**
- `model_config`
- `value: Any`
- `message: str`

**Properties:**
- `error_code`
- `is_failure`
- `is_success`

---

## `shared.stats`

### `BatchResult`

_Result of a batch operation._

**Class Variables:**
- `total: int`
- `success: int`
- `failed: int`
- `results: List[...]`
- `errors: Dict[...]`

**Properties:**
- `all_succeeded`
- `success_rate`

---

### `CacheStats`

_Statistics about a cache's current state._

**Class Variables:**
- `hits: int`
- `misses: int`
- `size: int`
- `max_size: Optional[...]`

**Properties:**
- `hit_rate`
- `total_requests`
- `utilization`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `QueueProcessingResult`

_Result of processing a queue of reports._

**Class Variables:**
- `success: int`
- `failed: int`
- `skipped: int`
- `errors: List[...]`

**Properties:**
- `success_rate`
- `total`

**Methods:**
- `to_dict() -> Dict[...]`

---

### `QueueStats`

_Statistics about a queue's current state._

**Class Variables:**
- `pending: int`
- `processing: int`
- `completed: int`
- `failed: int`

**Properties:**
- `active`
- `total`

**Methods:**
- `to_dict() -> Dict[...]`

---
