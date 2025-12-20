"""
Tests for SubUnitAnalysisTool.

Tests the deep sub-unit analysis capabilities using query_header endpoint.
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime

from pywats_agent.tools.subunit import SubUnitAnalysisTool
from pywats_agent.tools.subunit.subunit_tool import (
    SubUnitAnalysisInput,
    SubUnitAnalysisResult,
    SubUnitSummary,
    ParentWithSubUnits,
    DeviationResult,
    QueryType,
)


class TestQueryType:
    """Test QueryType enum."""
    
    def test_all_query_types_defined(self):
        """All query types should be defined."""
        assert hasattr(QueryType, "FILTER_BY_SUBUNIT")
        assert hasattr(QueryType, "GET_SUBUNITS")
        assert hasattr(QueryType, "STATISTICS")
        assert hasattr(QueryType, "DEVIATION")
    
    def test_query_type_values(self):
        """Query types should have correct string values."""
        assert QueryType.FILTER_BY_SUBUNIT.value == "filter_by_subunit"
        assert QueryType.GET_SUBUNITS.value == "get_subunits"
        assert QueryType.STATISTICS.value == "statistics"
        assert QueryType.DEVIATION.value == "deviation"


class TestSubUnitAnalysisInput:
    """Test SubUnitAnalysisInput validation."""
    
    def test_minimal_input(self):
        """Should accept minimal input."""
        input = SubUnitAnalysisInput()
        assert input.query_type == QueryType.GET_SUBUNITS
        assert input.report_type == "uut"
        assert input.max_results == 1000
    
    def test_full_input(self):
        """Should accept full input."""
        input = SubUnitAnalysisInput(
            query_type=QueryType.FILTER_BY_SUBUNIT,
            subunit_part_number="PN123",
            subunit_serial_number="SN456",
            parent_part_number="PARENT-PN",
            parent_serial_number="PARENT-SN",
            process_name="FCT",
            station_name="Station1",
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2024, 1, 31),
            report_type="uur",
            expected_subunit_pns=["PN1", "PN2"],
            expected_subunit_count=3,
            max_results=500,
        )
        assert input.query_type == QueryType.FILTER_BY_SUBUNIT
        assert input.subunit_part_number == "PN123"
        assert input.parent_part_number == "PARENT-PN"
        assert input.max_results == 500
    
    def test_input_defaults(self):
        """Should have sensible defaults."""
        input = SubUnitAnalysisInput()
        assert input.subunit_part_number is None
        assert input.subunit_serial_number is None
        assert input.parent_part_number is None
        assert input.expected_subunit_pns is None
        assert input.expected_subunit_count is None


class TestSubUnitSummary:
    """Test SubUnitSummary model."""
    
    def test_create_summary(self):
        """Should create summary with all fields."""
        summary = SubUnitSummary(
            part_number="PN123",
            revision="A",
            part_type="Component",
            count=10,
            unique_serials=8,
            sample_serials=["SN1", "SN2", "SN3"]
        )
        assert summary.part_number == "PN123"
        assert summary.count == 10
        assert summary.unique_serials == 8
        assert len(summary.sample_serials) == 3


class TestParentWithSubUnits:
    """Test ParentWithSubUnits model."""
    
    def test_create_parent(self):
        """Should create parent with sub-units."""
        parent = ParentWithSubUnits(
            uuid="test-uuid-123",
            serial_number="SN001",
            part_number="PARENT-PN",
            revision="B",
            status="Passed",
            test_date=datetime(2024, 1, 15),
            sub_unit_count=3,
            sub_units=[
                {"part_number": "SUB1", "serial_number": "S1"},
                {"part_number": "SUB2", "serial_number": "S2"},
                {"part_number": "SUB3", "serial_number": "S3"},
            ]
        )
        assert parent.serial_number == "SN001"
        assert parent.sub_unit_count == 3
        assert len(parent.sub_units) == 3


class TestDeviationResult:
    """Test DeviationResult model."""
    
    def test_deviation_types(self):
        """Should support different deviation types."""
        missing = DeviationResult(
            parent_serial="SN001",
            parent_uuid="uuid1",
            deviation_type="missing_subunit",
            expected="PN123",
            actual=None,
            details="Expected sub-unit PN 'PN123' not found"
        )
        assert missing.deviation_type == "missing_subunit"
        
        unexpected = DeviationResult(
            parent_serial="SN002",
            parent_uuid="uuid2",
            deviation_type="unexpected_subunit",
            expected=None,
            actual="PN999",
            details="Unexpected sub-unit PN 'PN999' found"
        )
        assert unexpected.deviation_type == "unexpected_subunit"
        
        count = DeviationResult(
            parent_serial="SN003",
            parent_uuid="uuid3",
            deviation_type="count_mismatch",
            expected="3",
            actual="2",
            details="Expected 3 sub-units, found 2"
        )
        assert count.deviation_type == "count_mismatch"


class TestSubUnitAnalysisResult:
    """Test SubUnitAnalysisResult model."""
    
    def test_empty_result(self):
        """Should create empty result."""
        result = SubUnitAnalysisResult(query_type="get_subunits")
        assert result.total_parents == 0
        assert result.total_subunits == 0
        assert len(result.parents) == 0
        assert len(result.subunit_types) == 0
        assert len(result.deviations) == 0
    
    def test_result_with_data(self):
        """Should create result with data."""
        result = SubUnitAnalysisResult(
            query_type="statistics",
            total_parents=100,
            total_subunits=350,
            subunit_types=[
                SubUnitSummary(part_number="PN1", count=200),
                SubUnitSummary(part_number="PN2", count=150),
            ],
            warnings=["Inferred expected values from data"]
        )
        assert result.total_parents == 100
        assert result.total_subunits == 350
        assert len(result.subunit_types) == 2


class TestSubUnitAnalysisToolDefinition:
    """Test tool metadata and definition."""
    
    def test_tool_name(self):
        """Tool should have correct name."""
        assert SubUnitAnalysisTool.name == "analyze_subunits"
    
    def test_tool_description(self):
        """Tool should have comprehensive description."""
        desc = SubUnitAnalysisTool.description
        
        # Should mention key capabilities
        assert "sub-unit" in desc.lower()
        assert "filter" in desc.lower()
        assert "statistics" in desc.lower()
        assert "deviation" in desc.lower()
    
    def test_get_definition(self):
        """Should return valid tool definition."""
        definition = SubUnitAnalysisTool.get_definition()
        
        assert definition["name"] == "analyze_subunits"
        assert "description" in definition
        assert "parameters" in definition
    
    def test_parameters_schema(self):
        """Should have correct parameter schema."""
        schema = SubUnitAnalysisTool.get_parameters_schema()
        
        assert "properties" in schema
        assert "query_type" in schema["properties"]
        assert "subunit_part_number" in schema["properties"]
        assert "parent_part_number" in schema["properties"]


class TestSubUnitAnalysisToolExecution:
    """Test tool execution with mocked API."""
    
    @pytest.fixture
    def mock_api(self):
        """Create mock pyWATS API."""
        api = Mock()
        api.reports = Mock()
        return api
    
    @pytest.fixture
    def tool(self, mock_api):
        """Create tool instance with mocked API."""
        return SubUnitAnalysisTool(mock_api)
    
    def test_filter_by_subunit_requires_identifier(self, tool):
        """Filter by subunit should require PN or SN."""
        params = {
            "query_type": "filter_by_subunit",
        }
        result = tool.execute(params)
        
        assert not result.success
        assert "subunit_part_number" in result.error or "subunit_serial_number" in result.error
    
    def test_filter_by_subunit_part_number(self, tool, mock_api):
        """Should filter parents by sub-unit part number."""
        # Mock the API response - use dicts for sub_units to avoid Mock issues
        mock_header = Mock()
        mock_header.uuid = "test-uuid"
        mock_header.serial_number = "SN001"
        mock_header.part_number = "PARENT-PN"
        mock_header.revision = "A"
        mock_header.status = "Passed"
        mock_header.start = datetime(2024, 1, 15)
        # Use dict instead of Mock for sub-units
        mock_header.sub_units = [
            {"serial_number": "SUB-SN1", "part_number": "SUB-PN1", "revision": "A", "part_type": "Component"}
        ]
        
        mock_api.reports.query_headers_by_subunit_part_number.return_value = [mock_header]
        
        params = {
            "query_type": "filter_by_subunit",
            "subunit_part_number": "SUB-PN1",
        }
        result = tool.execute(params)
        
        assert result.success
        assert result.data["query_type"] == "filter_by_subunit"
        assert result.data["total_parents"] == 1
        
        # Verify API was called correctly
        mock_api.reports.query_headers_by_subunit_part_number.assert_called_once()
    
    def test_get_subunits_empty_result(self, tool, mock_api):
        """Should handle empty results gracefully."""
        mock_api.reports.query_headers_with_subunits.return_value = []
        
        params = {
            "query_type": "get_subunits",
            "parent_part_number": "NONEXISTENT",
        }
        result = tool.execute(params)
        
        assert result.success
        assert result.data["total_parents"] == 0
        assert "No reports found" in result.summary
    
    def test_get_subunits_with_data(self, tool, mock_api):
        """Should return sub-units for matching parents."""
        mock_header = Mock()
        mock_header.uuid = "test-uuid"
        mock_header.serial_number = "SN001"
        mock_header.part_number = "PARENT-PN"
        mock_header.revision = "A"
        mock_header.status = "Passed"
        mock_header.start = datetime(2024, 1, 15)
        # Use dicts for sub_units
        mock_header.sub_units = [
            {"serial_number": "SUB-SN1", "part_number": "SUB-PN1", "revision": "A", "part_type": "Component"},
            {"serial_number": "SUB-SN2", "part_number": "SUB-PN2", "revision": "B", "part_type": "Module"},
        ]
        
        mock_api.reports.query_headers_with_subunits.return_value = [mock_header]
        
        params = {
            "query_type": "get_subunits",
            "parent_part_number": "PARENT-PN",
        }
        result = tool.execute(params)
        
        assert result.success
        assert result.data["total_parents"] == 1
        assert result.data["total_subunits"] == 2
        assert len(result.data["parents"]) == 1
        assert len(result.data["parents"][0]["sub_units"]) == 2
    
    def test_statistics(self, tool, mock_api):
        """Should calculate sub-unit statistics."""
        # Create multiple headers with different sub-units (using dicts)
        mock_headers = []
        for i in range(3):
            h = Mock()
            h.uuid = f"uuid-{i}"
            h.serial_number = f"SN00{i}"
            h.part_number = "PARENT-PN"
            h.revision = "A"
            h.status = "Passed"
            h.start = datetime(2024, 1, 15)
            h.sub_units = [
                {"serial_number": f"SUB-{i}-1", "part_number": "COMMON-PN", "revision": "A", "part_type": "Component"},
                {"serial_number": f"SUB-{i}-2", "part_number": f"UNIQUE-PN-{i}", "revision": "A", "part_type": "Module"},
            ]
            mock_headers.append(h)
        
        mock_api.reports.query_headers_with_subunits.return_value = mock_headers
        
        params = {
            "query_type": "statistics",
            "parent_part_number": "PARENT-PN",
        }
        result = tool.execute(params)
        
        assert result.success
        assert result.data["query_type"] == "statistics"
        assert result.data["total_parents"] == 3
        assert result.data["total_subunits"] == 6  # 2 per parent
        
        # Should have statistics by type
        types = result.data["subunit_types"]
        assert len(types) >= 1  # At least COMMON-PN
    
    def test_deviation_detection(self, tool, mock_api):
        """Should detect deviations from expected configuration."""
        # Create headers with varying sub-unit configurations (using dicts)
        mock_headers = []
        
        # Normal unit with expected sub-units
        h1 = Mock()
        h1.uuid = "uuid-1"
        h1.serial_number = "SN001"
        h1.part_number = "PARENT-PN"
        h1.revision = "A"
        h1.status = "Passed"
        h1.start = datetime(2024, 1, 15)
        h1.sub_units = [
            {"serial_number": "S1", "part_number": "PN-A", "revision": "A", "part_type": "Component"},
            {"serial_number": "S2", "part_number": "PN-B", "revision": "A", "part_type": "Component"},
        ]
        mock_headers.append(h1)
        
        # Unit missing expected sub-unit
        h2 = Mock()
        h2.uuid = "uuid-2"
        h2.serial_number = "SN002"
        h2.part_number = "PARENT-PN"
        h2.revision = "A"
        h2.status = "Passed"
        h2.start = datetime(2024, 1, 16)
        h2.sub_units = [
            {"serial_number": "S3", "part_number": "PN-A", "revision": "A", "part_type": "Component"},
            # Missing PN-B
        ]
        mock_headers.append(h2)
        
        mock_api.reports.query_headers_with_subunits.return_value = mock_headers
        
        params = {
            "query_type": "deviation",
            "parent_part_number": "PARENT-PN",
            "expected_subunit_pns": ["PN-A", "PN-B"],
            "expected_subunit_count": 2,
        }
        result = tool.execute(params)
        
        assert result.success
        assert result.data["query_type"] == "deviation"
        
        # Should detect deviation
        deviations = result.data["deviations"]
        assert len(deviations) > 0
        
        # Should find the missing sub-unit
        missing = [d for d in deviations if d["deviation_type"] == "missing_subunit"]
        assert len(missing) >= 1
    
    def test_deviation_auto_inference(self, tool, mock_api):
        """Should infer expected values from data when not provided."""
        # Create headers with consistent configuration (using dicts)
        mock_headers = []
        for i in range(5):
            h = Mock()
            h.uuid = f"uuid-{i}"
            h.serial_number = f"SN00{i}"
            h.part_number = "PARENT-PN"
            h.revision = "A"
            h.status = "Passed"
            h.start = datetime(2024, 1, 15)
            h.sub_units = [
                {"serial_number": f"S{i}1", "part_number": "COMMON", "revision": "A", "part_type": "Component"},
            ]
            mock_headers.append(h)
        
        mock_api.reports.query_headers_with_subunits.return_value = mock_headers
        
        params = {
            "query_type": "deviation",
            "parent_part_number": "PARENT-PN",
            # No expected values provided
        }
        result = tool.execute(params)
        
        assert result.success
        # Should add warning about inferred values
        assert len(result.data["warnings"]) > 0
        assert "Inferred" in result.data["warnings"][0]


class TestSubUnitAnalysisToolReportTypes:
    """Test tool handles UUT and UUR report types correctly."""
    
    @pytest.fixture
    def mock_api(self):
        """Create mock pyWATS API."""
        api = Mock()
        api.reports = Mock()
        return api
    
    @pytest.fixture
    def tool(self, mock_api):
        """Create tool instance with mocked API."""
        return SubUnitAnalysisTool(mock_api)
    
    def test_uut_report_type(self, tool, mock_api):
        """Should use sub_units field for UUT reports."""
        mock_header = Mock()
        mock_header.uuid = "test-uuid"
        mock_header.serial_number = "SN001"
        mock_header.part_number = "PN001"
        mock_header.revision = "A"
        mock_header.status = "Passed"
        mock_header.start = datetime(2024, 1, 15)
        # Use dicts for sub_units
        mock_header.sub_units = [{"part_number": "SUB", "serial_number": "S1", "revision": "A", "part_type": "C"}]
        mock_header.uur_sub_units = []  # Should not be used
        
        mock_api.reports.query_headers_with_subunits.return_value = [mock_header]
        
        result = tool.execute({
            "query_type": "get_subunits",
            "report_type": "uut",
        })
        
        assert result.success
        assert result.data["total_subunits"] == 1
    
    def test_uur_report_type(self, tool, mock_api):
        """Should use uur_sub_units field for UUR reports."""
        mock_header = Mock()
        mock_header.uuid = "test-uuid"
        mock_header.serial_number = "SN001"
        mock_header.part_number = "PN001"
        mock_header.revision = "A"
        mock_header.status = "Passed"
        mock_header.start = datetime(2024, 1, 15)
        mock_header.sub_units = []  # Should not be used
        # Use dicts for uur_sub_units
        mock_header.uur_sub_units = [{"part_number": "SUB", "serial_number": "S1", "revision": "A", "part_type": "C"}]
        
        mock_api.reports.query_headers_with_subunits.return_value = [mock_header]
        
        result = tool.execute({
            "query_type": "get_subunits",
            "report_type": "uur",
        })
        
        assert result.success
        assert result.data["total_subunits"] == 1


class TestSubUnitAnalysisToolRegistry:
    """Test tool is properly registered."""
    
    def test_tool_in_registry(self):
        """Tool should be discoverable in registry."""
        from pywats_agent.tools._registry import get_tool
        
        tool_cls = get_tool("analyze_subunits")
        assert tool_cls is not None
        assert tool_cls.name == "analyze_subunits"
    
    def test_tool_in_variants(self):
        """Tool should be in appropriate profiles."""
        from pywats_agent.tools.variants import PROFILES, TOOL_CATEGORIES
        
        # Should be in full profile
        assert "analyze_subunits" in PROFILES["full"].tools
        
        # Should be in unit profile
        assert "analyze_subunits" in PROFILES["unit"].tools
        
        # Should be categorized as unit tool
        from pywats_agent.tools.variants import ToolCategory
        assert TOOL_CATEGORIES.get("analyze_subunits") == ToolCategory.UNIT
