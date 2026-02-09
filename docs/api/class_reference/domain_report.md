# pywats.domains.report - Class Reference

Auto-generated class reference for `pywats.domains.report`.

---

## `report.async_repository`

### `AsyncReportRepository`

_Async Report data access layer._

**Properties:**
- `import_mode`

**Methods:**
- `import_mode(value: ImportMode) -> Any`

---

## `report.async_service`

### `AsyncReportService`

_Async Report business logic._

**Methods:**
- `create_uur_from_uut(uut_report: UUTReport, operator: Optional[...], comment: Optional[...]) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: UUID, test_operation_code_pos: Any) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: UUTReport, test_operation_code_pos: Any) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: Union[...], test_operation_code_pos: Optional[...]) -> UURReport`
- `create_uur_report(uut_or_guid_or_pn: str, test_operation_code_pos: int) -> UURReport`
- `create_uut_report(operator: str, part_number: str, revision: str, serial_number: str, operation_type: int) -> UUTReport`

---

### `StationInfo(Protocol)`

_Protocol for station information provider._

**Class Variables:**
- `name: str`
- `location: str`
- `purpose: str`

---

## `report.enums`

### `DateGrouping(IntEnum)`

_Date grouping options for filters._

**Class Variables:**
- `NONE`
- `YEAR`
- `QUARTER`
- `MONTH`
- `WEEK`
- `DAY`
- `HOUR`

---

### `ImportMode(Enum)`

_Import mode for UUT report creation._

**Class Variables:**
- `Import`
- `Active`

---

### `ReportType(str, Enum)`

_Report type for querying headers._

**Class Variables:**
- `UUT`
- `UUR`

---

## `report.models`

### `AttachmentMetadata(PyWATSModel)`

_Metadata for a report attachment from API responses._

**Class Variables:**
- `attachment_id: Optional[...]`
- `file_name: Optional[...]`
- `mime_type: Optional[...]`
- `size: Optional[...]`
- `description: Optional[...]`

---

### `HeaderAsset(PyWATSModel)`

_Asset info from OData expanded header query._

**Class Variables:**
- `serial_number: Optional[...]`
- `running_count: Optional[...]`
- `total_count: Optional[...]`
- `days_since_calibration: Optional[...]`
- `calibration_days_overdue: Optional[...]`

---

### `HeaderMiscInfo(PyWATSModel)`

_Misc info from OData expanded header query._

**Class Variables:**
- `description: Optional[...]`
- `value: Optional[...]`

---

### `HeaderSubUnit(PyWATSModel)`

_Sub-unit info from OData expanded header query._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `part_type: Optional[...]`

---

### `ReportHeader(PyWATSModel)`

_Represents a report header (summary info)._

**Class Variables:**
- `uuid: Optional[...]`
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `batch_number: Optional[...]`
- `report_type: Optional[...]`
- `station_name: Optional[...]`
- `location: Optional[...]`
- `purpose: Optional[...]`
- `process_code: Optional[...]`
- `process_name: Optional[...]`
- `result: Optional[...]`
- `start_utc: Optional[...]`
- `operator: Optional[...]`
- `comment: Optional[...]`
- `execution_time: Optional[...]`
- `sw_filename: Optional[...]`
- `sw_version: Optional[...]`
- `test_socket_index: Optional[...]`
- `fixture_id: Optional[...]`
- `run: Optional[...]`
- `passed_in_run: Optional[...]`
- `receive_count: Optional[...]`
- `report_size: Optional[...]`
- `caused_uut_failure: Optional[...]`
- `caused_uut_failure_path: Optional[...]`
- `error_code: Optional[...]`
- `error_message: Optional[...]`
- `referenced_uut: Optional[...]`
- `test_operation: Optional[...]`
- `root_node_type: Optional[...]`
- `sub_units: Optional[...]`
- `uur_sub_units: Optional[...]`
- `misc_info: Optional[...]`
- `assets: Optional[...]`

---

### `WATSFilter(PyWATSModel)`

_WATS filter for querying reports and statistics._

**Class Variables:**
- `serial_number: Optional[...]`
- `part_number: Optional[...]`
- `revision: Optional[...]`
- `batch_number: Optional[...]`
- `station_name: Optional[...]`
- `test_operation: Optional[...]`
- `status: Optional[...]`
- `yield_value: Optional[...]`
- `misc_description: Optional[...]`
- `misc_value: Optional[...]`
- `misc_info_description: Optional[...]`
- `misc_info_string: Optional[...]`
- `asset_serial_number: Optional[...]`
- `asset_name: Optional[...]`
- `product_group: Optional[...]`
- `level: Optional[...]`
- `sw_filename: Optional[...]`
- `sw_version: Optional[...]`
- `socket: Optional[...]`
- `date_from: Optional[...]`
- `date_to: Optional[...]`
- `date_grouping: Optional[...]`
- `period_count: Optional[...]`
- `include_current_period: Optional[...]`
- `max_count: Optional[...]`
- `min_count: Optional[...]`
- `top_count: Optional[...]`
- `dimensions: Optional[...]`
- `run: Optional[...]`
- `measurement_paths: Optional[...]`

**Methods:**
- `normalize_date_grouping(cls, v: object) -> object`
- `normalize_measurement_paths(cls, v: object) -> object`
- `normalize_run(cls, v: object) -> object`
- `normalize_status(cls, v: object) -> object`
- `serialize_datetime(v: Optional[...]) -> Optional[...]`

---

## `report.report_models.asset`

### `Asset(WATSBase)`

_Represents test equipment or assets used during testing._

**Class Variables:**
- `sn: str`
- `asset_type: Optional[...]`
- `pn: Optional[...]`
- `usage_count: Optional[...]`
- `calibration_date: Optional[...]`
- `calibration_due: Optional[...]`

**Methods:**
- `validate_sn(cls, v: str) -> str`

---

### `AssetStats(WATSBase)`

_Statistics about an asset._

**Class Variables:**
- `sn: Optional[...]`
- `running_count: Optional[...]`
- `running_count_exceeded: Optional[...]`
- `total_count: Optional[...]`
- `total_count_exceeded: Optional[...]`
- `days_since_calibration: Optional[...]`
- `is_days_since_calibration_unknown: Optional[...]`
- `calibration_days_overdue: Optional[...]`
- `days_since_maintenance: Optional[...]`
- `is_days_since_maintenance_unknown: Optional[...]`
- `maintenance_days_overdue: Optional[...]`
- `message: Optional[...]`

---

## `report.report_models.binary_data`

### `AdditionalData(WATSBase)`

_A collection of additional step, header, or station data._

**Class Variables:**
- `name: str`
- `props: List[...]`

---

### `AdditionalDataArray(WATSBase)`

_Information about array in additional data._

**Class Variables:**
- `dimension: int`
- `type: str`
- `indexes: List[...]`

---

### `AdditionalDataArrayIndex(WATSBase)`

_Information about an index in an array._

**Class Variables:**
- `text: str`
- `indexes: List[...]`
- `value: Optional[...]`

---

### `AdditionalDataProperty(WATSBase)`

_An additional data property._

**Class Variables:**
- `name: str`
- `type: str`
- `flags: Optional[...]`
- `value: Optional[...]`
- `comment: Optional[...]`
- `num_format: Optional[...]`
- `props: Optional[...]`
- `array: Optional[...]`

---

### `Attachment(WATSBase)`

_File attachment for reports or steps._

**Class Variables:**
- `DEFAULT_MAX_SIZE: ClassVar[...]`
- `name: str`
- `content_type: Optional[...]`
- `data: Optional[...]`
- `description: Optional[...]`
- `failure_idx: Optional[...]`

**Methods:**
- `from_bytes(cls, name: str, content: bytes, content_type: str, failure_idx: Optional[...], max_size: Optional[...]) -> Any`
- `get_bytes() -> bytes`

---

### `BinaryData(WATSBase)`

_Binary data embedded in a report._

**Class Variables:**
- `content_type: str`
- `data: str`
- `name: str`

**Methods:**
- `from_bytes(cls, data: bytes, name: str, content_type: str) -> Any`
- `get_bytes() -> bytes`

---

### `LoopInfo(WATSBase)`

_Loop iteration information for steps executed in loops._

**Class Variables:**
- `index: int`
- `count: Optional[...]`
- `parent: Optional[...]`

---

## `report.report_models.chart`

### `Chart(WATSBase)`

_Chart configuration and data for visualization._

**Class Variables:**
- `chart_type: ChartType`
- `label: str`
- `x_label: str`
- `x_unit: str`
- `y_label: str`
- `y_unit: str`
- `series: List[...]`

**Methods:**
- `AddSeries(name: str, y_label: str, y_values: List[...], x_label: str, x_values: Any) -> ChartSeries`
- `add_series(name: str, x_data: List[...], y_data: List[...], data_type: str) -> ChartSeries`

---

### `ChartSeries(WATSBase)`

_A single data series in a chart._

**Class Variables:**
- `data_type: str`
- `name: str`
- `x_data: Optional[...]`
- `y_data: Optional[...]`

---

## `report.report_models.common_types`

### `ChartType(str, Enum)`

_Chart visualization types._

**Class Variables:**
- `LINE`
- `LINE_LOG_XY`
- `LINE_LOG_X`
- `LINE_LOG_Y`

---

### `FlowType(str, Enum)`

_Flow control step types for GenericStep._

**Class Variables:**
- `NOP`
- `Statement`
- `Label`
- `Goto`
- `WATS_Goto`
- `Flow_If`
- `Flow_ElseIf`
- `Flow_Else`
- `Flow_End`
- `Flow_For`
- `Flow_ForEach`
- `Flow_Break`
- `Flow_Continue`
- `Flow_EndLoop`
- `Flow_While`
- `Flow_DoWhile`
- `Flow_Select`
- `Flow_Case`
- `Flow_Default`
- `Flow_EndSelect`

---

### `ReportStatus(str, Enum)`

_Overall report status with flexible string conversion._

**Class Variables:**
- `Passed`
- `Failed`
- `Done`
- `Error`
- `Terminated`

**Properties:**
- `full_name`
- `is_failure`
- `is_passing`

---

### `ReportType(str, Enum)`

_Report type discriminator._

**Class Variables:**
- `UUT`
- `UUR`

---

### `SequenceCallInfo(WATSBase)`

_Sequence call information for SequenceCall steps._

**Class Variables:**
- `path: str`
- `file_name: str`
- `version: str`

**Methods:**
- `set_defaults(cls, data)`

---

### `StepGroup(str, Enum)`

_Step group classification._

**Class Variables:**
- `Setup`
- `Main`
- `Cleanup`

---

### `StepStatus(str, Enum)`

_Step execution status with flexible string conversion._

**Class Variables:**
- `Passed`
- `Failed`
- `Skipped`
- `Done`
- `Error`
- `Terminated`

**Properties:**
- `full_name`
- `is_failure`
- `is_passing`

---

## `report.report_models.misc_info`

### `MiscInfo(WATSBase)`

_Miscellaneous information key-value pair._

**Class Variables:**
- `id: Optional[...]`
- `description: str`
- `string_value: Optional[...]`
- `numeric_value: Optional[...]`

**Methods:**
- `convert_numeric_to_string() -> Any`

---

### `UURMiscInfo(WATSBase)`

_UUR-specific miscellaneous information._

**Class Variables:**
- `key: str`
- `value: Optional[...]`

---

## `report.report_models.report`

### `Report(WATSBase, Unknown)`

_Base class for all WATS reports._

**Class Variables:**
- `id: UUID`
- `type: str`
- `pn: str`
- `sn: str`
- `rev: str`
- `process_code: int`
- `result: ReportResult`
- `station_name: str`
- `location: str`
- `purpose: str`
- `start: Optional[...]`
- `start_utc: Optional[...]`
- `info: Optional[...]`
- `sub_units: Optional[...]`
- `misc_infos: List[...]`
- `assets: Optional[...]`
- `asset_stats: Optional[...]`
- `binary_data: Optional[...]`
- `additional_data: Optional[...]`
- `origin: Optional[...]`
- `product_name: Optional[...]`
- `process_name: Optional[...]`
- `process_code_format: Optional[...]`

**Methods:**
- `add_asset(sn: str, usage_count: int) -> Asset`
- `add_binary_data(data: bytes, name: str, content_type: str) -> BinaryData`
- `add_misc_info(description: str, value: Any) -> MiscInfo`
- `add_sub_unit(part_type: str, sn: str, pn: str, rev: str) -> SubUnitT`
- `sync_start_times() -> Any`
- `validate_pn(cls, v: str) -> str`
- `validate_sn(cls, v: str) -> str`

---

## `report.report_models.report_info`

### `ReportInfo(WATSBase)`

_Base class for report-specific information._

**Class Variables:**
- `operator: str`
- `comment: Optional[...]`
- `exec_time: Optional[...]`

**Methods:**
- `serialize_exec_time(value: Optional[...]) -> Optional[...]`

---

## `report.report_models.sub_unit`

### `SubUnit(WATSBase)`

_Represents a sub-unit/component of a tested or repaired unit._

**Class Variables:**
- `pn: str`
- `rev: Optional[...]`
- `sn: str`
- `part_type: Optional[...]`

**Methods:**
- `validate_pn(cls, v: str) -> str`
- `validate_sn(cls, v: str) -> str`

---

## `report.report_models.uur.uur_failure`

### `UURFailure(WATSBase)`

_Failure record for UUR sub-units._

**Class Variables:**
- `category: str`
- `code: str`
- `comment: Optional[...]`
- `com_ref: Optional[...]`
- `func_block: Optional[...]`
- `ref_step_id: Optional[...]`
- `ref_step_name: Optional[...]`
- `art_number: Optional[...]`
- `art_rev: Optional[...]`
- `art_vendor: Optional[...]`
- `art_description: Optional[...]`

---

## `report.report_models.uur.uur_info`

### `UURInfo(ReportInfo)`

_UUR-specific information (serialized as 'uur' object)._

**Class Variables:**
- `process_code: Optional[...]`
- `process_code_format: Optional[...]`
- `process_name: Optional[...]`
- `test_operation_code: Optional[...]`
- `test_operation_name: Optional[...]`
- `test_operation_guid: Optional[...]`
- `ref_uut: Optional[...]`
- `confirm_date: Optional[...]`
- `finalize_date: Optional[...]`
- `active: bool`
- `parent: Optional[...]`

**Methods:**
- `get_repair_process_info() -> dict`
- `get_test_operation_info() -> dict`
- `set_dual_process_codes(repair_code: int, repair_name: str, test_code: int, test_name: str, test_guid: Optional[...]) -> Any`
- `sync_process_codes() -> Any`
- `to_dict() -> dict`
- `to_uur_type_dict() -> dict`
- `validate_dual_process_codes() -> tuple[...]`

---

## `report.report_models.uur.uur_report`

### `UURReport(Unknown)`

_Unit Under Repair (UUR) report._

**Class Variables:**
- `type: Literal[...]`
- `info: Optional[...]`
- `sub_units: List[...]`
- `asset_stats: Optional[...]`
- `attachments: List[...]`

**Properties:**
- `all_failures`
- `comment`
- `execution_time`
- `failures`
- `operator`
- `repair_operation_code`
- `repair_process_code`
- `test_operation_code`
- `uut_guid`

**Methods:**
- `add_attachment(attachment: Attachment) -> Any`
- `add_failure(category: str, code: str, comment: Optional[...], component_ref: Optional[...], ref_step_id: Optional[...], sub_unit_idx: Optional[...]) -> UURFailure`
- `add_failure_to_main_unit(category: str, code: str, comment: Optional[...], component_ref: Optional[...]) -> UURFailure`
- `add_failure_to_sub_unit(category: str, code: str, serial_number: Optional[...], idx: Optional[...], comment: Optional[...], component_ref: Optional[...], ref_step_id: Optional[...]) -> UURFailure`
- `add_main_failure(category: str, code: str) -> UURFailure`
- `add_sub_unit(pn: str, sn: str, rev: Optional[...], part_type: str, parent_idx: Optional[...]) -> UURSubUnit`
- `attach_bytes(name: str, content: bytes, mime_type: str) -> Attachment`
- `comment(value: str) -> Any`
- `copy_misc_from_uut(uut_report: Any) -> Any`
- `count_failures() -> int`
- `ensure_main_unit() -> Any`
- `execution_time(value: float) -> Any`
- `get_all_failures() -> List[...]`
- `get_main_unit() -> UURSubUnit`
- `get_sub_unit(idx: int) -> Optional[...]`
- `get_sub_unit_by_idx(idx: int) -> Optional[...]`
- `get_summary() -> dict`
- `link_to_uut(uut_id: UUID) -> Any`
- `operator(value: str) -> Any`
- `set_repair_process(code: int, name: Optional[...]) -> Any`
- `set_test_operation(code: int, name: Optional[...], guid: Optional[...]) -> Any`
- `uut_guid(value: UUID) -> Any`
- `validate_report() -> tuple[...]`

---

## `report.report_models.uur.uur_sub_unit`

### `UURSubUnit(SubUnit)`

_Extended sub-unit for UUR (repair) reports._

**Class Variables:**
- `sn: str`
- `part_type: Optional[...]`
- `idx: int`
- `parent_idx: Optional[...]`
- `position: Optional[...]`
- `replaced_idx: Optional[...]`
- `failures: Optional[...]`

**Methods:**
- `add_failure(category: str, code: str) -> UURFailure`
- `create_main_unit(cls, pn: str, sn: str, rev: str) -> Any`
- `get_failures() -> List[...]`
- `has_failures() -> bool`

---

## `report.report_models.uut.step`

### `Step(WATSBase, ABC)`

_Abstract base class for all WATS test steps._

**Class Variables:**
- `MAX_NAME_LENGTH: ClassVar[...]`
- `parent: Optional[...]`
- `fail_parent_on_failure: bool`
- `step_type: str`
- `name: str`
- `group: str`
- `status: StepStatus`
- `id: Optional[...]`
- `error_code: Optional[...]`
- `error_code_format: Optional[...]`
- `error_message: Optional[...]`
- `report_text: Optional[...]`
- `start: Optional[...]`
- `tot_time: Optional[...]`
- `tot_time_format: Optional[...]`
- `ts_guid: Optional[...]`
- `caused_seq_failure: Optional[...]`
- `caused_uut_failure: Optional[...]`
- `loop: Optional[...]`
- `additional_results: Optional[...]`
- `chart: Optional[...]`
- `attachment: Optional[...]`

**Methods:**
- `add_attachment(attachment: Attachment) -> Any`
- `add_chart(chart_type: ChartType, chart_label: str, x_label: str, x_unit: str, y_label: str, y_unit: str) -> Chart`
- `get_step_path() -> str`
- `propagate_failure() -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.action_step`

### `ActionStep(Step)`

_Action step with no measurement._

**Class Variables:**
- `step_type: Literal[...]`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.boolean_step`

### `MultiBooleanStep(Step)`

_Multi-boolean test step with multiple measurements._

**Class Variables:**
- `step_type: Literal[...]`
- `measurements: List[...]`

**Methods:**
- `add_measurement() -> MultiBooleanMeasurement`
- `check_for_duplicates(name: str) -> str`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

### `PassFailStep(Step)`

_Pass/Fail test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurement: Optional[...]`

**Properties:**
- `value`

**Methods:**
- `create(cls, name: str, value: Any) -> Any`
- `unwrap_measurement(cls, data: Any) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`
- `value(val: Any) -> Any`
- `wrap_measurement(cls, value: Optional[...]) -> Optional[...]`

---

## `report.report_models.uut.steps.callexe_step`

### `CallExeStep(Step)`

_Represents a step that calls an external executable._

**Class Variables:**
- `step_type: str`
- `info: Optional[...]`

---

### `CallExeStepInfo(WATSBase)`

_Information about a CallExecutable step._

**Class Variables:**
- `exit_code: Optional[...]`

---

## `report.report_models.uut.steps.chart_step`

### `ChartStep(Step)`

_Chart step for standalone chart display._

**Class Variables:**
- `step_type: Literal[...]`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.generic_step`

### `FlowType(Enum)`

_Flow control step types from TestStand._

**Class Variables:**
- `FTPFiles`
- `If`
- `ElseIf`
- `Else`
- `End`
- `For`
- `ForEach`
- `Break`
- `Continue`
- `DoWhile`
- `While`
- `Select`
- `Case`
- `NI_Flow_StreamLoop`
- `NI_Flow_SweepLoop`
- `Lock`
- `Rendezvous`
- `Queue`
- `Notification`
- `Wait`
- `Batch_Sync`
- `AutoSchedule`
- `UseResource`
- `ThreadPriority`
- `Semaphore`
- `BatchSpec`
- `BatchSync`
- `OpenDatabase`
- `OpenSQLStatement`
- `CloseSQLStatement`
- `CloseDatabase`
- `DataOperation`
- `NI_CPUAffinity`
- `NI_IviDmm`
- `NI_IviScope`
- `NI_IviFgen`
- `NI_IviDCPower`
- `NI_IviSwitch`
- `NI_IviTools`
- `NI_LV_DeployLibrary`
- `LV_CheckSystemStatus`
- `LV_RunVIAsynchronously`
- `NI_PropertyLoader`
- `NI_VariableAndPropertyLoader`
- `NI_NewCsvFileInputRecordStream`
- `NI_NewCsvFileOutputRecordStream`
- `NI_WriteRecord`
- `Goto`
- `Action`
- `Statement`
- `Label`
- `GenericTest`

---

### `GenericStep(Step)`

_Generic test step for custom/arbitrary data._

**Class Variables:**
- `step_type: GenericStepLiteral`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.limit_measurement`

### `LimitMeasurement(BaseMeasurement)`

_A measurement with limit checking._

**Class Variables:**
- `value: Union[...]`
- `value_format: Optional[...]`
- `comp_op: Optional[...]`
- `high_limit: Optional[...]`
- `high_limit_format: Optional[...]`
- `low_limit: Optional[...]`
- `low_limit_format: Optional[...]`

**Methods:**
- `calculate_status() -> str`

---

## `report.report_models.uut.steps.measurement`

### `BaseMeasurement(WATSBase, ABC)`

_Abstract base for all measurement types._

**Class Variables:**
- `status: StepStatus`
- `name: Optional[...]`

---

### `BooleanMeasurement(BaseMeasurement)`

_Boolean (pass/fail) measurement._

**Class Variables:**
- `value: Optional[...]`

**Methods:**
- `validate_against_expected(expected: bool) -> tuple[...]`

---

### `MultiBooleanMeasurement(BooleanMeasurement)`

_Boolean measurement with required name for multi-measurement steps._

**Class Variables:**
- `name: str`

---

### `MultiNumericMeasurement(NumericMeasurement)`

_Numeric measurement with required name for multi-measurement steps._

**Class Variables:**
- `name: str`

---

### `MultiStringMeasurement(StringMeasurement)`

_String measurement with required name for multi-measurement steps._

**Class Variables:**
- `name: str`

---

### `NumericMeasurement(BaseMeasurement)`

_Numeric measurement with limits._

**Class Variables:**
- `value: Optional[...]`
- `value_format: Optional[...]`
- `unit: Optional[...]`
- `comp_op: Optional[...]`
- `high_limit: Optional[...]`
- `high_limit_format: Optional[...]`
- `low_limit: Optional[...]`
- `low_limit_format: Optional[...]`

**Methods:**
- `calculate_status() -> str`
- `validate_against_limits() -> tuple[...]`

---

### `SingleMeasurementMixin(Unknown)`

_Mixin that provides wrap/unwrap serialization for single-measurement steps._

**Class Variables:**
- `measurement: Optional[...]`
- `_measurement_class: ClassVar[...]`

**Methods:**
- `unwrap_measurement_list(cls, data: Any) -> Any`
- `wrap_measurement_list(cls, value: Optional[...]) -> Optional[...]`

---

### `StringMeasurement(BaseMeasurement)`

_String measurement with comparison._

**Class Variables:**
- `value: Optional[...]`
- `comp_op: Optional[...]`
- `limit: Optional[...]`

**Methods:**
- `validate_against_limit() -> tuple[...]`

---

## `report.report_models.uut.steps.message_popup_step`

### `MessagePopUpStep(Step)`

_Represents a step that displays a message popup to the user._

**Class Variables:**
- `step_type: str`
- `info: Optional[...]`

---

### `MessagePopupInfo(WATSBase)`

_Information about a MessagePopup step._

**Class Variables:**
- `response: Optional[...]`
- `button: Optional[...]`

**Methods:**
- `set_default_response() -> Any`

---

## `report.report_models.uut.steps.numeric_step`

### `MultiNumericStep(Step)`

_Multi-numeric limit test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurements: List[...]`

**Methods:**
- `add_measurement()`
- `check_for_duplicates(name)`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

### `NumericStep(Step)`

_Numeric limit test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurement: Optional[...]`

**Properties:**
- `comp_op`
- `high_limit`
- `low_limit`
- `unit`
- `value`

**Methods:**
- `comp_op(val: Any) -> Any`
- `create(cls, name: str, value: Any) -> Any`
- `high_limit(val: Any) -> Any`
- `low_limit(val: Any) -> Any`
- `unit(val: Any) -> Any`
- `unwrap_measurement(cls, data: Any) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`
- `value(val: Any) -> Any`
- `wrap_measurement(cls, value: Optional[...]) -> Optional[...]`

---

## `report.report_models.uut.steps.sequence_call`

### `SequenceCall(Step)`

_Sequence call step - container for child steps._

**Class Variables:**
- `step_type: Literal[...]`
- `sequence: SequenceCallInfo`
- `caller: Optional[...]`
- `module: Optional[...]`
- `steps: StepList[...]`
- `add_pass_fail_step`

**Methods:**
- `add_action_step(name: str) -> ActionStep`
- `add_boolean_step() -> PassFailStep`
- `add_chart_step(name: str) -> ChartStep`
- `add_generic_step() -> GenericStep`
- `add_multi_boolean_step() -> MultiBooleanStep`
- `add_multi_numeric_step() -> MultiNumericStep`
- `add_multi_string_step() -> MultiStringStep`
- `add_numeric_step() -> NumericStep`
- `add_sequence_call(name: str) -> Any`
- `add_step(step: StepType) -> StepType`
- `add_string_step() -> StringValueStep`
- `assign_parent() -> Any`
- `count_steps(recursive: bool) -> int`
- `find_all_steps(name: Any, step_type: Any, recursive: bool) -> List[...]`
- `find_step(name: str, recursive: bool) -> Optional[...]`
- `get_failed_steps(recursive: bool) -> List[...]`
- `print_hierarchy(indent: int) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.steps.step_list`

### `StepList(Unknown)`

_A list that automatically sets parent reference on steps when added._

**Properties:**
- `parent`

**Methods:**
- `append(item: StepT) -> Any`
- `count_by_status() -> dict[...]`
- `extend(items: Iterable[...]) -> Any`
- `find_all_by_name(name: str) -> List[...]`
- `find_by_name(name: str) -> Optional[...]`
- `find_failed() -> List[...]`
- `get_by_status(status: Any) -> List[...]`
- `insert(index: int, item: StepT) -> Any`
- `parent(value: Optional[...]) -> Any`
- `set_parent(parent: Any) -> Any`

---

## `report.report_models.uut.steps.string_step`

### `MultiStringStep(Step)`

_Multi-string test step with multiple measurements._

**Class Variables:**
- `step_type: Literal[...]`
- `measurements: List[...]`

**Methods:**
- `add_measurement() -> MultiStringMeasurement`
- `check_for_duplicates(name: str) -> str`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

### `StringValueStep(Step)`

_String value test step._

**Class Variables:**
- `step_type: Literal[...]`
- `measurement: Optional[...]`

**Properties:**
- `comp`
- `limit`
- `value`

**Methods:**
- `comp(val: Any) -> Any`
- `create(cls, name: str, value: Any) -> Any`
- `limit(val: Any) -> Any`
- `unwrap_measurement(cls, data: Any) -> Any`
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`
- `value(val: Any) -> Any`
- `wrap_measurement(cls, value: Optional[...]) -> Optional[...]`

---

## `report.report_models.uut.steps.unknown_step`

### `UnknownStep(Step)`

_Fallback step type for steps not recognized by this version._

**Class Variables:**
- `model_config`
- `step_type: str`

**Methods:**
- `validate_step(trigger_children: bool, errors: Optional[...]) -> bool`

---

## `report.report_models.uut.uut_info`

### `RefUURs(WATSBase)`

_Repair reports that reference this test report._

**Class Variables:**
- `id: UUID`
- `start: Optional[...]`

---

### `UUTInfo(ReportInfo)`

_Unit Under Test information._

**Class Variables:**
- `fixture_id: Optional[...]`
- `socket_index: Optional[...]`
- `socket_index_format: Optional[...]`
- `error_code: Optional[...]`
- `error_code_format: Optional[...]`
- `error_message: Optional[...]`
- `batch_number: Optional[...]`
- `batch_fail_count: Optional[...]`
- `batch_fail_count_format: Optional[...]`
- `batch_loop_index: Optional[...]`
- `batch_loop_index_format: Optional[...]`
- `step_id_caused_uut_failure: Optional[...]`
- `referenced_by_uurs: Optional[...]`

---

## `report.report_models.uut.uut_report`

### `UUTReport(Unknown)`

_Complete UUT (Unit Under Test) report._

**Class Variables:**
- `info: Optional[...]`
- `root: SequenceCall`

**Properties:**
- `test_operation_code`

**Methods:**
- `add_sub_unit(part_type: str, sn: str, pn: str, rev: str) -> UUTSubUnit`
- `get_root_sequence_call() -> SequenceCall`
- `test_operation_code(value: int) -> Any`

---

### `UUTSubUnit(SubUnit)`

_UUT Sub-unit with its own test steps._

**Class Variables:**
- `root: Optional[...]`

---

## `report.report_models.wats_base`

### `DeserializationContext`

_Context for injecting default values during deserialization._

---

### `WATSBase(BaseModel)`

_Base class for all WATS Report Models._

**Class Variables:**
- `model_config`

**Methods:**
- `inject_defaults(cls, data: Any, info: ValidationInfo) -> Any`

---
