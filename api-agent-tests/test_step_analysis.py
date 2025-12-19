"""
Tests for Test Step Analysis (TSA) tool.

These tests verify the TSA domain knowledge is correctly implemented
without requiring a live server connection.
"""

import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta


# =============================================================================
# Import Tests - Verify module structure
# =============================================================================

class TestImports:
    """Verify all expected exports are available."""
    
    def test_step_analysis_tool_import(self):
        """StepAnalysisTool can be imported."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        assert StepAnalysisTool is not None
    
    def test_step_analysis_input_import(self):
        """StepAnalysisInput can be imported."""
        from pywats_agent.tools.step_analysis import StepAnalysisInput
        assert StepAnalysisInput is not None
    
    def test_cpk_status_import(self):
        """CpkStatus enum can be imported."""
        from pywats_agent.tools.step_analysis import CpkStatus
        assert CpkStatus is not None
    
    def test_cpk_thresholds_import(self):
        """Cpk threshold constants can be imported."""
        from pywats_agent.tools.step_analysis import (
            CPK_CAPABLE_THRESHOLD,
            CPK_MARGINAL_THRESHOLD,
            CPK_CRITICAL_THRESHOLD,
        )
        assert CPK_CAPABLE_THRESHOLD > CPK_MARGINAL_THRESHOLD
        assert CPK_MARGINAL_THRESHOLD > CPK_CRITICAL_THRESHOLD
    
    def test_result_classes_import(self):
        """Result dataclasses can be imported."""
        from pywats_agent.tools.step_analysis import (
            StepSummary,
            TSAResult,
            OverallProcessSummary,
            DataIntegrityResult,
        )
        assert StepSummary is not None
        assert TSAResult is not None


# =============================================================================
# CpkStatus Tests
# =============================================================================

class TestCpkStatus:
    """Test CpkStatus enum values."""
    
    def test_cpk_status_values(self):
        """CpkStatus has expected values."""
        from pywats_agent.tools.step_analysis import CpkStatus
        
        assert CpkStatus.CAPABLE.value == "capable"
        assert CpkStatus.MARGINAL.value == "marginal"
        assert CpkStatus.INCAPABLE.value == "incapable"
        assert CpkStatus.NO_DATA.value == "no_data"


# =============================================================================
# CPK Threshold Tests
# =============================================================================

class TestCpkThresholds:
    """Test Cpk threshold constants."""
    
    def test_capable_threshold_is_industry_standard(self):
        """Capable threshold is 1.33 (industry standard)."""
        from pywats_agent.tools.step_analysis import CPK_CAPABLE_THRESHOLD
        assert CPK_CAPABLE_THRESHOLD == 1.33
    
    def test_marginal_threshold_is_1_0(self):
        """Marginal threshold is 1.0."""
        from pywats_agent.tools.step_analysis import CPK_MARGINAL_THRESHOLD
        assert CPK_MARGINAL_THRESHOLD == 1.0
    
    def test_critical_threshold_is_0_67(self):
        """Critical threshold is 0.67."""
        from pywats_agent.tools.step_analysis import CPK_CRITICAL_THRESHOLD
        assert CPK_CRITICAL_THRESHOLD == 0.67


# =============================================================================
# StepAnalysisInput Tests
# =============================================================================

class TestStepAnalysisInput:
    """Test StepAnalysisInput filter model."""
    
    def test_required_fields(self):
        """part_number and test_operation are required."""
        from pywats_agent.tools.step_analysis import StepAnalysisInput
        
        # Should work with required fields
        input = StepAnalysisInput(
            part_number="TEST-001",
            test_operation="FCT"
        )
        assert input.part_number == "TEST-001"
        assert input.test_operation == "FCT"
    
    def test_default_values(self):
        """Default values are sensible."""
        from pywats_agent.tools.step_analysis import StepAnalysisInput
        
        input = StepAnalysisInput(
            part_number="TEST-001",
            test_operation="FCT"
        )
        
        assert input.days == 30
        assert input.run == 1
        assert input.max_count == 10000
        assert input.cpk_threshold == 1.33
        assert input.fail_rate_threshold == 5.0
    
    def test_optional_filters(self):
        """Optional filters can be set."""
        from pywats_agent.tools.step_analysis import StepAnalysisInput
        
        input = StepAnalysisInput(
            part_number="TEST-001",
            test_operation="FCT",
            revision="A",
            sw_filename="test.exe"
        )
        
        assert input.revision == "A"
        assert input.sw_filename == "test.exe"


# =============================================================================
# DataIntegrityResult Tests
# =============================================================================

class TestDataIntegrityResult:
    """Test data integrity result structure."""
    
    def test_consistent_result(self):
        """Consistent result has no warnings."""
        from pywats_agent.tools.step_analysis import DataIntegrityResult
        
        result = DataIntegrityResult(
            is_consistent=True,
            sw_versions=["test.exe"],
            revisions=["A"]
        )
        
        assert result.is_consistent
        assert result.warning_message is None
    
    def test_inconsistent_result(self):
        """Inconsistent result has warnings."""
        from pywats_agent.tools.step_analysis import DataIntegrityResult
        
        result = DataIntegrityResult(
            is_consistent=False,
            sw_versions=["test1.exe", "test2.exe"],
            revisions=["A", "B"],
            warning_message="Multiple SW versions detected",
            recommendation="Filter to specific version"
        )
        
        assert not result.is_consistent
        assert "Multiple SW" in result.warning_message
        assert result.recommendation is not None
    
    def test_to_dict(self):
        """to_dict returns expected structure."""
        from pywats_agent.tools.step_analysis import DataIntegrityResult
        
        result = DataIntegrityResult(
            is_consistent=True,
            sw_versions=["test.exe"]
        )
        
        d = result.to_dict()
        assert "is_consistent" in d
        assert "sw_versions" in d


# =============================================================================
# StepSummary Tests
# =============================================================================

class TestStepSummary:
    """Test StepSummary dataclass."""
    
    def test_create_step_summary(self):
        """Can create StepSummary with basic data."""
        from pywats_agent.tools.step_analysis import StepSummary, CpkStatus
        
        summary = StepSummary(
            step_name="Voltage Test",
            step_path="Main/Voltage Test",
            total_count=1000,
            passed_count=950,
            failed_count=50,
            pass_rate=95.0,
            cpk=1.45,
            cpk_status=CpkStatus.CAPABLE
        )
        
        assert summary.step_name == "Voltage Test"
        assert summary.pass_rate == 95.0
        assert summary.cpk == 1.45
    
    def test_caused_unit_fail_field(self):
        """caused_unit_fail field exists (critical for root cause)."""
        from pywats_agent.tools.step_analysis import StepSummary
        
        summary = StepSummary(
            step_name="Test",
            step_path="Test",
            caused_unit_fail=25
        )
        
        assert summary.caused_unit_fail == 25
    
    def test_to_dict(self):
        """to_dict includes all important fields."""
        from pywats_agent.tools.step_analysis import StepSummary, CpkStatus
        
        summary = StepSummary(
            step_name="Test",
            step_path="Main/Test",
            cpk=1.2,
            cpk_status=CpkStatus.MARGINAL
        )
        
        d = summary.to_dict()
        assert d["step_name"] == "Test"
        assert d["cpk"] == 1.2
        assert d["cpk_status"] == "marginal"


# =============================================================================
# OverallProcessSummary Tests
# =============================================================================

class TestOverallProcessSummary:
    """Test OverallProcessSummary dataclass."""
    
    def test_capability_counts(self):
        """Has capability distribution counts."""
        from pywats_agent.tools.step_analysis import OverallProcessSummary
        
        summary = OverallProcessSummary(
            capable_count=50,
            marginal_count=10,
            incapable_count=5
        )
        
        assert summary.capable_count == 50
        assert summary.marginal_count == 10
        assert summary.incapable_count == 5
    
    def test_cpk_aggregates(self):
        """Has Cpk aggregate statistics."""
        from pywats_agent.tools.step_analysis import OverallProcessSummary
        
        summary = OverallProcessSummary(
            avg_cpk=1.45,
            min_cpk=0.85,
            max_cpk=2.10
        )
        
        assert summary.avg_cpk == 1.45
        assert summary.min_cpk == 0.85
        assert summary.max_cpk == 2.10


# =============================================================================
# StepAnalysisTool Tests
# =============================================================================

class TestStepAnalysisTool:
    """Test StepAnalysisTool class."""
    
    def test_instantiation(self):
        """Tool can be instantiated with mock API."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        
        mock_api = MagicMock()
        tool = StepAnalysisTool(mock_api)
        
        assert tool._api == mock_api
    
    def test_has_name_and_description(self):
        """Tool has name and description."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        
        assert StepAnalysisTool.name == "analyze_test_steps_detailed"
        assert len(StepAnalysisTool.description) > 100
    
    def test_description_mentions_tsa_concepts(self):
        """Description mentions key TSA concepts."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        
        desc = StepAnalysisTool.description.lower()
        
        # Should mention Cpk
        assert "cpk" in desc
        
        # Should mention root cause
        assert "root cause" in desc or "caused" in desc
        
        # Should mention capability
        assert "capability" in desc or "capable" in desc
    
    def test_description_mentions_data_integrity(self):
        """Description mentions data integrity checks."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        
        desc = StepAnalysisTool.description.lower()
        
        assert "sw version" in desc or "software" in desc or "multiple" in desc
    
    def test_get_parameters_schema(self):
        """get_parameters_schema returns valid structure."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        
        schema = StepAnalysisTool.get_parameters_schema()
        
        assert schema["type"] == "object"
        assert "part_number" in schema["properties"]
        assert "test_operation" in schema["properties"]
        assert "cpk_threshold" in schema["properties"]
        assert schema["required"] == ["part_number", "test_operation"]


# =============================================================================
# Tool Definition Tests
# =============================================================================

class TestToolDefinition:
    """Test tool definition export."""
    
    def test_get_definition(self):
        """get_step_analysis_tool_definition returns expected structure."""
        from pywats_agent.tools.step_analysis import get_step_analysis_tool_definition
        
        definition = get_step_analysis_tool_definition()
        
        assert "name" in definition
        assert "description" in definition
        assert "parameters" in definition
    
    def test_definition_name(self):
        """Definition has correct name."""
        from pywats_agent.tools.step_analysis import get_step_analysis_tool_definition
        
        definition = get_step_analysis_tool_definition()
        assert definition["name"] == "analyze_test_steps_detailed"


# =============================================================================
# Process Capability Logic Tests
# =============================================================================

class TestCpkClassification:
    """Test Cpk classification logic (conceptual)."""
    
    def test_capable_cpk(self):
        """Cpk >= 1.33 is capable."""
        from pywats_agent.tools.step_analysis import (
            CpkStatus, CPK_CAPABLE_THRESHOLD
        )
        
        cpk = 1.5
        status = CpkStatus.CAPABLE if cpk >= CPK_CAPABLE_THRESHOLD else CpkStatus.MARGINAL
        assert status == CpkStatus.CAPABLE
    
    def test_marginal_cpk(self):
        """Cpk between 1.0 and 1.33 is marginal."""
        from pywats_agent.tools.step_analysis import (
            CpkStatus, CPK_CAPABLE_THRESHOLD, CPK_MARGINAL_THRESHOLD
        )
        
        cpk = 1.2
        if cpk >= CPK_CAPABLE_THRESHOLD:
            status = CpkStatus.CAPABLE
        elif cpk >= CPK_MARGINAL_THRESHOLD:
            status = CpkStatus.MARGINAL
        else:
            status = CpkStatus.INCAPABLE
        
        assert status == CpkStatus.MARGINAL
    
    def test_incapable_cpk(self):
        """Cpk < 1.0 is incapable."""
        from pywats_agent.tools.step_analysis import (
            CpkStatus, CPK_MARGINAL_THRESHOLD
        )
        
        cpk = 0.85
        status = CpkStatus.INCAPABLE if cpk < CPK_MARGINAL_THRESHOLD else CpkStatus.MARGINAL
        assert status == CpkStatus.INCAPABLE


# =============================================================================
# Documentation Coverage Tests
# =============================================================================

class TestDocumentationCoverage:
    """Test that documentation covers key concepts."""
    
    def test_module_docstring_mentions_workflow(self):
        """Module docstring explains workflow position."""
        from pywats_agent.tools import step_analysis
        
        docstring = step_analysis.__doc__
        assert docstring is not None
        assert "workflow" in docstring.lower() or "yield" in docstring.lower()
    
    def test_tool_docstring_mentions_single_product(self):
        """Tool docstring mentions single product/process recommendation."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        
        docstring = StepAnalysisTool.__doc__
        assert docstring is not None
        assert "single product" in docstring.lower() or "one product" in docstring.lower()
    
    def test_tool_docstring_mentions_step_caused_failure(self):
        """Tool docstring mentions step_caused_uut_failed concept."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        
        docstring = StepAnalysisTool.__doc__
        assert docstring is not None
        assert "caused" in docstring.lower() or "cause" in docstring.lower()


# =============================================================================
# Export from __init__ Tests
# =============================================================================

class TestToolsExport:
    """Test exports from tools __init__."""
    
    def test_step_analysis_tool_exported(self):
        """StepAnalysisTool is exported from tools package."""
        from pywats_agent.tools import StepAnalysisTool
        assert StepAnalysisTool is not None
    
    def test_step_analysis_input_exported(self):
        """StepAnalysisInput is exported."""
        from pywats_agent.tools import StepAnalysisInput
        assert StepAnalysisInput is not None
    
    def test_cpk_thresholds_exported(self):
        """Cpk thresholds are exported."""
        from pywats_agent.tools import (
            CPK_CAPABLE_THRESHOLD,
            CPK_MARGINAL_THRESHOLD,
        )
        assert CPK_CAPABLE_THRESHOLD == 1.33
    
    def test_result_classes_exported(self):
        """Result classes are exported."""
        from pywats_agent.tools import (
            TSAResult,
            StepSummary,
            OverallProcessSummary,
            DataIntegrityResult,
        )
        assert TSAResult is not None


# =============================================================================
# Integration with Workflow Tests
# =============================================================================

class TestWorkflowIntegration:
    """Test TSA fits into analysis workflow."""
    
    def test_tools_init_mentions_workflow(self):
        """Tools __init__ docstring explains workflow."""
        from pywats_agent import tools
        
        docstring = tools.__doc__
        assert docstring is not None
        assert "workflow" in docstring.lower()
    
    def test_workflow_order_in_docstring(self):
        """Workflow shows correct order: Yield -> Dimensional -> Step."""
        from pywats_agent import tools
        
        docstring = tools.__doc__
        # Should have some indication of order
        yield_pos = docstring.lower().find("yield")
        step_pos = docstring.lower().find("step")
        
        assert yield_pos >= 0
        assert step_pos >= 0
        # Yield should come before Step in the docstring
        assert yield_pos < step_pos


# =============================================================================
# Analyze Method Tests (with mocks)
# =============================================================================

class TestAnalyzeMethod:
    """Test analyze method behavior."""
    
    def test_analyze_returns_agent_result(self):
        """analyze returns AgentResult."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool, StepAnalysisInput
        from pywats_agent.result import AgentResult
        
        # Mock API
        mock_api = MagicMock()
        mock_api.analytics.get_dynamic_yield.return_value = []
        mock_api.analytics.get_test_step_analysis.return_value = []
        
        tool = StepAnalysisTool(mock_api)
        result = tool.analyze(StepAnalysisInput(
            part_number="TEST-001",
            test_operation="FCT"
        ))
        
        assert isinstance(result, AgentResult)
    
    def test_analyze_from_dict(self):
        """analyze_from_dict works with dict params."""
        from pywats_agent.tools.step_analysis import StepAnalysisTool
        from pywats_agent.result import AgentResult
        
        mock_api = MagicMock()
        mock_api.analytics.get_dynamic_yield.return_value = []
        mock_api.analytics.get_test_step_analysis.return_value = []
        
        tool = StepAnalysisTool(mock_api)
        result = tool.analyze_from_dict({
            "part_number": "TEST-001",
            "test_operation": "FCT"
        })
        
        assert isinstance(result, AgentResult)
