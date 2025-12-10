"""Software service - business logic layer.

All business operations for software distribution packages.
"""
from typing import Optional, List, Union
from uuid import UUID

from .repository import SoftwareRepository
from .models import Package, PackageFile, PackageTag, VirtualFolder
from .enums import PackageStatus
from ...core import HttpClient


class SoftwareService:
    """
    Software distribution business logic layer.

    Provides high-level operations for managing software packages.
    """

    def __init__(self, repository_or_client: Union[SoftwareRepository, HttpClient]):
        """
        Initialize with SoftwareRepository or HttpClient.

        Args:
            repository_or_client: SoftwareRepository instance or HttpClient (for backward compatibility)
        """
        if isinstance(repository_or_client, SoftwareRepository):
            self._repository = repository_or_client
        else:
            # Backward compatibility: create repository from HttpClient
            self._repository = SoftwareRepository(repository_or_client)

    # =========================================================================
    # Query Packages
    # =========================================================================

    def get_packages(self) -> List[Package]:
        """
        Get all available software packages.

        Returns:
            List of Package objects
        """
        return self._repository.get_packages()

    def get_package(self, package_id: Union[str, UUID]) -> Optional[Package]:
        """
        Get a specific software package by ID.

        Args:
            package_id: Package UUID

        Returns:
            Package object or None if not found
        """
        return self._repository.get_package(package_id)

    def get_package_by_name(
        self,
        name: str,
        status: Optional[PackageStatus] = None,
        version: Optional[int] = None,
    ) -> Optional[Package]:
        """
        Get a software package by name.

        Args:
            name: Package name
            status: Optional status filter
            version: Optional specific version number

        Returns:
            Package object or None if not found
        """
        return self._repository.get_package_by_name(name, status, version)

    def get_released_package(self, name: str) -> Optional[Package]:
        """
        Get the released version of a package.

        Args:
            name: Package name

        Returns:
            Released Package object or None
        """
        return self._repository.get_package_by_name(
            name, status=PackageStatus.RELEASED
        )

    def get_packages_by_tag(
        self,
        tag: str,
        value: str,
        status: Optional[PackageStatus] = None,
    ) -> List[Package]:
        """
        Get packages filtered by tag.

        Args:
            tag: Tag name to filter by
            value: Tag value to match
            status: Optional status filter

        Returns:
            List of matching Package objects
        """
        return self._repository.get_packages_by_tag(tag, value, status)

    # =========================================================================
    # Create, Update, Delete Packages
    # =========================================================================

    def create_package(
        self,
        name: str,
        description: Optional[str] = None,
        install_on_root: bool = False,
        root_directory: Optional[str] = None,
        priority: Optional[int] = None,
        tags: Optional[List[PackageTag]] = None,
    ) -> Optional[Package]:
        """
        Create a new package in Draft status.

        If name exists, version will be previous version + 1.

        Args:
            name: Package name (required)
            description: Package description
            install_on_root: Whether to install on root
            root_directory: Root directory path
            priority: Installation priority
            tags: List of PackageTag objects

        Returns:
            Created Package object or None
        """
        package = Package(
            name=name,
            description=description,
            install_on_root=install_on_root,
            root_directory=root_directory,
            priority=priority,
            tags=tags,
        )
        return self._repository.create_package(package)

    def update_package(self, package: Package) -> Optional[Package]:
        """
        Update a software package.

        Note: This will overwrite existing configuration.
        - Package in Draft: all details can be edited
        - Package in Pending/Released: only Status and Tags can be edited

        Args:
            package: Package object with updated data

        Returns:
            Updated Package object or None
        """
        if not package.package_id:
            return None
        return self._repository.update_package(package.package_id, package)

    def delete_package(self, package_id: Union[str, UUID]) -> bool:
        """
        Delete a software package by ID.

        Note: Status must be Draft or Revoked before deletion.

        Args:
            package_id: Package UUID to delete

        Returns:
            True if deleted successfully
        """
        return self._repository.delete_package(package_id)

    def delete_package_by_name(
        self, name: str, version: Optional[int] = None
    ) -> bool:
        """
        Delete a software package by name.

        Note: Status must be Draft or Revoked before deletion.

        Args:
            name: Package name
            version: Optional version number

        Returns:
            True if deleted successfully
        """
        return self._repository.delete_package_by_name(name, version)

    # =========================================================================
    # Package Status Workflow
    # =========================================================================

    def submit_for_review(self, package_id: Union[str, UUID]) -> bool:
        """
        Submit a draft package for review (Draft -> Pending).

        Args:
            package_id: Package UUID

        Returns:
            True if successful
        """
        return self._repository.update_package_status(
            package_id, PackageStatus.PENDING
        )

    def return_to_draft(self, package_id: Union[str, UUID]) -> bool:
        """
        Return a pending package to draft (Pending -> Draft).

        Args:
            package_id: Package UUID

        Returns:
            True if successful
        """
        return self._repository.update_package_status(
            package_id, PackageStatus.DRAFT
        )

    def release_package(self, package_id: Union[str, UUID]) -> bool:
        """
        Release a pending package (Pending -> Released).

        Args:
            package_id: Package UUID

        Returns:
            True if successful
        """
        return self._repository.update_package_status(
            package_id, PackageStatus.RELEASED
        )

    def revoke_package(self, package_id: Union[str, UUID]) -> bool:
        """
        Revoke a released package (Released -> Revoked).

        Args:
            package_id: Package UUID

        Returns:
            True if successful
        """
        return self._repository.update_package_status(
            package_id, PackageStatus.REVOKED
        )

    # =========================================================================
    # Package Files
    # =========================================================================

    def get_package_files(
        self, package_id: Union[str, UUID]
    ) -> List[PackageFile]:
        """
        Get files associated with a package.

        Args:
            package_id: Package UUID

        Returns:
            List of PackageFile objects
        """
        return self._repository.get_package_files(package_id)

    def upload_zip(
        self,
        package_id: Union[str, UUID],
        zip_content: bytes,
        clean_install: bool = False,
    ) -> bool:
        """
        Upload a zip file to a software package.

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
        return self._repository.upload_package_zip(
            package_id, zip_content, clean_install
        )

    def update_file_attribute(
        self, file_id: Union[str, UUID], attributes: str
    ) -> bool:
        """
        Update file attributes for a specific file.

        Get file ID by calling get_package_files() first.

        Args:
            file_id: The file ID (from get_package_files)
            attributes: Attribute data to update

        Returns:
            True if update successful
        """
        return self._repository.update_file_attribute(file_id, attributes)

    # =========================================================================
    # Virtual Folders
    # =========================================================================

    def get_virtual_folders(self) -> List[VirtualFolder]:
        """
        Get all virtual folders registered in Production Manager.

        Returns:
            List of VirtualFolder objects
        """
        return self._repository.get_virtual_folders()
