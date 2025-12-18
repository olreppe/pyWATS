"""App domain models.

Statistics and KPI data models.

FIELD NAMING CONVENTION:
------------------------
All fields use Python snake_case naming (e.g., part_number, station_name).
Backend API aliases (camelCase) are handled automatically.
Always use the Python field names when creating or accessing these models.
"""
from typing import Optional
from pydantic import Field, AliasChoices

from ...shared.base_model import PyWATSModel


class YieldData(PyWATSModel):
    """
    Represents yield statistics data.

    Attributes:
        part_number: Product part number (use this, not 'partNumber')
        revision: Product revision
        product_name: Product name (use this, not 'productName')
        product_group: Product group (use this, not 'productGroup')
        station_name: Test station name (use this, not 'stationName')
        test_operation: Test operation (use this, not 'testOperation')
        period: Time period
        unit_count: Total unit count (use this, not 'unitCount')
        fp_count: First pass count (use this, not 'fpCount')
        sp_count: Second pass count
        tp_count: Third pass count
        lp_count: Last pass count
        fpy: First pass yield
        spy: Second pass yield
        tpy: Third pass yield
        lpy: Last pass yield
        
    Example:
        >>> yield_data = YieldData(part_number="WIDGET-001", station_name="Station1")
        >>> print(yield_data.part_number)  # Access with Python field name
    """

    part_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("partNumber", "part_number"),
        serialization_alias="partNumber",
        description="Product part number"
    )
    revision: Optional[str] = Field(default=None, description="Product revision")
    product_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("productName", "product_name"),
        serialization_alias="productName",
        description="Product name"
    )
    product_group: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("productGroup", "product_group"),
        serialization_alias="productGroup",
        description="Product group"
    )
    station_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stationName", "station_name"),
        serialization_alias="stationName",
        description="Test station name"
    )
    test_operation: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("testOperation", "test_operation"),
        serialization_alias="testOperation",
        description="Test operation"
    )
    period: Optional[str] = Field(default=None, description="Time period")
    unit_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("unitCount", "unit_count"),
        serialization_alias="unitCount",
        description="Total unit count"
    )
    fp_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("fpCount", "fp_count"),
        serialization_alias="fpCount",
        description="First pass count"
    )
    sp_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("spCount", "sp_count"),
        serialization_alias="spCount",
        description="Second pass count"
    )
    tp_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("tpCount", "tp_count"),
        serialization_alias="tpCount",
        description="Third pass count"
    )
    lp_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("lpCount", "lp_count"),
        serialization_alias="lpCount",
        description="Last pass count"
    )
    fpy: Optional[float] = Field(default=None, description="First pass yield")
    spy: Optional[float] = Field(default=None, description="Second pass yield")
    tpy: Optional[float] = Field(default=None, description="Third pass yield")
    lpy: Optional[float] = Field(default=None, description="Last pass yield")
class ProcessInfo(PyWATSModel):
    """
    Represents process/test operation information.

    Attributes:
        code: Process code (e.g., 100, 500)
        name: Process name (e.g., "End of line test", "Repair")
        description: Process description
        is_test_operation: True if this is a test operation (use this, not 'isTestOperation')
        is_repair_operation: True if this is a repair operation (use this, not 'isRepairOperation')
        is_wip_operation: True if this is a WIP operation (use this, not 'isWipOperation')
        process_index: Process order index (use this, not 'processIndex')
        state: Process state
        
    Example:
        >>> process = ProcessInfo(code=100, name="EOL Test", is_test_operation=True)
        >>> print(process.is_test_operation)  # Access with Python field name
    """

    code: Optional[int] = Field(default=None, description="Process code")
    name: Optional[str] = Field(default=None, description="Process name")
    description: Optional[str] = Field(default=None, description="Process description")
    is_test_operation: bool = Field(
        default=False,
        validation_alias=AliasChoices("isTestOperation", "is_test_operation"),
        serialization_alias="isTestOperation",
        description="True if this is a test operation"
    )
    is_repair_operation: bool = Field(
        default=False,
        validation_alias=AliasChoices("isRepairOperation", "is_repair_operation"),
        serialization_alias="isRepairOperation",
        description="True if this is a repair operation"
    )
    is_wip_operation: bool = Field(
        default=False,
        validation_alias=AliasChoices("isWipOperation", "is_wip_operation"),
        serialization_alias="isWipOperation",
        description="True if this is a WIP operation"
    )
    process_index: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("processIndex", "process_index"),
        serialization_alias="processIndex",
        description="Process order index"
    )
    state: Optional[int] = Field(default=None, description="Process state")
    
    # Backward compatibility aliases
    @property
    def process_code(self) -> Optional[int]:
        """Alias for code (backward compatibility)"""
        return self.code
    
    @property
    def process_name(self) -> Optional[str]:
        """Alias for name (backward compatibility)"""
        return self.name
class LevelInfo(PyWATSModel):
    """
    Represents production level information.

    Attributes:
        level_id: Level ID (use this, not 'levelId')
        level_name: Level name (use this, not 'levelName')
        
    Example:
        >>> level = LevelInfo(level_id=1, level_name="PCBA")
        >>> print(level.level_name)  # Access with Python field name
    """

    level_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("levelId", "level_id"),
        serialization_alias="levelId",
        description="Level ID"
    )
    level_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("levelName", "level_name"),
        serialization_alias="levelName",
        description="Level name"
    )


class ProductGroup(PyWATSModel):
    """
    Represents a product group.

    Attributes:
        product_group_id: Product group ID (use this, not 'productGroupId')
        product_group_name: Product group name (use this, not 'productGroupName')
        
    Example:
        >>> group = ProductGroup(product_group_id=1, product_group_name="Electronics")
        >>> print(group.product_group_name)  # Access with Python field name
    """

    product_group_id: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("productGroupId", "product_group_id"),
        serialization_alias="productGroupId",
        description="Product group ID"
    )
    product_group_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("productGroupName", "product_group_name"),
        serialization_alias="productGroupName",
        description="Product group name"
    )


class StepAnalysisRow(PyWATSModel):
    """Represents a single step (and optional measurement) KPI row.

    Returned from POST /api/App/TestStepAnalysis.
    The API is in preview and the schema may change.
    
    IMPORTANT: Use Python field names (snake_case), not camelCase aliases.
    
    Attributes:
        step_name: Name of the test step (use this, not 'stepName')
        step_path: Full path to the step (use this, not 'stepPath')
        step_type: Type of step (use this, not 'stepType')
        step_group: Step group (use this, not 'stepGroup')
        step_count: Total step executions (use this, not 'stepCount')
        ... and many more statistical fields
        
    Example:
        >>> row = StepAnalysisRow(step_name="Voltage Test", step_count=100)
        >>> print(row.step_name)  # Access with Python field name
    """

    step_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stepName", "step_name"),
        serialization_alias="stepName"
    )
    step_path: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stepPath", "step_path"),
        serialization_alias="stepPath"
    )
    step_type: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stepType", "step_type"),
        serialization_alias="stepType"
    )
    step_group: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("stepGroup", "step_group"),
        serialization_alias="stepGroup"
    )

    step_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepCount", "step_count"),
        serialization_alias="stepCount"
    )
    step_passed_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepPassedCount", "step_passed_count"),
        serialization_alias="stepPassedCount"
    )
    step_done_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepDoneCount", "step_done_count"),
        serialization_alias="stepDoneCount"
    )
    step_skipped_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepSkippedCount", "step_skipped_count"),
        serialization_alias="stepSkippedCount"
    )
    step_failed_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepFailedCount", "step_failed_count"),
        serialization_alias="stepFailedCount"
    )
    step_error_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepErrorCount", "step_error_count"),
        serialization_alias="stepErrorCount"
    )
    step_terminated_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepTerminatedCount", "step_terminated_count"),
        serialization_alias="stepTerminatedCount"
    )
    step_other_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepOtherCount", "step_other_count"),
        serialization_alias="stepOtherCount"
    )

    step_failed_error_terminated_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepFailedErrorTerminatedCount", "step_failed_error_terminated_count"),
        serialization_alias="stepFailedErrorTerminatedCount"
    )
    step_caused_uut_failed_error_terminated: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepCausedUutFailedErrorTerminated", "step_caused_uut_failed_error_terminated"),
        serialization_alias="stepCausedUutFailedErrorTerminated"
    )
    step_caused_uut_failed: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepCausedUutFailed", "step_caused_uut_failed"),
        serialization_alias="stepCausedUutFailed"
    )
    step_caused_uut_error: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepCausedUutError", "step_caused_uut_error"),
        serialization_alias="stepCausedUutError"
    )
    step_caused_uut_terminated: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("stepCausedUutTerminated", "step_caused_uut_terminated"),
        serialization_alias="stepCausedUutTerminated"
    )

    limit1: Optional[float] = Field(default=None)
    limit1_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("limit1Wof", "limit1_wof"),
        serialization_alias="limit1Wof"
    )
    limit2: Optional[float] = Field(default=None)
    limit2_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("limit2Wof", "limit2_wof"),
        serialization_alias="limit2Wof"
    )
    comp_operator: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("compOperator", "comp_operator"),
        serialization_alias="compOperator"
    )

    step_time_avg: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("stepTimeAvg", "step_time_avg"),
        serialization_alias="stepTimeAvg"
    )
    step_time_max: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("stepTimeMax", "step_time_max"),
        serialization_alias="stepTimeMax"
    )
    step_time_min: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("stepTimeMin", "step_time_min"),
        serialization_alias="stepTimeMin"
    )

    measure_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("measureName", "measure_name"),
        serialization_alias="measureName"
    )
    measure_count: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("measureCount", "measure_count"),
        serialization_alias="measureCount"
    )
    measure_count_wof: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("measureCountWof", "measure_count_wof"),
        serialization_alias="measureCountWof"
    )

    min: Optional[float] = Field(default=None)
    min_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("minWof", "min_wof"),
        serialization_alias="minWof"
    )
    max: Optional[float] = Field(default=None)
    max_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("maxWof", "max_wof"),
        serialization_alias="maxWof"
    )
    avg: Optional[float] = Field(default=None)
    avg_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("avgWof", "avg_wof"),
        serialization_alias="avgWof"
    )
    stdev: Optional[float] = Field(default=None)
    stdev_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("stdevWof", "stdev_wof"),
        serialization_alias="stdevWof"
    )
    var: Optional[float] = Field(default=None)
    var_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("varWof", "var_wof"),
        serialization_alias="varWof"
    )

    cpk: Optional[float] = Field(default=None)
    cpk_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("cpkWof", "cpk_wof"),
        serialization_alias="cpkWof"
    )
    cp: Optional[float] = Field(default=None)
    cp_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("cpWof", "cp_wof"),
        serialization_alias="cpWof"
    )
    cp_lower: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("cpLower", "cp_lower"),
        serialization_alias="cpLower"
    )
    cp_lower_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("cpLowerWof", "cp_lower_wof"),
        serialization_alias="cpLowerWof"
    )
    cp_upper: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("cpUpper", "cp_upper"),
        serialization_alias="cpUpper"
    )
    cp_upper_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("cpUpperWof", "cp_upper_wof"),
        serialization_alias="cpUpperWof"
    )

    sigma_high_3: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("sigmaHigh3", "sigma_high_3"),
        serialization_alias="sigmaHigh3"
    )
    sigma_high_3_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("sigmaHigh3Wof", "sigma_high_3_wof"),
        serialization_alias="sigmaHigh3Wof"
    )
    sigma_low_3: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("sigmaLow3", "sigma_low_3"),
        serialization_alias="sigmaLow3"
    )
    sigma_low_3_wof: Optional[float] = Field(
        default=None,
        validation_alias=AliasChoices("sigmaLow3Wof", "sigma_low_3_wof"),
        serialization_alias="sigmaLow3Wof"
    )
