"""
Custom exceptions for the WATS API.

This module provides a hierarchy of exceptions specific to WATS operations,
allowing for better error handling and debugging.
"""

from typing import Optional, Dict, Any


class WATSException(Exception):
    """Base exception class for all WATS-related errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class WATSAPIError(WATSException):
    """Exception raised for API-related errors."""
    pass


class WATSConnectionError(WATSException):
    """Exception raised for connection-related errors."""
    pass


class WATSAuthenticationError(WATSException):
    """Exception raised for authentication-related errors."""
    pass


class WATSValidationError(WATSException):
    """Exception raised for data validation errors."""
    pass


class WATSNotFoundError(WATSException):
    """Exception raised when a requested resource is not found."""
    pass


class WATSConfigurationError(WATSException):
    """Exception raised for configuration-related errors."""
    pass


class WATSTimeoutError(WATSException):
    """Exception raised for timeout-related errors."""
    pass