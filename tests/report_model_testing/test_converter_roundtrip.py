"""
Report Model Roundtrip Test

This test validates that the report models can:
1. Deserialize WSJF JSON files using Pydantic model_validate
2. Submit reports to WATS API
3. Load reports back from server
4. Compare loaded data against original to find information loss

Test Workflow:
1. Load original JSON report
2. Deserialize directly into UUTReport/UURReport using model_validate
3. Modify: new UUID, append to serial number, set new start time
4. Submit via api.report.submit_report()
5. Wait for server processing
6. Load report back using the GUID
7. Save loaded reports to output folder
8. Compare original vs loaded to find differences

Usage:
    pytest tests/report_model_testing/test_converter_roundtrip.py -v -s
    
Note:
    This test requires WATS API access and will be skipped if wats_config is not available.
    A "perfect" sample report will be provided later to make this a crucial validation test.
"""
import asyncio
import copy
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

# Report Model imports (current implementation)
from pywats.domains.report.report_models import UUTReport
from pywats.domains.report.report_models import UURReport

# API client - use AsyncWATS for async tests
from pywats import AsyncWATS


# =============================================================================
# Test Configuration
# =============================================================================

TEST_DIR = Path(__file__).parent
ORIGINAL_REPORTS_DIR = TEST_DIR / "original reports"
OUTPUT_DIR = TEST_DIR / "files_after_conversion_and_reload"

# Test files
UUT_JSON_FILE = ORIGINAL_REPORTS_DIR / "new_report_example.json"
UUR_JSON_FILE = ORIGINAL_REPORTS_DIR / "uur_example.json"

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
def uut_json() -> Dict[str, Any]:
    """Load the UUT example JSON file."""
    if not UUT_JSON_FILE.exists():
        pytest.skip(f"UUT example file not found: {UUT_JSON_FILE}")
    with open(UUT_JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def uur_json() -> Dict[str, Any]:
    """Load the UUR example JSON file."""
    if not UUR_JSON_FILE.exists():
        pytest.skip(f"UUR example file not found: {UUR_JSON_FILE}")
    with open(UUR_JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================================================================
# Helper Functions
# =============================================================================

def remove_loop_steps(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove steps that contain 'loop' property from the report.
    
    NOTE: Loop steps are being skipped because the WATS server has strict validation
    rules for loops that older exported test files don't satisfy.
    
    TODO: Create a proper test file with valid loop structures to test loop roundtrip.
    """
    def filter_steps(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Recursively filter out steps with loops and process nested steps."""
        filtered = []
        for step in steps:
            if step.get('loop') is not None:
                continue
            step_copy = step.copy()
            if 'steps' in step_copy and step_copy['steps']:
                step_copy['steps'] = filter_steps(step_copy['steps'])
            filtered.append(step_copy)
        return filtered
    
    result = copy.deepcopy(data)
    
    if 'root' in result and 'steps' in result['root']:
        result['root']['steps'] = filter_steps(result['root']['steps'])
    elif 'steps' in result:
        result['steps'] = filter_steps(result['steps'])
    
    return result


def save_json(data: Any, filepath: Path) -> None:
    """Save data as formatted JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        if hasattr(data, 'model_dump'):
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
        suffix: Suffix to append to serial number
    
    Returns:
        Modified copy with new UUID, modified SN, and new start time
    """
    modified = copy.deepcopy(data)
    
    # New UUID
    modified["id"] = str(uuid.uuid4())
    
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
# UUT Report Roundtrip Tests
# =============================================================================

class TestUUTRoundtrip:
    """Test UUT report deserialization and roundtrip."""
    
    def test_uut_deserialize(self, uut_json: Dict[str, Any]) -> None:
        """Test that UUTReport can deserialize the JSON."""
        try:
            report = UUTReport.model_validate(uut_json)
            print(f"\n[OK] UUT deserialized successfully")
            print(f"  PN: {report.pn}")
            print(f"  SN: {report.sn}")
            print(f"  Result: {report.result}")
            assert report.pn, "Part number should be set"
            assert report.sn, "Serial number should be set"
        except Exception as e:
            pytest.fail(f"UUT deserialization failed: {e}")
    
    @pytest.mark.asyncio
    async def test_uut_roundtrip(
        self, 
        uut_json: Dict[str, Any],
        wats_config,
        output_directory: Path
    ) -> None:
        """Full UUT roundtrip: deserialize -> submit -> load -> compare."""
        # Remove loop steps (see remove_loop_steps docstring for why)
        data_without_loops = remove_loop_steps(uut_json)
        
        # Modify identifiers
        modified_data = modify_for_submission(data_without_loops, "roundtrip")
        report_id = modified_data["id"]
        
        print(f"\n=== UUT Roundtrip Test ===")
        print(f"UUID: {report_id}")
        print(f"SN: {modified_data.get('sn') or modified_data.get('serialNumber')}")
        
        # Deserialize into model
        try:
            report = UUTReport.model_validate(modified_data)
        except Exception as e:
            pytest.fail(f"UUT deserialization failed: {e}")
        
        # Save what we're submitting
        save_json(report, output_directory / "uut_submitted.json")
        print(f"Saved submitted report to: uut_submitted.json")
        
        # Submit using async client
        async with AsyncWATS(base_url=wats_config["base_url"], token=wats_config["token"]) as client:
            submitted_id = await client.report.submit_report(report)
            assert submitted_id, "Submit should return report ID"
            print(f"Submitted! ID: {submitted_id}")
            
            # Wait for server processing
            print(f"Waiting {SUBMIT_WAIT_TIME}s for server processing...")
            await asyncio.sleep(SUBMIT_WAIT_TIME)
            
            # Load back
            loaded_report = await client.report.get_report(report_id, detail_level=7)
            assert loaded_report, f"Should be able to load report {report_id}"
        
        # Save loaded report
        save_json(loaded_report, output_directory / "uut_loaded.json")
        print(f"Saved loaded report to: uut_loaded.json")
        
        # Compare
        submitted_dict = model_to_dict(report)
        loaded_dict = model_to_dict(loaded_report)
        
        differences = deep_diff(submitted_dict, loaded_dict)
        
        print(f"\n=== UUT Comparison Results ===")
        if differences:
            print(f"Differences found ({len(differences)}):")
            for diff in differences[:30]:
                print(f"  - {diff}")
            if len(differences) > 30:
                print(f"  ... and {len(differences) - 30} more")
        else:
            print("[OK] No differences found!")
        
        # Save diff report
        with open(output_directory / "uut_differences.txt", "w") as f:
            f.write(f"UUT Roundtrip Differences\n")
            f.write(f"=========================\n\n")
            f.write(f"Report ID: {report_id}\n")
            f.write(f"Total differences: {len(differences)}\n\n")
            for diff in differences:
                f.write(f"{diff}\n")


# =============================================================================
# UUR Report Roundtrip Tests
# =============================================================================

class TestUURRoundtrip:
    """Test UUR report deserialization and roundtrip."""
    
    def test_uur_deserialize(self, uur_json: Dict[str, Any]) -> None:
        """Test that UURReport can deserialize the JSON."""
        print("\n=== UUR Deserialization Test ===")
        try:
            report = UURReport.model_validate(uur_json)
            print(f"[OK] UUR deserialized: {report.pn}/{report.sn}")
            assert report.type == "R"
            assert report.info is not None
        except Exception as e:
            pytest.fail(f"UUR deserialization failed: {e}")
    
    @pytest.mark.asyncio
    async def test_uur_roundtrip(
        self, 
        uur_json: Dict[str, Any],
        wats_config,
        output_directory: Path
    ) -> None:
        """Full UUR roundtrip: deserialize -> submit -> load -> compare."""
        print("\n=== UUR Roundtrip Test ===")
        
        # Deserialize
        report = UURReport.model_validate(uur_json)
        
        # Modify for uniqueness
        new_uuid = uuid.uuid4()
        report.id = new_uuid
        report.sn = f"{report.sn}_roundtrip"
        report.start = datetime.now(timezone.utc)
        
        # Update main sub-unit serial to match
        if report.sub_units:
            for su in report.sub_units:
                if su.idx == 0:
                    su.sn = report.sn
                    break
        
        print(f"UUID: {new_uuid}")
        print(f"SN: {report.sn}")
        
        # Save submitted report
        save_json(report, output_directory / "uur_submitted.json")
        print(f"Saved submitted report to: uur_submitted.json")
        
        # Submit using async client
        async with AsyncWATS(base_url=wats_config["base_url"], token=wats_config["token"]) as client:
            try:
                submitted_id = await client.report.submit_report(report)
                print(f"Submitted! ID: {submitted_id}")
            except Exception as e:
                pytest.fail(f"Submit failed: {e}")
            
            # Wait for processing
            print(f"Waiting {SUBMIT_WAIT_TIME}s for server processing...")
            await asyncio.sleep(SUBMIT_WAIT_TIME)
            
            # Load back
            try:
                loaded_report = await client.report.get_report(str(new_uuid), detail_level=7)
                save_json(loaded_report, output_directory / "uur_loaded.json")
                print(f"Saved loaded report to: uur_loaded.json")
            except Exception as e:
                pytest.fail(f"Load failed: {e}")
        
        # Compare
        submitted_dict = model_to_dict(report)
        loaded_dict = model_to_dict(loaded_report)
        
        differences = deep_diff(submitted_dict, loaded_dict)
        
        print(f"\n=== UUR Comparison Results ===")
        if differences:
            print(f"Differences found ({len(differences)}):")
            for diff in differences[:10]:
                print(f"  - {diff}")
        else:
            print("[OK] No differences - perfect roundtrip!")
        
        # Save diff report
        with open(output_directory / "uur_differences.txt", "w") as f:
            f.write(f"UUR Roundtrip Differences\n")
            f.write(f"=========================\n\n")
            f.write(f"Report ID: {new_uuid}\n")
            f.write(f"Total differences: {len(differences)}\n\n")
            for diff in differences:
                f.write(f"{diff}\n")


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
        
        print(f"\nUUT file: {UUT_JSON_FILE}")
        print(f"UUR file: {UUR_JSON_FILE}")
        print(f"Output directory: {output_directory}")
        
        if output_directory.exists():
            files = sorted(output_directory.iterdir())
            print(f"\nGenerated files ({len(files)}):")
            for f in files:
                if f.is_file():
                    size = f.stat().st_size
                    print(f"  - {f.name} ({size:,} bytes)")
        
        print("\n" + "=" * 70)
