"""
Tests for the Product module.
"""
import pytest
from unittest.mock import Mock, MagicMock, patch

from pyWATS.modules import product
from pyWATS.modules.product import ProductModule, set_return_none_on_error


class TestProductModule:
    """Test cases for the Product module."""
    
    @pytest.fixture
    def mock_http_client(self):
        """Create a mock HTTP client for testing."""
        client = Mock()
        return client
    
    @pytest.fixture
    def product_module(self, mock_http_client):
        """Create a ProductModule instance with a mock client."""
        module = ProductModule(mock_http_client)
        return module
    
    @pytest.fixture(autouse=True)
    def reset_error_handling(self):
        """Reset error handling setting before each test."""
        set_return_none_on_error(False)
        yield
        set_return_none_on_error(False)
    
    # Tests for get_product
    def test_get_product_success(self, product_module):
        """Test get_product returns a product object when found."""
        # Mock product object with attributes
        mock_product = Mock()
        mock_product.part_number = "ABC123"
        mock_product.name = "Test Product"
        mock_product.product_id = 1
        
        # Mock the sync function - without revision uses get_product_sync
        with patch('pyWATS.modules.product.get_product_sync', return_value=mock_product):
            result = product_module.get_product("ABC123")
            
            assert result == mock_product
            assert result.part_number == "ABC123"
    
    def test_get_product_not_found_raises_exception(self, product_module):
        """Test get_product raises exception when product not found."""
        with patch('pyWATS.modules.product.get_product_sync', return_value=None):
            with pytest.raises(Exception):
                product_module.get_product("NOTFOUND")
    
    def test_get_product_not_found_returns_none(self, product_module):
        """Test get_product returns None when RETURN_NONE_ON_ERROR is True."""
        set_return_none_on_error(True)
        
        with patch('pyWATS.modules.product.get_product_sync', return_value=None):
            result = product_module.get_product("NOTFOUND")
            assert result is None
    
    # Tests for get_product_revision
    def test_get_product_revision_success(self, product_module):
        """Test get_product_revision returns a revision object when found."""
        mock_revision = Mock()
        mock_revision.part_number = "ABC123"
        mock_revision.revision = "A"
        mock_revision.name = "Test Product Rev A"
        
        with patch('pyWATS.modules.product.get_product_revision_sync', return_value=mock_revision):
            result = product_module.get_product_revision("ABC123", "A")
            
            assert result == mock_revision
            assert result.revision == "A"
    
    def test_get_product_revision_not_found_raises_exception(self, product_module):
        """Test get_product_revision raises exception when revision not found."""
        with patch('pyWATS.modules.product.get_product_revision_sync', return_value=None):
            with pytest.raises(Exception):
                product_module.get_product_revision("ABC123", "Z")
    
    def test_get_product_revision_not_found_returns_none(self, product_module):
        """Test get_product_revision returns None when RETURN_NONE_ON_ERROR is True."""
        set_return_none_on_error(True)
        
        with patch('pyWATS.modules.product.get_product_revision_sync', return_value=None):
            result = product_module.get_product_revision("ABC123", "Z")
            assert result is None
    
    # Tests for get_products
    def test_get_products_no_filter(self, product_module):
        """Test get_products returns all product objects when no filter is provided."""
        mock_product1 = Mock()
        mock_product1.part_number = "ABC123"
        mock_product1.name = "Product 1"
        
        mock_product2 = Mock()
        mock_product2.part_number = "DEF456"
        mock_product2.name = "Product 2"
        
        expected_products = [mock_product1, mock_product2]
        
        with patch('pyWATS.modules.product.get_products_sync', return_value=expected_products):
            result = product_module.get_products()
            
            assert result == expected_products
            assert len(result) == 2
    
    def test_get_products_with_filter(self, product_module):
        """Test get_products applies filter correctly."""
        mock_product1 = Mock()
        mock_product1.part_number = "ABC123"
        mock_product1.name = "Product 1"
        
        mock_product2 = Mock()
        mock_product2.part_number = "DEF456"
        mock_product2.name = "Product 2"
        
        all_products = [mock_product1, mock_product2]
        
        with patch('pyWATS.modules.product.get_products_sync', return_value=all_products):
            result = product_module.get_products(filter="part_number eq 'ABC123'")
            
            # Should filter to only ABC123
            assert len(result) == 1
            assert result[0].part_number == "ABC123"
    
    def test_get_products_error_raises_exception(self, product_module):
        """Test get_products raises exception on error."""
        with patch('pyWATS.modules.product.get_products_sync', side_effect=Exception("API Error")):
            with pytest.raises(Exception, match="API Error"):
                product_module.get_products()
    
    def test_get_products_error_returns_empty_list(self, product_module):
        """Test get_products returns empty list when RETURN_NONE_ON_ERROR is True."""
        set_return_none_on_error(True)
        
        with patch('pyWATS.modules.product.get_products_sync', side_effect=Exception("API Error")):
            result = product_module.get_products()
            assert result == []
    
    def test_get_products_none_response(self, product_module):
        """Test get_products handles None response."""
        with patch('pyWATS.modules.product.get_products_sync', return_value=None):
            result = product_module.get_products()
            assert result == []
    
    # Tests for error handling setting
    def test_set_return_none_on_error(self):
        """Test the set_return_none_on_error function."""
        # Test setting to True
        set_return_none_on_error(True)
        assert product.RETURN_NONE_ON_ERROR is True
        
        # Test setting to False
        set_return_none_on_error(False)
        assert product.RETURN_NONE_ON_ERROR is False