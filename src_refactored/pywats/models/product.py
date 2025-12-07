"""
Product models for pyWATS
"""
from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID
from enum import IntEnum

from .common import Setting


class ProductState(IntEnum):
    """Product/Revision state"""
    INACTIVE = 0
    ACTIVE = 1


@dataclass
class ProductRevision:
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
    revision: str
    name: Optional[str] = None
    description: Optional[str] = None
    state: ProductState = ProductState.ACTIVE
    product_revision_id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    xml_data: Optional[str] = None
    part_number: Optional[str] = None
    tags: List[Setting] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "ProductRevision":
        """Create ProductRevision from API response dictionary"""
        return cls(
            product_revision_id=UUID(data["productRevisionId"]) if data.get("productRevisionId") else None,
            product_id=UUID(data["productId"]) if data.get("productId") else None,
            revision=data.get("revision", ""),
            name=data.get("name"),
            description=data.get("description"),
            state=ProductState(data.get("state", 1)),
            xml_data=data.get("xmlData"),
            part_number=data.get("PartNumber") or data.get("partNumber"),
            tags=[Setting.from_dict(t) for t in data.get("tags", [])]
        )

    def to_dict(self, include_read_only: bool = False) -> dict:
        """
        Convert to dictionary for API requests.
        
        Args:
            include_read_only: If True, include read-only fields (for display purposes)
        """
        result = {
            "revision": self.revision,
            "state": self.state.value
        }
        
        if self.product_revision_id:
            result["productRevisionId"] = str(self.product_revision_id)
        if self.product_id:
            result["productId"] = str(self.product_id)
        if self.name is not None:
            result["name"] = self.name
        if self.description is not None:
            result["description"] = self.description
        if self.xml_data is not None:
            result["xmlData"] = self.xml_data
            
        if include_read_only:
            if self.part_number:
                result["PartNumber"] = self.part_number
            if self.tags:
                result["tags"] = [t.to_dict() for t in self.tags]
                
        return result


@dataclass
class Product:
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
    part_number: str
    name: Optional[str] = None
    description: Optional[str] = None
    non_serial: bool = False
    state: ProductState = ProductState.ACTIVE
    product_id: Optional[UUID] = None
    xml_data: Optional[str] = None
    product_category_id: Optional[UUID] = None
    product_category_name: Optional[str] = None
    revisions: List[ProductRevision] = field(default_factory=list)
    tags: List[Setting] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Create Product from API response dictionary"""
        return cls(
            product_id=UUID(data["productId"]) if data.get("productId") else None,
            part_number=data.get("partNumber", ""),
            name=data.get("name"),
            description=data.get("description"),
            non_serial=data.get("nonSerial", False),
            state=ProductState(data.get("state", 1)),
            xml_data=data.get("xmlData"),
            product_category_id=UUID(data["productCategoryId"]) if data.get("productCategoryId") else None,
            product_category_name=data.get("productCategoryName"),
            revisions=[ProductRevision.from_dict(r) for r in data.get("revisions", [])],
            tags=[Setting.from_dict(t) for t in data.get("tags", [])]
        )

    def to_dict(self, include_read_only: bool = False) -> dict:
        """
        Convert to dictionary for API requests.
        
        Args:
            include_read_only: If True, include read-only fields (for display purposes)
        """
        result = {
            "partNumber": self.part_number,
            "nonSerial": self.non_serial,
            "state": self.state.value
        }
        
        if self.product_id:
            result["productId"] = str(self.product_id)
        if self.name is not None:
            result["name"] = self.name
        if self.description is not None:
            result["description"] = self.description
        if self.xml_data is not None:
            result["xmlData"] = self.xml_data
        if self.product_category_id:
            result["productCategoryId"] = str(self.product_category_id)
            
        if include_read_only:
            if self.product_category_name:
                result["productCategoryName"] = self.product_category_name
            if self.revisions:
                result["revisions"] = [r.to_dict(include_read_only=True) for r in self.revisions]
            if self.tags:
                result["tags"] = [t.to_dict() for t in self.tags]
                
        return result

    def get_revision(self, revision: str) -> Optional[ProductRevision]:
        """Get a specific revision by revision name"""
        for rev in self.revisions:
            if rev.revision == revision:
                return rev
        return None


@dataclass
class ProductView:
    """
    Simplified product view (used in list views).
    
    Attributes:
        part_number: Part number
        name: Product name
        category: Category name
        non_serial: Flag indicating if product can have units
        state: Active(1) or Inactive(0)
    """
    part_number: str
    name: Optional[str] = None
    category: Optional[str] = None
    non_serial: bool = False
    state: ProductState = ProductState.ACTIVE

    @classmethod
    def from_dict(cls, data: dict) -> "ProductView":
        """Create ProductView from API response dictionary"""
        return cls(
            part_number=data.get("partNumber", ""),
            name=data.get("name"),
            category=data.get("category"),
            non_serial=data.get("nonSerial", False),
            state=ProductState(data.get("state", 1))
        )

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "partNumber": self.part_number,
            "name": self.name,
            "category": self.category,
            "nonSerial": self.non_serial,
            "state": self.state.value
        }
