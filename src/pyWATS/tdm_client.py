"""
Main TDM Client for WATS Test Data Management.

This module provides the main TDM (Test Data Management) client class that serves as 
the entry point for all TDM-related operations, equivalent to the C# TDM class.
"""

import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from enum import Enum

from .connection import WATSConnection as Connection
from .tdm import Analytics, Reports
from .rest_api.endpoints.report import submit_wsjf_report
from .rest_api.models import ReportInfo
from .tdm.models import UUTReport, UURReport, UURInfo, SubRepair


class APIStatusType(Enum):
    """API connection status enumeration."""
    Unknown = "Unknown"
    Online = "Online"
    Offline = "Offline"
    NotRegistered = "NotRegistered"
    NotActivated = "NotActivated"
    NotInstalled = "NotInstalled"
    Error = "Error"
    Disposing = "Disposing"


class ClientStateType(Enum):
    """Client state enumeration."""
    Unknown = "Unknown"
    NotConfigured = "NotConfigured"
    Active = "Active"
    Inactive = "Inactive"


class InitializationMode(Enum):
    """Initialization mode enumeration."""
    NoConnect = "NoConnect"
    Synchronous = "Synchronous"
    Asynchronous = "Asynchronous"
    UseExistingStatus = "UseExistingStatus"


class SubmitMethod(Enum):
    """Report submission method enumeration."""
    Online = "Online"
    Offline = "Offline"
    Automatic = "Automatic"


class ValidationModeType(Enum):
    """Validation mode enumeration."""
    ThrowExceptions = "ThrowExceptions"
    LogErrors = "LogErrors"


class TestModeType(Enum):
    """Test mode enumeration."""
    Active = "Active"
    Import = "Import"


class TDMClient:
    """
    Main TDM Client class for WATS Test Data Management.
    
    This class serves as the main entry point for all TDM operations,
    providing functionality for:
    - Connection management
    - Report creation and submission
    - Statistics and analytics
    - Operation type management
    """

    def __init__(self):
        """Initialize the TDM client."""
        self._connection: Optional[Connection] = None
        self._status = APIStatusType.Unknown
        self._client_state = ClientStateType.NotConfigured
        self._validation_mode = ValidationModeType.ThrowExceptions
        self._test_mode = TestModeType.Active
        self._rethrow_exception = True
        self._log_exceptions = True
        self._station_name: Optional[str] = None
        self._data_dir: Optional[str] = None
        self._location: Optional[str] = None
        self._purpose: Optional[str] = None
        self._root_step_name = "MainSequence Callback"
        self._last_service_exception: Optional[Exception] = None
        
        # Initialize sub-modules (will be created after connection is established)
        self._analytics: Optional[Analytics] = None
        self._reports: Optional[Reports] = None
        
        # Cached data
        self._operation_types: Optional[List[Dict[str, Any]]] = None
        self._repair_types: Optional[List[Dict[str, Any]]] = None
        self._processes: Optional[Dict[str, Any]] = None

    @property
    def connection(self) -> Optional[Connection]:
        """Get the connection instance."""
        return self._connection

    @property
    def status(self) -> APIStatusType:
        """Get current API status."""
        return self._status

    @property
    def client_state(self) -> ClientStateType:
        """Get current client state."""
        return self._client_state

    @property
    def validation_mode(self) -> ValidationModeType:
        """Get/set validation mode."""
        return self._validation_mode

    @validation_mode.setter
    def validation_mode(self, value: ValidationModeType) -> None:
        """Set validation mode."""
        self._validation_mode = value

    @property
    def test_mode(self) -> TestModeType:
        """Get/set test mode."""
        return self._test_mode

    @test_mode.setter
    def test_mode(self, value: TestModeType) -> None:
        """Set test mode."""
        self._test_mode = value

    @property
    def station_name(self) -> str:
        """Get/set station name."""
        return self._station_name or "DefaultStation"

    @station_name.setter
    def station_name(self, value: str) -> None:
        """Set station name."""
        self._station_name = value

    @property
    def data_dir(self) -> str:
        """Get data directory for pending reports."""
        if self._data_dir:
            return self._data_dir
        return os.path.join(os.getcwd(), "WATSData")

    @property
    def location(self) -> str:
        """Get test station location."""
        return self._location or "DefaultLocation"

    @property
    def purpose(self) -> str:
        """Get test station purpose."""
        return self._purpose or "DefaultPurpose"

    @property
    def root_step_name(self) -> str:
        """Get/set root step name."""
        return self._root_step_name

    @root_step_name.setter
    def root_step_name(self, value: str) -> None:
        """Set root step name."""
        self._root_step_name = value

    @property
    def last_service_exception(self) -> Optional[Exception]:
        """Get the last service exception."""
        return self._last_service_exception

    @property
    def rethrow_exception(self) -> bool:
        """Get/set whether to rethrow exceptions."""
        return self._rethrow_exception

    @rethrow_exception.setter
    def rethrow_exception(self, value: bool) -> None:
        """Set whether to rethrow exceptions."""
        self._rethrow_exception = value

    @property
    def log_exceptions(self) -> bool:
        """Get/set whether to log exceptions."""
        return self._log_exceptions

    @log_exceptions.setter
    def log_exceptions(self, value: bool) -> None:
        """Set whether to log exceptions."""
        self._log_exceptions = value

    @property
    def analytics(self) -> Optional[Analytics]:
        """Get the analytics module."""
        return self._analytics

    @property
    def reports(self) -> Optional[Reports]:
        """Get the reports module."""
        return self._reports

    def setup_api(
        self,
        data_dir: Optional[str] = None,
        location: Optional[str] = None,
        purpose: Optional[str] = None,
        persist: bool = False
    ) -> None:
        """
        Setup API with configuration values.
        
        Args:
            data_dir: Directory for temporary reports storage
            location: Test station location
            purpose: Test station purpose
            persist: Whether to persist values (not implemented in Python version)
        """
        if data_dir:
            self._data_dir = data_dir
        if location:
            self._location = location
        if purpose:
            self._purpose = purpose
            
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

    def initialize_api(
        self,
        try_connect_to_server: bool = True,
        download_metadata: bool = True
    ) -> None:
        """
        Initialize the API for use.
        
        Args:
            try_connect_to_server: Whether to attempt server connection
            download_metadata: Whether to download metadata from server
        """
        mode = InitializationMode.Synchronous if try_connect_to_server else InitializationMode.NoConnect
        self._initialize_api_with_mode(mode, download_metadata)

    def _initialize_api_with_mode(
        self,
        init_mode: InitializationMode,
        download_metadata: bool = True
    ) -> None:
        """Initialize API with specific mode."""
        try:
            if init_mode == InitializationMode.NoConnect:
                self._status = APIStatusType.Offline
                self._load_cached_metadata()
            elif init_mode == InitializationMode.Synchronous:
                if self._connect_server(download_metadata):
                    self._status = APIStatusType.Online
                else:
                    self._status = APIStatusType.Offline
            # Note: Asynchronous mode would require threading implementation
                
        except Exception as e:
            self._last_service_exception = e
            self._status = APIStatusType.Error
            if self._log_exceptions:
                print(f"Initialize API error: {e}")
            if self._rethrow_exception:
                raise

    def register_client(
        self,
        base_url: str,
        token: str
    ) -> None:
        """
        Register client with WATS server.
        
        Args:
            base_url: WATS server base URL  
            token: Authentication token (Basic auth encoded)
        """
        try:
            # Create connection
            self._connection = Connection(base_url=base_url, token=token)
            
            # Test connection
            if self._connection.test_connection():
                self._client_state = ClientStateType.Active
                
                # Initialize sub-modules now that we have a connection
                self._analytics = Analytics(self._connection)
                self._reports = Reports(self._connection)
            else:
                raise Exception("Failed to register client - connection test failed")
                
        except Exception as e:
            self._last_service_exception = e
            if self._log_exceptions:
                print(f"Register client error: {e}")
            if self._rethrow_exception:
                raise

    def unregister_client(self) -> None:
        """
        Disconnect client from server.
        Clears server URL and client token.
        """
        # Close connection and reset state
        if self._connection:
            self._connection.close()
            self._connection = None
        
        # Reset sub-modules
        self._statistics = None
        self._analytics = None
        self._reports = None
        
        self._client_state = ClientStateType.NotConfigured
        self._status = APIStatusType.NotRegistered

    def _connect_server(self, update_metadata: bool = True) -> bool:
        """
        Connect to configured server.
        
        Args:
            update_metadata: Whether to download metadata from server
            
        Returns:
            True if connection successful
        """
        try:
            # Test connection
            if not self._connection or not self._connection.test_connection():
                return False
            
            if update_metadata:
                self._download_metadata()
            else:
                self._load_cached_metadata()
                
            return True
            
        except Exception as e:
            self._last_service_exception = e
            if self._log_exceptions:
                print(f"Connect server error: {e}")
            return False

    def _download_metadata(self) -> None:
        """Download metadata from server."""
        try:
            if not self._connection:
                raise Exception("No connection available")
                
            # Download operation types and processes via REST API
            # Try the public REST API first, then fall back to internal API
            response = self._connection.client.get("/api/App/Processes", params={
                "includeTestOperations": True,
                "includeRepairOperations": True,
                "includeWipOperations": False,
                "includeInactiveProcesses": False
            })
            
            if response.status_code == 200:
                processes_data = response.json()
                # Wrap in the expected format
                self._processes = {
                    "processes": processes_data if isinstance(processes_data, list) else [processes_data]
                }
            else:
                # Try the internal API as fallback
                response = self._connection.client.get("/api/internal/process/GetProcesses")
                if response.status_code == 200:
                    processes_data = response.json()
                    self._processes = {
                        "processes": processes_data if isinstance(processes_data, list) else processes_data.get("processes", [])
                    }
                else:
                    raise Exception(f"Failed to get processes from both endpoints: {response.status_code}")
            
            # Cache the data locally
            self._cache_metadata()
            
        except Exception as e:
            # Fall back to cached data
            self._load_cached_metadata()
            raise

    def _cache_metadata(self) -> None:
        """Cache metadata locally."""
        try:
            cache_file = os.path.join(self.data_dir, "processes_cache.json")
            with open(cache_file, 'w') as f:
                json.dump(self._processes, f, indent=2)
        except Exception as e:
            if self._log_exceptions:
                print(f"Failed to cache metadata: {e}")

    def _load_cached_metadata(self) -> None:
        """Load cached metadata from disk."""
        try:
            cache_file = os.path.join(self.data_dir, "processes_cache.json")
            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    self._processes = json.load(f)
        except Exception as e:
            if self._log_exceptions:
                print(f"Failed to load cached metadata: {e}")

    def get_all_processes(self) -> List[Dict[str, Any]]:
        """
        Get all processes with their complete information including failure categories and codes.
        
        Returns:
            List of all process dictionaries with unified structure
        """
        if not self._processes:
            raise Exception("No processes available - ensure API is initialized")
            
        all_processes = []
        if 'processes' in self._processes:
            for process in self._processes['processes']:
                # Extract all process information with unified structure
                unified_process = {
                    'id': process.get('processId') or process.get('ProcessID'),
                    'code': process.get('code') or process.get('Code'),
                    'name': process.get('name') or process.get('Name'),
                    'description': process.get('description') or process.get('Description', ''),
                    'processIndex': process.get('processIndex'),
                    'state': process.get('state'),
                    'isTestOperation': process.get('isTestOperation', process.get('IsTestOperation', False)),
                    'isRepairOperation': process.get('isRepairOperation', process.get('IsRepairOperation', False)),
                    
                    # Extract failure categories and codes - check multiple possible field names
                    'failureCategories': self._extract_categories(process),
                    'failureCodes': self._extract_codes(process),
                    'repairInstructions': process.get('repairInstructions', process.get('RepairInstructions', []))
                }
                all_processes.append(unified_process)
        
        return all_processes

    def _extract_categories(self, process: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract failure categories from process, handling various field names and nested structures."""
        categories = []
        
        # First check direct fields
        possible_fields = ['failureCategories', 'FailureCategories', 'categories', 'Categories']
        for field in possible_fields:
            if field in process and process[field]:
                categories = process[field]
                break
        
        # If not found, check nested in repairOperation structure
        if not categories and 'repairOperation' in process:
            repair_op = process['repairOperation']
            if 'repairCategories' in repair_op and repair_op['repairCategories']:
                categories = repair_op['repairCategories']
        
        # Ensure categories are in consistent format
        standardized = []
        for cat in categories:
            if isinstance(cat, dict):
                standardized.append({
                    'name': cat.get('description', cat.get('name', cat.get('Name', ''))),
                    'code': cat.get('id', cat.get('code', cat.get('Code', ''))),
                    'description': cat.get('description', cat.get('Description', ''))
                })
            elif isinstance(cat, str):
                standardized.append({'name': cat, 'code': cat, 'description': ''})
                
        return standardized

    def _extract_codes(self, process: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract failure codes from process, handling various field names and nested structures."""
        codes = []
        
        # First check direct fields
        possible_fields = ['failureCodes', 'FailureCodes', 'codes', 'Codes']
        for field in possible_fields:
            if field in process and process[field]:
                codes = process[field]
                break
        
        # If not found, extract from nested repairOperation.repairCategories[].repairCodes
        if not codes and 'repairOperation' in process:
            repair_op = process['repairOperation']
            if 'repairCategories' in repair_op:
                for category in repair_op['repairCategories']:
                    if 'repairCodes' in category and category['repairCodes']:
                        codes.extend(category['repairCodes'])
        
        # Ensure codes are in consistent format
        standardized = []
        for code in codes:
            if isinstance(code, dict):
                standardized.append({
                    'code': code.get('description', code.get('name', code.get('Name', ''))),  # Use description as code
                    'name': code.get('description', code.get('name', code.get('Name', ''))),
                    'description': code.get('description', code.get('Description', '')),
                    'id': code.get('id'),  # Keep original ID for reference
                    'failureType': code.get('failureType'),
                    'category': code.get('category', '')  # Will be set when we process categories
                })
            elif isinstance(code, str):
                standardized.append({'code': code, 'name': code, 'description': ''})
                
        return standardized

    def get_operation_types(self) -> List[Dict[str, Any]]:
        """
        Get available operation types (test operations).
        
        Returns:
            List of operation type dictionaries
        """
        all_processes = self.get_all_processes()
        return [p for p in all_processes if p['isTestOperation']]

    def get_repair_operations(self) -> List[Dict[str, Any]]:
        """
        Get available repair operations from processes where isRepairOperation=true.
        
        Returns:
            List of repair operation dictionaries with categories and codes
        """
        all_processes = self.get_all_processes()
        return [p for p in all_processes if p['isRepairOperation']]

    def get_test_operations(self) -> List[Dict[str, Any]]:
        """
        Get available test operations from processes where isTestOperation=true.
        
        Returns:
            List of test operation dictionaries
        """
        all_processes = self.get_all_processes()
        return [p for p in all_processes if p['isTestOperation']]

    def get_repair_operation_by_code(self, code: Union[str, int]) -> Optional[Dict[str, Any]]:
        """
        Get repair operation by code.
        
        Args:
            code: Repair operation code
            
        Returns:
            Repair operation dict or None if not found
        """
        repair_ops = self.get_repair_operations()
        for repair_op in repair_ops:
            if str(repair_op.get('code')) == str(code) or repair_op.get('code') == code:
                return repair_op
        return None

    def get_operation_type_by_code(self, code: Union[str, int]) -> Dict[str, Any]:
        """
        Get operation type by code.
        
        Args:
            code: Operation type code (string or integer)
            
        Returns:
            Operation type dictionary
        """
        operation_types = self.get_operation_types()
        
        # Try to match by code
        code_str = str(code)
        for op_type in operation_types:
            if str(op_type.get('code')) == code_str:
                return op_type
                
        # Try to match by name if not found by code
        for op_type in operation_types:
            if op_type.get('name') == code:
                return op_type
                
        raise Exception(f"Operation type with code '{code}' not found")

    def get_operation_type_by_id(self, operation_id: Union[str, uuid.UUID]) -> Dict[str, Any]:
        """
        Get operation type by ID (GUID).
        
        Args:
            operation_id: Operation type ID
            
        Returns:
            Operation type dictionary
        """
        operation_types = self.get_operation_types()
        
        id_str = str(operation_id)
        for op_type in operation_types:
            if str(op_type.get('id')) == id_str:
                return op_type
                
        raise Exception(f"Operation type with ID '{operation_id}' not found")

    def get_repair_types(self) -> List[Dict[str, Any]]:
        """
        Get available repair types.
        
        Returns:
            List of repair type dictionaries
        """
        if not self._processes:
            raise Exception("No processes available - ensure API is initialized")
            
        # Filter for repair operations
        repair_types = []
        if 'processes' in self._processes:
            for process in self._processes['processes']:
                # Check both possible field names for compatibility
                is_repair_op = process.get('isRepairOperation', process.get('IsRepairOperation', False))
                if is_repair_op:
                    repair_types.append({
                        'id': process.get('processId') or process.get('ProcessID'),
                        'code': process.get('code') or process.get('Code'),
                        'name': process.get('name') or process.get('Name'),
                        'description': process.get('description') or process.get('Description', ''),
                        'uut_required': process.get('uutRequired') or process.get('UUTRequired', False),
                        'processIndex': process.get('processIndex'),
                        'state': process.get('state')
                    })
        
        return repair_types

    def create_uut_report(
        self,
        operator_name: str,
        part_number: str,
        revision: str,
        serial_number: str,
        operation_type: Union[str, int, Dict[str, Any]],
        sequence_file_name: str,
        sequence_file_version: str
    ) -> UUTReport:
        """
        Create a UUT (Unit Under Test) report.
        
        Args:
            operator_name: ATE Operator name
            part_number: Product part number
            revision: Product revision number
            serial_number: Serial number, unique within a part number
            operation_type: Type of test (code, name, or dict)
            sequence_file_name: Name of sequence file (test program)
            sequence_file_version: Version of sequence file (test program)
            
        Returns:
            UUTReport instance
        """
        # Resolve operation type and extract process code
        if isinstance(operation_type, (str, int)):
            op_type = self.get_operation_type_by_code(operation_type)
            process_code = op_type.get('code', 0) if isinstance(op_type, dict) else 0
        elif isinstance(operation_type, dict):
            op_type = operation_type
            # Extract process code, handling both integer and string codes
            code_value = op_type.get('code', 0)
            if isinstance(code_value, str):
                # Try to convert string to int, fallback to 0
                try:
                    process_code = int(code_value)
                except (ValueError, TypeError):
                    process_code = 0
            else:
                process_code = int(code_value) if code_value is not None else 0
        else:
            raise ValueError("Invalid operation_type parameter")
            
        # Create UUT info  
        from .tdm.models import UUTInfo
        uut_info = UUTInfo(
            user=operator_name or "Operator",
            execTime=0.0,
            fixtureId=""
        )
        
        # Create UUT report using WSJF model
        report = UUTReport(
            pn=part_number or "",
            sn=serial_number or "",
            rev=revision or "",
            process_code=process_code,
            result="P",  # Default to Passed, will be updated when completed
            machineName=self.station_name,
            location=self.location,
            purpose=self.purpose,
            start=datetime.now(timezone.utc)
        )
        
        # Set the UUT info after creation (this ensures proper alias handling)
        report.uut_info = uut_info


        # Create a SequenceCall instance and add it to the report
        from .tdm.models import SequenceCall
        root_sequence = report.get_root_Sequence_call()
        root_sequence.sequence_name = sequence_file_name
        root_sequence.sequence_version = sequence_file_version

        return report

    def create_uur_report(
        self,
        operator_name: str,
        repair_type: Union[str, Dict[str, Any]],
        uut_report: Optional[Union[Dict[str, Any], UUTReport]] = None,
        serial_number: Optional[str] = None,
        part_number: Optional[str] = None,
        revision: Optional[str] = None,
        failure_category: Optional[str] = None,
        failure_code: Optional[str] = None
    ) -> UURReport:
        """
        Create a UUR (Unit Under Repair) report.
        
        Args:
            operator_name: Operator name
            repair_type: Repair type (name or dict)
            uut_report: Associated UUT report (optional)
            serial_number: Serial number (required if no UUT report)
            part_number: Part number (required if no UUT report)
            revision: Revision (required if no UUT report)
            
        Returns:
            UURReport instance
        """
        # Resolve repair type
        if isinstance(repair_type, str):
            repair_types = self.get_repair_types()
            repair_type_dict = None
            for rt in repair_types:
                if rt.get('name') == repair_type:
                    repair_type_dict = rt
                    break
            if not repair_type_dict:
                raise ValueError(f"Repair type '{repair_type}' not found")
        else:
            repair_type_dict = repair_type
            
        # Validate UUT requirement
        if repair_type_dict.get('uut_required', False) and not uut_report:
            raise ValueError("This repair type requires a UUT report")
            
        # Get part info from UUT report or parameters
        if uut_report:
            if isinstance(uut_report, UUTReport):
                # Extract info from UUTReport instance
                part_sn = uut_report.sn
                part_pn = uut_report.pn
                part_rev = uut_report.rev
                uut_id = uut_report.id
            else:
                # Extract info from dictionary (legacy support)
                part_sn = uut_report.get('serial_number', '')
                part_pn = uut_report.get('part_number', '')
                part_rev = uut_report.get('revision', '')
                uut_id = uut_report.get('report_id')
        else:
            if not all([serial_number, part_number, revision]):
                raise ValueError("Serial number, part number, and revision are required when no UUT report is provided")
            part_sn = serial_number
            part_pn = part_number
            part_rev = revision
            uut_id = None
            
        # Extract process code from repair type, handling both integer and string codes
        if isinstance(repair_type_dict, dict):
            code_value = repair_type_dict.get('code', 0)
            if isinstance(code_value, str):
                try:
                    process_code = int(code_value)
                except (ValueError, TypeError):
                    process_code = 0
            else:
                process_code = int(code_value) if code_value is not None else 0
        else:
            process_code = 0
            
        # Extract UUT process code if available (for test operation reference)
        uut_process_code = None
        if uut_report:
            if isinstance(uut_report, UUTReport):
                uut_process_code = uut_report.process_code
            else:
                uut_process_code = uut_report.get('process_code', uut_report.get('processCode'))
        
        # Debug info: UUR uses repair operation code, UUT uses test operation code
        # UUR process_code should be isRepairOperation=true, UUT reference is via refUUT
        
        # Create UUR info with all required fields
        uur_info = UURInfo(
            user=operator_name or "Operator",
            processCode=uut_process_code,  # This should be the UUT's test operation code
            refUUT=str(uut_id) if uut_id else None,
            confirmDate=datetime.now(timezone.utc).isoformat() + "Z",
            finalizeDate=datetime.now(timezone.utc).isoformat() + "Z",
            execTime=0.0
        )
        
        # Create UUR report using WSJF model
        report = UURReport(
            pn=part_pn or "",
            sn=part_sn or "",
            rev=part_rev or "",
            process_code=process_code,
            result="P",  # Default to Passed, will be updated when completed
            machineName=self.station_name,
            location=self.location,
            purpose=self.purpose,
            start=datetime.now(timezone.utc),
            uut_report_id=uut_id
        )
        
        # Set the UUR info after creation (this ensures proper alias handling)
        report.uur_info = uur_info
        
        # Copy sub units from UUT report if available and has sub units
        sub_units_copied = False
        if uut_report and isinstance(uut_report, UUTReport) and uut_report.sub_units:
            # Copy sub units from UUT report and convert to SubRepair units
            for sub_unit in uut_report.sub_units:
                # Create SubRepair from existing SubUnit
                sub_repair = report.add_sub_repair(
                    part_type=sub_unit.part_type or "Main Unit",
                    sn=sub_unit.sn,
                    pn=sub_unit.pn,
                    rev=sub_unit.rev or "",
                    idx=sub_unit.idx,
                    parent_idx=sub_unit.parent_idx
                )
                
                # Add failure to the main sub repair unit (idx 0) if categories/codes provided
                if sub_unit.idx == 0 and failure_category and failure_code:
                    sub_repair.add_failure(
                        category=failure_category,
                        code=failure_code,
                        comment="Component replacement required during repair - using repair operation codes",
                        com_ref="C15"  # Example component reference
                    )
            sub_units_copied = True
        
        # Create main sub repair unit if no UUT sub units were copied
        if not sub_units_copied:
            sub_repair = report.add_sub_repair(
                part_type="Main Unit",
                sn=part_sn or "",
                pn=part_pn or "",
                rev=part_rev or "",
                idx=0  # Main unit must have index 0
            )
            
            # Add failure only if categories/codes are provided (may not be required for all UUR reports)
            if failure_category and failure_code:
                sub_repair.add_failure(
                    category=failure_category,
                    code=failure_code,
                    comment="Component replacement required during repair - using repair operation codes",
                    com_ref="C15"  # Example component reference
                )
        
        # Skip adding RepairType misc info to avoid validation errors
        # The repair operation code should be sufficient for server validation
            
        return report

    def submit_report(
        self,
        report: Union[Dict[str, Any], UUTReport, UURReport],
        method: SubmitMethod = SubmitMethod.Automatic
    ) -> bool:
        """
        Submit a report to the server.
        
        Args:
            report: Report to submit (dictionary or WSJF model instance)
            method: Submission method
            
        Returns:
            True if successful
        """
        try:
            if method == SubmitMethod.Offline:
                return self._save_report_offline(report)
            elif method == SubmitMethod.Online:
                return self._submit_report_online(report)
            elif method == SubmitMethod.Automatic:
                if self._status == APIStatusType.Online:
                    try:
                        return self._submit_report_online(report)
                    except Exception as e:
                        self._last_service_exception = e
                        self._status = APIStatusType.Offline
                        return self._save_report_offline(report)
                else:
                    return self._save_report_offline(report)
            else:
                raise ValueError(f"Invalid submit method: {method}")
                
        except Exception as e:
            self._last_service_exception = e
            if self._log_exceptions:
                print(f"Submit report error: {e}")
            if self._rethrow_exception:
                raise
            return False

    def _submit_report_online(self, report: Union[Dict[str, Any], UUTReport, UURReport]) -> bool:
        """Submit report directly to server using REST API."""
        try:
            if not self._connection:
                raise Exception("No connection available")
                
            # Convert WSJF model to dictionary if needed
            if isinstance(report, (UUTReport, UURReport)):
                # Use Pydantic's model_dump with by_alias=True to get proper field names
                # and mode='json' to handle UUID serialization automatically
                report_dict = report.model_dump(by_alias=True, exclude_none=True, mode='json')
            else:
                # Handle legacy dictionary format
                report_dict = report
            
            # Debug: Log the JSON being sent
            if self._log_exceptions:
                print(f"Submitting WSJF report to /api/Report/WSJF:")
                print(f"Report JSON: {json.dumps(report_dict, indent=2, default=str)}")
                
                # Debug: Inspect the original report object and converted dictionary
                print(f"\n=== DEBUG INFO ===")
                print(f"Report type: {type(report)}")
                if isinstance(report, (UUTReport, UURReport)):
                    print(f"Report model fields: {list(report.__dict__.keys())}")
                    print(f"Report.info: {getattr(report, 'info', 'NOT FOUND')}")
                    print(f"Report model dump keys: {list(report_dict.keys())}")
                    if isinstance(report, UUTReport):
                        print(f"Looking for 'uut' field in serialized data: {'uut' in report_dict}")
                    elif isinstance(report, UURReport):
                        print(f"Looking for 'uur' field in serialized data: {'uur' in report_dict}")
                print("=================\n")
            
            # Use the REST API function to submit report
            result = submit_wsjf_report(report_dict, client=self._connection.client)
            
            # Log the result
            if self._log_exceptions:
                print(f"Submission result: {result}")
                
            # Check if submission was successful
            if result and hasattr(result, 'report_id'):
                if self._log_exceptions:
                    print(f"✅ Report successfully submitted with ID: {result.report_id}")
                return True
            else:
                if self._log_exceptions:
                    print("❌ Report submission failed - no report ID returned")
                return False
                
        except Exception as e:
            self._last_service_exception = e
            
            # Enhanced error logging with REST API response details
            error_details = self._extract_api_error_details(e)
            
            if self._log_exceptions:
                print(f"❌ Report submission failed:")
                print(f"   Error Type: {type(e).__name__}")
                print(f"   Error Message: {str(e)}")
                if error_details:
                    print(f"   HTTP Status: {error_details.get('status_code', 'Unknown')}")
                    print(f"   Response Body: {error_details.get('response_body', 'No response body')}")
                    if error_details.get('validation_errors'):
                        print(f"   Validation Errors:")
                        for error in error_details['validation_errors']:
                            print(f"     - {error}")
            
            # Don't re-raise in this context, return False to indicate failure
            return False

    def _extract_api_error_details(self, exception: Exception) -> Dict[str, Any]:
        """Extract detailed error information from REST API exceptions."""
        error_details = {}
        
        # Check if the exception has a 'response' attribute before accessing it
        response = getattr(exception, 'response', None)
        if response is not None:
            error_details['status_code'] = getattr(response, 'status_code', None)
            
            # Try to get response body
            try:
                if hasattr(response, 'text'):
                    response_text = response.text
                elif hasattr(response, 'content'):
                    response_text = response.content.decode('utf-8') if response.content else ''
                else:
                    response_text = str(response)
                    
                error_details['response_body'] = response_text
                
                # Try to parse as JSON to get structured validation errors
                try:
                    response_json = json.loads(response_text)
                    error_details['response_json'] = response_json
                    
                    # Extract common validation error patterns
                    validation_errors = []
                    if isinstance(response_json, dict):
                        # Common patterns for validation errors
                        if 'errors' in response_json:
                            if isinstance(response_json['errors'], list):
                                validation_errors.extend(response_json['errors'])
                            elif isinstance(response_json['errors'], dict):
                                for field, msgs in response_json['errors'].items():
                                    if isinstance(msgs, list):
                                        for msg in msgs:
                                            validation_errors.append(f"{field}: {msg}")
                                    else:
                                        validation_errors.append(f"{field}: {msgs}")
                        
                        if 'message' in response_json:
                            validation_errors.append(response_json['message'])
                            
                        if 'detail' in response_json:
                            validation_errors.append(response_json['detail'])
                    
                    if validation_errors:
                        error_details['validation_errors'] = validation_errors
                        
                except json.JSONDecodeError:
                    # Response is not JSON, keep as text
                    pass
                    
            except Exception:
                error_details['response_body'] = 'Failed to read response body'
        
        # Check for other common error attributes
        status_code = getattr(exception, 'status_code', None)
        if status_code is not None:
            error_details['status_code'] = status_code
            
        return error_details

    def _save_report_offline(self, report: Union[Dict[str, Any], UUTReport, UURReport]) -> bool:
        """Save report to offline queue."""
        try:
            reports_dir = os.path.join(self.data_dir, "Reports")
            os.makedirs(reports_dir, exist_ok=True)
            
            # Convert to dictionary if needed
            if isinstance(report, (UUTReport, UURReport)):
                report_dict = report.model_dump(by_alias=True, exclude_none=True)
                report_id = str(report.id)
            else:
                report_dict = report
                report_id = report.get('report_id', report.get('id', 'unknown'))
            
            report_file = os.path.join(reports_dir, f"{report_id}.json")
            with open(report_file, 'w') as f:
                json.dump(report_dict, f, indent=2, default=str)
                
            return True
            
        except Exception as e:
            self._last_service_exception = e
            if self._log_exceptions:
                print(f"Save report offline error: {e}")
            return False

    def get_pending_report_count(self) -> int:
        """
        Get number of reports waiting to be sent to server.
        
        Returns:
            Number of pending reports
        """
        try:
            reports_dir = os.path.join(self.data_dir, "Reports")
            if not os.path.exists(reports_dir):
                return 0
                
            return len([f for f in os.listdir(reports_dir) if f.endswith('.json')])
            
        except Exception:
            return 0

    def submit_pending_reports(self) -> int:
        """
        Submit all pending reports to server.
        
        Returns:
            Number of reports successfully submitted
        """
        if self._status != APIStatusType.Online:
            return 0
            
        submitted_count = 0
        try:
            reports_dir = os.path.join(self.data_dir, "Reports")
            if not os.path.exists(reports_dir):
                return 0
                
            for filename in os.listdir(reports_dir):
                if not filename.endswith('.json'):
                    continue
                    
                try:
                    filepath = os.path.join(reports_dir, filename)
                    with open(filepath, 'r') as f:
                        report = json.load(f)
                        
                    if self._submit_report_online(report):
                        os.remove(filepath)
                        submitted_count += 1
                    else:
                        # Stop on first failure
                        break
                        
                except Exception as e:
                    if self._log_exceptions:
                        print(f"Error submitting pending report {filename}: {e}")
                    # Continue with next report
                    
        except Exception as e:
            self._last_service_exception = e
            if self._log_exceptions:
                print(f"Submit pending reports error: {e}")
                
        return submitted_count

    def ping(self) -> bool:
        """
        Send a ping to the server.
        
        Returns:
            True if server responds correctly
        """
        try:
            if not self._connection:
                return False
                
            # Use the existing test_connection method as a ping
            result = self._connection.test_connection()
            if result:
                self._status = APIStatusType.Online
            else:
                self._status = APIStatusType.Offline
            return result
            
        except Exception as e:
            self._last_service_exception = e
            self._status = APIStatusType.Offline
            if self._log_exceptions:
                print(f"Ping error: {e}")
            return False

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        # Cleanup if needed
        pass