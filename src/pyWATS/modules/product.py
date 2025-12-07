"""
Product module for WATS API.

This module provides functionality for managing products, product configurations,
and product-related operations in the WATS system.
"""

from typing import List, Optional, Dict, Any, Tuple, Union, cast
import io
from .base import BaseModule
from ..rest_api.public.api.product.product_public_get_products import sync as get_products_sync
from ..rest_api.public.api.product.product_public_get_product import sync as get_product_sync
from ..rest_api.public.api.product.product_public_get_product_revision import sync as get_product_revision_sync
from ..rest_api.public.api.product.product_public_put_product import sync as put_product_sync
from ..rest_api.public.api.product.product_public_put_product_revision import sync as put_product_revision_sync
from ..rest_api.public.client import Client
from ..rest_api.public.models.virinco_wats_web_dashboard_models_mes_product_public_product import (
    VirincoWATSWebDashboardModelsMesProductPublicProduct as Product
)
from ..rest_api.public.models.virinco_wats_web_dashboard_models_mes_product_product_view import (
    VirincoWATSWebDashboardModelsMesProductProductView
)
from ..rest_api.public.models.virinco_wats_web_dashboard_models_mes_product_public_product_revision import (
    VirincoWATSWebDashboardModelsMesProductPublicProductRevision as Revision
)
from ..exceptions import WATSException, WATSNotFoundError

# Module-level setting for error handling
RETURN_NONE_ON_ERROR = False


def set_return_none_on_error(value: bool):
    """
    Configure whether functions should return None instead of raising exceptions.
    
    Args:
        value: If True, functions return None on errors. If False, exceptions are raised.
    """
    global RETURN_NONE_ON_ERROR
    RETURN_NONE_ON_ERROR = value


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

    def get_product(self, part_number: str, revision: Optional[str] = None) -> Optional[Union[Product, Revision]]:
        """
        Get a product by part number, optionally with a specific revision.
        
        - Without revision: Returns full Product model with all revisions (from /api/Product/{partNumber})
        - With revision: Returns specific ProductRevision model (from /api/Product/{partNumber}/{revision})
        
        Args:
            part_number: The product part number
            revision: Optional product revision. If provided, returns ProductRevision instead of Product.
            
        Returns:
            Product object (without revision) or ProductRevision object (with revision)
            Returns None if RETURN_NONE_ON_ERROR is True and product not found
            
        Raises:
            WATSException: If product not found and RETURN_NONE_ON_ERROR is False
        """
        try:
            if revision:
                # Get specific revision: /api/Product/{partNumber}/{revision}
                # Returns VirincoWATSWebDashboardModelsMesProductPublicProductRevision
                response = get_product_revision_sync(
                    part_number=part_number,
                    revision=revision,
                    client=cast(Client, self.http_client)
                )
            else:
                # Get full product: /api/Product/{partNumber}
                # Returns VirincoWATSWebDashboardModelsMesProductPublicProduct with all revisions
                response = get_product_sync(
                    part_number=part_number,
                    client=cast(Client, self.http_client)
                )
            
            if response is None:
                if RETURN_NONE_ON_ERROR:
                    return None
                error_msg = f"Product '{part_number}/{revision}' not found" if revision else f"Product '{part_number}' not found"
                raise WATSNotFoundError(error_msg)
            
            return response
            
        except Exception as e:
            if RETURN_NONE_ON_ERROR:
                return None
            if isinstance(e, (WATSNotFoundError, WATSException)):
                raise
            raise WATSException(f"Failed to get product: {str(e)}")
    
    def get_product_revision(self, part_number: str, revision: str) -> Optional[Revision]:
        """
        Get a single product revision by part number and revision.
        
        Note: This is a convenience method. You can also use get_product(part_number, revision).
        
        Args:
            part_number: The product part number
            revision: The product revision
            
        Returns:
            Product revision object or None if RETURN_NONE_ON_ERROR is True and not found
            
        Raises:
            WATSException: If revision not found and RETURN_NONE_ON_ERROR is False
        """
        # Delegate to get_product with revision parameter
        # When revision is provided, get_product returns VirincoWATSWebDashboardModelsMesProductPublicProductRevision
        return cast(Optional[Revision], 
                   self.get_product(part_number=part_number, revision=revision))
    
    def get_products(self, filter: Optional[str] = None) -> List[VirincoWATSWebDashboardModelsMesProductProductView]:
        """
        Get a list of products with optional filtering.
        
        Args:
            filter: OData filter string (e.g., "partNumber eq 'ABC123'")
            
        Returns:
            List of product objects or empty list if RETURN_NONE_ON_ERROR is True and error occurs
            
        Raises:
            WATSException: If error occurs and RETURN_NONE_ON_ERROR is False
        """
        try:
            # TODO: Add support for OData filter parameter when REST API supports it
            # For now, the API doesn't accept filter parameters directly
            response = get_products_sync(client=cast(Client, self.http_client))
            
            if response is None:
                return []
            
            products = response
            
            # Apply client-side filtering if filter is provided
            # This is a temporary solution until API supports filtering
            if filter:
                # Basic OData filter parsing (e.g., "partNumber eq 'ABC123'")
                products = self._apply_filter_objects(products, filter)
            
            return products
            
        except Exception as e:
            if RETURN_NONE_ON_ERROR:
                return []
            raise WATSException(f"Failed to get products: {str(e)}")
    
    def _apply_filter_objects(self, products: List[VirincoWATSWebDashboardModelsMesProductProductView], filter_str: str) -> List[VirincoWATSWebDashboardModelsMesProductProductView]:
        """
        Apply OData-style filter to products list (client-side filtering).
        
        Args:
            products: List of product objects
            filter_str: OData filter string
            
        Returns:
            Filtered list of product objects
        """
        # Simple parser for basic OData filters like "field eq 'value'"
        try:
            if ' eq ' in filter_str:
                parts = filter_str.split(' eq ')
                if len(parts) == 2:
                    field = parts[0].strip()
                    value = parts[1].strip().strip("'\"")
                    # Use getattr to get object attributes
                    return [p for p in products if str(getattr(p, field, '')).lower() == value.lower()]
        except Exception:
            pass  # If filtering fails, return all products
        return products
    
    def update_product(self, product: Product) -> Optional[Product]:
        """
        Update an existing product or create a new one.
        
        To update an existing product, ensure the product object has a valid product_id.
        To create a new product, leave product_id as None or UNSET.
        
        Args:
            product: The product object to update or create
            
        Returns:
            Updated/created product object or None if RETURN_NONE_ON_ERROR is True and error occurs
            
        Raises:
            WATSException: If the update fails and RETURN_NONE_ON_ERROR is False
        """
        try:
            # Use sync_detailed to get full response info for debugging
            from ..rest_api.public.api.product.product_public_put_product import sync_detailed as put_product_detailed
            
            detailed_response = put_product_detailed(
                body=product,
                client=cast(Client, self.http_client)
            )
            
            # Check if the request succeeded
            if detailed_response.status_code != 200:
                error_msg = f"Failed to update product: Server returned status {detailed_response.status_code}"
                if detailed_response.content:
                    error_msg += f" - {detailed_response.content.decode('utf-8', errors='ignore')}"
                if RETURN_NONE_ON_ERROR:
                    return None
                raise WATSException(error_msg)
            
            response = detailed_response.parsed
            
            if response is None:
                if RETURN_NONE_ON_ERROR:
                    return None
                raise WATSException("Failed to update product: No response from server")
            
            return response
            
        except Exception as e:
            if RETURN_NONE_ON_ERROR:
                return None
            if isinstance(e, WATSException):
                raise
            raise WATSException(f"Failed to update product: {str(e)}")
    
    def update_product_revision(self, product_revision: Revision) -> Optional[Revision]:
        """
        Update an existing product revision or create a new one.
        
        To update an existing revision, ensure the product_revision object has a valid product_revision_id.
        To create a new revision, leave product_revision_id as None or UNSET (but product_id and revision must be set).
        
        Args:
            product_revision: The product revision object to update or create
            
        Returns:
            Updated/created product revision object or None if RETURN_NONE_ON_ERROR is True and error occurs
            
        Raises:
            WATSException: If the update fails and RETURN_NONE_ON_ERROR is False
        """
        try:
            # Use sync_detailed to get full response info for debugging
            from ..rest_api.public.api.product.product_public_put_product_revision import sync_detailed as put_product_revision_detailed
            
            detailed_response = put_product_revision_detailed(
                body=product_revision,
                client=cast(Client, self.http_client)
            )
            
            # Check if the request succeeded
            if detailed_response.status_code != 200:
                error_msg = f"Failed to update product revision: Server returned status {detailed_response.status_code}"
                if detailed_response.content:
                    error_msg += f" - {detailed_response.content.decode('utf-8', errors='ignore')}"
                if RETURN_NONE_ON_ERROR:
                    return None
                raise WATSException(error_msg)
            
            response = detailed_response.parsed
            
            if response is None:
                if RETURN_NONE_ON_ERROR:
                    return None
                raise WATSException("Failed to update product revision: No response from server")
            
            return response
            
        except Exception as e:
            if RETURN_NONE_ON_ERROR:
                return None
            if isinstance(e, WATSException):
                raise
            raise WATSException(f"Failed to update product revision: {str(e)}")
    
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