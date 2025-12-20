"""
Tests for the Unit Analysis tool.

Tests the UnitAnalysisTool and its components.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock, patch

# Import unit tool components
from pywats_agent.tools.unit import (
    UnitAnalysisTool,
    UnitAnalysisInput,
    UnitInfo,
    UnitStatus,
    TestSummary,
    SubUnitInfo,
)
from pywats_agent.tools.unit.unit_tool import (
    AnalysisScope,
    ProductionInfo,
    VerificationGrade,
    ProcessVerification,
)
from pywats_agent.result import AgentResult


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def mock_api():
    """Create a mock pyWATS API."""
    api = Mock()
    
    # Setup analytics domain
    api.analytics = Mock()
    api.analytics.get_serial_number_history = Mock(return_value=[])
    api.analytics.get_uut_reports = Mock(return_value=[])
    
    # Setup production domain
    api.production = Mock()
    api.production.get_unit = Mock(return_value=None)
    api.production.get_unit_grade = Mock(return_value=None)
    
    # Setup report domain
    api.report = Mock()
    api.report.get_uut = Mock(return_value=None)
    
    return api


@pytest.fixture
def tool(mock_api):
    """Create a UnitAnalysisTool instance."""
    return UnitAnalysisTool(mock_api)


@pytest.fixture
def mock_report_header():
    """Create a mock report header."""
    header = Mock()
    header.part_number = "TEST-PN-001"
    header.revision = "A"
    header.serial_number = "SN12345"
    header.status = "P"
    header.start = datetime.now() - timedelta(days=1)
    header.process_name = "ICT"
    header.station_name = "Station_01"
    return header


# =============================================================================
# Test UnitStatus Enum
# =============================================================================

class TestUnitStatus:
    """Tests for UnitStatus enum."""
    
    def test_status_values_exist(self):
        """Verify all status values exist."""
        assert UnitStatus.PASSING
        assert UnitStatus.FAILING
        assert UnitStatus.IN_PROGRESS
        assert UnitStatus.REPAIRED
        assert UnitStatus.SCRAPPED
        assert UnitStatus.UNKNOWN
    
    def test_status_values_are_strings(self):
        """Status values should be strings."""
        assert UnitStatus.PASSING.value == "passing"
        assert UnitStatus.FAILING.value == "failing"
        assert UnitStatus.UNKNOWN.value == "unknown"


# =============================================================================
# Test AnalysisScope Enum
# =============================================================================

class TestAnalysisScope:
    """Tests for AnalysisScope enum."""
    
    def test_scope_values_exist(self):
        """Verify all scope values exist."""
        assert AnalysisScope.QUICK
        assert AnalysisScope.STANDARD
        assert AnalysisScope.FULL
        assert AnalysisScope.HISTORY_ONLY
        assert AnalysisScope.VERIFICATION
    
    def test_scope_values_are_strings(self):
        """Scope values should be strings."""
        assert AnalysisScope.QUICK.value == "quick"
        assert AnalysisScope.STANDARD.value == "standard"
        assert AnalysisScope.FULL.value == "full"


# =============================================================================
# Test TestSummary Model
# =============================================================================

class TestTestSummaryModel:
    """Tests for TestSummary model."""
    
    def test_default_values(self):
        """Test default values."""
        summary = TestSummary()
        assert summary.total_tests == 0
        assert summary.passed == 0
        assert summary.failed == 0
        assert summary.error == 0
        assert summary.first_test is None
        assert summary.last_test is None
    
    def test_pass_rate_calculation(self):
        """Test pass rate calculation."""
        summary = TestSummary(total_tests=100, passed=85, failed=15)
        assert summary.pass_rate == 85.0
    
    def test_pass_rate_zero_tests(self):
        """Pass rate should be 0 when no tests."""
        summary = TestSummary()
        assert summary.pass_rate == 0.0
    
    def test_processes_and_stations_lists(self):
        """Test that lists are properly initialized."""
        summary = TestSummary(
            processes_tested=["ICT", "FCT"],
            stations_used=["Station_01", "Station_02"]
        )
        assert len(summary.processes_tested) == 2
        assert len(summary.stations_used) == 2


# =============================================================================
# Test SubUnitInfo Model
# =============================================================================

class TestSubUnitInfoModel:
    """Tests for SubUnitInfo model."""
    
    def test_create_subunit(self):
        """Test creating a sub-unit."""
        sub = SubUnitInfo(
            part_type="Capacitor",
            serial_number="CAP-001",
            part_number="C100UF",
            revision="1.0"
        )
        assert sub.part_type == "Capacitor"
        assert sub.serial_number == "CAP-001"
        assert sub.part_number == "C100UF"
    
    def test_subunit_with_test_summary(self):
        """Test sub-unit with nested test summary."""
        summary = TestSummary(total_tests=5, passed=5)
        sub = SubUnitInfo(
            serial_number="SUB-001",
            test_summary=summary
        )
        assert sub.test_summary.total_tests == 5


# =============================================================================
# Test UnitInfo Model
# =============================================================================

class TestUnitInfoModel:
    """Tests for UnitInfo model."""
    
    def test_create_unit_info(self):
        """Test creating unit info."""
        info = UnitInfo(
            serial_number="SN12345",
            part_number="TEST-PN-001"
        )
        assert info.serial_number == "SN12345"
        assert info.part_number == "TEST-PN-001"
        assert info.status == UnitStatus.UNKNOWN
    
    def test_unit_info_with_all_fields(self):
        """Test unit info with all fields populated."""
        info = UnitInfo(
            serial_number="SN12345",
            part_number="TEST-PN-001",
            revision="A",
            status=UnitStatus.PASSING,
            status_reason="All tests passed",
            test_summary=TestSummary(total_tests=10, passed=10),
            production=ProductionInfo(has_production_unit=True, phase="Finalized"),
            warnings=["Test warning"]
        )
        assert info.status == UnitStatus.PASSING
        assert info.test_summary.pass_rate == 100.0
        assert info.production.phase == "Finalized"
        assert len(info.warnings) == 1


# =============================================================================
# Test UnitAnalysisInput Model
# =============================================================================

class TestUnitAnalysisInput:
    """Tests for UnitAnalysisInput model."""
    
    def test_minimal_input(self):
        """Test minimal required input."""
        input = UnitAnalysisInput(serial_number="SN12345")
        assert input.serial_number == "SN12345"
        assert input.part_number is None
        assert input.scope == AnalysisScope.STANDARD
    
    def test_full_input(self):
        """Test fully specified input."""
        input = UnitAnalysisInput(
            serial_number="SN12345",
            part_number="TEST-PN-001",
            scope=AnalysisScope.FULL,
            include_sub_units=True,
            max_history=100
        )
        assert input.part_number == "TEST-PN-001"
        assert input.scope == AnalysisScope.FULL
        assert input.include_sub_units is True
        assert input.max_history == 100


# =============================================================================
# Test UnitAnalysisTool
# =============================================================================

class TestUnitAnalysisTool:
    """Tests for UnitAnalysisTool class."""
    
    def test_tool_instantiation(self, tool):
        """Test tool can be instantiated."""
        assert tool is not None
        assert tool.name == "analyze_unit"
    
    def test_tool_has_description(self, tool):
        """Tool should have a description."""
        assert tool.description
        assert len(tool.description) > 50
        assert "unit" in tool.description.lower()
    
    def test_tool_description_mentions_serial_number(self, tool):
        """Description should mention serial number."""
        assert "serial" in tool.description.lower()
    
    def test_tool_description_mentions_verification(self, tool):
        """Description should mention verification."""
        assert "verif" in tool.description.lower()
    
    def test_tool_description_mentions_sub_units(self, tool):
        """Description should mention sub-units."""
        assert "sub" in tool.description.lower()


class TestUnitAnalysisToolDefinition:
    """Tests for tool definition."""
    
    def test_get_definition(self, tool):
        """Test getting tool definition."""
        definition = tool.get_definition()
        assert definition is not None
        assert "name" in definition
        assert definition["name"] == "analyze_unit"
    
    def test_definition_has_parameters(self, tool):
        """Definition should have parameters."""
        definition = tool.get_definition()
        assert "parameters" in definition
        params = definition["parameters"]
        assert "properties" in params
    
    def test_definition_requires_serial_number(self, tool):
        """Serial number should be required."""
        definition = tool.get_definition()
        params = definition["parameters"]
        assert "serial_number" in params["properties"]
        assert "serial_number" in params.get("required", [])


class TestUnitAnalysisToolExecution:
    """Tests for tool execution."""
    
    def test_execute_no_history_no_part_number(self, tool, mock_api):
        """Should return error when no history and no part number."""
        result = tool.execute({"serial_number": "UNKNOWN-SN"})
        assert result.success is False
        assert "No test history" in (result.error or result.summary)
    
    def test_execute_with_history(self, tool, mock_api, mock_report_header):
        """Should analyze unit when history exists."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        result = tool.execute({
            "serial_number": "SN12345",
            "scope": "quick"
        })
        
        assert result.success is True
        assert result.data is not None
        assert result.data["serial_number"] == "SN12345"
    
    def test_execute_infers_part_number(self, tool, mock_api, mock_report_header):
        """Should infer part number from history."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        assert result.data["part_number"] == "TEST-PN-001"
        assert any("inferred" in w.lower() for w in result.data["warnings"])
    
    def test_execute_builds_test_summary(self, tool, mock_api, mock_report_header):
        """Should build test summary from history."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        summary = result.data["test_summary"]
        assert summary["total_tests"] == 1
        assert summary["passed"] == 1
    
    def test_execute_quick_scope(self, tool, mock_api, mock_report_header):
        """Quick scope should still work."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        result = tool.execute({
            "serial_number": "SN12345",
            "scope": "quick"
        })
        
        assert result.success is True
        assert result.summary is not None


class TestUnitStatusDetermination:
    """Tests for status determination logic."""
    
    def test_status_passing_all_tests(self, tool, mock_api):
        """Should determine passing when all tests pass."""
        header = Mock()
        header.part_number = "TEST-PN-001"
        header.revision = "A"
        header.status = "P"
        header.start = datetime.now()
        header.process_name = "ICT"
        header.station_name = "Station_01"
        
        mock_api.analytics.get_serial_number_history.return_value = [header]
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        assert result.data["status"] == "passing"
    
    def test_status_failing_last_test_failed(self, tool, mock_api):
        """Should determine failing when last test failed."""
        header = Mock()
        header.part_number = "TEST-PN-001"
        header.revision = "A"
        header.status = "F"
        header.start = datetime.now()
        header.process_name = "ICT"
        header.station_name = "Station_01"
        
        mock_api.analytics.get_serial_number_history.return_value = [header]
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        assert result.data["status"] == "failing"


class TestProductionInfo:
    """Tests for production info retrieval."""
    
    def test_production_info_retrieved(self, tool, mock_api, mock_report_header):
        """Should retrieve production info when available."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        # Setup production unit - use None for datetime fields to avoid serialization issues
        prod_unit = Mock()
        prod_unit.unit_phase = "Finalized"
        prod_unit.unit_phase_id = 16
        prod_unit.batch_number = "BATCH-001"
        prod_unit.current_location = None
        prod_unit.serial_date = None
        prod_unit.parent_serial_number = None
        prod_unit.sub_units = []
        mock_api.production.get_unit.return_value = prod_unit
        mock_api.production.get_unit_grade.return_value = None
        
        result = tool.execute({
            "serial_number": "SN12345",
            "scope": "standard"
        })
        
        assert result.success is True
        prod = result.data["production"]
        assert prod["has_production_unit"] is True
        assert prod["phase"] == "Finalized"
        assert prod["batch_number"] == "BATCH-001"
    
    def test_production_info_not_available(self, tool, mock_api, mock_report_header):
        """Should handle missing production info gracefully."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        mock_api.production.get_unit.return_value = None
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        prod = result.data["production"]
        assert prod["has_production_unit"] is False


class TestVerificationGrade:
    """Tests for verification grade retrieval."""
    
    def test_verification_with_rules(self, tool, mock_api, mock_report_header):
        """Should retrieve verification grade when rules exist."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        # Setup verification grade
        grade = Mock()
        grade.status = "Passed"
        grade.grade = "A"
        grade.all_processes_executed_in_correct_order = True
        grade.all_processes_passed_first_run = True
        grade.all_processes_passed_any_run = True
        grade.all_processes_passed_last_run = True
        grade.no_repairs = True
        grade.results = []
        mock_api.production.get_unit_grade.return_value = grade
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        verification = result.data["verification"]
        assert verification["has_rules"] is True
        assert verification["grade"] == "A"
        assert verification["all_passed_first_run"] is True
    
    def test_verification_no_rules(self, tool, mock_api, mock_report_header):
        """Should indicate when no verification rules exist."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        mock_api.production.get_unit_grade.return_value = None
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        verification = result.data["verification"]
        assert verification["has_rules"] is False
        assert "rule_suggestion" in verification


class TestSubUnitRetrieval:
    """Tests for sub-unit retrieval."""
    
    def test_sub_units_from_production(self, tool, mock_api, mock_report_header):
        """Should retrieve sub-units from production unit."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        mock_api.production.get_unit_grade.return_value = None
        
        # Setup production unit with sub-units
        prod_unit = Mock()
        prod_unit.unit_phase = None
        prod_unit.unit_phase_id = None
        prod_unit.batch_number = None
        prod_unit.current_location = None
        prod_unit.serial_date = None
        prod_unit.parent_serial_number = None
        sub = Mock()
        sub.serial_number = "SUB-001"
        sub.part_number = "SUB-PN"
        sub.revision = "1.0"
        prod_unit.sub_units = [sub]
        mock_api.production.get_unit.return_value = prod_unit
        
        result = tool.execute({
            "serial_number": "SN12345",
            "scope": "full"
        })
        
        assert result.success is True
        sub_units = result.data["sub_units"]
        assert len(sub_units) >= 1


class TestSummaryGeneration:
    """Tests for summary generation."""
    
    def test_summary_includes_status(self, tool, mock_api, mock_report_header):
        """Summary should include status."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        assert result.summary is not None
        assert "SN12345" in result.summary
    
    def test_summary_includes_test_count(self, tool, mock_api, mock_report_header):
        """Summary should include test count."""
        mock_api.analytics.get_serial_number_history.return_value = [mock_report_header]
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        # Check for test-related info in summary
        assert "Test" in result.summary or "test" in result.summary


# =============================================================================
# Test Tool Registration
# =============================================================================

class TestToolRegistration:
    """Tests for tool registration."""
    
    def test_tool_in_registry(self):
        """Unit tool should be discoverable in registry."""
        from pywats_agent.tools._registry import get_tool
        
        tool_cls = get_tool("analyze_unit")
        assert tool_cls is not None
        assert tool_cls == UnitAnalysisTool
    
    def test_tool_in_full_profile(self):
        """Unit tool should be in full profile."""
        from pywats_agent.tools.variants import PROFILES
        
        full_profile = PROFILES["full"]
        assert "analyze_unit" in full_profile.tools
    
    def test_tool_has_unit_profile(self):
        """Should have a unit-focused profile."""
        from pywats_agent.tools.variants import PROFILES
        
        assert "unit" in PROFILES
        unit_profile = PROFILES["unit"]
        assert "analyze_unit" in unit_profile.tools


# =============================================================================
# Test Edge Cases
# =============================================================================

class TestEdgeCases:
    """Tests for edge cases."""
    
    def test_empty_serial_number_handled(self, tool):
        """Should handle empty serial number gracefully."""
        result = tool.execute({"serial_number": ""})
        # Should return an error result rather than crash
        assert result.success is False or result.data.get("test_summary", {}).get("total_tests", 0) == 0
    
    def test_multiple_report_headers(self, tool, mock_api):
        """Should handle multiple report headers."""
        headers = []
        for i in range(10):
            h = Mock()
            h.part_number = "TEST-PN-001"
            h.revision = "A"
            h.status = "P" if i % 2 == 0 else "F"
            h.start = datetime.now() - timedelta(days=i)
            h.process_name = "ICT"
            h.station_name = f"Station_{i % 3:02d}"
            headers.append(h)
        
        mock_api.analytics.get_serial_number_history.return_value = headers
        
        result = tool.execute({"serial_number": "SN12345"})
        
        assert result.success is True
        summary = result.data["test_summary"]
        assert summary["total_tests"] == 10
        assert summary["passed"] == 5
        assert summary["failed"] == 5
    
    def test_api_exception_handling(self, tool, mock_api):
        """Should handle API exceptions gracefully."""
        mock_api.analytics.get_serial_number_history.side_effect = Exception("API Error")
        mock_api.analytics.get_uut_reports.return_value = []
        
        result = tool.execute({
            "serial_number": "SN12345",
            "part_number": "TEST-PN"
        })
        
        # Should not raise, should return error result or empty
        assert result is not None
