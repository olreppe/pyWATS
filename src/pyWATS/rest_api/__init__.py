"""
REST API package initialization.

Provides the main REST API interface for pyWATS.
"""

from .client import WATSClient, get_default_client, set_default_client
from .exceptions import (
    WATSAPIException, AuthenticationError, AuthorizationError, 
    NotFoundError, ValidationError, ServerError, RateLimitError, NetworkError
)
from . import models
from . import endpoints

__all__ = [
    # Client
    "WATSClient", "get_default_client", "set_default_client",
    
    # Exceptions
    "WATSAPIException", "AuthenticationError", "AuthorizationError",
    "NotFoundError", "ValidationError", "ServerError", "RateLimitError", "NetworkError",
    
    # Models and endpoints
    "models", "endpoints",
]