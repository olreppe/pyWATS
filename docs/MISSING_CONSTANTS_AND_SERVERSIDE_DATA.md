from enum import Enum
from typing import List, Dict, Optional
from uuid import UUID
import threading
import datetime

# --- Enums mirrored from .NET side (subset relevant for OperationType/RepairType/Processes) ---

class ProcessRecordState(Enum):
    INACTIVE = 0
    ACTIVE = 1
    DELETED = 2

class CodeType(Enum):
    STATUS = "Status"
    STEP_GROUP = "StepGroup"
    STEP_TYPE = "StepType"

# (Optional) Additional enums if needed later
class ReportResultType(Enum):
    PASSED = "Passed"
    FAILED = "Failed"
    ERROR = "Error"
    TERMINATED = "Terminated"

# --- Data Model Mirrors (Interface.TDM.Models) ---

class MiscInfo:
    guid: UUID
    description: str
    input_mask: Optional[str]
    valid_regex: Optional[str]
    status: int
    def __init__(self): pass

class FailCode:
    guid: UUID
    selectable: bool
    description: str
    sort_order: int
    failure_type: int
    image_constraint: Optional[str]
    status: int
    children: List["FailCode"]
    def __init__(self): pass

class RepairTypeProperties:  # Maps Models.RepairType (Process.Properties when IsRepairOperation)
    description: str
    uut_required: bool
    comp_ref_mask: Optional[str]
    comp_ref_mask_description: Optional[str]
    bom_constraint: Optional[str]
    categories: List[FailCode]          # Root failcode categories
    misc_infos: List[MiscInfo]
    def __init__(self): pass

class ProcessProperties:
    # Base for future extensions (only RepairType currently used)
    def __init__(self): pass

class Process:
    guid: UUID
    code: int
    name: str
    description: str
    state: ProcessRecordState
    process_index: Optional[int]
    is_test_operation: bool
    is_wip_operation: bool
    is_repair_operation: bool
    properties: Optional[ProcessProperties]  # RepairTypeProperties when repair
    def __init__(self): pass

class OperationType:
    id: UUID            # process.guid / processId
    code: int           # short code
    name: str
    description: str
    process: Process
    def __init__(self): pass

class RepairType:
    id: UUID
    code: int
    name: str
    description: str
    uut_required: bool
    component_reference_mask: Optional[str]
    component_reference_mask_description: Optional[str]
    process: Process
    properties: RepairTypeProperties
    def __init__(self): pass

# --- Internal cache container ---

class _ProcessCache:
    processes_by_code: Dict[int, Process]
    processes_by_id: Dict[UUID, Process]
    last_refresh: Optional[datetime.datetime]
    refresh_interval: datetime.timedelta
    lock: threading.RLock
    def __init__(self): pass

# --- Public API class (pyWATS main facade additions) ---

class PyWATSAPI:
    _process_cache: _ProcessCache

    # Initialization / configuration
    def __init__(self, base_url: str, api_token: Optional[str] = None): pass
    def set_refresh_interval_seconds(self, seconds: int): pass

    # Refresh / scheduling
    def refresh_process_metadata(self, force: bool = False): pass
    def start_auto_refresh(self): pass
    def stop_auto_refresh(self): pass

    # Low-level fetch (HTTP GET /api/internal/process/GetProcesses)
    def _fetch_processes_from_server(self) -> List[dict]: pass
    def _parse_process_payload(self, raw: List[dict]) -> List[Process]: pass
    def _update_cache(self, processes: List[Process]): pass

    # Accessors - Operation Types
    def get_operation_types(self) -> List[OperationType]: pass
    def get_operation_type_by_id(self, op_id: UUID) -> OperationType: pass
    def get_operation_type_by_code(self, code: int) -> OperationType: pass
    def get_operation_type_by_name(self, name: str) -> OperationType: pass

    # Accessors - Repair Types
    def get_repair_types(self) -> List[RepairType]: pass
    def get_repair_type_by_id(self, repair_id: UUID) -> RepairType: pass

    # Fail code hierarchy
    def get_root_failcodes(self, repair_type: RepairType) -> List[FailCode]: pass
    def get_child_failcodes(self, parent: FailCode, repair_type: RepairType) -> List[FailCode]: pass

    # Misc infos for a repair type
    def get_misc_infos(self, repair_type: RepairType) -> List[MiscInfo]: pass
    def get_misc_info_by_guid(self, repair_type: RepairType, guid: UUID) -> MiscInfo: pass

    # Code declarations helper (similar to GetCodeDeclaration)
    def generate_code_constants(self, repair_type: RepairType) -> str: pass

    # Health / introspection
    def last_metadata_refresh_utc(self) -> Optional[datetime.datetime]: pass
    def metadata_stale(self) -> bool: pass