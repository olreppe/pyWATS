"""Product Module for pyWATS

Provides high-level operations for managing products and product revisions.
"""
from typing import List, Optional
from uuid import UUID

from ..models import Product, ProductRevision, ProductView, ProductState
from ..rest_api import ProductApi

""" 
API INFO / SWAGGER DOC:

put /api/Product
Add a product or update an existing product. To add a new product, leave ProductId empty. To update an exisiting product, specify the ProductId of the exisiting product.

get /api/Product/{partNumber}/{revision}
Get a product or revision.

put /api/Product/BOM
Inserts or updates a BOM using WSBF (WATS Standard BOM Format) in the request body

post /api/Product/ProductGroupFilter
Add a product group filter to a pre-existing product group.

get /api/Product/ProductGroupsByProduct
Lookup product groups by part number and revision.

get /api/Product/Query
Returns the list of products matching the specified filter.

put /api/Product/Revision
Add a revision to a product or update an existing revision. To add a new revision, leave ProductRevisionId empty. To update an exisiting revision, specify the ProductRevisionId of the exisiting revision.

delete /api/Product/Vendors
Delete vendors.

get /api/Product/Vendors
Get all vendors.

put /api/Product/Vendors
Add vendors that doesn't already exist.

put /api/Products
For use with ERP intergration. Add or update products (part numbers).

put /api/Products/Revisions
For use with ERP intergration. Add or update revisions of products.





"""



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
        response = self._api.get_products()
        if response.is_success and response.data:
            return [ProductView.from_dict(p) for p in response.data]
        return []
    
    def get_product(self, part_number: str) -> Optional[Product]:
        """
        Get a product by part number.
        
        Args:
            part_number: The product part number
            
        Returns:
            Product object if found, None otherwise
        """
        response = self._api.get_product(part_number)
        if response.is_success and response.data:
            return Product.from_dict(response.data)
        return None
    
    def get_product_revision(self, part_number: str, revision: str) -> Optional[ProductRevision]:
        """
        Get a specific product revision.
        
        Args:
            part_number: The product part number
            revision: The revision identifier
            
        Returns:
            ProductRevision object if found, None otherwise
        """
        response = self._api.get_product_revision(part_number, revision)
        if response.is_success and response.data:
            return ProductRevision.from_dict(response.data)
        return None
    
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
        response = self._api.create_or_update_product(product.to_dict())
        if response.is_success and response.data:
            return Product.from_dict(response.data)
        return None
    
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
        
        response = self._api.create_or_update_product(product.to_dict())
        if response.is_success and response.data:
            return Product.from_dict(response.data)
        return None
    
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
        response = self._api.create_or_update_product_revision(rev.to_dict())
        if response.is_success and response.data:
            return ProductRevision.from_dict(response.data)
        return None
    
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
        
        response = self._api.create_or_update_product_revision(revision.to_dict())
        if response.is_success and response.data:
            return ProductRevision.from_dict(response.data)
        return None
    
    def bulk_create_or_update_products(self, products: List[Product]) -> List[Product]:
        """
        Bulk create or update products.
        
        For ERP integration - add or update products (part numbers).
        
        Args:
            products: List of Product objects
            
        Returns:
            List of created/updated Product objects
        """
        data = [p.to_dict() for p in products]
        response = self._api.bulk_create_or_update_products(data)
        if response.is_success and response.data:
            return [Product.from_dict(p) for p in response.data]
        return []
    
    def bulk_create_or_update_revisions(self, revisions: List[ProductRevision]) -> List[ProductRevision]:
        """
        Bulk create or update product revisions.
        
        For ERP integration - add or update revisions of products.
        
        Args:
            revisions: List of ProductRevision objects
            
        Returns:
            List of created/updated ProductRevision objects
        """
        data = [r.to_dict() for r in revisions]
        response = self._api.bulk_create_or_update_revisions(data)
        if response.is_success and response.data:
            return [ProductRevision.from_dict(r) for r in response.data]
        return []
    
    # -------------------------------------------------------------------------
    # BOM Operations
    # -------------------------------------------------------------------------
    
    def update_bom(self, bom_data: dict) -> dict:
        """
        Insert or update a BOM using WSBF (WATS Standard BOM Format).
        
        Args:
            bom_data: BOM data dictionary in WSBF format
            
        Returns:
            Updated BOM data
        """
        response = self._api.update_bom(bom_data)
        return response.data if response.is_success else {}
    
    # -------------------------------------------------------------------------
    # Product Groups
    # -------------------------------------------------------------------------
    
    def get_product_groups_by_product(self, part_number: str, revision: str) -> List[dict]:
        """
        Get product groups for a specific product.
        
        Args:
            part_number: Product part number
            revision: Revision identifier
            
        Returns:
            List of product groups
        """
        response = self._api.get_product_groups_by_product(part_number, revision)
        if response.is_success and response.data:
            return response.data
        return []
    
    # -------------------------------------------------------------------------
    # Vendor Operations
    # -------------------------------------------------------------------------
    
    def get_vendors(self) -> List[dict]:
        """
        Get all vendors.
        
        Returns:
            List of vendor data dictionaries
        """
        response = self._api.get_vendors()
        if response.is_success and response.data:
            return response.data
        return []
    
    def create_or_update_vendor(self, vendor_data: dict) -> dict:
        """
        Create or update a vendor.
        
        Args:
            vendor_data: Vendor data dictionary
            
        Returns:
            Created/updated vendor data
        """
        response = self._api.create_or_update_vendor(vendor_data)
        return response.data if response.is_success else {}
    
    def delete_vendor(self, vendor_id: str) -> bool:
        """
        Delete a vendor.
        
        Args:
            vendor_id: The vendor ID to delete
            
        Returns:
            True if deletion was successful
        """
        response = self._api.delete_vendor(vendor_id)
        return response.is_success
    
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
