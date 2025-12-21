"""
Test script for the agent toolset.

Run this to verify tool selection and parameter extraction without needing:
- A real API connection
- LLM API calls

Usage:
    python -m api-agent-tests.test_agent_harness
    
Or run specific tests:
    pytest api-agent-tests/test_agent_harness.py -v
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from unittest.mock import MagicMock

from pywats_agent import InMemoryDataStore, ToolExecutorV2
from pywats_agent.context import AgentContext
from pywats_agent.testing import (
    AgentTestHarness,
    TestCase,
    get_all_test_cases,
    get_step_analysis_test_cases,
    get_yield_tool_test_cases,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_api():
    """Create a mock pyWATS API for testing without real API calls."""
    api = MagicMock()
    api.analytics = MagicMock()
    return api


@pytest.fixture
def executor(mock_api):
    """Create an executor with mock API."""
    return ToolExecutorV2.with_default_tools(
        mock_api,
        datastore=InMemoryDataStore(),
        profile_name="minimal",
    )


@pytest.fixture
def harness(executor):
    """Create a test harness."""
    return AgentTestHarness(executor)


@pytest.fixture
def context_with_product():
    """Create context with a product set."""
    return AgentContext(
        current_product="WIDGET-001",
        current_station="Line1-FCT",
    )


# ============================================================================
# Tool Selection Tests
# ============================================================================

class TestToolSelection:
    """Test that prompts select the correct tools."""
    
    def test_yield_keywords(self, harness):
        """Test yield-related keywords select analyze_yield."""
        prompts = [
            "What's the yield for WIDGET-001?",
            "Show FPY by station",
            "What's the first pass yield?",
            "Show me the pass rate",
            "What's the failure rate?",
        ]
        for prompt in prompts:
            tool = harness.predict_tool(prompt)
            assert tool == "analyze_yield", f"Failed for: {prompt}"
    
    def test_step_analysis_keywords(self, harness):
        """Test step-related keywords select analyze_test_steps."""
        prompts = [
            "Which test steps are failing?",
            "Show step statistics",
            "What step is causing failures?",
            "Step analysis for FCT",
        ]
        for prompt in prompts:
            tool = harness.predict_tool(prompt)
            assert tool == "analyze_test_steps", f"Failed for: {prompt}"
    
    def test_measurement_stats_keywords(self, harness):
        """Test measurement statistics keywords."""
        prompts = [
            "What's the Cpk for voltage?",
            "Show measurement average",
            "What's the process capability?",
        ]
        for prompt in prompts:
            tool = harness.predict_tool(prompt)
            assert tool == "get_measurement_statistics", f"Failed for: {prompt}"
    
    def test_measurement_data_keywords(self, harness):
        """Test measurement data keywords."""
        prompts = [
            "Show raw measurement data",
            "Get individual measurements",
            "Show the last 100 measurements",
            "Recent measurement points",
        ]
        for prompt in prompts:
            tool = harness.predict_tool(prompt)
            assert tool == "get_measurement_data", f"Failed for: {prompt}"


# ============================================================================
# Parameter Extraction Tests
# ============================================================================

class TestParameterExtraction:
    """Test parameter extraction from natural language."""
    
    def test_part_number_extraction(self, harness):
        """Test part number extraction."""
        prompt = "What's the yield for WIDGET-001?"
        params = harness.extract_parameters(prompt)
        assert params.get("part_number") == "WIDGET-001"
    
    def test_days_extraction(self, harness):
        """Test days parameter extraction."""
        prompt = "Show yield for the last 7 days"
        params = harness.extract_parameters(prompt)
        assert params.get("days") == 7
    
    def test_perspective_extraction(self, harness):
        """Test perspective extraction."""
        cases = [
            ("Show yield by station", "by station"),
            ("Daily yield trend", "daily"),
            ("Yield by product", "by product"),
            ("Overall yield", "overall"),
        ]
        for prompt, expected in cases:
            params = harness.extract_parameters(prompt)
            assert params.get("perspective") == expected, f"Failed for: {prompt}"
    
    def test_test_operation_extraction(self, harness):
        """Test operation extraction."""
        prompt = "Which steps are failing in FCT?"
        params = harness.extract_parameters(prompt)
        assert params.get("test_operation") == "FCT"


# ============================================================================
# Context Tests
# ============================================================================

class TestContext:
    """Test context handling."""
    
    def test_context_defaults(self, context_with_product):
        """Test getting default parameters from context."""
        defaults = context_with_product.get_default_parameters()
        assert defaults["part_number"] == "WIDGET-001"
        assert defaults["station_name"] == "Line1-FCT"
    
    def test_context_system_prompt(self, context_with_product):
        """Test context to system prompt conversion."""
        prompt = context_with_product.to_system_prompt()
        assert "WIDGET-001" in prompt
        assert "Line1-FCT" in prompt
    
    def test_context_from_dict(self):
        """Test creating context from dictionary (like JSON request)."""
        data = {
            "current_product": "TEST-123",
            "current_station": "Station-A",
            "date_from": "2024-12-01",
        }
        context = AgentContext.from_dict(data)
        assert context.current_product == "TEST-123"
        assert context.current_station == "Station-A"
    
    # NOTE: v2 executor intentionally does not apply AgentContext defaults.


# ============================================================================
# Test Case Execution Tests
# ============================================================================

class TestTestCases:
    """Test running pre-built test cases."""
    
    def test_yield_test_cases(self, harness):
        """Run all yield tool test cases."""
        cases = get_yield_tool_test_cases()
        results = harness.run_tests(cases, execute_real=False)
        
        for result in results:
            assert result.passed, f"Failed: {result.test_case.name} - {result.error}"
    
    def test_step_analysis_test_cases(self, harness):
        """Run all step analysis test cases."""
        cases = get_step_analysis_test_cases()
        results = harness.run_tests(cases, execute_real=False)
        
        for result in results:
            assert result.passed, f"Failed: {result.test_case.name} - {result.error}"
    
    def test_custom_test_case(self, harness):
        """Test running a custom test case."""
        case = TestCase(
            name="custom_yield",
            prompt="What's the yield for WIDGET-001 by station for the last 14 days?",
            expected_tool="analyze_yield",
            expected_parameters={
                "part_number": "WIDGET-001",
                "perspective": "by station",
                "days": 14,
            }
        )
        result = harness.run_test(case)
        assert result.passed, result.error


# ============================================================================
# Dry Run Tests
# ============================================================================

class TestDryRun:
    """Test the dry run capability."""
    
    def test_dry_run_basic(self, harness):
        """Test basic dry run."""
        result = harness.dry_run("What's the yield for WIDGET-001?")
        
        assert result["predicted_tool"] == "analyze_yield"
        assert result["extracted_parameters"]["part_number"] == "WIDGET-001"
        assert result["would_execute"] is True
    
    def test_dry_run_with_context(self, executor, context_with_product):
        """Test dry run with context."""
        harness = AgentTestHarness(executor, context=context_with_product)
        
        # Query without specifying product - should use context default
        result = harness.dry_run("Show yield by station")
        
        assert result["predicted_tool"] == "analyze_yield"
        assert result["context_defaults"]["part_number"] == "WIDGET-001"
        assert result["final_parameters"]["part_number"] == "WIDGET-001"


# ============================================================================
# Interactive Testing (not pytest)
# ============================================================================

def run_interactive_test():
    """Run interactive tests to see the harness in action."""
    print("=" * 60)
    print("Agent Test Harness - Interactive Demo")
    print("=" * 60)
    
    # Create mock API and executor
    mock_api = MagicMock()
    executor = ToolExecutor(mock_api)
    harness = AgentTestHarness(executor)
    
    # Show available tools
    print("\n" + harness.get_tool_definitions_summary())
    
    # Test some prompts
    test_prompts = [
        "What's the yield for WIDGET-001?",
        "Show failing test steps for FCT",
        "What's the Cpk for voltage measurement?",
        "Get the last 100 temperature measurements",
    ]
    
    print("\n" + "=" * 60)
    print("Tool Selection Tests")
    print("=" * 60)
    
    for prompt in test_prompts:
        tool = harness.predict_tool(prompt)
        params = harness.extract_parameters(prompt)
        print(f"\nPrompt: {prompt}")
        print(f"  -> Tool: {tool}")
        print(f"  -> Params: {params}")
    
    # Run pre-built test suite
    print("\n" + "=" * 60)
    print("Running Pre-built Test Suite")
    print("=" * 60)
    
    results = harness.run_tests(get_all_test_cases())
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} passed")
    
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"  [{status}] {result.test_case.name}")
        if not result.passed:
            print(f"      Error: {result.error}")
    
    # Test with context
    print("\n" + "=" * 60)
    print("Context-Aware Testing")
    print("=" * 60)
    
    context = AgentContext(
        current_product="WIDGET-001",
        current_station="Line1-FCT",
        current_test_operation="FCT",
    )
    
    print(f"\nContext:\n{context.to_system_prompt()}")
    
    harness_with_context = AgentTestHarness(executor, context=context)
    dry_run = harness_with_context.dry_run("Show yield by station")
    
    print(f"\nDry run for: 'Show yield by station'")
    print(f"  Predicted tool: {dry_run['predicted_tool']}")
    print(f"  Extracted params: {dry_run['extracted_parameters']}")
    print(f"  Context defaults: {dry_run['context_defaults']}")
    print(f"  Final params: {dry_run['final_parameters']}")


if __name__ == "__main__":
    # Run interactive demo if called directly
    run_interactive_test()
