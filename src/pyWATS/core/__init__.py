"""Core infrastructure for pyWATS.

Contains HTTP client, authentication, error handling, and base exceptions.
"""
from .client import HttpClient, Response
from .exceptions import (
    # Error handling
    ErrorMode,
    ErrorHandler,
    # Exceptions
    PyWATSError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    ServerError,
    ConflictError,
    EmptyResponseError,
    ConnectionError,
    TimeoutError,
)

__all__ = [
    # Client
    "HttpClient",
    "Response",
    # Error handling
    "ErrorMode",
    "ErrorHandler",
    # Exceptions
    "PyWATSError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "ServerError",
    "ConflictError",
    "EmptyResponseError",
    "ConnectionError",
    "TimeoutError",
]
