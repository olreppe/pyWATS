# pywats_client.converters - Class Reference

Auto-generated class reference for `pywats_client.converters`.

---

## `converters.base`

### `CSVConverter(ConverterBase)`

_Example CSV converter implementation using the new architecture._

**Properties:**
- `description`
- `name`
- `supported_extensions`
- `supported_mime_types`
- `version`

**Methods:**
- `convert_file(file_path: Path, args: ConverterArguments) -> ConverterResult`
- `get_arguments() -> Dict[...]`
- `on_failure(file_path: Path, result: ConverterResult, args: ConverterArguments) -> Any`
- `on_success(file_path: Path, result: ConverterResult, args: ConverterArguments) -> Any`
- `validate_file(file_info: FileInfo) -> Tuple[...]`

---

### `ConverterArguments`

_Arguments passed to converter from the client/service._

**Class Variables:**
- `api_client: Any`
- `file_info: FileInfo`
- `drop_folder: Path`
- `done_folder: Path`
- `error_folder: Path`
- `user_settings: Dict[...]`
- `conversion_log: Optional[...]`

---

### `ConverterBase(ABC)`

_Base class for file-to-report converters._

**Properties:**
- `description`
- `name`
- `source_path`
- `supported_extensions`
- `supported_mime_types`
- `trusted_mode`
- `version`

**Methods:**
- `convert_file(file_path: Path, args: ConverterArguments) -> ConverterResult`
- `get_arguments() -> Dict[...]`
- `on_failure(file_path: Path, result: ConverterResult, args: ConverterArguments) -> Any`
- `on_success(file_path: Path, result: ConverterResult, args: ConverterArguments) -> Any`
- `source_path(path: Optional[...]) -> Any`
- `trusted_mode(value: bool) -> Any`
- `validate_file(file_info: FileInfo) -> Tuple[...]`
- `validate_report(report: Dict[...]) -> List[...]`

---

## `converters.context`

### `ConverterContext`

_Context passed to converters during validation and conversion._

**Class Variables:**
- `api_client: Optional[...]`
- `drop_folder: Optional[...]`
- `done_folder: Optional[...]`
- `error_folder: Optional[...]`
- `pending_folder: Optional[...]`
- `station_name: str`
- `station_id: str`
- `operator: str`
- `alarm_threshold: float`
- `reject_threshold: float`
- `max_retries: int`
- `retry_delay_seconds: int`
- `arguments: Dict[...]`
- `dry_run: bool`
- `verbose: bool`
- `metadata: Dict[...]`

**Methods:**
- `check_confidence(confidence: float) -> str`
- `copy_with() -> Any`
- `ensure_folders_exist() -> Any`
- `from_config(cls, config: Dict[...], api_client: Optional[...]) -> Any`
- `get_argument(name: str, default: Any) -> Any`
- `get_done_path(filename: str) -> Path`
- `get_error_path(filename: str) -> Path`
- `get_pending_path(filename: str) -> Path`
- `has_argument(name: str) -> bool`
- `log_debug(message: str) -> Any`
- `log_error(message: str) -> Any`
- `log_info(message: str) -> Any`
- `log_warning(message: str) -> Any`
- `set_argument(name: str, value: Any) -> Any`
- `to_dict() -> Dict[...]`

---

## `converters.conversion_log`

### `ConversionLog`

_Per-conversion detailed logging._

**Methods:**
- `create_for_file(cls, file_name: str, instance_id: str) -> Any`
- `error(message: str, step: str, metadata: Optional[...], exception: Optional[...], raise_after_log: bool) -> Any`
- `finalize(success: bool, report_id: Optional[...], error: Optional[...], metadata: Optional[...]) -> Any`
- `step(step_name: str, message: str, metadata: Optional[...]) -> Any`
- `warning(message: str, step: str, metadata: Optional[...]) -> Any`

---

### `ConversionLogEntry`

_Single log entry for a conversion step._

**Class Variables:**
- `timestamp: str`
- `level: str`
- `step: str`
- `message: str`
- `metadata: Optional[...]`

**Methods:**
- `to_dict() -> Dict[...]`

---

## `converters.example_csv`

### `CSVTestConverter(FileConverter)`

_Converts CSV test result files to WATS reports._

**Properties:**
- `arguments_schema`
- `author`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.file_converter`

### `FileConverter(ABC)`

_Base class for file-based converters._

**Properties:**
- `arguments_schema`
- `author`
- `converter_type`
- `default_post_action`
- `description`
- `file_patterns`
- `name`
- `source_path`
- `trusted_mode`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: Any) -> ConverterResult`
- `on_failure(source: ConverterSource, result: ConverterResult, context: Any) -> Any`
- `on_load(context: Any) -> Any`
- `on_success(source: ConverterSource, result: ConverterResult, context: Any) -> Any`
- `on_unload() -> Any`
- `read_file_bytes(path: Path) -> bytes`
- `read_file_lines(path: Path, encoding: str, strip: bool) -> List[...]`
- `read_file_text(path: Path, encoding: str, errors: str) -> str`
- `source_path(path: Optional[...]) -> Any`
- `trusted_mode(value: bool) -> Any`
- `validate(source: ConverterSource, context: Any) -> ValidationResult`

---

## `converters.folder_converter`

### `FolderConverter(ABC)`

_Base class for folder-based converters._

**Properties:**
- `arguments_schema`
- `author`
- `converter_type`
- `default_post_action`
- `description`
- `expected_files`
- `folder_patterns`
- `min_file_count`
- `name`
- `preserve_folder_structure`
- `readiness_marker`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: Any) -> ConverterResult`
- `delete_marker(folder: Path) -> bool`
- `is_folder_ready(folder_path: Path, context: Any) -> bool`
- `list_files(folder: Path, pattern: str, recursive: bool) -> List[...]`
- `on_failure(source: ConverterSource, result: ConverterResult, context: Any) -> Any`
- `on_load(context: Any) -> Any`
- `on_success(source: ConverterSource, result: ConverterResult, context: Any) -> Any`
- `on_unload() -> Any`
- `read_marker_data(folder: Path) -> Optional[...]`
- `validate(source: ConverterSource, context: Any) -> ValidationResult`

---

## `converters.models`

### `ArgumentDefinition`

_Definition of a configurable converter argument._

**Class Variables:**
- `arg_type: ArgumentType`
- `default: Any`
- `description: str`
- `required: bool`
- `choices: Optional[...]`
- `min_value: Optional[...]`
- `max_value: Optional[...]`
- `pattern: Optional[...]`

**Methods:**
- `validate(value: Any) -> Tuple[...]`

---

### `ArgumentType(Enum)`

_Types for converter arguments_

**Class Variables:**
- `STRING`
- `INTEGER`
- `FLOAT`
- `BOOLEAN`
- `PATH`
- `CHOICE`
- `PASSWORD`

---

### `ConversionRecord`

_Record of a conversion attempt._

**Class Variables:**
- `source_path: Path`
- `converter_name: str`
- `created_at: datetime`
- `attempts: int`
- `last_attempt: Optional[...]`
- `last_status: Optional[...]`
- `last_error: Optional[...]`
- `suspend_reason: Optional[...]`
- `next_retry_at: Optional[...]`
- `last_confidence: float`

**Methods:**
- `is_due_for_retry() -> bool`
- `record_attempt(status: ConversionStatus, error: Optional[...], suspend_reason: Optional[...], retry_after: Optional[...], confidence: float) -> Any`
- `should_retry(max_attempts: int) -> bool`

---

### `ConversionStatus(Enum)`

_Status of a conversion operation_

**Class Variables:**
- `SUCCESS`
- `FAILED`
- `SUSPENDED`
- `SKIPPED`
- `REJECTED`

---

### `ConverterResult`

_Result of a conversion operation._

**Class Variables:**
- `status: ConversionStatus`
- `report: Optional[...]`
- `reports: List[...]`
- `error: Optional[...]`
- `warnings: List[...]`
- `metadata: Dict[...]`
- `suspend_reason: Optional[...]`
- `retry_after: Optional[...]`
- `retry_count: int`
- `post_action: PostProcessAction`
- `processing_time_ms: Optional[...]`
- `records_processed: int`
- `validation: Optional[...]`

**Properties:**
- `has_multiple_reports`
- `success`

**Methods:**
- `failed_result(cls, error: str, post_action: PostProcessAction, warnings: Optional[...]) -> Any`
- `get_all_reports() -> List[...]`
- `rejected_result(cls, reason: str, confidence: float, threshold: float) -> Any`
- `skipped_result(cls, reason: str) -> Any`
- `success_result(cls, report: Optional[...], reports: Optional[...], post_action: PostProcessAction, warnings: Optional[...], metadata: Optional[...], processing_time_ms: Optional[...]) -> Any`
- `suspended_result(cls, reason: str, retry_after: Optional[...], retry_count: int, metadata: Optional[...]) -> Any`

---

### `ConverterSource`

_Abstraction over what's being converted._

**Class Variables:**
- `source_type: SourceType`
- `path: Optional[...]`
- `files: List[...]`
- `metadata: Dict[...]`
- `record_id: Optional[...]`
- `connection_info: Optional[...]`
- `_file_info: Optional[...]`

**Properties:**
- `file_info`
- `is_file`
- `is_folder`
- `primary_name`

**Methods:**
- `from_database_record(cls, record_id: str, connection_info: str, metadata: Optional[...]) -> Any`
- `from_file(cls, file_path: Path) -> Any`
- `from_folder(cls, folder_path: Path, include_pattern: str, recursive: bool) -> Any`
- `get_files_matching(pattern: str) -> List[...]`

---

### `ConverterType(Enum)`

_Type of converter_

**Class Variables:**
- `FILE`
- `FOLDER`
- `SCHEDULED`

---

### `FailureRecord`

_Record of a failed conversion for logging/reporting._

**Class Variables:**
- `source_path: Path`
- `converter_name: str`
- `error: str`
- `timestamp: datetime`
- `attempts: int`
- `final_status: ConversionStatus`
- `moved_to: Optional[...]`

---

### `FileInfo`

_Information about a single file._

**Class Variables:**
- `path: Path`

**Methods:**
- `matches_any_pattern(patterns: List[...]) -> bool`
- `matches_pattern(pattern: str) -> bool`

---

### `PostProcessAction(Enum)`

_Post-processing action after successful conversion_

**Class Variables:**
- `DELETE`
- `MOVE`
- `ZIP`
- `KEEP`

---

### `SourceType(Enum)`

_Type of source being converted_

**Class Variables:**
- `FILE`
- `FOLDER`
- `DATABASE`
- `API`

---

### `ValidationResult`

_Result of converter validation/preview._

**Class Variables:**
- `can_convert: bool`
- `confidence: float`
- `detected_part_number: Optional[...]`
- `detected_serial_number: Optional[...]`
- `detected_process: Optional[...]`
- `detected_start_time: Optional[...]`
- `detected_result: Optional[...]`
- `detected_station: Optional[...]`
- `message: str`
- `warnings: List[...]`
- `ready: bool`
- `missing_dependencies: List[...]`
- `retry_after: Optional[...]`

**Properties:**
- `is_below_alarm_threshold`

**Methods:**
- `check_thresholds(alarm_threshold: float, reject_threshold: float) -> Tuple[...]`
- `good_match(cls, confidence: float, message: str) -> Any`
- `no_match(cls, reason: str) -> Any`
- `not_ready(cls, missing: List[...], retry_after: Optional[...], confidence: float) -> Any`
- `pattern_match(cls, message: str) -> Any`
- `perfect_match(cls, message: str) -> Any`

---

## `converters.sandbox`

### `ConverterSandbox`

_High-level interface for sandboxed converter execution._

---

### `ConverterValidator`

_Static analysis validator for converter code._

**Class Variables:**
- `DANGEROUS_CALLS`
- `DANGEROUS_IMPORTS`

**Methods:**
- `validate_file(path: Path) -> tuple[...]`
- `validate_source(source: str) -> tuple[...]`

---

### `ResourceLimits`

_Resource limits for sandboxed converter execution._

**Class Variables:**
- `timeout_seconds: float`
- `cpu_time_seconds: float`
- `memory_mb: int`
- `max_output_size_mb: int`
- `max_open_files: int`
- `max_processes: int`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`

---

### `SandboxCapability(Enum)`

_Capabilities that can be granted to sandboxed converters._

**Class Variables:**
- `READ_INPUT`
- `READ_DROP_FOLDER`
- `WRITE_OUTPUT`
- `WRITE_TEMP`
- `NETWORK_LOCAL`
- `NETWORK_WATS`
- `LOG_INFO`
- `LOG_DEBUG`
- `READ_ENV_SAFE`

---

### `SandboxConfig`

_Configuration for the converter sandbox._

**Class Variables:**
- `capabilities: Set[...]`
- `resource_limits: ResourceLimits`
- `allowed_read_paths: List[...]`
- `allowed_write_paths: List[...]`
- `allowed_imports: Optional[...]`
- `blocked_imports: Set[...]`
- `safe_env_vars: Set[...]`

**Methods:**
- `from_dict(cls, data: Dict[...]) -> Any`
- `to_dict() -> Dict[...]`

---

### `SandboxError(Exception)`

_Base exception for sandbox errors._

---

### `SandboxMessage`

_Message for sandbox IPC._

**Class Variables:**
- `type: SandboxMessageType`
- `payload: Dict[...]`

**Methods:**
- `from_json(cls, data: str) -> Any`
- `to_json() -> str`

---

### `SandboxMessageType(Enum)`

_Message types for sandbox IPC._

**Class Variables:**
- `INIT`
- `CONVERT`
- `SHUTDOWN`
- `READY`
- `RESULT`
- `LOG`
- `ERROR`
- `HEARTBEAT`

---

### `SandboxProcess`

_Manages a sandboxed converter process._

**Properties:**
- `is_running`

---

### `SandboxResourceError(SandboxError)`

_Converter exceeded resource limits._

---

### `SandboxSecurityError(SandboxError)`

_Security violation in sandbox._

---

### `SandboxTimeoutError(SandboxError)`

_Converter execution timed out._

---

## `converters.sandbox_runner`

### `ConverterArguments`

**Class Variables:**
- `file_info: FileInfo`
- `drop_folder: PathType`
- `done_folder: PathType`
- `error_folder: PathType`
- `api_client: Any`
- `user_settings: Dict[...]`

---

### `FileInfo`

**Class Variables:**
- `path: PathType`
- `name: str`
- `stem: str`
- `extension: str`
- `size: int`

---

### `MessageType`

**Class Variables:**
- `INIT`
- `CONVERT`
- `SHUTDOWN`
- `READY`
- `RESULT`
- `LOG`
- `ERROR`
- `HEARTBEAT`

---

### `RestrictedImporter`

_Custom import hook that blocks dangerous imports._

**Methods:**
- `find_module(fullname: str, path)`
- `load_module(fullname: str)`

---

### `SafeFileHandler`

_Safe file operations with path restrictions._

**Methods:**
- `safe_open(file: Any, mode: str)`

---

### `SandboxRunner`

_Main sandbox execution environment._

**Methods:**
- `run() -> Any`
- `run_conversion(input_path: Path, output_path: Path, args: Dict[...]) -> Dict[...]`
- `setup(config: Dict[...]) -> Any`

---

## `converters.scheduled_converter`

### `ScheduledConverter(ABC)`

_Base class for scheduled converters._

**Properties:**
- `arguments_schema`
- `author`
- `converter_type`
- `cron_expression`
- `description`
- `is_running`
- `last_run`
- `max_concurrent_runs`
- `name`
- `next_run`
- `retry_delay`
- `retry_on_failure`
- `run_on_startup`
- `schedule_interval`
- `timeout`
- `version`

**Methods:**
- `calculate_next_run(from_time: Optional[...]) -> Optional[...]`
- `get_schedule_description() -> str`
- `on_load(context: Any) -> Any`
- `on_run_complete(results: List[...], context: Any) -> Any`
- `on_run_error(error: Exception, context: Any) -> Any`
- `on_run_start(context: Any) -> Any`
- `on_unload() -> Any`
- `should_run_now() -> bool`

---

## `converters.standard.ai_converter`

### `AIConverter(FileConverter)`

_Intelligent auto-selection converter._

**Class Variables:**
- `_converter_registry: Dict[...]`
- `_registry_initialized: bool`

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `clear_registry(cls) -> Any`
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `get_registered_converters(cls) -> Dict[...]`
- `initialize_default_converters(cls) -> Any`
- `on_load(context: ConverterContext) -> Any`
- `register_converter(cls, converter: FileConverter) -> Any`
- `register_converters(cls, converters: List[...]) -> Any`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.atml_converter`

### `ATMLConverter(FileConverter)`

_Converts IEEE ATML test result files to WATS reports._

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

### `ATMLVersion(Enum)`

_Supported ATML versions._

**Class Variables:**
- `V2_02`
- `V5_00`
- `V6_01`
- `UNKNOWN`

---

### `StepGroup(str, Enum)`

_Step group types for ATML conversion._

**Class Variables:**
- `MAIN`
- `SETUP`
- `CLEANUP`

---

## `converters.standard.keysight_testexec_sl_converter`

### `KeysightTestExecSLConverter(FileConverter)`

_Converts Keysight TestExec SL XML test result files to WATS reports._

**Class Variables:**
- `ROOT_ELEMENTS`
- `NAMESPACES`

**Properties:**
- `arguments_schema`
- `author`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.klippel_converter`

### `KlippelConverter(FileConverter)`

_Converts Klippel speaker test log files to WATS reports using UUTReport model._

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.seica_xml_converter`

### `SeicaXMLConverter(FileConverter)`

_Converts Seica flying probe XML test result files to WATS reports using UUTReport model._

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.spea_converter`

### `SPEAConverter(FileConverter)`

_Converts SPEA ICT test result files to WATS reports using UUTReport model._

**Class Variables:**
- `COMPONENT_TYPES`

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.teradyne_ict_converter`

### `Event(Enum)`

_Main event types_

**Class Variables:**
- `ABORTED`
- `PASS`
- `FAIL`
- `ERROR`
- `SYSTEM_ERROR`
- `CANCELLED`
- `RETURN_TO_DIAGNOSE`

---

### `PrefixUnit`

_Unit prefix with conversion factor_

**Methods:**
- `get_value(value: float) -> float`
- `get_value_inv(value: float) -> float`

---

### `TeradyneICTConverter(FileConverter)`

_Converts Teradyne ICT i3070 test result files to WATS reports._

**Class Variables:**
- `RE_START_PROGRAM`
- `RE_START_TEST`
- `RE_MAIN_EVENT`
- `RE_FAILURES_GEN`
- `RE_MEASURE`
- `RE_BATCH`
- `RE_BTEST`
- `RE_BLOCK`
- `RE_A_JUM`

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.teradyne_spectrum_ict_converter`

### `MainStep`

_Represents a main step with sub-steps_

**Class Variables:**
- `name: str`
- `status: str`
- `start: Optional[...]`
- `description: str`
- `sub_steps: List[...]`

---

### `SubStep`

_Represents a sub-step measurement_

**Class Variables:**
- `name: str`
- `type: str`
- `meas: Optional[...]`
- `meas_scale: str`
- `unit: str`
- `low_lim: Optional[...]`
- `low_scale: str`
- `high_lim: Optional[...]`
- `high_scale: str`
- `comment: str`
- `status: str`

---

### `TeradyneSpectrumICTConverter(FileConverter)`

_Converts Teradyne Spectrum ICT test result files to WATS reports using UUTReport model._

**Class Variables:**
- `RE_PROGRAM_NAME`
- `RE_SECTION_NAME`
- `RE_NEW_STEP`
- `RE_SNAME`
- `RE_DESC`
- `RE_STEP_TYPE`
- `RE_GROUP_NAME`
- `RE_CONNECTED_NODES`
- `RE_FSCAN_PIN`
- `RE_MEAS_VAL_THRESHOLD`
- `RE_SERIAL`
- `RE_OPERATOR`
- `RE_USER`
- `RE_PROG_NAME`

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.wats_standard_json_converter`

### `WATSStandardJsonConverter(FileConverter)`

_Converts WATS Standard JSON Format (WSJF) files to WATS reports._

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.wats_standard_text_converter`

### `ReportReadState(Enum)`

_Parser state_

**Class Variables:**
- `UNKNOWN`
- `IN_HEADER`
- `IN_TEST`
- `IN_FOOTER`
- `END_OF_FILE`

---

### `WATSStandardTextConverter(FileConverter)`

_Converts WATS Standard Text Format files to WATS reports._

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.wats_standard_xml_converter`

### `WATSStandardXMLConverter(FileConverter)`

_Converts WATS Standard XML Format (WSXF/WRML) files to WATS reports._

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---

## `converters.standard.xjtag_converter`

### `XJTAGConverter(FileConverter)`

_Converts XJTAG log ZIP files to WATS reports using the UUTReport model._

**Properties:**
- `arguments_schema`
- `description`
- `file_patterns`
- `name`
- `version`

**Methods:**
- `convert(source: ConverterSource, context: ConverterContext) -> ConverterResult`
- `validate(source: ConverterSource, context: ConverterContext) -> ValidationResult`

---
