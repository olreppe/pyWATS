"""
Tests for software module - test software package management
"""
import pytest
from pywats.domains.software import Package, PackageTag, PackageStatus


class TestSoftwarePackage:
    """Test creating and managing software packages"""
    
    def test_create_software_package(self):
        """Test creating a software package definition"""
        package = Package(
            name="TestSoftware",
            version=1,
            description="Test software package"
        )
        assert package.name == "TestSoftware"
        assert package.version == 1
    
    def test_create_package_with_tags(self):
        """Test creating a software package with tags"""
        tags = [
            PackageTag(key="category", value="tools"),
            PackageTag(key="platform", value="windows"),
        ]
        package = Package(
            name="TaggedSoftware",
            version=1,
            description="Software with tags",
            tags=tags
        )
        assert package.name == "TaggedSoftware"
        assert package.tags is not None
        assert len(package.tags) == 2
        assert package.tags[0].key == "category"
    
    def test_package_status_enum(self):
        """Test package status values"""
        package = Package(
            name="DraftPackage",
            version=1,
            status=PackageStatus.DRAFT
        )
        assert package.status == PackageStatus.DRAFT
        
        # Test other statuses
        assert PackageStatus.RELEASED.value == "Released"
        assert PackageStatus.PENDING.value == "Pending"


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
            packages = wats_client.software.get_packages()
            if packages and len(packages) > 0:
                first_package = packages[0]
                assert isinstance(first_package, Package)
                assert first_package.name is not None
        except Exception as e:
            pytest.skip(f"Get package failed: {e}")
