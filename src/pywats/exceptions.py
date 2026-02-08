"""Custom exceptions for pyWATS.

⚠️ DEPRECATED: This module is deprecated as of v0.5.1 and will be removed in v0.6.0.

All exception classes have been moved to pywats.core.exceptions with enhanced functionality.
This module now re-exports from pywats.core.exceptions for backward compatibility.

Migration Guide:
    # Before (deprecated):
    from pywats.exceptions import PyWATSError, NotFoundError
    
    # After (recommended):
    from pywats.core.exceptions import PyWATSError, NotFoundError

The new pywats.core.exceptions module provides:
- Consistent error handling across all domains
- ErrorMode.STRICT and ErrorMode.LENIENT support
- Better context and troubleshooting information
- Cleaner exception hierarchy

See MIGRATION.md for complete migration guide.
"""
import warnings

# Issue deprecation warning when this module is imported
warnings.warn(
    "pywats.exceptions is deprecated as of v0.5.1 and will be removed in v0.6.0. "
    "Please update imports to use pywats.core.exceptions instead. "
    "See MIGRATION.md for migration guide.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export everything from pywats.core.exceptions for backward compatibility
from pywats.core.exceptions import *  # noqa: F401, F403

# Explicit re-exports for IDE support and clarity
from pywats.core.exceptions import (  # noqa: F401
    PyWATSError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    AuthorizationError,
    ServerError,
    ConnectionError,
    TimeoutError,
    WatsApiError,
    ErrorMode,
    ConflictError,
    EmptyResponseError,
)

