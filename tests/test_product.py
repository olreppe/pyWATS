"""
Tests for product module - product definitions and revisions

These tests make actual API calls to the WATS server.
"""
from typing import Any, Dict
from datetime import datetime, timezone
from uuid import uuid4
import pytest
from pywats.domains.product import Product, ProductRevision
from pywats.domains.product.models import ProductRevisionRelation, BomItem


class TestProductRetrieval:
    """Test retrieving products from server"""

    def test_get_all_products(self, wats_client: Any) -> None:
        """Test getting all products"""
        print("\n=== GET ALL PRODUCTS ===")
        
        products = wats_client.product.get_products()
        
        print(f"Retrieved {len(products)} products")
        for p in products[:5]:
            print(f"  - {p.part_number}: {p.name}")
        print("========================\n")
        
        assert isinstance(products, list)

    def test_get_products_full(self, wats_client: Any) -> None:
        """Test getting all products with full details"""
        print("\n=== GET PRODUCTS FULL ===")
        
        products = wats_client.product.get_products_full()
        
        print(f"Retrieved {len(products)} products with full details")
        if products:
            p = products[0]
            print(f"First product: {p.part_number}")
            print(f"  Name: {p.name}")
            print(f"  State: {p.state}")
        print("=========================\n")
        
        assert isinstance(products, list)

    def test_get_product_by_part_number(self, wats_client: Any) -> None:
        """Test getting a specific product"""
        print("\n=== GET PRODUCT BY PN ===")
        
        # First get list of products to find an existing one
        products = wats_client.product.get_products()
        if not products:
            pytest.skip("No products available to retrieve")
        
        part_number = products[0].part_number
        print(f"Looking up: {part_number}")
        
        product = wats_client.product.get_product(part_number)
        
        print(f"Found: {product}")
        print("=========================\n")
        
        assert product is not None
        assert product.part_number == part_number


class TestProductCreation:
    """Test creating products on server"""

    def test_create_product(self, wats_client: Any) -> None:
        """Test creating a new product"""
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        part_number = f"PYTEST-{timestamp}"
        
        print("\n=== CREATE PRODUCT ===")
        print(f"Creating product: {part_number}")
        
        result = wats_client.product.create_product(
            part_number=part_number,
            name=f"PyTest Product {timestamp}",
            description="Created by pytest"
        )
        
        print(f"Create result: {result}")
        print("======================\n")
        
        assert result is not None
        assert result.part_number == part_number


class TestProductRevisions:
    """Test product revision operations"""

    def test_get_revisions(self, wats_client: Any) -> None:
        """Test getting revisions for a product"""
        print("\n=== GET REVISIONS ===")
        
        # First get a product
        products = wats_client.product.get_products()
        if not products:
            pytest.skip("No products available")
        
        part_number = products[0].part_number
        print(f"Getting revisions for: {part_number}")
        
        revisions = wats_client.product.get_revisions(part_number)
        
        print(f"Found {len(revisions)} revisions")
        for r in revisions[:5]:
            print(f"  - {r.revision}: {r.description}")
        print("=====================\n")
        
        assert isinstance(revisions, list)

    def test_create_revision(self, wats_client: Any) -> None:
        """Test creating a new revision"""
        timestamp = datetime.now(timezone.utc).strftime('%H%M%S')
        
        print("\n=== CREATE REVISION ===")
        
        # First get a product
        products = wats_client.product.get_products()
        if not products:
            pytest.skip("No products available")
        
        part_number = products[0].part_number
        revision_name = f"R{timestamp}"
        
        print(f"Creating revision {revision_name} for {part_number}")
        
        result = wats_client.product.create_revision(
            part_number=part_number,
            revision=revision_name,
            description=f"Test revision created {timestamp}"
        )
        
        print(f"Create result: {result}")
        print("=======================\n")
        
        assert result is not None


class TestProductGroups:
    """Test product group operations"""

    def test_get_groups(self, wats_client: Any) -> None:
        """Test getting product groups"""
        print("\n=== GET PRODUCT GROUPS ===")
        
        groups = wats_client.product.get_groups()
        
        print(f"Retrieved {len(groups)} groups")
        for g in groups[:5]:
            print(f"  - {g.name}")
        print("==========================\n")
        
        assert isinstance(groups, list)


class TestProductModel:
    """Test Product model creation (no server)"""

    def test_create_product_model(self, test_part_number: str) -> None:
        """Test creating a product model object"""
        product = Product(
            part_number=test_part_number,
            name="Test Product"
        )
        assert product.part_number == test_part_number
        assert product.name == "Test Product"

    def test_create_revision_model(
        self, test_part_number: str, test_revision: str
    ) -> None:
        """Test creating a revision model object"""
        revision = ProductRevision(
            part_number=test_part_number,
            revision=test_revision,
            description="Test revision"
        )
        assert revision.revision == test_revision
        assert revision.part_number == test_part_number


# =============================================================================
# Tag Management Tests
# =============================================================================

class TestProductTags:
    """Test product tag management operations.
    
    Note: Tags require dedicated API endpoints, not the Product PUT endpoint.
    The current implementation uses Product PUT which doesn't persist tags.
    These tests verify the API accepts the calls but don't verify persistence.
    
    TODO: Implement dedicated tag endpoints when available:
    - POST /api/Product/{pn}/Tag
    - DELETE /api/Product/{pn}/Tag/{key}
    """
    
    @pytest.fixture
    def test_product_pn(self) -> str:
        """A known product for tag testing"""
        return "PYWATS-TEST-001"
    
    def test_get_product_tags(self, wats_client: Any, test_product_pn: str) -> None:
        """Test getting tags for a product"""
        print("\n=== GET PRODUCT TAGS ===")
        
        tags = wats_client.product.get_product_tags(test_product_pn)
        
        print(f"Tags for {test_product_pn}:")
        for tag in tags:
            print(f"  - {tag['key']}: {tag['value']}")
        print("========================\n")
        
        assert isinstance(tags, list)
    
    def test_set_product_tags(self, wats_client: Any, test_product_pn: str) -> None:
        """Test setting tags on a product"""
        print("\n=== SET PRODUCT TAGS ===")
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        new_tags = [
            {"key": "pytest_test", "value": f"test-{timestamp}"},
            {"key": "environment", "value": "pytest"},
            {"key": "version", "value": "1.0"}
        ]
        
        print(f"Setting tags on {test_product_pn}:")
        for tag in new_tags:
            print(f"  - {tag['key']}: {tag['value']}")
        
        result = wats_client.product.set_product_tags(test_product_pn, new_tags)
        
        print(f"Result: {result is not None}")
        print("========================\n")
        
        # The API accepts the update - verification that tags persist
        # depends on the server implementation
        assert result is not None
    
    def test_add_product_tag(self, wats_client: Any, test_product_pn: str) -> None:
        """Test adding a single tag to a product"""
        print("\n=== ADD PRODUCT TAG ===")
        
        timestamp = datetime.now(timezone.utc).strftime('%H%M%S')
        key = f"added_tag_{timestamp}"
        value = f"value_{timestamp}"
        
        print(f"Adding tag to {test_product_pn}: {key}={value}")
        
        result = wats_client.product.add_product_tag(test_product_pn, key, value)
        
        print(f"Result: {result is not None}")
        print("=======================\n")
        
        # The API accepts the update - verification that tags persist
        # depends on the server implementation
        assert result is not None
    
    def test_get_revision_tags(self, wats_client: Any, test_product_pn: str) -> None:
        """Test getting tags for a product revision"""
        print("\n=== GET REVISION TAGS ===")
        
        # First get the product to find available revisions
        product = wats_client.product.get_product(test_product_pn)
        if not product or not product.revisions:
            pytest.skip("No revisions available for tag testing")
        
        revision = product.revisions[0].revision
        print(f"Using revision: {revision}")
        
        tags = wats_client.product.get_revision_tags(test_product_pn, revision)
        
        print(f"Tags for {test_product_pn}/{revision}:")
        for tag in tags:
            print(f"  - {tag['key']}: {tag['value']}")
        print("=========================\n")
        
        assert isinstance(tags, list)
    
    def test_set_revision_tags(self, wats_client: Any, test_product_pn: str) -> None:
        """Test setting tags on a product revision"""
        print("\n=== SET REVISION TAGS ===")
        
        # First get the product to find available revisions
        product = wats_client.product.get_product(test_product_pn)
        if not product or not product.revisions:
            pytest.skip("No revisions available for tag testing")
        
        revision = product.revisions[0].revision
        print(f"Using revision: {revision}")
        
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        new_tags = [
            {"key": "rev_test", "value": f"rev-{timestamp}"},
            {"key": "rev_env", "value": "pytest"}
        ]
        
        print(f"Setting tags on {test_product_pn}/{revision}:")
        for tag in new_tags:
            print(f"  - {tag['key']}: {tag['value']}")
        
        result = wats_client.product.set_revision_tags(test_product_pn, revision, new_tags)
        
        print(f"Result: {result is not None}")
        print("=========================\n")
        
        assert result is not None


# =============================================================================
# BOM Tests
# =============================================================================

class TestBomOperations:
    """Test BOM (Bill of Materials) operations.
    
    ⚠️ INTERNAL API - Uses internal BOM API endpoints.
    These tests may fail if the internal BOM API is not enabled on the server.
    """
    
    @pytest.fixture
    def test_product_pn(self) -> str:
        """A known product for BOM testing"""
        return "PYWATS-TEST-001"
    
    def test_get_bom(self, wats_client: Any, test_product_pn: str) -> None:
        """Test getting BOM for a product revision"""
        print("\n=== GET BOM ===")
        
        bom = wats_client.product_internal.get_bom(test_product_pn, "1.0")
        
        print(f"BOM for {test_product_pn}/1.0 ({len(bom)} items):")
        for item in bom[:10]:
            print(f"  - {item.component_ref}: {item.part_number} x{item.quantity}")
        if len(bom) > 10:
            print(f"  ... and {len(bom) - 10} more items")
        print("===============\n")
        
        assert isinstance(bom, list)
    
    def test_upload_bom(self, wats_client: Any, test_product_pn: str) -> None:
        """Test uploading BOM items using the public API (WSBF XML format)"""
        print("\n=== UPLOAD BOM (PUBLIC API) ===")
        
        timestamp = datetime.now(timezone.utc).strftime('%H%M%S')
        
        # Create test BOM items
        bom_items = [
            BomItem(
                component_ref=f"R{timestamp}1",
                part_number="RES-10K",
                description="10K Ohm Resistor",
                quantity=5,
                manufacturer="Vishay"
            ),
            BomItem(
                component_ref=f"C{timestamp}1",
                part_number="CAP-100NF",
                description="100nF Ceramic Capacitor",
                quantity=3,
                manufacturer="Murata"
            ),
            BomItem(
                component_ref=f"U{timestamp}1",
                part_number="MCU-STM32",
                description="STM32 Microcontroller",
                quantity=1,
                manufacturer="ST Microelectronics"
            )
        ]
        
        print(f"Uploading BOM to {test_product_pn}/1.0:")
        for item in bom_items:
            print(f"  - {item.component_ref}: {item.part_number} x{item.quantity}")
        
        # Use public API (WSBF XML format)
        result = wats_client.product.update_bom(
            test_product_pn, "1.0", bom_items
        )
        
        print(f"Upload result: {result}")
        print("=================\n")
        
        assert result is True
        
        # Note: Verification via internal API may not return items immediately
        # The upload was successful if result is True
    
    def test_upload_bom_from_dict(self, wats_client: Any, test_product_pn: str) -> None:
        """Test uploading BOM from dictionary format using public API"""
        print("\n=== UPLOAD BOM FROM DICT (PUBLIC API) ===")
        
        timestamp = datetime.now(timezone.utc).strftime('%H%M%S')
        
        # Create BOM data as dicts, then convert to BomItem objects
        bom_data = [
            BomItem(
                component_ref=f"D{timestamp}1",
                part_number="LED-RED",
                description="Red LED",
                quantity=2
            ),
            BomItem(
                component_ref=f"D{timestamp}2",
                part_number="LED-GREEN",
                description="Green LED",
                quantity=2
            )
        ]
        
        print(f"Uploading BOM to {test_product_pn}/1.0:")
        for item in bom_data:
            print(f"  - {item.component_ref}: {item.part_number}")
        
        # Use public API (WSBF XML format)
        result = wats_client.product.update_bom(
            test_product_pn, "1.0", bom_data
        )
        
        print(f"Upload result: {result}")
        print("============================\n")
        
        assert result is True


# =============================================================================
# Box Build Template Tests
# =============================================================================

class TestBoxBuildTemplate:
    """Test Box Build template management.
    
    ⚠️ INTERNAL API - Uses internal Product API endpoints.
    Box Build templates define which subunits are required to assemble a product.
    
    Note: Tests that modify box builds (add/remove subunits) require the 
    Production module to be enabled and are marked to skip if not available.
    """
    
    @pytest.fixture
    def parent_product_pn(self) -> str:
        """Parent product for box build testing"""
        return "PYWATS-TEST-001"
    
    @pytest.fixture
    def subunit_product_pn(self) -> str:
        """Subunit product for box build testing"""
        return "PYWATS-SUB-001"
    
    def test_get_box_build_template(
        self, wats_client: Any, parent_product_pn: str
    ) -> None:
        """Test getting a box build template"""
        print("\n=== GET BOX BUILD TEMPLATE ===")
        
        template = wats_client.product_internal.get_box_build(parent_product_pn, "1.0")
        
        print(f"Box Build Template: {template.parent_part_number}/{template.parent_revision}")
        print(f"Parent Revision ID: {template.parent_revision_id}")
        print(f"Subunits: {len(template.subunits)}")
        for sub in template.subunits:
            mask = f" [mask: {sub.revision_mask}]" if sub.revision_mask else ""
            print(f"  - {sub.child_part_number}/{sub.child_revision} x{sub.quantity}{mask}")
        print("==============================\n")
        
        assert template is not None
        assert template.parent_part_number == parent_product_pn
        assert template.parent_revision == "1.0"
    
    def test_get_required_parts(
        self, wats_client: Any, parent_product_pn: str
    ) -> None:
        """Test getting required parts summary"""
        print("\n=== GET REQUIRED PARTS ===")
        
        template = wats_client.product_internal.get_box_build(parent_product_pn, "1.0")
        parts = template.get_required_parts()
        
        print(f"Required parts for {parent_product_pn}/1.0:")
        for part in parts:
            print(f"  - {part['part_number']}/{part['default_revision']} x{part['quantity']}")
            if part['revision_mask']:
                print(f"    Accepts revisions: {part['revision_mask']}")
        print("==========================\n")
        
        assert isinstance(parts, list)
    
    @pytest.mark.skip(reason="Requires Production module - saves box build relations")
    def test_add_subunit_to_box_build(
        self, 
        wats_client: Any, 
        parent_product_pn: str,
        subunit_product_pn: str
    ) -> None:
        """Test adding a subunit to box build template"""
        print("\n=== ADD SUBUNIT TO BOX BUILD ===")
        
        template = wats_client.product_internal.get_box_build(parent_product_pn, "1.0")
        initial_count = len(template.subunits)
        
        print(f"Initial subunits: {initial_count}")
        print(f"Adding: {subunit_product_pn}/1.0 x2 with mask '1.%'")
        
        # Add subunit with revision mask
        template.add_subunit(
            subunit_product_pn, 
            "1.0", 
            quantity=2, 
            revision_mask="1.%"
        )
        
        print(f"After add (unsaved): {len(template.subunits)} subunits")
        print(f"Has pending changes: {template.has_pending_changes}")
        print(template)
        
        # Save changes
        print("\nSaving changes...")
        template.save()
        
        print(f"After save: {len(template.subunits)} subunits")
        print(f"Has pending changes: {template.has_pending_changes}")
        print("================================\n")
        
        assert len(template.subunits) >= initial_count
    
    @pytest.mark.skip(reason="Requires Production module - saves box build relations")
    def test_validate_subunit_revision(
        self, 
        wats_client: Any, 
        parent_product_pn: str,
        subunit_product_pn: str
    ) -> None:
        """Test validating subunit revisions against revision mask"""
        print("\n=== VALIDATE SUBUNIT REVISION ===")
        
        # First add a subunit with a revision mask
        template = wats_client.product_internal.get_box_build(parent_product_pn, "1.0")
        
        # Try to add a subunit with mask (may already exist)
        try:
            template.add_subunit(
                subunit_product_pn, 
                "1.0", 
                quantity=1, 
                revision_mask="1.%,2.0"
            )
            template.save()
        except ValueError:
            pass  # Subunit might already exist
        
        # Reload to get current state
        template.reload()
        
        print(f"Validating revisions for {subunit_product_pn}:")
        print(f"  1.0 valid: {template.validate_subunit(subunit_product_pn, '1.0')}")
        print(f"  1.5 valid: {template.validate_subunit(subunit_product_pn, '1.5')}")
        print(f"  2.0 valid: {template.validate_subunit(subunit_product_pn, '2.0')}")
        print(f"  3.0 valid: {template.validate_subunit(subunit_product_pn, '3.0')}")
        print("=================================\n")
        
        # At minimum, 1.0 should be valid (it's the default)
        # The full validation depends on what mask was saved
    
    @pytest.mark.skip(reason="Requires Production module - saves box build relations")
    def test_box_build_context_manager(
        self, 
        wats_client: Any, 
        parent_product_pn: str,
        subunit_product_pn: str
    ) -> None:
        """Test using box build template with context manager"""
        print("\n=== BOX BUILD CONTEXT MANAGER ===")
        
        timestamp = datetime.now(timezone.utc).strftime('%H%M%S')
        
        # Use context manager for auto-save
        with wats_client.product_internal.get_box_build(parent_product_pn, "1.0") as bb:
            print(f"Inside context: {bb.parent_part_number}/{bb.parent_revision}")
            print(f"Current subunits: {len(bb.subunits)}")
            
            # Make a change (update quantity if exists)
            if bb.subunits:
                sub = bb.subunits[0]
                print(f"Updating {sub.child_part_number} quantity to 3")
                bb.update_subunit(sub.child_part_number, sub.child_revision, quantity=3)
            
            print(f"Has pending changes: {bb.has_pending_changes}")
        
        # Changes should be auto-saved after context exit
        print("Exited context (auto-saved)")
        print("=================================\n")
    
    @pytest.mark.skip(reason="Requires Production module - saves box build relations")
    def test_remove_subunit_from_box_build(
        self, 
        wats_client: Any, 
        parent_product_pn: str,
        subunit_product_pn: str
    ) -> None:
        """Test removing a subunit from box build template"""
        print("\n=== REMOVE SUBUNIT FROM BOX BUILD ===")
        
        template = wats_client.product_internal.get_box_build(parent_product_pn, "1.0")
        
        print(f"Current subunits: {len(template.subunits)}")
        
        # Find a subunit to remove
        if template.subunits:
            sub = template.subunits[0]
            print(f"Removing: {sub.child_part_number}/{sub.child_revision}")
            
            template.remove_subunit(sub.child_part_number, sub.child_revision)
            
            print(f"After remove (unsaved): {len(template.subunits)} subunits")
            print(f"Has pending changes: {template.has_pending_changes}")
            
            # Save changes
            template.save()
            print(f"After save: {len(template.subunits)} subunits")
        else:
            print("No subunits to remove")
        
        print("=====================================\n")


# =============================================================================
# Revision Mask Model Tests (Unit Tests - No Server)
# =============================================================================

class TestRevisionMaskMatching:
    """Test revision mask matching logic (no server required)"""
    
    def test_exact_match(self) -> None:
        """Test exact revision matching"""
        rel = ProductRevisionRelation(
            parent_product_revision_id=uuid4(),
            child_product_revision_id=uuid4(),
            child_part_number="TEST-001",
            child_revision="1.0",
            revision_mask="1.0"
        )
        
        assert rel.matches_revision("1.0") is True
        assert rel.matches_revision("1.1") is False
        assert rel.matches_revision("2.0") is False
    
    def test_wildcard_match(self) -> None:
        """Test wildcard revision matching"""
        rel = ProductRevisionRelation(
            parent_product_revision_id=uuid4(),
            child_product_revision_id=uuid4(),
            child_part_number="TEST-001",
            child_revision="2.0",
            revision_mask="2.%"
        )
        
        assert rel.matches_revision("2.0") is True
        assert rel.matches_revision("2.1") is True
        assert rel.matches_revision("2.5a") is True
        assert rel.matches_revision("3.0") is False
        assert rel.matches_revision("12.0") is False
    
    def test_multiple_patterns(self) -> None:
        """Test comma-separated revision patterns"""
        rel = ProductRevisionRelation(
            parent_product_revision_id=uuid4(),
            child_product_revision_id=uuid4(),
            child_part_number="TEST-001",
            child_revision="A",
            revision_mask="A, B, C.%"
        )
        
        assert rel.matches_revision("A") is True
        assert rel.matches_revision("B") is True
        assert rel.matches_revision("C.1") is True
        assert rel.matches_revision("C.99") is True
        assert rel.matches_revision("D") is False
    
    def test_no_mask_uses_exact_revision(self) -> None:
        """Test that no mask falls back to exact child_revision match"""
        rel = ProductRevisionRelation(
            parent_product_revision_id=uuid4(),
            child_product_revision_id=uuid4(),
            child_part_number="TEST-001",
            child_revision="1.0",
            revision_mask=None
        )
        
        assert rel.matches_revision("1.0") is True
        assert rel.matches_revision("1.1") is False
    
    def test_complex_version_patterns(self) -> None:
        """Test complex version patterns"""
        rel = ProductRevisionRelation(
            parent_product_revision_id=uuid4(),
            child_product_revision_id=uuid4(),
            child_part_number="FIRMWARE",
            child_revision="v1.0.0",
            revision_mask="v1.%, v2.0.%, v2.1.0"
        )
        
        assert rel.matches_revision("v1.0.0") is True
        assert rel.matches_revision("v1.5.3") is True
        assert rel.matches_revision("v2.0.1") is True
        assert rel.matches_revision("v2.0.99") is True
        assert rel.matches_revision("v2.1.0") is True
        assert rel.matches_revision("v2.1.1") is False
        assert rel.matches_revision("v3.0.0") is False


class TestBomItemModel:
    """Test BomItem model creation (no server required)"""
    
    def test_create_bom_item(self) -> None:
        """Test creating a BomItem model"""
        item = BomItem(
            component_ref="R1",
            part_number="RES-10K",
            description="10K Resistor",
            quantity=5,
            manufacturer="Vishay"
        )
        
        assert item.component_ref == "R1"
        assert item.part_number == "RES-10K"
        assert item.quantity == 5
        assert item.manufacturer == "Vishay"
    
    def test_bom_item_serialization(self) -> None:
        """Test BomItem serialization to dict"""
        item = BomItem(
            component_ref="C1",
            part_number="CAP-100NF",
            quantity=3
        )
        
        data = item.model_dump(by_alias=True, exclude_none=True)
        
        assert data["componentRef"] == "C1"
        assert data["partNumber"] == "CAP-100NF"
        assert data["quantity"] == 3
