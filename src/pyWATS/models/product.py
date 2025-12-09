"""
Product models for pyWATS

Uses Pydantic 2 for validation and serialization.
Uses validation_alias for JSON deserialization from API responses while
keeping Python-style snake_case field names for __init__ and attribute access.
"""
from typing import Optional, List
from uuid import UUID
from enum import IntEnum
from pydantic import Field, AliasChoices

from .common import PyWATSModel, Setting


class ProductState(IntEnum):
    """Product/Revision state"""
    INACTIVE = 0
    ACTIVE = 1


class ProductRevision(PyWATSModel):
    """
    Represents a product revision in WATS.
    
    Attributes:
        product_revision_id: Unique identifier for this revision
        product_id: ID of the product this revision belongs to
        revision: Revision name/number
        name: Human readable name
        description: Revision description
        state: Active(1) or Inactive(0)
        xml_data: XML document with custom key-value pairs
        part_number: Part number (read-only, from parent product)
        tags: JSON formatted xmlData (read-only)
    """
    revision: str = Field(...)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    state: ProductState = Field(default=ProductState.ACTIVE)
    product_revision_id: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices(
            "productRevisionId", "product_revision_id"
        ),
        serialization_alias="productRevisionId"
    )
    product_id: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices("productId", "product_id"),
        serialization_alias="productId"
    )
    xml_data: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("xmlData", "xml_data"),
        serialization_alias="xmlData"
    )
    part_number: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("partNumber", "part_number"),
        serialization_alias="partNumber"
    )
    tags: List[Setting] = Field(default_factory=list)


class Product(PyWATSModel):
    """
    Represents a product in WATS.
    
    Attributes:
        product_id: Unique product identifier
        part_number: Part number
        name: Product name
        description: Product description
        non_serial: Flag indicating if product can have units
        state: Active(1) or Inactive(0)
        xml_data: XML document with custom key-value pairs
        product_category_id: ID of category this product belongs to
        product_category_name: Name of product category (read-only)
        revisions: List of product revisions
        tags: JSON formatted xmlData (read-only)
    """
    part_number: str = Field(
        ...,
        validation_alias=AliasChoices("partNumber", "part_number"),
        serialization_alias="partNumber"
    )
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    non_serial: bool = Field(
        default=False,
        validation_alias=AliasChoices("nonSerial", "non_serial"),
        serialization_alias="nonSerial"
    )
    state: ProductState = Field(default=ProductState.ACTIVE)
    product_id: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices("productId", "product_id"),
        serialization_alias="productId"
    )
    xml_data: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("xmlData", "xml_data"),
        serialization_alias="xmlData"
    )
    product_category_id: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices(
            "productCategoryId", "product_category_id"
        ),
        serialization_alias="productCategoryId"
    )
    product_category_name: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices(
            "productCategoryName", "product_category_name"
        ),
        serialization_alias="productCategoryName"
    )
    revisions: List[ProductRevision] = Field(default_factory=list)
    tags: List[Setting] = Field(default_factory=list)

    def get_revision(self, revision: str) -> Optional[ProductRevision]:
        """Get a specific revision by revision name"""
        for rev in self.revisions:
            if rev.revision == revision:
                return rev
        return None


class ProductView(PyWATSModel):
    """
    Simplified product view (used in list views).
    
    Attributes:
        part_number: Part number
        name: Product name
        category: Category name
        non_serial: Flag indicating if product can have units
        state: Active(1) or Inactive(0)
    """
    part_number: str = Field(
        ...,
        validation_alias=AliasChoices("partNumber", "part_number"),
        serialization_alias="partNumber"
    )
    name: Optional[str] = Field(default=None)
    category: Optional[str] = Field(default=None)
    non_serial: bool = Field(
        default=False,
        validation_alias=AliasChoices("nonSerial", "non_serial"),
        serialization_alias="nonSerial"
    )
    state: ProductState = Field(default=ProductState.ACTIVE)
