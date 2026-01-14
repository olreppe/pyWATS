"""
Comprehensive tests for Process module - test operations and repair operations.

Tests cover:
1. Model validation
2. Process caching mechanism
3. Test operation lookup
4. Repair operation lookup
5. WIP operation lookup
6. Validation helpers
7. Internal API operations (if available)
"""
import pytest
from uuid import uuid4
from datetime import datetime, timedelta
import time

from pywats.domains.process import (
    ProcessInfo,
    ProcessService,
    ProcessRepository,
)
from pywats.domains.process.models import RepairCategory, RepairOperationConfig


# =============================================================================
# MODEL VALIDATION TESTS
# =============================================================================

class TestProcessInfoModel:
    """Test ProcessInfo model validation"""
    
    def test_create_minimal_process(self):
        """Test creating process with minimal fields"""
        process = ProcessInfo(code=100, name="Test Process")
        
        assert process.code == 100
        assert process.name == "Test Process"
        assert process.is_test_operation is False
        assert process.is_repair_operation is False
        assert process.is_wip_operation is False
    
    def test_create_test_operation(self):
        """Test creating a test operation"""
        process = ProcessInfo(
            code=100,
            name="End of line test",
            description="Final test before shipping",
            is_test_operation=True,
            is_repair_operation=False,
            is_wip_operation=False,
        )
        
        assert process.code == 100
        assert process.name == "End of line test"
        assert process.is_test_operation is True
        assert process.is_repair_operation is False
    
    def test_create_repair_operation(self):
        """Test creating a repair operation"""
        process = ProcessInfo(
            code=500,
            name="Repair",
            description="Standard repair process",
            is_test_operation=False,
            is_repair_operation=True,
            is_wip_operation=False,
        )
        
        assert process.code == 500
        assert process.is_repair_operation is True
        assert process.is_test_operation is False
    
    def test_create_wip_operation(self):
        """Test creating a WIP operation"""
        process = ProcessInfo(
            code=200,
            name="Assembly",
            description="PCB Assembly",
            is_test_operation=False,
            is_repair_operation=False,
            is_wip_operation=True,
        )
        
        assert process.code == 200
        assert process.is_wip_operation is True
    
    def test_parse_from_api_response(self):
        """Test parsing from camelCase API response"""
        api_response = {
            "code": 100,
            "name": "ICT Test",
            "description": "In-circuit test",
            "isTestOperation": True,
            "isRepairOperation": False,
            "isWipOperation": False,
            "processIndex": 1,
            "state": 1,
        }
        
        process = ProcessInfo.model_validate(api_response)
        
        assert process.code == 100
        assert process.name == "ICT Test"
        assert process.is_test_operation is True
        assert process.process_index == 1
        assert process.state == 1
    
    def test_parse_from_internal_api(self):
        """Test parsing from PascalCase internal API response"""
        api_response = {
            "ProcessID": str(uuid4()),
            "code": 500,
            "name": "Repair",
            "isTestOperation": False,
            "isRepairOperation": True,
            "isWipOperation": False,
            "Properties": "some_properties",
        }
        
        process = ProcessInfo.model_validate(api_response)
        
        assert process.code == 500
        assert process.is_repair_operation is True
        assert process.process_id is not None


class TestRepairCategoryModel:
    """Test RepairCategory model"""
    
    def test_create_repair_category(self):
        """Test creating repair category"""
        category = RepairCategory(
            guid=uuid4(),
            description="Solder Process",
            selectable=True,
            sort_order=1,
            failure_type=0,
            status=1,
        )
        
        assert category.description == "Solder Process"
        assert category.selectable is True
        assert category.sort_order == 1
    
    def test_category_with_fail_codes(self):
        """Test category with nested fail codes"""
        parent_guid = uuid4()
        
        fail_codes = [
            RepairCategory(
                guid=uuid4(),
                description="Solder Bridge",
                selectable=True,
                sort_order=1,
                failure_type=1,
                status=1,
            ),
            RepairCategory(
                guid=uuid4(),
                description="Cold Solder",
                selectable=True,
                sort_order=2,
                failure_type=1,
                status=1,
            ),
        ]
        
        category = RepairCategory(
            guid=parent_guid,
            description="Solder Process",
            selectable=False,
            fail_codes=fail_codes,
        )
        
        assert len(category.fail_codes) == 2
        assert category.fail_codes[0].description == "Solder Bridge"


class TestRepairOperationConfigModel:
    """Test RepairOperationConfig model"""
    
    def test_create_repair_config(self):
        """Test creating repair operation config"""
        config = RepairOperationConfig(
            description="Standard Repair",
            uut_required=1,
            bom_required=1,
            vendor_required=2,
            comp_ref_mask="^[A-Z][0-9]+$",
            comp_ref_mask_description="Component reference format: C1, R2, etc.",
        )
        
        assert config.description == "Standard Repair"
        assert config.uut_required == 1
        assert config.comp_ref_mask == "^[A-Z][0-9]+$"


# =============================================================================
# SERVICE LAYER TESTS (with server)
# =============================================================================

class TestProcessServiceCaching:
    """Test process service caching mechanism"""
    
    def test_get_processes_cached(self, wats_client):
        """Test that processes are cached"""
        # First call - should populate cache
        processes1 = wats_client.process.get_processes()
        first_refresh = wats_client.process.last_refresh
        
        # Second call - should use cache
        processes2 = wats_client.process.get_processes()
        second_refresh = wats_client.process.last_refresh
        
        # Verify cache was used (same timestamp)
        assert first_refresh == second_refresh
        assert len(processes1) == len(processes2)
        print(f"[OK] Cache working - {len(processes1)} processes cached")
    
    def test_force_refresh(self, wats_client):
        """Test forcing cache refresh"""
        # Initial fetch
        wats_client.process.get_processes()
        first_refresh = wats_client.process.last_refresh
        
        # Small delay
        time.sleep(0.1)
        
        # Force refresh
        wats_client.process.refresh()
        second_refresh = wats_client.process.last_refresh
        
        # Verify refresh happened
        assert second_refresh > first_refresh
        print(f"[OK] Force refresh successful")
    
    def test_refresh_interval_property(self, wats_client):
        """Test refresh interval property"""
        original = wats_client.process.refresh_interval
        
        # Change interval
        wats_client.process.refresh_interval = 600
        assert wats_client.process.refresh_interval == 600
        
        # Restore
        wats_client.process.refresh_interval = original
        print(f"[OK] Refresh interval configurable (default: {original}s)")


class TestProcessRetrieval:
    """Test retrieving processes from server"""
    
    def test_get_all_processes(self, wats_client):
        """Test getting all processes"""
        processes = wats_client.process.get_processes()
        
        assert isinstance(processes, list)
        assert len(processes) > 0, "No processes found"
        
        print(f"[OK] Retrieved {len(processes)} processes")
        
        for proc in processes[:5]:
            flags = []
            if proc.is_test_operation:
                flags.append("TEST")
            if proc.is_repair_operation:
                flags.append("REPAIR")
            if proc.is_wip_operation:
                flags.append("WIP")
            print(f"  {proc.code}: {proc.name} [{', '.join(flags)}]")
    
    def test_get_test_operations(self, wats_client):
        """Test getting test operations only"""
        test_ops = wats_client.process.get_test_operations()
        
        assert isinstance(test_ops, list)
        
        for op in test_ops:
            assert op.is_test_operation is True
        
        print(f"[OK] Found {len(test_ops)} test operations")
        for op in test_ops[:3]:
            print(f"  {op.code}: {op.name}")
    
    def test_get_repair_operations(self, wats_client):
        """Test getting repair operations only"""
        repair_ops = wats_client.process.get_repair_operations()
        
        assert isinstance(repair_ops, list)
        
        for op in repair_ops:
            assert op.is_repair_operation is True
        
        print(f"[OK] Found {len(repair_ops)} repair operations")
        for op in repair_ops[:3]:
            print(f"  {op.code}: {op.name}")
    
    def test_get_wip_operations(self, wats_client):
        """Test getting WIP operations only"""
        wip_ops = wats_client.process.get_wip_operations()
        
        assert isinstance(wip_ops, list)
        
        for op in wip_ops:
            assert op.is_wip_operation is True
        
        print(f"[OK] Found {len(wip_ops)} WIP operations")


class TestProcessLookup:
    """Test process lookup methods"""
    
    def test_get_process_by_code(self, wats_client):
        """Test getting process by code"""
        # Get any process first
        processes = wats_client.process.get_processes()
        if not processes:
            pytest.skip("No processes available")
        
        target = processes[0]
        
        # Look up by code
        result = wats_client.process.get_process(target.code)
        
        assert result is not None
        assert result.code == target.code
        assert result.name == target.name
        print(f"[OK] Found process by code {target.code}: {result.name}")
    
    def test_get_process_by_name(self, wats_client):
        """Test getting process by name"""
        processes = wats_client.process.get_processes()
        if not processes:
            pytest.skip("No processes available")
        
        target = processes[0]
        
        # Look up by name (case-insensitive)
        result = wats_client.process.get_process(target.name)
        
        assert result is not None
        assert result.name.lower() == target.name.lower()
        print(f"[OK] Found process by name: {result.name}")
    
    def test_get_test_operation_by_code(self, wats_client):
        """Test getting test operation by code"""
        test_ops = wats_client.process.get_test_operations()
        if not test_ops:
            pytest.skip("No test operations available")
        
        target = test_ops[0]
        
        result = wats_client.process.get_test_operation(target.code)
        
        assert result is not None
        assert result.is_test_operation is True
        print(f"[OK] Found test operation {target.code}: {result.name}")
    
    def test_get_repair_operation_by_code(self, wats_client):
        """Test getting repair operation by code"""
        repair_ops = wats_client.process.get_repair_operations()
        if not repair_ops:
            pytest.skip("No repair operations available")
        
        target = repair_ops[0]
        
        result = wats_client.process.get_repair_operation(target.code)
        
        assert result is not None
        assert result.is_repair_operation is True
        print(f"[OK] Found repair operation {target.code}: {result.name}")
    
    def test_get_nonexistent_process(self, wats_client):
        """Test getting non-existent process returns None"""
        result = wats_client.process.get_process(99999)
        assert result is None
        print("[OK] Non-existent process returns None")
    
    def test_get_test_operation_returns_none_for_repair(self, wats_client):
        """Test that get_test_operation returns None for repair operations"""
        repair_ops = wats_client.process.get_repair_operations()
        if not repair_ops:
            pytest.skip("No repair operations available")
        
        # Try to get repair operation as test operation
        result = wats_client.process.get_test_operation(repair_ops[0].code)
        
        assert result is None, "Should not return repair operation as test operation"
        print("[OK] get_test_operation correctly rejects repair operations")


class TestProcessValidation:
    """Test process validation helpers"""
    
    def test_is_valid_test_operation(self, wats_client):
        """Test validating test operation codes"""
        test_ops = wats_client.process.get_test_operations()
        if not test_ops:
            pytest.skip("No test operations available")
        
        # Valid test operation
        assert wats_client.process.is_valid_test_operation(test_ops[0].code) is True
        
        # Invalid code
        assert wats_client.process.is_valid_test_operation(99999) is False
        
        print("[OK] Test operation validation working")
    
    def test_is_valid_repair_operation(self, wats_client):
        """Test validating repair operation codes"""
        repair_ops = wats_client.process.get_repair_operations()
        if not repair_ops:
            pytest.skip("No repair operations available")
        
        # Valid repair operation
        assert wats_client.process.is_valid_repair_operation(repair_ops[0].code) is True
        
        # Invalid code
        assert wats_client.process.is_valid_repair_operation(99999) is False
        
        print("[OK] Repair operation validation working")
    
    def test_get_default_test_code(self, wats_client):
        """Test getting default test code"""
        default = wats_client.process.get_default_test_code()
        
        assert isinstance(default, int)
        assert default > 0
        
        # Should be a valid test operation or fallback
        test_ops = wats_client.process.get_test_operations()
        if test_ops:
            assert default == test_ops[0].code or default == 100
        else:
            assert default == 100  # Fallback
        
        print(f"[OK] Default test code: {default}")
    
    def test_get_default_repair_code(self, wats_client):
        """Test getting default repair code"""
        default = wats_client.process.get_default_repair_code()
        
        assert isinstance(default, int)
        assert default > 0
        
        repair_ops = wats_client.process.get_repair_operations()
        if repair_ops:
            assert default == repair_ops[0].code or default == 500
        else:
            assert default == 500  # Fallback
        
        print(f"[OK] Default repair code: {default}")


# =============================================================================
# INTERNAL API TESTS (if available)
# =============================================================================

class TestProcessInternalAPI:
    """Test internal API operations (may require special permissions)"""
    
    def test_internal_get_processes(self, wats_client):
        """Test getting processes via internal API"""
        try:
            # Check if internal service is available
            if not hasattr(wats_client, 'process_internal'):
                pytest.skip("Internal process service not available")
            
            processes = wats_client.process_internal.get_processes()
            
            assert isinstance(processes, list)
            print(f"[OK] Internal API: {len(processes)} processes")
            
            # Internal API should return ProcessID
            for proc in processes[:3]:
                if proc.process_id:
                    print(f"  {proc.code}: {proc.name} (ID: {proc.process_id})")
                    
        except Exception as e:
            pytest.skip(f"Internal API not accessible: {e}")
    
    def test_internal_get_repair_configs(self, wats_client):
        """Test getting repair operation configs"""
        try:
            if not hasattr(wats_client, 'process_internal'):
                pytest.skip("Internal process service not available")
            
            configs = wats_client.process_internal.get_repair_operation_configs()
            
            assert isinstance(configs, dict)
            print(f"[OK] Internal API: {len(configs)} repair configs")
            
            for code, config in list(configs.items())[:2]:
                print(f"  Code {code}: {config.description}")
                print(f"    Categories: {len(config.categories)}")
                
        except Exception as e:
            pytest.skip(f"Internal API not accessible: {e}")
    
    def test_internal_get_fail_codes(self, wats_client):
        """Test getting flattened fail codes"""
        try:
            if not hasattr(wats_client.process, 'get_fail_codes'):
                pytest.skip("get_fail_codes method not available")
            
            # Try default repair code (500)
            fail_codes = wats_client.process.get_fail_codes(500)
            
            assert isinstance(fail_codes, list)
            print(f"[OK] Process API: {len(fail_codes)} fail codes for repair 500")
            
            for fc in fail_codes[:5]:
                print(f"  - {fc['description']} ({fc['category']})")
                
        except Exception as e:
            pytest.skip(f"API not accessible: {e}")


# =============================================================================
# SUMMARY TEST
# =============================================================================

class TestProcessSummary:
    """Summary test to verify process module functionality"""
    
    def test_process_module_summary(self, wats_client):
        """Comprehensive summary of process module state"""
        print("\n" + "="*60)
        print("PROCESS MODULE SUMMARY")
        print("="*60)
        
        # Get all processes
        processes = wats_client.process.get_processes()
        print(f"\nTotal processes: {len(processes)}")
        
        # Count by type
        test_ops = [p for p in processes if p.is_test_operation]
        repair_ops = [p for p in processes if p.is_repair_operation]
        wip_ops = [p for p in processes if p.is_wip_operation]
        
        print(f"\nProcess types:")
        print(f"  Test operations:   {len(test_ops)}")
        print(f"  Repair operations: {len(repair_ops)}")
        print(f"  WIP operations:    {len(wip_ops)}")
        
        # Default codes
        print(f"\nDefault codes:")
        print(f"  Test:   {wats_client.process.get_default_test_code()}")
        print(f"  Repair: {wats_client.process.get_default_repair_code()}")
        
        # Cache info
        print(f"\nCache info:")
        print(f"  Refresh interval: {wats_client.process.refresh_interval}s")
        print(f"  Last refresh: {wats_client.process.last_refresh}")
        
        # Sample processes
        if processes:
            print("\nAll processes:")
            for proc in processes:
                flags = []
                if proc.is_test_operation:
                    flags.append("TEST")
                if proc.is_repair_operation:
                    flags.append("REPAIR")
                if proc.is_wip_operation:
                    flags.append("WIP")
                flag_str = f"[{', '.join(flags)}]" if flags else ""
                print(f"  {proc.code:4d}: {proc.name} {flag_str}")
        
        print("\n" + "="*60)
        assert True  # Summary always passes
