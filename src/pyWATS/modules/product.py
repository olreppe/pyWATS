"""
Product module for WATS API.

This module provides functionality for managing products, product configurations,
and product-related operations in the WATS system.
"""

from typing import List, Optional, Dict, Any
from .base import BaseModule
from ..rest_api.public.api.product.product_public_get_products import sync as get_products_sync
from ..rest_api.public.api.product.product_public_get_product import sync as get_product_sync
from ..exceptions import WATSException, WATSNotFoundError


class ProductModule(BaseModule):
    """
    Product management module.
    
    Provides methods for:
    - Retrieving product information
    - Managing product configurations
    - Accessing product definitions and metadata
    """
    
    def get_all(self, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all products with optional pagination.
        
        Args:
            limit: Maximum number of products to return
            offset: Number of products to skip
            
        Returns:
            List of product dictionaries
            
        Raises:
            WATSException: If the API call fails
        """
        try:
            response = get_products_sync(client=self._http_client)
            products = self._extract_data(response)
            
            # Apply pagination if specified
            if offset is not None or limit is not None:
                start = offset or 0
                end = start + limit if limit is not None else None
                products = products[start:end]
            
            return [product.to_dict() if hasattr(product, 'to_dict') else product for product in products]
        except Exception as e:
            self._handle_api_error(e, "Get all products")
            raise WATSException(f"Failed to get products: {str(e)}")
    
    def get_count(self) -> int:
        """
        Get the total count of products.
        
        Returns:
            Total number of products
            
        Raises:
            WATSException: If the API call fails
        """
        try:
            products = self.get_all()
            return len(products)
        except Exception as e:
            raise WATSException(f"Failed to get product count: {str(e)}")
    
    def get_by_id(self, product_id: str) -> Dict[str, Any]:
        """
        Get a specific product by ID/part number.
        
        Args:
            product_id: The ID or part number of the product to retrieve
            
        Returns:
            Product data dictionary
            
        Raises:
            WATSException: If the product ID is invalid
            WATSNotFoundError: If the product is not found
        """
        self._validate_id(product_id, "product")
        
        try:
            response = get_product_sync(
                client=self._http_client,
                part_number=product_id
            )
            product = self._extract_data(response)
            return product.to_dict() if hasattr(product, 'to_dict') else product
        except Exception as e:
            if "404" in str(e) or "not found" in str(e).lower():
                raise WATSNotFoundError(f"Product with ID '{product_id}' not found")
            self._handle_api_error(e, f"Get product {product_id}")
            raise WATSException(f"Failed to get product {product_id}: {str(e)}")
    
    def get_definition(self, product_id: str) -> Dict[str, Any]:
        """
        Get the definition/configuration of a specific product.
        
        Args:
            product_id: The ID of the product
            
        Returns:
            Product definition data
            
        Raises:
            WATSException: If the product ID is invalid
            WATSNotFoundError: If the product is not found
        """
        return self.get_by_id(product_id)
    
    def search(self, name: Optional[str] = None, **filters) -> List[Dict[str, Any]]:
        """
        Search for products with optional filters.
        
        Args:
            name: Product name to search for
            **filters: Additional search filters
            
        Returns:
            List of matching products
            
        Raises:
            WATSException: If the search fails
        """
        try:
            all_products = self.get_all()
            
            if not name and not filters:
                return all_products
            
            filtered_products = []
            for product in all_products:
                match = True
                
                # Filter by name if provided
                if name and isinstance(product, dict):
                    product_name = product.get('name', '').lower()
                    if name.lower() not in product_name:
                        match = False
                
                # Apply additional filters
                for key, value in filters.items():
                    if isinstance(product, dict) and key in product:
                        if product[key] != value:
                            match = False
                            break
                
                if match:
                    filtered_products.append(product)
            
            return filtered_products
            
        except Exception as e:
            raise WATSException(f"Failed to search products: {str(e)}")
    
    def exists(self, product_id: str) -> bool:
        """
        Check if a product exists.
        
        Args:
            product_id: The ID of the product to check
            
        Returns:
            True if the product exists, False otherwise
        """
        try:
            self.get_by_id(product_id)
            return True
        except WATSNotFoundError:
            return False
        except Exception:
            # For other errors, we can't determine existence
            return False