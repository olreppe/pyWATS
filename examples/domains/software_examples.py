"""
Software Package Management Examples

This example demonstrates software package tracking in pyWATS.

DOMAIN KNOWLEDGE: Software Packages vs Firmware
================================================

1. SOFTWARE PACKAGE
   - Versioned software/firmware
   - Example: "Controller Firmware v2.4.1"
   - Tracks: Version, build date, files, checksums
   - Use: Ensure correct software loaded on units

2. PACKAGE DEPLOYMENT
   - Loading software onto units
   - Example: Load firmware v2.4.1 onto unit SN-12345
   - Tracks: What version is on which unit
   - Use: Configuration management, traceability

SOFTWARE LIFECYCLE:
===================

1. Create package (register version)
2. Upload files (firmware binary, config files)
3. Deploy to units (load onto hardware)
4. Track deployment history
5. Manage updates/rollbacks

USE CASES:
==========

- Firmware version control
- Configuration management
- Software traceability
- Audit compliance
- Rollback capability
"""

from pywats import pyWATS
from datetime import datetime
import os


def example_1_create_software_package(api: pyWATS):
    """Create and register a software package."""
    print("=" * 60)
    print("EXAMPLE 1: Create Software Package")
    print("=" * 60)
    
    package = api.software.create_package(
        name="Controller Firmware",
        version="2.4.1",
        description="Production firmware with bug fixes",
        release_date=datetime.now()
    )
    
    print(f"Package: {package.name}")
    print(f"Version: {package.version}")
    print(f"ID: {package.id}")
    print("=" * 60)
    
    return package.id


def example_2_deploy_to_unit(api: pyWATS):
    """Deploy software package to a unit."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Deploy Software to Unit")
    print("=" * 60)
    
    serial = f"SN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    print(f"Deploying firmware v2.4.1 to {serial}")
    print(f"Status: SUCCESS")
    print("=" * 60)


def example_3_version_history(api: pyWATS):
    """Track software versions over time."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Version History")
    print("=" * 60)
    
    versions = [
        {"version": "2.4.1", "date": "2026-01-15", "units": 450},
        {"version": "2.4.0", "date": "2025-12-01", "units": 280},
        {"version": "2.3.5", "date": "2025-10-15", "units": 95}
    ]
    
    print("Deployed Versions:\n")
    for v in versions:
        print(f"  v{v['version']}: {v['units']} units ({v['date']})")
    
    print("=" * 60)


def main():
    """Run all software examples."""
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("SOFTWARE DOMAIN EXAMPLES")
    print("=" * 60)
    
    example_1_create_software_package(api)
    example_2_deploy_to_unit(api)
    example_3_version_history(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
