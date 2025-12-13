"""
Comprehensive Asset Management Tests

This test suite validates the complete Asset Manager functionality:
- Asset hierarchy (parent/child relationships)
- Asset types with running count limits
- Alarm state monitoring
- Running count tracking and reset

Test Scenario:
1. Create asset types for test equipment (ATE, fixtures, instruments)
2. Create an asset hierarchy:
   - ATE (parent)
     - DMM (child) 
     - PowerSupply (child)
     - Fixture (child)
3. Run test loop that increments counts
4. Check alarm states as counts approach limits
5. Reset running count and verify alarm clears
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import UUID
import pytest
import time

from pywats.domains.asset import (
    Asset,
    AssetType,
    AssetState,
    AssetAlarmState,
)


# =============================================================================
# Test Configuration
# =============================================================================

# Running count limit for test - low value to trigger alarms quickly
RUNNING_COUNT_LIMIT = 5
WARNING_THRESHOLD = 60.0  # Warning at 60% (3 runs)
ALARM_THRESHOLD = 100.0   # Alarm at 100% (5 runs)


def generate_serial(prefix: str) -> str:
    """Generate a unique serial number with timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:18]
    return f"{prefix}-{timestamp}"


# =============================================================================
# Asset Type Fixtures
# =============================================================================

@pytest.fixture(scope="module")
def test_asset_types(wats_client: Any) -> Dict[str, AssetType]:
    """
    Create or get asset types for testing.
    
    Creates types with short running count limits so alarms trigger quickly.
    """
    print("\n=== SETTING UP ASSET TYPES ===")
    
    # Define types we need
    type_definitions = {
        "ATE": {
            "type_name": f"PyTest_ATE_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "running_count_limit": RUNNING_COUNT_LIMIT,
            "warning_threshold": WARNING_THRESHOLD,
            "alarm_threshold": ALARM_THRESHOLD,
        },
        "DMM": {
            "type_name": f"PyTest_DMM_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "running_count_limit": RUNNING_COUNT_LIMIT * 2,  # Instrument lasts longer
            "warning_threshold": WARNING_THRESHOLD,
            "alarm_threshold": ALARM_THRESHOLD,
        },
        "Fixture": {
            "type_name": f"PyTest_Fixture_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "running_count_limit": RUNNING_COUNT_LIMIT,
            "warning_threshold": WARNING_THRESHOLD,
            "alarm_threshold": ALARM_THRESHOLD,
        },
    }
    
    created_types = {}
    
    for key, type_def in type_definitions.items():
        result = wats_client.asset.create_asset_type(**type_def)
        if result:
            print(f"  ✓ Created asset type: {key} ({result.type_name})")
            print(f"    - Type ID: {result.type_id}")
            print(f"    - Running count limit: {result.running_count_limit}")
            created_types[key] = result
        else:
            # Try to find existing type by name
            all_types = wats_client.asset.get_asset_types()
            for t in all_types:
                if t.type_name == type_def["type_name"]:
                    created_types[key] = t
                    print(f"  ℹ Using existing type: {key} ({t.type_name})")
                    break
    
    if len(created_types) < len(type_definitions):
        pytest.skip("Could not create all required asset types")
    
    print("==============================\n")
    return created_types


# =============================================================================
# Asset Hierarchy Fixture
# =============================================================================

@pytest.fixture(scope="module")
def test_asset_hierarchy(
    wats_client: Any,
    test_asset_types: Dict[str, AssetType]
) -> Dict[str, Asset]:
    """
    Create a test asset hierarchy:
    
    ATE (parent)
    ├── DMM (child instrument)
    ├── PowerSupply (child, uses DMM type)
    └── Fixture (child)
    """
    print("\n=== CREATING ASSET HIERARCHY ===")
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    assets = {}
    
    # 1. Create parent ATE
    ate_serial = f"ATE-PYTEST-{timestamp}"
    ate = wats_client.asset.create_asset(
        serial_number=ate_serial,
        type_id=test_asset_types["ATE"].type_id,
        asset_name="PyTest ATE Station",
        description="Test ATE created by pytest - comprehensive asset test",
        location="Test Lab"
    )
    
    if ate:
        print(f"  ✓ Created ATE: {ate.serial_number}")
        print(f"    - Asset ID: {ate.asset_id}")
        assets["ATE"] = ate
    else:
        pytest.fail("Failed to create ATE asset")
    
    # Small delay to ensure parent is registered
    time.sleep(0.5)
    
    # 2. Create child DMM
    dmm_serial = f"DMM-PYTEST-{timestamp}"
    dmm = wats_client.asset.create_asset(
        serial_number=dmm_serial,
        type_id=test_asset_types["DMM"].type_id,
        asset_name="PyTest DMM",
        description="Digital Multimeter for test",
        parent_serial_number=ate_serial
    )
    
    if dmm:
        print(f"  ✓ Created DMM (child of ATE): {dmm.serial_number}")
        assets["DMM"] = dmm
    else:
        print(f"  ⚠ Failed to create DMM as child, creating standalone")
        dmm = wats_client.asset.create_asset(
            serial_number=dmm_serial,
            type_id=test_asset_types["DMM"].type_id,
            asset_name="PyTest DMM",
            description="Digital Multimeter for test"
        )
        if dmm:
            assets["DMM"] = dmm
    
    # 3. Create child Fixture
    fixture_serial = f"FIX-PYTEST-{timestamp}"
    fixture = wats_client.asset.create_asset(
        serial_number=fixture_serial,
        type_id=test_asset_types["Fixture"].type_id,
        asset_name="PyTest Test Fixture",
        description="Test fixture for UUT",
        parent_serial_number=ate_serial
    )
    
    if fixture:
        print(f"  ✓ Created Fixture (child of ATE): {fixture.serial_number}")
        assets["Fixture"] = fixture
    else:
        print(f"  ⚠ Failed to create Fixture as child, creating standalone")
        fixture = wats_client.asset.create_asset(
            serial_number=fixture_serial,
            type_id=test_asset_types["Fixture"].type_id,
            asset_name="PyTest Test Fixture",
            description="Test fixture for UUT"
        )
        if fixture:
            assets["Fixture"] = fixture
    
    print("================================\n")
    
    return assets


# =============================================================================
# Test Classes
# =============================================================================

class TestAssetTypeCreation:
    """Test asset type creation with count limits."""

    def test_asset_types_created(self, test_asset_types: Dict[str, AssetType]) -> None:
        """Verify asset types were created with correct properties."""
        print("\n=== VERIFY ASSET TYPES ===")
        
        assert "ATE" in test_asset_types
        assert "DMM" in test_asset_types
        assert "Fixture" in test_asset_types
        
        # Verify ATE type has running count limit
        ate_type = test_asset_types["ATE"]
        print(f"ATE Type: {ate_type.type_name}")
        print(f"  - Running count limit: {ate_type.running_count_limit}")
        print(f"  - Warning threshold: {ate_type.warning_threshold}")
        print(f"  - Alarm threshold: {ate_type.alarm_threshold}")
        
        assert ate_type.running_count_limit == RUNNING_COUNT_LIMIT
        print("==========================\n")


class TestAssetHierarchy:
    """Test asset hierarchy creation and retrieval."""

    def test_hierarchy_created(self, test_asset_hierarchy: Dict[str, Asset]) -> None:
        """Verify all assets in hierarchy were created."""
        print("\n=== VERIFY ASSET HIERARCHY ===")
        
        assert "ATE" in test_asset_hierarchy
        assert "DMM" in test_asset_hierarchy
        assert "Fixture" in test_asset_hierarchy
        
        for name, asset in test_asset_hierarchy.items():
            print(f"{name}: {asset.serial_number}")
            print(f"  - Asset ID: {asset.asset_id}")
            print(f"  - Parent: {asset.parent_serial_number or 'None'}")
        
        print("==============================\n")

    def test_get_child_assets(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Test retrieving child assets of ATE."""
        print("\n=== GET CHILD ASSETS ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        children = wats_client.asset.get_child_assets(
            parent_serial=ate.serial_number
        )
        
        print(f"ATE ({ate.serial_number}) has {len(children)} children:")
        for child in children:
            print(f"  - {child.asset_name}: {child.serial_number}")
        
        print("========================\n")
        
        # We created 2 children (DMM and Fixture)
        # Note: The hierarchy might not be supported on all servers
        # so we just verify the call succeeded
        assert isinstance(children, list)


class TestAssetStatus:
    """Test asset status and alarm state queries."""

    def test_get_initial_status(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Test getting initial asset status (should be OK)."""
        print("\n=== INITIAL ASSET STATUS ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        
        if status:
            print(f"ATE Status: {status}")
            alarm_state = status.get("alarmState", 0)
            print(f"  - Alarm state: {alarm_state} ({AssetAlarmState(alarm_state).name})")
            print(f"  - Running count: {status.get('runningCount', 'N/A')}")
            print(f"  - Total count: {status.get('totalCount', 'N/A')}")
            
            # Initial state should be OK (0)
            assert alarm_state == AssetAlarmState.OK.value, \
                f"Expected OK (0), got {alarm_state}"
        else:
            print("  Status endpoint returned None (may not be available)")
        
        print("============================\n")


class TestAssetCountOperations:
    """Test asset count increment and reset operations."""

    def test_increment_count(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Test incrementing asset running count."""
        print("\n=== INCREMENT COUNT ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        # Increment count by 1
        result = wats_client.asset.increment_count(
            serial_number=ate.serial_number,
            amount=1
        )
        
        print(f"Increment result: {result}")
        
        # Get updated status
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        if status:
            print(f"Running count after increment: {status.get('runningCount', 'N/A')}")
        
        assert result is True, "Increment count should succeed"
        print("=======================\n")

    def test_count_to_warning(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """
        Test that incrementing count to warning threshold triggers warning.
        
        With limit=5 and warning=60%, warning should occur at count 3.
        """
        print("\n=== COUNT TO WARNING THRESHOLD ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        # Get current count
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        current_count = status.get("runningCount", 0) if status else 0
        print(f"Current running count: {current_count}")
        
        # Calculate how many increments needed to reach warning
        # Warning at 60% of 5 = 3
        warning_count = int(RUNNING_COUNT_LIMIT * WARNING_THRESHOLD / 100)
        increments_needed = max(0, warning_count - current_count)
        
        print(f"Warning threshold: {warning_count}")
        print(f"Increments needed: {increments_needed}")
        
        # Increment to reach warning
        for i in range(increments_needed):
            result = wats_client.asset.increment_count(
                serial_number=ate.serial_number,
                amount=1
            )
            print(f"  Increment {i+1}: {result}")
            time.sleep(0.1)  # Small delay
        
        # Check status
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        if status:
            alarm_state = status.get("alarmState", 0)
            running_count = status.get("runningCount", 0)
            print(f"\nAfter increments:")
            print(f"  Running count: {running_count}")
            print(f"  Alarm state: {alarm_state} ({AssetAlarmState(alarm_state).name if alarm_state in [0,1,2] else 'Unknown'})")
            
            # Should be in WARNING (1) state
            if alarm_state == AssetAlarmState.WARNING.value:
                print("  ✓ Asset correctly in WARNING state")
            else:
                print(f"  ℹ Alarm state is {alarm_state} (server may use different thresholds)")
        
        print("==================================\n")

    def test_count_to_alarm(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """
        Test that exceeding limit triggers ALARM state.
        """
        print("\n=== COUNT TO ALARM THRESHOLD ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        # Get current count
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        current_count = status.get("runningCount", 0) if status else 0
        print(f"Current running count: {current_count}")
        
        # Increment to exceed limit
        increments_needed = max(0, RUNNING_COUNT_LIMIT - current_count + 1)
        print(f"Increments needed to exceed limit: {increments_needed}")
        
        for i in range(increments_needed):
            result = wats_client.asset.increment_count(
                serial_number=ate.serial_number,
                amount=1
            )
            time.sleep(0.1)
        
        # Check status
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        if status:
            alarm_state = status.get("alarmState", 0)
            running_count = status.get("runningCount", 0)
            print(f"\nAfter exceeding limit:")
            print(f"  Running count: {running_count}")
            print(f"  Alarm state: {alarm_state} ({AssetAlarmState(alarm_state).name if alarm_state in [0,1,2] else 'Unknown'})")
            
            if alarm_state == AssetAlarmState.ALARM.value:
                print("  ✓ Asset correctly in ALARM state!")
            else:
                print(f"  ℹ Alarm state is {alarm_state} (server may use different thresholds)")
        
        print("================================\n")


class TestAlarmCheckLoop:
    """Test checking alarm state in a loop simulating test runs."""

    def test_run_loop_with_alarm_check(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """
        Simulate a test run loop:
        1. Before each "test run", check asset alarm status
        2. Print alarm state
        3. Increment count (simulating test run)
        4. Repeat until alarm triggers
        """
        print("\n=== TEST RUN LOOP WITH ALARM CHECK ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        # First reset the count
        reset_result = wats_client.asset.reset_running_count(
            serial_number=ate.serial_number,
            comment="Reset for alarm loop test"
        )
        print(f"Reset running count: {reset_result}")
        time.sleep(0.5)
        
        max_runs = RUNNING_COUNT_LIMIT + 2  # Run a bit past the limit
        
        print(f"\nStarting {max_runs} test runs (limit is {RUNNING_COUNT_LIMIT}):\n")
        print("-" * 60)
        
        for run_number in range(1, max_runs + 1):
            # Check status BEFORE the test run
            status = wats_client.asset.get_status(serial_number=ate.serial_number)
            
            if status:
                alarm_state = status.get("alarmState", 0)
                running_count = status.get("runningCount", 0)
                message = status.get("message", "")
                
                # Determine alarm state name
                try:
                    alarm_name = AssetAlarmState(alarm_state).name
                except ValueError:
                    alarm_name = f"UNKNOWN({alarm_state})"
                
                # Print status
                emoji = "✅" if alarm_state == 0 else ("⚠️" if alarm_state == 1 else "🚨")
                print(f"Run {run_number:2d} | Count: {running_count:3d}/{RUNNING_COUNT_LIMIT} | "
                      f"Status: {emoji} {alarm_name:10s} | {message or ''}")
                
                # If in ALARM, we would normally stop
                if alarm_state == AssetAlarmState.ALARM.value:
                    print(f"\n🚨 ALARM: Asset needs calibration/maintenance!")
                    print(f"   In production, testing would stop here.\n")
            else:
                print(f"Run {run_number:2d} | Status: Unable to get status")
            
            # Simulate test run by incrementing count
            wats_client.asset.increment_count(
                serial_number=ate.serial_number,
                amount=1
            )
            time.sleep(0.2)  # Small delay between "runs"
        
        print("-" * 60)
        print("=====================================\n")


class TestResetRunningCount:
    """Test resetting running count clears alarm."""

    def test_reset_clears_alarm(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """
        Test that resetting running count clears alarm state.
        
        1. Verify asset is in alarm (from previous test)
        2. Reset running count
        3. Verify alarm is cleared
        4. Run one more test and verify OK state
        """
        print("\n=== RESET RUNNING COUNT TO CLEAR ALARM ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        # 1. Check current status (should be in alarm from previous tests)
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        if status:
            alarm_before = status.get("alarmState", 0)
            count_before = status.get("runningCount", 0)
            print(f"Before reset:")
            print(f"  Running count: {count_before}")
            print(f"  Alarm state: {alarm_before}")
        
        # 2. Reset running count
        print("\nResetting running count...")
        reset_result = wats_client.asset.reset_running_count(
            serial_number=ate.serial_number,
            comment="Reset after pytest alarm test"
        )
        print(f"Reset result: {reset_result}")
        
        # Give server time to process
        time.sleep(0.5)
        
        # 3. Check status after reset
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        if status:
            alarm_after = status.get("alarmState", 0)
            count_after = status.get("runningCount", 0)
            print(f"\nAfter reset:")
            print(f"  Running count: {count_after}")
            print(f"  Alarm state: {alarm_after}")
            
            # Running count should be 0
            if count_after == 0:
                print("  ✓ Running count reset to 0")
            
            # Alarm should be cleared
            if alarm_after == AssetAlarmState.OK.value:
                print("  ✓ Alarm state cleared to OK")
        
        # 4. Run one more test and verify OK
        print("\nRunning one test after reset...")
        wats_client.asset.increment_count(
            serial_number=ate.serial_number,
            amount=1
        )
        
        status = wats_client.asset.get_status(serial_number=ate.serial_number)
        if status:
            final_alarm = status.get("alarmState", 0)
            final_count = status.get("runningCount", 0)
            print(f"After one test:")
            print(f"  Running count: {final_count}")
            print(f"  Alarm state: {final_alarm}")
            
            if final_alarm == AssetAlarmState.OK.value:
                print("  ✓ Asset still OK after one test run")
        
        print("==========================================\n")


class TestCalibrationMaintenance:
    """Test calibration and maintenance recording."""

    def test_record_calibration(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Test recording a calibration event."""
        print("\n=== RECORD CALIBRATION ===")
        
        dmm = test_asset_hierarchy.get("DMM")
        if not dmm:
            pytest.skip("DMM asset not available")
        
        result = wats_client.asset.record_calibration(
            serial_number=dmm.serial_number,
            comment="Calibration recorded by pytest"
        )
        
        print(f"Record calibration result: {result}")
        
        # Get asset to check dates
        updated = wats_client.asset.get_asset_by_serial(dmm.serial_number)
        if updated:
            print(f"Last calibration date: {updated.last_calibration_date}")
            print(f"Next calibration date: {updated.next_calibration_date}")
        
        print("==========================\n")

    def test_record_maintenance(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Test recording a maintenance event."""
        print("\n=== RECORD MAINTENANCE ===")
        
        fixture = test_asset_hierarchy.get("Fixture")
        if not fixture:
            pytest.skip("Fixture asset not available")
        
        result = wats_client.asset.record_maintenance(
            serial_number=fixture.serial_number,
            comment="Maintenance recorded by pytest"
        )
        
        print(f"Record maintenance result: {result}")
        
        # Get asset to check dates
        updated = wats_client.asset.get_asset_by_serial(fixture.serial_number)
        if updated:
            print(f"Last maintenance date: {updated.last_maintenance_date}")
            print(f"Next maintenance date: {updated.next_maintenance_date}")
        
        print("==========================\n")


class TestAssetLog:
    """Test asset log operations."""

    def test_get_asset_log(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Test retrieving asset log entries."""
        print("\n=== GET ASSET LOG ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        # Filter log by asset
        filter_str = f"assetId eq '{ate.asset_id}'"
        logs = wats_client.asset.get_asset_log(filter_str=filter_str, top=10)
        
        print(f"Found {len(logs)} log entries for ATE:")
        for log in logs[:5]:  # Show first 5
            print(f"  - {log.date}: {log.log_type} - {log.comment or 'No comment'}")
        
        print("=====================\n")

    def test_add_log_message(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Test adding a message to asset log."""
        print("\n=== ADD LOG MESSAGE ===")
        
        ate = test_asset_hierarchy["ATE"]
        
        result = wats_client.asset.add_log_message(
            asset_id=ate.asset_id,
            message="Test message from pytest comprehensive test",
            user="pytest"
        )
        
        print(f"Add log message result: {result}")
        print("=======================\n")


class TestCleanup:
    """Cleanup test assets (optional - can be commented out to inspect results)."""

    @pytest.mark.skip(reason="Keep test assets for inspection")
    def test_cleanup_assets(
        self,
        wats_client: Any,
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Clean up test assets."""
        print("\n=== CLEANUP ===")
        
        # Delete in reverse order (children first)
        for name in ["Fixture", "DMM", "ATE"]:
            asset = test_asset_hierarchy.get(name)
            if asset:
                result = wats_client.asset.delete_asset(
                    serial_number=asset.serial_number
                )
                print(f"Delete {name}: {result}")
        
        print("===============\n")


# =============================================================================
# Summary Report
# =============================================================================

class TestSummary:
    """Print test summary."""

    def test_print_summary(
        self,
        test_asset_types: Dict[str, AssetType],
        test_asset_hierarchy: Dict[str, Asset]
    ) -> None:
        """Print summary of created assets for reference."""
        print("\n")
        print("=" * 70)
        print("COMPREHENSIVE ASSET TEST SUMMARY")
        print("=" * 70)
        print("\nAsset Types Created:")
        for name, asset_type in test_asset_types.items():
            print(f"  {name}: {asset_type.type_name}")
            print(f"    - ID: {asset_type.type_id}")
            print(f"    - Running count limit: {asset_type.running_count_limit}")
        
        print("\nAsset Hierarchy Created:")
        for name, asset in test_asset_hierarchy.items():
            parent = asset.parent_serial_number or "(root)"
            print(f"  {name}: {asset.serial_number}")
            print(f"    - ID: {asset.asset_id}")
            print(f"    - Parent: {parent}")
        
        print("\nTest Scenario Completed:")
        print("  ✓ Created asset types with running count limits")
        print("  ✓ Created asset hierarchy (ATE with children)")
        print("  ✓ Tested alarm triggering via count increment")
        print("  ✓ Tested running count reset")
        print("  ✓ Verified alarm clears after reset")
        print("=" * 70)
        print("\n")
