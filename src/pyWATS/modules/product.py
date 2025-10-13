"""
Product module for WATS API.

This module provides functionality for managing products, product configurations,
and product-related operations in the WATS system.
"""

from typing import List, Optional, Dict, Any, Tuple, cast
import io
from .base import BaseModule
from ..rest_api.public.api.product.product_public_get_products import sync as get_products_sync
from ..rest_api.public.api.product.product_public_get_product import sync as get_product_sync
from ..rest_api.public.client import Client
from ..rest_api.public.models.virinco_wats_web_dashboard_models_mes_product_public_product import (
    VirincoWATSWebDashboardModelsMesProductPublicProduct
)
from ..rest_api.public.models.virinco_wats_web_dashboard_models_mes_product_product_view import (
    VirincoWATSWebDashboardModelsMesProductProductView
)
from ..exceptions import WATSException, WATSNotFoundError


class Process:
    """Process data model."""
    def __init__(self, name: str, **kwargs):
        self.name = name
        # Add other process properties as needed


class ProductInfo:
    """Product information with hierarchy and tag support."""
    
    def __init__(self, part_number: str, revision: str = "", **kwargs):
        self.part_number = part_number
        self.revision = revision
        self._parent = kwargs.get('parent')
        self._children = kwargs.get('children', [])
        self._tags = kwargs.get('tags', {})
        self._xml_data = kwargs.get('xml_data', "")

    def has_parent(self) -> bool:
        """Check if product has a parent."""
        return self._parent is not None

    def get_parent(self) -> 'ProductInfo':
        """Get the parent product info."""
        if self._parent is None:
            raise WATSException("Product has no parent")
        return self._parent

    def get_child_count(self) -> int:
        """Get the number of child products."""
        return len(self._children)

    def get_child(self, index: int) -> 'ProductInfo':
        """
        Get a child product by index.
        
        Args:
            index: Index of the child
            
        Returns:
            ProductInfo object for the child
        """
        if index < 0 or index >= len(self._children):
            raise WATSException(f"Child index {index} out of range")
        return self._children[index]

    def get_children(self) -> List['ProductInfo']:
        """Get all child products."""
        return self._children.copy()

    def get_tag_value(self, tag: str, data_type: int) -> str:
        """
        Get a tag value with specified data type.
        
        Args:
            tag: Tag name
            data_type: Data type identifier
            
        Returns:
            Tag value as string
        """
        tag_value = self._tags.get(tag, "")
        return str(tag_value)

    def get_info(self, xpath: str) -> str:
        """
        Get product information using XPath.
        
        Args:
            xpath: XPath expression
            
        Returns:
            Information value
        """
        # TODO: Implement actual XPath parsing on self._xml_data
        # For now, return empty string as placeholder
        return ""


class ProductModule(BaseModule):
    """
    Product management module.
    
    Provides methods for:
    - Retrieving product information
    - Managing product configurations
    - Accessing product definitions and metadata
    - Product identification and selection
    """

    def is_connected(self) -> bool:
        """Check if product module is connected."""
        raise NotImplementedError("Product.is_connected not implemented")

    @staticmethod
    def deserialize_from_stream(stream: io.IOBase) -> Any:
        """
        Deserialize product data from a stream.
        
        Args:
            stream: Input stream
            
        Returns:
            Deserialized object
        """
        raise NotImplementedError("Product.deserialize_from_stream not implemented")

    def get_product_info(self, part_number: str, revision: str = "") -> ProductInfo:
        """
        Get product information.
        
        Args:
            part_number: Part number of the product
            revision: Revision of the product (optional)
            
        Returns:
            ProductInfo object
            
        Raises:
            WATSNotFoundError: If the product is not found
            WATSException: If the operation fails
        """
        self._validate_id(part_number, "part_number")
        
        try:
            # Call the REST API to get product data
            response = get_product_sync(
                part_number=part_number,
                client=cast(Client, self.http_client)
            )
            
            if response is None:
                raise WATSNotFoundError(f"Product with part number '{part_number}' not found")
            
            # Convert the REST API response to ProductInfo
            product_info = ProductInfo(
                part_number=response.part_number or part_number,
                revision=revision,  # REST API doesn't return revision directly
                xml_data=response.xml_data or ""
            )
            
            return product_info
            
        except Exception as e:
            if isinstance(e, (WATSNotFoundError, WATSException)):
                raise
            if "404" in str(e) or "not found" in str(e).lower():
                raise WATSNotFoundError(f"Product with part number '{part_number}' not found")
            raise WATSException(f"Failed to get product info for {part_number}: {str(e)}")

    def identify_product(self, filter_str: str, top_count: int, free_partnumber: bool,
                        include_revision: bool, include_serial_number: bool,
                        custom_text: str = "", always_on_top: bool = True) -> Tuple[str, str, str, Process, bool]:
        """
        Identify a product through user interface.
        
        Args:
            filter_str: Filter string
            top_count: Maximum number of results
            free_partnumber: Allow free part number entry
            include_revision: Include revision in selection
            include_serial_number: Include serial number in selection
            custom_text: Custom text for dialog
            always_on_top: Keep dialog always on top
            
        Returns:
            Tuple of (selected_serial_number, selected_part_number, selected_revision, selected_test_operation, continue)
        """
        raise NotImplementedError("Product.identify_product not implemented")

    def get_product(self, filter_str: str, top_count: int, include_non_serial: bool,
                   include_revision: bool) -> List[VirincoWATSWebDashboardModelsMesProductProductView]:
        """
        Get products with filtering options.
        
        Args:
            filter_str: Filter string
            top_count: Maximum number of results
            include_non_serial: Include non-serialized products
            include_revision: Include revision information
            
        Returns:
            List of product model objects
            
        Raises:
            WATSException: If the operation fails
        """
        try:
            # Call the REST API to get all products
            # Note: The current generated client doesn't support filtering parameters
            # This would need to be enhanced to support the specific filtering
            response = get_products_sync(client=cast(Client, self.http_client))
            
            if response is None:
                return []
            
            # TODO: Implement proper filtering based on parameters
            # For now, return the response limited to top_count
            products = response[:top_count] if top_count > 0 else response
            
            return products
            
        except Exception as e:
            raise WATSException(f"Failed to get products: {str(e)}")
    
    # Legacy methods for backward compatibility
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
            response = get_products_sync(client=cast(Client, self.http_client))
            products = response or []
            
            # Apply pagination if specified
            if offset is not None or limit is not None:
                start = offset or 0
                end = start + limit if limit is not None else None
                products = products[start:end]
            
            return [product.to_dict() for product in products]
        except Exception as e:
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
                client=cast(Client, self.http_client),
                part_number=product_id
            )
            if response is None:
                raise WATSNotFoundError(f"Product with ID '{product_id}' not found")
            return response.to_dict()
        except Exception as e:
            if isinstance(e, (WATSNotFoundError, WATSException)):
                raise
            if "404" in str(e) or "not found" in str(e).lower():
                raise WATSNotFoundError(f"Product with ID '{product_id}' not found")
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