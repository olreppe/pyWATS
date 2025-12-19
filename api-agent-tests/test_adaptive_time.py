"""
Tests for adaptive time filtering and process resolution.

These tests verify the domain knowledge implementations for:
1. Adaptive time filtering for high-volume production
2. Process name resolution and fuzzy matching
3. Mixed process problem detection
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch
from pywats_agent.tools.adaptive_time import (
    AdaptiveTimeFilter,
    AdaptiveTimeConfig,
    AdaptiveTimeResult,
    VolumeCategory,
)
from pywats_agent.tools.process_resolver import (
    ProcessResolver,
    PROCESS_ALIASES,
    diagnose_mixed_process_problem,
)
from pywats_agent.tools.yield_tool import YieldFilter, YieldAnalysisTool


class TestVolumeCategory:
    """Tests for volume category classification."""
    
    def test_volume_categories_exist(self):
        """Verify all expected volume categories exist."""
        assert hasattr(VolumeCategory, 'VERY_HIGH')
        assert hasattr(VolumeCategory, 'HIGH')
        assert hasattr(VolumeCategory, 'MEDIUM')
        assert hasattr(VolumeCategory, 'LOW')
        assert hasattr(VolumeCategory, 'VERY_LOW')
    
    def test_volume_categories_have_values(self):
        """Verify categories have human-readable values."""
        assert VolumeCategory.VERY_HIGH.value
        assert VolumeCategory.LOW.value


class TestAdaptiveTimeConfig:
    """Tests for adaptive time configuration."""
    
    def test_default_config(self):
        """Default config should have sensible values."""
        config = AdaptiveTimeConfig()
        
        assert config.initial_days >= 1
        assert config.max_days > config.initial_days
        assert config.target_records > 0
        assert config.min_records > 0
    
    def test_config_customization(self):
        """Config should be customizable."""
        config = AdaptiveTimeConfig(
            initial_days=3,
            max_days=60,
            target_records=500
        )
        
        assert config.initial_days == 3
        assert config.max_days == 60
        assert config.target_records == 500


class TestAdaptiveTimeFilter:
    """Tests for the adaptive time filter."""
    
    @pytest.fixture
    def mock_api(self):
        """Create a mock API."""
        api = Mock()
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return api
    
    def test_instantiation(self, mock_api):
        """Filter should instantiate with API."""
        filter = AdaptiveTimeFilter(mock_api)
        assert filter._api == mock_api
    
    def test_custom_config(self, mock_api):
        """Filter should accept custom config."""
        config = AdaptiveTimeConfig(initial_days=5)
        filter = AdaptiveTimeFilter(mock_api, config=config)
        assert filter._config.initial_days == 5
    
    def test_categorize_volume_very_high(self, mock_api):
        """Very high volume should be detected (>100k/day)."""
        filter = AdaptiveTimeFilter(mock_api)
        
        # 150,000 units/day = very high
        category = filter._categorize_volume(150000)
        assert category == VolumeCategory.VERY_HIGH
    
    def test_categorize_volume_low(self, mock_api):
        """Low volume should be detected (100-1000/day)."""
        filter = AdaptiveTimeFilter(mock_api)
        
        # 500 units/day = low
        category = filter._categorize_volume(500)
        assert category == VolumeCategory.LOW


class TestProcessAliases:
    """Tests for process name aliases."""
    
    def test_common_aliases_exist(self):
        """Common manufacturing test aliases should exist."""
        common_tests = ['ict', 'fct', 'aoi', 'eol', 'pcba', 'board']
        
        for test in common_tests:
            assert any(test in alias.lower() for alias in PROCESS_ALIASES.keys()), \
                f"Missing alias for: {test}"
    
    def test_pcba_aliases(self):
        """PCBA should have multiple aliases."""
        pcba_aliases = [k for k in PROCESS_ALIASES.keys() 
                        if 'pcba' in k.lower() or 'board' in k.lower()]
        assert len(pcba_aliases) >= 2  # pcba, board test, etc.
    
    def test_ict_fct_aliases(self):
        """ICT and FCT should have aliases."""
        assert any('ict' in k.lower() for k in PROCESS_ALIASES.keys())
        assert any('fct' in k.lower() for k in PROCESS_ALIASES.keys())


class TestProcessResolver:
    """Tests for process name resolution."""
    
    @pytest.fixture
    def mock_processes(self):
        """Create mock process objects with proper attribute values."""
        class MockProcess:
            def __init__(self, code, name, is_test_operation=True, is_repair_operation=False, is_wip_operation=False):
                self.code = code
                self.name = name
                self.is_test_operation = is_test_operation
                self.is_repair_operation = is_repair_operation
                self.is_wip_operation = is_wip_operation
        
        return [
            MockProcess(1, 'ICT Test'),
            MockProcess(2, 'FCT Functional Test'),
            MockProcess(3, 'PCBA Test Station'),
            MockProcess(4, 'EOL Test'),
        ]
    
    @pytest.fixture
    def mock_api(self, mock_processes):
        """Create a mock API with process service."""
        api = Mock()
        # Mock api.process (ProcessService with auto-updating cache)
        api.process = Mock()
        api.process.get_processes = Mock(return_value=mock_processes)
        api.process.get_test_operations = Mock(return_value=mock_processes)
        api.process.get_repair_operations = Mock(return_value=[])
        return api
    
    def test_instantiation(self, mock_api):
        """Resolver should instantiate with API."""
        resolver = ProcessResolver(mock_api)
        assert resolver._api == mock_api
    
    def test_get_processes_delegates_to_api(self, mock_api):
        """Should delegate to api.process (which has auto-updating cache)."""
        resolver = ProcessResolver(mock_api)
        processes = resolver.get_processes()
        
        # Should have called api.process.get_processes()
        mock_api.process.get_processes.assert_called_once()
        assert len(processes) == 4
    
    def test_resolve_exact_match(self, mock_api):
        """Exact match should work."""
        resolver = ProcessResolver(mock_api)
        
        result = resolver.resolve("ICT Test")
        assert result is not None
        assert result.name == "ICT Test"
    
    def test_resolve_case_insensitive(self, mock_api):
        """Matching should be case insensitive."""
        resolver = ProcessResolver(mock_api)
        
        result = resolver.resolve("ict test")
        assert result is not None
        assert result.name == "ICT Test"
    
    def test_resolve_with_candidates(self, mock_api):
        """Should return multiple candidates for fuzzy matches."""
        resolver = ProcessResolver(mock_api)
        
        candidates = resolver.resolve_with_candidates("test")
        assert len(candidates) > 1  # Multiple processes contain "test"


class TestMixedProcessProblem:
    """Tests for mixed process problem detection."""
    
    @pytest.fixture
    def mock_api(self):
        """Create a mock API."""
        api = Mock()
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return api
    
    def test_diagnose_function_exists(self):
        """Diagnosis function should exist."""
        assert callable(diagnose_mixed_process_problem)
    
    def test_diagnose_requires_process_name(self, mock_api):
        """Should require process_name parameter."""
        # Function signature requires process_name
        import inspect
        sig = inspect.signature(diagnose_mixed_process_problem)
        params = list(sig.parameters.keys())
        assert 'process_name' in params


class TestYieldFilterAdaptiveTime:
    """Tests for adaptive_time in YieldFilter."""
    
    def test_adaptive_time_field_exists(self):
        """YieldFilter should have adaptive_time field."""
        filter = YieldFilter()
        assert hasattr(filter, 'adaptive_time')
    
    def test_adaptive_time_default_false(self):
        """adaptive_time should default to False."""
        filter = YieldFilter()
        assert filter.adaptive_time is False
    
    def test_adaptive_time_can_be_set(self):
        """adaptive_time should be settable to True."""
        filter = YieldFilter(adaptive_time=True)
        assert filter.adaptive_time is True


class TestYieldToolProcessResolution:
    """Tests for process resolution in YieldAnalysisTool."""
    
    @pytest.fixture
    def mock_api(self):
        """Create a mock API."""
        api = Mock()
        api.process = Mock()
        api.process.list = Mock(return_value=[])
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return api
    
    def test_tool_has_resolve_process_method(self, mock_api):
        """Tool should have process resolution method."""
        tool = YieldAnalysisTool(mock_api)
        assert hasattr(tool, 'resolve_process_name')
        assert callable(tool.resolve_process_name)
    
    def test_tool_has_get_processes_method(self, mock_api):
        """Tool should have method to get available processes."""
        tool = YieldAnalysisTool(mock_api)
        assert hasattr(tool, 'get_available_processes')
        assert callable(tool.get_available_processes)


class TestYieldToolMixedProcessDetection:
    """Tests for mixed process problem detection in YieldAnalysisTool."""
    
    @pytest.fixture
    def mock_api(self):
        """Create a mock API."""
        api = Mock()
        api.process = Mock()
        api.process.list = Mock(return_value=[])
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return api
    
    def test_tool_has_mixed_process_check(self, mock_api):
        """Tool should have mixed process problem detection."""
        tool = YieldAnalysisTool(mock_api)
        assert hasattr(tool, '_check_mixed_process_problem')
        assert callable(tool._check_mixed_process_problem)
    
    def test_description_mentions_mixed_process(self, mock_api):
        """Tool description should mention mixed process problem."""
        tool = YieldAnalysisTool(mock_api)
        
        assert "mixed" in tool.description.lower() or "MIXED" in tool.description
        assert "sw_filename" in tool.description or "different test" in tool.description.lower()


class TestProcessTerminologyDocumentation:
    """Tests for process terminology in documentation."""
    
    @pytest.fixture
    def mock_api(self):
        """Create a mock API."""
        api = Mock()
        api.process = Mock()
        api.process.list = Mock(return_value=[])
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return api
    
    def test_tool_mentions_test_operation(self, mock_api):
        """Tool should mention test_operation terminology."""
        tool = YieldAnalysisTool(mock_api)
        
        assert "test_operation" in tool.description
    
    def test_tool_explains_process_types(self, mock_api):
        """Tool should explain different process types."""
        tool = YieldAnalysisTool(mock_api)
        
        # Should mention test_operation is for testing
        assert "UUT" in tool.description or "test" in tool.description.lower()
    
    def test_docstring_mentions_process_terminology(self, mock_api):
        """Class docstring should mention process terminology."""
        tool = YieldAnalysisTool(mock_api)
        docstring = tool.__class__.__doc__ or ""
        
        # Should have process context explanation
        assert "process" in docstring.lower() or "operation" in docstring.lower()


class TestFuzzyMatchingDescription:
    """Tests for fuzzy matching documentation."""
    
    @pytest.fixture
    def mock_api(self):
        """Create a mock API."""
        api = Mock()
        api.process = Mock()
        api.process.list = Mock(return_value=[])
        api.analytics = Mock()
        api.analytics.get_dynamic_yield = Mock(return_value=[])
        return api
    
    def test_tool_description_mentions_fuzzy_matching(self, mock_api):
        """Tool description should mention fuzzy matching of process names."""
        tool = YieldAnalysisTool(mock_api)
        description_lower = tool.description.lower()
        
        # Should mention that fuzzy names work
        has_fuzzy_mention = (
            "pcba" in description_lower or
            "board test" in description_lower or
            "fuzzy" in description_lower
        )
        assert has_fuzzy_mention
