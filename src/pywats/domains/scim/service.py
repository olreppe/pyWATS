"""SCIM domain service.

Business logic layer for SCIM (System for Cross-domain Identity Management) operations.

This module provides a high-level interface for SCIM user provisioning.

PUBLIC API
----------
Available via `client.scim`:
- get_token()           - Get JWT token for Azure provisioning
- get_users()           - Get all SCIM users
- iter_users()          - Iterate over users with automatic pagination
- create_user()         - Create a new user
- get_user()            - Get user by ID
- delete_user()         - Delete user by ID
- update_user()         - Update user attributes
- get_user_by_username() - Get user by username
- deactivate_user()     - Convenience method to deactivate a user
- set_user_active()     - Convenience method to set user active status

USAGE EXAMPLES
--------------
>>> # Get provisioning token for Azure AD configuration
>>> token = api.scim.get_token(duration_days=90)
>>> print(f"Token: {token.token}")

>>> # List all provisioned users
>>> users = api.scim.get_users()
>>> for user in users.resources:
...     print(f"{user.user_name}: {user.display_name}")

>>> # Iterate over users with automatic pagination (memory efficient)
>>> for user in api.scim.iter_users(page_size=50):
...     print(f"{user.user_name}: {user.display_name}")

>>> # Create a new user
>>> from pywats.domains.scim import ScimUser, ScimUserName
>>> user = ScimUser(
...     user_name="john.doe@example.com",
...     display_name="John Doe",
...     active=True,
...     name=ScimUserName(given_name="John", family_name="Doe")
... )
>>> created = api.scim.create_user(user)

>>> # Deactivate a user
>>> api.scim.deactivate_user(user.id)
"""
from typing import Optional, List, Any, Iterator, Callable

from .repository import ScimRepository
from .models import (
    ScimToken,
    ScimUser,
    ScimUserName,
    ScimUserEmail,
    ScimPatchRequest,
    ScimPatchOperation,
    ScimListResponse,
)


class ScimService:
    """
    Service for SCIM user provisioning operations.
    
    Provides high-level methods for managing SCIM users in WATS.
    
    SCIM (System for Cross-domain Identity Management) is used for automatic
    user provisioning from Azure Active Directory to WATS.
    
    Attributes:
        _repository: The underlying repository for API calls
        
    Example:
        >>> # Access via the main client
        >>> users = api.scim.get_users()
        >>> print(f"Total users: {users.total_results}")
    """

    def __init__(self, repository: ScimRepository):
        """
        Initialize the SCIM service.
        
        Args:
            repository: Repository instance for API access
        """
        self._repository = repository

    def get_token(self, duration_days: int = 90) -> Optional[ScimToken]:
        """
        Get a JWT token for SCIM provisioning from Azure AD.
        
        Generates a token that can be used to configure automatic user
        provisioning from Azure Active Directory to WATS.
        
        Args:
            duration_days: Token validity duration in days (default: 90)
            
        Returns:
            ScimToken with JWT and expiration info, or None on failure
            
        Raises:
            PyWATSError: If the request fails
            
        Example:
            >>> token = api.scim.get_token(duration_days=90)
            >>> if token:
            ...     print(f"Token: {token.token[:50]}...")
            ...     print(f"Expires: {token.expires_utc}")
        """
        return self._repository.get_token(duration_days=duration_days)

    def get_users(
        self,
        start_index: Optional[int] = None,
        count: Optional[int] = None,
    ) -> ScimListResponse:
        """
        Get SCIM users with optional pagination.
        
        Returns a list of users provisioned via SCIM.
        
        Args:
            start_index: 1-based starting index for pagination (SCIM spec)
            count: Maximum number of users to return per page
            
        Returns:
            ScimListResponse containing user resources (may be empty)
            
        Raises:
            PyWATSError: If the request fails
            
        Example:
            >>> # Get all users (single page)
            >>> response = api.scim.get_users()
            >>> print(f"Total users: {response.total_results}")
            >>> for user in response.resources or []:
            ...     status = "active" if user.active else "inactive"
            ...     print(f"  {user.user_name}: {status}")
            
            >>> # Get paginated results
            >>> page1 = api.scim.get_users(start_index=1, count=50)
            >>> page2 = api.scim.get_users(start_index=51, count=50)
        """
        return self._repository.get_users(start_index=start_index, count=count)

    def iter_users(
        self,
        page_size: int = 100,
        max_users: Optional[int] = None,
        on_page: Optional[Callable[[int, int, Optional[int]], None]] = None,
    ) -> Iterator[ScimUser]:
        """
        Iterate over all SCIM users with automatic pagination.
        
        Memory-efficient iterator that fetches users page by page.
        Supports early termination (break) without loading remaining pages.
        
        Args:
            page_size: Number of users per page (default: 100)
            max_users: Maximum users to retrieve (default: all)
            on_page: Optional callback (page_num, users_so_far, total)
            
        Yields:
            ScimUser objects one at a time
            
        Example:
            >>> # Iterate over all users
            >>> for user in api.scim.iter_users():
            ...     print(f"{user.user_name}: {user.display_name}")
            
            >>> # Process with progress tracking
            >>> def on_progress(page, count, total):
            ...     print(f"Page {page}: {count}/{total or '?'} users")
            >>> for user in api.scim.iter_users(page_size=50, on_page=on_progress):
            ...     process(user)
            
            >>> # Early termination - only fetches needed pages
            >>> for user in api.scim.iter_users():
            ...     if user.user_name == "target@example.com":
            ...         print(f"Found: {user.id}")
            ...         break
            
            >>> # Limit total users
            >>> first_100 = list(api.scim.iter_users(max_users=100))
            
        Note:
            - Uses SCIM pagination (1-based indexing)
            - Memory-efficient: only one page loaded at a time
            - Server determines total_results
        """
        from ...core.pagination import paginate
        
        return paginate(
            fetch_page=lambda start, count: self._repository.get_users(
                start_index=start, 
                count=count
            ),
            get_items=lambda response: response.resources or [],
            get_total=lambda response: response.total_results,
            page_size=page_size,
            start_index=1,  # SCIM uses 1-based indexing
            max_items=max_users,
            on_page=on_page,
        )

    def create_user(self, user: ScimUser) -> Optional[ScimUser]:
        """
        Create a new SCIM user.
        
        Creates a new user in the WATS system via SCIM provisioning.
        
        Args:
            user: User data to create
            
        Returns:
            The created ScimUser with assigned ID, or None on failure
            
        Raises:
            PyWATSError: If the request fails
            
        Example:
            >>> from pywats.domains.scim import ScimUser, ScimUserName
            >>> user = ScimUser(
            ...     user_name="jane.doe@example.com",
            ...     display_name="Jane Doe",
            ...     active=True,
            ...     name=ScimUserName(given_name="Jane", family_name="Doe")
            ... )
            >>> created = api.scim.create_user(user)
            >>> if created:
            ...     print(f"Created user ID: {created.id}")
        """
        return self._repository.create_user(user)

    def get_user(self, user_id: str) -> Optional[ScimUser]:
        """
        Get a SCIM user by ID.
        
        Retrieves user details by their unique identifier.
        
        Args:
            user_id: The unique user identifier (GUID)
            
        Returns:
            ScimUser details, or None if not found
            
        Raises:
            PyWATSError: If the request fails
            
        Example:
            >>> user = api.scim.get_user("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
            >>> print(f"User: {user.display_name}")
            >>> print(f"Email: {user.user_name}")
            >>> print(f"Active: {user.active}")
        """
        return self._repository.get_user(user_id)

    def delete_user(self, user_id: str) -> None:
        """
        Delete a SCIM user by ID.
        
        Removes a user from the WATS system.
        
        Args:
            user_id: The unique user identifier (GUID)
            
        Raises:
            PyWATSError: If the request fails or user not found
            
        Example:
            >>> api.scim.delete_user("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
            >>> print("User deleted successfully")
        """
        return self._repository.delete_user(user_id)

    def update_user(self, user_id: str, patch_request: ScimPatchRequest) -> Optional[ScimUser]:
        """
        Update a SCIM user using SCIM patch operations.
        
        Updates user attributes using the SCIM PatchOp format.
        Only "replace" operations are supported.
        
        Args:
            user_id: The unique user identifier (GUID)
            patch_request: SCIM patch request with operations to apply
            
        Returns:
            Updated ScimUser details, or None on failure
            
        Raises:
            PyWATSError: If the request fails or user not found
            
        Example:
            >>> from pywats.domains.scim import ScimPatchRequest, ScimPatchOperation
            >>> patch = ScimPatchRequest(
            ...     operations=[
            ...         ScimPatchOperation(op="replace", path="displayName", value="Jane Smith")
            ...     ]
            ... )
            >>> updated = api.scim.update_user("user-id", patch)
            >>> print(f"Updated name: {updated.display_name}")
        """
        return self._repository.update_user(user_id, patch_request)

    def get_user_by_username(self, username: str) -> Optional[ScimUser]:
        """
        Get a SCIM user by username.
        
        Retrieves user details by their username (typically email).
        
        Args:
            username: The username to search for
            
        Returns:
            ScimUser details, or None if not found
            
        Raises:
            PyWATSError: If the request fails
            
        Example:
            >>> user = api.scim.get_user_by_username("jane.doe@example.com")
            >>> if user:
            ...     print(f"User ID: {user.id}")
            ...     print(f"Active: {user.active}")
        """
        return self._repository.get_user_by_username(username)

    # Convenience methods

    def deactivate_user(self, user_id: str) -> Optional[ScimUser]:
        """
        Deactivate a SCIM user.
        
        Convenience method to set a user's active status to False.
        
        Args:
            user_id: The unique user identifier (GUID)
            
        Returns:
            Updated ScimUser details, or None on failure
            
        Raises:
            PyWATSError: If the request fails or user not found
            
        Example:
            >>> deactivated = api.scim.deactivate_user("user-id")
            >>> if deactivated:
            ...     print(f"User {deactivated.display_name} is now inactive")
        """
        return self.set_user_active(user_id, active=False)

    def set_user_active(self, user_id: str, active: bool) -> Optional[ScimUser]:
        """
        Set a SCIM user's active status.
        
        Convenience method to activate or deactivate a user.
        
        Args:
            user_id: The unique user identifier (GUID)
            active: True to activate, False to deactivate
            
        Returns:
            Updated ScimUser details, or None on failure
            
        Raises:
            PyWATSError: If the request fails or user not found
            
        Example:
            >>> # Activate a user
            >>> user = api.scim.set_user_active("user-id", active=True)
            >>> if user:
            ...     print(f"User active: {user.active}")
        """
        patch = ScimPatchRequest(
            operations=[
                ScimPatchOperation(op="replace", path="active", value=active)
            ]
        )
        return self._repository.update_user(user_id, patch)

    def update_display_name(self, user_id: str, display_name: str) -> Optional[ScimUser]:
        """
        Update a SCIM user's display name.
        
        Convenience method to update the display name.
        
        Args:
            user_id: The unique user identifier (GUID)
            display_name: New display name
            
        Returns:
            Updated ScimUser details, or None on failure
            
        Raises:
            PyWATSError: If the request fails or user not found
            
        Example:
            >>> updated = api.scim.update_display_name("user-id", "Jane Smith")
            >>> if updated:
            ...     print(f"New name: {updated.display_name}")
        """
        patch = ScimPatchRequest(
            operations=[
                ScimPatchOperation(op="replace", path="displayName", value=display_name)
            ]
        )
        return self._repository.update_user(user_id, patch)
