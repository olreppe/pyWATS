"""
Tests for product module - product definitions and revisions

These tests make actual API calls to the WATS server.
"""
from typing import Any, Dict
from datetime import datetime, timezone
import pytest
from pywats.domains.product import Product, ProductRevision


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
