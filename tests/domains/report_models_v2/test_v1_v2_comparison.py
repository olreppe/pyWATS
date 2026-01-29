"""
V1 vs V2 Comparison Testing Framework

Validates that report_models_v2 produces identical JSON output to report_models (v1).

This is critical for backward compatibility - v2 must serialize to the exact
same JSON structure as v1 to ensure existing systems continue to work.
"""

import pytest
import json
from uuid import uuid4
from datetime import datetime, timezone

# V1 imports
from pywats.domains.report.report_models.uut.uut_report import UUTReport as UUTReportV1
from pywats.domains.report.report_models.uur.uur_report import UURReport as UURReportV1

# V2 imports
from pywats.domains.report.report_models_v2.uut_report import UUTReport as UUTReportV2
from pywats.domains.report.report_models_v2.uur_report import UURReport as UURReportV2


def normalize_json(obj: dict) -> dict:
    """
    Normalize JSON for comparison.
    
    Handles:
    - None vs missing fields
    - Empty lists vs missing lists
    - UUID string formatting
    - Datetime formatting
    """
    if not isinstance(obj, dict):
        return obj
    
    result = {}
    for key, value in obj.items():
        # Skip None values
        if value is None:
            continue
        
        # Skip empty lists (treat same as missing)
        if isinstance(value, list) and len(value) == 0:
            continue
        
        # Recursively normalize nested dicts
        if isinstance(value, dict):
            normalized = normalize_json(value)
            if normalized:  # Only include non-empty dicts
                result[key] = normalized
        
        # Recursively normalize lists of dicts
        elif isinstance(value, list):
            result[key] = [normalize_json(item) if isinstance(item, dict) else item for item in value]
        
        else:
            result[key] = value
    
    return result


def compare_json_outputs(v1_json: str, v2_json: str, ignore_fields: list[str] | None = None) -> tuple[bool, str]:
    """
    Compare JSON outputs from v1 and v2 reports.
    
    Args:
        v1_json: JSON string from v1 report
        v2_json: JSON string from v2 report
        ignore_fields: Fields to ignore in comparison (e.g., timestamps)
        
    Returns:
        Tuple of (is_equal, difference_message)
    """
    ignore_fields = ignore_fields or []
    
    v1_data = json.loads(v1_json)
    v2_data = json.loads(v2_json)
    
    # Remove ignored fields
    for field in ignore_fields:
        v1_data.pop(field, None)
        v2_data.pop(field, None)
    
    # Normalize both
    v1_normalized = normalize_json(v1_data)
    v2_normalized = normalize_json(v2_data)
    
    if v1_normalized == v2_normalized:
        return True, ""
    
    # Generate diff message
    v1_keys = set(v1_normalized.keys())
    v2_keys = set(v2_normalized.keys())
    
    missing_in_v2 = v1_keys - v2_keys
    extra_in_v2 = v2_keys - v1_keys
    
    diff_lines = []
    
    if missing_in_v2:
        diff_lines.append(f"Missing in v2: {missing_in_v2}")
    
    if extra_in_v2:
        diff_lines.append(f"Extra in v2: {extra_in_v2}")
    
    for key in v1_keys & v2_keys:
        if v1_normalized[key] != v2_normalized[key]:
            diff_lines.append(f"Diff in '{key}':")
            diff_lines.append(f"  v1: {v1_normalized[key]}")
            diff_lines.append(f"  v2: {v2_normalized[key]}")
    
    return False, "\n".join(diff_lines)


class TestUUTReportComparison:
    """Compare UUTReport v1 vs v2 JSON output."""
    
    def test_minimal_uut_report(self):
        """Test minimal UUT report produces identical JSON."""
        # Create v1 report
        v1 = UUTReportV1(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="TestStation",
            location="Lab",
            purpose="Test"
        )
        
        # Create matching v2 report
        v2 = UUTReportV2.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=100,
            station_name="TestStation",
            location="Lab",
            purpose="Test"
        )
        
        # Match IDs for comparison
        v2.common.id = v1.id
        
        # Serialize both
        v1_json = v1.model_dump_json()
        v2_json = v2.model_dump_json()
        
        # Compare (ignore timestamps as they differ)
        is_equal, diff = compare_json_outputs(
            v1_json, 
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"JSON outputs differ:\n{diff}"
    
    def test_uut_with_steps(self):
        """Test UUT report with sequence call produces identical JSON."""
        from pywats.domains.report.report_models.uut.steps.sequence_call import SequenceCall
        
        # Create v1 report
        v1 = UUTReportV1(
            pn="BOARD-X",
            sn="B-001",
            rev="2.0",
            process_code=100,
            station_name="TestStation",
            location="Lab",
            purpose="Test"
        )
        
        # Add sequence call (v1 uses 'root' field)
        seq_v1 = SequenceCall(name="MainSequence")
        v1.root = seq_v1
        
        # Create matching v2 report
        v2 = UUTReportV2.create(
            pn="BOARD-X",
            sn="B-001",
            rev="2.0",
            process_code=100,
            station_name="TestStation",
            location="Lab",
            purpose="Test"
        )
        
        # Add sequence call (v2 also uses 'root')
        seq_v2 = SequenceCall(name="MainSequence")
        v2.root = seq_v2
        
        # Match IDs
        v2.common.id = v1.id
        
        # Serialize
        v1_json = v1.model_dump_json()
        v2_json = v2.model_dump_json()
        
        # Compare
        is_equal, diff = compare_json_outputs(
            v1_json,
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"JSON outputs differ:\n{diff}"
    
    def test_uut_with_result_and_misc_info(self):
        """Test UUT with result and misc info."""
        from pywats.domains.report.report_models.misc_info import MiscInfo
        
        # Create v1 (result is string in v1: "P"=Pass, "F"=Fail, etc.)
        v1 = UUTReportV1(
            pn="PART",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test",
            result="P"  # v1 uses string format
        )
        
        # Add misc info (v1 and v2 both take 2 args: description, value)
        v1.add_misc_info("Temperature", "25.5")
        v1.add_misc_info("Voltage", "5.0")
        
        # Create v2
        v2 = UUTReportV2.create(
            pn="PART",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test"
        )
        v2.common.result = "P"  # Match v1 string format
        
        # Add misc info (same signature as v1)
        v2.common.add_misc_info("Temperature", "25.5")
        v2.common.add_misc_info("Voltage", "5.0")
        
        # Match IDs
        v2.common.id = v1.id
        
        # Serialize
        v1_json = v1.model_dump_json()
        v2_json = v2.model_dump_json()
        
        # Compare
        is_equal, diff = compare_json_outputs(
            v1_json,
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"JSON outputs differ:\n{diff}"


class TestUURReportComparison:
    """Compare UURReport v1 vs v2 JSON output."""
    
    def test_minimal_uur_report(self):
        """Test minimal UUR report produces identical JSON."""
        from pywats.domains.report.report_models.uur.uur_info import UURInfo
        
        # Create v1 report (provide uur_info in constructor)
        uur_info_v1 = UURInfo(operator="John Doe", test_operation_code=100)
        v1 = UURReportV1(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            process_code=500,
            station_name="RepairStation",
            location="Lab",
            purpose="Repair",
            uur_info=uur_info_v1
        )
        
        # Create matching v2 report
        v2 = UURReportV2.create(
            pn="ABC123",
            sn="SN-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="RepairStation",
            location="Lab",
            purpose="Repair",
            operator="John Doe"
        )
        
        # Match IDs
        v2.common.id = v1.id
        
        # Serialize both
        v1_json = v1.model_dump_json()
        v2_json = v2.model_dump_json()
        
        # Compare (ignore timestamps)
        is_equal, diff = compare_json_outputs(
            v1_json,
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"JSON outputs differ:\n{diff}"
    
    def test_uur_with_dual_process_codes(self):
        """Test UUR with dual process code architecture."""
        from pywats.domains.report.report_models.uur.uur_info import UURInfo
        
        # Create v1 (provide uur_info in constructor)
        uur_info_v1 = UURInfo(
            operator="Jane Doe",
            test_operation_code=100,  # Original test code
            comment="Replaced capacitor"
        )
        v1 = UURReportV1(
            pn="BOARD",
            sn="B-001",
            rev="1.0",
            process_code=500,  # Repair code
            station_name="RepairStation",
            location="Lab",
            purpose="Repair",
            uur_info=uur_info_v1
        )
        
        # Create v2
        v2 = UURReportV2.create(
            pn="BOARD",
            sn="B-001",
            rev="1.0",
            repair_process_code=500,
            test_operation_code=100,
            station_name="RepairStation",
            location="Lab",
            purpose="Repair",
            operator="Jane Doe",
            comment="Replaced capacitor"
        )
        
        # Match IDs
        v2.common.id = v1.id
        
        # Serialize
        v1_json = v1.model_dump_json()
        v2_json = v2.model_dump_json()
        
        # Compare
        is_equal, diff = compare_json_outputs(
            v1_json,
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"JSON outputs differ:\n{diff}"
    
    def test_uur_with_sub_units_and_failures(self):
        """Test UUR with sub-units and failures."""
        from pywats.domains.report.report_models.uur.uur_info import UURInfo
        
        # Create v1 (provide uur_info in constructor)
        uur_info_v1 = UURInfo(operator="Bob", test_operation_code=100)
        v1 = UURReportV1(
            pn="MAIN",
            sn="M-001",
            rev="A",
            process_code=500,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            uur_info=uur_info_v1
        )
        
        # Add failure to main unit
        main_v1 = v1.get_main_unit()
        main_v1.add_failure(category="Component", code="CAP_FAIL")
        
        # Create v2
        v2 = UURReportV2.create(
            pn="MAIN",
            sn="M-001",
            rev="A",
            repair_process_code=500,
            test_operation_code=100,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            operator="Bob"
        )
        
        # Add failure to main unit
        main_v2 = v2.get_main_unit()
        main_v2.add_failure(category="Component", code="CAP_FAIL")
        
        # Match IDs
        v2.common.id = v1.id
        
        # Serialize
        v1_json = v1.model_dump_json()
        v2_json = v2.model_dump_json()
        
        # Compare
        is_equal, diff = compare_json_outputs(
            v1_json,
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"JSON outputs differ:\n{diff}"


class TestDeserializationCompatibility:
    """Test that v2 can deserialize v1 JSON output."""
    
    def test_v2_can_parse_v1_uut_json(self):
        """Test that v2 UUTReport can parse v1 JSON."""
        # Create v1 report
        v1 = UUTReportV1(
            pn="PART",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test",
            result="P"  # v1 uses string
        )
        
        # Serialize v1
        v1_json = v1.model_dump_json()
        
        # Parse with v2
        v2 = UUTReportV2.model_validate_json(v1_json)
        
        # Verify fields
        assert v2.common.pn == v1.pn
        assert v2.common.sn == v1.sn
        assert v2.common.rev == v1.rev
        assert v2.common.process_code == v1.process_code
        assert v2.common.result == v1.result
        assert v2.type == "T"
    
    def test_v2_can_parse_v1_uur_json(self):
        """Test that v2 UURReport can parse v1 JSON."""
        from pywats.domains.report.report_models.uur.uur_info import UURInfo
        
        # Create v1 report (provide uur_info in constructor)
        uur_info_v1 = UURInfo(
            operator="Alice",
            test_operation_code=100,
            comment="Fixed issue"
        )
        v1 = UURReportV1(
            pn="PART",
            sn="001",
            rev="A",
            process_code=500,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            uur_info=uur_info_v1
        )
        
        # Serialize v1
        v1_json = v1.model_dump_json()
        
        # Parse with v2
        v2 = UURReportV2.model_validate_json(v1_json)
        
        # Verify fields
        assert v2.common.pn == v1.pn
        assert v2.common.sn == v1.sn
        assert v2.common.process_code == v1.process_code
        assert v2.uur_info.operator == v1.uur_info.operator
        assert v2.uur_info.test_operation_code == v1.uur_info.test_operation_code
        assert v2.uur_info.comment == v1.uur_info.comment
        assert v2.type == "R"


class TestRoundtripCompatibility:
    """Test v1 → v2 → v1 roundtrip."""
    
    def test_uut_roundtrip(self):
        """Test UUT v1 → serialize → v2 parse → serialize → compare."""
        # Create v1
        v1_original = UUTReportV1(
            pn="PART",
            sn="001",
            rev="A",
            process_code=100,
            station_name="Station",
            location="Lab",
            purpose="Test",
            result="P"  # v1 uses string
        )
        
        # v1 → JSON
        v1_json = v1_original.model_dump_json()
        
        # JSON → v2
        v2 = UUTReportV2.model_validate_json(v1_json)
        
        # v2 → JSON
        v2_json = v2.model_dump_json()
        
        # Compare JSONs (should be identical)
        is_equal, diff = compare_json_outputs(
            v1_json,
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"Roundtrip failed:\n{diff}"
    
    def test_uur_roundtrip(self):
        """Test UUR v1 → serialize → v2 parse → serialize → compare."""
        from pywats.domains.report.report_models.uur.uur_info import UURInfo
        
        # Create v1 (provide uur_info in constructor)
        uur_info_v1 = UURInfo(operator="Bob", test_operation_code=100)
        v1_original = UURReportV1(
            pn="PART",
            sn="001",
            rev="A",
            process_code=500,
            station_name="Station",
            location="Lab",
            purpose="Repair",
            uur_info=uur_info_v1
        )
        
        # v1 → JSON
        v1_json = v1_original.model_dump_json()
        
        # JSON → v2
        v2 = UURReportV2.model_validate_json(v1_json)
        
        # v2 → JSON
        v2_json = v2.model_dump_json()
        
        # Compare
        is_equal, diff = compare_json_outputs(
            v1_json,
            v2_json,
            ignore_fields=['start', 'startUTC', 'start_utc']
        )
        
        assert is_equal, f"Roundtrip failed:\n{diff}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
