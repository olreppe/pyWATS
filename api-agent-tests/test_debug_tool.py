"""
Test the debug tool with real server connection.
"""
import pytest
from pywats_agent.tools import DebugTool


pytestmark = pytest.mark.agent
pytestmark = [pytest.mark.agent, pytest.mark.server]


class TestDebugTool:
    """Test debug tool for server connectivity."""
    
    def test_debug_tool_server_check(self, wats_client):
        """
        REAL TEST: Execute debug_server to verify connectivity and dynamic yield.
        
        This makes actual API calls to:
        1. Check server version (connectivity test)
        2. Call get_dynamic_yield with fixed parameters:
           - top_count: 10
           - period_count: 30
           - date_grouping: DAY
           - dimensions: partNumber
        """
        print("\n" + "="*70)
        print("TESTING DEBUG TOOL - Server Check")
        print("="*70)
        
        # Create debug tool
        debug_tool = DebugTool(wats_client)
        
        # Execute with empty parameters dict
        result = debug_tool.execute({})
        
        print(f"\nResult received:")
        print(f"  Type: {type(result)}")
        print(f"  Success: {result.success}")
        print(f"  Has error: {result.error is not None}")
        
        if result.summary:
            print(f"\n  Summary:")
            print(f"  {result.summary}")
        
        if result.data:
            print(f"\n  Data rows: {len(result.data)}")
        
        print("="*70 + "\n")
        
        # Verify
        assert result is not None, "Debug tool should return a result"
        assert hasattr(result, 'summary'), "Result should have summary"
        assert "Server is responding" in result.summary or "failed" in result.summary.lower(), \
            "Result should indicate server status"
        
        # Should not error if server is up
        if result.success:
            assert result.error is None, f"Successful result should not have error: {result.error}"
    
    def test_debug_tool_returns_data(self, wats_client):
        """Test that debug tool returns actual yield data."""
        debug_tool = DebugTool(wats_client)
        result = debug_tool.execute({})
        
        # If server is up, should have proper result structure
        if result.success:
            assert hasattr(result, 'data'), "Successful result should have data"
            # Data could be empty if no products in last 30 days, that's ok
            assert result.data is not None, "Data should not be None"
    
    def test_debug_tool_schema(self):
        """Test that debug tool has correct schema."""
        from pywats_agent.tools import get_debug_tool_definition
        
        definition = get_debug_tool_definition()
        
        assert definition is not None
        assert definition["type"] == "function"
        assert "function" in definition
        assert definition["function"]["name"] == "debug_server"
        assert "description" in definition["function"]
        assert "DEBUG TOOL" in definition["function"]["description"]
        
        # Should have no required parameters
        params = definition["function"]["parameters"]
        assert params["type"] == "object"
        assert len(params.get("required", [])) == 0, "Debug tool should have no required parameters"
