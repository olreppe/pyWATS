"""
TDM (Test Data Management) module for pyWATS.

⚠️ DEPRECATED: This module is deprecated and will be removed in a future version.
Use WATSApi.report and WATSApi.app instead:

- TDM.create_uut_report() → WATSApi.report.create_uut_report()
- TDM.create_uur_report() → WATSApi.report.create_uur_report()
- TDM.submit() → WATSApi.report.submit_report()
- TDM.setup_api() → WATSApi.app.configure_system()

This module provides backward compatibility by delegating to the new modules.
"""

from typing import Optional, Dict, Any, List, Union
import warnings
import datetime
from uuid import uuid4

from .modules.base import BaseModule
from .exceptions import WATSException, WATSNotFoundError
from .models.report import UUTReport, UURReport, Report


class TDM(BaseModule):
    """
    Test Data Management module.
    
    ⚠️ DEPRECATED: This class is deprecated. Use WATSApi.report and WATSApi.app instead.
    
    This class provides backward compatibility by delegating to the new modules.
    """
    
    def __init__(self, client):
        """
        Initialize the TDM module.
        
        ⚠️ DEPRECATED: Use WATSApi instead.
        """
        warnings.warn(
            "TDM class is deprecated. Use WATSApi.report and WATSApi.app instead.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(client)
        
        # Initialize the new modules for delegation
        from .modules.report import ReportModule
        from .modules.app import AppModule
        self._report_module = ReportModule(client)
        self._app_module = AppModule(client)

    def setup_api(self, data_dir: str, location: str, purpose: str) -> None:
        """
        Set up the TDM API with directory and context information.
        
        ⚠️ DEPRECATED: Use WATSApi.app.configure_system() instead.
        
        Args:
            data_dir: Directory for storing report data
            location: Testing location identifier
            purpose: Purpose of the testing
        """
        warnings.warn(
            "TDM.setup_api() is deprecated. Use WATSApi.app.configure_system() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._app_module.configure_system(data_dir, location, purpose)

    def create_uut_report(
        self, 
        operator: str, 
        part_number: str, 
        revision: str, 
        serial_number: str,
        operation_type: str, 
        sequence_file: str, 
        version: str
    ) -> UUTReport:
        """
        Create a new UUT (Unit Under Test) report.
        
        ⚠️ DEPRECATED: Use WATSApi.report.create_uut_report() instead.
        
        Args:
            operator: Name of the test operator
            part_number: Part number of the unit being tested
            revision: Revision of the unit
            serial_number: Serial number of the unit
            operation_type: Type of operation being performed
            sequence_file: Test sequence file name
            version: Version of the test sequence
            
        Returns:
            A new UUTReport object
        """
        warnings.warn(
            "TDM.create_uut_report() is deprecated. Use WATSApi.report.create_uut_report() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Get configuration from app module
        config = self._app_module.get_configuration()
        
        return self._report_module.create_uut_report(
            operator=operator,
            part_number=part_number,
            revision=revision,
            serial_number=serial_number,
            operation_type=operation_type,
            sequence_file=sequence_file,
            version=version,
            station_name=config.get("location"),
            location=config.get("location"),
            purpose=config.get("purpose")
        )
    
    def create_uur_report(
        self,
        operator: str,
        repair_type: str,
        operation_type: str,
        serial_number: str,
        part_number: str,
        revision: str
    ) -> UURReport:
        """
        Create a new UUR (Unit Under Repair) report.
        
        ⚠️ DEPRECATED: Use WATSApi.report.create_uur_report() instead.
        
        Args:
            operator: Name of the repair operator
            repair_type: Type of repair being performed
            operation_type: Type of operation
            serial_number: Serial number of the unit
            part_number: Part number of the unit
            revision: Revision of the unit
            
        Returns:
            A new UURReport object
        """
        warnings.warn(
            "TDM.create_uur_report() is deprecated. Use WATSApi.report.create_uur_report() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        
        # Get configuration from app module
        config = self._app_module.get_configuration()
        
        return self._report_module.create_uur_report(
            operator=operator,
            repair_type=repair_type,
            operation_type=operation_type,
            serial_number=serial_number,
            part_number=part_number,
            revision=revision,
            station_name=config.get("location"),
            location=config.get("location"),
            purpose=config.get("purpose")
        )
    
    def submit(self, report: Union[UUTReport, UURReport]) -> str:
        """
        Submit a report to WATS.
        
        ⚠️ DEPRECATED: Use WATSApi.report.submit_report() instead.
        
        Args:
            report: The report to submit
            
        Returns:
            Report ID from WATS
        """
        warnings.warn(
            "TDM.submit() is deprecated. Use WATSApi.report.submit_report() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.submit_report(report)
    
    def submit_pending_reports(self) -> List[str]:
        """
        Submit all pending reports.
        
        ⚠️ DEPRECATED: Use WATSApi.report.submit_pending_reports() instead.
        
        Returns:
            List of report IDs that were submitted
        """
        warnings.warn(
            "TDM.submit_pending_reports() is deprecated. Use WATSApi.report.submit_pending_reports() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.submit_pending_reports()
    
    def load_report(self, report_id: str) -> Union[UUTReport, UURReport]:
        """
        Load a report from WATS by ID.
        
        ⚠️ DEPRECATED: Use WATSApi.report.load_report() instead.
        
        Args:
            report_id: The ID of the report to load
            
        Returns:
            The loaded report
            
        Raises:
            WATSNotFoundError: If the report is not found
        """
        warnings.warn(
            "TDM.load_report() is deprecated. Use WATSApi.report.load_report() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.load_report(report_id)
    
    def get_operation_types(self) -> List[Dict[str, Any]]:
        """
        Get all available operation types.
        
        ⚠️ DEPRECATED: Use WATSApi.report.get_operation_types() instead.
        
        Returns:
            List of operation types
        """
        warnings.warn(
            "TDM.get_operation_types() is deprecated. Use WATSApi.report.get_operation_types() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.get_operation_types()
    
    def get_operation_type(self, id_or_name: Union[str, int]) -> Dict[str, Any]:
        """
        Get a specific operation type by ID or name.
        
        ⚠️ DEPRECATED: Use WATSApi.report.get_operation_type() instead.
        
        Args:
            id_or_name: Operation type ID or name
            
        Returns:
            Operation type details
            
        Raises:
            WATSNotFoundError: If the operation type is not found
        """
        warnings.warn(
            "TDM.get_operation_type() is deprecated. Use WATSApi.report.get_operation_type() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.get_operation_type(id_or_name)
    
    def get_repair_types(self) -> List[Dict[str, Any]]:
        """
        Get all available repair types.
        
        ⚠️ DEPRECATED: Use WATSApi.report.get_repair_types() instead.
        
        Returns:
            List of repair types
        """
        warnings.warn(
            "TDM.get_repair_types() is deprecated. Use WATSApi.report.get_repair_types() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.get_repair_types()
    
    def get_root_fail_codes(self, repair_type: Union[str, int]) -> List[Dict[str, Any]]:
        """
        Get root failure codes for a repair type.
        
        ⚠️ DEPRECATED: Use WATSApi.report.get_root_fail_codes() instead.
        
        Args:
            repair_type: Repair type ID or name
            
        Returns:
            List of failure codes
        """
        warnings.warn(
            "TDM.get_root_fail_codes() is deprecated. Use WATSApi.report.get_root_fail_codes() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.get_root_fail_codes(repair_type)

    def get_yield_monitor_statistics(self, 
                                   start_date: Optional[datetime.datetime] = None,
                                   end_date: Optional[datetime.datetime] = None) -> Dict[str, Any]:
        """
        Get yield monitoring statistics.
        
        ⚠️ DEPRECATED: Use WATSApi.report.get_yield_monitor_statistics() instead.
        
        Args:
            start_date: Start date for statistics
            end_date: End date for statistics
            
        Returns:
            Yield statistics
        """
        warnings.warn(
            "TDM.get_yield_monitor_statistics() is deprecated. Use WATSApi.report.get_yield_monitor_statistics() instead.",
            DeprecationWarning,
            stacklevel=2
        )
        return self._report_module.get_yield_monitor_statistics(start_date, end_date)