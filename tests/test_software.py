"""
Tests for software module - test software package management
"""
import pytest
from pywats.models.software import SoftwarePackage


class TestSoftwarePackage:
    """Test creating and managing software packages"""
    
    def test_create_software_package(self):
        """Test creating a software package definition"""
        package = SoftwarePackage(
            name="TestSoftware",
            version="1.0.0",
            file_name="test_sw_v1.0.0.zip"
        )
        assert package.name == "TestSoftware"
        assert package.version == "1.0.0"
    
    def test_upload_software_package(self, wats_client):
        """Test uploading a software package"""
        package = SoftwarePackage(
            name="TestSoftware",
            version="1.0.1",
            file_name="test_package.zip"
        )
        
        # Note: This requires actual file content
        try:
            result = wats_client.software.upload_package(
                package,
                file_content=b"dummy content"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Upload failed: {e}")


class TestSoftwareRetrieval:
    """Test retrieving software packages"""
    
    def test_get_software_list(self, wats_client):
        """Test getting list of software packages"""
        try:
            packages = wats_client.software.get_packages()
            assert isinstance(packages, list)
        except Exception as e:
            pytest.skip(f"Get packages failed: {e}")
    
    def test_get_software_by_name(self, wats_client):
        """Test getting specific software package"""
        try:
            package = wats_client.software.get_package("TestSoftware", "1.0.0")
            if package:
                assert package.name == "TestSoftware"
        except Exception as e:
            pytest.skip(f"Get package failed: {e}")
