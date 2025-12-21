from __future__ import annotations

from .registry import ToolProfile, ToolRegistry
from .tools import (
    AnalyzeYieldToolV2,
    AnalyzeTestStepsToolV2,
    AnalyzeFailureModesToolV2,
    AnalyzeProcessCapabilityToolV2,
    AnalyzeRootCauseToolV2,
    AnalyzeSubUnitsToolV2,
    AnalyzeUnitToolV2,
    ControlPanelToolV2,
    GetMeasurementDataToolV2,
    GetMeasurementStatisticsToolV2,
)


DEFAULT_TOOL_CLASSES = (
    AnalyzeYieldToolV2,
    AnalyzeTestStepsToolV2,
    AnalyzeRootCauseToolV2,
    AnalyzeFailureModesToolV2,
    AnalyzeProcessCapabilityToolV2,
    GetMeasurementStatisticsToolV2,
    GetMeasurementDataToolV2,
    AnalyzeUnitToolV2,
    AnalyzeSubUnitsToolV2,
    ControlPanelToolV2,
)


def build_default_registry() -> ToolRegistry:
    reg = ToolRegistry()
    reg.register_many(DEFAULT_TOOL_CLASSES)
    return reg


PROFILES: dict[str, ToolProfile] = {
    "minimal": ToolProfile(name="minimal", enabled_tools=("analyze_yield",)),
    "analysis": ToolProfile(
        name="analysis",
        enabled_tools=(
            "analyze_yield",
            "analyze_test_steps",
            "analyze_root_cause",
            "analyze_failure_modes",
        ),
    ),
    "measurement": ToolProfile(
        name="measurement",
        enabled_tools=(
            "get_measurement_statistics",
            "get_measurement_data",
            "analyze_process_capability",
        ),
    ),
    "full": ToolProfile(
        name="full",
        enabled_tools=(
            "analyze_yield",
            "analyze_test_steps",
            "analyze_root_cause",
            "analyze_failure_modes",
            "analyze_process_capability",
            "get_measurement_statistics",
            "get_measurement_data",
            "analyze_unit",
            "analyze_subunits",
            "control_panel",
        ),
    ),
}


def get_profile(name: str) -> ToolProfile:
    return PROFILES[name]
