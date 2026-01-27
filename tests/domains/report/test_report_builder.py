"""
Tests for ReportBuilder

Validates that the simple report builder creates correct WATS reports.
"""

import pytest
from datetime import datetime

from pywats.tools.report_builder import ReportBuilder, quick_report
from pywats.shared.enums import CompOp


class TestReportBuilder:
    """Test ReportBuilder functionality"""
    
    def test_simple_report(self):
        """Test creating a simple flat report"""
        builder = ReportBuilder(
            part_number="TEST-PN",
            serial_number="TEST-SN"
        )
        
        builder.add_step("Voltage", 5.0, unit="V", low_limit=4.5, high_limit=5.5)
        builder.add_step("Current", 1.2, unit="A")
        builder.add_step("Status", True)
        
        report = builder.build()
        
        # Verify header
        assert report.pn == "TEST-PN"
        assert report.sn == "TEST-SN"
        assert report.result == "P"  # All passed
        
        # Verify root sequence exists
        root = report.get_root_sequence_call()
        assert root is not None
        assert len(root.steps) == 3
    
    def test_grouped_report(self):
        """Test creating a hierarchical report with groups"""
        builder = ReportBuilder("PN", "SN")
        
        builder.add_step("VCC", 3.3, unit="V", group="Power")
        builder.add_step("VDD", 1.8, unit="V", group="Power")
        builder.add_step("UART", True, group="Communication")
        
        report = builder.build()
        root = report.get_root_sequence_call()
        
        # Should have 2 sequences (Power, Communication)
        sequences = [s for s in root.steps if hasattr(s, 'steps')]
        assert len(sequences) == 2
    
    def test_auto_type_inference(self):
        """Test that step types are inferred correctly"""
        builder = ReportBuilder("PN", "SN")
        
        builder.add_step("Boolean", True)
        builder.add_step("Numeric", 5.0)
        builder.add_step("String", "ABC")
        builder.add_step("MultiNumeric", [1.0, 2.0, 3.0])
        
        report = builder.build()
        root = report.get_root_sequence_call()
        
        assert len(root.steps) == 4
    
    def test_auto_status_calculation(self):
        """Test that pass/fail is calculated from limits"""
        builder = ReportBuilder("PN", "SN")
        
        # In range = pass
        builder.add_step("Pass", 5.0, low_limit=4.0, high_limit=6.0)
        
        # Out of range = fail
        builder.add_step("Fail", 10.0, low_limit=4.0, high_limit=6.0)
        
        report = builder.build()
        
        # Overall should be fail
        assert report.result == "F"
    
    def test_status_normalization(self):
        """Test that various status formats are normalized"""
        builder = ReportBuilder("PN", "SN")
        
        builder.add_step("Test1", 5.0, status="PASS")
        builder.add_step("Test2", 5.0, status="P")
        builder.add_step("Test3", 5.0, status="Passed")
        builder.add_step("Test4", 5.0, status=True)
        builder.add_step("Test5", 5.0, status="FAIL")
        
        report = builder.build()
        
        # Should build successfully (status normalized)
        assert report is not None
    
    def test_string_limit_conversion(self):
        """Test that string limits are converted to floats"""
        builder = ReportBuilder("PN", "SN")
        
        # Limits as strings
        builder.add_step("Test", "5.0", low_limit="4.5", high_limit="5.5")
        
        report = builder.build()
        root = report.get_root_sequence_call()
        
        # Should work without errors
        assert len(root.steps) == 1
    
    def test_add_step_from_dict(self):
        """Test adding steps from dictionaries"""
        builder = ReportBuilder("PN", "SN")
        
        test_dict = {
            "name": "Voltage",
            "value": 5.0,
            "unit": "V",
            "low_limit": 4.5,
            "high_limit": 5.5
        }
        
        builder.add_step_from_dict(test_dict)
        
        report = builder.build()
        root = report.get_root_sequence_call()
        
        assert len(root.steps) == 1
    
    def test_flexible_dict_keys(self):
        """Test that various dictionary key names work"""
        builder = ReportBuilder("PN", "SN")
        
        # Different key names
        test_dict = {
            "TestName": "Voltage",
            "MeasuredValue": 5.0,
            "Unit": "V"
        }
        
        builder.add_step_from_dict(test_dict)
        
        report = builder.build()
        assert report is not None
    
    def test_misc_info(self):
        """Test adding misc info"""
        builder = ReportBuilder("PN", "SN")
        
        builder.add_misc_info("Operator", "John Doe")
        builder.add_misc_info("Batch", "BATCH-001")
        
        report = builder.build()
        
        assert len(report.misc_infos) == 2
    
    def test_sub_units(self):
        """Test adding sub-units"""
        builder = ReportBuilder("PN", "SN")
        
        builder.add_sub_unit(
            part_type="CPU",
            part_number="CPU-001",
            serial_number="CPU-SN-001"
        )
        
        report = builder.build()
        
        assert len(report.sub_units) == 1
        assert report.sub_units[0].part_type == "CPU"
    
    def test_method_chaining(self):
        """Test that methods return self for chaining"""
        builder = ReportBuilder("PN", "SN")
        
        result = (builder
                  .add_step("Test1", 5.0)
                  .add_step("Test2", True)
                  .add_misc_info("Key", "Value"))
        
        assert result is builder
    
    def test_quick_report_function(self):
        """Test the quick_report convenience function"""
        steps = [
            {"name": "Voltage", "value": 5.0, "unit": "V"},
            {"name": "Current", "value": 1.2, "unit": "A"},
            {"name": "Status", "value": True}
        ]
        
        report = quick_report(
            part_number="QUICK-PN",
            serial_number="QUICK-SN",
            steps=steps
        )
        
        assert report.pn == "QUICK-PN"
        assert report.sn == "QUICK-SN"
        
        root = report.get_root_sequence_call()
        assert len(root.steps) == 3
    
    def test_explicit_result_override(self):
        """Test that explicit result overrides auto-calculation"""
        builder = ReportBuilder("PN", "SN", result="P")
        
        # Add a failing test
        builder.add_step("Fail", 10.0, low_limit=4.0, high_limit=6.0)
        
        report = builder.build()
        
        # Explicit result should override
        assert report.result == "P"
    
    def test_empty_report(self):
        """Test building a report with no steps"""
        builder = ReportBuilder("PN", "SN")
        
        report = builder.build()
        
        assert report.pn == "PN"
        assert report.sn == "SN"
        assert report.result == "P"  # Default
        
        root = report.get_root_sequence_call()
        assert len(root.steps) == 0
    
    def test_multi_value_steps(self):
        """Test multi-value step types"""
        builder = ReportBuilder("PN", "SN")
        
        builder.add_step("MultiNumeric", [1.0, 2.0, 3.0], unit="V")
        builder.add_step("MultiBool", [True, True, False])
        builder.add_step("MultiString", ["A", "B", "C"])
        
        report = builder.build()
        root = report.get_root_sequence_call()
        
        assert len(root.steps) == 3
    
    def test_comparison_operator_inference(self):
        """Test that comparison operators are inferred correctly"""
        builder = ReportBuilder("PN", "SN")
        
        # Both limits = GELE
        builder.add_step("Test1", 5.0, low_limit=4.0, high_limit=6.0)
        
        # Only low limit = GE
        builder.add_step("Test2", 5.0, low_limit=4.0)
        
        # Only high limit = LE
        builder.add_step("Test3", 5.0, high_limit=6.0)
        
        # No limits = LOG
        builder.add_step("Test4", 5.0)
        
        report = builder.build()
        
        # Should build successfully with correct operators
        assert report is not None


class TestReportBuilderEdgeCases:
    """Test edge cases and error handling"""
    
    def test_missing_required_fields(self):
        """Test that missing required fields raise errors"""
        with pytest.raises(TypeError):
            ReportBuilder()  # Missing part_number and serial_number
    
    def test_none_values(self):
        """Test handling of None values"""
        builder = ReportBuilder("PN", "SN")
        
        builder.add_step("Test", None)  # None value
        
        report = builder.build()
        
        # Should create a string step with "N/A"
        assert report is not None
    
    def test_invalid_dict_keys(self):
        """Test that missing name in dict raises error"""
        builder = ReportBuilder("PN", "SN")
        
        bad_dict = {"value": 5.0}  # Missing name
        
        with pytest.raises(ValueError, match="Could not find step name"):
            builder.add_step_from_dict(bad_dict)
    
    def test_mixed_types_in_list(self):
        """Test handling of mixed types in list values"""
        builder = ReportBuilder("PN", "SN")
        
        # First element determines type
        builder.add_step("Test", [1.0, 2.0, 3.0])  # Numeric
        
        report = builder.build()
        assert report is not None


class TestReportBuilderIntegration:
    """Integration tests with actual report submission (requires API)"""
    
    @pytest.mark.skip(reason="Requires live WATS server")
    def test_submit_simple_report(self):
        """Test submitting a simple report (integration test)"""
        from pywats import pyWATS
        
        api = pyWATS(
            base_url="https://your-server.com",
            token="your-token"
        )
        
        builder = ReportBuilder(
            part_number="TEST-PN",
            serial_number="TEST-SN-001"
        )
        
        builder.add_step("Voltage", 5.0, unit="V", low_limit=4.5, high_limit=5.5)
        builder.add_step("Status", True)
        
        report = builder.build()
        response = api.report.submit_report(report)
        
        assert response.id is not None
