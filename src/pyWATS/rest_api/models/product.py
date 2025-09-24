"""
Product Models

Models for product management endpoints.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

from .common import PublicWatsFilter


class Setting(BaseModel):
    """Key-value setting model."""
    key: Optional[str] = None
    value: Optional[str] = None
    change: Optional[int] = None


class ProductRevision(BaseModel):
    """Product revision model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    product_revision_id: Optional[UUID] = Field(None, alias="productRevisionId")
    product_id: Optional[UUID] = Field(None, alias="productId")
    revision: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[int] = None
    xml_data: Optional[str] = Field(None, alias="xmlData")
    part_number: Optional[str] = Field(None, alias="PartNumber")
    tags: Optional[List[Setting]] = []


class Product(BaseModel):
    """Product model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    product_id: Optional[UUID] = Field(None, alias="productId")
    non_serial: Optional[bool] = Field(None, alias="nonSerial")
    part_number: Optional[str] = Field(None, alias="partNumber")
    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[int] = None
    xml_data: Optional[str] = Field(None, alias="xmlData")
    product_category_id: Optional[UUID] = Field(None, alias="productCategoryId")
    product_category_name: Optional[str] = Field(None, alias="productCategoryName")
    revisions: Optional[List[ProductRevision]] = []
    tags: Optional[List[Setting]] = []


class ProductView(BaseModel):
    """Product view model for queries."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    part_number: Optional[str] = Field(None, alias="partNumber")
    name: Optional[str] = None
    category: Optional[str] = None
    non_serial: Optional[bool] = Field(None, alias="nonSerial")
    state: Optional[int] = None


class Vendor(BaseModel):
    """Vendor model."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    vendor_name: Optional[str] = Field(None, alias="VendorName")