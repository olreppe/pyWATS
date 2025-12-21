from __future__ import annotations

from typing import Any

from ...result import AgentResult
from ..tooling import AgentToolV2

# Import legacy input models + tool implementations (to be wrapped into v2)
from ...tools.yield_pkg import YieldAnalysisTool, YieldFilter
from ...tools.step import TestStepAnalysisTool, TestStepAnalysisFilter
from ...tools.measurement import (
    AggregatedMeasurementTool,
    MeasurementDataTool,
    MeasurementFilter,
)
from ...tools.unit import UnitAnalysisInput, UnitAnalysisTool
from ...tools.subunit.subunit_tool import SubUnitAnalysisInput, SubUnitAnalysisTool
from ...tools.control_panel import ControlPanelInput, ControlPanelTool
from ...tools.root_cause import (
    FailureModeFilter,
    RootCauseInput,
)
from ...tools.root_cause import DimensionalAnalysisTool as _FailureModesTool
from ...tools.root_cause import RootCauseAnalysisTool as _RootCauseTool
from ...tools.capability import ProcessCapabilityInput, ProcessCapabilityTool


def _convert_v1_result(result: AgentResult) -> tuple[bool, str, Any, dict[str, Any]]:
    if result.success:
        return True, result.summary, result.data, dict(result.metadata or {})

    metadata: dict[str, Any] = dict(result.metadata or {})
    if result.error:
        metadata["error"] = result.error
    return False, result.summary, None, metadata


class AnalyzeYieldToolV2(AgentToolV2[YieldFilter]):
    """V2 wrapper around the existing YieldAnalysisTool."""

    name = "analyze_yield"
    description = "Analyze yield using the existing yield tool (wrapped into v2 envelope + data handles)."
    input_model = YieldFilter

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = YieldAnalysisTool(api)

    def run(self, input_obj: YieldFilter):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class AnalyzeTestStepsToolV2(AgentToolV2[TestStepAnalysisFilter]):
    """V2 wrapper around the existing TestStepAnalysisTool."""

    name = "analyze_test_steps"
    description = "Analyze step-level statistics (wrapped into v2 envelope + data handles)."
    input_model = TestStepAnalysisFilter

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = TestStepAnalysisTool(api)

    def run(self, input_obj: TestStepAnalysisFilter):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class GetMeasurementStatisticsToolV2(AgentToolV2[MeasurementFilter]):
    """V2 wrapper around the existing AggregatedMeasurementTool."""

    name = "get_measurement_statistics"
    description = "Get aggregated measurement statistics (wrapped into v2 envelope + data handles)."
    input_model = MeasurementFilter

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = AggregatedMeasurementTool(api)

    def run(self, input_obj: MeasurementFilter):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class GetMeasurementDataToolV2(AgentToolV2[MeasurementFilter]):
    """V2 wrapper around the existing MeasurementDataTool."""

    name = "get_measurement_data"
    description = "Get individual measurement datapoints (wrapped into v2 envelope + data handles)."
    input_model = MeasurementFilter

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = MeasurementDataTool(api)

    def run(self, input_obj: MeasurementFilter):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class AnalyzeUnitToolV2(AgentToolV2[UnitAnalysisInput]):
    """V2 wrapper around the existing UnitAnalysisTool."""

    name = "analyze_unit"
    description = "Analyze a single unit (wrapped into v2 envelope + data handles)."
    input_model = UnitAnalysisInput

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = UnitAnalysisTool(api)

    def run(self, input_obj: UnitAnalysisInput):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class AnalyzeSubUnitsToolV2(AgentToolV2[SubUnitAnalysisInput]):
    """V2 wrapper around the existing SubUnitAnalysisTool."""

    name = "analyze_subunits"
    description = "Analyze sub-unit (component) relationships (wrapped into v2 envelope + data handles)."
    input_model = SubUnitAnalysisInput

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = SubUnitAnalysisTool(api)

    def run(self, input_obj: SubUnitAnalysisInput):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class ControlPanelToolV2(AgentToolV2[ControlPanelInput]):
    """V2 wrapper around the existing ControlPanelTool."""

    name = "control_panel"
    description = "Administrative WATS management operations (wrapped into v2 envelope + data handles)."
    input_model = ControlPanelInput

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = ControlPanelTool(api)

    def run(self, input_obj: ControlPanelInput):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class AnalyzeProcessCapabilityToolV2(AgentToolV2[ProcessCapabilityInput]):
    """V2 wrapper around the existing ProcessCapabilityTool."""

    name = "analyze_process_capability"
    description = "Advanced capability analysis (stability, dual Cpk) wrapped into v2 envelope + data handles."
    input_model = ProcessCapabilityInput

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = ProcessCapabilityTool(api)

    def run(self, input_obj: ProcessCapabilityInput):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class AnalyzeRootCauseToolV2(AgentToolV2[RootCauseInput]):
    """V2 wrapper around the existing RootCauseAnalysisTool."""

    name = "analyze_root_cause"
    description = "Top-down root cause investigation (wrapped into v2 envelope + data handles)."
    input_model = RootCauseInput

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = _RootCauseTool(api)

    def run(self, input_obj: RootCauseInput):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)


class AnalyzeFailureModesToolV2(AgentToolV2[FailureModeFilter]):
    """V2 wrapper around the existing DimensionalAnalysisTool (failure modes)."""

    name = "analyze_failure_modes"
    description = "Dimensional yield splitting to detect failure modes (wrapped into v2 envelope + data handles)."
    input_model = FailureModeFilter

    def __init__(self, api: Any):
        super().__init__(api)
        self._tool = _FailureModesTool(api)

    def run(self, input_obj: FailureModeFilter):
        result = self._tool.analyze(input_obj)
        return _convert_v1_result(result)
