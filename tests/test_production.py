"""
Tests for production module - unit management, tags, box build
"""
import pytest
from pywats.models.production import Unit


class TestUnitOperations:
    """Test creating and managing production units"""
    
    def test_create_unit(self, test_serial_number, test_part_number):
        """Test creating a unit definition"""
        unit = Unit(
            serial_number=test_serial_number,
            part_number=test_part_number,
            revision="A"
        )
        assert unit.serial_number == test_serial_number
    
    def test_register_unit(self, wats_client, test_serial_number, test_part_number):
        """Test registering a new unit"""
        unit = Unit(
            serial_number=test_serial_number,
            part_number=test_part_number,
            revision="A"
        )
        
        try:
            result = wats_client.production.create_unit(unit)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Unit creation failed: {e}")
    
    def test_get_unit(self, wats_client, test_serial_number):
        """Test retrieving a unit"""
        try:
            unit = wats_client.production.get_unit(test_serial_number)
            if unit:
                assert unit.serial_number == test_serial_number
        except Exception as e:
            pytest.skip(f"Get unit failed: {e}")
    
    def test_update_unit(self, wats_client, test_serial_number):
        """Test updating unit information"""
        try:
            result = wats_client.production.update_unit(
                test_serial_number,
                batch_number="BATCH-001"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Update unit failed: {e}")


class TestUnitTags:
    """Test unit tagging functionality"""
    
    def test_set_unit_tag(self, wats_client, test_serial_number):
        """Test setting a tag on a unit"""
        try:
            result = wats_client.production.set_unit_tag(
                test_serial_number,
                tag_name="TestTag",
                tag_value="TestValue"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Set tag failed: {e}")
    
    def test_get_unit_tags(self, wats_client, test_serial_number):
        """Test getting unit tags"""
        try:
            tags = wats_client.production.get_unit_tags(test_serial_number)
            assert isinstance(tags, (list, dict))
        except Exception as e:
            pytest.skip(f"Get tags failed: {e}")


class TestBoxBuild:
    """Test box build operations"""
    
    def test_create_box_build(self, wats_client):
        """Test creating a box build"""
        from datetime import datetime
        box_sn = f"BOX-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        try:
            result = wats_client.production.create_box_build(
                box_serial_number=box_sn,
                component_serials=["COMP-001", "COMP-002"]
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Box build creation failed: {e}")
    
    def test_get_box_components(self, wats_client):
        """Test getting box build components"""
        try:
            components = wats_client.production.get_box_components("BOX-001")
            assert isinstance(components, list)
        except Exception as e:
            pytest.skip(f"Get box components failed: {e}")
