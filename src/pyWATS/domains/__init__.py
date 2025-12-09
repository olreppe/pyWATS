"""Domain modules for pyWATS.

Each domain contains:
- models.py: Pure data models (Pydantic)
- enums.py: Domain-specific enumerations
- service.py: Business logic
- repository.py: Data access (API calls)
"""
from . import asset
from . import product
from . import query
from . import production
from . import report

__all__ = [
    "asset",
    "product",
    "query",
    "production",
    "report",
]

