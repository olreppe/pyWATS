"""
LangChain tools for pyWATS.

Native LangChain tool implementations that wrap the pyWATS agent tools.
"""

from typing import Any, Dict, List, Optional, Type, TYPE_CHECKING
from pydantic import BaseModel, Field

try:
    from langchain_core.tools import BaseTool
    from langchain_core.callbacks import CallbackManagerForToolRun
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    BaseTool = object
    CallbackManagerForToolRun = None

from pywats_agent import YieldAnalysisTool, YieldFilter

if TYPE_CHECKING:
    from pywats import pyWATS


class YieldAnalysisInput(BaseModel):
    """Input schema for the yield analysis tool."""
    
    perspective: Optional[str] = Field(
        default=None,
        description="""
How to group/analyze the data. Natural language options:
- Time: "trend", "daily", "weekly", "monthly"
- Equipment: "by station", "by fixture", "by line"
- Product: "by product", "by revision", "by product group"
- Process: "by operation", "by process"
- Other: "by operator", "by batch", "by level"
- Combined: "station trend", "product trend"
Leave empty for overall aggregated yield.
        """.strip()
    )
    part_number: Optional[str] = Field(
        default=None,
        description="Filter by product part number (e.g., 'WIDGET-001')"
    )
    revision: Optional[str] = Field(
        default=None,
        description="Filter by product revision"
    )
    station_name: Optional[str] = Field(
        default=None,
        description="Filter by test station name"
    )
    product_group: Optional[str] = Field(
        default=None,
        description="Filter by product group"
    )
    level: Optional[str] = Field(
        default=None,
        description="Filter by production level (PCBA, Box Build)"
    )
    test_operation: Optional[str] = Field(
        default=None,
        description="Filter by test operation (FCT, EOL)"
    )
    process_code: Optional[str] = Field(
        default=None,
        description="Filter by process code"
    )
    batch_number: Optional[str] = Field(
        default=None,
        description="Filter by production batch"
    )
    operator: Optional[str] = Field(
        default=None,
        description="Filter by operator name"
    )
    location: Optional[str] = Field(
        default=None,
        description="Filter by location/production line"
    )
    days: int = Field(
        default=30,
        description="Number of days to analyze (default: 30)"
    )


if LANGCHAIN_AVAILABLE:
    class WATSYieldTool(BaseTool):
        """
        LangChain tool for analyzing manufacturing yield data.
        
        This tool provides intelligent yield analysis with semantic
        perspective mapping. Use natural language to specify how
        you want to group and analyze the data.
        
        Example:
            >>> from pywats import pyWATS
            >>> from pywats_langchain import WATSYieldTool
            >>> 
            >>> api = pyWATS(base_url="...", token="...")
            >>> tool = WATSYieldTool(api=api)
            >>> 
            >>> # Use with an agent
            >>> result = tool.invoke({
            ...     "part_number": "WIDGET-001",
            ...     "perspective": "by station"
            ... })
        """
        
        name: str = "analyze_yield"
        description: str = """
Analyze manufacturing yield/quality data with flexible grouping.

Use this tool to answer questions like:
- "What's the yield for WIDGET-001?" (overall yield)
- "How is yield trending over time?" (perspective: "trend")
- "Compare yield by station" (perspective: "by station")
- "Which product has the worst yield?" (perspective: "by product")
- "Show daily yield for the past week" (perspective: "daily", days: 7)

The 'perspective' parameter determines how data is grouped.
Use natural language: "by station", "trend", "daily", "by product", etc.

Available perspectives:
- Time: trend, daily, weekly, monthly
- Equipment: by station, by fixture, by line
- Product: by product, by revision, by product group
- Process: by operation, by process
- Other: by operator, by batch, by level
- Combined: station trend, product trend
"""
        args_schema: Type[BaseModel] = YieldAnalysisInput
        
        # Custom attributes
        api: Any = None
        _tool: YieldAnalysisTool = None
        
        def __init__(self, api: "pyWATS", **kwargs):
            """
            Initialize the yield tool.
            
            Args:
                api: Configured pyWATS instance
            """
            super().__init__(api=api, **kwargs)
            self._tool = YieldAnalysisTool(api)
        
        def _run(
            self,
            perspective: Optional[str] = None,
            part_number: Optional[str] = None,
            revision: Optional[str] = None,
            station_name: Optional[str] = None,
            product_group: Optional[str] = None,
            level: Optional[str] = None,
            test_operation: Optional[str] = None,
            process_code: Optional[str] = None,
            batch_number: Optional[str] = None,
            operator: Optional[str] = None,
            location: Optional[str] = None,
            days: int = 30,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            """Execute the yield analysis."""
            
            filter_input = YieldFilter(
                perspective=perspective,
                part_number=part_number,
                revision=revision,
                station_name=station_name,
                product_group=product_group,
                level=level,
                test_operation=test_operation,
                process_code=process_code,
                batch_number=batch_number,
                operator=operator,
                location=location,
                days=days,
            )
            
            result = self._tool.analyze(filter_input)
            
            # Return summary for LLM consumption
            if result.success:
                return result.summary
            else:
                return f"Error: {result.error}"
        
        async def _arun(self, *args, **kwargs) -> str:
            """Async version - just calls sync for now."""
            return self._run(*args, **kwargs)
else:
    # Stub class when LangChain is not installed
    class WATSYieldTool:
        """Stub - LangChain not installed."""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain is required for WATSYieldTool. "
                "Install with: pip install pywats-langchain[langchain]"
            )


class WATSToolkit:
    """
    Complete toolkit of WATS tools for LangChain agents.
    
    Provides all available WATS tools in a single package.
    
    Example:
        >>> from pywats import pyWATS
        >>> from pywats_langchain import WATSToolkit
        >>> from langchain.agents import create_react_agent
        >>> 
        >>> api = pyWATS(base_url="...", token="...")
        >>> toolkit = WATSToolkit(api)
        >>> 
        >>> # Get tools for agent
        >>> tools = toolkit.get_tools()
        >>> agent = create_react_agent(llm, tools, prompt)
    """
    
    def __init__(self, api: "pyWATS"):
        """
        Initialize the toolkit.
        
        Args:
            api: Configured pyWATS instance
        """
        self._api = api
        self._tools: List[Any] = []
        
        if LANGCHAIN_AVAILABLE:
            self._tools = [
                WATSYieldTool(api=api),
                # Add more tools here as they're implemented
            ]
    
    def get_tools(self) -> List[Any]:
        """
        Get all available tools.
        
        Returns:
            List of LangChain tools
        """
        return self._tools
    
    @property
    def yield_tool(self) -> "WATSYieldTool":
        """Get the yield analysis tool."""
        return self._tools[0] if self._tools else None
