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
