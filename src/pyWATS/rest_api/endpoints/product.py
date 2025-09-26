"""
Product Endpoints

Product management endpoints for CRUD operations on products and revisions.
These endpoints are grouped by the "Product" tag in the OpenAPI specification.
"""

from typing import Optional, Dict, Any, List
import httpx

from ..client import get_default_client, WATSClient
from ..exceptions import handle_response_error
from ..models import Product, ProductRevision, ProductView, Vendor


def create_product(
    product: Product,
    client: Optional[WATSClient] = None
) -> Product:
    """
    Add a product or update an existing product.
    
    To add a new product, leave ProductId empty.
    To update an existing product, specify the ProductId.
    
    Args:
        product: Product to add or update
        client: Optional WATS client instance
        
    Returns:
        Created/updated product
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    # Use model_dump with mode='json' for proper UUID serialization
    if hasattr(product, 'model_dump'):
        product_data = product.model_dump(exclude_none=True, by_alias=True, mode='json')
    else:
        product_data = product.dict(exclude_none=True, by_alias=True)
    
    response = client.put(
        "/api/Product",
        json=product_data
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return Product(**data)


def get_product(
    part_number: str,
    client: Optional[WATSClient] = None
) -> Product:
    """
    Get product by part number.
    
    Args:
        part_number: Part number of the product
        client: Optional WATS client instance
        
    Returns:
        Product data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get(f"/api/Product/{part_number}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return Product(**data)


def get_product_revision(
    part_number: str,
    revision: str,
    client: Optional[WATSClient] = None
) -> ProductRevision:
    """
    Get product revision.
    
    Args:
        part_number: Product part number
        revision: Product revision
        client: Optional WATS client instance
        
    Returns:
        Product revision data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get(f"/api/Product/{part_number}/{revision}")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return ProductRevision(**data)


def upload_bom(
    bom_xml: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Insert or update a BOM using WSBF (WATS Standard BOM Format).
    
    Args:
        bom_xml: BOM XML content in WSBF format  
        client: Optional WATS client instance
        
    Returns:
        BOM upload result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.put(
        "/api/Product/BOM",
        data=bom_xml,
        headers={"Content-Type": "application/xml"}
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def add_product_group_filter(
    product_group: str,
    part_number: str,
    revision: Optional[str] = None,
    exclude: Optional[bool] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Add a product group filter to a pre-existing product group.
    
    Args:
        product_group: Pre-existing product group name
        part_number: Part number to add
        revision: Revision to add
        exclude: Indicate if the filter should be an exclude filter
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "productGroup": product_group,
        "partNumber": part_number
    }
    if revision:
        params["revision"] = revision
    if exclude is not None:
        params["exclude"] = exclude
    
    response = client.post("/api/Product/ProductGroupFilter", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_product_groups_by_product(
    part_number: str,
    revision: Optional[str] = None,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Lookup product groups by part number and revision.
    
    Args:
        part_number: Part number
        revision: Revision
        client: Optional WATS client instance
        
    Returns:
        Product groups data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {"partNumber": part_number}
    if revision:
        params["revision"] = revision
    
    response = client.get("/api/Product/ProductGroupsByProduct", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def query_products(
    odata_filter: Optional[str] = None,
    odata_top: Optional[int] = None,
    client: Optional[WATSClient] = None
) -> List[ProductView]:
    """
    Query products with OData support.
    
    Only returns $top=1000 if $filter option is not specified.
    
    Args:
        odata_filter: OData $filter parameter
        odata_top: OData $top parameter
        client: Optional WATS client instance
        
    Returns:
        List of product views
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {}
    if odata_filter:
        params["$filter"] = odata_filter
    if odata_top is not None:
        params["$top"] = odata_top
    
    response = client.get("/api/Product/Query", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return [ProductView(**item) for item in data]


def create_product_revision(
    revision: ProductRevision,
    client: Optional[WATSClient] = None
) -> ProductRevision:
    """
    Add a revision to a product or update an existing revision.
    
    To add a new revision, leave ProductRevisionId empty.
    To update an existing revision, specify the ProductRevisionId.
    
    Args:
        revision: Revision to add or update
        client: Optional WATS client instance
        
    Returns:
        Created/updated revision
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.put(
        "/api/Product/Revision",
        json=revision.dict(exclude_none=True, by_alias=True)
    )
    
    if response.status_code != 200:
        handle_response_error(response)
    
    data = response.json()
    return ProductRevision(**data)


def get_vendors(client: Optional[WATSClient] = None) -> Dict[str, Any]:
    """
    Get all vendors.
    
    Args:
        client: Optional WATS client instance
        
    Returns:
        Vendors data
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    response = client.get("/api/Product/Vendors")
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_vendors(
    vendors: List[Vendor],
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Add vendors that don't already exist.
    
    Args:
        vendors: Vendors to add
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    vendor_data = [vendor.dict(exclude_none=True, by_alias=True) for vendor in vendors]
    
    response = client.put("/api/Product/Vendors", json=vendor_data)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def get_bom(
    part_number: str,
    revision: str,
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Get BOM (Bill of Materials) for a product revision.
    
    Args:
        part_number: Product part number
        revision: Product revision
        client: Optional WATS client instance
        
    Returns:
        BOM data including xmlData field with BOM content
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    params = {
        "partNumber": part_number,
        "revision": revision
    }
    
    response = client.get("/api/Product/BOM", params=params)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def delete_vendors(
    vendors: List[Vendor],
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    Delete vendors.
    
    Args:
        vendors: Vendors to delete
        client: Optional WATS client instance
        
    Returns:
        Deletion result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    vendor_data = [vendor.dict(exclude_none=True, by_alias=True) for vendor in vendors]
    
    response = client.delete("/api/Product/Vendors", json=vendor_data)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_products_bulk(
    products: List[Product],
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    For use with ERP integration. Add or update products (part numbers).
    
    Args:
        products: Products to add
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    product_data = [product.dict(exclude_none=True, by_alias=True) for product in products]
    
    response = client.put("/api/Products", json=product_data)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()


def create_product_revisions_bulk(
    product_revisions: List[ProductRevision],
    client: Optional[WATSClient] = None
) -> Dict[str, Any]:
    """
    For use with ERP integration. Add or update revisions of products.
    
    Args:
        product_revisions: Product revisions to add
        client: Optional WATS client instance
        
    Returns:
        Operation result
        
    Raises:
        WATSAPIException: On API errors
    """
    client = client or get_default_client()
    
    revision_data = [revision.dict(exclude_none=True, by_alias=True) for revision in product_revisions]
    
    response = client.put("/api/Products/Revisions", json=revision_data)
    
    if response.status_code != 200:
        handle_response_error(response)
    
    return response.json()