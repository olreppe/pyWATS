"""
MES Production Module

Handles unit information, production operations, and unit lifecycle management.
This module mirrors the Interface.MES Production functionality.
"""

from typing import Optional, List, Union, Dict, Any
from datetime import datetime

from .base import MESBase
from .models import (
    UnitInfo, UnitHistory, UnitVerificationResponse, UnitPhase, 
    IdentifyUnitRequest, StatusEnum, MESResponse
)
from ..rest_api.client import WATSClient
from ..connection import WATSConnection


class Production(MESBase):
    """
    Production management for WATS MES.
    
    Provides functionality for:
    - Unit information retrieval and management
    - Unit lifecycle operations (create, update, phase changes)
    - Parent/child unit relationships
    - Unit history and verification
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Production module.
        
        Args:
            connection: WATS connection or client instance
        """
        super().__init__(connection)
    
    def is_connected(self) -> bool:
        """
        Check if connected to WATS MES Server.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            response = self._client.get("/api/internal/Production/isConnected")
            return response.status_code == 200
        except Exception:
            return False
    
    def get_unit_info(
        self, 
        serial_number: str, 
        part_number: Optional[str] = None
    ) -> Optional[UnitInfo]:
        """
        Get unit information without GUI.
        
        Args:
            serial_number: Unit serial number
            part_number: Optional part number for validation
            
        Returns:
            UnitInfo object or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {"serialNumber": serial_number}
        if part_number:
            params["partNumber"] = part_number
        
        try:
            # ?? INTERNAL API: Uses internal production endpoint
            response_data = self._rest_get_json(
                "/api/internal/Production/GetUnitInfo", 
                response_type=UnitInfo
            )
            if isinstance(response_data, UnitInfo):
                return response_data
            elif isinstance(response_data, dict):
                return UnitInfo.model_validate(response_data)  # type: ignore
            return None
        except Exception:
            return None
    
    def identify_uut(
        self,
        part_number: Optional[str] = None,
        serial_number: Optional[str] = None,
        include_test_operation: bool = False,
        select_test_operation: bool = True,
        custom_text: Optional[str] = None,
        always_on_top: bool = True,
        use_workflow: bool = False,
        workflow_status: StatusEnum = StatusEnum.RELEASED,
        context: Optional[Dict[str, Any]] = None
    ) -> Optional[UnitInfo]:
        """
        Display unit identification dialog.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Optional part number filter
            serial_number: Optional serial number pre-fill
            include_test_operation: Include test operation in dialog
            select_test_operation: Allow test operation selection
            custom_text: Custom dialog text
            always_on_top: Keep dialog on top
            use_workflow: Use workflow context
            workflow_status: Workflow status filter
            context: Additional context data
            
        Returns:
            Selected UnitInfo or None if cancelled
            
        Raises:
            WATSAPIException: On API errors
        """
        request = IdentifyUnitRequest(
            partNumber=part_number,
            serialNumber=serial_number,
            includeTestOperation=include_test_operation,
            selectTestOperation=select_test_operation,
            customText=custom_text,
            alwaysOnTop=always_on_top,
            useWorkflow=use_workflow,
            workflowStatus=workflow_status,
            context=context or {}
        )
        
        response_data = self._rest_post_json(
            "/api/internal/Production/IdentifyUUT",
            request,
            response_type=UnitInfo
        )
        if isinstance(response_data, UnitInfo):
            return response_data
        elif isinstance(response_data, dict):
            return UnitInfo.model_validate(response_data)  # type: ignore
        return None
    
    def set_unit_process(
        self, 
        serial_number: str, 
        part_number: str, 
        process_name: str
    ) -> bool:
        """
        Set unit's process.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            process_name: Process name to set
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "processName": process_name
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/SetUnitProcess",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def set_unit_phase(
        self, 
        serial_number: str, 
        part_number: str, 
        phase: Union[UnitPhase, str]
    ) -> bool:
        """
        Set unit's phase.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            phase: Phase to set (UnitPhase enum or string)
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        phase_value = phase.value if isinstance(phase, UnitPhase) else phase
        
        data = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "phase": phase_value
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/SetUnitPhase",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def get_unit_process(self, serial_number: str, part_number: str) -> Optional[str]:
        """
        Get unit's current process.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            
        Returns:
            Process name or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        
        try:
            response = self._rest_get_json("/api/internal/Production/GetUnitProcess")
            return response.get("processName")
        except Exception:
            return None
    
    def get_unit_phase(
        self, 
        serial_number: str, 
        part_number: str
    ) -> Optional[UnitPhase]:
        """
        Get unit's current phase.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            
        Returns:
            UnitPhase or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        
        try:
            response = self._rest_get_json("/api/internal/Production/GetUnitPhase")
            phase_value = response.get("phase")
            return UnitPhase(phase_value) if phase_value is not None else None
        except Exception:
            return None
    
    def get_unit_phase_string(
        self, 
        serial_number: str, 
        part_number: str
    ) -> Optional[str]:
        """
        Get unit's phase as string.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            
        Returns:
            Phase name or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        phase = self.get_unit_phase(serial_number, part_number)
        return phase.name if phase else None
    
    def get_unit_state_history(
        self, 
        serial_number: str, 
        part_number: str
    ) -> int:
        """
        Get unit state/phase change history count.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            
        Returns:
            Number of state changes
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "serialNumber": serial_number,
            "partNumber": part_number
        }
        
        response = self._rest_get_json("/api/internal/Production/GetUnitStateHistory")
        return response.get("count", 0)
    
    def get_unit_history(
        self,
        serial_number: str,
        part_number: Optional[str] = None,
        details: bool = False
    ) -> List[UnitHistory]:
        """
        Get unit history list.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Optional unit part number
            details: Include detailed information
            
        Returns:
            List of UnitHistory objects
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "serialNumber": serial_number,
            "details": details
        }
        if part_number:
            params["partNumber"] = part_number
        
        response = self._rest_get_json("/api/internal/Production/GetUnitHistory")
        history_data = response.get("history", [])
        
        return [UnitHistory.parse_obj(item) for item in history_data]
    
    def set_parent(
        self, 
        serial_number: str, 
        parent_serial_number: str
    ) -> bool:
        """
        Create parent/child unit relationship.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Child unit serial number
            parent_serial_number: Parent unit serial number
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "parentSerialNumber": parent_serial_number
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/SetParent",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def create_unit(
        self,
        serial_number: str,
        part_number: str,
        revision: str,
        batch_number: str
    ) -> bool:
        """
        Create a new unit.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            revision: Unit revision
            batch_number: Batch number
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "revision": revision,
            "batchNumber": batch_number
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/CreateUnit",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def add_child_unit(
        self,
        culture_code: str,
        parent_serial_number: str,
        parent_part_number: str,
        child_serial_number: str,
        child_part_number: str,
        check_part_number: str,
        check_revision: str
    ) -> bool:
        """
        Add child unit to parent (box build).
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            culture_code: Culture code for localization
            parent_serial_number: Parent unit serial number
            parent_part_number: Parent unit part number
            child_serial_number: Child unit serial number
            child_part_number: Child unit part number
            check_part_number: Part number to validate
            check_revision: Revision to validate
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "cultureCode": culture_code,
            "parentSerialNumber": parent_serial_number,
            "parentPartNumber": parent_part_number,
            "childSerialNumber": child_serial_number,
            "childPartNumber": child_part_number,
            "checkPartNumber": check_part_number,
            "checkRevision": check_revision
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/AddChildUnit",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def remove_child_unit(
        self,
        culture_code: str,
        parent_serial_number: str,
        parent_part_number: str,
        child_serial_number: str,
        child_part_number: str
    ) -> bool:
        """
        Remove child unit from parent.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            culture_code: Culture code for localization
            parent_serial_number: Parent unit serial number
            parent_part_number: Parent unit part number
            child_serial_number: Child unit serial number
            child_part_number: Child unit part number
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "cultureCode": culture_code,
            "parentSerialNumber": parent_serial_number,
            "parentPartNumber": parent_part_number,
            "childSerialNumber": child_serial_number,
            "childPartNumber": child_part_number
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/RemoveChildUnit",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def remove_all_child_units(
        self,
        culture_code: str,
        parent_serial_number: str,
        parent_part_number: str
    ) -> bool:
        """
        Remove all child units from parent.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            culture_code: Culture code for localization
            parent_serial_number: Parent unit serial number
            parent_part_number: Parent unit part number
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "cultureCode": culture_code,
            "parentSerialNumber": parent_serial_number,
            "parentPartNumber": parent_part_number
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/RemoveAllChildUnits",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def update_unit(
        self,
        serial_number: str,
        part_number: str,
        new_part_number: str,
        new_revision: str
    ) -> bool:
        """
        Update unit's part number and revision.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Current part number
            new_part_number: New part number
            new_revision: New revision
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "newPartNumber": new_part_number,
            "newRevision": new_revision
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/UpdateUnit",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def update_unit_tag(
        self,
        serial_number: str,
        part_number: str,
        tag_name: str,
        tag_value: str
    ) -> bool:
        """
        Add or update unit tag value.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            tag_name: Tag name
            tag_value: Tag value
            
        Returns:
            True if successful
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "serialNumber": serial_number,
            "partNumber": part_number,
            "tagName": tag_name,
            "tagValue": tag_value
        }
        
        response = self._rest_post_json(
            "/api/internal/Production/UpdateUnitTag",
            data,
            response_type=MESResponse
        )
        if isinstance(response, MESResponse):
            return response.success
        elif isinstance(response, dict):
            return response.get("success", False)
        return False
    
    def get_unit_verification(
        self,
        serial_number: str,
        part_number: Optional[str] = None
    ) -> Optional[UnitVerificationResponse]:
        """
        Get unit verification response.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Optional unit part number
            
        Returns:
            UnitVerificationResponse or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {"serialNumber": serial_number}
        if part_number:
            params["partNumber"] = part_number
        
        try:
            response = self._rest_get_json(
                "/api/internal/Production/GetUnitVerification",
                response_type=UnitVerificationResponse
            )
            if isinstance(response, UnitVerificationResponse):
                return response
            elif isinstance(response, dict):
                return UnitVerificationResponse.model_validate(response)  # type: ignore
            return None
        except Exception:
            return None