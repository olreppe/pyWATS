SCIM Domain
===========

The SCIM (System for Cross-domain Identity Management) domain provides comprehensive user and group provisioning capabilities for WATS. It enables seamless integration with Azure Active Directory and other identity providers for automated user lifecycle management. Features include:

- Generate JWT tokens for Azure AD automatic provisioning
- Create, read, update, and deactivate users programmatically
- User lifecycle management (onboarding, updates, offboarding)
- User search by ID or username
- SCIM 2.0 compliant PATCH operations for user updates
- Async support for high-performance batch operations

**Use Cases:**
- Azure AD automatic user provisioning and SSO integration
- Automated user onboarding and offboarding workflows
- User profile synchronization from external systems
- Bulk user management and migrations
- Audit trail of user provisioning events
- Self-service user management portals

**Domain Health:** A (56/60) - Excellent, production-ready

---

Quick Start
-----------

Generate Provisioning Token for Azure AD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get a JWT token to configure Azure AD automatic provisioning:

.. code-block:: python

   from pywats import pyWATS
   
   api = pyWATS(base_url="https://wats.example.com", token="admin_token")
   
   # Generate token valid for 90 days (default)
   token_response = api.scim.get_token(duration_days=90)
   
   print(f"SCIM Token: {token_response.token}")
   print(f"Expires: {token_response.expires_utc}")
   
   # Use this token in Azure AD Enterprise Application
   # -> Provisioning -> Admin Credentials -> Secret Token

List All Users
^^^^^^^^^^^^^^

Retrieve all SCIM users with pagination:

.. code-block:: python

   # Get first page of users (100 per page by default)
   response = api.scim.get_users(start_index=1, count=100)
   
   print(f"Total users: {response.total_results}")
   for user in response.resources:
       status = "Active" if user.active else "Inactive"
       print(f"{user.user_name} - {user.display_name} [{status}]")

Create New User
^^^^^^^^^^^^^^^

Provision a new user programmatically:

.. code-block:: python

   from pywats.domains.scim import ScimUser, ScimUserName, ScimUserEmail
   
   # Create user object
   new_user = ScimUser(
       user_name="jane.smith@example.com",
       display_name="Jane Smith",
       active=True,
       name=ScimUserName(
           given_name="Jane",
           family_name="Smith"
       ),
       emails=[
           ScimUserEmail(
               value="jane.smith@example.com",
               type="work",
               primary=True
           )
       ]
   )
   
   # Provision user
   created = api.scim.create_user(new_user)
   print(f"User created with ID: {created.id}")

---

Core Concepts
-------------

SCIM 2.0 Protocol
^^^^^^^^^^^^^^^^^

SCIM (System for Cross-domain Identity Management) is an industry-standard REST protocol for managing user identities. The WATS SCIM implementation follows RFC 7643 and RFC 7644 specifications.

User Resource Model
^^^^^^^^^^^^^^^^^^^

SCIM users contain standard attributes defined by the SCIM specification:

.. code-block:: python

   from pywats.domains.scim import ScimUser, ScimUserName
   
   user = ScimUser(
       id="550e8400-e29b-41d4-a716-446655440000",
       user_name="john.doe@example.com",
       display_name="John Doe",
       active=True,
       external_id="azure-ad-object-id",
       name=ScimUserName(
           given_name="John",
           family_name="Doe"
       )
   )

---

Common Use Cases
----------------

Azure AD Automatic Provisioning Setup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete Azure AD integration workflow:

.. code-block:: python

   from pywats import AsyncWATS
   
   async with AsyncWATS(base_url="...", token="...") as api:
       
       # Step 1: Generate SCIM token for Azure AD
       token_response = await api.scim.get_token(duration_days=90)
       
       print("Azure AD SCIM Configuration:")
       print(f"  Tenant URL: {api.base_url}/api/scim/v2")
       print(f"  Secret Token: {token_response.token}")
       print(f"  Token Expires: {token_response.expires_utc}")
       
       # Step 2: In Azure AD Portal:
       # - Go to Enterprise Applications → Your App
       # - Provisioning → Admin Credentials
       # - Tenant URL: https://wats.example.com/api/scim/v2
       # - Secret Token: <paste token from above>
       # - Test Connection → Save
       
       # Step 3: Verify connectivity
       users = await api.scim.get_users(start_index=1, count=10)
       print(f"\n✓ Connection verified - {users.total_results} users found")

User Lifecycle Management
^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete user onboarding and offboarding workflow:

.. code-block:: python

   from pywats.domains.scim import ScimUser, ScimUserName, ScimUserEmail
   
   async def onboard_new_employee(employee_data: dict):
       """Provision new employee in WATS."""
       
       # Create user
       new_user = ScimUser(
           user_name=employee_data['email'],
           display_name=f"{employee_data['first_name']} {employee_data['last_name']}",
           active=True,
           external_id=employee_data.get('azure_ad_id'),
           name=ScimUserName(
               given_name=employee_data['first_name'],
               family_name=employee_data['last_name']
           ),
           emails=[
               ScimUserEmail(
                   value=employee_data['email'],
                   type="work",
                   primary=True
               )
           ]
       )
       
       created = await api.scim.create_user(new_user)
       print(f"✓ User {created.user_name} provisioned (ID: {created.id})")
       return created
   
   async def offboard_employee(user_id: str):
       """Deactivate departing employee."""
       
       # Deactivate user (sets active=False)
       await api.scim.deactivate_user(user_id)
       print(f"✓ User {user_id} deactivated")
       
       # Verify deactivation
       user = await api.scim.get_user_by_id(user_id)
       assert not user.active, "Deactivation failed"

Bulk User Operations
^^^^^^^^^^^^^^^^^^^^^

Efficiently process multiple users with async:

.. code-block:: python

   import asyncio
   from typing import List
   
   async def bulk_create_users(users_data: List[dict]):
       """Create multiple users concurrently."""
       
       tasks = []
       for user_data in users_data:
           user = ScimUser(
               user_name=user_data['email'],
               display_name=user_data['name'],
               active=True,
               external_id=user_data.get('external_id')
           )
           task = api.scim.create_user(user)
           tasks.append(task)
       
       # Create all users in parallel
       results = await asyncio.gather(*tasks, return_exceptions=True)
       
       # Process results
       success_count = sum(1 for r in results if not isinstance(r, Exception))
       print(f"Created {success_count}/{len(users_data)} users")
       
       return results
   
   async def bulk_deactivate_users(user_ids: List[str]):
       """Deactivate multiple users concurrently."""
       
       tasks = [api.scim.deactivate_user(uid) for uid in user_ids]
       await asyncio.gather(*tasks)
       print(f"✓ Deactivated {len(user_ids)} users")

User Profile Synchronization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sync user profiles from external HR system:

.. code-block:: python

   from pywats.domains.scim import ScimPatchRequest, ScimPatchOperation
   
   async def sync_user_from_hr_system(hr_record: dict):
       """Update WATS user from HR system data."""
       
       # Find user by username
       user = await api.scim.get_user_by_username(hr_record['email'])
       
       if not user:
           print(f"User {hr_record['email']} not found - creating...")
           return await onboard_new_employee(hr_record)
       
       # Build PATCH operations for changed fields
       operations = []
       
       if hr_record['display_name'] != user.display_name:
           operations.append(
               ScimPatchOperation(
                   op="replace",
                   path="displayName",
                   value=hr_record['display_name']
               )
           )
       
       if hr_record['active'] != user.active:
           operations.append(
               ScimPatchOperation(
                   op="replace",
                   path="active",
                   value=hr_record['active']
               )
           )
       
       if operations:
           patch_request = ScimPatchRequest(Operations=operations)
           updated = await api.scim.patch_user(user.id, patch_request)
           print(f"✓ Updated {user.user_name}: {len(operations)} changes")
       else:
           print(f"✓ {user.user_name}: No changes needed")

User Search and Reporting
^^^^^^^^^^^^^^^^^^^^^^^^^^

Query and analyze user directory:

.. code-block:: python

   async def generate_user_report():
       """Generate comprehensive user directory report."""
       
       # Get all users efficiently with pagination
       all_users = []
       start_index = 1
       page_size = 100
       
       while True:
           response = await api.scim.get_users(
               start_index=start_index,
               count=page_size
           )
           
           all_users.extend(response.resources)
           
           if len(all_users) >= response.total_results:
               break
           
           start_index += page_size
       
       # Analyze users
       active_users = [u for u in all_users if u.active]
       inactive_users = [u for u in all_users if not u.active]
       azure_synced = [u for u in all_users if u.external_id]
       
       print("\nUser Directory Report:")
       print(f"  Total Users: {len(all_users)}")
       print(f"  Active: {len(active_users)}")
       print(f"  Inactive: {len(inactive_users)}")
       print(f"  Azure AD Synced: {len(azure_synced)}")
       
       # List recently inactive users
       print("\nRecently Deactivated Users:")
       for user in inactive_users[:10]:
           print(f"  - {user.user_name} ({user.display_name})")

Integration Monitoring and Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Monitor Azure AD sync health:

.. code-block:: python

   from datetime import datetime, timedelta
   
   async def validate_azure_ad_sync():
       """Verify Azure AD synchronization is working correctly."""
       
       # Get all users
       response = await api.scim.get_users(start_index=1, count=1000)
       users = response.resources
       
       # Check for users without external IDs (not synced from Azure AD)
       unsynced = [u for u in users if not u.external_id]
       
       # Check for duplicate usernames
       usernames = [u.user_name for u in users]
       duplicates = [un for un in set(usernames) if usernames.count(un) > 1]
       
       # Check for invalid email formats
       invalid_emails = [
           u for u in users 
           if '@' not in u.user_name or '.' not in u.user_name
       ]
       
       # Generate sync health report
       print("\nAzure AD Sync Health:")
       print(f"  Total Users: {len(users)}")
       print(f"  Synced from Azure AD: {len(users) - len(unsynced)}")
       print(f"  Manual/Unsynced: {len(unsynced)}")
       
       if duplicates:
           print(f"  ⚠ Duplicate Usernames: {len(duplicates)}")
           for dup in duplicates:
               print(f"    - {dup}")
       
       if invalid_emails:
           print(f"  ⚠ Invalid Email Formats: {len(invalid_emails)}")
       
       # Test token validity
       try:
           token = await api.scim.get_token(duration_days=1)
           print(f"  ✓ SCIM Token Valid (expires: {token.expires_utc})")
       except Exception as e:
           print(f"  ✗ Token Generation Failed: {e}")

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.scim.async_service.AsyncScimService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. note::
   The repository is the low-level data access layer. Most users should use 
   the service layer (AsyncScimService) instead.

.. autoclass:: pywats.domains.scim.async_repository.AsyncScimRepository
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

User Models
^^^^^^^^^^^

.. autoclass:: pywats.domains.scim.models.ScimUser
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.scim.models.ScimUserName
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.scim.models.ScimUserEmail
   :members:
   :undoc-members:
   :show-inheritance:

Token and Response Models
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.scim.models.ScimToken
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.scim.models.ScimListResponse
   :members:
   :undoc-members:
   :show-inheritance:

PATCH Models
^^^^^^^^^^^^

.. autoclass:: pywats.domains.scim.models.ScimPatchRequest
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywats.domains.scim.models.ScimPatchOperation
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Secure Token Management**
   Store SCIM tokens securely and rotate them regularly. Never commit tokens to source control.

2. **Use Convenience Methods**
   Leverage ``deactivate_user()`` and ``set_user_active()`` instead of manually creating PATCH requests.

3. **Leverage Async for Batch Operations**
   When creating, updating, or deactivating multiple users, always use ``AsyncWATS`` with ``asyncio.gather()``.

4. **Handle Pagination for Large User Sets**
   Use ``iter_users()`` for memory-efficient processing of large user directories.

5. **Validate External IDs**
   Always set ``external_id`` when integrating with Azure AD for proper user mapping.

---

Related Documentation
---------------------

- :doc:`../usage/scim-domain` - Detailed usage guide with Azure AD setup
- :doc:`../getting-started` - Installation and setup
- Azure AD SCIM Documentation: https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/

---

Domain Health
-------------

**Score:** 56/60 (A) - Excellent, production-ready

**Strengths:**
- Clean Service→Repository→HttpClient architecture
- 100% ErrorHandler coverage on all operations
- SCIM 2.0 compliant implementation (RFC 7643, RFC 7644)
- Full async support with memory-efficient iterators
- Production-tested with Azure AD integration
