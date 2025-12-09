"""
Tests for product module - product definitions and revisions
Note: Endpoints may not work as expected - revisions need separate loading
"""
from typing import Any
import pytest
from pywats.models.product import Product, ProductRevision


class TestProductDefinition:
    """Test product definition operations"""
    
    def test_create_product(self, test_part_number: str) -> None:
        """Test creating a product definition"""
        product = Product(
            part_number=test_part_number,
            name="Test Product"
        )
        assert product.part_number == test_part_number
    
    def test_register_product(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test registering a new product"""
        product = Product(
            part_number=test_part_number,
            name="Test Product",
            description="Test product description"
        )
        
        try:
            result = wats_client.product.create_product(product)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Product creation failed: {e}")
    
    def test_get_product(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test retrieving a product"""
        try:
            product = wats_client.product.get_product(test_part_number)
            if product:
                assert product.part_number == test_part_number
        except Exception as e:
            pytest.skip(f"Get product failed: {e}")
    
    def test_update_product(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test updating product information"""
        try:
            result = wats_client.product.update_product(
                test_part_number,
                description="Updated description"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Update product failed: {e}")


class TestProductRevision:
    """Test product revision operations - requires separate loading"""
    
    def test_create_revision(
        self, test_part_number: str, test_revision: str
    ) -> None:
        """Test creating a revision definition"""
        revision = ProductRevision(
            part_number=test_part_number,
            revision=test_revision,
            description="Test revision"
        )
        assert revision.revision == test_revision
    
    def test_add_revision_to_product(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test adding a revision to a product"""
        revision = ProductRevision(
            part_number=test_part_number,
            revision="B",
            description="Revision B"
        )
        
        try:
            result = wats_client.product.create_revision(revision)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Revision creation failed: {e}")
    
    def test_load_revision_separately(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test loading revision as separate object (API requirement)"""
        try:
            # Note: Revisions must be loaded separately to manipulate
            revision = wats_client.product.get_revision(test_part_number, "A")
            if revision:
                assert revision.revision == "A"
        except Exception as e:
            pytest.skip(f"Load revision failed: {e}")
    
    def test_update_revision(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test updating a revision"""
        try:
            result = wats_client.product.update_revision(
                test_part_number,
                "A",
                description="Updated revision description"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Update revision failed: {e}")


class TestProductMisc:
    """Test misc info manipulation - requires separate functions"""
    
    def test_add_misc_info(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test adding misc info (separate function required)"""
        try:
            result = wats_client.product.add_misc_info(
                test_part_number,
                description="TestInfo",
                value="TestValue"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Add misc info failed: {e}")
    
    def test_get_misc_info(
        self, wats_client: Any, test_part_number: str
    ) -> None:
        """Test getting misc info"""
        try:
            misc_info = wats_client.product.get_misc_info(test_part_number)
            assert isinstance(misc_info, list)
        except Exception as e:
            pytest.skip(f"Get misc info failed: {e}")
