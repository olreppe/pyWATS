"""Product service - business logic layer.

High-level operations for product management.
"""
from typing import Optional, List, Dict, Any

from .models import Product, ProductRevision, ProductGroup, ProductView
from .enums import ProductState
from .repository import ProductRepository


class ProductService:
    """
    Product business logic.

    Provides high-level operations for managing products, revisions,
    groups, and vendors.
    """

    def __init__(self, repository: ProductRepository):
        """
        Initialize with repository.

        Args:
            repository: ProductRepository for data access
        """
        self._repo = repository

    # =========================================================================
    # Product Operations
    # =========================================================================

    def get_products(self) -> List[ProductView]:
        """
        Get all products as simplified views.

        Returns:
            List of ProductView objects
        """
        products = self._repo.get_all()
        return [
            ProductView(
                part_number=p.part_number,
                name=p.name,
                non_serial=p.non_serial,
                state=p.state
            )
            for p in products
        ]

    def get_products_full(self) -> List[Product]:
        """
        Get all products with full details.

        Returns:
            List of Product objects
        """
        return self._repo.get_all()

    def get_product(self, part_number: str) -> Optional[Product]:
        """
        Get a product by part number.

        Args:
            part_number: The product part number

        Returns:
            Product if found, None otherwise
        """
        return self._repo.get_by_part_number(part_number)

    def create_product(
        self,
        part_number: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        non_serial: bool = False,
        state: ProductState = ProductState.ACTIVE,
        **kwargs: Any
    ) -> Optional[Product]:
        """
        Create a new product.

        Args:
            part_number: Unique part number
            name: Product name
            description: Product description
            non_serial: Whether product can have units
            state: Product state
            **kwargs: Additional product fields

        Returns:
            Created Product object
        """
        product = Product(
            part_number=part_number,
            name=name,
            description=description,
            non_serial=non_serial,
            state=state,
            **kwargs
        )
        return self._repo.save(product)

    def update_product(self, product: Product) -> Optional[Product]:
        """
        Update an existing product.

        Args:
            product: Product object with updated fields

        Returns:
            Updated Product object
        """
        return self._repo.save(product)

    def bulk_save_products(
        self, products: List[Product]
    ) -> List[Product]:
        """
        Bulk create or update products.

        Args:
            products: List of Product objects

        Returns:
            List of saved Product objects
        """
        return self._repo.save_bulk(products)

    def is_active(self, product: Product) -> bool:
        """
        Check if a product is active.

        Args:
            product: Product to check

        Returns:
            True if product is active
        """
        return product.state == ProductState.ACTIVE

    def get_active_products(self) -> List[ProductView]:
        """
        Get all active products.

        Returns:
            List of active ProductView objects
        """
        return [p for p in self.get_products() if p.state == ProductState.ACTIVE]

    # =========================================================================
    # Revision Operations
    # =========================================================================

    def get_revision(
        self, part_number: str, revision: str
    ) -> Optional[ProductRevision]:
        """
        Get a specific product revision.

        Args:
            part_number: The product part number
            revision: The revision identifier

        Returns:
            ProductRevision if found, None otherwise
        """
        return self._repo.get_revision(part_number, revision)

    def get_revisions(self, part_number: str) -> List[ProductRevision]:
        """
        Get all revisions for a product.

        Args:
            part_number: The product part number

        Returns:
            List of ProductRevision objects
        """
        product = self._repo.get_by_part_number(part_number)
        return product.revisions if product else []

    def create_revision(
        self,
        part_number: str,
        revision: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        state: ProductState = ProductState.ACTIVE,
        **kwargs: Any
    ) -> Optional[ProductRevision]:
        """
        Create a new product revision.

        Args:
            part_number: Product part number
            revision: Revision identifier
            name: Revision name
            description: Revision description
            state: Revision state
            **kwargs: Additional fields

        Returns:
            Created ProductRevision object
        """
        # Get product to link revision
        product = self._repo.get_by_part_number(part_number)
        if not product:
            return None

        rev = ProductRevision(
            revision=revision,
            name=name,
            description=description,
            state=state,
            product_id=product.product_id,
            part_number=part_number,
            **kwargs
        )
        return self._repo.save_revision(rev)

    def update_revision(
        self, revision: ProductRevision
    ) -> Optional[ProductRevision]:
        """
        Update an existing product revision.

        Args:
            revision: ProductRevision object with updated fields

        Returns:
            Updated ProductRevision object
        """
        return self._repo.save_revision(revision)

    def bulk_save_revisions(
        self, revisions: List[ProductRevision]
    ) -> List[ProductRevision]:
        """
        Bulk create or update revisions.

        Args:
            revisions: List of ProductRevision objects

        Returns:
            List of saved ProductRevision objects
        """
        return self._repo.save_revisions_bulk(revisions)

    # =========================================================================
    # Bill of Materials
    # =========================================================================

    def update_bom(self, bom_data: Dict[str, Any]) -> bool:
        """
        Update product BOM (Bill of Materials).

        Args:
            bom_data: BOM data dictionary

        Returns:
            True if successful
        """
        return self._repo.update_bom(bom_data)

    # =========================================================================
    # Product Groups
    # =========================================================================

    def get_groups(
        self,
        filter_str: Optional[str] = None,
        top: Optional[int] = None
    ) -> List[ProductGroup]:
        """
        Get product groups.

        Args:
            filter_str: OData filter string
            top: Max number of results

        Returns:
            List of ProductGroup objects
        """
        return self._repo.get_groups(filter_str=filter_str, top=top)

    def get_groups_for_product(
        self, part_number: str, revision: str
    ) -> List[ProductGroup]:
        """
        Get product groups for a specific product.

        Args:
            part_number: The product part number
            revision: The revision identifier

        Returns:
            List of ProductGroup objects
        """
        return self._repo.get_groups_for_product(part_number, revision)

    # =========================================================================
    # Vendors
    # =========================================================================

    def get_vendors(self) -> List[Dict[str, Any]]:
        """
        Get all vendors.

        Returns:
            List of vendor dictionaries
        """
        return self._repo.get_vendors()

    def save_vendor(
        self, vendor_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create or update a vendor.

        Args:
            vendor_data: Vendor data dictionary

        Returns:
            Created/updated vendor data
        """
        return self._repo.save_vendor(vendor_data)

    def delete_vendor(self, vendor_id: str) -> bool:
        """
        Delete a vendor.

        Args:
            vendor_id: The vendor ID

        Returns:
            True if successful
        """
        return self._repo.delete_vendor(vendor_id)
