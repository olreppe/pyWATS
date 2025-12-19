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

from .yield_tool import (
    YieldAnalysisTool,
    YieldFilter,
    AnalysisPerspective,
    PERSPECTIVE_ALIASES,
    resolve_perspective,
    get_yield_tool_definition,
)
from .test_step_analysis_tool import (
    TestStepAnalysisTool,
    TestStepAnalysisFilter,
    get_test_step_analysis_tool_definition,
)
from .step_analysis import (
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
from .process_capability import (
    ProcessCapabilityTool,
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
from .measurement_tool import (
    AggregatedMeasurementTool,
    MeasurementDataTool,
    MeasurementFilter,
    get_aggregated_measurement_tool_definition,
    get_measurement_data_tool_definition,
)
from .dimensional_analysis import (
    DimensionalAnalysisTool,
    DimensionYieldResult,
    FailureModeResult,
    FailureModeFilter,
    SignificanceLevel,
    STANDARD_DIMENSIONS,
    get_dimensional_analysis_tool_definition,
)
from .root_cause_analysis import (
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
)
from .adaptive_time import (
    AdaptiveTimeFilter,
    AdaptiveTimeConfig,
    AdaptiveTimeResult,
    VolumeCategory,
)
from .process_resolver import (
    ProcessResolver,
    PROCESS_ALIASES,
    diagnose_mixed_process_problem,
)

__all__ = [
    # Yield tool
    "YieldAnalysisTool",
    "YieldFilter",
    "AnalysisPerspective",
    "PERSPECTIVE_ALIASES",
    "resolve_perspective",
    "get_yield_tool_definition",
    # Dimensional analysis (failure modes)
    "DimensionalAnalysisTool",
    "DimensionYieldResult",
    "FailureModeResult",
    "FailureModeFilter",
    "SignificanceLevel",
    "STANDARD_DIMENSIONS",
    "get_dimensional_analysis_tool_definition",
    # Step analysis (TSA) - comprehensive
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
    # Process Capability Analysis (advanced)
    "ProcessCapabilityTool",
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
    # Test step analysis tool (basic)
    "TestStepAnalysisTool",
    "TestStepAnalysisFilter",
    "get_test_step_analysis_tool_definition",
    # Measurement tools
    "AggregatedMeasurementTool",
    "MeasurementDataTool",
    "MeasurementFilter",
    "get_aggregated_measurement_tool_definition",
    "get_measurement_data_tool_definition",
    # Root Cause Analysis (top-down, trend-aware)
    "RootCauseAnalysisTool",
    "RootCauseInput",
    "RootCauseResult",
    "YieldAssessmentResult",
    "SuspectFinding",
    "TrendAnalysis",
    "TrendPattern",
    "YieldAssessment",
    "InvestigationPriority",
    # Step 6-9 classes
    "StepTrendPattern",
    "FailingStepFinding",
    "TrendQualifiedStep",
    "ContextualComparison",
    "ExplainableFinding",
    "get_root_cause_analysis_tool_definition",
    # Adaptive time filter
    "AdaptiveTimeFilter",
    "AdaptiveTimeConfig",
    "AdaptiveTimeResult",
    "VolumeCategory",
    # Process resolver
    "ProcessResolver",
    "PROCESS_ALIASES",
    "diagnose_mixed_process_problem",
]
