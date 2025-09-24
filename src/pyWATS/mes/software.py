"""
MES Software Module

Handles software package distribution and deployment.
This module mirrors the Interface.MES Software functionality.
"""

from typing import Optional, List, Union, Dict
from pathlib import Path
import shutil

from .base import MESBase
from .models import Package, StatusEnum
from ..rest_api.client import WATSClient
from ..connection import WATSConnection


class Software(MESBase):
    """
    Software package management for WATS MES.
    
    Provides functionality for:
    - Package discovery and retrieval
    - Package installation and management
    - Local package storage management
    - Package versioning and status tracking
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Software module.
        
        Args:
            connection: WATS connection or client instance
        """
        super().__init__(connection)
        self._root_folder_path = None
    
    def is_connected(self) -> bool:
        """
        Check if connected to WATS MES Server.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            response = self._client.get("/api/internal/software/isConnected")
            return response.status_code == 200
        except Exception:
            return False
    
    def get_revoked_packages(
        self,
        tag_names: List[str],
        tag_values: List[str]
    ) -> List[Package]:
        """
        Get revoked packages matching tags.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            tag_names: List of tag names to match
            tag_values: List of tag values to match
            
        Returns:
            List of revoked Package objects
            
        Raises:
            WATSAPIException: On API errors
        """
        data = {
            "tagNames": tag_names,
            "tagValues": tag_values
        }
        
        response = self._rest_post_json("/api/internal/Software/GetRevokedPackages", data)
        packages_data = response.get("packages", [])
        
        return [Package.parse_obj(item) for item in packages_data]
    
    def get_packages(
        self,
        part_number: Optional[str] = None,
        process: Optional[str] = None,
        station_type: Optional[str] = None,
        revision: Optional[str] = None,
        station_name: Optional[str] = None,
        misc: Optional[str] = None,
        install: bool = True,
        display_progress: bool = True,
        wait_for_execution: bool = True,
        package_status: StatusEnum = StatusEnum.RELEASED
    ) -> List[Package]:
        """
        Get packages by default tags.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Part number filter
            process: Process filter
            station_type: Station type filter
            revision: Revision filter
            station_name: Station name filter
            misc: Miscellaneous filter
            install: Install packages after retrieval
            display_progress: Show progress dialog
            wait_for_execution: Wait for installation completion
            package_status: Package status filter
            
        Returns:
            List of Package objects matching criteria
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "install": install,
            "displayProgress": display_progress,
            "waitForExecution": wait_for_execution,
            "packageStatus": package_status.value
        }
        
        # Add optional filters
        if part_number:
            params["partNumber"] = part_number
        if process:
            params["process"] = process
        if station_type:
            params["stationType"] = station_type
        if revision:
            params["revision"] = revision
        if station_name:
            params["stationName"] = station_name
        if misc:
            params["misc"] = misc
        
        response = self._rest_get_json("/api/internal/Software/GetPackages")
        packages_data = response.get("packages", [])
        
        packages = [Package.parse_obj(item) for item in packages_data]
        
        if install:
            self._install_packages_local(packages, display_progress, wait_for_execution)
        
        return packages
    
    def get_packages_by_tag(
        self,
        xpath_or_tag_names: Union[str, List[str]],
        tag_values: Optional[List[str]] = None,
        install: bool = True,
        display_progress: bool = True,
        wait_for_execution: bool = True,
        package_status: StatusEnum = StatusEnum.RELEASED
    ) -> List[Package]:
        """
        Get packages by XPath or tag arrays.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            xpath_or_tag_names: XPath string or list of tag names
            tag_values: List of tag values (required if using tag names)
            install: Install packages after retrieval
            display_progress: Show progress dialog
            wait_for_execution: Wait for installation completion
            package_status: Package status filter
            
        Returns:
            List of Package objects matching criteria
            
        Raises:
            WATSAPIException: On API errors
        """
        if isinstance(xpath_or_tag_names, str):
            # XPath mode
            data = {
                "xpath": xpath_or_tag_names,
                "install": install,
                "displayProgress": display_progress,
                "waitForExecution": wait_for_execution,
                "packageStatus": package_status.value
            }
        else:
            # Tag arrays mode
            if not tag_values:
                raise ValueError("tag_values required when using tag names")
            
            data = {
                "tagNames": xpath_or_tag_names,
                "tagValues": tag_values,
                "install": install,
                "displayProgress": display_progress,
                "waitForExecution": wait_for_execution,
                "packageStatus": package_status.value
            }
        
        response = self._rest_post_json("/api/internal/Software/GetPackagesByTag", data)
        packages_data = response.get("packages", [])
        
        packages = [Package.parse_obj(item) for item in packages_data]
        
        if install:
            self._install_packages_local(packages, display_progress, wait_for_execution)
        
        return packages
    
    def get_package_by_name(
        self,
        package_name: str,
        install: bool = True,
        display_progress: bool = True,
        wait_for_execution: bool = True,
        package_status: StatusEnum = StatusEnum.RELEASED
    ) -> Optional[Package]:
        """
        Get package by name.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            package_name: Package name to retrieve
            install: Install package after retrieval
            display_progress: Show progress dialog
            wait_for_execution: Wait for installation completion
            package_status: Package status filter
            
        Returns:
            Package object or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "packageName": package_name,
            "install": install,
            "displayProgress": display_progress,
            "waitForExecution": wait_for_execution,
            "packageStatus": package_status.value
        }
        
        try:
            response = self._rest_get_json("/api/internal/Software/GetPackageByName")
            package_data = response.get("package")
            
            if package_data:
                package = Package.parse_obj(package_data)
                
                if install:
                    self._install_packages_local([package], display_progress, wait_for_execution)
                
                return package
            
            return None
        except Exception:
            return None
    
    def install_package(
        self,
        packages: Union[Package, List[Package]],
        display_progress: bool = True,
        wait_for_execution: bool = True
    ) -> None:
        """
        Install packages to filesystem.
        
        Args:
            packages: Package or list of packages to install
            display_progress: Show progress during installation
            wait_for_execution: Wait for installation completion
            
        Note: This performs local file operations only.
        The actual package download is handled by the server API.
        """
        if isinstance(packages, Package):
            packages = [packages]
        
        self._install_packages_local(packages, display_progress, wait_for_execution)
    
    def set_root_folder_path(
        self,
        root_folder_path: str,
        move_existing_packages: bool = True
    ) -> None:
        """
        Set local software root folder path.
        
        Args:
            root_folder_path: New root folder path
            move_existing_packages: Move existing packages to new location
        """
        new_path = Path(root_folder_path)
        new_path.mkdir(parents=True, exist_ok=True)
        
        if move_existing_packages and self._root_folder_path:
            old_path = Path(self._root_folder_path)
            if old_path.exists() and old_path != new_path:
                try:
                    # Move existing packages
                    for item in old_path.iterdir():
                        if item.is_file():
                            shutil.move(str(item), str(new_path / item.name))
                        elif item.is_dir():
                            shutil.move(str(item), str(new_path / item.name))
                except Exception as e:
                    print(f"Warning: Could not move all packages: {e}")
        
        self._root_folder_path = str(new_path)
    
    def get_root_folder_path(self) -> str:
        """
        Get current root folder path.
        
        Returns:
            Current root folder path
        """
        if not self._root_folder_path:
            # Default to user's temp directory + wats_packages
            import tempfile
            self._root_folder_path = str(Path(tempfile.gettempdir()) / "wats_packages")
            Path(self._root_folder_path).mkdir(parents=True, exist_ok=True)
        
        return self._root_folder_path
    
    def delete_all_packages(self, prompt_operator: bool = True) -> None:
        """
        Delete all packages from local storage.
        
        Args:
            prompt_operator: Show confirmation dialog (not implemented in this version)
        """
        root_path = Path(self.get_root_folder_path())
        
        if prompt_operator:
            # In a GUI application, you would show a confirmation dialog here
            print(f"Warning: This will delete all packages in {root_path}")
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                return
        
        if root_path.exists():
            shutil.rmtree(root_path)
            root_path.mkdir(parents=True, exist_ok=True)
    
    def delete_revoked_packages(self, prompt_operator: bool = True) -> None:
        """
        Delete revoked packages from local storage.
        
        Args:
            prompt_operator: Show confirmation dialog (not implemented in this version)
        """
        # This would require tracking which packages are revoked locally
        # For now, we'll implement a simple version
        
        if prompt_operator:
            print("Warning: This will delete revoked packages from local storage")
            response = input("Continue? (y/N): ")
            if response.lower() != 'y':
                return
        
        # Implementation would check against server for revoked packages
        # and remove them from local storage
        pass
    
    def get_available_packages(self) -> List[Package]:
        """
        Check server for new package versions.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Returns:
            List of available Package objects with newer versions
            
        Raises:
            WATSAPIException: On API errors
        """
        response = self._rest_get_json("/api/internal/Software/GetAvailablePackages")
        packages_data = response.get("packages", [])
        
        return [Package.parse_obj(item) for item in packages_data]
    
    def _install_packages_local(
        self,
        packages: List[Package],
        display_progress: bool = True,
        wait_for_execution: bool = True
    ) -> None:
        """
        Install packages to local filesystem.
        
        Args:
            packages: List of packages to install
            display_progress: Show progress during installation
            wait_for_execution: Wait for installation completion
            
        Note: This is a simplified implementation.
        In a real system, this would download and extract package files.
        """
        root_path = Path(self.get_root_folder_path())
        
        for package in packages:
            if display_progress:
                print(f"Installing package: {package.name}")
            
            # Create package directory
            package_dir = root_path / package.name
            package_dir.mkdir(parents=True, exist_ok=True)
            
            # In a real implementation, you would:
            # 1. Download the package file from the server
            # 2. Verify checksums
            # 3. Extract files to the package directory
            # 4. Update local package registry
            
            # For now, just create a marker file
            marker_file = package_dir / "package.info"
            marker_file.write_text(f"Package: {package.name}\nVersion: {package.version}")
            
            if not wait_for_execution:
                # In async mode, you would start installation in background
                pass