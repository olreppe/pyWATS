"""Core infrastructure for pyWATS.

Contains HTTP client, authentication, error handling, and base exceptions.
"""
from .client import HttpClient, Response
from .config import (
    APISettings,
    APIConfigManager,
    DomainSettings,
    ProductDomainSettings,
    ReportDomainSettings,
    ProductionDomainSettings,
    ProcessDomainSettings,
    SoftwareDomainSettings,
    AssetDomainSettings,
    RootCauseDomainSettings,
    AppDomainSettings,
    get_api_settings,
    get_api_config_manager,
)
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
    # Config
    "APISettings",
    "APIConfigManager",
    "DomainSettings",
    "ProductDomainSettings",
    "ReportDomainSettings",
    "ProductionDomainSettings",
    "ProcessDomainSettings",
    "SoftwareDomainSettings",
    "AssetDomainSettings",
    "RootCauseDomainSettings",
    "AppDomainSettings",
    "get_api_settings",
    "get_api_config_manager",
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
