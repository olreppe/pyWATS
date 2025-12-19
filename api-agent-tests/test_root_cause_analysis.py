"""
Tests for the Root Cause Analysis Tool.

Tests the top-down, trend-aware failure investigation methodology.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch

from pywats_agent.tools.root_cause_analysis import (
    RootCauseAnalysisTool,
    RootCauseInput,
    RootCauseResult,
    YieldAssessmentResult,
    SuspectFinding,
    TrendAnalysis,
    TrendPattern,
    YieldAssessment,
    InvestigationPriority,
    STANDARD_DIMENSIONS,
    # Step 6-9 classes
    StepTrendPattern,
    FailingStepFinding,
    TrendQualifiedStep,
    ContextualComparison,
    ExplainableFinding,
)


class TestRootCauseInput:
    """Test input model validation."""
    
    def test_default_values(self):
        """Test default input values."""
        input_model = RootCauseInput()
        
        assert input_model.part_number is None
        assert input_model.test_operation is None
        assert input_model.days == 30
        assert input_model.target_yield == 95.0
        assert input_model.include_step_analysis is True
        assert input_model.max_suspects == 10
        assert input_model.force_investigate is False
    
    def test_custom_values(self):
        """Test custom input values."""
        input_model = RootCauseInput(
            part_number="WIDGET-001",
            test_operation="FCT",
            days=7,
            target_yield=98.0,
            force_investigate=True,
        )
        
        assert input_model.part_number == "WIDGET-001"
        assert input_model.test_operation == "FCT"
        assert input_model.days == 7
        assert input_model.target_yield == 98.0
        assert input_model.force_investigate is True


class TestTrendAnalysis:
    """Test trend analysis calculations."""
    
    def test_trend_to_dict(self):
        """Test trend serialization."""
        trend = TrendAnalysis(
            pattern=TrendPattern.EMERGING,
            current_value=85.0,
            previous_value=90.0,
            delta=-5.0,
            delta_percent=-5.5,
            slope=-0.5,
            periods_analyzed=7,
            variability=2.5,
            confidence=0.8,
            description="Emerging problem: yield declining.",
        )
        
        result = trend.to_dict()
        
        assert result["pattern"] == "emerging"
        assert result["current_value"] == 85.0
        assert result["previous_value"] == 90.0
        assert result["delta"] == -5.0
        assert result["slope"] == -0.5
        assert result["periods_analyzed"] == 7


class TestTrendPatterns:
    """Test trend pattern classification."""
    
    def test_pattern_values(self):
        """Test all pattern enum values exist."""
        assert TrendPattern.EMERGING.value == "emerging"
        assert TrendPattern.CHRONIC.value == "chronic"
        assert TrendPattern.RECOVERING.value == "recovering"
        assert TrendPattern.INTERMITTENT.value == "intermittent"
        assert TrendPattern.STABLE.value == "stable"
        assert TrendPattern.UNKNOWN.value == "unknown"


class TestYieldAssessment:
    """Test yield assessment status."""
    
    def test_assessment_values(self):
        """Test all assessment enum values exist."""
        assert YieldAssessment.HEALTHY.value == "healthy"
        assert YieldAssessment.CONCERNING.value == "concerning"
        assert YieldAssessment.POOR.value == "poor"
        assert YieldAssessment.CRITICAL.value == "critical"
        assert YieldAssessment.INSUFFICIENT_DATA.value == "insufficient_data"


class TestInvestigationPriority:
    """Test investigation priority levels."""
    
    def test_priority_values(self):
        """Test all priority enum values exist."""
        assert InvestigationPriority.CRITICAL.value == "critical"
        assert InvestigationPriority.HIGH.value == "high"
        assert InvestigationPriority.MEDIUM.value == "medium"
        assert InvestigationPriority.LOW.value == "low"
        assert InvestigationPriority.INFO.value == "info"


class TestSuspectFinding:
    """Test suspect finding data structure."""
    
    def test_suspect_to_dict(self):
        """Test suspect serialization."""
        suspect = SuspectFinding(
            dimension="stationName",
            value="Station-3",
            display_name="Station",
            fpy=82.0,
            unit_count=500,
            baseline_fpy=95.0,
            yield_delta=-13.0,
            yield_delta_percent=-13.7,
            impact_score=65.0,
            priority=InvestigationPriority.CRITICAL,
        )
        
        result = suspect.to_dict()
        
        assert result["dimension"] == "stationName"
        assert result["value"] == "Station-3"
        assert result["display_name"] == "Station"
        assert result["fpy"] == 82.0
        assert result["yield_delta"] == -13.0
        assert result["priority"] == "critical"
        assert result["impact_score"] == 65.0


class TestYieldAssessmentResult:
    """Test yield assessment result structure."""
    
    def test_healthy_result(self):
        """Test healthy yield assessment."""
        result = YieldAssessmentResult(
            status=YieldAssessment.HEALTHY,
            fpy=96.0,
            lpy=98.0,
            unit_count=1000,
            target_yield=95.0,
            yield_gap=-1.0,
            should_investigate=False,
            reason="Yield is healthy at 96%."
        )
        
        assert result.status == YieldAssessment.HEALTHY
        assert result.should_investigate is False
        assert result.fpy == 96.0
    
    def test_critical_result(self):
        """Test critical yield assessment."""
        result = YieldAssessmentResult(
            status=YieldAssessment.CRITICAL,
            fpy=80.0,
            lpy=85.0,
            unit_count=1000,
            target_yield=95.0,
            yield_gap=15.0,
            should_investigate=True,
            reason="CRITICAL: Yield is 80%, 15% below target!"
        )
        
        assert result.status == YieldAssessment.CRITICAL
        assert result.should_investigate is True
        assert result.yield_gap == 15.0


class TestStandardDimensions:
    """Test standard dimensions configuration."""
    
    def test_standard_dimensions_defined(self):
        """Test all standard dimensions are defined."""
        expected = [
            "stationName",
            "operator",
            "fixtureId",
            "batchNumber",
            "location",
            "period",
        ]
        
        for dim in expected:
            assert dim in STANDARD_DIMENSIONS, f"Missing dimension: {dim}"


class TestRootCauseAnalysisTool:
    """Test the main root cause analysis tool."""
    
    def test_tool_metadata(self):
        """Test tool name and description exist."""
        mock_api = Mock()
        tool = RootCauseAnalysisTool(mock_api)
        
        assert tool.name == "analyze_root_cause"
        assert len(tool.description) > 100  # Should have detailed description


class TestRootCauseResult:
    """Test root cause result structure."""
    
    def test_result_to_dict(self):
        """Test result serialization."""
        yield_assessment = YieldAssessmentResult(
            status=YieldAssessment.POOR,
            fpy=88.0,
            lpy=92.0,
            unit_count=1000,
            target_yield=95.0,
            yield_gap=7.0,
            should_investigate=True,
            reason="Yield is poor."
        )
        
        result = RootCauseResult(
            part_number="WIDGET-001",
            test_operation="FCT",
            days=30,
            date_from=datetime(2024, 11, 19),
            date_to=datetime(2024, 12, 19),
            yield_assessment=yield_assessment,
            suspects=[],
            summary="Investigation complete.",
            recommendations=["Investigate Station-3."],
            steps_completed=["yield_assessment", "dimensional_analysis"],
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["part_number"] == "WIDGET-001"
        assert result_dict["test_operation"] == "FCT"
        assert result_dict["yield_assessment"]["status"] == "poor"
        assert len(result_dict["recommendations"]) == 1
        assert len(result_dict["steps_completed"]) == 2


# =============================================================================
# Step 6-9 Tests
# =============================================================================

class TestStepTrendPattern:
    """Test step trend pattern classification (Step 7)."""
    
    def test_pattern_values(self):
        """Test all step trend pattern enum values exist."""
        assert StepTrendPattern.INCREASING.value == "increasing"
        assert StepTrendPattern.DECREASING.value == "decreasing"
        assert StepTrendPattern.STABLE.value == "stable"
        assert StepTrendPattern.VARIABLE.value == "variable"
        assert StepTrendPattern.UNKNOWN.value == "unknown"


class TestFailingStepFinding:
    """Test Step 6 failing step data structure."""
    
    def test_failing_step_to_dict(self):
        """Test failing step serialization."""
        finding = FailingStepFinding(
            step_name="Voltage_Check",
            step_path="/Main/Power/Voltage_Check",
            step_group="Power Tests",
            step_type="NumericLimitTest",
            total_executions=1000,
            failed_count=50,
            caused_unit_failure=35,
            failure_contribution_pct=25.0,
            failure_rate=5.0,
            suspect_context="Station:Station-3",
        )
        
        result = finding.to_dict()
        
        assert result["step_name"] == "Voltage_Check"
        assert result["step_path"] == "/Main/Power/Voltage_Check"
        assert result["caused_unit_failure"] == 35
        assert result["failure_contribution_pct"] == 25.0
        assert result["failure_rate"] == 5.0
        assert result["suspect_context"] == "Station:Station-3"
    
    def test_default_values(self):
        """Test default values for optional fields."""
        finding = FailingStepFinding(
            step_name="Test_Step",
            step_path="/Test_Step",
        )
        
        assert finding.total_executions == 0
        assert finding.failed_count == 0
        assert finding.caused_unit_failure == 0
        assert finding.failure_contribution_pct == 0.0


class TestTrendQualifiedStep:
    """Test Step 7 trend-qualified step data structure."""
    
    def test_trend_qualified_step_to_dict(self):
        """Test trend qualified step serialization."""
        step_finding = FailingStepFinding(
            step_name="Current_Measure",
            step_path="/Main/Current_Measure",
            total_executions=500,
            failed_count=30,
            caused_unit_failure=20,
            failure_contribution_pct=15.0,
            failure_rate=6.0,
        )
        
        trend_step = TrendQualifiedStep(
            step=step_finding,
            trend_pattern=StepTrendPattern.INCREASING,
            failure_rates_over_time=[4.0, 4.5, 5.0, 5.5, 6.0],
            trend_slope=0.5,
            trend_variability=0.7,
            is_regression=True,
            is_noise=False,
            trend_confidence=0.85,
            trend_description="REGRESSION: Step failures increasing.",
        )
        
        result = trend_step.to_dict()
        
        assert result["step"]["step_name"] == "Current_Measure"
        assert result["trend_pattern"] == "increasing"
        assert result["is_regression"] is True
        assert result["is_noise"] is False
        assert result["trend_confidence"] == 0.85
        assert len(result["failure_rates_over_time"]) == 5
    
    def test_regression_classification(self):
        """Test regression vs noise classification."""
        step = FailingStepFinding(step_name="Test", step_path="/Test")
        
        # Regression
        regression = TrendQualifiedStep(
            step=step,
            trend_pattern=StepTrendPattern.INCREASING,
            is_regression=True,
            is_noise=False,
        )
        assert regression.is_regression is True
        
        # Noise
        noise = TrendQualifiedStep(
            step=step,
            trend_pattern=StepTrendPattern.VARIABLE,
            is_regression=False,
            is_noise=True,
        )
        assert noise.is_noise is True


class TestContextualComparison:
    """Test Step 8 contextual comparison data structure."""
    
    def test_contextual_comparison_to_dict(self):
        """Test contextual comparison serialization."""
        comparison = ContextualComparison(
            step_name="Voltage_Check",
            step_path="/Main/Power/Voltage_Check",
            suspect_failure_rate=8.0,
            suspect_unit_count=500,
            suspect_caused_failures=35,
            non_suspect_failure_rate=2.0,
            non_suspect_unit_count=1500,
            non_suspect_caused_failures=25,
            historical_failure_rate=1.5,
            historical_unit_count=5000,
            rate_ratio=4.0,
            rate_delta=6.0,
            vs_historical_delta=6.5,
            is_causally_linked=True,
            causality_confidence=0.9,
            explanation="Step fails 4x more often in Station-3.",
        )
        
        result = comparison.to_dict()
        
        assert result["step_name"] == "Voltage_Check"
        assert result["suspect_failure_rate"] == 8.0
        assert result["non_suspect_failure_rate"] == 2.0
        assert result["rate_ratio"] == 4.0
        assert result["is_causally_linked"] is True
        assert result["causality_confidence"] == 0.9
    
    def test_causality_detection(self):
        """Test causality detection based on rate ratio."""
        # Causally linked (high rate ratio)
        causal = ContextualComparison(
            step_name="Test",
            step_path="/Test",
            suspect_failure_rate=10.0,
            non_suspect_failure_rate=2.0,
            rate_ratio=5.0,
            is_causally_linked=True,
        )
        assert causal.is_causally_linked is True
        
        # Not causally linked (similar rates)
        not_causal = ContextualComparison(
            step_name="Test",
            step_path="/Test",
            suspect_failure_rate=3.0,
            non_suspect_failure_rate=2.5,
            rate_ratio=1.2,
            is_causally_linked=False,
        )
        assert not_causal.is_causally_linked is False


class TestExplainableFinding:
    """Test Step 9 explainable finding data structure."""
    
    def test_explainable_finding_to_dict(self):
        """Test explainable finding serialization."""
        finding = ExplainableFinding(
            finding_id=1,
            priority=InvestigationPriority.CRITICAL,
            confidence=0.85,
            suspect_dimension="stationName",
            suspect_value="Station-3",
            suspect_impact=-13.0,
            step_name="Voltage_Check",
            step_path="/Main/Power/Voltage_Check",
            step_failure_contribution=25.0,
            yield_evidence="Product yield is CRITICAL at 82%.",
            trend_evidence="REGRESSION: Step failures increasing.",
            suspect_evidence="Station-3 has FPY 82% (-13% from baseline).",
            step_evidence="Step caused 35 unit failures (25% of total).",
            contextual_evidence="Step fails 4x more in Station-3 vs others.",
            explanation="Full investigation summary...",
            recommendation="Check Station-3 calibration.",
            expected_impact="Fixing could improve yield by 3%.",
        )
        
        result = finding.to_dict()
        
        assert result["finding_id"] == 1
        assert result["priority"] == "critical"
        assert result["confidence"] == 0.85
        assert result["suspect_dimension"] == "stationName"
        assert result["suspect_value"] == "Station-3"
        assert result["step_name"] == "Voltage_Check"
        assert result["step_failure_contribution"] == 25.0
        assert "REGRESSION" in result["trend_evidence"]
        assert "recommendation" in result
    
    def test_evidence_chain(self):
        """Test that evidence chain is complete."""
        finding = ExplainableFinding(
            finding_id=1,
            priority=InvestigationPriority.HIGH,
            confidence=0.75,
            suspect_dimension="operator",
            suspect_value="John",
            yield_evidence="Yield evidence here.",
            trend_evidence="Trend evidence here.",
            suspect_evidence="Suspect evidence here.",
            step_evidence="Step evidence here.",
            contextual_evidence="Contextual evidence here.",
        )
        
        result = finding.to_dict()
        
        # All evidence fields should be present
        assert result["yield_evidence"] != ""
        assert result["trend_evidence"] != ""
        assert result["suspect_evidence"] != ""
        assert result["step_evidence"] != ""
        assert result["contextual_evidence"] != ""


class TestRootCauseResultWithExtendedAnalysis:
    """Test RootCauseResult with Step 6-9 fields."""
    
    def test_result_with_extended_fields(self):
        """Test result includes Step 6-9 data."""
        yield_assessment = YieldAssessmentResult(
            status=YieldAssessment.POOR,
            fpy=85.0,
            lpy=90.0,
            unit_count=1000,
            target_yield=95.0,
            yield_gap=10.0,
            should_investigate=True,
            reason="Yield is poor."
        )
        
        failing_step = FailingStepFinding(
            step_name="Voltage_Check",
            step_path="/Main/Voltage_Check",
            caused_unit_failure=30,
            failure_contribution_pct=25.0,
        )
        
        trend_step = TrendQualifiedStep(
            step=failing_step,
            trend_pattern=StepTrendPattern.INCREASING,
            is_regression=True,
        )
        
        comparison = ContextualComparison(
            step_name="Voltage_Check",
            step_path="/Main/Voltage_Check",
            is_causally_linked=True,
        )
        
        explainable = ExplainableFinding(
            finding_id=1,
            priority=InvestigationPriority.CRITICAL,
            step_name="Voltage_Check",
            step_path="/Main/Voltage_Check",
        )
        
        result = RootCauseResult(
            part_number="WIDGET-001",
            test_operation="FCT",
            days=30,
            date_from=datetime(2024, 11, 19),
            date_to=datetime(2024, 12, 19),
            yield_assessment=yield_assessment,
            top_failing_steps=[failing_step],
            trend_qualified_steps=[trend_step],
            contextual_comparisons=[comparison],
            explainable_findings=[explainable],
            steps_completed=[
                "yield_assessment",
                "dimensional_analysis",
                "trend_analysis",
                "suspect_prioritization",
                "step_analysis",
                "top_failing_steps",
                "trend_qualified_steps",
                "contextual_analysis",
                "explainable_findings",
            ],
        )
        
        result_dict = result.to_dict()
        
        # Verify extended fields are in result
        assert len(result_dict["top_failing_steps"]) == 1
        assert len(result_dict["trend_qualified_steps"]) == 1
        assert len(result_dict["contextual_comparisons"]) == 1
        assert len(result_dict["explainable_findings"]) == 1
        assert "explainable_findings" in result_dict["steps_completed"]
        
        # Verify step data
        assert result_dict["top_failing_steps"][0]["step_name"] == "Voltage_Check"
        assert result_dict["trend_qualified_steps"][0]["is_regression"] is True
        assert result_dict["contextual_comparisons"][0]["is_causally_linked"] is True
        assert result_dict["explainable_findings"][0]["priority"] == "critical"


class TestInputExtendedOptions:
    """Test extended input options for Step 6-9."""
    
    def test_extended_analysis_defaults(self):
        """Test extended analysis default options."""
        input_model = RootCauseInput()
        
        assert input_model.include_extended_step_analysis is True
        assert input_model.min_failure_contribution == 5.0
    
    def test_custom_extended_options(self):
        """Test custom extended analysis options."""
        input_model = RootCauseInput(
            part_number="WIDGET-001",
            include_extended_step_analysis=False,
            min_failure_contribution=10.0,
        )
        
        assert input_model.include_extended_step_analysis is False
        assert input_model.min_failure_contribution == 10.0
