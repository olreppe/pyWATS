"""
MES Product Models

Consolidated product models for Manufacturing Execution System operations.
Combines comprehensive product management models with MES-specific product types.

Moved from rest_api.models.product and mes.models for better domain separation.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

# Common models - import from rest_api
try:
    from ...rest_api.models.common import PublicWatsFilter
except ImportError:
    # Fallback during development  
    PublicWatsFilter = None


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
    """Product model for comprehensive product management."""
    
    model_config = ConfigDict(populate_by_name=True)
    
    product_id: Optional[UUID] = Field(None, alias="productId")
    non_serial: Optional[bool] = Field(None, alias="nonSerial")
    part_number: str = Field(..., alias="partNumber")
    name: Optional[str] = None
    description: Optional[str] = None
    state: Optional[int] = None
    xml_data: Optional[str] = Field(None, alias="xmlData")
    product_category_id: Optional[UUID] = Field(None, alias="productCategoryId")
    product_category_name: Optional[str] = Field(None, alias="productCategoryName")
    revisions: Optional[List[ProductRevision]] = []
    tags: Optional[List[Setting]] = []
    
    # MES-specific fields
    revision: Optional[str] = None  # Single revision for MES operations
    product_group: Optional[str] = Field(None, alias="productGroup")
    created_date: Optional[datetime] = Field(None, alias="createdDate")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate")
    include_revision: bool = Field(False, alias="includeRevision")
    include_serial_number: bool = Field(False, alias="includeSerialNumber")


class ProductInfo(BaseModel):
    """Product information model for MES operations."""
    part_number: str = Field(..., alias="partNumber")
    revision: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    product_group: Optional[str] = Field(None, alias="productGroup")
    created_date: Optional[datetime] = Field(None, alias="createdDate")
    updated_date: Optional[datetime] = Field(None, alias="updatedDate")
    
    model_config = ConfigDict(populate_by_name=True)


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