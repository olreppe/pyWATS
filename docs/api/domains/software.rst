Software Domain
===============

The Software domain provides comprehensive software distribution and package management capabilities for WATS. It enables you to:

- Manage software packages with versioning and lifecycle tracking
- Deploy test sequencer updates, drivers, and configuration files
- Control release workflows (Draft → Pending → Released → Revoked)
- Upload and distribute software packages as zip archives
- Track package dependencies and metadata with tags
- Monitor download history and package availability
- Manage virtual folder mappings for Production Manager

**Use Cases:**
- Test station software distribution and updates
- Sequencer and driver version management
- Configuration file deployment across manufacturing sites
- License and dependency tracking
- Automated software rollback and revocation
- Package compliance and audit trails

**Domain Health:** A- (52/60) - Very good, production-ready

---

Quick Start
-----------

List Available Packages
^^^^^^^^^^^^^^^^^^^^^^^^

Get all software packages in the system:

.. code-block:: python

   from pywats import pyWATS
   
   api = pyWATS(base_url="https://wats.example.com", token="token")
   
   # Get all packages
   packages = api.software.get_packages()
   
   for pkg in packages:
       print(f"{pkg.name} v{pkg.version} - {pkg.status}")
       print(f"  Created: {pkg.created_utc}")
       print(f"  Files: {len(pkg.files) if pkg.files else 0}")

Get Package by Name
^^^^^^^^^^^^^^^^^^^

Retrieve a specific package with status filtering:

.. code-block:: python

   from pywats.domains.software import PackageStatus
   
   # Get released version of a package
   package = api.software.get_released_package("TestStand Sequencer")
   
   if package:
       print(f"Package: {package.name}")
       print(f"Version: {package.version}")
       print(f"Status: {package.status}")
       print(f"Description: {package.description}")
   
   # Get specific version
   package_v2 = api.software.get_package_by_name(
       "TestStand Sequencer",
       status=PackageStatus.RELEASED,
       version=2
   )

Create and Deploy Package
^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a package, upload files, and release:

.. code-block:: python

   from pywats.domains.software import PackageTag
   
   # Create package in Draft status
   package = api.software.create_package(
       name="TestStand Sequencer Update",
       description="Bug fixes and performance improvements",
       install_on_root=False,
       root_directory="C:\\Program Files\\TestStand",
       priority=10,
       tags=[
           PackageTag(key="component", value="sequencer"),
           PackageTag(key="platform", value="windows")
       ]
   )
   
   print(f"Created: {package.name} (ID: {package.package_id})")
   
   # Upload package files as zip
   with open("sequencer_update.zip", "rb") as f:
       zip_content = f.read()
   
   api.software.upload_zip(
       package.package_id,
       zip_content,
       clean_install=True  # Delete existing files first
   )
   
   # Release workflow: Draft → Pending → Released
   api.software.submit_for_review(package.package_id)
   api.software.release_package(package.package_id)
   
   print("Package released!")

Async Usage for Performance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For concurrent operations and better performance:

.. code-block:: python

   import asyncio
   from pywats import AsyncWATS
   from pywats.domains.software import PackageStatus
   
   async def deploy_multiple_packages():
       async with AsyncWATS(base_url="...", token="...") as api:
           # Get multiple packages concurrently
           pkg_names = ["Sequencer", "Driver Pack", "Config Files"]
           
           packages = await asyncio.gather(*[
               api.software.get_package_by_name(
                   name,
                   status=PackageStatus.RELEASED
               )
               for name in pkg_names
           ])
           
           for pkg in packages:
               if pkg:
                   print(f"Found: {pkg.name} v{pkg.version}")
   
   asyncio.run(deploy_multiple_packages())

Query Packages by Tag
^^^^^^^^^^^^^^^^^^^^^

Filter packages using tag-based metadata:

.. code-block:: python

   # Get all Windows packages
   windows_pkgs = api.software.get_packages_by_tag(
       tag="platform",
       value="windows",
       status=PackageStatus.RELEASED
   )
   
   print(f"Found {len(windows_pkgs)} Windows packages")
   
   # Get all sequencer components
   sequencer_pkgs = api.software.get_packages_by_tag(
       tag="component",
       value="sequencer"
   )

---

Core Concepts
-------------

Type-Safe Enums
^^^^^^^^^^^^^^^

The Software domain provides type-safe enums for IDE autocomplete and compile-time validation:

.. code-block:: python

   from pywats.domains.software import PackageStatus
   
   # Package lifecycle states
   PackageStatus.DRAFT      # "Draft" - Initial creation, editable
   PackageStatus.PENDING    # "Pending" - Under review, locked
   PackageStatus.RELEASED   # "Released" - Production deployment
   PackageStatus.REVOKED    # "Revoked" - Withdrawn from use

Package Model
^^^^^^^^^^^^^

The ``Package`` model represents a software distribution package:

.. code-block:: python

   from pywats.domains.software import Package, PackageTag
   from datetime import datetime
   from uuid import UUID
   
   # Package attributes
   package = Package(
       package_id=UUID("..."),           # Unique identifier
       name="TestStand Sequencer",       # Package name
       description="Test sequencer",     # Description
       version=3,                        # Version number (auto-increment)
       status=PackageStatus.RELEASED,    # Lifecycle status
       install_on_root=False,            # Install location flag
       root_directory="C:\\Program Files\\TestStand",
       priority=10,                      # Installation priority (higher = first)
       tags=[...],                       # List of PackageTag objects
       created_utc=datetime.utcnow(),    # Creation timestamp
       modified_utc=datetime.utcnow(),   # Last modification
       created_by="user@company.com",    # Creator username
       modified_by="admin@company.com",  # Last modifier
       files=[...]                       # List of PackageFile objects
   )

Package Files
^^^^^^^^^^^^^

Files within a package are represented by ``PackageFile``:

.. code-block:: python

   from pywats.domains.software import PackageFile
   
   # Get files in a package
   files = api.software.get_package_files(package.package_id)
   
   for file in files:
       print(f"File: {file.filename}")
       print(f"  Path: {file.path}")
       print(f"  Size: {file.size} bytes")
       print(f"  Checksum: {file.checksum}")
       print(f"  Modified: {file.modified_utc}")

Virtual Folders
^^^^^^^^^^^^^^^

Virtual folders map network paths to local directories:

.. code-block:: python

   # Get all virtual folders
   folders = api.software.get_virtual_folders()
   
   for folder in folders:
       print(f"{folder.name}: {folder.path}")
       print(f"  Description: {folder.description}")

---

Common Use Cases
----------------

Package Release Workflow
^^^^^^^^^^^^^^^^^^^^^^^^^

Complete workflow from draft to release:

.. code-block:: python

   from pywats.domains.software import PackageStatus, PackageTag
   
   # 1. Create package in Draft
   package = api.software.create_package(
       name="Driver Update v2.5",
       description="Critical bug fixes",
       tags=[PackageTag(key="severity", value="high")]
   )
   
   print(f"Created package ID: {package.package_id}")
   
   # 2. Upload package content
   with open("driver_v2.5.zip", "rb") as f:
       api.software.upload_zip(package.package_id, f.read())
   
   # 3. Submit for review (Draft → Pending)
   api.software.submit_for_review(package.package_id)
   print("Status: Pending Review")
   
   # 4. Verify package
   pkg_files = api.software.get_package_files(package.package_id)
   print(f"Package contains {len(pkg_files)} files")
   
   # 5. Release (Pending → Released)
   api.software.release_package(package.package_id)
   print("Status: Released")
   
   # 6. If issues found, revoke (Released → Revoked)
   # api.software.revoke_package(package.package_id)

Update Existing Package
^^^^^^^^^^^^^^^^^^^^^^^

Modify package metadata and files:

.. code-block:: python

   # Get existing package
   package = api.software.get_package_by_name("Config Files")
   
   if package:
       # Update metadata
       package.description = "Updated configuration for Q1 2026"
       package.priority = 20
       
       # Add new tag
       if not package.tags:
           package.tags = []
       package.tags.append(PackageTag(key="quarter", value="Q1-2026"))
       
       # Save changes
       updated = api.software.update_package(package)
       print(f"Updated: {updated.name}")

Find and Filter Packages
^^^^^^^^^^^^^^^^^^^^^^^^^

Query packages with various filters:

.. code-block:: python

   from pywats.domains.software import PackageStatus
   
   # All packages
   all_packages = api.software.get_packages()
   
   # Released packages only
   released = [p for p in all_packages 
               if p.status == PackageStatus.RELEASED]
   
   # Draft packages (work in progress)
   drafts = [p for p in all_packages 
             if p.status == PackageStatus.DRAFT]
   
   # High-priority packages
   high_priority = [p for p in all_packages 
                    if p.priority and p.priority >= 50]
   
   # Recent packages (last 30 days)
   from datetime import datetime, timedelta
   cutoff = datetime.utcnow() - timedelta(days=30)
   recent = [p for p in all_packages 
             if p.created_utc and p.created_utc >= cutoff]
   
   print(f"Released: {len(released)}")
   print(f"Drafts: {len(drafts)}")
   print(f"High Priority: {len(high_priority)}")
   print(f"Recent (30d): {len(recent)}")

Package Cleanup
^^^^^^^^^^^^^^^

Delete old or obsolete packages:

.. code-block:: python

   # Delete by ID
   deleted = api.software.delete_package(package_id)
   if deleted:
       print("Package deleted")
   
   # Delete by name and version
   deleted = api.software.delete_package_by_name(
       "Old Sequencer",
       version=1
   )
   
   # Bulk cleanup of revoked packages
   all_packages = api.software.get_packages()
   revoked = [p for p in all_packages 
              if p.status == PackageStatus.REVOKED]
   
   for pkg in revoked:
       api.software.delete_package(pkg.package_id)
       print(f"Deleted: {pkg.name} v{pkg.version}")

---

Advanced Features
-----------------

Package Version Management
^^^^^^^^^^^^^^^^^^^^^^^^^^

Automatic version tracking and history:

.. code-block:: python

   # Version numbers auto-increment when creating packages
   # with the same name
   
   # Create v1
   v1 = api.software.create_package(name="My Software")
   print(f"Version: {v1.version}")  # 1
   
   # Create v2 (same name)
   v2 = api.software.create_package(name="My Software")
   print(f"Version: {v2.version}")  # 2
   
   # Get specific version
   specific = api.software.get_package_by_name(
       "My Software",
       version=1
   )

File Attribute Management
^^^^^^^^^^^^^^^^^^^^^^^^^^

Update attributes for individual package files:

.. code-block:: python

   # Get package files
   files = api.software.get_package_files(package_id)
   
   # Update file attributes
   for file in files:
       if file.filename.endswith('.exe'):
           api.software.update_file_attribute(
               file.file_id,
               attributes="executable,signed"
           )

Rollback Workflow
^^^^^^^^^^^^^^^^^

Revoke problematic release and deploy previous version:

.. code-block:: python

   # Revoke current release (v3)
   current = api.software.get_package_by_name(
       "TestStand Sequencer",
       status=PackageStatus.RELEASED,
       version=3
   )
   
   if current:
       api.software.revoke_package(current.package_id)
       print(f"Revoked v{current.version}")
   
   # Re-release previous version (v2)
   previous = api.software.get_package_by_name(
       "TestStand Sequencer",
       version=2
   )
   
   if previous:
       # Return to draft if needed
       if previous.status == PackageStatus.REVOKED:
           api.software.return_to_draft(previous.package_id)
       
       # Release again
       api.software.submit_for_review(previous.package_id)
       api.software.release_package(previous.package_id)
       print(f"Re-released v{previous.version}")

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.software.async_service.AsyncSoftwareService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. note::
   The repository layer is for internal use. Most users should use the service layer above.

.. autoclass:: pywats.domains.software.async_repository.AsyncSoftwareRepository
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

Package
^^^^^^^

.. autoclass:: pywats.domains.software.models.Package
   :members:
   :undoc-members:
   :show-inheritance:

PackageFile
^^^^^^^^^^^

.. autoclass:: pywats.domains.software.models.PackageFile
   :members:
   :undoc-members:
   :show-inheritance:

PackageTag
^^^^^^^^^^

.. autoclass:: pywats.domains.software.models.PackageTag
   :members:
   :undoc-members:
   :show-inheritance:

VirtualFolder
^^^^^^^^^^^^^

.. autoclass:: pywats.domains.software.models.VirtualFolder
   :members:
   :undoc-members:
   :show-inheritance:

Enums
-----

.. automodule:: pywats.domains.software.enums
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Use Type-Safe Enums**
   Always use ``PackageStatus`` enum instead of string literals for better IDE support and fewer errors.

2. **Leverage Async for Performance**
   When deploying multiple packages or querying many items, use ``AsyncWATS`` and ``asyncio.gather()`` for significant performance gains.

3. **Tag Your Packages**
   Use ``PackageTag`` objects to add metadata (platform, component, severity) for easier filtering and organization.

4. **Follow Release Workflow**
   Always go through Draft → Pending → Released workflow to maintain proper audit trails and approvals.

5. **Use Priority Wisely**
   Set higher priority values (e.g., 50-100) for critical packages that must be installed first. Default is 0.

6. **Clean Installs for Major Updates**
   Use ``clean_install=True`` when uploading zips for major updates to avoid file conflicts.

7. **Version Control Integration**
   Match package versions to your source control tags for traceability (v1 = tag v1.0.0).

---

Related Documentation
---------------------

- :doc:`../usage/software-domain` - Detailed usage guide with more examples
- :doc:`../domains/production` - Production tracking and station management
- :doc:`../getting-started` - Installation and setup
- :doc:`../../examples/software` - Complete example scripts

---

Domain Health
-------------

**Score:** 52/60 (A-) - Very good, production-ready

See :doc:`../../domain_health/software` for detailed domain health assessment.

**Strengths:**
- Perfect Service→Repository→HttpClient architecture
- 100% ErrorHandler coverage
- Complete ``Raises:`` documentation (17 methods)
- Clean package management models
- Type-safe enums for better developer experience
- Comprehensive workflow support (Draft/Pending/Released/Revoked)

**Recent Improvements (Jan 2026):**
- Added ``Raises:`` sections to all 17 service methods
- Enhanced model documentation with field descriptions
- Improved test coverage for package lifecycle

**Key Features:**
- ✅ Package versioning with auto-increment
- ✅ Tag-based metadata and filtering
- ✅ Zip file upload and distribution
- ✅ Status workflow (Draft→Pending→Released→Revoked)
- ✅ Virtual folder management
- ✅ File checksum validation
- ✅ Download history tracking
