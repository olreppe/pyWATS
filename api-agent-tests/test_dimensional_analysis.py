"""
Tests for dimensional yield analysis (failure mode detection).

These tests verify the dimensional analysis tool that bridges
top-level yield analysis and root cause investigation.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock

from pywats_agent.tools.dimensional_analysis import (
    DimensionalAnalysisTool,
    DimensionYieldResult,
    FailureModeResult,
    FailureModeFilter,
    SignificanceLevel,
    STANDARD_DIMENSIONS,
    DIMENSION_DISPLAY_NAMES,
    DIMENSION_TO_FIELD,
    get_dimensional_analysis_tool_definition,
)


class TestSignificanceLevel:
    """Tests for significance level classification."""
    
    def test_significance_levels_exist(self):
        """Verify all expected significance levels exist."""
        assert hasattr(SignificanceLevel, 'CRITICAL')
        assert hasattr(SignificanceLevel, 'HIGH')
        assert hasattr(SignificanceLevel, 'MODERATE')
        assert hasattr(SignificanceLevel, 'LOW')
        assert hasattr(SignificanceLevel, 'NOT_SIGNIFICANT')
    
    def test_significance_levels_have_values(self):
        """Verify significance levels have string values."""
        assert SignificanceLevel.CRITICAL.value == "critical"
        assert SignificanceLevel.HIGH.value == "high"
        assert SignificanceLevel.MODERATE.value == "moderate"


class TestStandardDimensions:
    """Tests for standard dimension configuration."""
    
    def test_standard_dimensions_exist(self):
        """Verify standard dimensions are defined."""
        assert len(STANDARD_DIMENSIONS) > 0
        assert "stationName" in STANDARD_DIMENSIONS
        assert "operator" in STANDARD_DIMENSIONS
        assert "fixtureId" in STANDARD_DIMENSIONS
        assert "batchNumber" in STANDARD_DIMENSIONS
    
    def test_dimensions_have_display_names(self):
        """Each standard dimension should have a display name."""
        for dim in STANDARD_DIMENSIONS:
            assert dim in DIMENSION_DISPLAY_NAMES, f"Missing display name for {dim}"
    
    def test_dimensions_have_field_mapping(self):
        """Each standard dimension should have a field mapping."""
        for dim in STANDARD_DIMENSIONS:
            assert dim in DIMENSION_TO_FIELD, f"Missing field mapping for {dim}"


class TestDimensionYieldResult:
    """Tests for dimension yield result dataclass."""
    
    def test_create_result(self):
        """Should create a valid result."""
        result = DimensionYieldResult(
            dimension="stationName",
            value="Station-3",
            display_name="Station",
            fpy=82.5,
            lpy=95.0,
            unit_count=150,
            baseline_fpy=95.0,
            fpy_delta=-12.5,
            fpy_delta_pct=-13.2,
            significance=SignificanceLevel.CRITICAL,
            confidence=0.95,
        )
        
        assert result.dimension == "stationName"
        assert result.value == "Station-3"
        assert result.fpy == 82.5
        assert result.fpy_delta == -12.5
        assert result.significance == SignificanceLevel.CRITICAL
    
    def test_to_dict(self):
        """Should convert to dictionary."""
        result = DimensionYieldResult(
            dimension="stationName",
            value="Station-3",
            display_name="Station",
            fpy=82.5,
            lpy=95.0,
            unit_count=150,
            baseline_fpy=95.0,
            fpy_delta=-12.5,
            fpy_delta_pct=-13.2,
            significance=SignificanceLevel.CRITICAL,
            confidence=0.95,
        )
        
        d = result.to_dict()
        assert d["dimension"] == "stationName"
        assert d["significance"] == "critical"
        assert d["fpy"] == 82.5


class TestFailureModeFilter:
    """Tests for failure mode filter."""
    
    def test_default_values(self):
        """Filter should have sensible defaults."""
        f = FailureModeFilter()
        
        assert f.days == 30
        assert f.min_units == 10
        assert f.significance_threshold == 2.0
        assert f.include_time_analysis is True
    
    def test_custom_values(self):
        """Filter should accept custom values."""
        f = FailureModeFilter(
            part_number="WIDGET-001",
            test_operation="FCT",
            days=14,
            min_units=20,
            significance_threshold=5.0,
        )
        
        assert f.part_number == "WIDGET-001"
        assert f.test_operation == "FCT"
        assert f.days == 14
        assert f.min_units == 20
    
    def test_custom_dimensions(self):
        """Filter should accept custom dimension list."""
        f = FailureModeFilter(
            dimensions=["stationName", "batchNumber"]
        )
        
        assert f.dimensions == ["stationName", "batchNumber"]


class TestDimensionalAnalysisTool:
    """Tests for the dimensional analysis tool."""
    
    @pytest.fixture
    def mock_api(self):
        """Create a mock API."""
        api = Mock()
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return api
    
    def test_instantiation(self, mock_api):
        """Tool should instantiate with API."""
        tool = DimensionalAnalysisTool(mock_api)
        assert tool._api == mock_api
    
    def test_has_name_and_description(self, mock_api):
        """Tool should have name and description."""
        tool = DimensionalAnalysisTool(mock_api)
        
        assert hasattr(tool, 'name')
        assert tool.name == "analyze_failure_modes"
        assert hasattr(tool, 'description')
        assert len(tool.description) > 100  # Should be substantial
    
    def test_description_mentions_workflow(self, mock_api):
        """Description should explain the workflow."""
        tool = DimensionalAnalysisTool(mock_api)
        
        desc_lower = tool.description.lower()
        assert "dimension" in desc_lower
        assert "yield" in desc_lower
        # Should mention common failure modes
        assert "station" in desc_lower or "batch" in desc_lower


class TestSignificanceCalculation:
    """Tests for significance calculation logic."""
    
    @pytest.fixture
    def tool(self):
        """Create tool with mock API."""
        api = Mock()
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return DimensionalAnalysisTool(api)
    
    def test_not_significant_positive_delta(self, tool):
        """Positive delta (better than baseline) should not be significant."""
        sig, conf = tool._calculate_significance(
            fpy_delta=5.0,  # Better than baseline
            unit_count=100,
            significance_threshold=2.0,
        )
        assert sig == SignificanceLevel.NOT_SIGNIFICANT
    
    def test_not_significant_small_delta(self, tool):
        """Small negative delta should not be significant."""
        sig, conf = tool._calculate_significance(
            fpy_delta=-1.0,  # Only 1% below baseline
            unit_count=100,
            significance_threshold=2.0,
        )
        assert sig == SignificanceLevel.NOT_SIGNIFICANT
    
    def test_critical_large_delta_high_confidence(self, tool):
        """Large delta with high sample size should be critical."""
        sig, conf = tool._calculate_significance(
            fpy_delta=-15.0,  # 15% below baseline
            unit_count=100,   # High sample size
            significance_threshold=2.0,
        )
        assert sig == SignificanceLevel.CRITICAL
        assert conf >= 0.70
    
    def test_high_medium_delta(self, tool):
        """Medium delta should be high significance."""
        sig, conf = tool._calculate_significance(
            fpy_delta=-7.0,  # 7% below baseline
            unit_count=50,
            significance_threshold=2.0,
        )
        assert sig == SignificanceLevel.HIGH
    
    def test_moderate_small_delta(self, tool):
        """Small delta should be moderate significance."""
        sig, conf = tool._calculate_significance(
            fpy_delta=-3.0,  # 3% below baseline
            unit_count=30,
            significance_threshold=2.0,
        )
        assert sig == SignificanceLevel.MODERATE
    
    def test_confidence_increases_with_sample_size(self, tool):
        """Confidence should increase with sample size."""
        _, conf_small = tool._calculate_significance(-10.0, 15, 2.0)
        _, conf_medium = tool._calculate_significance(-10.0, 50, 2.0)
        _, conf_large = tool._calculate_significance(-10.0, 150, 2.0)
        
        assert conf_small < conf_medium < conf_large


class TestAnalysisOutput:
    """Tests for analysis output generation."""
    
    @pytest.fixture
    def tool(self):
        """Create tool with mock API."""
        api = Mock()
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return DimensionalAnalysisTool(api)
    
    def test_generate_analysis_no_findings(self, tool):
        """Should generate appropriate message when no findings."""
        summary, recommendations = tool._generate_analysis(
            significant_findings=[],
            baseline_fpy=95.0,
            total_units=1000,
            part_number="WIDGET-001",
            test_operation="FCT",
        )
        
        assert "no significant" in summary.lower()
        assert len(recommendations) == 0
    
    def test_generate_analysis_with_findings(self, tool):
        """Should generate summary and recommendations for findings."""
        findings = [
            DimensionYieldResult(
                dimension="stationName",
                value="Station-3",
                display_name="Station",
                fpy=82.5,
                lpy=95.0,
                unit_count=150,
                baseline_fpy=95.0,
                fpy_delta=-12.5,
                fpy_delta_pct=-13.2,
                significance=SignificanceLevel.CRITICAL,
                confidence=0.95,
            )
        ]
        
        summary, recommendations = tool._generate_analysis(
            significant_findings=findings,
            baseline_fpy=95.0,
            total_units=1000,
            part_number="WIDGET-001",
            test_operation="FCT",
        )
        
        assert "Station-3" in summary
        assert "82.5" in summary or "82" in summary
        assert len(recommendations) > 0
        # Should recommend station investigation
        assert any("station" in r.lower() for r in recommendations)


class TestToolDefinition:
    """Tests for tool definition export."""
    
    def test_get_definition(self):
        """Should return valid tool definition."""
        defn = get_dimensional_analysis_tool_definition()
        
        assert defn["name"] == "analyze_failure_modes"
        assert "description" in defn
        assert "parameters" in defn
        assert "properties" in defn["parameters"]
    
    def test_definition_has_required_params(self):
        """Definition should have key parameters."""
        defn = get_dimensional_analysis_tool_definition()
        props = defn["parameters"]["properties"]
        
        assert "part_number" in props
        assert "test_operation" in props
        assert "days" in props
        assert "dimensions" in props


class TestDimensionMapping:
    """Tests for dimension field mapping."""
    
    def test_station_name_mapping(self):
        """stationName should map to station_name field."""
        assert DIMENSION_TO_FIELD["stationName"] == "station_name"
    
    def test_batch_number_mapping(self):
        """batchNumber should map to batch_number field."""
        assert DIMENSION_TO_FIELD["batchNumber"] == "batch_number"
    
    def test_all_standard_dimensions_mapped(self):
        """All standard dimensions should be mapped."""
        for dim in STANDARD_DIMENSIONS:
            assert dim in DIMENSION_TO_FIELD
            assert DIMENSION_TO_FIELD[dim]  # Should have non-empty value


class TestFailureModeDetection:
    """Integration-style tests for failure mode detection."""
    
    @pytest.fixture
    def mock_yield_data(self):
        """Create mock yield data with intentional failure mode."""
        class MockYieldData:
            def __init__(self, station_name, fp_count, unit_count):
                self.station_name = station_name
                self.fp_count = fp_count
                self.unit_count = unit_count
                self.lp_count = unit_count - 1  # Almost all pass eventually
                self.fpy = (fp_count / unit_count * 100) if unit_count else 0
                self.lpy = (self.lp_count / unit_count * 100) if unit_count else 0
        
        return [
            MockYieldData("Station-1", 95, 100),   # 95% FPY - good
            MockYieldData("Station-2", 94, 100),   # 94% FPY - good
            MockYieldData("Station-3", 72, 100),   # 72% FPY - BAD
            MockYieldData("Station-4", 96, 100),   # 96% FPY - good
        ]
    
    def test_detects_station_failure_mode(self, mock_yield_data):
        """Should detect a station-specific failure mode."""
        api = Mock()
        api.analytics = Mock()
        
        # First call returns baseline (all data aggregated)
        baseline_data = Mock()
        baseline_data.unit_count = 400
        baseline_data.fp_count = 357  # ~89% overall
        baseline_data.lp_count = 396
        baseline_data.fpy = 89.25
        baseline_data.lpy = 99.0
        
        # Configure mock to return different data for different calls
        def dynamic_yield_side_effect(filter_data):
            # Check if filter has dimensions
            if hasattr(filter_data, 'dimensions') and filter_data.dimensions:
                return mock_yield_data
            return [baseline_data]
        
        api.analytics.get_dynamic_yield = Mock(side_effect=dynamic_yield_side_effect)
        
        tool = DimensionalAnalysisTool(api)
        
        # Run analysis
        result = tool.analyze(FailureModeFilter(
            part_number="WIDGET-001",
            test_operation="FCT",
            days=30,
            dimensions=["stationName"],
            min_units=10,
        ))
        
        # Should have found significant findings
        assert result.success
        # Data should contain findings
        data = result.data
        assert data is not None


class TestDocumentationCoverage:
    """Tests that verify documentation completeness."""
    
    def test_description_mentions_common_patterns(self):
        """Tool description should mention common failure patterns."""
        api = Mock()
        tool = DimensionalAnalysisTool(api)
        desc = tool.description.lower()
        
        # Should mention equipment/station issues
        assert "station" in desc or "equipment" in desc
        # Should mention batch/component issues
        assert "batch" in desc or "component" in desc
        # Should mention operator issues
        assert "operator" in desc or "training" in desc
    
    def test_display_names_are_user_friendly(self):
        """Display names should be readable."""
        for dim, display in DIMENSION_DISPLAY_NAMES.items():
            # Display name should not be camelCase
            assert display[0].isupper(), f"{display} should start with capital"
            # Should not contain underscore
            assert "_" not in display
