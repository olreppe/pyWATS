# pywats.domains.analytics - Class Reference

Auto-generated class reference for `pywats.domains.analytics`.

---

## `analytics.async_repository`

### `AsyncAnalyticsRepository`

_Async Analytics/Statistics data access layer._

---

## `analytics.async_service`

### `AsyncAnalyticsService`

_Async Analytics/Statistics business logic layer._

---

## `analytics.enums`

### `AlarmType(IntEnum)`

_Types of WATS alarms and notifications._

**Class Variables:**
- `REPORT`
- `YIELD_VOLUME`
- `SERIAL_NUMBER`
- `MEASUREMENT`
- `ASSET`

---

### `Dimension(str, Enum)`

_Dimension fields for dynamic yield/repair queries._

**Class Variables:**
- `PART_NUMBER`
- `PRODUCT_NAME`
- `PRODUCT_GROUP`
- `REVISION`
- `STATION_NAME`
- `LOCATION`
- `PURPOSE`
- `TEST_OPERATION`
- `PROCESS_CODE`
- `PERIOD`
- `SW_FILENAME`
- `SW_VERSION`
- `LEVEL`
- `BATCH_NUMBER`
- `OPERATOR`
- `FIXTURE_ID`
- `SOCKET_INDEX`
- `ERROR_CODE`
- `STEP_CAUSED_UUT_FAILURE`
- `STEP_PATH_CAUSED_UUT_FAILURE`
- `MISC_INFO_DESCRIPTION`
- `MISC_INFO_STRING`
- `ASSET_SERIAL_NUMBER`
- `ASSET_NAME`
- `UNIT_TYPE`

---

### `DimensionBuilder`

_Builder for constructing dimension query strings with type safety._

**Methods:**
- `add(dimension: Union[...], direction: Optional[...]) -> Any`
- `add_all() -> Any`
- `build() -> str`
- `clear() -> Any`
- `top_failing_products(cls) -> Any`
- `yield_by_product(cls, include_period: bool) -> Any`
- `yield_by_station(cls, include_period: bool) -> Any`

---

### `KPI(str, Enum)`

_Key Performance Indicators for yield/repair queries._

**Class Variables:**
- `UNIT_COUNT`
- `FP_COUNT`
- `SP_COUNT`
- `TP_COUNT`
- `LP_COUNT`
- `FP_FAIL_COUNT`
- `SP_FAIL_COUNT`
- `TP_FAIL_COUNT`
- `LP_FAIL_COUNT`
- `FPY`
- `SPY`
- `TPY`
- `LPY`
- `PPM_FPY`
- `PPM_SPY`
- `PPM_TPY`
- `PPM_LPY`
- `PPM_TEST_YIELD`
- `TEST_YIELD_COUNT`
- `TEST_REPORT_COUNT`
- `TEST_YIELD`
- `RETEST_COUNT`
- `FIRST_UTC`
- `LAST_UTC`

---

### `ProcessType(IntEnum)`

_Process/operation categories._

**Class Variables:**
- `TEST`
- `REPAIR`
- `CALIBRATION`

---

### `RepairDimension(str, Enum)`

_Additional dimensions specific to repair statistics._

**Class Variables:**
- `REPAIR_OPERATION`
- `REPAIR_CODE`
- `REPAIR_CATEGORY`
- `REPAIR_TYPE`
- `COMPONENT_REF`
- `COMPONENT_NUMBER`
- `COMPONENT_REVISION`
- `COMPONENT_VENDOR`
- `COMPONENT_DESCRIPTION`
- `FUNCTION_BLOCK`
- `REFERENCED_STEP`
- `REFERENCED_STEP_PATH`
- `TEST_PERIOD`
- `TEST_LEVEL`
- `TEST_STATION_NAME`
- `TEST_LOCATION`
- `TEST_PURPOSE`
- `TEST_OPERATOR`

---

### `RepairKPI(str, Enum)`

_KPIs specific to repair statistics._

**Class Variables:**
- `REPAIR_REPORT_COUNT`
- `REPAIR_COUNT`

---

### `YieldDataType(IntEnum)`

_Types of yield data calculations._

**Class Variables:**
- `FIRST_PASS`
- `FINAL`
- `ROLLED`

---

## `analytics.models`

### `AggregatedMeasurement(PyWATSModel)`

_Represents aggregated measurement statistics._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `count: Optional[...]`
- `min: Optional[...]`
- `max: Optional[...]`
- `avg: Optional[...]`
- `stdev: Optional[...]`
- `variance: Optional[...]`
- `limit_low: Optional[...]`
- `limit_high: Optional[...]`
- `cpk: Optional[...]`
- `cp: Optional[...]`
- `cp_lower: Optional[...]`
- `cp_upper: Optional[...]`
- `unit: Optional[...]`

---

### `AlarmLog(PyWATSModel)`

_Represents a triggered alarm or notification log entry._

**Class Variables:**
- `model_config`
- `log_id: Optional[...]`
- `name: Optional[...]`
- `log_date: Optional[...]`
- `trigger_id: Optional[...]`
- `type: Optional[...]`
- `state: Optional[...]`
- `grouping_set: Optional[...]`
- `calculations_string: Optional[...]`
- `client_group_ids: Optional[...]`
- `product_selection_ids: Optional[...]`
- `part_number: Optional[...]`
- `product_name: Optional[...]`
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `report_guid: Optional[...]`
- `serial_number: Optional[...]`
- `revision: Optional[...]`
- `station_name: Optional[...]`
- `operator: Optional[...]`
- `result: Optional[...]`
- `start_utc: Optional[...]`
- `fpy: Optional[...]`
- `spy: Optional[...]`
- `tpy: Optional[...]`
- `lpy: Optional[...]`
- `test_yield: Optional[...]`
- `fpy_trend: Optional[...]`
- `spy_trend: Optional[...]`
- `tpy_trend: Optional[...]`
- `lpy_trend: Optional[...]`
- `test_yield_trend: Optional[...]`
- `uut_count: Optional[...]`
- `unit_count: Optional[...]`
- `fp_count: Optional[...]`
- `lp_count: Optional[...]`
- `retest_count: Optional[...]`
- `sequence_count: Optional[...]`
- `sequential_match: Optional[...]`
- `free: Optional[...]`
- `reserved: Optional[...]`
- `serial_number_type: Optional[...]`
- `cp: Optional[...]`
- `cpk: Optional[...]`
- `min: Optional[...]`
- `max: Optional[...]`
- `avg: Optional[...]`
- `stdev: Optional[...]`
- `measurement_path: Optional[...]`
- `asset_name: Optional[...]`
- `asset_serial_number: Optional[...]`
- `type_id: Optional[...]`
- `asset_state: Optional[...]`
- `bubbled_status: Optional[...]`
- `tags: Optional[...]`
- `is_days_since_calibration_unknown: Optional[...]`
- `is_days_since_maintenance_unknown: Optional[...]`

**Properties:**
- `alarm_type_name`
- `fpy_percent`
- `fpy_trend_percent`

---

### `LevelInfo(PyWATSModel)`

_Represents production level information._

**Class Variables:**
- `level_id: Optional[...]`
- `level_name: Optional[...]`

---

### `MeasurementData(PyWATSModel)`

_Represents individual measurement data points._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `report_id: Optional[...]`
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `value: Optional[...]`
- `limit_low: Optional[...]`
- `limit_high: Optional[...]`
- `unit: Optional[...]`
- `status: Optional[...]`
- `timestamp: Optional[...]`

**Properties:**
- `step_path_display`

---

### `MeasurementListItem(PyWATSModel)`

_Represents measurement list data from the MeasurementList endpoint._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `report_id: Optional[...]`
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `value: Optional[...]`
- `string_value: Optional[...]`
- `limit_low: Optional[...]`
- `limit_high: Optional[...]`
- `unit: Optional[...]`
- `status: Optional[...]`
- `timestamp: Optional[...]`
- `station_name: Optional[...]`
- `model_config`

---

### `OeeAnalysisResult(PyWATSModel)`

_Represents OEE (Overall Equipment Effectiveness) analysis results._

**Class Variables:**
- `oee: Optional[...]`
- `availability: Optional[...]`
- `performance: Optional[...]`
- `quality: Optional[...]`
- `total_time: Optional[...]`
- `run_time: Optional[...]`
- `down_time: Optional[...]`
- `planned_production_time: Optional[...]`
- `total_count: Optional[...]`
- `good_count: Optional[...]`
- `reject_count: Optional[...]`
- `ideal_cycle_time: Optional[...]`
- `actual_cycle_time: Optional[...]`
- `period: Optional[...]`
- `part_number: Optional[...]`
- `station_name: Optional[...]`

---

### `ProcessInfo(PyWATSModel)`

_Represents process/test operation information._

**Class Variables:**
- `code: Optional[...]`
- `name: Optional[...]`
- `description: Optional[...]`
- `is_test_operation: bool`
- `is_repair_operation: bool`
- `is_wip_operation: bool`
- `process_index: Optional[...]`
- `state: Optional[...]`

---

### `ProductGroup(PyWATSModel)`

_Represents a product group._

**Class Variables:**
- `product_group_id: Optional[...]`
- `product_group_name: Optional[...]`

---

### `RepairHistoryRecord(PyWATSModel)`

_Represents a repair history record for a specific part._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `report_id: Optional[...]`
- `repair_date: Optional[...]`
- `fail_step_name: Optional[...]`
- `fail_step_path: Optional[...]`
- `fail_code: Optional[...]`
- `repair_code: Optional[...]`
- `symptom: Optional[...]`
- `cause: Optional[...]`
- `action: Optional[...]`

---

### `RepairStatistics(PyWATSModel)`

_Represents repair statistics data from dynamic repair analysis._

**Class Variables:**
- `model_config`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `product_group: Optional[...]`
- `product_name: Optional[...]`
- `unit_type: Optional[...]`
- `repair_operation: Optional[...]`
- `station_name: Optional[...]`
- `test_operation: Optional[...]`
- `period: Optional[...]`
- `level: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `operator: Optional[...]`
- `misc_info_description: Optional[...]`
- `misc_info_string: Optional[...]`
- `repair_category: Optional[...]`
- `repair_type: Optional[...]`
- `component_ref: Optional[...]`
- `component_number: Optional[...]`
- `component_revision: Optional[...]`
- `component_vendor: Optional[...]`
- `component_description: Optional[...]`
- `function_block: Optional[...]`
- `referenced_step: Optional[...]`
- `referenced_step_path: Optional[...]`
- `test_period: Optional[...]`
- `test_level: Optional[...]`
- `test_station_name: Optional[...]`
- `test_location: Optional[...]`
- `test_purpose: Optional[...]`
- `test_operator: Optional[...]`
- `batch_number: Optional[...]`
- `sw_filename: Optional[...]`
- `sw_version: Optional[...]`
- `repair_report_count: Optional[...]`
- `repair_count: Optional[...]`
- `total_count: Optional[...]`
- `repair_rate: Optional[...]`
- `fail_code: Optional[...]`
- `repair_code: Optional[...]`

---

### `StepAnalysisRow(PyWATSModel)`

_Represents a single step (and optional measurement) KPI row._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `step_type: Optional[...]`
- `step_group: Optional[...]`
- `step_count: Optional[...]`
- `step_passed_count: Optional[...]`
- `step_done_count: Optional[...]`
- `step_skipped_count: Optional[...]`
- `step_failed_count: Optional[...]`
- `step_error_count: Optional[...]`
- `step_terminated_count: Optional[...]`
- `step_other_count: Optional[...]`
- `step_failed_error_terminated_count: Optional[...]`
- `step_caused_uut_failed_error_terminated: Optional[...]`
- `step_caused_uut_failed: Optional[...]`
- `step_caused_uut_error: Optional[...]`
- `step_caused_uut_terminated: Optional[...]`
- `limit1: Optional[...]`
- `limit1_wof: Optional[...]`
- `limit2: Optional[...]`
- `limit2_wof: Optional[...]`
- `comp_operator: Optional[...]`
- `step_time_avg: Optional[...]`
- `step_time_max: Optional[...]`
- `step_time_min: Optional[...]`
- `measure_name: Optional[...]`
- `measure_count: Optional[...]`
- `measure_count_wof: Optional[...]`
- `min: Optional[...]`
- `min_wof: Optional[...]`
- `max: Optional[...]`
- `max_wof: Optional[...]`
- `avg: Optional[...]`
- `avg_wof: Optional[...]`
- `stdev: Optional[...]`
- `stdev_wof: Optional[...]`
- `var: Optional[...]`
- `var_wof: Optional[...]`
- `cpk: Optional[...]`
- `cpk_wof: Optional[...]`
- `cp: Optional[...]`
- `cp_wof: Optional[...]`
- `cp_lower: Optional[...]`
- `cp_lower_wof: Optional[...]`
- `cp_upper: Optional[...]`
- `cp_upper_wof: Optional[...]`
- `sigma_high_3: Optional[...]`
- `sigma_high_3_wof: Optional[...]`
- `sigma_low_3: Optional[...]`
- `sigma_low_3_wof: Optional[...]`

**Properties:**
- `step_path_display`

---

### `StepStatusItem(PyWATSModel)`

_Represents step status data from the StepStatusList endpoint._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `step_type: Optional[...]`
- `step_group: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `pass_count: Optional[...]`
- `fail_count: Optional[...]`
- `total_count: Optional[...]`
- `status: Optional[...]`
- `timestamp: Optional[...]`
- `serial_number: Optional[...]`
- `report_id: Optional[...]`
- `model_config`

---

### `TopFailedStep(PyWATSModel)`

_Represents a top failed step from failure analysis._

**Class Variables:**
- `step_name: Optional[...]`
- `step_path: Optional[...]`
- `step_type: Optional[...]`
- `step_group: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `product_group: Optional[...]`
- `fail_count: Optional[...]`
- `total_count: Optional[...]`
- `fail_rate: Optional[...]`
- `first_fail_date: Optional[...]`
- `last_fail_date: Optional[...]`

**Properties:**
- `step_path_display`

---

### `UnitFlowFilter(PyWATSModel)`

_Filter parameters for Unit Flow queries._

**Class Variables:**
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `serial_number: Optional[...]`
- `serial_numbers: Optional[...]`
- `station_name: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `date_from: Optional[...]`
- `date_to: Optional[...]`
- `process_codes: Optional[...]`
- `include_passed: Optional[...]`
- `include_failed: Optional[...]`
- `split_by: Optional[...]`
- `unit_order: Optional[...]`
- `show_list: Optional[...]`
- `hide_list: Optional[...]`
- `expand_operations: Optional[...]`

**Methods:**
- `serialize_datetime(v: Optional[...]) -> Optional[...]`

---

### `UnitFlowLink(PyWATSModel)`

_Represents a link (edge) between nodes in the unit flow diagram._

**Class Variables:**
- `id: Optional[...]`
- `source_id: Optional[...]`
- `target_id: Optional[...]`
- `source_name: Optional[...]`
- `target_name: Optional[...]`
- `unit_count: Optional[...]`
- `pass_count: Optional[...]`
- `fail_count: Optional[...]`
- `avg_time: Optional[...]`
- `is_visible: Optional[...]`
- `model_config`

---

### `UnitFlowNode(PyWATSModel)`

_Represents a node in the unit flow diagram._

**Class Variables:**
- `id: Optional[...]`
- `name: Optional[...]`
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `station_name: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `unit_count: Optional[...]`
- `pass_count: Optional[...]`
- `fail_count: Optional[...]`
- `yield_percent: Optional[...]`
- `avg_time: Optional[...]`
- `is_expanded: Optional[...]`
- `is_visible: Optional[...]`
- `level: Optional[...]`
- `parent_id: Optional[...]`
- `model_config`

---

### `UnitFlowResult(PyWATSModel)`

_Complete result from a Unit Flow query._

**Class Variables:**
- `nodes: Optional[...]`
- `links: Optional[...]`
- `units: Optional[...]`
- `total_units: Optional[...]`
- `model_config`

---

### `UnitFlowUnit(PyWATSModel)`

_Represents a unit in the unit flow analysis._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `status: Optional[...]`
- `start_time: Optional[...]`
- `end_time: Optional[...]`
- `total_time: Optional[...]`
- `node_path: Optional[...]`
- `current_node: Optional[...]`
- `model_config`

---

### `YieldData(PyWATSModel)`

_Represents yield statistics data._

**Class Variables:**
- `model_config`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `product_name: Optional[...]`
- `product_group: Optional[...]`
- `station_name: Optional[...]`
- `test_operation: Optional[...]`
- `period: Optional[...]`
- `unit_count: Optional[...]`
- `fp_count: Optional[...]`
- `sp_count: Optional[...]`
- `tp_count: Optional[...]`
- `lp_count: Optional[...]`
- `fpy: Optional[...]`
- `spy: Optional[...]`
- `tpy: Optional[...]`
- `lpy: Optional[...]`

---
