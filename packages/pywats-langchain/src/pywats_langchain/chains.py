"""
LangChain chains and agents for pyWATS.

Pre-configured agents and chains for common WATS analysis tasks.
"""

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from .tools import WATSToolkit, LANGCHAIN_AVAILABLE

if TYPE_CHECKING:
    from pywats import pyWATS

if LANGCHAIN_AVAILABLE:
    try:
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_core.messages import SystemMessage
        from langchain.agents import AgentExecutor, create_tool_calling_agent
        AGENTS_AVAILABLE = True
    except ImportError:
        AGENTS_AVAILABLE = False
else:
    AGENTS_AVAILABLE = False


WATS_SYSTEM_PROMPT = """You are a manufacturing analytics assistant with access to WATS (Web-based Automated Test System) data.

You help users analyze:
- Yield and quality metrics (First Pass Yield, Final Yield)
- Test station performance
- Product quality trends
- Failure analysis
- Production efficiency

When analyzing yield data, consider:
1. The perspective (how to group data): by station, by product, over time, etc.
2. The filters: specific products, stations, time periods
3. The context: what insight is the user looking for?

Available perspectives for yield analysis:
- Time-based: "trend", "daily", "weekly", "monthly"
- Equipment: "by station", "by line", "by fixture"
- Product: "by product", "by revision", "by product group"
- Process: "by operation", "by process"
- Other: "by operator", "by batch", "by level"
- Combined: "station trend", "product trend"

Always provide actionable insights based on the data. If yield is low, suggest investigating the worst performers. If there's a trend, highlight it.

Be concise but thorough. Use specific numbers when available."""


def create_wats_agent(
    api: "pyWATS",
    model_name: str = "gpt-4",
    temperature: float = 0.0,
    verbose: bool = False,
) -> "AgentExecutor":
    """
    Create a pre-configured WATS analytics agent.
    
    This creates a ReAct-style agent with all WATS tools and
    a system prompt optimized for manufacturing analytics.
    
    Args:
        api: Configured pyWATS instance
        model_name: OpenAI model to use (default: gpt-4)
        temperature: Model temperature (default: 0.0 for consistency)
        verbose: Whether to print agent steps
        
    Returns:
        LangChain AgentExecutor ready to use
        
    Example:
        >>> from pywats import pyWATS
        >>> from pywats_langchain import create_wats_agent
        >>> 
        >>> api = pyWATS(base_url="...", token="...")
        >>> agent = create_wats_agent(api)
        >>> 
        >>> result = agent.invoke({
        ...     "input": "What's the yield for WIDGET-001 and which station is worst?"
        ... })
        >>> print(result["output"])
    """
    if not LANGCHAIN_AVAILABLE:
        raise ImportError(
            "LangChain is required. Install with: pip install pywats-langchain[langchain]"
        )
    
    if not AGENTS_AVAILABLE:
        raise ImportError(
            "LangChain agents are required. Install with: pip install langchain langchain-openai"
        )
    
    try:
        from langchain_openai import ChatOpenAI
    except ImportError:
        raise ImportError(
            "langchain-openai is required. Install with: pip install langchain-openai"
        )
    
    # Create LLM
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    
    # Get tools
    toolkit = WATSToolkit(api)
    tools = toolkit.get_tools()
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=WATS_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create executor
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        handle_parsing_errors=True,
        max_iterations=10,
    )
    
    return executor


class WATSAnalyticsChain:
    """
    High-level analytics chain for common WATS queries.
    
    Provides pre-built analysis workflows that combine multiple
    tool calls for comprehensive insights.
    
    Example:
        >>> chain = WATSAnalyticsChain(api)
        >>> 
        >>> # Get comprehensive product analysis
        >>> result = chain.analyze_product("WIDGET-001")
        >>> print(result.summary)
    """
    
    def __init__(self, api: "pyWATS"):
        """
        Initialize the analytics chain.
        
        Args:
            api: Configured pyWATS instance
        """
        self._api = api
        self._toolkit = WATSToolkit(api)
    
    def analyze_product(
        self, 
        part_number: str, 
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Comprehensive product analysis.
        
        Analyzes:
        - Overall yield trend
        - Station comparison
        - (Future: Top failures)
        
        Args:
            part_number: Product to analyze
            days: Number of days
            
        Returns:
            Dictionary with analysis results
        """
        yield_tool = self._toolkit.yield_tool
        
        results = {
            "part_number": part_number,
            "days": days,
            "analyses": {}
        }
        
        # Get trend
        from pywats_agent import YieldFilter
        
        trend_result = yield_tool._tool.analyze(YieldFilter(
            part_number=part_number,
            perspective="trend",
            days=days
        ))
        results["analyses"]["trend"] = {
            "summary": trend_result.summary,
            "data": trend_result.data
        }
        
        # Get station comparison
        station_result = yield_tool._tool.analyze(YieldFilter(
            part_number=part_number,
            perspective="by station",
            days=days
        ))
        results["analyses"]["stations"] = {
            "summary": station_result.summary,
            "data": station_result.data
        }
        
        # Build overall summary
        summaries = [
            f"Product Analysis: {part_number} (last {days} days)",
            "",
            "=== Yield Trend ===",
            trend_result.summary,
            "",
            "=== Station Comparison ===",
            station_result.summary,
        ]
        results["summary"] = "\n".join(summaries)
        
        return results
    
    def compare_stations(
        self,
        station_names: Optional[List[str]] = None,
        part_number: Optional[str] = None,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Compare multiple stations.
        
        Args:
            station_names: Specific stations to compare (None for all)
            part_number: Filter by product
            days: Number of days
            
        Returns:
            Comparison results
        """
        yield_tool = self._toolkit.yield_tool
        
        from pywats_agent import YieldFilter
        
        result = yield_tool._tool.analyze(YieldFilter(
            part_number=part_number,
            perspective="by station",
            days=days
        ))
        
        return {
            "summary": result.summary,
            "data": result.data,
            "metadata": result.metadata
        }
