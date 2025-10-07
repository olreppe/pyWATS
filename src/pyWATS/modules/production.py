"""
Production module for WATS API.

This module provides functionality for managing production tracking,
control, and production-related operations in the WATS system.
"""

from typing import List, Optional, Dict, Any, Tuple, cast
from datetime import datetime
from enum import Enum
from uuid import UUID
import io
from .base import BaseModule
from ..exceptions import WATSException, WATSNotFoundError

# Import REST API endpoints
from ..rest_api.public.api.production import (
    production_get_unit_public,
    production_get_unit_verification,
    production_set_unit_phase_public
)
from ..rest_api.public.client import Client
from ..rest_api.public.models.production_get_unit_public_response_200 import (
    ProductionGetUnitPublicResponse200
)
from ..rest_api.public.models.virinco_wats_web_dashboard_models_public_unit_verification_grade import (
    VirincoWATSWebDashboardModelsPublicUnitVerificationGrade
)


class StatusEnum(Enum):
    """Status enumeration."""
    RELEASED = "Released"
    DRAFT = "Draft"
    OBSOLETE = "Obsolete"


class Unit_Phase(Enum):
    """Unit phase enumeration."""
    INITIAL = "Initial"
    IN_PROCESS = "InProcess"
    PASSED = "Passed"
    FAILED = "Failed"
    SCRAPPED = "Scrapped"


class UnitVerificationResponse:
    """Response for unit verification operations."""
    def __init__(self, is_valid: bool = True, message: str = ""):
        self.is_valid = is_valid
        self.message = message


class UnitHistory:
    """Unit history information."""
    def __init__(self, serial_number: str, **kwargs):
        self.serial_number = serial_number
        self.timestamp = kwargs.get('timestamp', datetime.now())
        self.operation = kwargs.get('operation', '')
        self.details = kwargs.get('details', {})


class UnitInfo:
    """Unit information with hierarchy and tag support."""
    
    class DataType(Enum):
        """Data type enumeration for unit info."""
        STRING = 0
        INTEGER = 1
        FLOAT = 2
        BOOLEAN = 3
        DATETIME = 4

    def __init__(self, serial_number: str, part_number: str = "", **kwargs):
        self.serial_number = serial_number
        self.part_number = part_number
        self._parent = kwargs.get('parent')
        self._children = kwargs.get('children', [])
        self._tags = kwargs.get('tags', {})
        self._xml_data = kwargs.get('xml_data', "")

    def get_info_by_field(self, field: str, data_type: 'UnitInfo.DataType') -> str:
        """
        [Obsolete] Get information by field name.
        
        Args:
            field: Field name
            data_type: Data type
            
        Returns:
            Field value as string
        """
        # Basic implementation for common fields
        if field == "serial_number":
            return self.serial_number
        elif field == "part_number":
            return self.part_number
        return ""

    def get_tag_value(self, tag: str, data_type: 'UnitInfo.DataType') -> str:
        """
        Get a tag value with specified data type.
        
        Args:
            tag: Tag name
            data_type: Data type
            
        Returns:
            Tag value as string
        """
        tag_value = self._tags.get(tag, "")
        return str(tag_value)

    def get_tag_value_int(self, tag: str, data_type: int) -> str:
        """
        Get a tag value with integer data type identifier.
        
        Args:
            tag: Tag name
            data_type: Data type as integer
            
        Returns:
            Tag value as string
        """
        # Convert integer to DataType enum if possible
        try:
            enum_type = UnitInfo.DataType(data_type)
            return self.get_tag_value(tag, enum_type)
        except ValueError:
            return str(self._tags.get(tag, ""))

    def set_tag_value(self, tag: str, tag_value: str) -> bool:
        """
        Set a tag value.
        
        Args:
            tag: Tag name
            tag_value: Tag value
            
        Returns:
            True if successful
        """
        try:
            self._tags[tag] = tag_value
            return True
        except Exception:
            return False

    def get_info(self, xpath: str, data_type: 'UnitInfo.DataType') -> str:
        """
        Get unit information using XPath with DataType enum.
        
        Args:
            xpath: XPath expression
            data_type: Data type
            
        Returns:
            Information value
        """
        # TODO: Implement actual XPath parsing on self._xml_data
        # For now, return empty string as placeholder
        return ""

    def get_info_int(self, xpath: str, data_type: int) -> str:
        """
        Get unit information using XPath with integer type.
        
        Args:
            xpath: XPath expression
            data_type: Data type as integer
            
        Returns:
            Information value
        """
        try:
            enum_type = UnitInfo.DataType(data_type)
            return self.get_info(xpath, enum_type)
        except ValueError:
            return ""

    def has_parent(self) -> bool:
        """Check if unit has a parent."""
        return self._parent is not None

    def get_child_count(self) -> int:
        """Get the number of child units."""
        return len(self._children)

    def get_parent(self) -> 'UnitInfo':
        """Get the parent unit info."""
        if self._parent is None:
            raise WATSException("Unit has no parent")
        return self._parent

    def get_child(self, index: int) -> 'UnitInfo':
        """
        Get a child unit by index.
        
        Args:
            index: Index of the child
            
        Returns:
            UnitInfo object for the child
        """
        if index < 0 or index >= len(self._children):
            raise WATSException(f"Child index {index} out of range")
        return self._children[index]

    def get_children(self) -> List['UnitInfo']:
        """Get all child units."""
        return self._children.copy()


class SerialNumberType:
    """Serial number type information."""
    def __init__(self, name: str, **kwargs):
        self.name = name


class SerialNumbersSN:
    """Serial number structure."""
    def __init__(self, serial_number: str, **kwargs):
        self.serial_number = serial_number


class SerialNumberHandler:
    """Serial number handler for managing serial numbers."""
    
    class RequestType(Enum):
        """Request type enumeration."""
        SINGLE = "Single"
        BATCH = "Batch"
        POOL = "Pool"

    class Status(Enum):
        """Handler status enumeration."""
        INITIALIZED = "Initialized"
        CONNECTED = "Connected"
        DISCONNECTED = "Disconnected"
        ERROR = "Error"

    def __init__(self, serial_number_type_name: str):
        """
        Initialize serial number handler.
        
        Args:
            serial_number_type_name: Name of the serial number type
        """
        self.serial_number_type_name = serial_number_type_name

    @staticmethod
    def get_serial_number_types() -> List[SerialNumberType]:
        """Get available serial number types."""
        raise NotImplementedError("SerialNumberHandler.get_serial_number_types not implemented")

    def get_local_serial_numbers(self) -> List[SerialNumbersSN]:
        """Get local serial numbers."""
        raise NotImplementedError("SerialNumberHandler.get_local_serial_numbers not implemented")

    def format_as_mac(self, i: int, separator: str) -> str:
        """
        Format integer as MAC address.
        
        Args:
            i: Integer value
            separator: Separator character
            
        Returns:
            Formatted MAC address string
        """
        raise NotImplementedError("SerialNumberHandler.format_as_mac not implemented")

    def generate_and_upload_serial_numbers(self, token_id: str, service_url: str,
                                          from_sn: int, to_sn: int, separator: str,
                                          token: UUID) -> Tuple[List[str], int, int]:
        """
        Generate and upload serial numbers.
        
        Args:
            token_id: Token identifier
            service_url: Service URL
            from_sn: Starting serial number
            to_sn: Ending serial number
            separator: Separator character
            token: Token UUID
            
        Returns:
            Tuple of (serial_numbers, uploaded_count, rejected_count)
        """
        raise NotImplementedError("SerialNumberHandler.generate_and_upload_serial_numbers not implemented")

    def upload_serial_numbers_from_file(self, token_id: str, service_url: str,
                                       file_name: str, token: UUID) -> Tuple[List[str], int, int]:
        """
        Upload serial numbers from file.
        
        Args:
            token_id: Token identifier
            service_url: Service URL
            file_name: File name
            token: Token UUID
            
        Returns:
            Tuple of (serial_numbers, uploaded_count, rejected_count)
        """
        raise NotImplementedError("SerialNumberHandler.upload_serial_numbers_from_file not implemented")

    def initialize(self, token_id: str, service_url: str, request_type: 'SerialNumberHandler.RequestType',
                  only_in_sequence: bool, batch_size: int, fetch_when_less_than: int,
                  start_from_serial_number: str, site_name: str, token: Optional[UUID] = None):
        """
        Initialize the serial number handler.
        
        Args:
            token_id: Token identifier
            service_url: Service URL
            request_type: Request type
            only_in_sequence: Only in sequence flag
            batch_size: Batch size
            fetch_when_less_than: Fetch threshold
            start_from_serial_number: Starting serial number
            site_name: Site name
            token: Optional token UUID
        """
        raise NotImplementedError("SerialNumberHandler.initialize not implemented")

    def set_reuse_on_duplicate_request(self, on: bool):
        """Set reuse on duplicate request flag."""
        raise NotImplementedError("SerialNumberHandler.set_reuse_on_duplicate_request not implemented")

    def get_reuse_on_duplicate_request(self) -> bool:
        """Get reuse on duplicate request flag."""
        raise NotImplementedError("SerialNumberHandler.get_reuse_on_duplicate_request not implemented")

    def cancel_reservations(self, token: Optional[UUID] = None):
        """Cancel reservations."""
        raise NotImplementedError("SerialNumberHandler.cancel_reservations not implemented")

    def get_status(self) -> 'SerialNumberHandler.Status':
        """Get handler status."""
        raise NotImplementedError("SerialNumberHandler.get_status not implemented")

    def get_free_local_serial_numbers(self) -> int:
        """Get count of free local serial numbers."""
        raise NotImplementedError("SerialNumberHandler.get_free_local_serial_numbers not implemented")

    def get_pool_info(self) -> Tuple[bool, int, int, str, str]:
        """
        Get pool information (basic version).
        
        Returns:
            Tuple of (only_in_sequence, batch_size, fetch_when_less_than, start_from_serial_number, site_name)
        """
        raise NotImplementedError("SerialNumberHandler.get_pool_info not implemented")

    def get_pool_info_extended(self) -> Tuple[bool, int, int, str, str, 'SerialNumberHandler.RequestType']:
        """
        Get extended pool information.
        
        Returns:
            Tuple of (only_in_sequence, batch_size, fetch_when_less_than, start_from_serial_number, site_name, request_type)
        """
        raise NotImplementedError("SerialNumberHandler.get_pool_info_extended not implemented")

    def get_serial_numbers(self, num_to_get: int, serialnumber_ref: str, partnumber_ref: str) -> List[str]:
        """
        Get multiple serial numbers.
        
        Args:
            num_to_get: Number of serial numbers to get
            serialnumber_ref: Serial number reference
            partnumber_ref: Part number reference
            
        Returns:
            List of serial numbers
        """
        raise NotImplementedError("SerialNumberHandler.get_serial_numbers not implemented")

    def get_serial_number(self, serialnumber_ref: str, partnumber_ref: str) -> str:
        """
        Get a single serial number.
        
        Args:
            serialnumber_ref: Serial number reference
            partnumber_ref: Part number reference
            
        Returns:
            Serial number
        """
        raise NotImplementedError("SerialNumberHandler.get_serial_number not implemented")

    def get_taken_serial_numbers(self, serialnumber_ref: str, partnumber_ref: str) -> List[str]:
        """
        Get taken serial numbers.
        
        Args:
            serialnumber_ref: Serial number reference
            partnumber_ref: Part number reference
            
        Returns:
            List of taken serial numbers
        """
        raise NotImplementedError("SerialNumberHandler.get_taken_serial_numbers not implemented")

    def mac_to_int(self, mac: str) -> int:
        """
        Convert MAC address to integer.
        
        Args:
            mac: MAC address string
            
        Returns:
            Integer value
        """
        raise NotImplementedError("SerialNumberHandler.mac_to_int not implemented")

    @staticmethod
    def cancel_all_reservations():
        """Cancel all reservations (static method)."""
        raise NotImplementedError("SerialNumberHandler.cancel_all_reservations not implemented")


class ProductionModule(BaseModule):
    """
    Production tracking and control module.
    
    Provides methods for:
    - Unit identification and management
    - Production tracking and control
    - Unit state and phase management
    - Unit history and verification
    - Parent-child unit relationships
    """

    def __init__(self, http_client, culture_code: Optional[str] = None):
        """
        Initialize production module.
        
        Args:
            http_client: HTTP client
            culture_code: Optional culture code
        """
        super().__init__(http_client)
        self.culture_code = culture_code

    def is_connected(self) -> bool:
        """Check if production module is connected."""
        raise NotImplementedError("Production.is_connected not implemented")

    def get_unit_info(self, serial_number: str, part_number: str = "") -> UnitInfo:
        """
        Get unit information.
        
        Args:
            serial_number: Serial number of the unit
            part_number: Part number of the unit (optional)
            
        Returns:
            UnitInfo object
            
        Raises:
            WATSNotFoundError: If the unit is not found
            WATSException: If the operation fails
        """
        self._validate_id(serial_number, "serial_number")
        
        if not part_number:
            raise WATSException("Part number is required for get_unit_info")
        
        try:
            # Call the REST API to get unit data
            response = production_get_unit_public.sync(
                serial_number=serial_number,
                part_number=part_number,
                client=cast(Client, self.http_client)
            )
            
            if response is None:
                raise WATSNotFoundError(f"Unit with serial number '{serial_number}' and part number '{part_number}' not found")
            
            # Convert the REST API response to UnitInfo
            unit_info = UnitInfo(
                serial_number=serial_number,
                part_number=part_number,
                # TODO: Map additional fields from response
            )
            
            return unit_info
            
        except Exception as e:
            if isinstance(e, (WATSNotFoundError, WATSException)):
                raise
            if "404" in str(e) or "not found" in str(e).lower():
                raise WATSNotFoundError(f"Unit with serial number '{serial_number}' not found")
            raise WATSException(f"Failed to get unit info for {serial_number}: {str(e)}")

    def identify_uut_simple(self, part_number: str = "") -> Tuple[UnitInfo, bool]:
        """
        Simple UUT identification.
        
        Args:
            part_number: Part number (optional)
            
        Returns:
            Tuple of (UnitInfo, continue_flag)
        """
        raise NotImplementedError("Production.identify_uut (simple) not implemented")

    def identify_uut(self, selected_test_operation, serial_number: str = "", part_number: str = "",
                    include_test_operation: bool = False, select_test_operation: bool = True,
                    custom_text: Optional[str] = None, always_on_top: bool = True, use_workflow: bool = False,
                    workflow_status: StatusEnum = StatusEnum.RELEASED,
                    context: Optional[Dict[str, Any]] = None) -> Tuple[UnitInfo, bool]:
        """
        Full UUT identification with options.
        
        Args:
            selected_test_operation: Reference to selected test operation
            serial_number: Serial number
            part_number: Part number
            include_test_operation: Include test operation
            select_test_operation: Select test operation
            custom_text: Custom text
            always_on_top: Always on top flag
            use_workflow: Use workflow flag
            workflow_status: Workflow status
            context: Context dictionary
            
        Returns:
            Tuple of (UnitInfo, continue_flag)
        """
        raise NotImplementedError("Production.identify_uut (full) not implemented")

    def set_unit_process(self, serial_number: str, part_number: str, process_name: str):
        """
        Set unit process.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            process_name: Process name
        """
        raise NotImplementedError("Production.set_unit_process not implemented")

    def verify_unit(self, serial_number: str, part_number: str = "") -> UnitVerificationResponse:
        """
        Verify a unit.
        
        Args:
            serial_number: Serial number of the unit
            part_number: Part number of the unit (optional)
            
        Returns:
            UnitVerificationResponse object
            
        Raises:
            WATSException: If the verification fails
        """
        self._validate_id(serial_number, "serial_number")
        
        try:
            # Call the REST API to verify the unit
            from ..rest_api.public.types import UNSET
            response = production_get_unit_verification.sync(
                serial_number=serial_number,
                part_number=part_number if part_number else UNSET,
                client=cast(Client, self.http_client)
            )
            
            if response is None:
                return UnitVerificationResponse(is_valid=False, message="Unit verification failed")
            
            # TODO: Properly interpret the verification response
            # For now, assume valid if we got a response
            return UnitVerificationResponse(is_valid=True, message="Unit verified successfully")
            
        except Exception as e:
            return UnitVerificationResponse(is_valid=False, message=f"Verification failed: {str(e)}")

    def set_unit_phase(self, serial_number: str, part_number: str, phase: Unit_Phase):
        """
        Set unit phase using enum.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            phase: Unit phase enum
            
        Raises:
            WATSException: If the operation fails
        """
        self._validate_id(serial_number, "serial_number")
        self._validate_id(part_number, "part_number")
        
        try:
            # Convert enum to integer for API call
            phase_mapping = {
                Unit_Phase.INITIAL: 0,
                Unit_Phase.IN_PROCESS: 1,
                Unit_Phase.PASSED: 2,
                Unit_Phase.FAILED: 3,
                Unit_Phase.SCRAPPED: 4
            }
            phase_int = phase_mapping.get(phase, 0)
            
            # Call the REST API to set unit phase
            response = production_set_unit_phase_public.sync(
                serial_number=serial_number,
                part_number=part_number,
                phase=phase_int,
                client=cast(Client, self.http_client)
            )
            
            # TODO: Check response for success/failure
            
        except Exception as e:
            raise WATSException(f"Failed to set unit phase for {serial_number}: {str(e)}")

    def set_unit_phase_string(self, serial_number: str, part_number: str, phase: str):
        """
        Set unit phase using string.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            phase: Phase as string
            
        Raises:
            WATSException: If the operation fails
        """
        try:
            # Convert string to enum first for validation
            phase_enum = Unit_Phase(phase)
            self.set_unit_phase(serial_number, part_number, phase_enum)
        except ValueError:
            raise WATSException(f"Invalid phase value: {phase}")
        except Exception as e:
            raise WATSException(f"Failed to set unit phase for {serial_number}: {str(e)}")

    def get_unit_process(self, serial_number: str, part_number: str) -> str:
        """
        Get unit process.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            
        Returns:
            Process name
        """
        raise NotImplementedError("Production.get_unit_process not implemented")

    def get_unit_phase(self, serial_number: str, part_number: str) -> Unit_Phase:
        """
        Get unit phase as enum.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            
        Returns:
            Unit phase enum
        """
        raise NotImplementedError("Production.get_unit_phase not implemented")

    def get_unit_phase_string(self, serial_number: str, part_number: str) -> str:
        """
        Get unit phase as string.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            
        Returns:
            Phase as string
        """
        raise NotImplementedError("Production.get_unit_phase_string not implemented")

    def get_unit_state_history(self, serial_number: str, part_number: str) -> Tuple[int, List[str], List[str], List[datetime]]:
        """
        Get unit state history.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            
        Returns:
            Tuple of (count, states, phases, date_times)
        """
        raise NotImplementedError("Production.get_unit_state_history not implemented")

    def get_unit_history(self, serial_number: str, part_number: Optional[str] = None, details: bool = False) -> List[UnitHistory]:
        """
        Get unit history.
        
        Args:
            serial_number: Serial number
            part_number: Part number (optional)
            details: Include details flag
            
        Returns:
            List of UnitHistory objects
        """
        raise NotImplementedError("Production.get_unit_history not implemented")

    def set_parent(self, serial_number: str, parent_serial_number: str) -> bool:
        """
        Set parent unit.
        
        Args:
            serial_number: Serial number
            parent_serial_number: Parent serial number
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Production.set_parent not implemented")

    def create_unit(self, serial_number: str, part_number: str, revision: str, batch_number: str) -> bool:
        """
        Create a new unit.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            revision: Revision
            batch_number: Batch number
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Production.create_unit not implemented")

    def add_child_unit(self, culture_code: str, parent_serial_number: str, parent_part_number: str,
                      child_serial_number: str, child_part_number: str, check_part_number: str,
                      check_revision: str) -> Tuple[bool, str]:
        """
        Add child unit.
        
        Args:
            culture_code: Culture code
            parent_serial_number: Parent serial number
            parent_part_number: Parent part number
            child_serial_number: Child serial number
            child_part_number: Child part number
            check_part_number: Check part number
            check_revision: Check revision
            
        Returns:
            Tuple of (success, message)
        """
        raise NotImplementedError("Production.add_child_unit not implemented")

    def remove_child_unit(self, culture_code: str, parent_serial_number: str, parent_part_number: str,
                         child_serial_number: str, child_part_number: str) -> Tuple[bool, str]:
        """
        Remove child unit.
        
        Args:
            culture_code: Culture code
            parent_serial_number: Parent serial number
            parent_part_number: Parent part number
            child_serial_number: Child serial number
            child_part_number: Child part number
            
        Returns:
            Tuple of (success, message)
        """
        raise NotImplementedError("Production.remove_child_unit not implemented")

    def remove_all_child_units(self, culture_code: str, parent_serial_number: str,
                              parent_part_number: str) -> Tuple[bool, str]:
        """
        Remove all child units.
        
        Args:
            culture_code: Culture code
            parent_serial_number: Parent serial number
            parent_part_number: Parent part number
            
        Returns:
            Tuple of (success, message)
        """
        raise NotImplementedError("Production.remove_all_child_units not implemented")

    def update_unit_obsolete(self, serial_number: str, new_part_number: str, new_revision: str) -> bool:
        """
        [Obsolete] Update unit.
        
        Args:
            serial_number: Serial number
            new_part_number: New part number
            new_revision: New revision
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Production.update_unit (obsolete) not implemented")

    def update_unit(self, serial_number: str, part_number: str, new_part_number: str, new_revision: str) -> bool:
        """
        Update unit.
        
        Args:
            serial_number: Serial number
            part_number: Current part number
            new_part_number: New part number
            new_revision: New revision
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Production.update_unit not implemented")

    def update_unit_attribute_obsolete(self, serial_number: str, attribute_name: str, attribute_value: str) -> bool:
        """
        [Obsolete] Update unit attribute.
        
        Args:
            serial_number: Serial number
            attribute_name: Attribute name
            attribute_value: Attribute value
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Production.update_unit_attribute (obsolete) not implemented")

    def update_unit_tag(self, serial_number: str, part_number: str, tag_name: str, tag_value: str) -> bool:
        """
        Update unit tag.
        
        Args:
            serial_number: Serial number
            part_number: Part number
            tag_name: Tag name
            tag_value: Tag value
            
        Returns:
            True if successful
        """
        raise NotImplementedError("Production.update_unit_tag not implemented")

    def get_unit_verification(self, serial_number: str, part_number: Optional[str] = None) -> UnitVerificationResponse:
        """
        Get unit verification.
        
        Args:
            serial_number: Serial number
            part_number: Part number (optional)
            
        Returns:
            UnitVerificationResponse object
        """
        raise NotImplementedError("Production.get_unit_verification not implemented")

    # Legacy methods for backward compatibility
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all production records."""
        return [{"message": "Production functionality will be implemented with actual API endpoints"}]
    
    def get_by_id(self, production_id: str) -> Dict[str, Any]:
        """Get a specific production record by ID."""
        self._validate_id(production_id, "production")
        return {"message": f"Production {production_id} functionality will be implemented with actual API endpoints"}
    
    def get_active_jobs(self) -> List[Dict[str, Any]]:
        """Get currently active production jobs."""
        return [{"message": "Active production jobs functionality will be implemented with actual API endpoints"}]