"""
Software module for WATS API.

This module provides functionality for managing software packages,
deployments, and software-related operations in the WATS system.
"""

from typing import List, Optional, Dict, Any, Tuple
import io
from .base import BaseModule
from ..exceptions import WATSException, WATSNotFoundError


class StatusEnum:
    """Status enumeration for packages."""
    RELEASED = "Released"
    DRAFT = "Draft"
    OBSOLETE = "Obsolete"


class Package:
    """Software package information."""
    
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.version = kwargs.get('version', '1.0')
        self.status = kwargs.get('status', StatusEnum.RELEASED)
        self.part_number = kwargs.get('part_number')
        self.process = kwargs.get('process')
        self.station_type = kwargs.get('station_type')
        self.revision = kwargs.get('revision')
        self.station_name = kwargs.get('station_name')
        self.misc = kwargs.get('misc')


class SoftwareModule(BaseModule):
    """
    Software management module.
    
    Provides methods for:
    - Package management and deployment
    - Software installation and configuration
    - Package selection and identification
    - Software lifecycle management
    """

    def is_connected(self) -> bool:
        """Check if software module is connected."""
        raise NotImplementedError("Software.is_connected not implemented")

    def get_revoked_packages(self, tag_names: List[str], tag_values: List[str]) -> Tuple[List[Package], Package, bool, List[io.FileIO], List[io.FileIO]]:
        """
        Get revoked packages with file information.
        
        Args:
            tag_names: List of tag names
            tag_values: List of tag values
            
        Returns:
            Tuple of (packages, selected_package, continue_flag, execute_files, top_level_sequences)
        """
        raise NotImplementedError("Software.get_revoked_packages not implemented")

    def get_packages(self, part_number: Optional[str] = None, process: Optional[str] = None,
                    station_type: Optional[str] = None, revision: Optional[str] = None,
                    station_name: Optional[str] = None, misc: Optional[str] = None,
                    install: bool = True, display_progress: bool = True,
                    wait_for_execution: bool = True, package_status: str = StatusEnum.RELEASED) -> List[Package]:
        """
        Get packages with filtering options.
        
        Args:
            part_number: Part number filter
            process: Process filter
            station_type: Station type filter
            revision: Revision filter
            station_name: Station name filter
            misc: Miscellaneous filter
            install: Install packages flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            List of Package objects
        """
        raise NotImplementedError("Software.get_packages not implemented")

    def get_packages_by_tag_xpath(self, xpath: str, install: bool = True, display_progress: bool = True,
                                 wait_for_execution: bool = True, package_status: str = StatusEnum.RELEASED) -> Tuple[List[Package], List[io.FileIO], List[io.FileIO]]:
        """
        Get packages by XPath tag with file information.
        
        Args:
            xpath: XPath expression
            install: Install packages flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            Tuple of (packages, execute_files, top_level_sequences)
        """
        raise NotImplementedError("Software.get_packages_by_tag (xpath with files) not implemented")

    def get_packages_by_tag_xpath_simple(self, xpath: str, install: bool = True, display_progress: bool = True,
                                        wait_for_execution: bool = True, package_status: str = StatusEnum.RELEASED) -> List[Package]:
        """
        Get packages by XPath tag (simple version).
        
        Args:
            xpath: XPath expression
            install: Install packages flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            List of Package objects
        """
        raise NotImplementedError("Software.get_packages_by_tag (xpath simple) not implemented")

    def get_packages_by_tag_dict_simple(self, tag_value: Dict[str, str], install: bool, display_progress: bool,
                                       wait_for_execution: bool, package_status: str = StatusEnum.RELEASED) -> List[Package]:
        """
        Get packages by tag dictionary (simple version).
        
        Args:
            tag_value: Dictionary of tag names and values
            install: Install packages flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            List of Package objects
        """
        raise NotImplementedError("Software.get_packages_by_tag (dict simple) not implemented")

    def get_packages_by_tag_arrays(self, tag_names: List[str], tag_values: List[str],
                                  install: bool, display_progress: bool, wait_for_execution: bool,
                                  package_status: str = StatusEnum.RELEASED) -> Tuple[List[Package], List[io.FileIO], List[io.FileIO]]:
        """
        Get packages by tag arrays with file information.
        
        Args:
            tag_names: List of tag names
            tag_values: List of tag values
            install: Install packages flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            Tuple of (packages, execute_files, top_level_sequences)
        """
        raise NotImplementedError("Software.get_packages_by_tag (arrays with files) not implemented")

    def get_packages_by_tag_dict(self, tag_value: Dict[str, str], install: bool, display_progress: bool,
                                wait_for_execution: bool, package_status: str = StatusEnum.RELEASED) -> Tuple[List[Package], List[io.FileIO], List[io.FileIO]]:
        """
        Get packages by tag dictionary with file information.
        
        Args:
            tag_value: Dictionary of tag names and values
            install: Install packages flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            Tuple of (packages, execute_files, top_level_sequences)
        """
        raise NotImplementedError("Software.get_packages_by_tag (dict with files) not implemented")

    def get_package_by_name(self, package_name: str, install: bool = True, display_progress: bool = True,
                           wait_for_execution: bool = True, package_status: str = StatusEnum.RELEASED) -> Package:
        """
        Get package by name (simple version).
        
        Args:
            package_name: Package name
            install: Install package flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            Package object
        """
        raise NotImplementedError("Software.get_package_by_name (simple) not implemented")

    def get_package_by_name_with_files(self, package_name: str, install: bool, display_progress: bool,
                                      wait_for_execution: bool, package_status: str = StatusEnum.RELEASED) -> Tuple[Package, List[io.FileIO], List[io.FileIO]]:
        """
        Get package by name with file information.
        
        Args:
            package_name: Package name
            install: Install package flag
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            package_status: Package status filter
            
        Returns:
            Tuple of (package, execute_files, top_level_sequences)
        """
        raise NotImplementedError("Software.get_package_by_name (with files) not implemented")

    def install_package_array(self, packages: List[Package], display_progress: bool, wait_for_execution: bool):
        """
        Install multiple packages (simple version).
        
        Args:
            packages: List of packages to install
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
        """
        raise NotImplementedError("Software.install_package (array simple) not implemented")

    def install_package_array_with_files(self, packages: List[Package], display_progress: bool,
                                        wait_for_execution: bool) -> Tuple[List[io.FileIO], List[io.FileIO]]:
        """
        Install multiple packages with file information.
        
        Args:
            packages: List of packages to install
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            
        Returns:
            Tuple of (execute_files, top_level_sequences)
        """
        raise NotImplementedError("Software.install_package (array with files) not implemented")

    def install_package_single(self, package: Package, display_progress: bool, wait_for_execution: bool):
        """
        Install single package (simple version).
        
        Args:
            package: Package to install
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
        """
        raise NotImplementedError("Software.install_package (single simple) not implemented")

    def install_package_single_with_files(self, package: Package, display_progress: bool,
                                         wait_for_execution: bool) -> Tuple[List[io.FileIO], List[io.FileIO]]:
        """
        Install single package with file information.
        
        Args:
            package: Package to install
            display_progress: Display progress flag
            wait_for_execution: Wait for execution flag
            
        Returns:
            Tuple of (execute_files, top_level_sequences)
        """
        raise NotImplementedError("Software.install_package (single with files) not implemented")

    @staticmethod
    def set_root_folder_path(root_folder_path: str, move_existing_packages: bool = True):
        """
        Set root folder path for packages.
        
        Args:
            root_folder_path: Root folder path
            move_existing_packages: Move existing packages flag
        """
        raise NotImplementedError("Software.set_root_folder_path not implemented")

    @staticmethod
    def get_root_folder_path() -> str:
        """
        Get root folder path for packages.
        
        Returns:
            Root folder path
        """
        raise NotImplementedError("Software.get_root_folder_path not implemented")

    def delete_all_packages(self, prompt_operator: bool = True):
        """
        Delete all packages.
        
        Args:
            prompt_operator: Prompt operator flag
        """
        raise NotImplementedError("Software.delete_all_packages not implemented")

    def delete_revoked_packages(self, prompt_operator: bool = True):
        """
        Delete revoked packages.
        
        Args:
            prompt_operator: Prompt operator flag
        """
        raise NotImplementedError("Software.delete_revoked_packages not implemented")

    def get_available_packages(self) -> Tuple[List[Package], bool]:
        """
        Get available packages.
        
        Returns:
            Tuple of (packages, packages_available_flag)
        """
        raise NotImplementedError("Software.get_available_packages not implemented")