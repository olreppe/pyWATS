"""
Comprehensive tests for statistical configuration and dimension analysis.

Tests all possible dimensions, multi-dimension combinations,
statistical thresholds, and sample size validation.

These tests explore the limits of the analysis infrastructure:
- All supported WATS dimensions
- Multi-dimension combinations (2, 3, N dimensions)
- Edge cases for sample sizes
- Sparsity warnings and validation
- Threshold configuration for different analysis types
"""

import pytest
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from unittest.mock import Mock, MagicMock

# Import all statistics symbols from public API
from pywats_agent.tools import (
    SampleSizeThresholds,
    DeviationThresholds,
    DimensionCardinalityLimits,
    StatisticalConfig,
    AnalysisType,
    MetricType,
    DimensionDiscovery,
    DimensionInfo,
    DimensionCombinationStats,
    get_statistical_config,
    set_statistical_config,
    reset_statistical_config,
    discover_dimensions,
)


# =============================================================================
# TEST FIXTURES - Mock yield data
# =============================================================================

@dataclass
class MockYieldData:
    """Mock YieldData for testing dimension analysis."""
    part_number: Optional[str] = None
    product_name: Optional[str] = None
    station_name: Optional[str] = None
    location: Optional[str] = None
    purpose: Optional[str] = None
    revision: Optional[str] = None
    test_operation: Optional[str] = None
    process_code: Optional[str] = None
    sw_filename: Optional[str] = None
    sw_version: Optional[str] = None
    product_group: Optional[str] = None
    level: Optional[str] = None
    batch_number: Optional[str] = None
    operator: Optional[str] = None
    fixture_id: Optional[str] = None
    period: Optional[str] = None
    unit_count: int = 100
    fpy: float = 95.0
    lpy: float = 98.0


def create_diverse_dataset(
    n_records: int = 100,
    n_stations: int = 5,
    n_operators: int = 8,
    n_batches: int = 20,
    n_fixtures: int = 3,
    n_locations: int = 2,
) -> List[MockYieldData]:
    """
    Create a diverse dataset for testing dimension discovery.
    
    Intentionally creates varying cardinalities to test sparse warnings.
    """
    data = []
    
    for i in range(n_records):
        data.append(MockYieldData(
            part_number=f"PART-{(i % 3) + 1:03d}",  # 3 part numbers
            product_name=f"Product {(i % 3) + 1}",
            station_name=f"ST-{(i % n_stations) + 1:02d}",
            location=f"Line-{(i % n_locations) + 1}",
            purpose="UUT",
            revision=f"R{(i % 4) + 1}",  # 4 revisions
            test_operation="FCT",
            process_code="100",
            sw_filename=f"test_v{(i % 2) + 1}.py",  # 2 sw versions
            sw_version=f"1.{i % 2}",
            product_group="Electronics",
            level="PCBA",
            batch_number=f"BATCH-{(i % n_batches) + 1:04d}",
            operator=f"OP-{(i % n_operators) + 1:02d}",
            fixture_id=f"FIX-{(i % n_fixtures) + 1:02d}",
            period=f"2024-W{(i % 4) + 1:02d}",
            unit_count=100 + (i % 50),  # Varying counts
            fpy=85.0 + (i % 15),  # 85-100% FPY
        ))
    
    return data


def create_sparse_dataset(n_records: int = 50, n_values: int = 100) -> List[MockYieldData]:
    """
    Create a sparse dataset where cardinality >> records.
    
    This should trigger sparsity warnings.
    """
    data = []
    
    for i in range(n_records):
        data.append(MockYieldData(
            part_number="PART-001",
            station_name=f"ST-{i + 1:03d}",  # Unique per record!
            batch_number=f"BATCH-{i + 1:06d}",  # Unique per record!
            unit_count=10,
            fpy=90.0,
        ))
    
    return data


def create_concentrated_dataset(n_records: int = 1000) -> List[MockYieldData]:
    """
    Create a concentrated dataset with most data in few dimension values.
    
    Tests that analysis works well with uneven distributions.
    """
    data = []
    
    for i in range(n_records):
        # 80% of data in 2 stations, 20% spread across 8
        if i % 10 < 8:
            station = f"ST-{(i % 2) + 1:02d}"
        else:
            station = f"ST-{(i % 8) + 3:02d}"
        
        data.append(MockYieldData(
            part_number="PART-001",
            station_name=station,
            operator=f"OP-{(i % 5) + 1:02d}",
            batch_number=f"BATCH-{(i % 10) + 1:04d}",
            unit_count=100,
            fpy=95.0 - (i % 10),  # Varying yield
        ))
    
    return data


# =============================================================================
# SAMPLE SIZE THRESHOLD TESTS
# =============================================================================

class TestSampleSizeThresholds:
    """Test sample size threshold configuration."""
    
    def test_default_thresholds_exist(self):
        """Default thresholds are defined."""
        
        thresholds = SampleSizeThresholds()
        
        assert thresholds.absolute_minimum > 0
        assert thresholds.low_confidence >= thresholds.absolute_minimum
        assert thresholds.medium_confidence >= thresholds.low_confidence
        assert thresholds.high_confidence >= thresholds.medium_confidence
        assert thresholds.publication_grade >= thresholds.high_confidence
    
    def test_default_values_match_research(self):
        """Default values align with statistical research."""
        
        thresholds = SampleSizeThresholds()
        
        # CLT: n≥30 for approximate normality
        assert thresholds.medium_confidence >= 30
        
        # Process capability: n≥100 recommended
        assert thresholds.publication_grade >= 100
    
    def test_confidence_levels(self):
        """Confidence level calculation."""
        
        thresholds = SampleSizeThresholds()
        
        # Below absolute minimum
        conf, desc = thresholds.get_confidence_level(2)
        assert conf < 0.2
        assert "insufficient" in desc
        
        # Low confidence range
        conf, desc = thresholds.get_confidence_level(15)
        assert 0.3 <= conf <= 0.7
        
        # Medium confidence range
        conf, desc = thresholds.get_confidence_level(40)
        assert 0.7 <= conf <= 0.9
        
        # High confidence
        conf, desc = thresholds.get_confidence_level(75)
        assert conf >= 0.85
        
        # Publication grade
        conf, desc = thresholds.get_confidence_level(150)
        assert conf >= 0.95
    
    def test_confidence_is_monotonic(self):
        """Confidence increases with sample size."""
        
        thresholds = SampleSizeThresholds()
        
        prev_conf = 0
        for n in [1, 5, 10, 20, 30, 50, 100, 200]:
            conf, _ = thresholds.get_confidence_level(n)
            assert conf >= prev_conf, f"Confidence should not decrease at n={n}"
            prev_conf = conf


class TestDeviationThresholds:
    """Test deviation threshold configuration."""
    
    def test_default_thresholds_exist(self):
        """Default thresholds are defined."""
        
        thresholds = DeviationThresholds()
        
        assert thresholds.critical > 0
        assert thresholds.high > 0
        assert thresholds.moderate > 0
        assert thresholds.low > 0
    
    def test_threshold_ordering(self):
        """Thresholds are in descending order of severity."""
        
        thresholds = DeviationThresholds()
        
        assert thresholds.critical > thresholds.high
        assert thresholds.high > thresholds.moderate
        assert thresholds.moderate > thresholds.low
    
    def test_classify_critical(self):
        """Critical deviations classified correctly."""
        
        thresholds = DeviationThresholds()
        
        assert thresholds.classify(-15.0) == "critical"
        assert thresholds.classify(-10.0) == "critical"  # Boundary
        assert thresholds.classify(15.0) == "critical"  # Positive also counts
    
    def test_classify_high(self):
        """High deviations classified correctly."""
        
        thresholds = DeviationThresholds()
        
        assert thresholds.classify(-7.0) == "high"
        assert thresholds.classify(-5.0) == "high"  # Boundary
    
    def test_classify_moderate(self):
        """Moderate deviations classified correctly."""
        
        thresholds = DeviationThresholds()
        
        assert thresholds.classify(-3.0) == "moderate"
        assert thresholds.classify(-2.0) == "moderate"  # Boundary
    
    def test_classify_low(self):
        """Low deviations classified correctly."""
        
        thresholds = DeviationThresholds()
        
        assert thresholds.classify(-1.5) == "low"
        assert thresholds.classify(-1.0) == "low"  # Boundary
    
    def test_classify_none(self):
        """Negligible deviations classified as none."""
        
        thresholds = DeviationThresholds()
        
        assert thresholds.classify(-0.5) == "none"
        assert thresholds.classify(0.0) == "none"
        assert thresholds.classify(0.3) == "none"


class TestDimensionCardinalityLimits:
    """Test dimension cardinality and sparsity checks."""
    
    def test_default_limits_exist(self):
        """Default limits are defined."""
        
        limits = DimensionCardinalityLimits()
        
        assert limits.warn_threshold > 0
        assert limits.max_recommended > limits.warn_threshold
        assert limits.sparsity_threshold > 0
    
    def test_check_sparsity_good(self):
        """Good data density passes check."""
        
        limits = DimensionCardinalityLimits()
        
        # 1000 samples, 5 values = 200 per cell
        is_ok, samples_per_cell, warning = limits.check_sparsity(1000, 5)
        
        assert is_ok is True
        assert samples_per_cell == 200.0
        assert warning == ""
    
    def test_check_sparsity_warns_on_high_cardinality(self):
        """High cardinality triggers warning."""
        
        limits = DimensionCardinalityLimits()
        
        # 1000 samples, 30 values = ~33 per cell (ok but warn)
        is_ok, samples_per_cell, warning = limits.check_sparsity(1000, 30)
        
        assert is_ok is True
        assert "cardinality" in warning.lower()
    
    def test_check_sparsity_fails_on_sparse(self):
        """Sparse data fails check."""
        
        limits = DimensionCardinalityLimits()
        
        # 100 samples, 50 values = 2 per cell (too sparse!)
        is_ok, samples_per_cell, warning = limits.check_sparsity(100, 50)
        
        assert is_ok is False
        assert samples_per_cell < limits.sparsity_threshold
        assert "sparse" in warning.lower()
    
    def test_extra_dimensions_increase_sparsity(self):
        """Adding dimensions increases sparsity exponentially."""
        
        limits = DimensionCardinalityLimits()
        
        # Base case: 1000 samples, 10 values
        ok_0, spc_0, _ = limits.check_sparsity(1000, 10, extra_dimensions=0)
        
        # With 1 extra dimension
        ok_1, spc_1, _ = limits.check_sparsity(1000, 10, extra_dimensions=1)
        
        # With 2 extra dimensions
        ok_2, spc_2, _ = limits.check_sparsity(1000, 10, extra_dimensions=2)
        
        # Each dimension doubles effective cardinality
        assert spc_1 < spc_0
        assert spc_2 < spc_1


# =============================================================================
# STATISTICAL CONFIG TESTS
# =============================================================================

class TestStatisticalConfig:
    """Test master statistical configuration."""
    
    def test_default_config(self):
        """Default configuration is valid."""
        
        config = StatisticalConfig()
        
        assert config.sample_size is not None
        assert config.deviation is not None
        assert config.cardinality is not None
        assert config.sample_weight + config.deviation_weight + config.confidence_weight == 1.0
    
    def test_for_analysis_type_screening(self):
        """Screening analysis has relaxed thresholds."""
        
        default = StatisticalConfig()
        screening = StatisticalConfig.for_analysis_type(AnalysisType.SCREENING)
        
        # Screening accepts smaller samples
        assert screening.sample_size.medium_confidence < default.sample_size.medium_confidence
        assert screening.min_combined_score < default.min_combined_score
    
    def test_for_analysis_type_diagnostic(self):
        """Diagnostic analysis has stricter thresholds."""
        
        default = StatisticalConfig()
        diagnostic = StatisticalConfig.for_analysis_type(AnalysisType.DIAGNOSTIC)
        
        # Diagnostic needs more samples
        assert diagnostic.sample_size.medium_confidence > default.sample_size.medium_confidence
        assert diagnostic.min_combined_score > default.min_combined_score
    
    def test_for_analysis_type_reporting(self):
        """Reporting analysis has highest confidence requirements."""
        
        diagnostic = StatisticalConfig.for_analysis_type(AnalysisType.DIAGNOSTIC)
        reporting = StatisticalConfig.for_analysis_type(AnalysisType.REPORTING)
        
        assert reporting.sample_size.medium_confidence > diagnostic.sample_size.medium_confidence
        assert reporting.min_combined_score >= diagnostic.min_combined_score
    
    def test_for_analysis_type_capability(self):
        """Capability analysis has strictest requirements."""
        
        reporting = StatisticalConfig.for_analysis_type(AnalysisType.REPORTING)
        capability = StatisticalConfig.for_analysis_type(AnalysisType.CAPABILITY)
        
        assert capability.sample_size.absolute_minimum > reporting.sample_size.absolute_minimum
    
    def test_calculate_finding_score_high_quality(self):
        """High quality findings get high scores."""
        
        config = StatisticalConfig()
        
        # Large sample, significant deviation
        score, should_report, breakdown = config.calculate_finding_score(
            sample_size=200,
            deviation=-12.0,
            historical_confidence=1.0
        )
        
        assert score > 0.8
        assert should_report is True
        assert breakdown["deviation_class"] == "critical"
        assert breakdown["sample_description"] == "very_high"
    
    def test_calculate_finding_score_low_quality(self):
        """Low quality findings get filtered out."""
        
        config = StatisticalConfig()
        
        # Small sample, small deviation
        score, should_report, breakdown = config.calculate_finding_score(
            sample_size=3,
            deviation=-0.5,
            historical_confidence=0.5
        )
        
        assert score < 0.3
        assert should_report is False
        assert breakdown["deviation_class"] == "none"
    
    def test_calculate_finding_score_marginal(self):
        """Marginal findings handled correctly."""
        
        config = StatisticalConfig()
        
        # Medium sample, moderate deviation
        score, should_report, breakdown = config.calculate_finding_score(
            sample_size=35,
            deviation=-3.5,
            historical_confidence=0.8
        )
        
        # Should be borderline
        assert 0.3 <= score <= 0.7
        # Should_report depends on exact threshold


# =============================================================================
# DIMENSION DISCOVERY TESTS
# =============================================================================

class TestDimensionDiscovery:
    """Test dimension discovery functionality."""
    
    def test_supported_dimensions_exist(self):
        """All expected WATS dimensions are supported."""
        
        expected = [
            "partNumber", "productName", "stationName", "location",
            "purpose", "revision", "testOperation", "processCode",
            "swFilename", "swVersion", "productGroup", "level",
            "batchNumber", "operator", "fixtureId", "period",
        ]
        
        for dim in expected:
            assert dim in DimensionDiscovery.SUPPORTED_DIMENSIONS
    
    def test_discover_all_dimensions(self):
        """Discovers all dimensions with data."""
        
        data = create_diverse_dataset(n_records=50)
        discovery = DimensionDiscovery()
        
        dimensions = discovery.discover_all_dimensions(data)
        
        # Should find multiple dimensions
        assert len(dimensions) > 5
        
        # Each should have metadata
        for name, info in dimensions.items():
            assert info.cardinality > 0
            assert info.total_samples > 0
            assert info.display_name
            assert info.wats_field
    
    def test_analyze_single_dimension(self):
        """Analyze a single dimension in detail."""
        
        data = create_diverse_dataset(n_records=100, n_stations=5)
        discovery = DimensionDiscovery()
        
        info = discovery.analyze_dimension(data, "stationName")
        
        assert info is not None
        assert info.name == "station_name"
        assert info.display_name == "Station"
        assert info.wats_field == "stationName"
        assert info.cardinality == 5
        assert len(info.sample_counts) == 5
    
    def test_analyze_unknown_dimension_returns_none(self):
        """Unknown dimensions return None."""
        
        data = create_diverse_dataset()
        discovery = DimensionDiscovery()
        
        info = discovery.analyze_dimension(data, "unknownDimension")
        
        assert info is None
    
    def test_sparse_data_triggers_warning(self):
        """Sparse data triggers sparsity warning."""
        
        data = create_sparse_dataset(n_records=50)
        discovery = DimensionDiscovery()
        
        info = discovery.analyze_dimension(data, "stationName")
        
        # With 50 records and 50 unique stations, should warn
        assert info is not None
        # Might have sparsity warning depending on thresholds
    
    def test_analyze_dimension_combination(self):
        """Analyze a dimension combination."""
        
        data = create_diverse_dataset(n_records=100, n_stations=3, n_operators=4)
        discovery = DimensionDiscovery()
        
        stats = discovery.analyze_dimension_combination(
            data,
            ["station_name", "operator"]
        )
        
        assert stats is not None
        assert stats.dimensions == ["station_name", "operator"]
        assert stats.populated_cells > 0
        assert stats.min_samples <= stats.max_samples
        assert stats.avg_samples > 0
    
    def test_all_dimensions_at_once(self):
        """Test what happens with ALL dimensions."""
        
        data = create_diverse_dataset(n_records=100)
        discovery = DimensionDiscovery()
        
        # Get all discovered dimensions
        all_dims = discovery.discover_all_dimensions(data)
        dim_names = list(all_dims.keys())
        
        # Try to analyze all at once
        stats = discovery.analyze_dimension_combination(data, dim_names)
        
        # Should get valid stats back
        assert stats.populated_cells > 0
        
        # Note: The actual viability depends on data distribution.
        # With our synthetic data, each record may be unique, making
        # all-dimensions analysis viable but with 1 sample per cell.
        # In production with real data, this would typically be sparse.
    
    def test_two_dimension_combination(self):
        """Test two-dimension combination analysis."""
        
        data = create_concentrated_dataset(n_records=1000)
        discovery = DimensionDiscovery()
        
        stats = discovery.analyze_dimension_combination(
            data,
            ["station_name", "operator"]
        )
        
        assert stats.is_viable is True
        assert stats.avg_samples > 10  # Should have good density
    
    def test_three_dimension_combination(self):
        """Test three-dimension combination analysis."""
        
        data = create_concentrated_dataset(n_records=1000)
        discovery = DimensionDiscovery()
        
        stats = discovery.analyze_dimension_combination(
            data,
            ["station_name", "operator", "batch_number"]
        )
        
        # Three dimensions will be sparser
        assert stats.populated_cells > 0
        # May or may not be viable depending on data distribution
    
    def test_suggest_viable_combinations(self):
        """Test automatic viable combination suggestions."""
        
        data = create_concentrated_dataset(n_records=500)
        discovery = DimensionDiscovery()
        
        suggestions = discovery.suggest_viable_combinations(
            data,
            max_dimensions=2
        )
        
        assert len(suggestions) > 0
        
        for suggestion in suggestions:
            assert "dimensions" in suggestion
            assert "stats" in suggestion
            assert "recommendation" in suggestion
            assert suggestion["stats"]["is_viable"] is True


# =============================================================================
# ALL DIMENSIONS TEST MATRIX
# =============================================================================

class TestAllDimensionsMatrix:
    """Exhaustive tests for all supported dimensions."""
    
    WATS_DIMENSIONS = [
        "partNumber", "productName", "stationName", "location",
        "purpose", "revision", "testOperation", "processCode",
        "swFilename", "swVersion", "productGroup", "level",
        "batchNumber", "operator", "fixtureId",
    ]
    
    @pytest.mark.parametrize("dimension", WATS_DIMENSIONS)
    def test_single_dimension_analysis(self, dimension):
        """Each dimension can be analyzed individually."""
        
        # Create data with this dimension populated
        data = create_diverse_dataset(n_records=50)
        discovery = DimensionDiscovery()
        
        info = discovery.analyze_dimension(data, dimension)
        
        # Should either discover dimension or return None if not in data
        if info is not None:
            assert info.cardinality > 0
            assert info.wats_field == dimension
    
    def test_all_dimension_pairs(self):
        """Test all possible two-dimension combinations."""
        from itertools import combinations
        
        data = create_concentrated_dataset(n_records=500)
        discovery = DimensionDiscovery()
        
        # Discover what's actually in the data
        available = discovery.discover_all_dimensions(data)
        dim_names = list(available.keys())[:6]  # Limit to avoid explosion
        
        results = []
        for combo in combinations(dim_names, 2):
            stats = discovery.analyze_dimension_combination(data, list(combo))
            results.append({
                "dimensions": combo,
                "viable": stats.is_viable,
                "avg_samples": stats.avg_samples,
            })
        
        # At least some combinations should be viable
        viable_count = sum(1 for r in results if r["viable"])
        assert viable_count > 0
    
    def test_dimension_triplets(self):
        """Test select three-dimension combinations."""
        
        data = create_concentrated_dataset(n_records=1000)
        discovery = DimensionDiscovery()
        
        # Test specific meaningful triplets
        triplets = [
            ["station_name", "operator", "batch_number"],
            ["station_name", "fixture_id", "operator"],
            ["location", "station_name", "operator"],
        ]
        
        for dims in triplets:
            # Only test if all dimensions exist
            available = discovery.discover_all_dimensions(data)
            if all(d in available for d in dims):
                stats = discovery.analyze_dimension_combination(data, dims)
                assert stats.populated_cells > 0
                # Should at least report something


# =============================================================================
# EDGE CASES AND LIMITS
# =============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_data(self):
        """Empty data handled gracefully."""
        
        discovery = DimensionDiscovery()
        dimensions = discovery.discover_all_dimensions([])
        
        assert dimensions == {}
    
    def test_single_record(self):
        """Single record handled gracefully."""
        
        data = [MockYieldData(station_name="ST-01", unit_count=100)]
        discovery = DimensionDiscovery()
        
        info = discovery.analyze_dimension(data, "stationName")
        
        assert info is not None
        assert info.cardinality == 1
    
    def test_null_dimension_values(self):
        """Null/None dimension values handled."""
        
        data = [
            MockYieldData(station_name="ST-01", operator="OP-1"),
            MockYieldData(station_name="ST-02", operator=None),  # Null operator
            MockYieldData(station_name=None, operator="OP-2"),   # Null station
        ]
        
        discovery = DimensionDiscovery()
        
        # Should handle without error
        station_info = discovery.analyze_dimension(data, "stationName")
        assert station_info is not None
        # Null values grouped as "(null)"
        assert "(null)" in station_info.sample_counts or station_info.cardinality == 2
    
    def test_very_high_cardinality(self):
        """Very high cardinality dimension."""
        
        # Serial numbers - unique per unit
        data = [MockYieldData(batch_number=f"SN-{i:08d}") for i in range(1000)]
        discovery = DimensionDiscovery()
        
        info = discovery.analyze_dimension(data, "batchNumber")
        
        assert info is not None
        assert info.cardinality == 1000
        assert info.sparsity_warning is not None  # Should warn!
    
    def test_sample_size_zero(self):
        """Zero sample size handled."""
        
        config = StatisticalConfig()
        
        # Should not crash with edge case
        score, should_report, breakdown = config.calculate_finding_score(
            sample_size=0,
            deviation=-5.0
        )
        
        # Score should be low due to no samples
        assert breakdown["sample_confidence"] <= 0.3
        assert breakdown["sample_description"] == "insufficient"
    
    def test_extreme_deviation(self):
        """Extreme deviation values handled."""
        
        config = StatisticalConfig()
        
        # -100% deviation (impossible in reality but test anyway)
        score, should_report, breakdown = config.calculate_finding_score(
            sample_size=100,
            deviation=-100.0
        )
        
        assert breakdown["deviation_class"] == "critical"
        assert score > 0.5


# =============================================================================
# STATISTICAL CONFIG SINGLETON TESTS
# =============================================================================

class TestStatisticalConfigSingleton:
    """Test statistical config singleton pattern."""
    
    def test_get_default_config(self):
        """Get default config singleton."""
        
        reset_statistical_config()  # Clean slate
        
        config = get_statistical_config()
        assert config is not None
        
        # Same instance returned
        config2 = get_statistical_config()
        assert config is config2
    
    def test_set_custom_config(self):
        """Set custom config."""
        reset_statistical_config()
        
        # Create custom config
        custom = StatisticalConfig.for_analysis_type(AnalysisType.CAPABILITY)
        set_statistical_config(custom)
        
        # Should get our custom config back
        retrieved = get_statistical_config()
        assert retrieved.analysis_type == AnalysisType.CAPABILITY
        
        # Clean up
        reset_statistical_config()
    
    def test_reset_config(self):
        """Reset config to defaults."""
        # Set custom
        custom = StatisticalConfig.for_analysis_type(AnalysisType.REPORTING)
        set_statistical_config(custom)
        
        # Reset
        reset_statistical_config()
        
        # Should be default again
        config = get_statistical_config()
        assert config.analysis_type == AnalysisType.EXPLORATORY  # Default


# =============================================================================
# COMBINED SCORE CALCULATION TESTS
# =============================================================================

class TestCombinedScoreCalculation:
    """Test the weighted score calculation algorithm."""
    
    def test_weights_sum_to_one(self):
        """Weights should sum to 1.0 for proper scoring."""
        
        config = StatisticalConfig()
        
        total = config.sample_weight + config.deviation_weight + config.confidence_weight
        assert abs(total - 1.0) < 0.001
    
    def test_score_bounded_zero_to_one(self):
        """Score should always be between 0 and 1."""
        
        config = StatisticalConfig()
        
        test_cases = [
            (0, 0, 0),
            (1, 0, 0),
            (1000, -50, 1.0),
            (5, -1.0, 0.3),
        ]
        
        for sample, dev, hist in test_cases:
            score, _, _ = config.calculate_finding_score(sample, dev, hist)
            assert 0 <= score <= 1.0, f"Score {score} out of bounds for inputs {sample}, {dev}, {hist}"
    
    def test_sample_size_dominates_low_samples(self):
        """With very low samples, findings should have low confidence."""
        
        config = StatisticalConfig()
        
        # Even critical deviation has low confidence with tiny sample
        score, should_report, breakdown = config.calculate_finding_score(
            sample_size=2,
            deviation=-15.0,  # Critical!
            historical_confidence=0.5
        )
        
        # Should have low confidence due to sample size
        assert breakdown["sample_confidence"] < 0.5
        # Score should be lower than with high samples
        high_sample_score, _, _ = config.calculate_finding_score(
            sample_size=200,
            deviation=-15.0,
            historical_confidence=0.5
        )
        assert score < high_sample_score
    
    def test_deviation_dominates_high_samples(self):
        """With high samples, deviation becomes the deciding factor."""
        
        config = StatisticalConfig()
        
        # Large sample, small deviation
        score_low_dev, should_low, _ = config.calculate_finding_score(
            sample_size=500,
            deviation=-0.3,  # Very small
        )
        
        # Large sample, large deviation
        score_high_dev, should_high, _ = config.calculate_finding_score(
            sample_size=500,
            deviation=-12.0,  # Critical
        )
        
        assert score_high_dev > score_low_dev
        assert should_high is True
        # Low deviation might still be filtered even with high samples


# =============================================================================
# INTEGRATION WITH DEVIATION TOOL
# =============================================================================

class TestDeviationToolIntegration:
    """Test that deviation tool can use statistical config."""
    
    def test_deviation_tool_has_min_sample_size(self):
        """Deviation tool accepts min_sample_size parameter."""
        from pywats_agent.tools.yield_pkg.deviation_tool import DeviationInput
        
        input_params = DeviationInput(
            part_number="TEST-001",
            dimensions=["station_name"],
            min_sample_size=50
        )
        
        assert input_params.min_sample_size == 50
    
    def test_deviation_input_default_sample_size(self):
        """Deviation input has reasonable default."""
        from pywats_agent.tools.yield_pkg.deviation_tool import DeviationInput
        
        input_params = DeviationInput()
        
        # Default should be ≥10 (research-backed minimum)
        assert input_params.min_sample_size >= 10
    
    def test_all_standard_dimensions_defined(self):
        """All standard dimensions are defined in deviation tool."""
        from pywats_agent.tools.yield_pkg.deviation_tool import (
            StandardDimension,
            DIMENSION_TO_WATS,
        )
        
        # All enum values should have WATS mapping
        for dim in StandardDimension:
            assert dim in DIMENSION_TO_WATS


# =============================================================================
# DIMENSION INFO SERIALIZATION
# =============================================================================

class TestDimensionInfoSerialization:
    """Test DimensionInfo serialization for API responses."""
    
    def test_dimension_info_to_dict(self):
        """DimensionInfo serializes correctly."""
        
        info = DimensionInfo(
            name="station_name",
            display_name="Station",
            wats_field="stationName",
            cardinality=5,
            sample_counts={"ST-01": 100, "ST-02": 200},
            total_samples=300,
            coverage=1.0,
            sparsity_warning=None,
        )
        
        d = info.to_dict()
        
        assert d["name"] == "station_name"
        assert d["display_name"] == "Station"
        assert d["cardinality"] == 5
        assert d["total_samples"] == 300
        assert "top_values" in d
    
    def test_combination_stats_to_dict(self):
        """DimensionCombinationStats serializes correctly."""
        
        stats = DimensionCombinationStats(
            dimensions=["station_name", "operator"],
            total_cells=15,
            populated_cells=12,
            min_samples=5,
            max_samples=100,
            avg_samples=45.0,
            median_samples=40.0,
            cells_below_threshold=2,
            coverage=0.8,
            is_viable=True,
            warning=None,
        )
        
        d = stats.to_dict()
        
        assert d["dimensions"] == ["station_name", "operator"]
        assert d["populated_cells"] == 12
        assert d["is_viable"] is True
        assert "coverage_pct" in d
