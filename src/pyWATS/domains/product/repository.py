"""Product repository - data access layer.

All API interactions for products, revisions, groups, and vendors.
"""
from typing import Optional, List, Dict, Any, Union, Sequence, TYPE_CHECKING, cast

if TYPE_CHECKING:
    from ...core import HttpClient

from .models import Product, ProductRevision, ProductGroup


class ProductRepository:
    """
    Product data access layer.

    Handles all WATS API interactions for products.
    """

    def __init__(self, client: "HttpClient"):
        """
        Initialize with HTTP client.

        Args:
            client: HttpClient for making HTTP requests
        """
        self._http = client

    # =========================================================================
    # Product CRUD
    # =========================================================================

    def get_all(self) -> List[Product]:
        """
        Get all products.

        GET /api/Product/Query

        Returns:
            List of Product objects
        """
        response = self._http.get("/api/Product/Query")
        if response.is_success and response.data:
            return [Product.model_validate(item) for item in response.data]
        return []

    def get_by_part_number(self, part_number: str) -> Optional[Product]:
        """
        Get a product by part number.

        GET /api/Product/{partNumber}

        Args:
            part_number: The product part number

        Returns:
            Product object or None if not found
        """
        response = self._http.get(f"/api/Product/{part_number}")
        if response.is_success and response.data:
            return Product.model_validate(response.data)
        return None

    def save(
        self, product: Union[Product, Dict[str, Any]]
    ) -> Optional[Product]:
        """
        Create or update a product.

        PUT /api/Product

        To create: Leave productId empty
        To update: Include the productId

        Args:
            product: Product object or data dictionary

        Returns:
            Created/updated Product object
        """
        if isinstance(product, Product):
            data = product.model_dump(by_alias=True, exclude_none=True)
        else:
            data = product
        response = self._http.put("/api/Product", data=data)
        if response.is_success and response.data:
            return Product.model_validate(response.data)
        return None

    def save_bulk(
        self, products: Sequence[Union[Product, Dict[str, Any]]]
    ) -> List[Product]:
        """
        Bulk create or update products.

        PUT /api/Product/Products

        Args:
            products: List of Product objects or data dictionaries

        Returns:
            List of created/updated Product objects
        """
        data = [
            p.model_dump(by_alias=True, exclude_none=True)
            if isinstance(p, Product) else p
            for p in products
        ]
        response = self._http.put("/api/Product/Products", data=data)
        if response.is_success and response.data:
            return [Product.model_validate(item) for item in response.data]
        return []

    # =========================================================================
    # Revision Operations
    # =========================================================================

    def get_revision(
        self, part_number: str, revision: str
    ) -> Optional[ProductRevision]:
        """
        Get a specific product revision.

        GET /api/Product/{partNumber}/{revision}

        Args:
            part_number: The product part number
            revision: The revision identifier

        Returns:
            ProductRevision object or None if not found
        """
        response = self._http.get(f"/api/Product/{part_number}/{revision}")
        if response.is_success and response.data:
            return ProductRevision.model_validate(response.data)
        return None

    def save_revision(
        self, revision: Union[ProductRevision, Dict[str, Any]]
    ) -> Optional[ProductRevision]:
        """
        Create or update a product revision.

        PUT /api/Product/Revision

        To create: Leave productRevisionId empty
        To update: Include the productRevisionId

        Args:
            revision: ProductRevision object or data dictionary

        Returns:
            Created/updated ProductRevision object
        """
        if isinstance(revision, ProductRevision):
            data = revision.model_dump(mode="json", by_alias=True, exclude_none=True)
        else:
            data = revision
        response = self._http.put("/api/Product/Revision", data=data)
        if response.is_success and response.data:
            return ProductRevision.model_validate(response.data)
        return None

    def save_revisions_bulk(
        self, revisions: Sequence[Union[ProductRevision, Dict[str, Any]]]
    ) -> List[ProductRevision]:
        """
        Bulk create or update product revisions.

        PUT /api/Product/Revisions

        Args:
            revisions: List of ProductRevision objects or data dictionaries

        Returns:
            List of created/updated ProductRevision objects
        """
        data = [
            r.model_dump(by_alias=True, exclude_none=True)
            if isinstance(r, ProductRevision) else r
            for r in revisions
        ]
        response = self._http.put("/api/Product/Revisions", data=data)
        if response.is_success and response.data:
            return [ProductRevision.model_validate(item) for item in response.data]
        return []

    # =========================================================================
    # Bill of Materials
    # =========================================================================

    def update_bom(self, bom_data: Dict[str, Any]) -> bool:
        """
        Update product BOM (Bill of Materials).

        PUT /api/Product/BOM

        Args:
            bom_data: BOM data dictionary

        Returns:
            True if successful
        """
        response = self._http.put("/api/Product/BOM", data=bom_data)
        return response.is_success

    # =========================================================================
    # Product Groups
    # =========================================================================

    def get_groups(
        self,
        filter_str: Optional[str] = None,
        orderby: Optional[str] = None,
        top: Optional[int] = None,
        skip: Optional[int] = None
    ) -> List[ProductGroup]:
        """
        Get product groups with OData filtering.

        POST /api/Product/GroupFilter

        Args:
            filter_str: OData filter string
            orderby: Order by clause
            top: Number of records to return
            skip: Number of records to skip

        Returns:
            List of ProductGroup objects
        """
        params: Dict[str, Any] = {}
        if filter_str:
            params["$filter"] = filter_str
        if orderby:
            params["$orderby"] = orderby
        if top:
            params["$top"] = top
        if skip:
            params["$skip"] = skip

        response = self._http.post("/api/Product/GroupFilter", params=params)
        if response.is_success and response.data:
            return [ProductGroup.model_validate(item) for item in response.data]
        return []

    def get_groups_for_product(
        self, part_number: str, revision: str
    ) -> List[ProductGroup]:
        """
        Get product groups for a specific product.

        GET /api/Product/Groups/{partNumber}/{revision}

        Args:
            part_number: The product part number
            revision: The revision identifier

        Returns:
            List of ProductGroup objects
        """
        response = self._http.get(
            f"/api/Product/Groups/{part_number}/{revision}"
        )
        if response.is_success and response.data:
            return [ProductGroup.model_validate(item) for item in response.data]
        return []

    # =========================================================================
    # Vendors
    # =========================================================================

    def get_vendors(self) -> List[Dict[str, Any]]:
        """
        Get all vendors.

        GET /api/Product/Vendors

        Returns:
            List of vendor dictionaries
        """
        response = self._http.get("/api/Product/Vendors")
        if response.is_success and response.data:
            return cast(List[Dict[str, Any]], response.data)
        return []

    def save_vendor(
        self, vendor_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create or update a vendor.

        PUT /api/Product/Vendors

        Args:
            vendor_data: Vendor data dictionary

        Returns:
            Created/updated vendor data
        """
        response = self._http.put("/api/Product/Vendors", data=vendor_data)
        if response.is_success and response.data:
            return cast(Dict[str, Any], response.data)
        return None

    def delete_vendor(self, vendor_id: str) -> bool:
        """
        Delete a vendor.

        DELETE /api/Product/Vendors/{vendorId}

        Args:
            vendor_id: The vendor ID

        Returns:
            True if successful
        """
        response = self._http.delete(f"/api/Product/Vendors/{vendor_id}")
        return response.is_success
