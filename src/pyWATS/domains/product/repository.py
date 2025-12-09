"""Product repository - data access layer.

All API interactions for products, revisions, groups, and vendors.
"""
from typing import Optional, List, Dict, Any, Union, Sequence, TYPE_CHECKING, cast
import xml.etree.ElementTree as ET

if TYPE_CHECKING:
    from ...core import HttpClient

from .models import Product, ProductRevision, ProductGroup, BomItem


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
            # mode='json' ensures UUIDs are serialized as strings
            data = product.model_dump(by_alias=True, exclude_none=True, mode='json')
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
            p.model_dump(by_alias=True, exclude_none=True, mode='json')
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

        GET /api/Product?partNumber={partNumber}&revision={revision}

        Note: Using query parameters instead of path parameters because
        revisions containing dots (e.g., "1.0") are misinterpreted as
        file extensions in the path-based URL.

        Args:
            part_number: The product part number
            revision: The revision identifier

        Returns:
            ProductRevision object or None if not found
        """
        # Use query parameters to handle revisions with dots (e.g., "1.0")
        response = self._http.get(
            "/api/Product", 
            params={"partNumber": part_number, "revision": revision}
        )
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
            r.model_dump(by_alias=True, exclude_none=True, mode='json')
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

    def update_bom(
        self,
        part_number: str,
        revision: str,
        bom_items: List[BomItem],
        description: Optional[str] = None
    ) -> bool:
        """
        Update product BOM (Bill of Materials) using WSBF XML format.

        PUT /api/Product/BOM
        
        The public API uses WSBF (WATS Standard BOM Format) XML.
        Example:
            <BOM xmlns="http://wats.virinco.com/schemas/WATS/wsbf" 
                 Partnumber="100100" Revision="1.0" Desc="Product Description">
                <Component Number="100200" Rev="1.0" Qty="2" Desc="Description" Ref="R1;R2"/>
            </BOM>

        Args:
            part_number: Product part number
            revision: Product revision
            bom_items: List of BomItem objects
            description: Optional product description

        Returns:
            True if successful
        """
        xml_content = self._generate_wsbf_xml(part_number, revision, bom_items, description)
        
        # Send as XML with proper content type
        response = self._http.put(
            "/api/Product/BOM",
            data=xml_content,
            headers={"Content-Type": "application/xml"}
        )
        return response.is_success
    
    def _generate_wsbf_xml(
        self,
        part_number: str,
        revision: str,
        bom_items: List[BomItem],
        description: Optional[str] = None
    ) -> str:
        """
        Generate WSBF (WATS Standard BOM Format) XML.
        
        Args:
            part_number: Product part number
            revision: Product revision
            bom_items: List of BomItem objects
            description: Optional product description
            
        Returns:
            WSBF XML string
        """
        # Create root BOM element with namespace
        nsmap = {"xmlns": "http://wats.virinco.com/schemas/WATS/wsbf"}
        root = ET.Element("BOM", attrib={
            "xmlns": "http://wats.virinco.com/schemas/WATS/wsbf",
            "Partnumber": part_number,
            "Revision": revision
        })
        
        if description:
            root.set("Desc", description)
        
        # Add Component elements for each BOM item
        for item in bom_items:
            comp_attrib: Dict[str, str] = {}
            
            # Required: Number (part number)
            if item.part_number:
                comp_attrib["Number"] = item.part_number
            
            # Optional attributes
            if item.component_ref:
                comp_attrib["Ref"] = item.component_ref
            
            if item.quantity:
                comp_attrib["Qty"] = str(item.quantity)
            
            if item.description:
                comp_attrib["Desc"] = item.description
            
            # Add revision if we can get it (from vendor_pn as fallback)
            # The WSBF format uses "Rev" for component revision
            if item.manufacturer_pn:
                comp_attrib["Rev"] = item.manufacturer_pn
            
            ET.SubElement(root, "Component", attrib=comp_attrib)
        
        # Generate XML string
        return ET.tostring(root, encoding="unicode")

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
