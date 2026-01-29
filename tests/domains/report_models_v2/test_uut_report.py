"""
Unit tests for UUTReport v2 (composition-based)

Tests:
- Parent injection mechanism (StepList from v1)
- Constructor and factory patterns
- Step hierarchy integration
- Serialization compatibility with v1
"""

import pytest
from datetime import datetime

from pywats.domains.report.report_models_v2.uut_report import UUTReport
from pywats.domains.report.report_models_v2.report_common import ReportCommon


class TestUUTReportCreation:
    """Test different ways to create UUTReport."""
    
    def test_create_with_explicit_common(self):
        """Test creating UUTReport with explicit ReportCommon."""
        common = ReportCommon(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        report = UUTReport(common=common)
        
        assert report.type == "T"
        assert report.common.pn == "ABC123"
        assert report.common.sn == "SN-001"
        assert report.root is not None
    
    def test_create_with_factory_method(self):
        """Test creating UUTReport with factory method."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        assert report.type == "T"
        assert report.common.pn == "ABC123"
        assert report.common.sn == "SN-001"
        assert report.root is not None


class TestUUTReportStepHierarchy:
    """Test Step hierarchy integration (imported from v1)."""
    
    def test_get_root_sequence_call(self):
        """Test getting root sequence call."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        root = report.get_root_sequence_call()
        
        assert root is not None
        assert root.name == "MainSequence Callback"
        assert root == report.root  # Same object
    
    def test_add_numeric_step(self):
        """Test adding a numeric step."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        root = report.get_root_sequence_call()
        step = root.add_numeric_step(
            name="Voltage",
            value=3.3,
            unit="V",
            low_limit=3.0,
            high_limit=3.6
        )
        
        assert step.name == "Voltage"
        assert len(root.steps) == 1
        assert root.steps[0] == step
    
    def test_parent_injection_works(self):
        """Test that parent injection still works (from v1 StepList)."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        root = report.get_root_sequence_call()
        
        # Add a child sequence
        child_seq = root.add_sequence_call(name="SubSequence")
        
        # Add a step to the child sequence
        step = child_seq.add_numeric_step(
            name="Test",
            value=10.0
        )
        
        # Parent should be injected by StepList
        assert step.parent == child_seq
        assert child_seq.parent == root
    
    def test_nested_sequences(self):
        """Test nested sequence calls with parent injection."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        root = report.get_root_sequence_call()
        
        # Create nested structure: root -> level1 -> level2 -> step
        level1 = root.add_sequence_call(name="Level1")
        level2 = level1.add_sequence_call(name="Level2")
        step = level2.add_numeric_step(name="DeepTest", value=5.0)
        
        # Verify parent chain
        assert step.parent == level2
        assert level2.parent == level1
        assert level1.parent == root


class TestUUTReportSerialization:
    """Test serialization for v1 compatibility."""
    
    def test_serialization_flattens_common(self):
        """Test that serialization flattens common fields to top level."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        data = report.model_dump(by_alias=True)
        
        # Common fields should be at top level (flattened)
        assert "pn" in data
        assert "sn" in data
        assert "processCode" in data
        assert "machineName" in data
        
        # Should NOT have nested common
        assert "common" not in data
        
        # UUT-specific fields
        assert "type" in data
        assert data["type"] == "T"
        assert "root" in data
    
    def test_deserialization_handles_flat_format(self):
        """Test that deserialization handles v1 flat format."""
        flat_data = {
            "pn": "ABC123",
            "sn": "SN-001",
            "rev": "A",
            "processCode": 100,
            "machineName": "Station1",
            "location": "TestLab",
            "purpose": "Development",
            "type": "T"
        }
        
        report = UUTReport.model_validate(flat_data)
        
        assert report.type == "T"
        assert report.common.pn == "ABC123"
        assert report.common.sn == "SN-001"
        assert report.common.process_code == 100
    
    def test_roundtrip_serialization(self):
        """Test that roundtrip serialization preserves data."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        root = report.get_root_sequence_call()
        root.add_numeric_step(name="Voltage", value=3.3, unit="V")
        
        # Serialize
        json_str = report.model_dump_json(by_alias=True)
        
        # Deserialize
        report2 = UUTReport.model_validate_json(json_str)
        
        assert report2.common.pn == report.common.pn
        assert report2.type == report.type
        assert len(report2.root.steps) == len(report.root.steps)


class TestUUTReportHelperMethods:
    """Test helper methods delegated to common."""
    
    def test_add_misc_info_via_common(self):
        """Test adding misc info through common."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        report.common.add_misc_info("Operator", "John Doe")
        
        assert len(report.common.misc_infos) == 1
        assert report.common.misc_infos[0].description == "Operator"
    
    def test_add_sub_unit_via_common(self):
        """Test adding sub-unit through common."""
        report = UUTReport.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="Station1",
            location="TestLab",
            purpose="Development"
        )
        
        report.common.add_sub_unit("PCB", "PCB-001", "PCB-ABC", "1.0")
        
        assert len(report.common.sub_units) == 1
        assert report.common.sub_units[0].part_type == "PCB"
