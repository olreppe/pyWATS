"""Production domain.

Provides models, services, and repository for production unit management.
"""
from .models import (
    Unit, UnitChange, ProductionBatch, SerialNumberType,
    UnitVerification, UnitVerificationGrade
)
from .enums import SerialNumberIdentifier
from .service import ProductionService
from .repository import ProductionRepository

# Rebuild Unit model to resolve forward references to Product/ProductRevision
from ..product.models import Product, ProductRevision
Unit.model_rebuild()

__all__ = [
    # Models
    "Unit",
    "UnitChange",
    "ProductionBatch",
    "SerialNumberType",
    "UnitVerification",
    "UnitVerificationGrade",
    # Enums
    "SerialNumberIdentifier",
    # Service & Repository
    "ProductionService",
    "ProductionRepository",
]
