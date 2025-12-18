"""
pyWATS Agent - AI agent tools for pyWATS.

Provides tool definitions and executors for AI agents (LangChain, OpenAI, etc.)
to interact with WATS manufacturing data.

Example:
    >>> from pywats import pyWATS
    >>> from pywats_agent import ToolExecutor, YieldAnalysisTool
    >>> 
    >>> api = pyWATS(base_url="...", token="...")
    >>> executor = ToolExecutor(api)
    >>> 
    >>> # Execute a tool call from an LLM
    >>> result = executor.execute("analyze_yield", {
    ...     "part_number": "WIDGET-001",
    ...     "perspective": "by station",
    ...     "days": 7
    ... })
    >>> print(result.summary)
"""

from .result import AgentResult
from .executor import ToolExecutor
from .tools import (
    YieldAnalysisTool,
    YieldFilter,
    AnalysisPerspective,
    PERSPECTIVE_ALIASES,
    resolve_perspective,
    get_yield_tool_definition,
    TestStepAnalysisTool,
    TestStepAnalysisFilter,
    get_test_step_analysis_tool_definition,
    AggregatedMeasurementTool,
    MeasurementDataTool,
    MeasurementFilter,
    get_aggregated_measurement_tool_definition,
    get_measurement_data_tool_definition,
)

__version__ = "0.1.0"
__all__ = [
    # Core
    "AgentResult",
    "ToolExecutor",
    # Yield tool
    "YieldAnalysisTool",
    "YieldFilter",
    "AnalysisPerspective",
    "PERSPECTIVE_ALIASES",
    "resolve_perspective",
    "get_yield_tool_definition",
    # Test step analysis tool
    "TestStepAnalysisTool",
    "TestStepAnalysisFilter",
    "get_test_step_analysis_tool_definition",
    # Measurement tools
    "AggregatedMeasurementTool",
    "MeasurementDataTool",
    "MeasurementFilter",
    "get_aggregated_measurement_tool_definition",
    "get_measurement_data_tool_definition",
]
