"""
REST API Exceptions

Custom exceptions for REST API operations.
"""


class WATSAPIException(Exception):
    """Base exception for WATS API errors."""
    
    def __init__(self, message: str, status_code: int | None = None, response: str | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(WATSAPIException):
    """Authentication failed."""
    pass


class AuthorizationError(WATSAPIException):
    """Authorization failed - insufficient permissions."""
    pass


class NotFoundError(WATSAPIException):
    """Resource not found."""
    pass


class ValidationError(WATSAPIException):
    """Request validation failed."""
    pass


class ServerError(WATSAPIException):
    """Server error occurred."""
    pass


class RateLimitError(WATSAPIException):
    """Rate limit exceeded."""
    pass


class NetworkError(WATSAPIException):
    """Network connection error."""
    pass


def handle_response_error(response) -> None:
    """
    Handle HTTP response errors and raise appropriate exceptions.
    
    Args:
        response: HTTP response object
        
    Raises:
        WATSAPIException: Appropriate exception based on status code
    """
    status_code = response.status_code
    
    try:
        error_text = response.text
    except:
        error_text = "Unknown error"
    
    if status_code == 401:
        raise AuthenticationError(
            "Authentication failed", 
            status_code=status_code, 
            response=error_text
        )
    elif status_code == 403:
        raise AuthorizationError(
            "Authorization failed - insufficient permissions", 
            status_code=status_code, 
            response=error_text
        )
    elif status_code == 404:
        raise NotFoundError(
            "Resource not found", 
            status_code=status_code, 
            response=error_text
        )
    elif status_code == 400:
        raise ValidationError(
            "Request validation failed", 
            status_code=status_code, 
            response=error_text
        )
    elif status_code == 429:
        raise RateLimitError(
            "Rate limit exceeded", 
            status_code=status_code, 
            response=error_text
        )
    elif status_code >= 500:
        raise ServerError(
            f"Server error: {status_code}", 
            status_code=status_code, 
            response=error_text
        )
    else:
        raise WATSAPIException(
            f"API error: {status_code}", 
            status_code=status_code, 
            response=error_text
        )