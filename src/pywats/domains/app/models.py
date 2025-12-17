"""App domain models.

Statistics and KPI data models.
"""
from typing import Optional
from pydantic import Field

from ...shared.base_model import PyWATSModel


class YieldData(PyWATSModel):
    """
    Represents yield statistics data.

    Attributes:
        part_number: Product part number
        revision: Product revision
        product_name: Product name
        product_group: Product group
        station_name: Test station name
        test_operation: Test operation
        period: Time period
        unit_count: Total unit count
        fp_count: First pass count
        sp_count: Second pass count
        tp_count: Third pass count
        lp_count: Last pass count
        fpy: First pass yield
        spy: Second pass yield
        tpy: Third pass yield
        lpy: Last pass yield
    """

    part_number: Optional[str] = Field(default=None, alias="partNumber")
    revision: Optional[str] = Field(default=None, alias="revision")
    product_name: Optional[str] = Field(default=None, alias="productName")
    product_group: Optional[str] = Field(default=None, alias="productGroup")
    station_name: Optional[str] = Field(default=None, alias="stationName")
    test_operation: Optional[str] = Field(default=None, alias="testOperation")
    period: Optional[str] = Field(default=None, alias="period")
    unit_count: Optional[int] = Field(default=None, alias="unitCount")
    fp_count: Optional[int] = Field(default=None, alias="fpCount")
    sp_count: Optional[int] = Field(default=None, alias="spCount")
    tp_count: Optional[int] = Field(default=None, alias="tpCount")
    lp_count: Optional[int] = Field(default=None, alias="lpCount")
    fpy: Optional[float] = Field(default=None, alias="fpy")
    spy: Optional[float] = Field(default=None, alias="spy")
    tpy: Optional[float] = Field(default=None, alias="tpy")
    lpy: Optional[float] = Field(default=None, alias="lpy")


class ProcessInfo(PyWATSModel):
    """
    Represents process/test operation information.

    Attributes:
        code: Process code (e.g., 100, 500)
        name: Process name (e.g., "End of line test", "Repair")
        description: Process description
        is_test_operation: True if this is a test operation
        is_repair_operation: True if this is a repair operation
        is_wip_operation: True if this is a WIP operation
        process_index: Process order index
        state: Process state
    """

    code: Optional[int] = Field(default=None, alias="code")
    name: Optional[str] = Field(default=None, alias="name")
    description: Optional[str] = Field(default=None, alias="description")
    is_test_operation: bool = Field(default=False, alias="isTestOperation")
    is_repair_operation: bool = Field(default=False, alias="isRepairOperation")
    is_wip_operation: bool = Field(default=False, alias="isWipOperation")
    process_index: Optional[int] = Field(default=None, alias="processIndex")
    state: Optional[int] = Field(default=None, alias="state")
    
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
        level_id: Level ID
        level_name: Level name
    """

    level_id: Optional[int] = Field(default=None, alias="levelId")
    level_name: Optional[str] = Field(default=None, alias="levelName")


class ProductGroup(PyWATSModel):
    """
    Represents a product group.

    Attributes:
        product_group_id: Product group ID
        product_group_name: Product group name
    """

    product_group_id: Optional[int] = Field(
        default=None, alias="productGroupId"
    )
    product_group_name: Optional[str] = Field(
        default=None, alias="productGroupName"
    )


class StepAnalysisRow(PyWATSModel):
    """Represents a single step (and optional measurement) KPI row.

    Returned from POST /api/App/TestStepAnalysis.
    The API is in preview and the schema may change.
    """

    step_name: Optional[str] = Field(default=None, alias="stepName")
    step_path: Optional[str] = Field(default=None, alias="stepPath")
    step_type: Optional[str] = Field(default=None, alias="stepType")
    step_group: Optional[str] = Field(default=None, alias="stepGroup")

    step_count: Optional[int] = Field(default=None, alias="stepCount")
    step_passed_count: Optional[int] = Field(default=None, alias="stepPassedCount")
    step_done_count: Optional[int] = Field(default=None, alias="stepDoneCount")
    step_skipped_count: Optional[int] = Field(default=None, alias="stepSkippedCount")
    step_failed_count: Optional[int] = Field(default=None, alias="stepFailedCount")
    step_error_count: Optional[int] = Field(default=None, alias="stepErrorCount")
    step_terminated_count: Optional[int] = Field(default=None, alias="stepTerminatedCount")
    step_other_count: Optional[int] = Field(default=None, alias="stepOtherCount")

    step_failed_error_terminated_count: Optional[int] = Field(
        default=None, alias="stepFailedErrorTerminatedCount"
    )
    step_caused_uut_failed_error_terminated: Optional[int] = Field(
        default=None, alias="stepCausedUutFailedErrorTerminated"
    )
    step_caused_uut_failed: Optional[int] = Field(
        default=None, alias="stepCausedUutFailed"
    )
    step_caused_uut_error: Optional[int] = Field(
        default=None, alias="stepCausedUutError"
    )
    step_caused_uut_terminated: Optional[int] = Field(
        default=None, alias="stepCausedUutTerminated"
    )

    limit1: Optional[float] = Field(default=None, alias="limit1")
    limit1_wof: Optional[float] = Field(default=None, alias="limit1Wof")
    limit2: Optional[float] = Field(default=None, alias="limit2")
    limit2_wof: Optional[float] = Field(default=None, alias="limit2Wof")
    comp_operator: Optional[str] = Field(default=None, alias="compOperator")

    step_time_avg: Optional[float] = Field(default=None, alias="stepTimeAvg")
    step_time_max: Optional[float] = Field(default=None, alias="stepTimeMax")
    step_time_min: Optional[float] = Field(default=None, alias="stepTimeMin")

    measure_name: Optional[str] = Field(default=None, alias="measureName")
    measure_count: Optional[int] = Field(default=None, alias="measureCount")
    measure_count_wof: Optional[int] = Field(default=None, alias="measureCountWof")

    min: Optional[float] = Field(default=None, alias="min")
    min_wof: Optional[float] = Field(default=None, alias="minWof")
    max: Optional[float] = Field(default=None, alias="max")
    max_wof: Optional[float] = Field(default=None, alias="maxWof")
    avg: Optional[float] = Field(default=None, alias="avg")
    avg_wof: Optional[float] = Field(default=None, alias="avgWof")
    stdev: Optional[float] = Field(default=None, alias="stdev")
    stdev_wof: Optional[float] = Field(default=None, alias="stdevWof")
    var: Optional[float] = Field(default=None, alias="var")
    var_wof: Optional[float] = Field(default=None, alias="varWof")

    cpk: Optional[float] = Field(default=None, alias="cpk")
    cpk_wof: Optional[float] = Field(default=None, alias="cpkWof")
    cp: Optional[float] = Field(default=None, alias="cp")
    cp_wof: Optional[float] = Field(default=None, alias="cpWof")
    cp_lower: Optional[float] = Field(default=None, alias="cpLower")
    cp_lower_wof: Optional[float] = Field(default=None, alias="cpLowerWof")
    cp_upper: Optional[float] = Field(default=None, alias="cpUpper")
    cp_upper_wof: Optional[float] = Field(default=None, alias="cpUpperWof")

    sigma_high_3: Optional[float] = Field(default=None, alias="sigmaHigh3")
    sigma_high_3_wof: Optional[float] = Field(default=None, alias="sigmaHigh3Wof")
    sigma_low_3: Optional[float] = Field(default=None, alias="sigmaLow3")
    sigma_low_3_wof: Optional[float] = Field(default=None, alias="sigmaLow3Wof")
