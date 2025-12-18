"""Domain modules for pyWATS.

Each domain contains:
- models.py: Pure data models (Pydantic)
- enums.py: Domain-specific enumerations
- service.py: Business logic
- repository.py: Data access (API calls)

Some domains also have internal API implementations:
- service_internal.py: Business logic using internal API
- repository_internal.py: Data access using internal API
"""
from . import analytics
from . import app  # Backward compatibility shim
from . import asset
from . import process
from . import product
from . import production
from . import report
from . import rootcause
from . import software

__all__ = [
    "analytics",
    "app",  # Deprecated alias for analytics
    "asset",
    "process",
    "product",
    "production",
    "report",
    "rootcause",
    "software",
]
