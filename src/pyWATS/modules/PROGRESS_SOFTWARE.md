# Software Module - Functions and REST API Endpoints

## Overview
This document lists all public functions in the Software module and identifies potential REST API endpoints to implement them.

## Function to REST API Endpoint Mapping

| Function | Parameters | Description | Potential REST API Endpoint |
|----------|------------|-------------|----------------------------|
| `is_connected` | None | Check if software module is connected | `software_get_status.sync()` |
| `get_revoked_packages` | tag_names, tag_values | Get revoked packages with file information | `software_get_revoked_packages.sync()` |
| `get_packages` | part_number, process, station_type, revision, station_name, misc, install, display_progress, wait_for_execution, package_status | Get packages based on criteria | `software_get_packages.sync()` |
| `get_packages_by_tag_xpath` | xpath, install, display_progress, wait_for_execution, package_status | Get packages using XPath tag selection | `software_get_packages_by_tag.sync()` |
| `get_packages_by_tag_xpath_simple` | xpath, install, display_progress, wait_for_execution, package_status | Simplified version of XPath tag selection | `software_get_packages_by_tag.sync()` |
| `get_packages_by_tag_dict_simple` | tag_value, install, display_progress, wait_for_execution, package_status | Get packages by tag dictionary (simplified) | `software_get_packages_by_tag.sync()` |
| `get_packages_by_tag_arrays` | tag_names, tag_values, install, display_progress, wait_for_execution, package_status | Get packages by tag arrays | `software_get_packages_by_tag_arrays.sync()` |
| `get_packages_by_tag_dict` | tag_value, install, display_progress, wait_for_execution, package_status | Get packages by tag dictionary | `software_get_packages_by_tag_dict.sync()` |
| `get_package_by_name` | package_name, install, display_progress, wait_for_execution, package_status | Get specific package by name | `software_get_package_by_name.sync()` |
| `get_package_by_name_with_files` | package_name, install, display_progress, wait_for_execution, package_status | Get specific package with associated files | `software_get_package_by_name.sync()` (with file details) |
| `install_package_array` | packages, display_progress, wait_for_execution | Install multiple packages | `software_install_packages.sync()` |
| `install_package_array_with_files` | packages, display_progress, wait_for_execution | Install multiple packages with file handling | `software_install_packages.sync()` (with file handling) |
| `install_package_single` | package, display_progress, wait_for_execution | Install a single package | `software_install_package.sync()` |
| `install_package_single_with_files` | package, display_progress, wait_for_execution | Install a single package with file handling | `software_install_package.sync()` (with file handling) |
| `set_root_folder_path` (static) | root_folder_path, move_existing_packages | Configure root folder for packages | `software_set_root_folder.sync()` |
| `get_root_folder_path` (static) | None | Get current root folder path | `software_get_root_folder.sync()` |
| `delete_all_packages` | prompt_operator | Remove all installed packages | `software_delete_all_packages.sync()` |
| `delete_revoked_packages` | prompt_operator | Remove revoked packages | `software_delete_revoked_packages.sync()` |
| `get_available_packages` | None | Get list of available packages | `software_get_available_packages.sync()` |

## Implementation Status

All functions are currently unimplemented (`NotImplementedError`). The recommended approach is to:

1. Verify if these REST API endpoints actually exist in the codebase
2. Implement the core functions first:
   - `get_packages`
   - `get_package_by_name`
   - `install_package_single`
   - `get_available_packages`
3. Then implement the specialized functions

**Note**: The actual REST API endpoints should be confirmed before implementation as they may have different naming conventions or functionality than suggested here.