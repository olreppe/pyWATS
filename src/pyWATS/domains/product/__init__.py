"""Product domain.

Provides models, services, and repository for product management.
"""
from .models import Product, ProductRevision, ProductView, ProductGroup
from .enums import ProductState
from .service import ProductService
from .repository import ProductRepository

__all__ = [
    # Models
    "Product",
    "ProductRevision",
    "ProductView",
    "ProductGroup",
    # Enums
    "ProductState",
    # Service & Repository
    "ProductService",
    "ProductRepository",
]
