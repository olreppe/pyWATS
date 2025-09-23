"""
Endpoints package initialization.

Imports all endpoint modules for easy access.
"""

# Import all endpoint modules
from . import app
from . import asset
from . import auth
from . import internal
from . import product
from . import production
from . import report

__all__ = [
    "app",
    "asset", 
    "auth",
    "internal",
    "product",
    "production",
    "report",
]