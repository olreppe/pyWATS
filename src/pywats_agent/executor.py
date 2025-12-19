"""
Tool executor that bridges agent calls to pyWATS API.

This is the main entry point for executing agent tool calls.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .result import AgentResult
from .context import AgentContext
from .tools import (
    YieldAnalysisTool,
    get_yield_tool_definition,
    TestStepAnalysisTool,
    get_test_step_analysis_tool_definition,
    AggregatedMeasurementTool,
    MeasurementDataTool,
    get_aggregated_measurement_tool_definition,
    get_measurement_data_tool_definition,
)

if TYPE_CHECKING:
    from pywats import pyWATS


class ToolExecutor:
    """
    Executes agent tool calls against the pyWATS API.
    
    This class bridges LLM tool calls to actual pyWATS API operations,
    returning structured results with human-readable summaries.
    
    Example:
        >>> from pywats import pyWATS
        >>> from pywats_agent import ToolExecutor
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
        "Yield analysis for product WIDGET-001 grouped by station (last 7 days):
        • Average FPY: 94.5%
        • Total units: 1,234
        • Data points: 5
        • Best: Station-A (98.2%)
        • Worst: Station-E (89.1%)"
    """
    
    def __init__(
        self, 
        api: "pyWATS",
        context: Optional[AgentContext] = None
    ):
        """
        Initialize the executor with a pyWATS instance.
        
        Args:
            api: Configured pyWATS API instance
            context: Optional context from frontend (current product, station, etc.)
        """
        self._api = api
        self._context = context
        
        # Initialize tools
        self._yield_tool = YieldAnalysisTool(api)
        self._test_step_analysis_tool = TestStepAnalysisTool(api)
        self._aggregated_measurement_tool = AggregatedMeasurementTool(api)
        self._measurement_data_tool = MeasurementDataTool(api)
        
        # Tool registry
        self._tools: Dict[str, Any] = {
            "analyze_yield": self._yield_tool,
            "analyze_test_steps": self._test_step_analysis_tool,
            "get_measurement_statistics": self._aggregated_measurement_tool,
            "get_measurement_data": self._measurement_data_tool,
        }
    
    def list_tools(self) -> List[str]:
        """
        List available tool names.
        
        Returns:
            List of tool names that can be executed
        """
        return list(self._tools.keys())
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """
        Get all tool definitions for agent frameworks.
        
        Returns:
            List of tool definition dictionaries
        """
        return [
            get_yield_tool_definition(),
            get_test_step_analysis_tool_definition(),
            get_aggregated_measurement_tool_definition(),
            get_measurement_data_tool_definition(),
        ]
    
    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """
        Get tool schemas in OpenAI function calling format.
        
        Returns:
            List of OpenAI-compatible tool schemas
        """
        return [
            {
                "type": "function",
                "function": tool_def
            }
            for tool_def in self.get_tool_definitions()
        ]
    
    @property
    def context(self) -> Optional[AgentContext]:
        """Get the current context."""
        return self._context
    
    @context.setter
    def context(self, value: Optional[AgentContext]) -> None:
        """Set the context."""
        self._context = value
    
    def get_system_prompt(self) -> str:
        """
        Get system prompt text including context.
        
        Use this to build the system prompt for the LLM.
        
        Returns:
            System prompt text with context information
        """
        base_prompt = """You are a manufacturing data analyst assistant.
You help users analyze test data, yield metrics, and measurements.
Use the available tools to retrieve and analyze data."""
        
        if self._context:
            context_text = self._context.to_system_prompt()
            return f"{base_prompt}\n\n{context_text}"
        
        return base_prompt
    
    def _apply_context_defaults(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply context defaults to parameters where not explicitly set.
        
        Args:
            parameters: Tool parameters from the user/LLM
            
        Returns:
            Parameters with context defaults applied
        """
        if not self._context:
            return parameters
        
        defaults = self._context.get_default_parameters()
        result = parameters.copy()
        
        for key, value in defaults.items():
            if key not in result or result[key] is None:
                result[key] = value
        
        return result
    
    def execute(
        self, 
        tool_name: str, 
        parameters: Dict[str, Any],
        apply_context: bool = True
    ) -> AgentResult:
        """
        Execute a tool with the given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters as a dictionary
            apply_context: If True, apply context defaults to missing parameters
            
        Returns:
            AgentResult with data and human-readable summary
            
        Example:
            >>> result = executor.execute("analyze_yield", {
            ...     "part_number": "WIDGET-001",
            ...     "perspective": "by station"
            ... })
            >>> print(result.success)
            True
            >>> print(result.summary)
            "Yield analysis for product WIDGET-001..."
        """
        # Apply context defaults if enabled
        if apply_context:
            parameters = self._apply_context_defaults(parameters)
        
        if tool_name not in self._tools:
            available = ", ".join(self.list_tools())
            return AgentResult.fail(
                f"Unknown tool: {tool_name}. Available tools: {available}"
            )
        
        try:
            tool = self._tools[tool_name]
            
            # Route to appropriate handler
            if tool_name == "analyze_yield":
                return tool.analyze_from_dict(parameters)
            elif tool_name == "analyze_test_steps":
                return tool.analyze_from_dict(parameters)
            elif tool_name == "get_measurement_statistics":
                return tool.analyze_from_dict(parameters)
            elif tool_name == "get_measurement_data":
                return tool.analyze_from_dict(parameters)
            else:
                return AgentResult.fail(f"Tool {tool_name} has no handler")
                
        except Exception as e:
            return AgentResult.fail(f"Error executing {tool_name}: {str(e)}")
    
    def execute_openai_tool_call(self, tool_call: Any) -> AgentResult:
        """
        Execute an OpenAI tool call object directly.
        
        Args:
            tool_call: OpenAI ChatCompletionMessageToolCall object
            
        Returns:
            AgentResult with data and summary
            
        Example:
            >>> # After getting response from OpenAI
            >>> tool_call = response.choices[0].message.tool_calls[0]
            >>> result = executor.execute_openai_tool_call(tool_call)
        """
        import json
        
        tool_name = tool_call.function.name
        parameters = json.loads(tool_call.function.arguments)
        
        return self.execute(tool_name, parameters)
    
    # =========================================================================
    # Convenience methods for direct tool access
    # =========================================================================
    
    @property
    def yield_tool(self) -> YieldAnalysisTool:
        """Get the yield analysis tool directly."""
        return self._yield_tool
    
    @property
    def test_step_analysis_tool(self) -> TestStepAnalysisTool:
        """Get the test step analysis tool directly."""
        return self._test_step_analysis_tool
    
    @property
    def aggregated_measurement_tool(self) -> AggregatedMeasurementTool:
        """Get the aggregated measurement tool directly."""
        return self._aggregated_measurement_tool
    
    @property
    def measurement_data_tool(self) -> MeasurementDataTool:
        """Get the measurement data tool directly."""
        return self._measurement_data_tool
    
    def analyze_yield(
        self,
        part_number: Optional[str] = None,
        station_name: Optional[str] = None,
        perspective: Optional[str] = None,
        days: int = 30,
        **kwargs
    ) -> AgentResult:
        """
        Convenience method to analyze yield directly.
        
        Args:
            part_number: Filter by product
            station_name: Filter by station
            perspective: How to group data (e.g., "by station", "trend")
            days: Number of days to analyze
            **kwargs: Additional filter parameters
            
        Returns:
            AgentResult with yield data
        """
        params = {
            "part_number": part_number,
            "station_name": station_name,
            "perspective": perspective,
            "days": days,
            **kwargs
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        
        return self.execute("analyze_yield", params)
