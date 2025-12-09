"""
Tests for production module - unit management and serial numbers

These tests make actual API calls to the WATS server.
"""
from typing import Any
from datetime import datetime, timezone
import pytest
from pywats.domains.production import Unit
from pywats.core.exceptions import NotFoundError


class TestUnitModel:
    """Test Unit model creation (no server)"""

    def test_create_unit_model(
        self, test_serial_number: str, test_part_number: str
    ) -> None:
        """Test creating a unit model object"""
        unit = Unit(
            serial_number=test_serial_number,
            part_number=test_part_number,
            revision="A"
        )
        assert unit.serial_number == test_serial_number
        assert unit.part_number == test_part_number


class TestUnitRetrieval:
    """Test retrieving units from server"""

    def test_get_unit(self, wats_client: Any) -> None:
        """Test getting a specific unit - may not exist in test database"""
        print("\n=== GET UNIT ===")
        
        # We need to know an existing serial number and part number
        # Try to get from report headers first
        headers = wats_client.report.query_uut_headers()
        if not headers:
            pytest.skip("No report headers available to find unit")
        
        header = headers[0]
        serial_number = header.serial_number
        part_number = header.part_number
        
        print(f"Looking up unit: {serial_number} / {part_number}")
        
        try:
            unit = wats_client.production.get_unit(serial_number, part_number)
            print(f"Found unit: {unit}")
        except NotFoundError:
            print("Unit not tracked in production system (expected for test data)")
            unit = None
        
        print("================\n")
        
        # Test passes if call completed without unexpected errors


class TestUnitVerification:
    """Test unit verification operations"""

    def test_verify_unit(self, wats_client: Any) -> None:
        """Test verifying a unit"""
        print("\n=== VERIFY UNIT ===")
        
        # Get a known unit from report headers
        headers = wats_client.report.query_uut_headers()
        if not headers:
            pytest.skip("No report headers available")
        
        header = headers[0]
        print(f"Verifying: {header.serial_number} / {header.part_number}")
        
        result = wats_client.production.verify_unit(
            serial_number=header.serial_number,
            part_number=header.part_number
        )
        
        print(f"Verification result: {result}")
        print("===================\n")
        
        # Result might be None if verification not available

    def test_is_unit_passing(self, wats_client: Any) -> None:
        """Test checking if unit is passing"""
        print("\n=== IS UNIT PASSING ===")
        
        headers = wats_client.report.query_uut_headers()
        if not headers:
            pytest.skip("No report headers available")
        
        header = headers[0]
        print(f"Checking: {header.serial_number} / {header.part_number}")
        
        is_passing = wats_client.production.is_unit_passing(
            serial_number=header.serial_number,
            part_number=header.part_number
        )
        
        print(f"Is passing: {is_passing}")
        print("=======================\n")


class TestSerialNumberTypes:
    """Test serial number type operations"""

    def test_get_serial_number_types(self, wats_client: Any) -> None:
        """Test getting serial number types"""
        print("\n=== GET SERIAL NUMBER TYPES ===")
        
        types = wats_client.production.get_serial_number_types()
        
        print(f"Retrieved {len(types)} serial number types")
        for t in types[:5]:
            print(f"  - {t.name}: identifier={t.identifier}, format={t.format}")
        print("===============================\n")
        
        assert isinstance(types, list)


class TestUnitChanges:
    """Test unit change tracking"""

    def test_get_unit_changes(self, wats_client: Any) -> None:
        """Test getting unit changes - may not exist for test units"""
        print("\n=== GET UNIT CHANGES ===")
        
        # Get a known unit
        headers = wats_client.report.query_uut_headers()
        if not headers:
            pytest.skip("No report headers available")
        
        header = headers[0]
        print(f"Getting changes for: {header.serial_number} / {header.part_number}")
        
        try:
            changes = wats_client.production.get_unit_changes(
                serial_number=header.serial_number,
                part_number=header.part_number
            )
            print(f"Found {len(changes)} changes")
            assert isinstance(changes, list)
        except NotFoundError:
            print("Unit changes not available (expected for test data)")
            changes = []
        
        print("========================\n")


class TestAssemblyOperations:
    """Test assembly relationship operations"""

    def test_verify_assembly(self, wats_client: Any) -> None:
        """Test verifying an assembly - may not exist for test units"""
        print("\n=== VERIFY ASSEMBLY ===")
        
        # Get a known unit
        headers = wats_client.report.query_uut_headers()
        if not headers:
            pytest.skip("No report headers available")
        
        header = headers[0]
        revision = header.revision or "A"  # Default to "A" if no revision
        print(f"Verifying assembly: {header.serial_number} / {header.part_number} / {revision}")
        
        try:
            result = wats_client.production.verify_assembly(
                serial_number=header.serial_number,
                part_number=header.part_number,
                revision=revision
            )
            print(f"Assembly verification: {result}")
        except NotFoundError:
            print("Assembly not configured (expected for test data)")
            result = None
        
        print("=======================\n")


class TestSerialNumberAllocation:
    """Test serial number allocation from all types"""

    def test_allocate_serial_numbers_from_all_types(self, wats_client: Any) -> None:
        """
        Test allocating serial numbers from each available type.
        
        This test verifies the allocation API works correctly.
        If pools are empty (NotFoundError), that's an expected server state.
        If pools have serial numbers, we verify allocation succeeds.
        """
        print("\n=== ALLOCATE SERIAL NUMBERS FROM ALL TYPES ===")
        
        # First get all serial number types
        types = wats_client.production.get_serial_number_types()
        
        if not types:
            pytest.skip("No serial number types configured on server")
        
        print(f"Found {len(types)} serial number types")
        
        allocated_serials = {}
        empty_pools = {}
        unexpected_errors = {}
        
        for sn_type in types:
            type_name = sn_type.name
            print(f"\n  Allocating from type: {type_name}")
            
            try:
                # Allocate 1 serial number from each type
                serial_numbers = wats_client.production.allocate_serial_numbers(
                    type_name=type_name,
                    count=1
                )
                
                if serial_numbers:
                    allocated_serials[type_name] = serial_numbers
                    print(f"    ✓ Allocated: {serial_numbers}")
                else:
                    empty_pools[type_name] = "Empty response"
                    print(f"    - No serial numbers available in pool")
                    
            except NotFoundError:
                # Pool is empty - this is expected for test environments
                empty_pools[type_name] = "Pool empty (NotFoundError)"
                print(f"    - Pool empty (no serial numbers pre-loaded)")
                    
            except Exception as e:
                # Unexpected error - track it
                unexpected_errors[type_name] = str(e)
                print(f"    ✗ Unexpected error: {e}")
        
        print(f"\n=== SUMMARY ===")
        print(f"  Successful allocations: {len(allocated_serials)}")
        print(f"  Empty pools: {len(empty_pools)}")
        print(f"  Unexpected errors: {len(unexpected_errors)}")
        
        if allocated_serials:
            print(f"\n  Allocated serial numbers:")
            for type_name, serials in allocated_serials.items():
                print(f"    {type_name}: {serials}")
        
        if empty_pools:
            print(f"\n  Empty pools (expected for test environment):")
            for type_name, reason in empty_pools.items():
                print(f"    {type_name}: {reason}")
        
        if unexpected_errors:
            print(f"\n  Unexpected errors:")
            for type_name, error in unexpected_errors.items():
                print(f"    {type_name}: {error}")
        
        print("================================================\n")
        
        # Fail if we had unexpected errors (not NotFoundError)
        assert len(unexpected_errors) == 0, f"Unexpected errors: {unexpected_errors}"
        
        # At least verify we tested something
        assert len(types) > 0, "Should have tested at least one serial number type"
        assert (len(allocated_serials) + len(empty_pools)) == len(types), \
            "All types should have been attempted"
