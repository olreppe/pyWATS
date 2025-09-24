"""
MES Workflow Module

Handles automated workflow operations and test orchestration.
This module mirrors the Interface.MES Workflow functionality.
"""

from typing import Optional, Union, Dict, Any
from datetime import datetime

from .base import MESBase
from .models import (
    WorkflowResult, WorkflowContext, ActivityTestResult, 
    ActivityMethod, StatusEnum
)
from ..rest_api.client import WATSClient
from ..connection import WATSConnection


class Workflow(MESBase):
    """
    Workflow management for WATS MES.
    
    Provides functionality for:
    - Automated test orchestration
    - Workflow lifecycle management (start/end/suspend/resume)
    - Test validation and initialization
    - Check-in/check-out operations
    - Repair workflows
    - Box build operations
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Workflow module.
        
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
            response = self._client.get("/api/internal/workflow/isConnected")
            return response.status_code == 200
        except Exception:
            return False
    
    def start_test(
        self,
        serial_number: str,
        part_number: str,
        operation: str,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Start automated test.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            operation: Operation/test name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=operation,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/StartTest",
                workflow_context,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to start test: {str(e)}",
                context=workflow_context
            )
    
    def end_test(
        self,
        serial_number: str,
        part_number: str,
        operation: str,
        result: ActivityTestResult,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        End automated test.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            operation: Operation/test name
            result: Test result
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating success/failure
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=operation,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        data = {
            "context": workflow_context.dict(by_alias=True),
            "result": result.value
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/EndTest",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to end test: {str(e)}",
                result=result,
                context=workflow_context
            )
    
    def validate(
        self,
        serial_number: str,
        part_number: str,
        method: ActivityMethod,
        name: str,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Validate workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            method: Activity method to validate
            name: Validation name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating validation result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=name,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        data = {
            "context": workflow_context.dict(by_alias=True),
            "method": method.value,
            "name": name
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/Validate",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to validate workflow: {str(e)}",
                context=workflow_context
            )
    
    def initialize(
        self,
        serial_number: str,
        part_number: str,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Initialize workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating initialization result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/Initialize",
                workflow_context,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to initialize workflow: {str(e)}",
                context=workflow_context
            )
    
    def check_in(
        self,
        serial_number: str,
        part_number: str,
        operation: str,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Perform check-in operation.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            operation: Operation name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating check-in result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=operation,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/CheckIn",
                workflow_context,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to check in: {str(e)}",
                context=workflow_context
            )
    
    def check_out(
        self,
        serial_number: str,
        part_number: str,
        operation: str,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Perform check-out operation.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            operation: Operation name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating check-out result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=operation,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/CheckOut",
                workflow_context,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to check out: {str(e)}",
                context=workflow_context
            )
    
    def user_input(
        self,
        serial_number: str,
        part_number: str,
        operation: str,
        user_input_data: str,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Handle user input in workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            operation: Operation name
            user_input_data: User input data
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating input processing result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=operation,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        data = {
            "context": workflow_context.dict(by_alias=True),
            "userInput": user_input_data
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/UserInput",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to process user input: {str(e)}",
                context=workflow_context
            )
    
    def start_repair(
        self,
        serial_number: str,
        part_number: str,
        operation: Optional[str] = None,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Start repair workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            operation: Optional operation name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating repair start result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=operation,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/StartRepair",
                workflow_context,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to start repair: {str(e)}",
                context=workflow_context
            )
    
    def end_repair(
        self,
        serial_number: str,
        part_number: str,
        result: ActivityTestResult,
        operation: Optional[str] = None,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        End repair workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            result: Repair result
            operation: Optional operation name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating repair end result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            operation=operation,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        data = {
            "context": workflow_context.dict(by_alias=True),
            "result": result.value
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/EndRepair",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to end repair: {str(e)}",
                result=result,
                context=workflow_context
            )
    
    def scrap(
        self,
        serial_number: str,
        part_number: str,
        reason: Optional[str] = None,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Scrap unit under repair.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            reason: Scrap reason
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating scrap result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        data = {
            "context": workflow_context.dict(by_alias=True),
            "reason": reason
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/Scrap",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to scrap unit: {str(e)}",
                context=workflow_context
            )
    
    def suspend(
        self,
        serial_number: str,
        part_number: str,
        reason: Optional[str] = None,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Suspend workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            reason: Suspension reason
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating suspension result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        data = {
            "context": workflow_context.dict(by_alias=True),
            "reason": reason
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/Suspend",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to suspend workflow: {str(e)}",
                context=workflow_context
            )
    
    def resume(
        self,
        serial_number: str,
        part_number: str,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Resume suspended workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating resume result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/Resume",
                workflow_context,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to resume workflow: {str(e)}",
                context=workflow_context
            )
    
    def cancel(
        self,
        serial_number: str,
        part_number: str,
        reason: Optional[str] = None,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Cancel active workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            serial_number: Unit serial number
            part_number: Unit part number
            reason: Cancellation reason
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating cancellation result
            
        Raises:
            WATSAPIException: On API errors
        """
        workflow_context = WorkflowContext(
            serial_number=serial_number,
            part_number=part_number,
            station_name=station_name,
            operator=operator,
            context_data=context or {}
        )
        
        data = {
            "context": workflow_context.dict(by_alias=True),
            "reason": reason
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/Cancel",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to cancel workflow: {str(e)}",
                context=workflow_context
            )
    
    def add_unit(
        self,
        parent_serial_number: str,
        parent_part_number: str,
        child_serial_number: str,
        child_part_number: str,
        operation: Optional[str] = None,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Add unit in box build workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            parent_serial_number: Parent unit serial number
            parent_part_number: Parent unit part number
            child_serial_number: Child unit serial number
            child_part_number: Child unit part number
            operation: Optional operation name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating add unit result
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "parentSerialNumber": parent_serial_number,
            "parentPartNumber": parent_part_number,
            "childSerialNumber": child_serial_number,
            "childPartNumber": child_part_number,
            "operation": operation,
            "stationName": station_name,
            "operator": operator,
            "context": context or {}
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/AddUnit",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to add unit: {str(e)}"
            )
    
    def remove_unit(
        self,
        parent_serial_number: str,
        parent_part_number: str,
        child_serial_number: str,
        child_part_number: str,
        operation: Optional[str] = None,
        station_name: Optional[str] = None,
        operator: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> WorkflowResult:
        """
        Remove sub unit from box build workflow.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            parent_serial_number: Parent unit serial number
            parent_part_number: Parent unit part number
            child_serial_number: Child unit serial number
            child_part_number: Child unit part number
            operation: Optional operation name
            station_name: Station name
            operator: Operator name
            context: Additional context data
            
        Returns:
            WorkflowResult indicating remove unit result
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "parentSerialNumber": parent_serial_number,
            "parentPartNumber": parent_part_number,
            "childSerialNumber": child_serial_number,
            "childPartNumber": child_part_number,
            "operation": operation,
            "stationName": station_name,
            "operator": operator,
            "context": context or {}
        }
        
        try:
            response = self._rest_post_json(
                "/api/internal/Workflow/RemoveUnit",
                data,
                response_type=WorkflowResult
            )
            return response
        except Exception as e:
            return WorkflowResult(
                success=False,
                message=f"Failed to remove unit: {str(e)}"
            )