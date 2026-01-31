"""
Report Model Roundtrip Test - V1 vs V3 Comparison

This test validates that V1 and V3 report models can:
1. Deserialize original WSJF JSON files using Pydantic model_validate
2. Submit reports to WATS API
3. Load reports back from server
4. Compare loaded data against original to find information loss

Test Workflow:
1. Load original JSON report
2. Deserialize directly into UUTReport using model_validate (V1 and V3 separately)
3. Modify: new UUID, append to serial number, set new start time
4. Submit via api.report.submit_report()
5. Wait for server processing
6. Load report back using the GUID
7. Save loaded reports to output folder
8. Compare original vs loaded to find differences

Usage:
    pytest tests/report_model_testing/test_converter_roundtrip.py -v -s
"""
import asyncio
import copy
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

# V1 Report Model imports
from pywats.domains.report.report_models import UUTReport as UUTReportV1
from pywats.domains.report.report_models import UURReport as UURReportV1

# V3 Report Model imports  
from pywats.domains.report.report_models_v3 import UUTReport as UUTReportV3
from pywats.domains.report.report_models_v3 import UURReport as UURReportV3

# API client - use AsyncWATS for async tests
from pywats import AsyncWATS


# =============================================================================
# Test Configuration
# =============================================================================

TEST_DIR = Path(__file__).parent
ORIGINAL_REPORTS_DIR = TEST_DIR / "original reports"
OUTPUT_DIR = TEST_DIR / "files_after_conversion_and_reload"

# Original test file - use new_report_example.json for simpler roundtrip test
JSON_ORIGINAL = Path(__file__).parent / "original reports" / "new_report_example.json"
UUR_ORIGINAL = Path(__file__).parent / "original reports" / "uur_example.json"

# Wait time after submit (seconds)
SUBMIT_WAIT_TIME = 5


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture(scope="module")
def output_directory() -> Path:
    """Ensure output directory exists."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


@pytest.fixture(scope="module")
def original_json() -> Dict[str, Any]:
    """Load the original WSJF JSON file."""
    with open(JSON_ORIGINAL, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def uur_json() -> Dict[str, Any]:
    """Load the UUR example JSON file."""
    with open(UUR_ORIGINAL, "r", encoding="utf-8") as f:
        return json.load(f)


# Note: We use the wats_client fixture from the global conftest.py
# It provides a pyWATS instance configured with proper credentials.


# =============================================================================
# Helper Functions
# =============================================================================

def remove_loop_steps(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove steps that contain 'loop' property from the report.
    
    NOTE: Loop steps are being skipped because the WATS server has strict validation
    rules for loops that the exported test files don't satisfy:
    - endingIndex must equal the highest index in the loop
    - num must be one more than endingIndex  
    - All iterations must match the Summary step structure exactly
    
    These validation rules are stricter than what older WATS exports contained.
    This is a known limitation for roundtrip testing with legacy export files.
    
    TODO: Create a proper test file with valid loop structures to test loop roundtrip.
    """
    def filter_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recursively filter out steps with loops and process nested steps."""
        filtered = []
        for step in steps:
            if step.get('loop') is not None:
                # Skip steps with loop property
                continue
            # Process nested steps recursively
            step_copy = step.copy()
            if 'steps' in step_copy and step_copy['steps']:
                step_copy['steps'] = filter_steps(step_copy['steps'])
            filtered.append(step_copy)
        return filtered
    
    result = copy.deepcopy(data)
    
    # Handle both flat structure and nested root structure
    if 'root' in result and 'steps' in result['root']:
        result['root']['steps'] = filter_steps(result['root']['steps'])
    elif 'steps' in result:
        result['steps'] = filter_steps(result['steps'])
    
    return result


def save_json(data: Any, filepath: Path) -> None:
    """Save data as formatted JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        if hasattr(data, 'model_dump'):
            # Pydantic model
            json.dump(data.model_dump(mode='json', by_alias=True, exclude_none=True), 
                     f, indent=2, default=str, ensure_ascii=False)
        else:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)


def model_to_dict(report: Any) -> Dict[str, Any]:
    """Convert a report model to dictionary for comparison."""
    if hasattr(report, 'model_dump'):
        return report.model_dump(mode='json', by_alias=True, exclude_none=True)
    raise ValueError(f"Cannot convert {type(report)} to dict")


def modify_for_submission(data: Dict[str, Any], suffix: str) -> Dict[str, Any]:
    """
    Create a copy with modified identifiers to avoid overwrites.
    
    Args:
        data: Original report dict
        suffix: Suffix to append to serial number (e.g., '_v1_test')
    
    Returns:
        Modified copy with new UUID, modified SN, and new start time
    """
    modified = copy.deepcopy(data)
    
    # New UUID
    new_id = str(uuid.uuid4())
    modified["id"] = new_id
    
    # Modify serial number
    original_sn = modified.get("sn") or modified.get("serialNumber", "UNKNOWN")
    new_sn = f"{original_sn}_{suffix}"
    if "sn" in modified:
        modified["sn"] = new_sn
    if "serialNumber" in modified:
        modified["serialNumber"] = new_sn
    
    # New start time
    now = datetime.now(timezone.utc)
    modified["start"] = now.isoformat()
    if "startUTC" in modified:
        modified["startUTC"] = now.isoformat()
    
    return modified


def deep_diff(
    original: Any,
    loaded: Any,
    path: str = "",
    ignore_keys: Optional[set] = None
) -> List[str]:
    """
    Deep comparison finding all differences.
    
    Returns list of difference descriptions.
    """
    if ignore_keys is None:
        # Keys that will naturally differ
        ignore_keys = {"id", "sn", "serialNumber", "start", "startUTC", "startUtc"}
    
    differences = []
    
    if type(original) != type(loaded):
        differences.append(f"TYPE: {path}: {type(original).__name__} vs {type(loaded).__name__}")
        return differences
    
    if isinstance(original, dict):
        all_keys = set(original.keys()) | set(loaded.keys())
        for key in all_keys:
            if key in ignore_keys:
                continue
            current_path = f"{path}.{key}" if path else key
            if key not in original:
                differences.append(f"ADDED: {current_path}")
            elif key not in loaded:
                differences.append(f"MISSING: {current_path}")
            else:
                differences.extend(deep_diff(original[key], loaded[key], current_path, ignore_keys))
    
    elif isinstance(original, list):
        if len(original) != len(loaded):
            differences.append(f"LENGTH: {path}: {len(original)} vs {len(loaded)}")
        for i, (o, l) in enumerate(zip(original, loaded)):
            differences.extend(deep_diff(o, l, f"{path}[{i}]", ignore_keys))
    
    elif original != loaded:
        differences.append(f"VALUE: {path}: {original!r} vs {loaded!r}")
    
    return differences


# =============================================================================
# V1 Model Tests
# =============================================================================

class TestV1ModelRoundtrip:
    """Test V1 model deserialization and roundtrip."""
    
    def test_v1_deserialize_original(self, original_json: Dict[str, Any]) -> None:
        """Test that V1 can deserialize the original JSON."""
        try:
            report = UUTReportV1.model_validate(original_json)
            print(f"\n[OK] V1 deserialized successfully")
            print(f"  PN: {report.pn}")
            print(f"  SN: {report.sn}")
            print(f"  Result: {report.result}")
            assert report.pn, "Part number should be set"
            assert report.sn, "Serial number should be set"
        except Exception as e:
            pytest.fail(f"V1 failed to deserialize: {e}")
    
    @pytest.mark.asyncio
    async def test_v1_roundtrip(
        self, 
        original_json: Dict[str, Any],
        wats_config,
        output_directory: Path
    ) -> None:
        """Full V1 roundtrip: deserialize -> submit -> load -> compare."""
        # 0. Remove loop steps (see remove_loop_steps docstring for why)
        data_without_loops = remove_loop_steps(original_json)
        
        # 1. Modify identifiers
        modified_data = modify_for_submission(data_without_loops, "v1_roundtrip")
        report_id = modified_data["id"]
        
        print(f"\n=== V1 Roundtrip Test ===")
        print(f"UUID: {report_id}")
        print(f"SN: {modified_data.get('sn') or modified_data.get('serialNumber')}")
        
        # 2. Deserialize into V1 model
        try:
            report_v1 = UUTReportV1.model_validate(modified_data)
        except Exception as e:
            pytest.fail(f"V1 deserialization failed: {e}")
        
        # Save what we're submitting
        save_json(report_v1, output_directory / "v1_submitted.json")
        print(f"Saved submitted report to: v1_submitted.json")
        
        # 3. Submit using async client
        async with AsyncWATS(base_url=wats_config["base_url"], token=wats_config["token"]) as client:
            submitted_id = await client.report.submit_report(report_v1)
            assert submitted_id, "Submit should return report ID"
            print(f"Submitted! ID: {submitted_id}")
            
            # 4. Wait for server processing
            print(f"Waiting {SUBMIT_WAIT_TIME}s for server processing...")
            await asyncio.sleep(SUBMIT_WAIT_TIME)
            
            # 5. Load back
            loaded_report = await client.report.get_report(report_id, detail_level=7)
            assert loaded_report, f"Should be able to load report {report_id}"
        
        # 6. Save loaded report
        save_json(loaded_report, output_directory / "v1_loaded.json")
        print(f"Saved loaded report to: v1_loaded.json")
        
        # 7. Compare
        submitted_dict = model_to_dict(report_v1)
        loaded_dict = model_to_dict(loaded_report)
        
        differences = deep_diff(submitted_dict, loaded_dict)
        
        print(f"\n=== V1 Comparison Results ===")
        if differences:
            print(f"Differences found ({len(differences)}):")
            for diff in differences[:30]:
                print(f"  - {diff}")
            if len(differences) > 30:
                print(f"  ... and {len(differences) - 30} more")
        else:
            print("[OK] No differences found!")
        
        # Save diff report
        with open(output_directory / "v1_differences.txt", "w") as f:
            f.write(f"V1 Roundtrip Differences\n")
            f.write(f"========================\n\n")
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Total differences: {len(differences)}\n\n")
            for diff in differences:
                f.write(f"{diff}\n")


# =============================================================================
# V3 Model Tests
# =============================================================================

class TestV3ModelRoundtrip:
    """Test V3 model deserialization and roundtrip."""
    
    def test_v3_deserialize_original(self, original_json: Dict[str, Any]) -> None:
        """Test that V3 can deserialize the original JSON."""
        try:
            report = UUTReportV3.model_validate(original_json)
            print(f"\n[OK] V3 deserialized successfully")
            print(f"  PN: {report.pn}")
            print(f"  SN: {report.sn}")
            print(f"  Result: {report.result}")
            assert report.pn, "Part number should be set"
            assert report.sn, "Serial number should be set"
        except Exception as e:
            pytest.fail(f"V3 failed to deserialize: {e}")
    
    @pytest.mark.asyncio
    async def test_v3_roundtrip(
        self, 
        original_json: Dict[str, Any],
        wats_config,
        output_directory: Path
    ) -> None:
        """Full V3 roundtrip: deserialize -> submit -> load -> compare."""
        # 0. Remove loop steps (see remove_loop_steps docstring for why)
        data_without_loops = remove_loop_steps(original_json)
        
        # 1. Modify identifiers
        modified_data = modify_for_submission(data_without_loops, "v3_roundtrip")
        report_id = modified_data["id"]
        
        print(f"\n=== V3 Roundtrip Test ===")
        print(f"UUID: {report_id}")
        print(f"SN: {modified_data.get('sn') or modified_data.get('serialNumber')}")
        
        # 2. Deserialize into V3 model
        try:
            report_v3 = UUTReportV3.model_validate(modified_data)
        except Exception as e:
            pytest.fail(f"V3 deserialization failed: {e}")
        
        # Save what we're submitting
        save_json(report_v3, output_directory / "v3_submitted.json")
        print(f"Saved submitted report to: v3_submitted.json")
        
        # 3. Submit using async client
        async with AsyncWATS(base_url=wats_config["base_url"], token=wats_config["token"]) as client:
            submitted_id = await client.report.submit_report(report_v3)
            assert submitted_id, "Submit should return report ID"
            print(f"Submitted! ID: {submitted_id}")
            
            # 4. Wait for server processing
            print(f"Waiting {SUBMIT_WAIT_TIME}s for server processing...")
            await asyncio.sleep(SUBMIT_WAIT_TIME)
            
            # 5. Load back
            loaded_report = await client.report.get_report(report_id, detail_level=7)
            assert loaded_report, f"Should be able to load report {report_id}"
        
        # 6. Save loaded report
        save_json(loaded_report, output_directory / "v3_loaded.json")
        print(f"Saved loaded report to: v3_loaded.json")
        
        # 7. Compare
        submitted_dict = model_to_dict(report_v3)
        loaded_dict = model_to_dict(loaded_report)
        
        differences = deep_diff(submitted_dict, loaded_dict)
        
        print(f"\n=== V3 Comparison Results ===")
        if differences:
            print(f"Differences found ({len(differences)}):")
            for diff in differences[:30]:
                print(f"  - {diff}")
            if len(differences) > 30:
                print(f"  ... and {len(differences) - 30} more")
        else:
            print("[OK] No differences found!")
        
        # Save diff report
        with open(output_directory / "v3_differences.txt", "w") as f:
            f.write(f"V3 Roundtrip Differences\n")
            f.write(f"========================\n\n")
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Total differences: {len(differences)}\n\n")
            for diff in differences:
                f.write(f"{diff}\n")


# =============================================================================
# V1 vs V3 Comparison
# =============================================================================

class TestV1VsV3Comparison:
    """Compare V1 and V3 model handling of the same data."""
    
    def test_deserialization_parity(self, original_json: Dict[str, Any]) -> None:
        """Test that V1 and V3 deserialize to equivalent structures."""
        # Deserialize with both
        report_v1 = UUTReportV1.model_validate(original_json)
        report_v3 = UUTReportV3.model_validate(original_json)
        
        # Convert back to dict
        dict_v1 = model_to_dict(report_v1)
        dict_v3 = model_to_dict(report_v3)
        
        # Compare
        differences = deep_diff(dict_v1, dict_v3)
        
        print(f"\n=== V1 vs V3 Deserialization Comparison ===")
        if differences:
            print(f"Differences ({len(differences)}):")
            for diff in differences[:20]:
                print(f"  - {diff}")
            if len(differences) > 20:
                print(f"  ... and {len(differences) - 20} more")


# =============================================================================
#  UUR (Repair) Report Tests
# =============================================================================

class TestV1UURRoundtrip:
    """V1 UUR model roundtrip test."""
    
    @pytest.mark.asyncio
    async def test_v1_uur_deserialize(self, uur_json: Dict[str, Any]) -> None:
        """Test V1 can deserialize the UUR JSON."""
        print("\n=== V1 UUR Deserialization Test ===")
        try:
            report = UURReportV1.model_validate(uur_json)
            print(f"✓ V1 deserialized UUR report: {report.pn}/{report.sn}")
            assert report.type == "R"
            assert report.info is not None
            assert report.info.operator == "RepairOperator"
        except Exception as e:
            pytest.fail(f"V1 UUR deserialization failed: {e}")
    
    @pytest.mark.asyncio
    async def test_v1_uur_roundtrip(
        self, 
        uur_json: Dict[str, Any],
        wats_config,
        output_directory: Path
    ) -> None:
        """Full V1 UUR roundtrip: deserialize → submit → load → compare."""
        print("\n=== V1 UUR Roundtrip Test ===")
        
        # Deserialize
        report_v1 = UURReportV1.model_validate(uur_json)
        
        # Modify for uniqueness
        new_uuid = uuid.uuid4()
        report_v1.id = new_uuid
        report_v1.sn = f"{report_v1.sn}_v1"
        report_v1.start = datetime.now(timezone.utc)
        
        # Update main sub-unit serial to match
        if report_v1.sub_units:
            for su in report_v1.sub_units:
                if su.idx == 0:  # Main unit
                    su.sn = report_v1.sn
                    break
        
        print(f"UUID: {new_uuid}")
        print(f"SN: {report_v1.sn}")
        
        # Submit
        submitted_json = report_v1.model_dump(mode="json", by_alias=True, exclude_none=True)
        output_directory.joinpath("uur_v1_submitted.json").write_text(
            json.dumps(submitted_json, indent=2), encoding="utf-8"
        )
        print(f"Saved submitted report to: uur_v1_submitted.json")
        
        # Submit using async client
        async with AsyncWATS(base_url=wats_config["base_url"], token=wats_config["token"]) as client:
            try:
                submitted_id = await client.report.submit_report(report_v1)
                print(f"Submitted! ID: {submitted_id}")
            except Exception as e:
                pytest.fail(f"Submit failed: {e}")
            
            # Wait for processing
            print(f"Waiting {SUBMIT_WAIT_TIME}s for server processing...")
            await asyncio.sleep(SUBMIT_WAIT_TIME)
            
            # Load back
            try:
                loaded_report = await client.report.get_report(str(new_uuid), detail_level=7)
                loaded_json = loaded_report.model_dump(mode="json", by_alias=True)
                output_directory.joinpath("uur_v1_loaded.json").write_text(
                    json.dumps(loaded_json, indent=2), encoding="utf-8"
                )
                print(f"Saved loaded report to: uur_v1_loaded.json")
            except Exception as e:
                pytest.fail(f"Load failed: {e}")
        
        # Compare
        submitted_dict = model_to_dict(report_v1)
        loaded_dict = model_to_dict(loaded_report)
        
        differences = deep_diff(submitted_dict, loaded_dict)
        
        print(f"\n=== V1 UUR Comparison Results ===")
        if differences:
            print(f"Differences found ({len(differences)}):")
            for diff in differences[:10]:  # Show first 10
                print(f"  - {diff}")
        else:
            print("✓ No differences - perfect roundtrip!")


class TestV3UURRoundtrip:
    """V3 UUR model roundtrip test."""
    
    @pytest.mark.asyncio
    async def test_v3_uur_deserialize(self, uur_json: Dict[str, Any]) -> None:
        """Test V3 can deserialize the UUR JSON."""
        print("\n=== V3 UUR Deserialization Test ===")
        try:
            report = UURReportV3.model_validate(uur_json)
            print(f"✓ V3 deserialized UUR report: {report.pn}/{report.sn}")
            assert report.type == "R"
            assert report.uur_info is not None
            assert report.uur_info.operator == "RepairOperator"
        except Exception as e:
            pytest.fail(f"V3 UUR deserialization failed: {e}")
    
    @pytest.mark.asyncio
    async def test_v3_uur_roundtrip(
        self, 
        uur_json: Dict[str, Any],
        wats_config,
        output_directory: Path
    ) -> None:
        """Full V3 UUR roundtrip: deserialize → submit → load → compare."""
        print("\n=== V3 UUR Roundtrip Test ===")
        
        # Deserialize
        report_v3 = UURReportV3.model_validate(uur_json)
        
        # Modify for uniqueness
        new_uuid = uuid.uuid4()
        report_v3.id = new_uuid
        report_v3.sn = f"{report_v3.sn}_v3"
        report_v3.start = datetime.now(timezone.utc)
        
        # Update main sub-unit serial to match
        if report_v3.sub_units:
            for su in report_v3.sub_units:
                if su.idx == 0:  # Main unit
                    su.sn = report_v3.sn
                    break
        
        print(f"UUID: {new_uuid}")
        print(f"SN: {report_v3.sn}")
        
        # Submit
        submitted_json = report_v3.model_dump(mode="json", by_alias=True, exclude_none=True)
        output_directory.joinpath("uur_v3_submitted.json").write_text(
            json.dumps(submitted_json, indent=2), encoding="utf-8"
        )
        print(f"Saved submitted report to: uur_v3_submitted.json")
        
        # Submit using async client
        async with AsyncWATS(base_url=wats_config["base_url"], token=wats_config["token"]) as client:
            try:
                submitted_id = await client.report.submit_report(report_v3)
                print(f"Submitted! ID: {submitted_id}")
            except Exception as e:
                pytest.fail(f"Submit failed: {e}")
            
            # Wait for processing
            print(f"Waiting {SUBMIT_WAIT_TIME}s for server processing...")
            await asyncio.sleep(SUBMIT_WAIT_TIME)
            
            # Load back
            try:
                loaded_report = await client.report.get_report(str(new_uuid), detail_level=7)
                loaded_json = loaded_report.model_dump(mode="json", by_alias=True)
                output_directory.joinpath("uur_v3_loaded.json").write_text(
                    json.dumps(loaded_json, indent=2), encoding="utf-8"
                )
                print(f"Saved loaded report to: uur_v3_loaded.json")
            except Exception as e:
                pytest.fail(f"Load failed: {e}")
        
        # Compare
        submitted_dict = model_to_dict(report_v3)
        loaded_dict = model_to_dict(loaded_report)
        
        differences = deep_diff(submitted_dict, loaded_dict)
        
        print(f"\n=== V3 UUR Comparison Results ===")
        if differences:
            print(f"Differences found ({len(differences)}):")
            for diff in differences[:10]:  # Show first 10
                print(f"  - {diff}")
        else:
            print("✓ No differences - perfect roundtrip!")


# =============================================================================
#           print("[OK] V1 and V3 produce identical output!")
        
        # This is informational - we expect them to be the same if V3 is drop-in
        # Don't fail the test, just report


# =============================================================================
# Summary
# =============================================================================

class TestSummary:
    """Print summary of test output."""
    
    def test_print_summary(self, output_directory: Path) -> None:
        """Print summary of generated files."""
        print("\n" + "=" * 70)
        print("ROUNDTRIP TEST SUMMARY")
        print("=" * 70)
        
        print(f"\nOriginal file: {JSON_ORIGINAL}")
        print(f"Output directory: {output_directory}")
        
        if output_directory.exists():
            files = sorted(output_directory.iterdir())
            print(f"\nGenerated files ({len(files)}):")
            for f in files:
                if f.is_file():
                    size = f.stat().st_size
                    print(f"  - {f.name} ({size:,} bytes)")
        
        print("\n" + "=" * 70)
