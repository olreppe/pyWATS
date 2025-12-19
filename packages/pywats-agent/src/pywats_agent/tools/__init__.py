"""
Agent tools for pyWATS.

Smart tools that translate semantic concepts to WATS API calls.

ANALYSIS WORKFLOW:
1. YieldAnalysisTool - Top-level yield by product/process
2. RootCauseAnalysisTool - Top-down, trend-aware failure investigation (9 steps)
3. DimensionalAnalysisTool - Find which factors affect yield (failure modes)
4. StepAnalysisTool - Comprehensive step analysis (Cpk, root cause)
5. ProcessCapabilityTool - Advanced capability analysis (stability, dual Cpk)
6. MeasurementDataTool - Analyze measurement distributions and raw data

TOP-DOWN ROOT CAUSE ANALYSIS (9-Step Methodology):
┌─────────────────────────────────────────────────────────────────────────────────┐
│ CORE PRINCIPLE: Start at yield level. Test steps are SYMPTOMS.                  │
│ Only dive into step-level analysis when yield deviations justify it.            │
└─────────────────────────────────────────────────────────────────────────────────┘

Step 1: PRODUCT-LEVEL YIELD ASSESSMENT
    - Evaluate overall yield against expected thresholds
    - If yield is healthy → STOP (no problem to investigate)
    - Poor/degrading yield → triggers root cause analysis

Step 2: DIMENSIONAL YIELD SPLITTING
    - Split yield using UUT header dimensions (station, fixture, operator, etc.)
    - Build yield matrix to find statistically significant deviations
    - Identify "suspects" - configurations with lower-than-expected yield

Step 3: TEMPORAL TREND ANALYSIS
    - Include time trends (day-over-day, week-over-week)
    - Classify issues: EMERGING | CHRONIC | RECOVERING | INTERMITTENT
    - Classification impacts prioritization (emerging > chronic)

Step 4: TREND-AWARE SUSPECT PRIORITIZATION
    - Rank by: absolute impact, peer deviation, trend direction, variability
    - Prioritize EMERGING/DEGRADING over stable known problems

Step 5: STEP-LEVEL INVESTIGATION (Only if warranted)
    - Drill into test steps ONLY for high-priority suspects
    - Focus on steps that CAUSE unit failures

Step 6: IDENTIFICATION OF TOP FAILING STEPS
    - Identify steps using failure contribution metrics (step_caused_uut_failed)
    - Only highest-impact steps proceed for detailed analysis

Step 7: TREND-QUALIFIED STEP ANALYSIS
    - Classify step failure patterns: INCREASING | DECREASING | STABLE | VARIABLE
    - Separate regressions from noise using trend analysis

Step 8: CONTEXTUAL ANALYSIS BASED ON SUSPECTS
    - Compare step failure rates: suspect context vs non-suspect context
    - Compare vs historical baseline to confirm causality

Step 9: EXPLAINABLE PRIORITIZED FINDINGS
    - Each finding traces: yield → suspect → step → trend
    - Includes evidence chain, confidence score, recommendations
    - Supports efficient, high-confidence corrective actions

LEGACY ANALYSIS PATH:
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Yield       │ --> │ Dimensional  │ --> │ Step        │ --> │ Process      │ --> │ Measurement │
│ Analysis    │     │ Analysis     │     │ Analysis    │     │ Capability   │     │ Deep Dive   │
│             │     │ (optional)   │     │ (TSA)       │     │ Analysis     │     │             │
└─────────────┘     └──────────────┘     └─────────────┘     └──────────────┘     └─────────────┘
     |                    |                    |                    |                    |
"What's failing?"   "Where/when?"      "Which step?"     "Is it stable?"      "Why exactly?"
                                                          "Cpk vs Cpk_wof?"
                                                          "Hidden modes?"

PROCESS CAPABILITY WORKFLOW:
┌─────────────────────────────────────────────────────────────────────────────────┐
│ 1. DATA INTEGRITY CHECK                                                         │
│    - Verify single product/process configuration                                │
│    - Check SW version consistency                                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 2. STABILITY ASSESSMENT (MUST DO FIRST!)                                        │
│    - Is process under statistical control?                                      │
│    - Detect trends, shifts, outliers                                           │
│    - If NOT stable → Cpk is meaningless!                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 3. DUAL CpK ANALYSIS                                                            │
│    - Cpk (all): Actual capability including failures                           │
│    - Cpk_wof: Potential without failures                                       │
│    - Compare: Cpk << Cpk_wof means failures hurt capability                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 4. HIDDEN MODE DETECTION                                                        │
│    - Outliers beyond 3σ                                                        │
│    - Trends (drift up/down)                                                    │
│    - Approaching specification limits                                          │
│    - Centering issues (Cp >> Cpk)                                              │
│    - Bimodal distributions                                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 5. IMPROVEMENT RECOMMENDATIONS                                                  │
│    - Prioritized: Critical → High → Medium → Low                               │
│    - Specific actions based on findings                                        │
└─────────────────────────────────────────────────────────────────────────────────┘
"""

# =============================================================================
# BACKWARD COMPATIBLE IMPORTS FROM SUBPACKAGES
# =============================================================================
# These imports provide backward compatibility with the old flat structure.
# New code should import directly from the subpackages.
# =============================================================================

# Yield tools (yield_pkg because 'yield' is a Python keyword)
from .yield_pkg import (
    YieldAnalysisTool,
    YieldFilter,
    AnalysisPerspective,
    PERSPECTIVE_ALIASES,
    resolve_perspective,
    get_yield_tool_definition,
)

# Step analysis tools
from .step import (
    TestStepAnalysisTool,
    TestStepAnalysisFilter,
    get_test_step_analysis_tool_definition,
    StepAnalysisTool,
    StepAnalysisInput,
    StepSummary,
    TSAResult,
    OverallProcessSummary,
    DataIntegrityResult,
    CpkStatus,
    CPK_CAPABLE_THRESHOLD,
    CPK_MARGINAL_THRESHOLD,
    CPK_CRITICAL_THRESHOLD,
    get_step_analysis_tool_definition,
)

# Process capability tools
from .capability import (
    ProcessCapabilityTool,
    ProcessCapabilityFilter,
    ProcessCapabilityInput,
    ProcessCapabilityResult,
    MeasurementCapabilityResult,
    DualCpkAnalysis,
    StabilityAnalysis,
    HiddenMode,
    StabilityStatus,
    CapabilityStatus,
    ImprovementPriority,
    HiddenModeType,
    CPK_CAPABLE,
    CPK_MARGINAL,
    CPK_CRITICAL,
    CPK_EXCELLENT,
    get_process_capability_tool_definition,
)

# Measurement tools
from .measurement import (
    AggregatedMeasurementTool,
    MeasurementDataTool,
    MeasurementFilter,
    get_aggregated_measurement_tool_definition,
    get_measurement_data_tool_definition,
)

# Root cause analysis tools
from .root_cause import (
    RootCauseAnalysisTool,
    RootCauseInput,
    RootCauseResult,
    YieldAssessmentResult,
    SuspectFinding,
    TrendAnalysis,
    TrendPattern,
    YieldAssessment,
    InvestigationPriority,
    # Step 6-9 classes
    StepTrendPattern,
    FailingStepFinding,
    TrendQualifiedStep,
    ContextualComparison,
    ExplainableFinding,
    get_root_cause_analysis_tool_definition,
    # Dimensional analysis
    DimensionalAnalysisTool,
    DimensionYieldResult,
    FailureModeResult,
    FailureModeFilter,
    SignificanceLevel,
    STANDARD_DIMENSIONS,
    get_dimensional_analysis_tool_definition,
)

# Legacy aliases for backward compatibility
RootCauseAnalysisFilter = RootCauseInput
RootCauseAnalysisResult = RootCauseResult
DimensionalAnalysisFilter = FailureModeFilter

# Shared utilities
from .shared import (
    AdaptiveTimeFilter,
    AdaptiveTimeConfig,
    AdaptiveTimeResult,
    VolumeCategory,
    ProcessResolver,
    PROCESS_ALIASES,
    diagnose_mixed_process_problem,
)

# Asset analysis tools
from .asset import (
    # Tools
    AssetDimensionTool,
    AssetHealthTool,
    AssetDegradationTool,
    # Tool definitions
    get_asset_dimension_tool_definition,
    get_asset_health_tool_definition,
    get_asset_degradation_tool_definition,
    # Enums
    AssetHealthStatus,
    CalibrationStatus,
    AssetImpactLevel,
    DegradationTrend,
    # Filter models
    AssetDimensionFilter,
    AssetHealthFilter,
    AssetDegradationFilter,
    # Result models
    AssetYieldImpact,
    AssetHealthInfo,
    CalibrationCycleMetrics,
    AssetDegradationAnalysis,
    AssetDimensionResult,
    AssetHealthResult,
)

# Base infrastructure (new)
from ._base import (
    ToolInput,
    AgentTool,
    AnalysisTool,
)
from ._registry import (
    register_tool,
    get_all_tools,
    get_tools_by_category,
    create_tool_instance,
)

__all__ = [
    # Base infrastructure
    "ToolInput",
    "AgentTool",
    "AnalysisTool",
    "register_tool",
    "get_all_tools",
    "get_tools_by_category",
    "create_tool_instance",
    
    # Yield tools
    "YieldAnalysisTool",
    "YieldFilter",
    "AnalysisPerspective",
    "PERSPECTIVE_ALIASES",
    "resolve_perspective",
    "get_yield_tool_definition",
    
    # Step analysis
    "StepAnalysisTool",
    "StepAnalysisInput",
    "StepSummary",
    "TSAResult",
    "OverallProcessSummary",
    "DataIntegrityResult",
    "CpkStatus",
    "CPK_CAPABLE_THRESHOLD",
    "CPK_MARGINAL_THRESHOLD",
    "CPK_CRITICAL_THRESHOLD",
    "get_step_analysis_tool_definition",
    "TestStepAnalysisTool",
    "TestStepAnalysisFilter",
    "get_test_step_analysis_tool_definition",
    
    # Process capability
    "ProcessCapabilityTool",
    "ProcessCapabilityFilter",
    "ProcessCapabilityInput",
    "ProcessCapabilityResult",
    "MeasurementCapabilityResult",
    "DualCpkAnalysis",
    "StabilityAnalysis",
    "HiddenMode",
    "StabilityStatus",
    "CapabilityStatus",
    "ImprovementPriority",
    "HiddenModeType",
    "CPK_CAPABLE",
    "CPK_MARGINAL",
    "CPK_CRITICAL",
    "CPK_EXCELLENT",
    "get_process_capability_tool_definition",
    
    # Measurement tools
    "AggregatedMeasurementTool",
    "MeasurementDataTool",
    "MeasurementFilter",
    "get_aggregated_measurement_tool_definition",
    "get_measurement_data_tool_definition",
    
    # Root cause analysis
    "RootCauseAnalysisTool",
    "RootCauseInput",
    "RootCauseAnalysisFilter",
    "RootCauseResult",
    "RootCauseAnalysisResult",
    "YieldAssessmentResult",
    "SuspectFinding",
    "TrendAnalysis",
    "TrendPattern",
    "YieldAssessment",
    "InvestigationPriority",
    "StepTrendPattern",
    "FailingStepFinding",
    "TrendQualifiedStep",
    "ContextualComparison",
    "ExplainableFinding",
    "get_root_cause_analysis_tool_definition",
    
    # Dimensional analysis
    "DimensionalAnalysisTool",
    "DimensionYieldResult",
    "FailureModeResult",
    "FailureModeFilter",
    "DimensionalAnalysisFilter",
    "SignificanceLevel",
    "STANDARD_DIMENSIONS",
    "get_dimensional_analysis_tool_definition",
    
    # Shared utilities
    "AdaptiveTimeFilter",
    "AdaptiveTimeConfig",
    "AdaptiveTimeResult",
    "VolumeCategory",
    "ProcessResolver",
    "PROCESS_ALIASES",
    "diagnose_mixed_process_problem",
    
    # Asset analysis tools
    "AssetDimensionTool",
    "AssetHealthTool",
    "AssetDegradationTool",
    "get_asset_dimension_tool_definition",
    "get_asset_health_tool_definition",
    "get_asset_degradation_tool_definition",
    # Asset enums
    "AssetHealthStatus",
    "CalibrationStatus",
    "AssetImpactLevel",
    "DegradationTrend",
    # Asset filters
    "AssetDimensionFilter",
    "AssetHealthFilter",
    "AssetDegradationFilter",
    # Asset results
    "AssetYieldImpact",
    "AssetHealthInfo",
    "CalibrationCycleMetrics",
    "AssetDegradationAnalysis",
    "AssetDimensionResult",
    "AssetHealthResult",
]
