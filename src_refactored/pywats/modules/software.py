"""Software Distribution Module for pyWATS

Provides operations for software distribution and versioning.

Public API Endpoints (from Swagger):
- GET /api/Software/Packages - List all packages
- GET /api/Software/Package/{id} - Get package by ID
- GET /api/Software/PackageByName - Get package by name
- GET /api/Software/PackagesByTag - Get packages by tag
- POST /api/Software/Package - Create new draft package
- PUT /api/Software/Package/{id} - Update package
- DELETE /api/Software/Package/{id} - Delete package by ID
- DELETE /api/Software/PackageByName - Delete package by name
- POST /api/Software/PackageStatus/{id} - Update package status
- GET /api/Software/PackageFiles/{id} - Get file list
- POST /api/Software/Package/UploadZip/{id} - Upload zip file
- POST /api/Software/Package/FileAttribute/{id} - Update file attribute
- GET /api/Software/VirtualFolders - Get virtual folders
"""
from typing import List, Optional, Dict, Any

from ..rest_api import SoftwareApi


class SoftwareModule:
    """
    Software distribution module.
    
    Provides operations for:
    - Managing software packages
    - Software versioning
    - Package file management
    - Virtual folder access
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # List all packages
        packages = api.software.get_packages()
        
        # Get package by name
        package = api.software.get_package_by_name("MyPackage", status="Released")
        
        # Create new package
        new_pkg = api.software.create_package({
            "name": "MyPackage",
            "description": "My software package"
        })
    """
    
    def __init__(self, api: SoftwareApi):
        """
        Initialize SoftwareModule with REST API client.
        
        Args:
            api: SoftwareApi instance for making HTTP requests
        """
        self._api = api
    
    # =========================================================================
    # Query Packages
    # =========================================================================
    
    def get_packages(self) -> List[dict]:
        """
        Get all available software packages.
        
        GET /api/Software/Packages
        
        Returns:
            List of software package dictionaries
        """
        response = self._api.get_packages()
        return response.data if response.data else []
    
    def get_package(self, package_id: str) -> Optional[dict]:
        """
        Get a specific software package by ID.
        
        GET /api/Software/Package/{id}
        
        Args:
            package_id: Package UUID
            
        Returns:
            Package data if found, None otherwise
        """
        response = self._api.get_package(package_id)
        return response.data
    
    def get_package_by_name(
        self,
        name: str,
        status: Optional[str] = None,
        version: Optional[int] = None
    ) -> Optional[dict]:
        """
        Get a software package by name.
        
        GET /api/Software/PackageByName
        
        Args:
            name: Package name
            status: Optional status filter (Draft, Pending, Released, Revoked)
            version: Optional specific version number
            
        Returns:
            Package data if found, None otherwise
        """
        response = self._api.get_package_by_name(name, status, version)
        return response.data
    
    def get_packages_by_tag(
        self,
        tag: str,
        value: str,
        status: Optional[str] = None
    ) -> List[dict]:
        """
        Get packages filtered by tag.
        
        GET /api/Software/PackagesByTag
        
        Args:
            tag: Tag name to filter by
            value: Tag value to match
            status: Optional status filter
            
        Returns:
            List of matching packages
        """
        response = self._api.get_packages_by_tag(tag, value, status)
        return response.data if response.data else []
    
    # =========================================================================
    # Create, Update, Delete Packages
    # =========================================================================
    
    def create_package(self, package_data: Dict[str, Any]) -> dict:
        """
        Create a new package in Draft status.
        
        POST /api/Software/Package
        
        If name exists, version will be previous version + 1.
        
        Args:
            package_data: Package metadata dictionary containing:
                - name: Package name (required)
                - description: Package description
                - installOnRoot: Whether to install on root
                - rootDirectory: Root directory path
                - priority: Installation priority
                - tags: List of {key, value} tag objects
            
        Returns:
            Created package data
        """
        response = self._api.create_package(package_data)
        return response.data
    
    def update_package(self, package_id: str, package_data: Dict[str, Any]) -> dict:
        """
        Update a software package.
        
        PUT /api/Software/Package/{id}
        
        Note: This will overwrite existing configuration.
        - Package in Draft: all details can be edited
        - Package in Pending/Released: only Status and Tags can be edited
        - Tags format: <PackageInfo><tagName>TagValue</tagName></PackageInfo>
        
        Args:
            package_id: Package UUID
            package_data: Updated package data
            
        Returns:
            Updated package data
        """
        response = self._api.update_package(package_id, package_data)
        return response.data
    
    def delete_package(self, package_id: str) -> bool:
        """
        Delete a software package by ID.
        
        DELETE /api/Software/Package/{id}
        
        Note: Status must be Draft or Revoked before deletion.
        
        Args:
            package_id: Package UUID to delete
            
        Returns:
            True if deleted successfully
        """
        response = self._api.delete_package(package_id)
        return response.is_success
    
    def delete_package_by_name(
        self,
        name: str,
        version: Optional[int] = None
    ) -> bool:
        """
        Delete a software package by name.
        
        DELETE /api/Software/PackageByName
        
        Note: Status must be Draft or Revoked before deletion.
        
        Args:
            name: Package name
            version: Optional version number
            
        Returns:
            True if deleted successfully
        """
        response = self._api.delete_package_by_name(name, version)
        return response.is_success
    
    # =========================================================================
    # Package Status
    # =========================================================================
    
    def update_status(self, package_id: str, status: str) -> bool:
        """
        Update the status of a software package.
        
        POST /api/Software/PackageStatus/{id}
        
        Status transitions:
        - Draft -> Pending
        - Pending -> Draft OR Released
        - Released -> Revoked
        
        Args:
            package_id: Package UUID
            status: New status (Draft, Pending, Released, Revoked)
            
        Returns:
            True if status updated successfully
        """
        response = self._api.update_package_status(package_id, status)
        return response.is_success
    
    # =========================================================================
    # Package Files
    # =========================================================================
    
    def get_package_files(self, package_id: str) -> List[dict]:
        """
        Get files associated with a package.
        
        GET /api/Software/PackageFiles/{id}
        
        Note: Returns file metadata, not actual file contents.
        
        Args:
            package_id: Package UUID
            
        Returns:
            List of file metadata dictionaries
        """
        response = self._api.get_package_files(package_id)
        return response.data if response.data else []
    
    def upload_zip(
        self,
        package_id: str,
        zip_content: bytes,
        clean_install: bool = False
    ) -> bool:
        """
        Upload a zip file to a software package.
        
        POST /api/Software/Package/UploadZip/{id}
        
        Note:
        - Will merge files by default
        - Use clean_install=True to delete all files before installing
        - Zip cannot contain files on root level
        - All files must be in a folder: zipFile/myFolder/myFile.txt
        
        Args:
            package_id: Package UUID
            zip_content: Zip file content as bytes
            clean_install: If True, delete existing files first
            
        Returns:
            True if upload successful
        """
        response = self._api.upload_package_zip(package_id, zip_content, clean_install)
        return response.is_success
    
    def update_file_attribute(
        self,
        file_id: str,
        attribute_data: Dict[str, Any]
    ) -> bool:
        """
        Update file attributes for a specific file.
        
        POST /api/Software/Package/FileAttribute/{id}
        
        Get file ID by calling get_package_files() first.
        
        Args:
            file_id: The file ID (from get_package_files)
            attribute_data: Attribute data to update
            
        Returns:
            True if update successful
        """
        response = self._api.update_file_attribute(file_id, attribute_data)
        return response.is_success
    
    # =========================================================================
    # Virtual Folders
    # =========================================================================
    
    def get_virtual_folders(self) -> List[dict]:
        """
        Get all virtual folders registered in Production Manager.
        
        GET /api/Software/VirtualFolders
        
        Returns:
            List of virtual folder dictionaries
        """
        response = self._api.get_virtual_folders()
        return response.data if response.data else []
