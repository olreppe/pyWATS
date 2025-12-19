"""
Central registry of all agent tools.

Provides a single source of truth for:
- What tools exist
- Tool metadata and discovery
- Tool instantiation

Usage:
    >>> from pywats_agent.tools._registry import get_all_tools, get_tool
    >>> 
    >>> # List all available tools
    >>> tools = get_all_tools()
    >>> 
    >>> # Get a specific tool class
    >>> YieldTool = get_tool("analyze_yield")
"""

from typing import Dict, Type, List, Optional, Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ._base import AgentTool
    from pywats import pyWATS


# Central registry - maps tool name to tool class
_TOOL_REGISTRY: Dict[str, Type["AgentTool"]] = {}

# Tool categories for organization
_TOOL_CATEGORIES: Dict[str, List[str]] = {
    "yield": [],           # Yield analysis tools
    "root_cause": [],      # Root cause investigation
    "capability": [],      # Process capability analysis
    "measurement": [],     # Measurement data tools
    "step": [],            # Step-level analysis
    "shared": [],          # Utility tools
}


def register_tool(
    name: str, 
    category: str = "shared",
) -> Callable[[Type["AgentTool"]], Type["AgentTool"]]:
    """
    Decorator to register a tool in the central registry.
    
    Args:
        name: Unique tool name (used in LLM function calls)
        category: Tool category for organization
        
    Returns:
        Decorator function
        
    Example:
        >>> @register_tool("analyze_yield", category="yield")
        ... class YieldAnalysisTool(AgentTool):
        ...     pass
    """
    def decorator(cls: Type["AgentTool"]) -> Type["AgentTool"]:
        if name in _TOOL_REGISTRY:
            raise ValueError(f"Tool '{name}' already registered")
        
        _TOOL_REGISTRY[name] = cls
        cls.name = name  # Ensure name is set on class
        
        if category in _TOOL_CATEGORIES:
            _TOOL_CATEGORIES[category].append(name)
        else:
            _TOOL_CATEGORIES[category] = [name]
            
        return cls
    
    return decorator


def get_tool(name: str) -> Optional[Type["AgentTool"]]:
    """
    Get a tool class by name.
    
    Args:
        name: Tool name
        
    Returns:
        Tool class or None if not found
    """
    return _TOOL_REGISTRY.get(name)


def get_all_tools() -> List[str]:
    """
    Get list of all registered tool names.
    
    Returns:
        List of tool names
    """
    return list(_TOOL_REGISTRY.keys())


def get_tools_by_category(category: str) -> List[str]:
    """
    Get tool names in a specific category.
    
    Args:
        category: Category name
        
    Returns:
        List of tool names in that category
    """
    return _TOOL_CATEGORIES.get(category, [])


def get_all_categories() -> Dict[str, List[str]]:
    """
    Get all categories and their tools.
    
    Returns:
        Dictionary mapping category names to tool lists
    """
    return dict(_TOOL_CATEGORIES)


def get_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get OpenAI-format definitions for all registered tools.
    
    Returns:
        List of tool definition dictionaries
    """
    return [cls.get_definition() for cls in _TOOL_REGISTRY.values()]


def get_tool_definitions_by_category(category: str) -> List[Dict[str, Any]]:
    """
    Get tool definitions for a specific category.
    
    Args:
        category: Category name
        
    Returns:
        List of tool definitions in that category
    """
    names = _TOOL_CATEGORIES.get(category, [])
    return [
        _TOOL_REGISTRY[name].get_definition() 
        for name in names 
        if name in _TOOL_REGISTRY
    ]


def create_tool_instance(name: str, api: "pyWATS") -> Optional["AgentTool"]:
    """
    Create an instance of a tool.
    
    Args:
        name: Tool name
        api: pyWATS instance
        
    Returns:
        Tool instance or None if not found
    """
    cls = get_tool(name)
    if cls:
        return cls(api)
    return None


def create_all_tools(api: "pyWATS") -> Dict[str, "AgentTool"]:
    """
    Create instances of all registered tools.
    
    Args:
        api: pyWATS instance
        
    Returns:
        Dictionary mapping tool names to instances
    """
    return {
        name: cls(api) 
        for name, cls in _TOOL_REGISTRY.items()
    }


# Registry summary for documentation
def print_registry_summary() -> None:
    """Print a summary of all registered tools."""
    print("=" * 60)
    print("PYWATS AGENT TOOL REGISTRY")
    print("=" * 60)
    
    for category, tools in sorted(_TOOL_CATEGORIES.items()):
        if tools:
            print(f"\n{category.upper()}:")
            for tool_name in sorted(tools):
                cls = _TOOL_REGISTRY.get(tool_name)
                if cls:
                    desc = cls.description[:50] + "..." if len(cls.description) > 50 else cls.description
                    print(f"  • {tool_name}: {desc}")
    
    print(f"\nTotal: {len(_TOOL_REGISTRY)} tools")
    print("=" * 60)
