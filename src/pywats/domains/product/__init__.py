"""Product domain.

Provides models, services, and repository for product management.
"""
from .models import (
    Product, 
    ProductRevision, 
    ProductView, 
    ProductGroup,
    ProductCategory,
    ProductRevisionRelation,
    BomItem,
)
from .enums import ProductState

# Async implementations (primary API)
from .async_repository import AsyncProductRepository
from .async_service import AsyncProductService, AsyncBoxBuildTemplate, BoxBuildTemplate

__all__ = [
    # Models
    "Product",
    "ProductRevision",
    "ProductView",
    "ProductGroup",
    "ProductCategory",
    "ProductRevisionRelation",
    "BomItem",
    # Box Build
    "AsyncBoxBuildTemplate",
    "BoxBuildTemplate",
    # Enums
    "ProductState",
    # Async implementations
    "AsyncProductRepository",
    "AsyncProductService",
]
