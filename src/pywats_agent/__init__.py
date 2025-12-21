"""pyWATS Agent (BETA).

Public API policy (BETA): **no backwards compatibility**.

Use the v2 executor + result envelope (data handles + bounded previews).

Example:
    >>> from pywats import pyWATS
    >>> from pywats_agent import ToolExecutorV2, InMemoryDataStore
    >>>
    >>> api = pyWATS(base_url="...", token="...")
    >>> executor = ToolExecutorV2.with_default_tools(api, datastore=InMemoryDataStore())
    >>>
    >>> env = executor.execute("analyze_yield", {"part_number": "WIDGET-001"})
    >>> print(env.summary)
"""
from .visualization import (
    ChartType,
    DataSeries,
    ReferenceLine,
    Annotation,
    ChartPayload,
    TableColumn,
    TablePayload,
    KPIPayload,
    DrillDownOption,
    VisualizationPayload,
    VizBuilder,
    merge_visualizations,
    empty_visualization,
)

# Clean-sheet agent core (v2): registry/profiles + datastore handles + LLM-safe envelopes
from .agent import (
    AgentToolV2,
    DataStore,
    InMemoryDataStore,
    build_default_registry,
    get_profile,
    ResponsePolicy,
    ToolExecutorV2,
    ToolProfile,
    ToolRegistry,
    ToolResultEnvelope,
    ToolInput,
)

__version__ = "0.1.0b17"
__all__ = [
    # Clean-sheet agent core (v2)
    "AgentToolV2",
    "DataStore",
    "InMemoryDataStore",
    "build_default_registry",
    "get_profile",
    "ResponsePolicy",
    "ToolExecutorV2",
    "ToolProfile",
    "ToolRegistry",
    "ToolResultEnvelope",
    "ToolInput",
    # Visualization (sidecar pattern)
    "ChartType",
    "DataSeries",
    "ReferenceLine",
    "Annotation",
    "ChartPayload",
    "TableColumn",
    "TablePayload",
    "KPIPayload",
    "DrillDownOption",
    "VisualizationPayload",
    "VizBuilder",
    "merge_visualizations",
    "empty_visualization",
]
