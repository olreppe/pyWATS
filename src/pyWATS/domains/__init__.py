"""Domain modules for pyWATS.

Each domain contains:
- models.py: Pure data models (Pydantic)
- enums.py: Domain-specific enumerations
- service.py: Business logic
- repository.py: Data access (API calls)
"""
from . import app
from . import asset
from . import product
from . import production
from . import report
from . import rootcause
from . import software

__all__ = [
    "app",
    "asset",
    "product",
    "production",
    "report",
    "rootcause",
    "software",
]

