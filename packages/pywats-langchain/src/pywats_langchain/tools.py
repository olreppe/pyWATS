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

from pywats_agent import (
    YieldAnalysisTool, 
    YieldFilter,
    TestStepAnalysisTool,
    TestStepAnalysisFilter,
    AggregatedMeasurementTool,
    MeasurementDataTool,
    MeasurementFilter,
)

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
    
    class WATSTestStepAnalysisTool(BaseTool):
        """
        LangChain tool for analyzing test step statistics.
        
        This tool provides detailed step-level execution statistics
        and failure analysis for manufacturing tests.
        
        Example:
            >>> from pywats import pyWATS
            >>> from pywats_langchain import WATSTestStepAnalysisTool
            >>> 
            >>> api = pyWATS(base_url="...", token="...")
            >>> tool = WATSTestStepAnalysisTool(api=api)
            >>> 
            >>> # Use with an agent
            >>> result = tool.invoke({
            ...     "part_number": "WIDGET-001",
            ...     "test_operation": "FCT"
            ... })
        """
        
        name: str = "analyze_test_steps"
        description: str = """
Analyze test step execution statistics and failure patterns.

Use this tool to answer questions like:
- "Which test steps are failing for WIDGET-001?" 
- "What are the failure rates for each step in FCT?"
- "Show me step-level statistics for product X"

Provides detailed execution statistics for each test step.
"""
        
        # Define input schema inline
        class TestStepAnalysisInput(BaseModel):
            """Input schema for test step analysis."""
            part_number: str = Field(description="Product part number (required)")
            test_operation: str = Field(description="Test operation (required, e.g., 'FCT', 'EOL')")
            revision: Optional[str] = Field(default=None, description="Product revision")
            days: int = Field(default=30, description="Number of days to analyze")
            run: int = Field(default=1, description="Run number to analyze")
            max_count: int = Field(default=10000, description="Maximum results")
        
        args_schema: Type[BaseModel] = TestStepAnalysisInput
        
        # Custom attributes
        api: Any = None
        _tool: TestStepAnalysisTool = None
        
        def __init__(self, api: "pyWATS", **kwargs):
            """Initialize the tool."""
            super().__init__(api=api, **kwargs)
            self._tool = TestStepAnalysisTool(api)
        
        def _run(
            self,
            part_number: str,
            test_operation: str,
            revision: Optional[str] = None,
            days: int = 30,
            run: int = 1,
            max_count: int = 10000,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            """Execute the test step analysis."""
            
            filter_input = TestStepAnalysisFilter(
                part_number=part_number,
                test_operation=test_operation,
                revision=revision,
                days=days,
                run=run,
                max_count=max_count,
            )
            
            result = self._tool.analyze(filter_input)
            
            if result.success:
                return result.summary
            else:
                return f"Error: {result.error}"
        
        async def _arun(self, *args, **kwargs) -> str:
            """Async version."""
            return self._run(*args, **kwargs)
    
    class WATSAggregatedMeasurementTool(BaseTool):
        """
        LangChain tool for analyzing aggregated measurement statistics.
        
        Provides statistical analysis of measurement data including
        process capability metrics.
        
        Example:
            >>> from pywats import pyWATS
            >>> from pywats_langchain import WATSAggregatedMeasurementTool
            >>> 
            >>> api = pyWATS(base_url="...", token="...")
            >>> tool = WATSAggregatedMeasurementTool(api=api)
            >>> 
            >>> result = tool.invoke({
            ...     "measurement_path": "Main/Voltage Test/Output Voltage",
            ...     "part_number": "WIDGET-001"
            ... })
        """
        
        name: str = "get_measurement_statistics"
        description: str = """
Get aggregated measurement statistics and process capability metrics.

Use this tool to answer questions like:
- "What's the average output voltage for WIDGET-001?"
- "Show me Cpk for voltage measurements"
- "What are the min/max values for temperature?"

Provides aggregate statistics including min, max, avg, Cpk, etc.
"""
        
        class AggregatedMeasurementInput(BaseModel):
            """Input schema for aggregated measurements."""
            measurement_path: str = Field(description="Path to measurement (required)")
            part_number: Optional[str] = Field(default=None, description="Product part number")
            revision: Optional[str] = Field(default=None, description="Product revision")
            station_name: Optional[str] = Field(default=None, description="Test station")
            days: int = Field(default=30, description="Number of days to analyze")
            grouping: Optional[str] = Field(default=None, description="Group results by dimension")
        
        args_schema: Type[BaseModel] = AggregatedMeasurementInput
        
        api: Any = None
        _tool: AggregatedMeasurementTool = None
        
        def __init__(self, api: "pyWATS", **kwargs):
            """Initialize the tool."""
            super().__init__(api=api, **kwargs)
            self._tool = AggregatedMeasurementTool(api)
        
        def _run(
            self,
            measurement_path: str,
            part_number: Optional[str] = None,
            revision: Optional[str] = None,
            station_name: Optional[str] = None,
            days: int = 30,
            grouping: Optional[str] = None,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            """Execute the aggregated measurement analysis."""
            
            filter_input = MeasurementFilter(
                measurement_path=measurement_path,
                part_number=part_number,
                revision=revision,
                station_name=station_name,
                days=days,
                grouping=grouping,
            )
            
            result = self._tool.analyze(filter_input)
            
            if result.success:
                return result.summary
            else:
                return f"Error: {result.error}"
        
        async def _arun(self, *args, **kwargs) -> str:
            """Async version."""
            return self._run(*args, **kwargs)
    
    class WATSMeasurementDataTool(BaseTool):
        """
        LangChain tool for retrieving individual measurement data points.
        
        Provides access to raw measurement values with timestamps
        and serial numbers.
        
        Example:
            >>> from pywats import pyWATS
            >>> from pywats_langchain import WATSMeasurementDataTool
            >>> 
            >>> api = pyWATS(base_url="...", token="...")
            >>> tool = WATSMeasurementDataTool(api=api)
            >>> 
            >>> result = tool.invoke({
            ...     "measurement_path": "Main/Voltage Test/Output Voltage",
            ...     "part_number": "WIDGET-001",
            ...     "top_count": 100
            ... })
        """
        
        name: str = "get_measurement_data"
        description: str = """
Get individual measurement data points with timestamps and serial numbers.

Use this tool to answer questions like:
- "Show me the last 100 voltage measurements"
- "What were the actual values for serial number X?"
- "Get raw measurement data for temperature"

Provides individual data points with serial numbers, values, and timestamps.
"""
        
        class MeasurementDataInput(BaseModel):
            """Input schema for measurement data."""
            measurement_path: str = Field(description="Path to measurement (required)")
            part_number: Optional[str] = Field(default=None, description="Product part number")
            revision: Optional[str] = Field(default=None, description="Product revision")
            serial_number: Optional[str] = Field(default=None, description="Unit serial number")
            station_name: Optional[str] = Field(default=None, description="Test station")
            days: int = Field(default=30, description="Number of days")
            top_count: Optional[int] = Field(default=1000, description="Limit data points")
        
        args_schema: Type[BaseModel] = MeasurementDataInput
        
        api: Any = None
        _tool: MeasurementDataTool = None
        
        def __init__(self, api: "pyWATS", **kwargs):
            """Initialize the tool."""
            super().__init__(api=api, **kwargs)
            self._tool = MeasurementDataTool(api)
        
        def _run(
            self,
            measurement_path: str,
            part_number: Optional[str] = None,
            revision: Optional[str] = None,
            serial_number: Optional[str] = None,
            station_name: Optional[str] = None,
            days: int = 30,
            top_count: Optional[int] = 1000,
            run_manager: Optional[CallbackManagerForToolRun] = None,
        ) -> str:
            """Execute the measurement data retrieval."""
            
            filter_input = MeasurementFilter(
                measurement_path=measurement_path,
                part_number=part_number,
                revision=revision,
                serial_number=serial_number,
                station_name=station_name,
                days=days,
                top_count=top_count,
            )
            
            result = self._tool.analyze(filter_input)
            
            if result.success:
                return result.summary
            else:
                return f"Error: {result.error}"
        
        async def _arun(self, *args, **kwargs) -> str:
            """Async version."""
            return self._run(*args, **kwargs)

else:
    # Stub classes when LangChain is not installed
    class WATSYieldTool:
        """Stub - LangChain not installed."""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain is required for WATSYieldTool. "
                "Install with: pip install pywats-langchain[langchain]"
            )
    
    class WATSTestStepAnalysisTool:
        """Stub - LangChain not installed."""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain is required for WATSTestStepAnalysisTool. "
                "Install with: pip install pywats-langchain[langchain]"
            )
    
    class WATSAggregatedMeasurementTool:
        """Stub - LangChain not installed."""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain is required for WATSAggregatedMeasurementTool. "
                "Install with: pip install pywats-langchain[langchain]"
            )
    
    class WATSMeasurementDataTool:
        """Stub - LangChain not installed."""
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "LangChain is required for WATSMeasurementDataTool. "
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
                WATSTestStepAnalysisTool(api=api),
                WATSAggregatedMeasurementTool(api=api),
                WATSMeasurementDataTool(api=api),
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
        for tool in self._tools:
            if isinstance(tool, WATSYieldTool):
                return tool
        return None
    
    @property
    def test_step_analysis_tool(self) -> "WATSTestStepAnalysisTool":
        """Get the test step analysis tool."""
        for tool in self._tools:
            if isinstance(tool, WATSTestStepAnalysisTool):
                return tool
        return None
    
    @property
    def aggregated_measurement_tool(self) -> "WATSAggregatedMeasurementTool":
        """Get the aggregated measurement tool."""
        for tool in self._tools:
            if isinstance(tool, WATSAggregatedMeasurementTool):
                return tool
        return None
    
    @property
    def measurement_data_tool(self) -> "WATSMeasurementDataTool":
        """Get the measurement data tool."""
        for tool in self._tools:
            if isinstance(tool, WATSMeasurementDataTool):
                return tool
        return None
