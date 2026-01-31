"""
UUTReport - v3 Implementation

Complete UUT test report with UUT-specific features.
"""
from __future__ import annotations

from typing import Optional, List, Literal

from ..report import Report
from ..sub_unit import SubUnit
from ..common_types import Field, ReportType
from .uut_info import UUTInfo
from .step import Step
from .steps import SequenceCall, StepList, StepType


class UUTSubUnit(SubUnit):
    """
    UUT Sub-unit with its own test steps.
    
    Represents a sub-assembly or component of the main UUT
    that has its own serial number and test results.
    
    C# Name: UutSubUnit
    """
    
    # Sub-unit test steps
    root: Optional[SequenceCall] = Field(
        default=None,
        description="Root sequence containing sub-unit test steps."
    )


class UUTReport(Report[UUTSubUnit]):
    """
    Complete UUT (Unit Under Test) report.
    
    This is the main report class for hardware/software testing.
    Contains:
        - UUT identification (part number, serial number, etc.)
        - Test hierarchy (SequenceCall with nested steps)
        - Sub-units (tested components)
        - Assets (test equipment)
        - Binary data and attachments
    
    C# Name: UutReport
    
    Example:
        report = UUTReport(
            pn="WIDGET-001",
            sn="SN123456",
            operation="FinalTest",
            result="P"
        )
        
        # Add root sequence
        root = SequenceCall(name="MainSequence")
        root.add_numeric_step("Voltage", value=5.0, comp=CompOp.GELE, limit_l=4.5, limit_h=5.5)
        report.root = root
        
        # Submit
        await client.submit_report(report)
    """
    
    # ========================================================================
    # UUT Info - Required by server, serializes as "uut"
    # ========================================================================
    
    info: Optional[UUTInfo] = Field(
        default=None,
        validation_alias="uut",
        serialization_alias="uut",
        description="UUT-specific information (serializes as 'uut')."
    )
    
    # ========================================================================
    # Test Steps
    # ========================================================================
    
    # Root sequence - contains all test steps
    root: SequenceCall = Field(
        default_factory=SequenceCall,
        description="Root sequence containing all test steps."
    )
    
    # ========================================================================
    # Factory Methods
    # ========================================================================
    
    def get_root_sequence_call(self) -> SequenceCall:
        """
        Get or create the root sequence call.
        
        Returns:
            The root SequenceCall (use its factory methods to add steps).
        """
        self.root.name = "MainSequence Callback"
        return self.root
    
    # ========================================================================
    # Sub-Unit Management
    # ========================================================================
    
    def add_sub_unit(self, part_type: str, sn: str, pn: str, rev: str) -> UUTSubUnit:
        """
        Add a UUT sub-unit.
        
        Args:
            part_type: Part type
            sn: Serial number
            pn: Part number
            rev: Revision
            
        Returns:
            The created UUTSubUnit.
        """
        sub_unit = UUTSubUnit(
            part_type=part_type,
            sn=sn,
            pn=pn,
            rev=rev,
        )
        if self.sub_units is None:
            self.sub_units = []
        self.sub_units.append(sub_unit)
        return sub_unit
    

