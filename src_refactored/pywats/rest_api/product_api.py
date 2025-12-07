"""
Product API Endpoints

Provides all REST API calls for product management.
"""

from typing import Optional, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..http_client import HttpClient, Response


class ProductApi:
    """
    Product API endpoints.
    
    Endpoints for managing products and product revisions in WATS.
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Product endpoints
    # =========================================================================
    
    def get_products(self) -> 'Response':
        """
        Get all products.
        
        GET /api/Product/Query
        
        Returns:
            Response with list of products
        """
        return self._http.get("/api/Product/Query")
    
    def get_product(self, part_number: str) -> 'Response':
        """
        Get a product by part number.
        
        GET /api/Product/{partNumber}
        
        Args:
            part_number: The product part number
            
        Returns:
            Response with product data
        """
        return self._http.get(f"/api/Product/{part_number}")
    
    def get_product_revision(self, part_number: str, revision: str) -> 'Response':
        """
        Get a specific product revision.
        
        GET /api/Product/{partNumber}/{revision}
        
        Args:
            part_number: The product part number
            revision: The revision identifier
            
        Returns:
            Response with product revision data
        """
        return self._http.get(f"/api/Product/{part_number}/{revision}")
    
    def create_or_update_product(self, product_data: Dict[str, Any]) -> 'Response':
        """
        Create a new product or update an existing one.
        
        PUT /api/Product
        
        To create: Leave productId empty
        To update: Include the productId
        
        Args:
            product_data: Product data dictionary
            
        Returns:
            Response with created/updated product
        """
        return self._http.put("/api/Product", data=product_data)
    
    def create_or_update_product_revision(self, revision_data: Dict[str, Any]) -> 'Response':
        """
        Create a new product revision or update an existing one.
        
        PUT /api/Product/Revision
        
        To create: Leave productRevisionId empty
        To update: Include the productRevisionId
        
        Args:
            revision_data: Product revision data dictionary
            
        Returns:
            Response with created/updated revision
        """
        return self._http.put("/api/Product/Revision", data=revision_data)
    
    def bulk_create_or_update_products(self, products: List[Dict[str, Any]]) -> 'Response':
        """
        Bulk create or update products.
        
        PUT /api/Product/Products
        
        Args:
            products: List of product data dictionaries
            
        Returns:
            Response with results
        """
        return self._http.put("/api/Product/Products", data=products)
    
    def bulk_create_or_update_revisions(self, revisions: List[Dict[str, Any]]) -> 'Response':
        """
        Bulk create or update product revisions.
        
        PUT /api/Product/Revisions
        
        Args:
            revisions: List of revision data dictionaries
            
        Returns:
            Response with results
        """
        return self._http.put("/api/Product/Revisions", data=revisions)
    
    # =========================================================================
    # Product BOM (Bill of Materials)
    # =========================================================================
    
    def update_bom(self, bom_data: Dict[str, Any]) -> 'Response':
        """
        Update product BOM (Bill of Materials).
        
        PUT /api/Product/BOM
        
        Args:
            bom_data: BOM data dictionary
            
        Returns:
            Response with result
        """
        return self._http.put("/api/Product/BOM", data=bom_data)
    
    # =========================================================================
    # Product Groups
    # =========================================================================
    
    def get_product_groups(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> 'Response':
        """
        Get product groups with OData filtering.
        
        POST /api/Product/GroupFilter
        
        Args:
            filter_str: OData filter string
            orderby: Order by clause
            top: Number of records to return
            skip: Number of records to skip
            
        Returns:
            Response with product groups
        """
        params = {}
        if filter_str:
            params["$filter"] = filter_str
        if orderby:
            params["$orderby"] = orderby
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip
        
        return self._http.post("/api/Product/GroupFilter", params=params)
    
    def get_product_groups_by_product(self, part_number: str, revision: str) -> 'Response':
        """
        Get product groups for a specific product.
        
        GET /api/Product/Groups/{partNumber}/{revision}
        
        Args:
            part_number: The product part number
            revision: The revision identifier
            
        Returns:
            Response with product groups
        """
        return self._http.get(f"/api/Product/Groups/{part_number}/{revision}")
    
    # =========================================================================
    # Vendors
    # =========================================================================
    
    def get_vendors(self) -> 'Response':
        """
        Get all vendors.
        
        GET /api/Product/Vendors
        
        Returns:
            Response with list of vendors
        """
        return self._http.get("/api/Product/Vendors")
    
    def create_or_update_vendor(self, vendor_data: Dict[str, Any]) -> 'Response':
        """
        Create or update a vendor.
        
        PUT /api/Product/Vendors
        
        Args:
            vendor_data: Vendor data dictionary
            
        Returns:
            Response with vendor data
        """
        return self._http.put("/api/Product/Vendors", data=vendor_data)
    
    def delete_vendor(self, vendor_id: str) -> 'Response':
        """
        Delete a vendor.
        
        DELETE /api/Product/Vendors/{vendorId}
        
        Args:
            vendor_id: The vendor ID
            
        Returns:
            Response with result
        """
        return self._http.delete(f"/api/Product/Vendors/{vendor_id}")
