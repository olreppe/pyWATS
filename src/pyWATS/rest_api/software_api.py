"""
Software Distribution API Endpoints

Provides all REST API calls for software package management.
All methods return typed responses instead of raw Response objects.
Based on the public endpoints at /api/Software/...
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient


class SoftwareApi:
    """
    Software Distribution API endpoints.
    
    Endpoints for creating, uploading, and managing software packages.
    All methods return typed responses.
    
    Public endpoints available:
    - GET/POST /api/Software/Package
    - GET/PUT/DELETE /api/Software/Package/{id}
    - GET /api/Software/Packages
    - GET/DELETE /api/Software/PackageByName
    - GET /api/Software/PackagesByTag
    - GET /api/Software/PackageFiles/{id}
    - POST /api/Software/Package/FileAttribute/{id}
    - POST /api/Software/Package/UploadZip/{id}
    - POST /api/Software/PackageStatus/{id}
    - GET /api/Software/VirtualFolders
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Software Packages - List and Query
    # =========================================================================
    
    def get_packages(self) -> List[Dict[str, Any]]:
        """
        Get all software packages.
        
        GET /api/Software/Packages
        
        Returns:
            List of package dictionaries
        """
        response = self._http.get("/api/Software/Packages")
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else []
        return []
    
    def get_package(self, package_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific software package by ID.
        
        GET /api/Software/Package/{id}
        
        Args:
            package_id: The package UUID
            
        Returns:
            Package data dictionary or None if not found
        """
        response = self._http.get(f"/api/Software/Package/{package_id}")
        if response.is_success and response.data:
            return response.data
        return None
    
    def get_package_by_name(
        self,
        name: str,
        status: Optional[str] = None,
        version: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get a software package by name.
        
        GET /api/Software/PackageByName
        
        Args:
            name: Package name
            status: Optional status filter (Draft, Pending, Released, Revoked)
            version: Optional specific version number
            
        Returns:
            Package data dictionary or None if not found
        """
        params: Dict[str, Any] = {"name": name}
        if status:
            params["status"] = status
        if version is not None:
            params["version"] = version
        response = self._http.get("/api/Software/PackageByName", params=params)
        if response.is_success and response.data:
            return response.data
        return None
    
    def get_packages_by_tag(
        self,
        tag: str,
        value: str,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get packages filtered by tag.
        
        GET /api/Software/PackagesByTag
        
        Args:
            tag: Tag name to filter by
            value: Tag value to match
            status: Optional status filter
            
        Returns:
            List of matching package dictionaries
        """
        params: Dict[str, Any] = {"tag": tag, "value": value}
        if status:
            params["status"] = status
        response = self._http.get("/api/Software/PackagesByTag", params=params)
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else []
        return []
    
    # =========================================================================
    # Software Packages - Create, Update, Delete
    # =========================================================================
    
    def create_package(self, package_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new package in Draft status.
        
        POST /api/Software/Package
        
        If name exists, version will be previous version + 1.
        
        Args:
            package_data: Package metadata dictionary
            
        Returns:
            Created package dictionary or None if failed
        """
        response = self._http.post("/api/Software/Package", data=package_data)
        if response.is_success and response.data:
            return response.data
        return None
    
    def update_package(self, package_id: str, package_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a software package.
        
        PUT /api/Software/Package/{id}
        
        Note: This will overwrite existing configuration.
        - Package in Draft: all details can be edited
        - Package in Pending/Released: only Status and Tags can be edited
        - Tags format: <PackageInfo><tagName>TagValue</tagName></PackageInfo>
        
        Args:
            package_id: The package UUID
            package_data: Updated package data
            
        Returns:
            Updated package dictionary or None if failed
        """
        response = self._http.put(f"/api/Software/Package/{package_id}", data=package_data)
        if response.is_success and response.data:
            return response.data
        return None
    
    def delete_package(self, package_id: str) -> bool:
        """
        Delete a software package by ID.
        
        DELETE /api/Software/Package/{id}
        
        Note: Status must be Draft or Revoked before deletion.
        
        Args:
            package_id: The package UUID to delete
            
        Returns:
            True if successful
        """
        response = self._http.delete(f"/api/Software/Package/{package_id}")
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
            True if successful
        """
        params: Dict[str, Any] = {"name": name}
        if version is not None:
            params["version"] = version
        response = self._http.delete("/api/Software/PackageByName", params=params)
        return response.is_success
    
    # =========================================================================
    # Package Status
    # =========================================================================
    
    def update_package_status(self, package_id: str, status: str) -> bool:
        """
        Update the status of a software package.
        
        POST /api/Software/PackageStatus/{id}
        
        Status transitions:
        - Draft -> Pending
        - Pending -> Draft OR Released
        - Released -> Revoked
        
        Args:
            package_id: The package UUID
            status: New status (Draft, Pending, Released, Revoked)
            
        Returns:
            True if successful
        """
        response = self._http.post(
            f"/api/Software/PackageStatus/{package_id}",
            params={"status": status}
        )
        return response.is_success
    
    # =========================================================================
    # Package Files
    # =========================================================================
    
    def get_package_files(self, package_id: str) -> List[Dict[str, Any]]:
        """
        Get files associated with a package.
        
        GET /api/Software/PackageFiles/{id}
        
        Note: Returns file metadata, not actual file contents.
        
        Args:
            package_id: The package UUID
            
        Returns:
            List of file metadata dictionaries
        """
        response = self._http.get(f"/api/Software/PackageFiles/{package_id}")
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else []
        return []
    
    def upload_package_zip(
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
            package_id: The package UUID
            zip_content: Zip file content as bytes
            clean_install: If True, delete existing files first
            
        Returns:
            True if successful
        """
        params = {"cleanInstall": "true"} if clean_install else {}
        headers = {"Content-Type": "application/zip"}
        response = self._http.post(
            f"/api/Software/Package/UploadZip/{package_id}",
            data=zip_content,
            params=params,
            headers=headers
        )
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
            file_id: The file ID
            attribute_data: Attribute data to update
            
        Returns:
            True if successful
        """
        response = self._http.post(
            f"/api/Software/Package/FileAttribute/{file_id}",
            data=attribute_data
        )
        return response.is_success
    
    # =========================================================================
    # Virtual Folders
    # =========================================================================
    
    def get_virtual_folders(self) -> List[Dict[str, Any]]:
        """
        Get all virtual folders registered in Production Manager.
        
        GET /api/Software/VirtualFolders
        
        Returns:
            List of virtual folder dictionaries
        """
        response = self._http.get("/api/Software/VirtualFolders")
        if response.is_success and response.data:
            return response.data if isinstance(response.data, list) else []
        return []
