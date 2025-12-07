"""Product Module for pyWATS

Provides high-level operations for managing products and product revisions.
"""
from typing import Any, Dict, List, Optional
from uuid import UUID

from ..models import Product, ProductRevision, ProductView, ProductState
from ..rest_api import ProductApi


class ProductModule:
    """
    Product management module.
    
    Provides operations for:
    - Getting products and product revisions
    - Creating products and revisions
    - Updating products and revisions
    - Managing Bill of Materials (BOM)
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Get all products
        products = api.product.get_products()
        
        # Get a specific product
        product = api.product.get_product("PART-001")
        
        # Get a specific revision
        revision = api.product.get_product_revision("PART-001", "A")
        
        # Create a new product
        new_product = api.product.create_product(
            part_number="PART-002",
            name="New Product"
        )
    """
    
    def __init__(self, api: ProductApi):
        """
        Initialize ProductModule with REST API client.
        
        Args:
            api: ProductApi instance for making HTTP requests
        """
        self._api = api
    
    # -------------------------------------------------------------------------
    # Get Operations
    # -------------------------------------------------------------------------
    
    def get_products(self) -> List[ProductView]:
        """
        Get all products in the system.
        
        Returns:
            List of ProductView objects with basic product information
        """
        # REST API now returns List[Product] directly
        products = self._api.get_products()
        # Convert Product to ProductView for backward compatibility
        return [
            ProductView(
                part_number=p.part_number,
                name=p.name,
                non_serial=p.non_serial,
                state=p.state
            ) for p in products
        ]
    
    def get_product(self, part_number: str) -> Optional[Product]:
        """
        Get a product by part number.
        
        Args:
            part_number: The product part number
            
        Returns:
            Product object if found, None otherwise
        """
        # REST API now returns Optional[Product] directly
        return self._api.get_product(part_number)
    
    def get_product_revision(self, part_number: str, revision: str) -> Optional[ProductRevision]:
        """
        Get a specific product revision.
        
        Args:
            part_number: The product part number
            revision: The revision identifier
            
        Returns:
            ProductRevision object if found, None otherwise
        """
        # REST API now returns Optional[ProductRevision] directly
        return self._api.get_product_revision(part_number, revision)
    
    # -------------------------------------------------------------------------
    # Create/Update Operations
    # -------------------------------------------------------------------------
    
    def create_product(
        self,
        part_number: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        non_serial: bool = False,
        state: ProductState = ProductState.ACTIVE,
        xml_data: Optional[str] = None,
        product_category_id: Optional[UUID] = None
    ) -> Optional[Product]:
        """
        Create a new product.
        
        Note: Leave product_id empty for new products.
        
        Args:
            part_number: Part number for the new product (required)
            name: Product name
            description: Product description
            non_serial: True if product doesn't have serial numbers
            state: Product state (default: Active)
            xml_data: Custom XML data
            product_category_id: Product category ID
            
        Returns:
            Created Product object, or None on failure
        """
        product = Product(
            part_number=part_number,
            name=name,
            description=description,
            non_serial=non_serial,
            state=state,
            xml_data=xml_data,
            product_category_id=product_category_id
        )
        # REST API accepts Product and returns Optional[Product]
        return self._api.create_or_update_product(product)
    
    def update_product(self, product: Product) -> Optional[Product]:
        """
        Update an existing product.
        
        Args:
            product: Product object with updated values.
                     Must have product_id set to update.
            
        Returns:
            Updated Product object, or None on failure
        """
        if not product.product_id:
            raise ValueError("Product must have product_id set for update")
        
        # REST API accepts Product and returns Optional[Product]
        return self._api.create_or_update_product(product)
    
    def create_revision(
        self,
        part_number: str,
        revision: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        state: ProductState = ProductState.ACTIVE,
        xml_data: Optional[str] = None
    ) -> Optional[ProductRevision]:
        """
        Create a new revision for an existing product.
        
        Note: Leave product_revision_id empty for new revisions.
        
        Args:
            part_number: Part number of the parent product
            revision: Revision identifier (e.g., "A", "1.0")
            name: Human readable revision name
            description: Revision description
            state: Revision state (default: Active)
            xml_data: Custom XML data
            
        Returns:
            Created ProductRevision object, or None on failure
        """
        rev = ProductRevision(
            revision=revision,
            part_number=part_number,
            name=name,
            description=description,
            state=state,
            xml_data=xml_data
        )
        # REST API accepts ProductRevision and returns Optional[ProductRevision]
        return self._api.create_or_update_product_revision(rev)
    
    def update_revision(self, revision: ProductRevision) -> Optional[ProductRevision]:
        """
        Update an existing product revision.
        
        Args:
            revision: ProductRevision object with updated values.
                      Must have product_revision_id set to update.
            
        Returns:
            Updated ProductRevision object, or None on failure
        """
        if not revision.product_revision_id:
            raise ValueError("Revision must have product_revision_id set for update")
        
        # REST API accepts ProductRevision and returns Optional[ProductRevision]
        return self._api.create_or_update_product_revision(revision)
    
    def bulk_create_or_update_products(self, products: List[Product]) -> List[Product]:
        """
        Bulk create or update products.
        
        For ERP integration - add or update products (part numbers).
        
        Args:
            products: List of Product objects
            
        Returns:
            List of created/updated Product objects
        """
        # REST API now returns List[Product] directly
        return self._api.bulk_create_or_update_products(products)  # type: ignore[arg-type]
    
    def bulk_create_or_update_revisions(self, revisions: List[ProductRevision]) -> List[ProductRevision]:
        """
        Bulk create or update product revisions.
        
        For ERP integration - add or update revisions of products.
        
        Args:
            revisions: List of ProductRevision objects
            
        Returns:
            List of created/updated ProductRevision objects
        """
        # REST API now returns List[ProductRevision] directly
        return self._api.bulk_create_or_update_revisions(revisions)  # type: ignore[arg-type]
    
    # -------------------------------------------------------------------------
    # BOM Operations
    # -------------------------------------------------------------------------
    
    def update_bom(self, bom_data: Dict[str, Any]) -> bool:
        """
        Insert or update a BOM using WSBF (WATS Standard BOM Format).
        
        Args:
            bom_data: BOM data dictionary in WSBF format
            
        Returns:
            True if successful
        """
        # REST API now returns bool directly
        return self._api.update_bom(bom_data)
    
    # -------------------------------------------------------------------------
    # Product Groups
    # -------------------------------------------------------------------------
    
    def get_product_groups_by_product(self, part_number: str, revision: str) -> List[Dict[str, Any]]:
        """
        Get product groups for a specific product.
        
        Args:
            part_number: Product part number
            revision: Revision identifier
            
        Returns:
            List of product groups
        """
        # REST API now returns List[ProductGroup] directly  
        groups = self._api.get_product_groups_by_product(part_number, revision)
        # Convert to dicts for backward compatibility
        return [g.model_dump(by_alias=True, exclude_none=True) for g in groups]
    
    # -------------------------------------------------------------------------
    # Vendor Operations
    # -------------------------------------------------------------------------
    
    def get_vendors(self) -> List[Dict[str, Any]]:
        """
        Get all vendors.
        
        Returns:
            List of vendor data dictionaries
        """
        # REST API now returns List[Dict] directly
        return self._api.get_vendors()
    
    def create_or_update_vendor(self, vendor_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create or update a vendor.
        
        Args:
            vendor_data: Vendor data dictionary
            
        Returns:
            Created/updated vendor data, or None on failure
        """
        # REST API now returns Optional[Dict] directly
        return self._api.create_or_update_vendor(vendor_data)
    
    def delete_vendor(self, vendor_id: str) -> bool:
        """
        Delete a vendor.
        
        Args:
            vendor_id: The vendor ID to delete
            
        Returns:
            True if deletion was successful
        """
        # REST API now returns bool directly
        return self._api.delete_vendor(vendor_id)
    
    # -------------------------------------------------------------------------
    # Helper Methods
    # -------------------------------------------------------------------------
    
    def exists(self, part_number: str) -> bool:
        """
        Check if a product exists.
        
        Args:
            part_number: Product part number
            
        Returns:
            True if product exists, False otherwise
        """
        try:
            return self.get_product(part_number) is not None
        except Exception:
            return False
    
    def get_active_products(self) -> List[ProductView]:
        """
        Get all active products.
        
        Returns:
            List of active ProductView objects
        """
        products = self.get_products()
        return [p for p in products if p.state == ProductState.ACTIVE]
