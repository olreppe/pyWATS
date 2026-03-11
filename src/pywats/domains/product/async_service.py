"""Async Product service - business logic layer.

Async version of the product service for non-blocking operations.
Includes both public and internal API methods.

⚠️ INTERNAL API methods are marked and may change without notice.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
import logging
from pywats.core.logging import get_logger

from .models import Product, ProductRevision, ProductGroup, ProductView, BomItem, ProductRevisionRelation
from .enums import ProductState
from .async_repository import AsyncProductRepository

logger = get_logger(__name__)


class AsyncProductService:
    """
    Async Product business logic.

    Provides high-level async operations for managing products, revisions,
    groups, and vendors.
    Includes both public and internal API methods (marked with ⚠️).
    """

    def __init__(
        self, 
        repository: AsyncProductRepository,
        base_url: str = ""
    ) -> None:
        """
        Initialize with async repository.

        Args:
            repository: AsyncProductRepository for data access
            base_url: Base URL for internal API calls
        """
        self._repository = repository
        self._base_url = base_url.rstrip("/") if base_url else ""

    # =========================================================================
    # Product Operations
    # =========================================================================

    async def get_products(self) -> List[Product]:
        """
        Get all products (lightweight list view).

        Returns Product objects with basic fields populated:
        - part_number, name, product_category_name (category), non_serial, state
        
        Optional fields (description, product_id, xml_data, revisions, tags) 
        will be None/empty. Use get_product(part_number) to fetch complete details.

        Returns:
            List of Product objects with basic fields only
        """
        return await self._repository.get_all()

    async def get_products_full(self) -> List[Product]:
        """
        Get all products (lightweight list view).
        
        Alias for get_products(). Despite the name, this returns the same
        lightweight data as get_products() - use get_product(part_number) 
        for complete product information.

        Returns:
            List of Product objects with basic fields only
        """
        return await self.get_products()

    async def get_product(self, part_number: str) -> Optional[Product]:
        """
        Get a product by part number with complete details.
        
        Returns full Product object with all fields populated (where available),
        including description, product_id, xml_data, revisions, and tags.

        Args:
            part_number: The product part number

        Returns:
            Product with all available fields populated, or None if not found
        """
        if not part_number or not part_number.strip():
            raise ValueError("part_number is required")
        return await self._repository.get_by_part_number(part_number)

    async def create_product(
        self,
        part_number: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        non_serial: bool = False,
        state: ProductState = ProductState.ACTIVE,
        *,
        xml_data: Optional[str] = None,
        product_category_id: Optional[str] = None,
    ) -> Optional[Product]:
        """
        Create a new product.

        Args:
            part_number: Unique part number (required)
            name: Product display name
            description: Product description text
            non_serial: If True, product cannot have serialized units
            state: Product state (default: ACTIVE)
            xml_data: Custom XML data for key-value storage
            product_category_id: UUID of product category to assign

        Returns:
            Created Product object, or None on failure
        """
        if not part_number or not part_number.strip():
            raise ValueError("part_number is required")
        product = Product(
            part_number=part_number,
            name=name,
            description=description,
            non_serial=non_serial,
            state=state,
            xml_data=xml_data,
            product_category_id=UUID(product_category_id) if product_category_id else None,
        )
        result = await self._repository.save(product)
        if result:
            logger.info(f"PRODUCT_CREATED: {result.part_number} (name={name}, state={state.name})")
        return result

    async def update_product(self, product: Product) -> Optional[Product]:
        """
        Update an existing product.

        Args:
            product: Product object with updated fields

        Returns:
            Updated Product object
        """
        result = await self._repository.save(product)
        if result:
            logger.info(f"PRODUCT_UPDATED: {result.part_number}")
        return result

    async def bulk_save_products(
        self, products: List[Product]
    ) -> List[Product]:
        """
        Bulk create or update products.

        Args:
            products: List of Product objects

        Returns:
            List of saved Product objects
        """
        results = await self._repository.save_bulk(products)
        if results:
            logger.info(f"PRODUCTS_BULK_SAVED: count={len(results)}")
        return results

    async def get_active_products(self) -> List[Product]:
        """
        Get all active products (lightweight list view).
        
        Returns Product objects with basic fields only. For complete product 
        details including description, revisions, etc., use get_product(part_number).

        Returns:
            List of active Product objects (state == ACTIVE) with basic fields
        """
        products = await self.get_products()
        return [p for p in products if p.state == ProductState.ACTIVE]

    def is_active(self, product: Product) -> bool:
        """
        Check if a product is in active state.
        
        Args:
            product: Product to check
            
        Returns:
            True if product state is ACTIVE
        """
        return product.state == ProductState.ACTIVE

    # =========================================================================
    # Revision Operations
    # =========================================================================

    async def get_revisions(self, part_number: str) -> List[ProductRevision]:
        """
        Get all revisions for a product.
        
        Args:
            part_number: Product part number
            
        Returns:
            List of ProductRevision objects
        """
        product = await self.get_product(part_number)
        if not product:
            return []
        return product.revisions

    async def get_revision(
        self, part_number: str, revision: str
    ) -> Optional[ProductRevision]:
        """
        Get a specific product revision.

        Args:
            part_number: The product part number
            revision: The revision identifier

        Returns:
            ProductRevision or None if not found
        """
        if not part_number or not part_number.strip():
            raise ValueError("part_number is required")
        if not revision or not revision.strip():
            raise ValueError("revision is required")
        
        product = await self._repository.get_by_part_number(part_number)
        if not product:
            return None
        
        for rev in product.revisions:
            if rev.revision == revision:
                rev.part_number = part_number
                return rev
        return None

    async def create_revision(
        self,
        part_number: str,
        revision: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        state: ProductState = ProductState.ACTIVE
    ) -> Optional[ProductRevision]:
        """
        Create a new product revision.

        Args:
            part_number: Product part number
            revision: Revision identifier
            name: Revision name/title
            description: Revision description
            state: Revision state

        Returns:
            Created ProductRevision object
        """
        if not part_number or not part_number.strip():
            raise ValueError("part_number is required")
        if not revision or not revision.strip():
            raise ValueError("revision is required")
        
        # Get or create the product to obtain product_id
        product = await self._repository.get_by_part_number(part_number)
        
        rev = ProductRevision(
            part_number=part_number,
            revision=revision,
            name=name,
            description=description,
            state=state,
            product_id=product.product_id if product else None
        )
        result = await self._repository.save_revision(rev)
        if result:
            logger.info(f"REVISION_CREATED: {part_number}/{revision}")
        return result

    async def update_revision(
        self, revision: ProductRevision
    ) -> Optional[ProductRevision]:
        """
        Update an existing product revision.

        Args:
            revision: ProductRevision object with updated fields

        Returns:
            Updated ProductRevision object
        """
        result = await self._repository.save_revision(revision)
        if result:
            logger.info(f"REVISION_UPDATED: {revision.part_number}/{revision.revision}")
        return result

    async def bulk_save_revisions(
        self, revisions: List[ProductRevision]
    ) -> List[ProductRevision]:
        """
        Bulk create or update product revisions.
        
        Args:
            revisions: List of ProductRevision objects
            
        Returns:
            List of saved ProductRevision objects
        """
        results = []
        for rev in revisions:
            result = await self._repository.save_revision(rev)
            if result:
                results.append(result)
        if results:
            logger.info(f"REVISIONS_BULK_SAVED: count={len(results)}")
        return results

    # =========================================================================
    # Product Groups
    # =========================================================================

    async def get_groups(self) -> List[ProductGroup]:
        """
        Get all product groups.

        Returns:
            List of ProductGroup objects
        """
        return await self._repository.get_groups()

    async def create_group(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Optional[ProductGroup]:
        """
        Create a new product group.

        Args:
            name: Group name
            description: Group description

        Returns:
            Created ProductGroup object
        """
        group = ProductGroup(product_group_name=name)
        result = await self._repository.save_group(group)
        if result:
            logger.info(f"GROUP_CREATED: {name}")
        return result

    # =========================================================================
    # ⚠️ INTERNAL API - BOM Operations
    # =========================================================================

    async def get_bom(self, part_number: str, revision: str) -> List[BomItem]:
        """
        ⚠️ INTERNAL: Get BOM (Bill of Materials) for a product revision.

        Args:
            part_number: Product part number
            revision: Product revision

        Returns:
            List of BomItem objects
        """
        return await self._repository.get_bom(part_number, revision)

    async def upload_bom(
        self,
        part_number: str,
        revision: str,
        bom_items: List[Dict[str, Any]],
        format: str = "json"
    ) -> bool:
        """
        ⚠️ INTERNAL: Upload/update BOM items.

        Args:
            part_number: Product part number
            revision: Product revision
            bom_items: List of BOM item dictionaries
            format: BOM format (default: "json")

        Returns:
            True if successful
        """
        return await self._repository.upload_bom(part_number, revision, bom_items, format)

    # =========================================================================
    # ⚠️ INTERNAL API - Box Build / Revision Relations
    # =========================================================================

    async def get_product_hierarchy(
        self,
        part_number: str,
        revision: str
    ) -> List[Dict[str, Any]]:
        """
        ⚠️ INTERNAL: Get product hierarchy including all child revision relations.

        Args:
            part_number: Product part number
            revision: Product revision

        Returns:
            List of hierarchy items
        """
        return await self._repository.get_product_hierarchy(part_number, revision)

    async def add_subunit(
        self,
        parent_part_number: str,
        parent_revision: str,
        child_part_number: str,
        child_revision: str,
        quantity: int = 1,
        revision_mask: Optional[str] = None
    ) -> Optional[ProductRevisionRelation]:
        """
        ⚠️ INTERNAL: Add a subunit to a product's box build template.

        Args:
            parent_part_number: Parent product part number
            parent_revision: Parent product revision
            child_part_number: Child product part number
            child_revision: Child product revision
            quantity: Number of child units required
            revision_mask: Optional revision mask pattern

        Returns:
            Created ProductRevisionRelation or None
        """
        parent = await self.get_revision(parent_part_number, parent_revision)
        if not parent or not parent.product_revision_id:
            raise ValueError(f"Parent revision not found: {parent_part_number}/{parent_revision}")
        
        child = await self.get_revision(child_part_number, child_revision)
        if not child or not child.product_revision_id:
            raise ValueError(f"Child revision not found: {child_part_number}/{child_revision}")
        
        result = await self._repository.create_revision_relation(
            parent_revision_id=parent.product_revision_id,
            child_revision_id=child.product_revision_id,
            quantity=quantity,
            revision_mask=revision_mask
        )
        if result:
            logger.info(f"SUBUNIT_ADDED: {child_part_number}/{child_revision} -> {parent_part_number}/{parent_revision}")
        return result

    async def remove_subunit(self, relation_id: UUID) -> bool:
        """
        ⚠️ INTERNAL: Remove a subunit from a product's box build template.

        Args:
            relation_id: The relation ID to remove

        Returns:
            True if successful
        """
        result = await self._repository.delete_revision_relation(relation_id)
        if result:
            logger.info(f"SUBUNIT_REMOVED: relation_id={relation_id}")
        return result

    # =========================================================================
    # ⚠️ INTERNAL API - Product Categories
    # =========================================================================

    async def get_product_categories(self) -> List[Dict[str, Any]]:
        """
        ⚠️ INTERNAL: Get all product categories.

        Returns:
            List of category dictionaries
        """
        return await self._repository.get_categories()

    async def save_product_categories(self, categories: List[Dict[str, Any]]) -> bool:
        """
        ⚠️ INTERNAL: Save product categories.

        Args:
            categories: List of category dictionaries

        Returns:
            True if successful
        """
        return await self._repository.save_categories(categories)

    # =========================================================================
    # Tags (using product/revision updates)
    # =========================================================================

    async def get_product_tags(self, part_number: str) -> List[Dict[str, str]]:
        """
        Get tags for a product.
        
        Args:
            part_number: Product part number
            
        Returns:
            List of tag dictionaries with 'key' and 'value'
        """
        product = await self.get_product(part_number)
        if product and product.tags:
            return [{"key": t.key, "value": t.value or ""} for t in product.tags]
        return []

    async def set_product_tags(
        self,
        part_number: str,
        tags: List[Dict[str, str]]
    ) -> Optional[Product]:
        """
        Set tags for a product (replaces existing tags).
        
        Args:
            part_number: Product part number
            tags: List of tag dictionaries with 'key' and 'value'
            
        Returns:
            Updated Product or None if not found
        """
        from ...shared import Setting, ChangeType
        product = await self.get_product(part_number)
        if not product:
            return None
        
        product.tags = [
            Setting(key=t["key"], value=t["value"], change=ChangeType.ADD)
            for t in tags
        ]
        return await self.update_product(product)

    async def add_product_tag(
        self,
        part_number: str,
        name: str,
        value: str
    ) -> Optional[Product]:
        """
        Add a single tag to a product.
        
        Args:
            part_number: Product part number
            name: Tag key/name
            value: Tag value
            
        Returns:
            Updated Product or None if not found
        """
        from ...shared import Setting, ChangeType
        product = await self.get_product(part_number)
        if not product:
            return None
        
        if not product.tags:
            product.tags = []
        
        # Check if tag already exists
        for tag in product.tags:
            if tag.key == name:
                tag.value = value
                tag.change = ChangeType.UPDATE
                return await self.update_product(product)
        
        # Add new tag
        product.tags.append(Setting(key=name, value=value, change=ChangeType.ADD))
        return await self.update_product(product)

    async def get_revision_tags(
        self,
        part_number: str,
        revision: str
    ) -> List[Dict[str, str]]:
        """
        Get tags for a product revision.
        
        Args:
            part_number: Product part number
            revision: Revision identifier
            
        Returns:
            List of tag dictionaries
        """
        rev = await self.get_revision(part_number, revision)
        if rev and rev.tags:
            return [{"key": t.key, "value": t.value or ""} for t in rev.tags]
        return []

    async def set_revision_tags(
        self,
        part_number: str,
        revision: str,
        tags: List[Dict[str, str]]
    ) -> Optional[ProductRevision]:
        """
        Set tags for a product revision.
        
        Args:
            part_number: Product part number
            revision: Revision identifier
            tags: List of tag dictionaries
            
        Returns:
            Updated ProductRevision or None if not found
        """
        from ...shared import Setting, ChangeType
        rev = await self.get_revision(part_number, revision)
        if not rev:
            return None
        
        rev.tags = [
            Setting(key=t["key"], value=t["value"], change=ChangeType.ADD)
            for t in tags
        ]
        return await self.update_revision(rev)

    async def add_revision_tag(
        self,
        part_number: str,
        revision: str,
        name: str,
        value: str
    ) -> Optional[ProductRevision]:
        """
        Add a single tag to a product revision.
        
        Args:
            part_number: Product part number
            revision: Revision identifier
            name: Tag key/name
            value: Tag value
            
        Returns:
            Updated ProductRevision or None if not found
        """
        from ...shared import Setting, ChangeType
        rev = await self.get_revision(part_number, revision)
        if not rev:
            return None
        
        if not rev.tags:
            rev.tags = []
        
        # Check if tag already exists
        for tag in rev.tags:
            if tag.key == name:
                tag.value = value
                tag.change = ChangeType.UPDATE
                return await self.update_revision(rev)
        
        # Add new tag
        rev.tags.append(Setting(key=name, value=value, change=ChangeType.ADD))
        return await self.update_revision(rev)

    # =========================================================================
    # ⚠️ INTERNAL API - Vendors
    # =========================================================================

    async def get_vendors(self) -> List[Dict[str, Any]]:
        """
        ⚠️ INTERNAL: Get all vendors.
        
        Returns:
            List of vendor dictionaries
        """
        return await self._repository.get_vendors()

    async def save_vendor(
        self,
        name: str,
        vendor_id: Optional[str] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        ⚠️ INTERNAL: Create or update a vendor.
        
        Args:
            name: Vendor name
            vendor_id: Vendor ID for updates
            **kwargs: Additional vendor fields
            
        Returns:
            Saved vendor dictionary or None
        """
        return await self._repository.save_vendor(name, vendor_id, **kwargs)

    async def delete_vendor(self, vendor_id: str) -> bool:
        """
        ⚠️ INTERNAL: Delete a vendor.
        
        Args:
            vendor_id: Vendor ID to delete
            
        Returns:
            True if successful
        """
        return await self._repository.delete_vendor(vendor_id)

    # =========================================================================
    # ⚠️ INTERNAL API - Box Build Template
    # =========================================================================

    async def _load_box_build_relations(
        self, 
        part_number: str, 
        revision: str
    ) -> List[ProductRevisionRelation]:
        """
        Load existing box build relations from server.
        
        ⚠️ INTERNAL API
        
        Uses GetProductInfo which returns the full hierarchy including
        all child relations with their ProductRevisionRelationId.
        
        Args:
            part_number: Product part number
            revision: Product revision
            
        Returns:
            List of ProductRevisionRelation
        """
        hierarchy = await self._repository.get_product_hierarchy(part_number, revision)
        if not hierarchy:
            return []
        
        # Extract child relations (hlevel > 0 with ProductRevisionRelationId)
        relations = []
        for item in hierarchy:
            if item.get("hlevel", 0) > 0 and item.get("ProductRevisionRelationId"):
                try:
                    # Map hierarchy fields to ProductRevisionRelation fields
                    rel_data = {
                        "ProductRevisionRelationId": item.get("ProductRevisionRelationId"),
                        "ParentProductRevisionId": item.get("ParentProductRevisionId"),
                        "ProductRevisionId": item.get("ProductRevisionId"),
                        "Quantity": item.get("Quantity", 1),
                        "RevisionMask": item.get("RevisionMask"),
                        "ChildPartNumber": item.get("PartNumber"),
                        "ChildRevision": item.get("Revision"),
                    }
                    relations.append(ProductRevisionRelation.model_validate(rel_data))
                except Exception as e:
                    logger.debug(f"Skipping invalid product revision relation: {e}")
        
        return relations

    async def get_box_build_template(
        self,
        part_number: str,
        revision: str
    ) -> "AsyncBoxBuildTemplate":
        """
        Get or create a box build template for a product revision.
        
        ⚠️ INTERNAL API
        
        A box build template defines WHAT subunits are required to build a product.
        This is a PRODUCT-LEVEL definition - it does not create production units.
        
        Use the returned AsyncBoxBuildTemplate to add/remove subunits, then call
        save() to persist changes to the server.
        
        Args:
            part_number: Parent product part number
            revision: Parent product revision
            
        Returns:
            AsyncBoxBuildTemplate for managing subunits
            
        Raises:
            ValueError: If product revision not found
        """
        # Get the parent revision
        parent_revision = await self.get_revision(part_number, revision)
        if not parent_revision:
            raise ValueError(f"Product revision not found: {part_number}/{revision}")
        
        # Load existing relations
        relations = await self._load_box_build_relations(part_number, revision)
        
        return AsyncBoxBuildTemplate(
            parent_revision=parent_revision,
            service=self,
            existing_relations=relations
        )

    async def get_box_build_subunits(
        self,
        part_number: str,
        revision: str
    ) -> List[ProductRevisionRelation]:
        """
        Get subunits for a box build (read-only).
        
        ⚠️ INTERNAL API
        
        Args:
            part_number: Parent product part number
            revision: Parent product revision
            
        Returns:
            List of ProductRevisionRelation representing subunits
        """
        return await self._load_box_build_relations(part_number, revision)

    async def get_groups_for_product(
        self,
        part_number: str
    ) -> List[ProductGroup]:
        """
        Get product groups that contain a specific product.
        
        Args:
            part_number: Product part number
            
        Returns:
            List of ProductGroup objects containing this product
        """
        product = await self.get_product(part_number)
        if not product:
            return []
        return await self._repository.get_groups_for_product(part_number)

    async def get_bom_items(
        self,
        part_number: str,
        revision: str
    ) -> List[BomItem]:
        """
        ⚠️ INTERNAL: Get BOM items (alias for get_bom).
        
        Args:
            part_number: Product part number
            revision: Revision identifier
            
        Returns:
            List of BomItem objects
        """
        return await self.get_bom(part_number, revision)

    async def update_bom(
        self,
        part_number: str,
        revision: str,
        bom_items: List[BomItem],
        description: Optional[str] = None
    ) -> bool:
        """
        Update product BOM (Bill of Materials).
        
        Uses the public API which accepts WSBF (WATS Standard BOM Format) XML.
        
        Args:
            part_number: Product part number
            revision: Revision identifier
            bom_items: List of BomItem objects
            description: Optional product description
            
        Returns:
            True if successful
        """
        result = await self._repository.update_bom(part_number, revision, bom_items, description)
        if result:
            logger.info(f"BOM_UPDATED: {part_number}/{revision} (items={len(bom_items)})")
        return result


# =============================================================================
# Box Build Template
# =============================================================================


class AsyncBoxBuildTemplate:
    """
    Async builder class for managing box build templates (product-level definitions).

    A box build template defines the subunits required to build a parent product.
    For example, a controller module may require 2 PCBAs, 1 power supply, etc.

    This class provides a fluent interface for adding/removing subunits and
    commits all changes to the server when save() is called.

    Example:
        # Get or create a box build template
        template = await api.product.get_box_build_template("MAIN-BOARD", "A")

        # Add subunits (defines what's needed)
        await template.add_subunit("PCBA-001", "A", quantity=2)
        await template.add_subunit("PSU-100", "B", quantity=1)

        # Remove a subunit
        await template.remove_subunit("OLD-PART", "A")

        # Save all changes
        await template.save()

        # Or use async context manager for auto-save
        async with await api.product.get_box_build_template("MAIN-BOARD", "A") as template:
            await template.add_subunit("PCBA-001", "A", quantity=2)
        # Changes saved automatically
    """

    def __init__(
        self,
        parent_revision: ProductRevision,
        service: "AsyncProductService",
        existing_relations: Optional[List[ProductRevisionRelation]] = None
    ) -> None:
        """
        Initialize box build template.

        Args:
            parent_revision: The parent product revision
            service: AsyncProductService for API operations
            existing_relations: Existing relations loaded from server
        """
        self._parent = parent_revision
        self._service = service

        # Track current state
        self._relations: List[ProductRevisionRelation] = list(existing_relations or [])

        # Track pending changes
        self._to_add: List[ProductRevisionRelation] = []
        self._to_update: List[ProductRevisionRelation] = []
        self._to_delete: List[UUID] = []

    # =========================================================================
    # Properties
    # =========================================================================

    @property
    def parent_part_number(self) -> Optional[str]:
        """Get the parent product part number."""
        return self._parent.part_number

    @property
    def parent_revision(self) -> str:
        """Get the parent product revision."""
        return self._parent.revision

    @property
    def parent_revision_id(self) -> Optional[UUID]:
        """Get the parent product revision ID."""
        return self._parent.product_revision_id

    @property
    def subunits(self) -> List[ProductRevisionRelation]:
        """
        Get current subunits (including pending additions, excluding pending deletions).

        Returns:
            List of ProductRevisionRelation representing subunits
        """
        current = [r for r in self._relations if r.relation_id not in self._to_delete]
        return current + self._to_add

    @property
    def has_pending_changes(self) -> bool:
        """Check if there are unsaved changes."""
        return bool(self._to_add or self._to_update or self._to_delete)

    # =========================================================================
    # Async Fluent Builder Methods
    # =========================================================================

    async def add_subunit(
        self,
        part_number: str,
        revision: str,
        quantity: int = 1,
        item_number: Optional[str] = None,
        revision_mask: Optional[str] = None
    ) -> "AsyncBoxBuildTemplate":
        """
        Add a subunit to the box build template.

        Args:
            part_number: Subunit part number
            revision: Subunit revision (default revision for the subunit)
            quantity: Number of subunits required (default: 1)
            item_number: Optional item/position number
            revision_mask: Optional revision mask pattern

        Returns:
            Self for method chaining
        """
        # Get the child revision ID
        child_revision = await self._service.get_revision(part_number, revision)
        if not child_revision or not child_revision.product_revision_id:
            raise ValueError(f"Product revision not found: {part_number}/{revision}")

        if not self._parent.product_revision_id:
            raise ValueError("Parent product revision ID is not set")

        # Check if already exists
        for rel in self.subunits:
            if rel.child_product_revision_id == child_revision.product_revision_id:
                # Update quantity instead of adding duplicate
                return await self.update_subunit(
                    part_number, revision,
                    quantity=quantity,
                    item_number=item_number,
                    revision_mask=revision_mask
                )

        # Create new relation with revision mask
        relation = ProductRevisionRelation(
            parent_product_revision_id=self._parent.product_revision_id,
            child_product_revision_id=child_revision.product_revision_id,
            quantity=quantity,
            item_number=item_number,
            child_part_number=part_number,
            child_revision=revision,
            revision_mask=revision_mask
        )
        self._to_add.append(relation)

        return self

    async def update_subunit(
        self,
        part_number: str,
        revision: str,
        quantity: Optional[int] = None,
        item_number: Optional[str] = None,
        revision_mask: Optional[str] = None
    ) -> "AsyncBoxBuildTemplate":
        """
        Update an existing subunit in the box build template.

        Args:
            part_number: Subunit part number
            revision: Subunit revision
            quantity: New quantity (if provided)
            item_number: New item number (if provided)
            revision_mask: New revision mask pattern (if provided)

        Returns:
            Self for method chaining
        """
        # Find existing relation
        for rel in self._relations:
            if rel.child_part_number == part_number and rel.child_revision == revision:
                if quantity is not None:
                    rel.quantity = quantity
                if item_number is not None:
                    rel.item_number = item_number
                if revision_mask is not None:
                    rel.revision_mask = revision_mask
                if rel not in self._to_update:
                    self._to_update.append(rel)
                return self

        # Check pending additions
        for rel in self._to_add:
            if rel.child_part_number == part_number and rel.child_revision == revision:
                if quantity is not None:
                    rel.quantity = quantity
                if item_number is not None:
                    rel.item_number = item_number
                if revision_mask is not None:
                    rel.revision_mask = revision_mask
                return self

        raise ValueError(f"Subunit not found: {part_number}/{revision}")

    async def remove_subunit(self, part_number: str, revision: str) -> "AsyncBoxBuildTemplate":
        """
        Remove a subunit from the box build template.

        Args:
            part_number: Subunit part number
            revision: Subunit revision

        Returns:
            Self for method chaining
        """
        # Check existing relations
        for rel in self._relations:
            if rel.child_part_number == part_number and rel.child_revision == revision:
                if rel.relation_id:
                    self._to_delete.append(rel.relation_id)
                # Remove from update list if present
                if rel in self._to_update:
                    self._to_update.remove(rel)
                return self

        # Check pending additions
        for rel in self._to_add:
            if rel.child_part_number == part_number and rel.child_revision == revision:
                self._to_add.remove(rel)
                return self

        raise ValueError(f"Subunit not found: {part_number}/{revision}")

    def clear_all(self) -> "AsyncBoxBuildTemplate":
        """
        Mark all subunits for removal.

        Returns:
            Self for method chaining
        """
        for rel in self._relations:
            if rel.relation_id:
                self._to_delete.append(rel.relation_id)
        self._to_add.clear()
        self._to_update.clear()
        return self

    async def set_quantity(self, part_number: str, revision: str, quantity: int) -> "AsyncBoxBuildTemplate":
        """
        Set the quantity for a subunit.

        Args:
            part_number: Subunit part number
            revision: Subunit revision
            quantity: New quantity

        Returns:
            Self for method chaining
        """
        return await self.update_subunit(part_number, revision, quantity=quantity)

    # =========================================================================
    # Save/Commit Operations
    # =========================================================================

    async def save(self) -> "AsyncBoxBuildTemplate":
        """
        Save all pending changes to the server.

        Performs all additions, updates, and deletions in order.

        Returns:
            Self for method chaining
        """
        # Process deletions first
        for relation_id in self._to_delete:
            await self._service._repository.delete_revision_relation(relation_id)

        # Remove deleted relations from our list
        self._relations = [r for r in self._relations if r.relation_id not in self._to_delete]
        self._to_delete.clear()

        # Process updates
        for relation in self._to_update:
            updated = await self._service._repository.update_revision_relation(relation)
            if updated:
                idx = next((i for i, r in enumerate(self._relations) if r.relation_id == updated.relation_id), None)
                if idx is not None:
                    self._relations[idx] = updated
        self._to_update.clear()

        # Process additions
        for relation in self._to_add:
            created_data = await self._service._repository.create_revision_relation(
                parent_revision_id=relation.parent_product_revision_id,
                child_revision_id=relation.child_product_revision_id,
                quantity=relation.quantity,
                item_number=relation.item_number,
                revision_mask=relation.revision_mask
            )
            if created_data:
                created = ProductRevisionRelation.model_validate(created_data)
                self._relations.append(created)
        self._to_add.clear()

        return self

    def discard(self) -> "AsyncBoxBuildTemplate":
        """
        Discard all pending changes.

        Returns:
            Self for method chaining
        """
        self._to_add.clear()
        self._to_update.clear()
        self._to_delete.clear()
        return self

    async def reload(self) -> "AsyncBoxBuildTemplate":
        """
        Reload relations from server, discarding pending changes.

        Returns:
            Self for method chaining
        """
        self.discard()
        self._relations = await self._service._load_box_build_relations(
            self._parent.part_number or "",
            self._parent.revision
        )
        return self

    # =========================================================================
    # Validation Helpers
    # =========================================================================

    def validate_subunit(self, part_number: str, revision: str) -> bool:
        """
        Check if a specific subunit revision is valid for this box build.

        Args:
            part_number: The part number to validate
            revision: The revision to validate

        Returns:
            True if the subunit/revision combination is valid
        """
        for rel in self.subunits:
            if rel.child_part_number == part_number:
                return rel.matches_revision(revision)
        return False

    def get_matching_subunits(self, part_number: str) -> List[ProductRevisionRelation]:
        """
        Get all subunit definitions for a given part number.

        Args:
            part_number: The part number to search for

        Returns:
            List of matching ProductRevisionRelation objects
        """
        return [rel for rel in self.subunits if rel.child_part_number == part_number]

    def get_required_parts(self) -> List[dict]:
        """
        Get a summary of all required parts for this box build.

        Returns:
            List of dicts with part_number, default_revision, quantity, revision_mask
        """
        return [
            {
                "part_number": rel.child_part_number,
                "default_revision": rel.child_revision,
                "quantity": rel.quantity,
                "revision_mask": rel.revision_mask,
                "item_number": rel.item_number
            }
            for rel in self.subunits
        ]

    # =========================================================================
    # Async Context Manager Support
    # =========================================================================

    async def __aenter__(self) -> "AsyncBoxBuildTemplate":
        """Enter async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object]
    ) -> None:
        """Exit async context manager - auto-save if no exception."""
        if exc_type is None and self.has_pending_changes:
            await self.save()

    # =========================================================================
    # String Representation
    # =========================================================================

    def __repr__(self) -> str:
        return (
            f"AsyncBoxBuildTemplate(parent='{self.parent_part_number}/{self.parent_revision}', "
            f"subunits={len(self.subunits)}, pending_changes={self.has_pending_changes})"
        )

    def __str__(self) -> str:
        lines = [f"Box Build: {self.parent_part_number}/{self.parent_revision}"]
        lines.append(f"Subunits ({len(self.subunits)}):")
        for sub in self.subunits:
            mask_info = f" [mask: {sub.revision_mask}]" if sub.revision_mask else ""
            lines.append(f"  - {sub.child_part_number}/{sub.child_revision} x{sub.quantity}{mask_info}")
        if self.has_pending_changes:
            lines.append(f"Pending: +{len(self._to_add)} ~{len(self._to_update)} -{len(self._to_delete)}")
        return "\n".join(lines)


# Alias for backward compatibility and sync wrapper usage
BoxBuildTemplate = AsyncBoxBuildTemplate
