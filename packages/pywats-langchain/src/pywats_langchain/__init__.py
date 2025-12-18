"""
pyWATS LangChain - LangChain integration for pyWATS.

Provides native LangChain tools, agents, and chains for
interacting with WATS manufacturing data.

Example:
    >>> from pywats import pyWATS
    >>> from pywats_langchain import WATSToolkit, create_wats_agent
    >>> 
    >>> api = pyWATS(base_url="...", token="...")
    >>> 
    >>> # Use individual tools
    >>> toolkit = WATSToolkit(api)
    >>> tools = toolkit.get_tools()
    >>> 
    >>> # Or create a pre-configured agent
    >>> agent = create_wats_agent(api, model_name="gpt-4")
    >>> result = agent.invoke({"input": "What's the yield for WIDGET-001?"})
"""

from .tools import (
    WATSYieldTool, 
    WATSToolkit, 
    LANGCHAIN_AVAILABLE,
    WATSTestStepAnalysisTool,
    WATSAggregatedMeasurementTool,
    WATSMeasurementDataTool,
)
from .chains import create_wats_agent, WATSAnalyticsChain

__version__ = "0.1.0"
__all__ = [
    # Tools
    "WATSYieldTool",
    "WATSTestStepAnalysisTool",
    "WATSAggregatedMeasurementTool",
    "WATSMeasurementDataTool",
    "WATSToolkit",
    # Chains and agents
    "create_wats_agent",
    "WATSAnalyticsChain",
    # Utils
    "LANGCHAIN_AVAILABLE",
]
