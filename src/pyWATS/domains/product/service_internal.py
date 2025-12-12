"""Product service - internal API business logic layer.

⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️

Uses internal WATS API endpoints that are not publicly documented.
These methods may change or be removed without notice.
"""
from typing import List, Optional, Dict, Any
from uuid import UUID

from .repository import ProductRepository
from .repository_internal import ProductRepositoryInternal
from .models import (
    Product, ProductRevision, ProductRevisionRelation, 
    BomItem, ProductCategory
)
from .box_build import BoxBuildTemplate


class ProductServiceInternal:
    """
    Product business logic layer using internal API.
    
    ⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️
    
    Provides extended operations including:
    - Box build template management
    - BOM operations
    - Product categories
    """
    
    def __init__(
        self, 
        repository: ProductRepository,
        repository_internal: ProductRepositoryInternal
    ):
        """
        Initialize service with repositories.
        
        Args:
            repository: ProductRepository for public API
            repository_internal: ProductRepositoryInternal for internal API
        """
        self._repository = repository
        self._repo_internal = repository_internal
    
    # =========================================================================
    # Product/Revision Lookup (uses public API)
    # =========================================================================
    
    def get_product(self, part_number: str) -> Optional[Product]:
        """
        Get a product by part number.
        
        Args:
            part_number: The product part number
            
        Returns:
            Product or None if not found
        """
        return self._repository.get_by_part_number(part_number)
    
    def get_revision(self, part_number: str, revision: str) -> Optional[ProductRevision]:
        """
        Get a specific product revision.
        
        Args:
            part_number: The product part number
            revision: The revision identifier
            
        Returns:
            ProductRevision or None if not found
        """
        # Get the product which includes revisions
        product = self.get_product(part_number)
        if not product:
            return None
        
        # Find the matching revision
        for rev in product.revisions:
            if rev.revision == revision:
                # Ensure part_number is set
                rev.part_number = part_number
                return rev
        
        return None
    
    # =========================================================================
    # Box Build Templates
    # =========================================================================
    
    def get_box_build(self, part_number: str, revision: str) -> BoxBuildTemplate:
        """
        Get or create a box build template for a product revision.
        
        ⚠️ INTERNAL API
        
        A box build template defines the subunits required to build a product.
        Use the returned BoxBuildTemplate to add/remove subunits, then call
        save() to persist changes.
        
        Args:
            part_number: Parent product part number
            revision: Parent product revision
            
        Returns:
            BoxBuildTemplate for managing subunits
            
        Raises:
            ValueError: If product revision not found
            
        Example:
            # Simple usage
            template = api.product_internal.get_box_build("MAIN-BOARD", "A")
            template.add_subunit("PCBA-001", "A", quantity=2)
            template.save()
            
            # Context manager (auto-save)
            with api.product_internal.get_box_build("MAIN-BOARD", "A") as bb:
                bb.add_subunit("PCBA-001", "A", quantity=2)
                bb.add_subunit("PSU-100", "B")
        """
        # Get the parent revision
        parent_revision = self.get_revision(part_number, revision)
        if not parent_revision:
            raise ValueError(f"Product revision not found: {part_number}/{revision}")
        
        # Load existing relations
        relations = self._load_box_build_relations(part_number, revision)
        
        return BoxBuildTemplate(
            parent_revision=parent_revision,
            service=self,
            existing_relations=relations
        )
    
    def _load_box_build_relations(
        self, 
        part_number: str, 
        revision: str
    ) -> List[ProductRevisionRelation]:
        """
        Load existing box build relations from server.
        
        ⚠️ INTERNAL API
        
        Args:
            part_number: Product part number
            revision: Product revision
            
        Returns:
            List of ProductRevisionRelation
        """
        data = self._repo_internal.get_product_with_relations(part_number)
        if not data:
            return []
        
        # Find the matching revision
        revisions_data = data.get("ProductRevisions", [])
        for rev_data in revisions_data:
            if rev_data.get("Revision") == revision:
                # Extract child relations (subunits in box build)
                relations_data = rev_data.get("ChildProductRevisionRelations") or []
                relations = []
                for rel_data in relations_data:
                    try:
                        relations.append(ProductRevisionRelation.model_validate(rel_data))
                    except Exception:
                        pass  # Skip invalid relations
                return relations
        
        return []
    
    def get_box_build_subunits(
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
        return self._load_box_build_relations(part_number, revision)
    
    # =========================================================================
    # BOM Operations
    # =========================================================================
    
    def get_bom(self, part_number: str, revision: str) -> List[BomItem]:
        """
        Get BOM (Bill of Materials) for a product revision.
        
        ⚠️ INTERNAL API
        
        Args:
            part_number: Product part number
            revision: Product revision
            
        Returns:
            List of BomItem objects
        """
        return self._repo_internal.get_bom(part_number, revision)
    
    def upload_bom(
        self, 
        part_number: str, 
        revision: str,
        bom_items: List[BomItem]
    ) -> bool:
        """
        Upload/update BOM for a product revision.
        
        ⚠️ INTERNAL API
        
        Args:
            part_number: Product part number
            revision: Product revision
            bom_items: List of BomItem objects
            
        Returns:
            True if successful
        """
        # Get the product revision to get its ID
        rev = self.get_revision(part_number, revision)
        if not rev or not rev.product_revision_id:
            raise ValueError(f"Product revision not found: {part_number}/{revision}")
        
        # Set the product revision ID on all items
        items_data = []
        for item in bom_items:
            item_dict = item.model_dump(by_alias=True, exclude_none=True)
            item_dict["productRevisionId"] = str(rev.product_revision_id)
            items_data.append(item_dict)
        
        return self._repo_internal.upload_bom(part_number, revision, items_data)
    
    def upload_bom_from_dict(
        self,
        part_number: str,
        revision: str,
        bom_data: List[Dict[str, Any]]
    ) -> bool:
        """
        Upload BOM from dictionary data.
        
        ⚠️ INTERNAL API
        
        Args:
            part_number: Product part number
            revision: Product revision
            bom_data: List of BOM item dictionaries
            
        Returns:
            True if successful
        """
        # Get the product revision to get its ID
        rev = self.get_revision(part_number, revision)
        if not rev or not rev.product_revision_id:
            raise ValueError(f"Product revision not found: {part_number}/{revision}")
        
        # Set the product revision ID on all items
        for item in bom_data:
            item["productRevisionId"] = str(rev.product_revision_id)
        
        return self._repo_internal.upload_bom(part_number, revision, bom_data)
    
    # =========================================================================
    # Product Categories
    # =========================================================================
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Get all product categories.
        
        ⚠️ INTERNAL API
        
        Returns:
            List of category dictionaries
        """
        return self._repo_internal.get_categories()
    
    def save_categories(self, categories: List[Dict[str, Any]]) -> bool:
        """
        Save product categories.
        
        ⚠️ INTERNAL API
        
        Args:
            categories: List of category dictionaries
            
        Returns:
            True if successful
        """
        return self._repo_internal.save_categories(categories)
