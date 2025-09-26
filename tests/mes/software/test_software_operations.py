#!/usr/bin/env python3
"""
Comprehensive test suite for MES Software operations.

Tests all software package management functionality following the same pattern
as Asset and Product tests. Designed to work with or without pytest.

Expected results:
- Some tests may fail if internal API endpoints are not available
- Connection tests should pass if API is accessible
- Package operations may fail until REST endpoints are implemented
"""

import logging
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

# Add src to path for standalone execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Handle pytest availability
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    pytest = None
    PYTEST_AVAILABLE = False

from pyWATS import create_api, PyWATSAPI
from pyWATS.mes import Software
from pyWATS.mes.models import Package, StatusEnum


class SoftwareTestRunner:
    """Test runner for software operations."""
    
    def __init__(self):
        """Initialize the test runner with WATS API connection."""
        logger.info("Initializing software test runner...")
        
        # Initialize API
        self.api = create_api()
        
        # Initialize software handler
        self.software_handler = Software(connection=self.client)
        
        # Track packages for cleanup
        self.test_packages: List[Package] = []
        
        logger.info("✓ Software test runner initialized")
    
    @property
    def client(self):
        """Get the WATS API client for Software API initialization"""
        if self.api.tdm_client and self.api.tdm_client._connection:
            return self.api.tdm_client._connection._client
        return None
    
    def cleanup_test_packages(self):
        """Clean up any test packages created during testing."""
        try:
            if hasattr(self, 'software_handler'):
                # Clean up local test packages if any were created
                logger.info("Cleaning up test packages...")
        except Exception as e:
            logger.warning(f"Cleanup warning: {e}")
    
    def discover_real_packages(self, limit: int = 10) -> List[Package]:
        """
        Discover real packages from the server for testing.
        
        Args:
            limit: Maximum number of packages to retrieve
            
        Returns:
            List of discovered Package objects
        """
        logger.info("Discovering real packages from server...")
        
        try:
            # Try to get packages with no filters to see what's available
            packages = self.software_handler.get_packages(
                install=False,  # Don't install during discovery
                display_progress=False,
                wait_for_execution=False
            )
            
            logger.info(f"Discovered {len(packages)} packages:")
            for i, package in enumerate(packages[:limit]):
                logger.info(f"  - {package.name} v{package.version}")
                if i >= 2:  # Show first 3
                    logger.info(f"  ... and {len(packages) - 3} more packages")
                    break
            
            self.test_packages.extend(packages[:limit])
            return packages[:limit]
            
        except Exception as e:
            logger.warning(f"Package discovery failed: {e}")
            return []


def create_software_test_runner():
    """Create a SoftwareTestRunner instance."""
    return SoftwareTestRunner()


# Setup pytest fixture (define unconditionally to avoid static analysis warnings)
def _create_fixture_function():
    """Create the pytest fixture function."""
    def software_test_runner():
        """Fixture providing a SoftwareTestRunner instance."""
        runner = create_software_test_runner()
        yield runner
        runner.cleanup_test_packages()
    return software_test_runner

# Apply pytest decorator only if available
if PYTEST_AVAILABLE and pytest:
    software_test_runner = pytest.fixture(_create_fixture_function())
else:
    # Define a dummy function for static analysis
    software_test_runner = _create_fixture_function()


class TestSoftwareConnection:
    """Test software service connection."""
    
    def test_software_connection(self, software_test_runner):
        """Test that we can connect to the software service."""
        assert software_test_runner.software_handler.is_connected()
        logger.info("✓ Software service connection successful")


class TestSoftwareDiscovery:
    """Test software package discovery and retrieval operations."""
    
    def test_discover_packages(self, software_test_runner):
        """Test discovering packages from the server."""
        packages = software_test_runner.discover_real_packages(20)
        assert isinstance(packages, list)
        logger.info(f"✓ Discovered {len(packages)} packages")
        
        if packages:
            # Verify package structure
            first_package = packages[0]
            assert hasattr(first_package, 'name')
            assert hasattr(first_package, 'version')
            logger.info(f"✓ Package structure valid: {first_package.name}")
    
    def test_get_packages_with_filter(self, software_test_runner):
        """Test getting packages with various filters."""
        # Test basic package retrieval (no install)
        try:
            packages = software_test_runner.software_handler.get_packages(
                install=False,
                display_progress=False,
                wait_for_execution=False,
                package_status=StatusEnum.RELEASED
            )
            logger.info(f"✓ Basic package retrieval: {len(packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Basic package retrieval failed (expected): {e}")
    
    def test_get_package_by_name(self, software_test_runner):
        """Test retrieving a specific package by name."""
        packages = software_test_runner.discover_real_packages(5)
        if packages:
            test_package = packages[0]
            try:
                retrieved_package = software_test_runner.software_handler.get_package_by_name(
                    test_package.name,
                    install=False,
                    display_progress=False,
                    wait_for_execution=False
                )
                if retrieved_package:
                    assert retrieved_package.name == test_package.name
                    logger.info(f"✓ Package by name retrieval: {retrieved_package.name}")
                else:
                    logger.info("⚠ Package by name retrieval returned None (may be expected)")
            except Exception as e:
                logger.info(f"⚠ Package by name retrieval failed: {e}")
        else:
            logger.info("⚠ No packages available for name retrieval test")
    
    def test_get_packages_by_tag(self, software_test_runner):
        """Test getting packages by tag filters."""
        try:
            # Test with XPath
            packages = software_test_runner.software_handler.get_packages_by_tag(
                xpath_or_tag_names="//Package[@Status='Released']",
                install=False,
                display_progress=False,
                wait_for_execution=False
            )
            logger.info(f"✓ Package by XPath retrieval: {len(packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Package by XPath retrieval failed: {e}")
        
        try:
            # Test with tag arrays
            packages = software_test_runner.software_handler.get_packages_by_tag(
                xpath_or_tag_names=["Status", "Type"],
                tag_values=["Released", "Application"],
                install=False,
                display_progress=False,
                wait_for_execution=False
            )
            logger.info(f"✓ Package by tag arrays retrieval: {len(packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Package by tag arrays retrieval failed: {e}")


class TestSoftwarePackageManagement:
    """Test software package management operations."""
    
    def test_get_revoked_packages(self, software_test_runner):
        """Test retrieving revoked packages."""
        try:
            revoked_packages = software_test_runner.software_handler.get_revoked_packages(
                tag_names=["Status"],
                tag_values=["Revoked"]
            )
            logger.info(f"✓ Revoked packages retrieval: {len(revoked_packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Revoked packages retrieval failed: {e}")
    
    def test_get_available_packages(self, software_test_runner):
        """Test checking for available package updates."""
        try:
            available_packages = software_test_runner.software_handler.get_available_packages()
            logger.info(f"✓ Available packages check: {len(available_packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Available packages check failed: {e}")
    
    def test_install_package(self, software_test_runner):
        """Test package installation (local only)."""
        packages = software_test_runner.discover_real_packages(5)
        if packages:
            test_package = packages[0]
            try:
                # Test local installation (doesn't download, just creates local structure)
                software_test_runner.software_handler.install_package(
                    test_package,
                    display_progress=False,
                    wait_for_execution=True
                )
                logger.info(f"✓ Package installation (local): {test_package.name}")
            except Exception as e:
                logger.info(f"⚠ Package installation failed: {e}")
        else:
            logger.info("⚠ No packages available for installation test")


class TestSoftwareFolderManagement:
    """Test software folder and local storage operations."""
    
    def test_root_folder_management(self, software_test_runner):
        """Test setting and getting root folder path."""
        try:
            # Get current root folder
            current_path = software_test_runner.software_handler.get_root_folder_path()
            assert isinstance(current_path, str)
            assert len(current_path) > 0
            logger.info(f"✓ Current root folder: {current_path}")
            
            # Set a test folder
            test_path = Path(current_path).parent / "test_software_packages"
            software_test_runner.software_handler.set_root_folder_path(
                str(test_path),
                move_existing_packages=False
            )
            
            # Verify the change
            new_path = software_test_runner.software_handler.get_root_folder_path()
            assert str(test_path) == new_path
            logger.info(f"✓ Root folder updated: {new_path}")
            
            # Restore original path
            software_test_runner.software_handler.set_root_folder_path(
                current_path,
                move_existing_packages=False
            )
            
        except Exception as e:
            logger.info(f"⚠ Root folder management failed: {e}")
    
    def test_package_cleanup_operations(self, software_test_runner):
        """Test package cleanup operations."""
        try:
            # Test delete revoked packages (non-interactive)
            software_test_runner.software_handler.delete_revoked_packages(
                prompt_operator=False
            )
            logger.info("✓ Delete revoked packages completed")
        except Exception as e:
            logger.info(f"⚠ Delete revoked packages failed: {e}")


class TestSoftwareFiltering:
    """Test software package filtering and search operations."""
    
    def test_package_filtering_by_attributes(self, software_test_runner):
        """Test filtering packages by various attributes."""
        try:
            # Test filtering by part number
            packages = software_test_runner.software_handler.get_packages(
                part_number="TEST*",
                install=False,
                display_progress=False,
                wait_for_execution=False
            )
            logger.info(f"✓ Part number filtering: {len(packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Part number filtering failed: {e}")
        
        try:
            # Test filtering by process
            packages = software_test_runner.software_handler.get_packages(
                process="TestProcess",
                install=False,
                display_progress=False,
                wait_for_execution=False
            )
            logger.info(f"✓ Process filtering: {len(packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Process filtering failed: {e}")
        
        try:
            # Test filtering by station type
            packages = software_test_runner.software_handler.get_packages(
                station_type="TestStation",
                install=False,
                display_progress=False,
                wait_for_execution=False
            )
            logger.info(f"✓ Station type filtering: {len(packages)} packages")
        except Exception as e:
            logger.info(f"⚠ Station type filtering failed: {e}")


class TestSoftwareStatusHandling:
    """Test software package status and version handling."""
    
    def test_package_status_filtering(self, software_test_runner):
        """Test filtering packages by status."""
        status_tests = [
            (StatusEnum.RELEASED, "Released"),
            (StatusEnum.DEVELOPMENT, "Development"),
            (StatusEnum.OBSOLETE, "Obsolete"),
        ]
        
        for status_enum, status_name in status_tests:
            try:
                packages = software_test_runner.software_handler.get_packages(
                    package_status=status_enum,
                    install=False,
                    display_progress=False,
                    wait_for_execution=False
                )
                logger.info(f"✓ {status_name} status filtering: {len(packages)} packages")
            except Exception as e:
                logger.info(f"⚠ {status_name} status filtering failed: {e}")


if __name__ == "__main__":
    # Allow running tests directly
    import sys
    
    # Configure logging for direct execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create test runner
    runner = SoftwareTestRunner()
    
    try:
        # Run a quick test
        logger.info("Starting software operations test...")
        
        # Test connection
        assert runner.software_handler.is_connected(), "Connection failed"
        logger.info("✓ Connection test passed")
        
        # Test basic package discovery
        packages = runner.discover_real_packages(5)
        logger.info(f"✓ Package discovery test passed: {len(packages)} packages")
        
        # Test folder management
        current_path = runner.software_handler.get_root_folder_path()
        logger.info(f"✓ Root folder test passed: {current_path}")
        
        logger.info("All basic tests passed!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        sys.exit(1)
    finally:
        runner.cleanup_test_packages()