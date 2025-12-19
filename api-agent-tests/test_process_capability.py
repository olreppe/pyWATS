"""
Tests for Process Capability Analysis tool.

Tests cover:
1. Module structure and imports
2. Enums and constants
3. Data classes
4. Input model validation
5. Cpk analysis logic
6. Stability analysis logic
7. Hidden mode detection
8. Tool definition export
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch


class TestImports:
    """Test module can be imported correctly."""
    
    def test_import_module(self):
        """Module should import without errors."""
        from pywats_agent.tools import process_capability
        assert process_capability is not None
    
    def test_import_tool_class(self):
        """ProcessCapabilityTool should be importable."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        assert ProcessCapabilityTool is not None
    
    def test_import_from_init(self):
        """Should be importable from tools package."""
        from pywats_agent.tools import (
            ProcessCapabilityTool,
            ProcessCapabilityInput,
            ProcessCapabilityResult,
            MeasurementCapabilityResult,
            DualCpkAnalysis,
            StabilityAnalysis,
            HiddenMode,
            StabilityStatus,
            CapabilityStatus,
            ImprovementPriority,
            HiddenModeType,
        )
        assert ProcessCapabilityTool is not None
        assert ProcessCapabilityInput is not None
        assert ProcessCapabilityResult is not None


class TestStabilityStatus:
    """Test StabilityStatus enum."""
    
    def test_stability_values(self):
        """Enum should have expected values."""
        from pywats_agent.tools.process_capability import StabilityStatus
        
        assert StabilityStatus.STABLE.value == "stable"
        assert StabilityStatus.WARNING.value == "warning"
        assert StabilityStatus.UNSTABLE.value == "unstable"
        assert StabilityStatus.INSUFFICIENT_DATA.value == "insufficient_data"
    
    def test_stability_count(self):
        """Should have exactly 4 status levels."""
        from pywats_agent.tools.process_capability import StabilityStatus
        assert len(StabilityStatus) == 4


class TestCapabilityStatus:
    """Test CapabilityStatus enum."""
    
    def test_capability_values(self):
        """Enum should have expected values."""
        from pywats_agent.tools.process_capability import CapabilityStatus
        
        assert CapabilityStatus.CAPABLE.value == "capable"
        assert CapabilityStatus.MARGINAL.value == "marginal"
        assert CapabilityStatus.INCAPABLE.value == "incapable"
        assert CapabilityStatus.CRITICAL.value == "critical"
        assert CapabilityStatus.NO_DATA.value == "no_data"


class TestImprovementPriority:
    """Test ImprovementPriority enum."""
    
    def test_priority_values(self):
        """Enum should have expected values."""
        from pywats_agent.tools.process_capability import ImprovementPriority
        
        assert ImprovementPriority.CRITICAL.value == "critical"
        assert ImprovementPriority.HIGH.value == "high"
        assert ImprovementPriority.MEDIUM.value == "medium"
        assert ImprovementPriority.LOW.value == "low"
        assert ImprovementPriority.NONE.value == "none"


class TestHiddenModeType:
    """Test HiddenModeType enum."""
    
    def test_hidden_mode_values(self):
        """Enum should have expected mode types."""
        from pywats_agent.tools.process_capability import HiddenModeType
        
        expected = {
            "outliers", "trend_up", "trend_down", "shift",
            "bimodal", "alternating", "high_variance",
            "centering", "approaching_limit"
        }
        actual = {m.value for m in HiddenModeType}
        assert actual == expected


class TestCpkConstants:
    """Test Cpk threshold constants."""
    
    def test_cpk_thresholds(self):
        """Constants should have expected values."""
        from pywats_agent.tools.process_capability import (
            CPK_CAPABLE,
            CPK_MARGINAL,
            CPK_CRITICAL,
            CPK_EXCELLENT,
        )
        
        assert CPK_CAPABLE == 1.33
        assert CPK_MARGINAL == 1.0
        assert CPK_CRITICAL == 0.67
        assert CPK_EXCELLENT == 1.67
    
    def test_threshold_ordering(self):
        """Thresholds should be in correct order."""
        from pywats_agent.tools.process_capability import (
            CPK_CAPABLE,
            CPK_MARGINAL,
            CPK_CRITICAL,
            CPK_EXCELLENT,
        )
        
        assert CPK_CRITICAL < CPK_MARGINAL < CPK_CAPABLE < CPK_EXCELLENT


class TestDualCpkAnalysis:
    """Test DualCpkAnalysis dataclass."""
    
    def test_default_values(self):
        """Should have correct defaults."""
        from pywats_agent.tools.process_capability import DualCpkAnalysis
        
        analysis = DualCpkAnalysis()
        assert analysis.cpk_all is None
        assert analysis.cpk_wof is None
        assert analysis.failure_impact == "unknown"
        assert analysis.centering_issue is False
        assert analysis.critical_limit is None
    
    def test_to_dict(self):
        """Should convert to dictionary correctly."""
        from pywats_agent.tools.process_capability import DualCpkAnalysis
        
        analysis = DualCpkAnalysis(
            cpk_all=1.2,
            cpk_wof=1.5,
            failure_impact="significant"
        )
        d = analysis.to_dict()
        
        assert d["cpk_all"] == 1.2
        assert d["cpk_wof"] == 1.5
        assert d["failure_impact"] == "significant"


class TestHiddenMode:
    """Test HiddenMode dataclass."""
    
    def test_creation(self):
        """Should create with required fields."""
        from pywats_agent.tools.process_capability import HiddenMode, HiddenModeType
        
        mode = HiddenMode(
            mode_type=HiddenModeType.OUTLIERS,
            severity="high",
            description="Found outliers beyond 3σ"
        )
        
        assert mode.mode_type == HiddenModeType.OUTLIERS
        assert mode.severity == "high"
        assert "outliers" in mode.description.lower()
    
    def test_to_dict(self):
        """Should convert to dictionary correctly."""
        from pywats_agent.tools.process_capability import HiddenMode, HiddenModeType
        
        mode = HiddenMode(
            mode_type=HiddenModeType.CENTERING,
            severity="medium",
            description="Off center",
            evidence={"offset": 0.3},
            recommendation="Adjust process center"
        )
        d = mode.to_dict()
        
        assert d["mode_type"] == "centering"
        assert d["severity"] == "medium"
        assert d["evidence"]["offset"] == 0.3


class TestStabilityAnalysis:
    """Test StabilityAnalysis dataclass."""
    
    def test_default_values(self):
        """Should have correct defaults."""
        from pywats_agent.tools.process_capability import StabilityAnalysis, StabilityStatus
        
        stability = StabilityAnalysis(status=StabilityStatus.STABLE)
        assert stability.status == StabilityStatus.STABLE
        assert stability.sample_count == 0
        assert stability.issues == []
        assert stability.hidden_modes == []
    
    def test_to_dict_includes_modes(self):
        """to_dict should include hidden modes."""
        from pywats_agent.tools.process_capability import (
            StabilityAnalysis, StabilityStatus, HiddenMode, HiddenModeType
        )
        
        stability = StabilityAnalysis(
            status=StabilityStatus.WARNING,
            sample_count=100,
            hidden_modes=[
                HiddenMode(HiddenModeType.CENTERING, "medium", "Off center")
            ]
        )
        d = stability.to_dict()
        
        assert d["status"] == "warning"
        assert len(d["hidden_modes"]) == 1


class TestMeasurementCapabilityResult:
    """Test MeasurementCapabilityResult dataclass."""
    
    def test_creation(self):
        """Should create with required fields."""
        from pywats_agent.tools.process_capability import MeasurementCapabilityResult
        
        result = MeasurementCapabilityResult(
            step_name="Voltage Test",
            step_path="Main/Voltage Test"
        )
        
        assert result.step_name == "Voltage Test"
        assert result.step_path == "Main/Voltage Test"
    
    def test_to_dict_structure(self):
        """to_dict should have expected structure."""
        from pywats_agent.tools.process_capability import MeasurementCapabilityResult
        
        result = MeasurementCapabilityResult(
            step_name="Test",
            step_path="Main/Test"
        )
        d = result.to_dict()
        
        assert "step_name" in d
        assert "dual_cpk" in d
        assert "stability" in d
        assert "capability_status" in d
        assert "improvement_priority" in d


class TestProcessCapabilityResult:
    """Test ProcessCapabilityResult dataclass."""
    
    def test_default_counts(self):
        """Should have zero counts by default."""
        from pywats_agent.tools.process_capability import ProcessCapabilityResult
        
        result = ProcessCapabilityResult()
        assert result.capable_count == 0
        assert result.marginal_count == 0
        assert result.incapable_count == 0
        assert result.critical_count == 0
        assert result.stable_count == 0
        assert result.unstable_count == 0
    
    def test_to_dict_structure(self):
        """to_dict should have expected structure."""
        from pywats_agent.tools.process_capability import ProcessCapabilityResult
        
        result = ProcessCapabilityResult()
        d = result.to_dict()
        
        assert "total_measurements" in d
        assert "capable_count" in d
        assert "avg_cpk_all" in d
        assert "avg_cpk_wof" in d
        assert "critical_measurements" in d
        assert "unstable_measurements" in d
        assert "top_recommendations" in d


class TestProcessCapabilityInput:
    """Test ProcessCapabilityInput model."""
    
    def test_required_fields(self):
        """Should require part_number and test_operation."""
        from pywats_agent.tools.process_capability import ProcessCapabilityInput
        
        with pytest.raises(Exception):
            ProcessCapabilityInput()
        
        # Should work with required fields
        input_model = ProcessCapabilityInput(
            part_number="TEST-001",
            test_operation="FCT"
        )
        assert input_model.part_number == "TEST-001"
    
    def test_default_values(self):
        """Should have correct defaults."""
        from pywats_agent.tools.process_capability import ProcessCapabilityInput, CPK_CAPABLE
        
        input_model = ProcessCapabilityInput(
            part_number="TEST-001",
            test_operation="FCT"
        )
        
        assert input_model.days == 30
        assert input_model.run == 1
        assert input_model.cpk_threshold == CPK_CAPABLE
        assert input_model.include_stable_only is False
        assert input_model.max_measurements == 50
    
    def test_optional_filters(self):
        """Should accept optional filters."""
        from pywats_agent.tools.process_capability import ProcessCapabilityInput
        
        input_model = ProcessCapabilityInput(
            part_number="TEST-001",
            test_operation="FCT",
            revision="A",
            step_path="Main/*",
            step_name="Voltage"
        )
        
        assert input_model.revision == "A"
        assert input_model.step_path == "Main/*"
        assert input_model.step_name == "Voltage"


class TestProcessCapabilityTool:
    """Test ProcessCapabilityTool class."""
    
    def test_instantiation(self):
        """Should instantiate with API."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        assert tool._api is mock_api
        assert tool.name == "analyze_process_capability"
    
    def test_has_description(self):
        """Should have detailed description."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        assert len(ProcessCapabilityTool.description) > 200
        assert "stability" in ProcessCapabilityTool.description.lower()
        assert "cpk" in ProcessCapabilityTool.description.lower()
    
    def test_parameters_schema(self):
        """Should have valid parameter schema."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        schema = ProcessCapabilityTool.get_parameters_schema()
        
        assert schema["type"] == "object"
        assert "part_number" in schema["required"]
        assert "test_operation" in schema["required"]
        assert "cpk_threshold" in schema["properties"]
        assert "include_stable_only" in schema["properties"]


class TestToolDefinition:
    """Test tool definition export."""
    
    def test_definition_structure(self):
        """Should return valid tool definition."""
        from pywats_agent.tools.process_capability import get_process_capability_tool_definition
        
        definition = get_process_capability_tool_definition()
        
        assert "name" in definition
        assert "description" in definition
        assert "parameters" in definition
        assert definition["name"] == "analyze_process_capability"


class TestDualCpkAnalysisLogic:
    """Test the dual Cpk analysis logic."""
    
    def test_failure_impact_significant(self):
        """Should detect significant failure impact."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        # Create mock row with significant Cpk difference
        row = Mock()
        row.cpk = 0.9  # Low with failures
        row.cpk_wof = 1.5  # Much better without
        row.cp = 1.0
        row.cp_wof = 1.5
        row.cp_upper = 1.0
        row.cp_lower = 0.9
        row.cp_upper_wof = 1.5
        row.cp_lower_wof = 1.4
        
        analysis = tool._analyze_dual_cpk(row)
        
        assert analysis.cpk_all == 0.9
        assert analysis.cpk_wof == 1.5
        assert analysis.failure_impact == "significant"
        assert analysis.cpk_ratio > 1.3
    
    def test_centering_issue_detection(self):
        """Should detect centering issue when Cp >> Cpk."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        row = Mock()
        row.cpk = 0.8  # Low due to off-center
        row.cpk_wof = None
        row.cp = 1.5  # High - process has potential
        row.cp_wof = None
        row.cp_upper = 0.8
        row.cp_lower = 1.5
        row.cp_upper_wof = None
        row.cp_lower_wof = None
        
        analysis = tool._analyze_dual_cpk(row)
        
        assert analysis.centering_issue is True
    
    def test_critical_limit_upper(self):
        """Should identify upper as critical limit."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        row = Mock()
        row.cpk = 1.0
        row.cpk_wof = None
        row.cp = 1.2
        row.cp_wof = None
        row.cp_upper = 0.8  # Upper is worse
        row.cp_lower = 1.5
        row.cp_upper_wof = None
        row.cp_lower_wof = None
        
        analysis = tool._analyze_dual_cpk(row)
        
        assert analysis.critical_limit == "upper"


class TestStabilityAnalysisLogic:
    """Test stability analysis logic."""
    
    def test_insufficient_data(self):
        """Should report insufficient data for small samples."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool, StabilityStatus
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        row = Mock()
        row.measure_count = 10  # Less than MIN_SAMPLES_FOR_STABILITY
        row.step_count = 10
        row.measure_count_wof = 10
        row.avg = 5.0
        row.avg_wof = 5.0
        row.stdev = 0.1
        row.stdev_wof = 0.1
        row.sigma_high_3 = None
        row.sigma_low_3 = None
        row.sigma_high_3_wof = None
        row.sigma_low_3_wof = None
        row.limit1 = None
        row.limit2 = None
        
        stability = tool._analyze_stability(row)
        
        assert stability.status == StabilityStatus.INSUFFICIENT_DATA
        assert "Insufficient" in stability.issues[0]
    
    def test_high_variance_detection(self):
        """Should detect high variance relative to spec."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool, HiddenModeType
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        row = Mock()
        row.measure_count = 100
        row.step_count = 100
        row.measure_count_wof = 100
        row.avg = 5.0
        row.avg_wof = 5.0
        row.stdev = 0.5  # 6σ = 3.0, spec range = 2.0
        row.stdev_wof = 0.5
        row.sigma_high_3 = 6.5
        row.sigma_low_3 = 3.5
        row.sigma_high_3_wof = 6.5
        row.sigma_low_3_wof = 3.5
        row.limit1 = 4.0  # Spec range = 2.0
        row.limit2 = 6.0
        
        stability = tool._analyze_stability(row)
        
        # Should detect high variance
        mode_types = [m.mode_type for m in stability.hidden_modes]
        assert HiddenModeType.HIGH_VARIANCE in mode_types
    
    def test_centering_detection(self):
        """Should detect off-center process."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool, HiddenModeType
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        row = Mock()
        row.measure_count = 100
        row.step_count = 100
        row.measure_count_wof = 100
        row.avg = 5.8  # Far from center (5.0)
        row.avg_wof = 5.8
        row.stdev = 0.1
        row.stdev_wof = 0.1
        row.sigma_high_3 = 6.1
        row.sigma_low_3 = 5.5
        row.sigma_high_3_wof = 6.1
        row.sigma_low_3_wof = 5.5
        row.limit1 = 4.0  # Center = 5.0
        row.limit2 = 6.0
        
        stability = tool._analyze_stability(row)
        
        # Should detect centering issue
        mode_types = [m.mode_type for m in stability.hidden_modes]
        assert HiddenModeType.CENTERING in mode_types
    
    def test_approaching_limit_detection(self):
        """Should detect when approaching spec limit."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool, HiddenModeType
        
        mock_api = Mock()
        tool = ProcessCapabilityTool(mock_api)
        
        row = Mock()
        row.measure_count = 100
        row.step_count = 100
        row.measure_count_wof = 100
        row.avg = 5.85  # Very close to upper limit
        row.avg_wof = 5.85
        row.stdev = 0.1  # 2σ to limit
        row.stdev_wof = 0.1
        row.sigma_high_3 = 6.15
        row.sigma_low_3 = 5.55
        row.sigma_high_3_wof = 6.15
        row.sigma_low_3_wof = 5.55
        row.limit1 = 4.0
        row.limit2 = 6.0  # Only 0.15 away from mean
        
        stability = tool._analyze_stability(row)
        
        # Should detect approaching limit
        mode_types = [m.mode_type for m in stability.hidden_modes]
        assert HiddenModeType.APPROACHING_LIMIT in mode_types


class TestAnalyzeMethod:
    """Test the analyze method with mock data."""
    
    def test_analyze_no_data(self):
        """Should handle no data gracefully."""
        from pywats_agent.tools.process_capability import (
            ProcessCapabilityTool, ProcessCapabilityInput
        )
        
        mock_api = Mock()
        mock_api.analytics.get_test_step_analysis.return_value = []
        
        tool = ProcessCapabilityTool(mock_api)
        result = tool.analyze(ProcessCapabilityInput(
            part_number="TEST-001",
            test_operation="FCT"
        ))
        
        assert result.success is True
        assert result.data["measurements_analyzed"] == 0
    
    def test_analyze_with_measurements(self):
        """Should analyze measurements correctly."""
        from pywats_agent.tools.process_capability import (
            ProcessCapabilityTool, ProcessCapabilityInput
        )
        
        # Create mock measurement data
        mock_row = Mock()
        mock_row.step_name = "Voltage Test"
        mock_row.step_path = "Main/Voltage Test"
        mock_row.measure_name = "Output V"
        mock_row.cpk = 1.5
        mock_row.cpk_wof = 1.6
        mock_row.cp = 1.6
        mock_row.cp_wof = 1.7
        mock_row.cp_upper = 1.5
        mock_row.cp_lower = 1.6
        mock_row.cp_upper_wof = 1.6
        mock_row.cp_lower_wof = 1.7
        mock_row.measure_count = 100
        mock_row.step_count = 100
        mock_row.measure_count_wof = 95
        mock_row.avg = 5.0
        mock_row.avg_wof = 5.0
        mock_row.stdev = 0.1
        mock_row.stdev_wof = 0.09
        mock_row.sigma_high_3 = 5.3
        mock_row.sigma_low_3 = 4.7
        mock_row.sigma_high_3_wof = 5.27
        mock_row.sigma_low_3_wof = 4.73
        mock_row.limit1 = 4.0
        mock_row.limit2 = 6.0
        
        mock_api = Mock()
        mock_api.analytics.get_test_step_analysis.return_value = [mock_row]
        
        tool = ProcessCapabilityTool(mock_api)
        result = tool.analyze(ProcessCapabilityInput(
            part_number="TEST-001",
            test_operation="FCT"
        ))
        
        assert result.success is True
        assert result.data["measurements_analyzed"] == 1
        assert result.data["capable_count"] == 1
    
    def test_analyze_from_dict(self):
        """Should work with dictionary parameters."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        mock_api = Mock()
        mock_api.analytics.get_test_step_analysis.return_value = []
        
        tool = ProcessCapabilityTool(mock_api)
        result = tool.analyze_from_dict({
            "part_number": "TEST-001",
            "test_operation": "FCT"
        })
        
        assert result.success is True


class TestToolsExport:
    """Test exports from tools package."""
    
    def test_all_process_capability_exports(self):
        """All process capability exports should be in __all__."""
        from pywats_agent.tools import __all__
        
        expected_exports = [
            "ProcessCapabilityTool",
            "ProcessCapabilityInput",
            "ProcessCapabilityResult",
            "MeasurementCapabilityResult",
            "DualCpkAnalysis",
            "StabilityAnalysis",
            "HiddenMode",
            "StabilityStatus",
            "CapabilityStatus",
            "ImprovementPriority",
            "HiddenModeType",
            "CPK_CAPABLE",
            "CPK_MARGINAL",
            "CPK_CRITICAL",
            "CPK_EXCELLENT",
            "get_process_capability_tool_definition",
        ]
        
        for export in expected_exports:
            assert export in __all__, f"Missing export: {export}"


class TestDocumentation:
    """Test documentation coverage."""
    
    def test_module_docstring(self):
        """Module should have comprehensive docstring."""
        from pywats_agent.tools import process_capability
        
        doc = process_capability.__doc__
        assert doc is not None
        assert "Cpk" in doc
        assert "stability" in doc.lower()
        assert "hidden mode" in doc.lower()
    
    def test_tool_docstring(self):
        """Tool class should have detailed docstring."""
        from pywats_agent.tools.process_capability import ProcessCapabilityTool
        
        doc = ProcessCapabilityTool.__doc__
        assert doc is not None
        assert "STABILITY" in doc
        assert "DUAL" in doc
        assert "HIDDEN MODE" in doc


class TestWorkflowIntegration:
    """Test workflow integration documentation."""
    
    def test_workflow_in_init_docstring(self):
        """__init__.py should document process capability in workflow."""
        from pywats_agent import tools
        
        doc = tools.__doc__
        assert "Process" in doc
        assert "Capability" in doc
        assert "stable" in doc.lower()
    
    def test_cpk_comparison_documented(self):
        """Dual Cpk comparison should be documented."""
        from pywats_agent.tools import process_capability
        
        doc = process_capability.__doc__
        assert "Cpk_wof" in doc or "cpk_wof" in doc
        assert "Cpk (all)" in doc or "Cpk_all" in doc or "cpk_all" in doc
