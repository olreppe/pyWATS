"""
Agent result wrapper for consistent responses.

Provides a standardized format for tool execution results,
including both structured data and human-readable summaries.
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class AgentResult(BaseModel):
    """
    Standardized result from agent tool execution.
    
    Provides both structured data and human-readable summary
    for AI agents to consume and relay to users.
    
    Attributes:
        success: Whether the operation succeeded
        data: Structured data result (dict or list of dicts)
        summary: Human-readable summary of the result
        error: Error message if the operation failed
        metadata: Additional context (counts, averages, etc.)
    
    Example:
        >>> result = AgentResult.success(
        ...     data=[{"station": "A", "fpy": 95.0}],
        ...     summary="Found 1 station with 95% FPY",
        ...     metadata={"total_records": 1}
        ... )
        >>> print(result.summary)
        "Found 1 station with 95% FPY"
    """
    
    success: bool = Field(
        description="Whether the operation succeeded"
    )
    data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(
        default=None, 
        description="Structured data result"
    )
    summary: str = Field(
        description="Human-readable summary of the result"
    )
    error: Optional[str] = Field(
        default=None, 
        description="Error message if failed"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (counts, averages, etc.)"
    )
    
    @classmethod
    def success(
        cls,
        data: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None,
        summary: str = "Operation completed successfully",
        metadata: Optional[Dict[str, Any]] = None
    ) -> "AgentResult":
        """
        Create a successful result.
        
        Args:
            data: The structured data to return
            summary: Human-readable summary
            metadata: Additional context
            
        Returns:
            AgentResult indicating success
        """
        return cls(
            success=True,
            data=data,
            summary=summary,
            metadata=metadata or {}
        )
    
    @classmethod
    def error(cls, message: str) -> "AgentResult":
        """
        Create an error result.
        
        Args:
            message: Error description
            
        Returns:
            AgentResult indicating failure
        """
        return cls(
            success=False,
            error=message,
            summary=f"Error: {message}"
        )
    
    def to_openai_response(self) -> str:
        """
        Format result for OpenAI tool response.
        
        Returns:
            JSON string suitable for OpenAI tool response
        """
        import json
        
        if self.success:
            return json.dumps({
                "success": True,
                "summary": self.summary,
                "data": self.data,
                "metadata": self.metadata
            })
        else:
            return json.dumps({
                "success": False,
                "error": self.error
            })
    
    def __str__(self) -> str:
        """Return the summary as string representation."""
        return self.summary
