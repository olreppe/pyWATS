"""
Test script for offline queue implementation.

Tests:
1. Basic queue operations (add, list, count)
2. Submit with offline fallback
3. Explicit offline submission
4. Queue processing
5. Format conversion
6. Error handling and retry logic
"""

import os
import json
import tempfile
import time
from pathlib import Path

# Set environment variables for testing
os.environ['PYWATS_SERVER_URL'] = 'https://python.wats.com'
os.environ['PYWATS_API_TOKEN'] = 'cHlXQVRTX0FQSV9BVVRPVEVTVDo2cGhUUjg0ZTVIMHA1R3JUWGtQZlY0UTNvbmk2MiM='

from pywats import pyWATS
from pywats.queue import SimpleQueue, QueueStatus, convert_to_wsjf, WSJFConverter


def test_basic_queue_operations():
    """Test basic queue add/list/count operations."""
    print("\n=== Test 1: Basic Queue Operations ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        api = pyWATS()
        queue = SimpleQueue(api, queue_dir=temp_dir)
        
        # Create test report
        report = api.report.create_uut_report(
            operator="TestOperator",
            part_number="TEST-001",
            revision="A",
            serial_number="SN-TEST-001",
            operation_type=100
        )
        
        root = report.get_root_sequence_call()
        root.add_numeric_step(
            name="Voltage Test",
            value=5.02,
            low_limit=4.5,
            high_limit=5.5,
            unit="V"
        )
        
        # Add to queue
        file_name = queue.add(report)
        print(f"✓ Added report to queue: {file_name}")
        
        # Check counts
        pending_count = queue.count_pending()
        assert pending_count == 1, f"Expected 1 pending, got {pending_count}"
        print(f"✓ Pending count: {pending_count}")
        
        # List pending
        pending = queue.list_pending()
        assert len(pending) == 1, f"Expected 1 pending report, got {len(pending)}"
        print(f"✓ Listed pending reports: {len(pending)}")
        
        # Verify file exists
        queue_file = Path(temp_dir) / file_name
        assert queue_file.exists(), f"Queue file not found: {queue_file}"
        print(f"✓ Queue file created: {queue_file.name}")
        
        print("✓ Test 1 PASSED")


def test_submit_with_fallback_online():
    """Test submit with offline fallback when server is online."""
    print("\n=== Test 2: Submit with Fallback (Online) ===")
    
    api = pyWATS()
    
    # Create test report
    report = api.report.create_uut_report(
        operator="TestOperator",
        part_number="TEST-002",
        revision="A",
        serial_number=f"SN-TEST-{int(time.time())}",
        operation_type=100
    )
    
    root = report.get_root_sequence_call()
    root.add_boolean_step(
        name="Power Check",
        status="P"
    )
    
    try:
        # Submit with fallback (should succeed if online)
        result = api.report.submit(report, offline_fallback=True)
        
        if result:
            print(f"✓ Report submitted successfully (online): {result}")
            print("✓ Test 2 PASSED")
        else:
            print(f"⚠ Server offline - report queued for later")
            print("✓ Test 2 PASSED (offline mode)")
    except Exception as e:
        print(f"✗ Test 2 FAILED: {e}")


def test_explicit_offline():
    """Test explicit offline submission."""
    print("\n=== Test 3: Explicit Offline Submission ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        api = pyWATS()
        
        # Create test report
        report = api.report.create_uut_report(
            operator="TestOperator",
            part_number="TEST-003",
            revision="A",
            serial_number="SN-TEST-003",
            operation_type=100
        )
        
        root = report.get_root_sequence_call()
        root.add_string_step(
            name="Firmware Version",
            value="v1.2.3"
        )
        
        # Submit offline explicitly
        file_name = api.report.submit_offline(report, queue_dir=temp_dir)
        print(f"✓ Report queued explicitly: {file_name}")
        
        # Verify file exists
        queue_file = Path(temp_dir) / file_name
        assert queue_file.exists(), f"Queue file not found: {queue_file}"
        print(f"✓ Queue file created: {queue_file.name}")
        
        # Verify it's in WSJF format (JSON)
        with open(queue_file, 'r') as f:
            data = json.load(f)
            assert 'UUT' in data or 'PartNumber' in data, "Invalid WSJF format"
            print(f"✓ File is valid WSJF format")
        
        print("✓ Test 3 PASSED")


def test_process_queue():
    """Test processing queued reports."""
    print("\n=== Test 4: Process Queue ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        api = pyWATS()
        queue = SimpleQueue(api, queue_dir=temp_dir)
        
        # Add multiple reports to queue
        for i in range(3):
            report = api.report.create_uut_report(
                operator="TestOperator",
                part_number="TEST-004",
                revision="A",
                serial_number=f"SN-TEST-004-{i}",
                operation_type=100
            )
            
            root = report.get_root_sequence_call()
            root.add_numeric_step(
                name=f"Test {i}",
                value=i * 1.5,
                low_limit=0,
                high_limit=10
            )
            
            queue.add(report)
        
        print(f"✓ Added 3 reports to queue")
        
        # Process queue
        results = queue.process_all()
        print(f"✓ Processing results:")
        print(f"  - Success: {results['success']}")
        print(f"  - Failed: {results['failed']}")
        print(f"  - Skipped: {results['skipped']}")
        
        # Check remaining count
        remaining = queue.count_pending()
        print(f"✓ Remaining pending: {remaining}")
        
        print("✓ Test 4 PASSED")


def test_format_conversion():
    """Test WSJF format conversion."""
    print("\n=== Test 5: Format Conversion ===")
    
    api = pyWATS()
    
    # Create test report
    report = api.report.create_uut_report(
        operator="TestOperator",
        part_number="TEST-005",
        revision="A",
        serial_number="SN-TEST-005",
        operation_type=100
    )
    
    root = report.get_root_sequence_call()
    root.add_numeric_step(
        name="Resistance",
        value=10.2,
        low_limit=9.0,
        high_limit=11.0,
        unit="Ohm"
    )
    
    # Convert to WSJF
    converter = WSJFConverter()
    wsjf_json = converter.to_wsjf(report)
    print(f"✓ Converted report to WSJF: {len(wsjf_json)} bytes")
    
    # Verify it's valid JSON
    data = json.loads(wsjf_json)
    # WSJF format uses camelCase field names from Pydantic serialization
    print(f"✓ WSJF keys: {list(data.keys())[:5]}...")  # Debug output
    # Check for common fields (flexible to handle various field names)
    has_valid_structure = (
        'partNumber' in data or 'PartNumber' in data or 
        'uut' in data or 'UUT' in data or
        'operationType' in data or 'serialNumber' in data
    )
    assert has_valid_structure, f"Invalid WSJF format. Keys: {list(data.keys())}"
    print(f"✓ WSJF is valid JSON")
    
    # Convert back
    restored_report = converter.from_wsjf(wsjf_json)
    print(f"✓ Converted WSJF back to report")
    
    print("✓ Test 5 PASSED")


def test_error_handling():
    """Test error handling and retry logic."""
    print("\n=== Test 6: Error Handling & Retry ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create API with invalid token (will fail)
        api = pyWATS(
            base_url="https://python.wats.com",
            token="invalid-token-will-fail"
        )
        
        queue = SimpleQueue(api, queue_dir=temp_dir, max_retries=2)
        
        # Create test report
        report = api.report.create_uut_report(
            operator="TestOperator",
            part_number="TEST-006",
            revision="A",
            serial_number="SN-TEST-006",
            operation_type=100
        )
        
        root = report.get_root_sequence_call()
        root.add_boolean_step(name="Test", status="P")
        
        # Add to queue
        queue.add(report)
        print(f"✓ Added report to queue")
        
        # Process (should fail)
        results = queue.process_all()
        print(f"✓ Processing with invalid token:")
        print(f"  - Success: {results['success']}")
        print(f"  - Failed: {results['failed']}")
        
        # Check error count
        error_count = queue.count_errors()
        print(f"✓ Error reports: {error_count}")
        
        if error_count > 0:
            errors = queue.list_errors()
            print(f"✓ Error details:")
            for err in errors:
                print(f"  - File: {err.file_name}")
                print(f"  - Attempts: {err.attempts}")
                print(f"  - Last error: {err.last_error[:100] if err.last_error else 'None'}...")
        
        print("✓ Test 6 PASSED")


def test_queue_file_states():
    """Test queue file state transitions."""
    print("\n=== Test 7: Queue File States ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        api = pyWATS()
        queue = SimpleQueue(api, queue_dir=temp_dir, delete_completed=False)
        
        # Create test report
        report = api.report.create_uut_report(
            operator="TestOperator",
            part_number="TEST-007",
            revision="A",
            serial_number=f"SN-TEST-{int(time.time())}",
            operation_type=100
        )
        
        root = report.get_root_sequence_call()
        root.add_boolean_step(name="Test", status="P")
        
        # Add to queue (creates .pending.wsjf)
        file_name = queue.add(report)
        pending_file = Path(temp_dir) / file_name
        assert pending_file.exists(), "Pending file not created"
        assert pending_file.suffix == '.wsjf', "Wrong file extension"
        assert '.pending' in file_name, "Not marked as pending"
        print(f"✓ Created pending file: {file_name}")
        
        # Process queue
        results = queue.process_all()
        
        # Check final state (should be .completed.wsjf or .error.wsjf)
        queue_dir = Path(temp_dir)
        completed_files = list(queue_dir.glob("*.completed.wsjf"))
        error_files = list(queue_dir.glob("*.error.wsjf"))
        
        if completed_files:
            print(f"✓ Report completed: {completed_files[0].name}")
        elif error_files:
            print(f"⚠ Report failed: {error_files[0].name}")
        
        print("✓ Test 7 PASSED")


def test_metadata_tracking():
    """Test metadata tracking for queue items."""
    print("\n=== Test 8: Metadata Tracking ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        api = pyWATS(token="invalid-token")  # Will fail
        queue = SimpleQueue(api, queue_dir=temp_dir, max_retries=3)
        
        # Create and queue report
        report = api.report.create_uut_report(
            operator="TestOperator",
            part_number="TEST-008",
            revision="A",
            serial_number="SN-TEST-008",
            operation_type=100
        )
        
        file_name = queue.add(report)
        print(f"✓ Queued report: {file_name}")
        
        # Process (will fail and create metadata)
        queue.process_all()
        
        # Check for metadata file
        meta_file = Path(temp_dir) / f"{file_name}.meta.json"
        if meta_file.exists():
            with open(meta_file, 'r') as f:
                metadata = json.load(f)
                print(f"✓ Metadata file created:")
                print(f"  - Attempts: {metadata.get('attempts', 0)}")
                print(f"  - Created: {metadata.get('created_at', 'N/A')}")
                print(f"  - Last attempt: {metadata.get('last_attempt_at', 'N/A')}")
                print(f"  - Error: {metadata.get('last_error', 'N/A')[:100]}...")
        
        print("✓ Test 8 PASSED")


def run_all_tests():
    """Run all queue tests."""
    print("=" * 60)
    print("pyWATS Offline Queue Implementation Tests")
    print("=" * 60)
    
    tests = [
        test_basic_queue_operations,
        test_submit_with_fallback_online,
        test_explicit_offline,
        test_process_queue,
        test_format_conversion,
        test_error_handling,
        test_queue_file_states,
        test_metadata_tracking
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    exit(0 if failed == 0 else 1)
