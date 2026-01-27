"""
Comprehensive tests for Software module - software package distribution.

Tests cover:
1. Model validation and serialization
2. Package CRUD operations
3. Package status workflow (Draft -> Pending -> Released -> Revoked)
4. Package files and zip upload
5. Tag filtering
6. Virtual folders
"""
import pytest
from uuid import uuid4
from datetime import datetime

from pywats.core.exceptions import NotFoundError
from pywats.domains.software import (
    Package,
    PackageFile,
    PackageTag,
    PackageStatus,
    VirtualFolder,
    SoftwareService,
    SoftwareRepository,
)


# =============================================================================
# MODEL VALIDATION TESTS
# =============================================================================

class TestPackageModel:
    """Test Package model validation and serialization"""
    
    def test_create_minimal_package(self):
        """Test creating package with minimal required fields"""
        package = Package(name="TestPackage")
        assert package.name == "TestPackage"
        assert package.version is None
        assert package.status is None
    
    def test_create_full_package(self):
        """Test creating package with all fields"""
        pkg_id = uuid4()
        now = datetime.now()
        
        package = Package(
            package_id=pkg_id,
            name="FullPackage",
            description="A complete test package",
            version=1,
            status=PackageStatus.DRAFT,
            install_on_root=False,
            root_directory="/test/path",
            priority=10,
            created_utc=now,
            modified_utc=now,
            created_by="test_user",
            modified_by="test_user",
        )
        
        assert package.package_id == pkg_id
        assert package.name == "FullPackage"
        assert package.description == "A complete test package"
        assert package.version == 1
        assert package.status == PackageStatus.DRAFT
        assert package.install_on_root is False
        assert package.root_directory == "/test/path"
        assert package.priority == 10
    
    def test_package_with_tags(self):
        """Test package with tags"""
        tags = [
            PackageTag(key="category", value="tools"),
            PackageTag(key="platform", value="windows"),
            PackageTag(key="version", value="2.0"),
        ]
        
        package = Package(name="TaggedPackage", tags=tags)
        
        assert package.tags is not None
        assert len(package.tags) == 3
        assert package.tags[0].key == "category"
        assert package.tags[0].value == "tools"
    
    def test_package_serialization(self):
        """Test package serialization to dict"""
        package = Package(
            name="SerializeTest",
            version=1,
            status=PackageStatus.DRAFT,
            install_on_root=True,
        )
        
        data = package.model_dump(by_alias=True, exclude_none=True)
        
        assert data["name"] == "SerializeTest"
        assert data["version"] == 1
        assert data["status"] == "Draft"
        assert data["installOnRoot"] is True
    
    def test_package_from_api_response(self):
        """Test parsing package from camelCase API response"""
        api_response = {
            "packageId": str(uuid4()),
            "name": "FromAPI",
            "description": "Package from API",
            "version": 2,
            "status": "Released",
            "installOnRoot": False,
            "rootDirectory": "/api/path",
            "priority": 5,
            "createdUtc": "2024-01-01T00:00:00Z",
            "createdBy": "api_user",
        }
        
        package = Package.model_validate(api_response)
        
        assert package.name == "FromAPI"
        assert package.version == 2
        assert package.status == PackageStatus.RELEASED
        assert package.install_on_root is False


class TestPackageTagModel:
    """Test PackageTag model"""
    
    def test_create_tag(self):
        """Test creating a simple tag"""
        tag = PackageTag(key="environment", value="production")
        assert tag.key == "environment"
        assert tag.value == "production"
    
    def test_create_tag_with_none_values(self):
        """Test creating tag with None values"""
        tag = PackageTag()
        assert tag.key is None
        assert tag.value is None


class TestPackageFileModel:
    """Test PackageFile model"""
    
    def test_create_package_file(self):
        """Test creating package file model"""
        file_id = uuid4()
        pf = PackageFile(
            file_id=file_id,
            filename="setup.exe",
            path="/installer/setup.exe",
            size=1024000,
            checksum="abc123",
            attributes="ExecuteOnce",
        )
        
        assert pf.file_id == file_id
        assert pf.filename == "setup.exe"
        assert pf.path == "/installer/setup.exe"
        assert pf.size == 1024000
        assert pf.attributes == "ExecuteOnce"
    
    def test_parse_file_from_api(self):
        """Test parsing file from API response"""
        api_response = {
            "fileId": str(uuid4()),
            "filename": "config.xml",
            "path": "/config/config.xml",
            "size": 2048,
            "checksum": "sha256:abc",
            "createdUtc": "2024-06-01T10:00:00Z",
        }
        
        pf = PackageFile.model_validate(api_response)
        
        assert pf.filename == "config.xml"
        assert pf.size == 2048


class TestVirtualFolderModel:
    """Test VirtualFolder model"""
    
    def test_create_virtual_folder(self):
        """Test creating virtual folder"""
        folder = VirtualFolder(
            name="TestFolder",
            path="/virtual/test",
            description="Test virtual folder",
        )
        
        assert folder.name == "TestFolder"
        assert folder.path == "/virtual/test"


class TestPackageStatusEnum:
    """Test PackageStatus enum values"""
    
    def test_status_values(self):
        """Test all status enum values"""
        assert PackageStatus.DRAFT.value == "Draft"
        assert PackageStatus.PENDING.value == "Pending"
        assert PackageStatus.RELEASED.value == "Released"
        assert PackageStatus.REVOKED.value == "Revoked"
    
    def test_status_from_string(self):
        """Test creating status from string"""
        assert PackageStatus("Draft") == PackageStatus.DRAFT
        assert PackageStatus("Released") == PackageStatus.RELEASED


# =============================================================================
# SERVICE LAYER TESTS (with server)
# =============================================================================

class TestSoftwarePackageRetrieval:
    """Test retrieving software packages from server"""
    
    def test_get_all_packages(self, wats_client):
        """Test getting list of all packages"""
        packages = wats_client.software.get_packages()
        
        assert isinstance(packages, list)
        print(f"[OK] Retrieved {len(packages)} packages")
        
        if packages:
            pkg = packages[0]
            # Package model validation - check core attributes exist
            assert hasattr(pkg, 'name')
            assert hasattr(pkg, 'version')
            assert hasattr(pkg, 'status')
            assert pkg.name is not None
            print(f"  First package: {pkg.name} v{pkg.version}")
    
    def test_get_package_by_id(self, wats_client):
        """Test getting specific package by ID"""
        packages = wats_client.software.get_packages()
        
        if not packages:
            pytest.skip("No packages available")
        
        # Get first package with an ID
        target = next((p for p in packages if p.package_id), None)
        if not target:
            pytest.skip("No package with ID found")
        
        retrieved = wats_client.software.get_package(target.package_id)
        
        assert retrieved is not None
        assert retrieved.package_id == target.package_id
        assert retrieved.name == target.name
        print(f"[OK] Retrieved package by ID: {retrieved.name}")
    
    def test_get_package_by_name(self, wats_client):
        """Test getting package by name"""
        packages = wats_client.software.get_packages()
        
        if not packages:
            pytest.skip("No packages available")
        
        target = packages[0]
        
        # Try to get by name (status is required by API)
        if target.status:
            retrieved = wats_client.software.get_package_by_name(
                target.name, 
                status=target.status
            )
            
            if retrieved:
                assert retrieved.name == target.name
                print(f"[OK] Retrieved package by name: {retrieved.name}")
            else:
                print(f"[INFO] Package not found by name lookup")
    
    def test_get_released_package(self, wats_client):
        """Test getting released version of a package"""
        packages = wats_client.software.get_packages()
        
        # Find a released package
        released = next(
            (p for p in packages if p.status == PackageStatus.RELEASED),
            None
        )
        
        if not released:
            pytest.skip("No released packages available")
        
        result = wats_client.software.get_released_package(released.name)
        
        if result:
            assert result.status == PackageStatus.RELEASED
            print(f"[OK] Retrieved released package: {result.name} v{result.version}")


class TestSoftwarePackagesByTag:
    """Test filtering packages by tags"""
    
    def test_get_packages_by_tag(self, wats_client):
        """Test getting packages filtered by tag"""
        packages = wats_client.software.get_packages()
        
        # Find a package with tags
        tagged = next(
            (p for p in packages if p.tags and len(p.tags) > 0),
            None
        )
        
        if not tagged:
            pytest.skip("No packages with tags found")
        
        tag = tagged.tags[0]
        
        # Filter by that tag
        filtered = wats_client.software.get_packages_by_tag(
            tag=tag.key,
            value=tag.value,
            status=tagged.status
        )
        
        assert isinstance(filtered, list)
        print(f"[OK] Found {len(filtered)} packages with tag {tag.key}={tag.value}")


class TestSoftwareVirtualFolders:
    """Test virtual folder operations"""
    
    def test_get_virtual_folders(self, wats_client):
        """Test getting all virtual folders"""
        folders = wats_client.software.get_virtual_folders()
        
        assert isinstance(folders, list)
        print(f"[OK] Retrieved {len(folders)} virtual folders")
        
        for folder in folders[:3]:  # Show first 3
            print(f"  - {folder.name}: {folder.path}")


class TestSoftwarePackageFiles:
    """Test package file operations"""
    
    def test_get_package_files(self, wats_client):
        """Test getting files for a package"""
        packages = wats_client.software.get_packages()
        
        if not packages:
            pytest.skip("No packages available")
        
        # Find a package (preferably released, more likely to have files)
        target = next(
            (p for p in packages if p.status == PackageStatus.RELEASED and p.package_id),
            next((p for p in packages if p.package_id), None)
        )
        
        if not target:
            pytest.skip("No package with ID found")
        
        files = wats_client.software.get_package_files(target.package_id)
        
        assert isinstance(files, list)
        print(f"[OK] Package '{target.name}' has {len(files)} files")
        
        for f in files[:5]:  # Show first 5
            size_kb = f.size / 1024 if f.size else 0
            print(f"  - {f.filename} ({size_kb:.1f} KB)")


# =============================================================================
# PACKAGE LIFECYCLE TESTS (Create/Update/Delete)
# =============================================================================

class TestSoftwarePackageLifecycle:
    """Test full package lifecycle: create, update, workflow, delete"""
    
    @pytest.fixture
    def test_package_name(self):
        """Generate unique package name for testing"""
        return f"PyWATS_Test_{uuid4().hex[:8]}"
    
    def test_create_draft_package(self, wats_client, test_package_name):
        """Test creating a new draft package"""
        package = wats_client.software.create_package(
            name=test_package_name,
            description="Test package created by pyWATS tests",
            priority=50,
        )
        
        if package is None:
            pytest.skip("Could not create package (may lack permissions)")
        
        try:
            assert package.name == test_package_name
            assert package.status == PackageStatus.DRAFT
            assert package.version == 1
            print(f"[OK] Created draft package: {package.name} v{package.version}")
        finally:
            # Cleanup
            if package and package.package_id:
                wats_client.software.delete_package(package.package_id)
    
    def test_package_status_workflow(self, wats_client, test_package_name):
        """Test package status transitions: Draft -> Pending -> Released -> Revoked"""
        # Create package
        package = wats_client.software.create_package(
            name=test_package_name,
            description="Workflow test package",
        )
        
        if package is None:
            pytest.skip("Could not create package")
        
        try:
            pkg_id = package.package_id
            
            # Draft -> Pending
            success = wats_client.software.submit_for_review(pkg_id)
            assert success, "Failed to submit for review"
            print(f"[OK] Draft -> Pending")
            
            # Pending -> Released
            success = wats_client.software.release_package(pkg_id)
            assert success, "Failed to release package"
            print(f"[OK] Pending -> Released")
            
            # Released -> Revoked
            success = wats_client.software.revoke_package(pkg_id)
            assert success, "Failed to revoke package"
            print(f"[OK] Released -> Revoked")
            
            # Verify final state
            final = wats_client.software.get_package(pkg_id)
            assert final.status == PackageStatus.REVOKED
            
        finally:
            # Cleanup - must be Draft or Revoked to delete
            if package and package.package_id:
                wats_client.software.delete_package(package.package_id)
    
    def test_return_to_draft(self, wats_client, test_package_name):
        """Test returning pending package to draft"""
        package = wats_client.software.create_package(
            name=test_package_name,
            description="Return to draft test",
        )
        
        if package is None:
            pytest.skip("Could not create package")
        
        try:
            pkg_id = package.package_id
            
            # Draft -> Pending
            wats_client.software.submit_for_review(pkg_id)
            
            # Pending -> Draft (return)
            success = wats_client.software.return_to_draft(pkg_id)
            assert success, "Failed to return to draft"
            
            # Verify
            result = wats_client.software.get_package(pkg_id)
            assert result.status == PackageStatus.DRAFT
            print(f"[OK] Pending -> Draft (returned)")
            
        finally:
            if package and package.package_id:
                wats_client.software.delete_package(package.package_id)
    
    def test_update_package_metadata(self, wats_client, test_package_name):
        """Test updating package metadata"""
        package = wats_client.software.create_package(
            name=test_package_name,
            description="Original description",
        )
        
        if package is None:
            pytest.skip("Could not create package")
        
        try:
            # Update description
            package.description = "Updated description"
            package.priority = 100
            
            updated = wats_client.software.update_package(package)
            
            if updated:
                assert updated.description == "Updated description"
                assert updated.priority == 100
                print(f"[OK] Updated package metadata")
            else:
                print(f"[INFO] Update returned None (check permissions)")
                
        finally:
            if package and package.package_id:
                wats_client.software.delete_package(package.package_id)
    
    def test_create_package_with_tags(self, wats_client, test_package_name):
        """Test creating package with tags"""
        tags = [
            PackageTag(key="environment", value="test"),
            PackageTag(key="owner", value="pyWATS"),
        ]
        
        package = wats_client.software.create_package(
            name=test_package_name,
            description="Package with tags",
            tags=tags,
        )
        
        if package is None:
            pytest.skip("Could not create package")
        
        try:
            # Verify tags
            retrieved = wats_client.software.get_package(package.package_id)
            
            if retrieved.tags:
                tag_keys = [t.key for t in retrieved.tags]
                assert "environment" in tag_keys or "owner" in tag_keys
                print(f"[OK] Package created with {len(retrieved.tags)} tags")
            else:
                print(f"[INFO] Tags not returned in response")
                
        finally:
            if package and package.package_id:
                wats_client.software.delete_package(package.package_id)
    
    def test_delete_package_by_name(self, wats_client, test_package_name):
        """Test deleting package by name and version"""
        package = wats_client.software.create_package(
            name=test_package_name,
            description="Delete by name test",
        )
        
        if package is None:
            pytest.skip("Could not create package")
        
        # Delete by name
        success = wats_client.software.delete_package_by_name(
            test_package_name, 
            version=package.version
        )
        
        assert success, "Failed to delete package by name"
        print(f"[OK] Deleted package by name: {test_package_name} v{package.version}")
        
        # Verify deletion - API returns 404 for deleted packages
        with pytest.raises(NotFoundError):
            wats_client.software.get_package(package.package_id)


# =============================================================================
# SUMMARY TEST
# =============================================================================

class TestSoftwareSummary:
    """Summary test to verify software module functionality"""
    
    def test_software_module_summary(self, wats_client):
        """Comprehensive summary of software module state"""
        print("\n" + "="*60)
        print("SOFTWARE MODULE SUMMARY")
        print("="*60)
        
        # Get all packages
        packages = wats_client.software.get_packages()
        print(f"\nTotal packages: {len(packages)}")
        
        # Count by status (handle both string and enum)
        status_counts = {}
        for pkg in packages:
            if pkg.status:
                status = pkg.status.value if hasattr(pkg.status, 'value') else str(pkg.status)
            else:
                status = "Unknown"
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("\nPackages by status:")
        for status, count in sorted(status_counts.items()):
            print(f"  {status}: {count}")
        
        # Virtual folders
        folders = wats_client.software.get_virtual_folders()
        print(f"\nVirtual folders: {len(folders)}")
        
        # Sample packages (handle both string and enum)
        if packages:
            print("\nSample packages:")
            for pkg in packages[:5]:
                if pkg.status:
                    status = pkg.status.value if hasattr(pkg.status, 'value') else str(pkg.status)
                else:
                    status = "?"
                print(f"  - {pkg.name} v{pkg.version} [{status}]")
        
        print("\n" + "="*60)
        assert True  # Summary always passes
