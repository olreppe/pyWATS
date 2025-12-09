"""Core infrastructure for pyWATS.

Contains HTTP client, authentication, and base exceptions.
"""
from .client import HttpClient
from .exceptions import (
    PyWATSError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    ServerError,
    ConnectionError,
    TimeoutError,
)

__all__ = [
    "HttpClient",
    "PyWATSError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "ServerError",
    "ConnectionError",
    "TimeoutError",
]
