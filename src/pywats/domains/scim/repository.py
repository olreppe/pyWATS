"""SCIM domain repository.

Data access layer for SCIM (System for Cross-domain Identity Management) operations.

This module provides direct API access for SCIM user provisioning endpoints.

BACKEND API MAPPING
-------------------
- GET    /api/SCIM/v2/Token           -> get_token()
- GET    /api/SCIM/v2/Users           -> get_users()
- POST   /api/SCIM/v2/Users           -> create_user()
- GET    /api/SCIM/v2/Users/{id}      -> get_user()
- DELETE /api/SCIM/v2/Users/{id}      -> delete_user()
- PATCH  /api/SCIM/v2/Users/{id}      -> update_user()
- GET    /api/SCIM/v2/Users/userName={userName} -> get_user_by_username()

USAGE NOTE:
-----------
This class is typically not instantiated directly. Instead, use the service layer
via `client.scim` for a more user-friendly interface.
"""
from typing import Optional, TYPE_CHECKING
import logging

if TYPE_CHECKING:
    from ...core import HttpClient
    from ...core.exceptions import ErrorHandler

from .models import (
    ScimToken,
    ScimUser,
    ScimPatchRequest,
    ScimListResponse,
)

logger = logging.getLogger(__name__)


class ScimRepository:
    """
    Repository for SCIM API operations.
    
    Provides low-level data access methods for SCIM user provisioning.
    
    This repository maps directly to the backend SCIM API endpoints.
    For most use cases, prefer using the ScimService via `client.scim`.
    
    Attributes:
        _http_client: HTTP client for API calls
        _error_handler: Error handler for response processing
        
    Example:
        >>> # Direct repository usage (typically use service instead)
        >>> repo = ScimRepository(http_client, error_handler)
        >>> token = repo.get_token(duration_days=90)
    """

    def __init__(
        self, 
        http_client: "HttpClient",
        error_handler: Optional["ErrorHandler"] = None
    ):
        """
        Initialize the SCIM repository.
        
        Args:
            http_client: Configured HTTP client for API calls
            error_handler: Error handler for response processing (default: STRICT mode)
        """
        self._http_client = http_client
        # Import here to avoid circular imports
        from ...core.exceptions import ErrorHandler, ErrorMode
        self._error_handler = error_handler or ErrorHandler(ErrorMode.STRICT)

    def get_token(self, duration_days: int = 90) -> Optional[ScimToken]:
        """
        Get a JWT token for SCIM provisioning from Azure AD.
        
        Generates a token that can be used to configure automatic user
        provisioning from Azure Active Directory to WATS.
        
        Maps to: GET /api/SCIM/v2/Token?duration={duration}
        
        Args:
            duration_days: Token validity duration in days (default: 90)
            
        Returns:
            ScimToken with JWT and expiration info, or None if not found
            
        Raises:
            PyWATSError: If the request fails or server returns an error
            
        Example:
            >>> token = repo.get_token(duration_days=90)
            >>> print(f"Token expires: {token.expires_utc}")
        """
        response = self._http_client.get(
            "/api/SCIM/v2/Token",
            params={"duration": duration_days}
        )
        data = self._error_handler.handle_response(
            response, operation="get_token", allow_empty=False
        )
        if data:
            return ScimToken.model_validate(data)
        return None

    def get_users(self) -> ScimListResponse:
        """
        Get all SCIM users.
        
        Returns a list of all users provisioned via SCIM.
        
        Maps to: GET /api/SCIM/v2/Users
        
        Returns:
            ScimListResponse containing user resources (may be empty)
            
        Raises:
            PyWATSError: If the request fails or server returns an error
            
        Example:
            >>> response = repo.get_users()
            >>> for user in response.resources or []:
            ...     print(f"{user.user_name}: {user.active}")
        """
        response = self._http_client.get("/api/SCIM/v2/Users")
        data = self._error_handler.handle_response(
            response, operation="get_users", allow_empty=True
        )
        if data:
            return ScimListResponse.model_validate(data)
        # Return empty list response
        return ScimListResponse(resources=[], total_results=0)

    def create_user(self, user: ScimUser) -> Optional[ScimUser]:
        """
        Create a new SCIM user.
        
        Creates a new user in the WATS system via SCIM provisioning.
        
        Maps to: POST /api/SCIM/v2/Users
        
        Args:
            user: User data to create
            
        Returns:
            The created ScimUser with assigned ID, or None on failure
            
        Raises:
            PyWATSError: If the request fails or server returns an error
            
        Example:
            >>> new_user = ScimUser(
            ...     user_name="jane.doe@example.com",
            ...     display_name="Jane Doe",
            ...     active=True
            ... )
            >>> created = repo.create_user(new_user)
            >>> print(f"User created with ID: {created.id}")
        """
        response = self._http_client.post(
            "/api/SCIM/v2/Users",
            json=user.model_dump(by_alias=True, exclude_none=True)
        )
        data = self._error_handler.handle_response(
            response, operation="create_user", allow_empty=False
        )
        if data:
            logger.info(f"Created SCIM user: {user.user_name}")
            return ScimUser.model_validate(data)
        return None

    def get_user(self, user_id: str) -> Optional[ScimUser]:
        """
        Get a SCIM user by ID.
        
        Retrieves user details by their unique identifier.
        
        Maps to: GET /api/SCIM/v2/Users/{id}
        
        Args:
            user_id: The unique user identifier (GUID)
            
        Returns:
            ScimUser details, or None if not found
            
        Raises:
            PyWATSError: If the request fails
            
        Example:
            >>> user = repo.get_user("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
            >>> if user:
            ...     print(f"User: {user.display_name}")
        """
        response = self._http_client.get(f"/api/SCIM/v2/Users/{user_id}")
        data = self._error_handler.handle_response(
            response, operation="get_user", allow_empty=True
        )
        if data:
            return ScimUser.model_validate(data)
        return None

    def delete_user(self, user_id: str) -> None:
        """
        Delete a SCIM user by ID.
        
        Removes a user from the WATS system.
        
        Maps to: DELETE /api/SCIM/v2/Users/{id}
        
        Args:
            user_id: The unique user identifier (GUID)
            
        Raises:
            PyWATSError: If the request fails or user not found
            
        Example:
            >>> repo.delete_user("a1b2c3d4-e5f6-7890-abcd-ef1234567890")
            >>> print("User deleted")
        """
        response = self._http_client.delete(f"/api/SCIM/v2/Users/{user_id}")
        self._error_handler.handle_response(
            response, operation="delete_user", allow_empty=True
        )
        logger.info(f"Deleted SCIM user: {user_id}")

    def update_user(self, user_id: str, patch_request: ScimPatchRequest) -> Optional[ScimUser]:
        """
        Update a SCIM user using SCIM patch operations.
        
        Updates user attributes using the SCIM PatchOp format.
        Only "replace" operations are supported.
        
        Maps to: PATCH /api/SCIM/v2/Users/{id}
        
        Args:
            user_id: The unique user identifier (GUID)
            patch_request: SCIM patch request with operations to apply
            
        Returns:
            Updated ScimUser details, or None on failure
            
        Raises:
            PyWATSError: If the request fails or user not found
            
        Example:
            >>> patch = ScimPatchRequest(
            ...     operations=[
            ...         ScimPatchOperation(op="replace", path="active", value=False)
            ...     ]
            ... )
            >>> updated = repo.update_user("user-id", patch)
            >>> print(f"User active: {updated.active}")
        """
        response = self._http_client.patch(
            f"/api/SCIM/v2/Users/{user_id}",
            json=patch_request.model_dump(by_alias=True, exclude_none=True)
        )
        data = self._error_handler.handle_response(
            response, operation="update_user", allow_empty=False
        )
        if data:
            logger.info(f"Updated SCIM user: {user_id}")
            return ScimUser.model_validate(data)
        return None

    def get_user_by_username(self, username: str) -> Optional[ScimUser]:
        """
        Get a SCIM user by username.
        
        Retrieves user details by their username (typically email).
        
        Maps to: GET /api/SCIM/v2/Users/userName={userName}
        
        Args:
            username: The username to search for
            
        Returns:
            ScimUser details, or None if not found
            
        Raises:
            PyWATSError: If the request fails
            
        Example:
            >>> user = repo.get_user_by_username("jane.doe@example.com")
            >>> if user:
            ...     print(f"User ID: {user.id}")
        """
        response = self._http_client.get(f"/api/SCIM/v2/Users/userName={username}")
        data = self._error_handler.handle_response(
            response, operation="get_user_by_username", allow_empty=True
        )
        if data:
            return ScimUser.model_validate(data)
        return None
