"""
MES Product Module

Handles product information, part numbers, revisions, and product management.
This module mirrors the Interface.MES Product functionality.
"""

from typing import Optional, List, Union
from io import BytesIO

from .base import MESBase
from .models import ProductInfo, Product, IdentifyProductRequest
from ..rest_api.client import WATSClient
from ..connection import WATSConnection


class Product(MESBase):
    """
    Product management for WATS MES.
    
    Provides functionality for:
    - Product information retrieval
    - Product search and filtering
    - Product identification dialogs
    """
    
    def __init__(self, connection: Optional[Union[WATSConnection, WATSClient]] = None):
        """
        Initialize Product module.
        
        Args:
            connection: WATS connection or client instance
        """
        super().__init__(connection)
    
    def is_connected(self) -> bool:
        """
        Check if connected to WATS MES Server.
        
        Returns:
            True if connected, False otherwise
        """
        try:
            response = self._client.get("/api/internal/Product/isConnected")
            return response.status_code == 200
        except Exception:
            return False
    
    def deserialize_from_stream(self, stream: BytesIO) -> dict:
        """
        Deserialize object from stream.
        
        Note: This is a placeholder for C# stream deserialization functionality.
        In Python, this would typically be handled by json.load() or similar.
        
        Args:
            stream: BytesIO stream containing serialized data
            
        Returns:
            Deserialized object as dictionary
        """
        import json
        stream.seek(0)
        return json.load(stream)
    
    def get_product_info(
        self, 
        part_number: str, 
        revision: str = ""
    ) -> Optional[ProductInfo]:
        """
        Get product information by part number.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            part_number: Product part number
            revision: Optional product revision
            
        Returns:
            ProductInfo object or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {"partNumber": part_number}
        if revision:
            params["revision"] = revision
        
        try:
            response = self._rest_get_json(
                "/api/internal/Product/GetProductInfo",
                response_type=ProductInfo
            )
            return response
        except Exception:
            return None
    
    def identify_product(
        self,
        filter_text: str = "",
        top_count: int = 10,
        free_partnumber: bool = False,
        include_revision: bool = True,
        include_serial_number: bool = False,
        custom_text: str = "",
        always_on_top: bool = True
    ) -> Optional[Product]:
        """
        Display product identification dialog with filters.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            filter_text: Filter string for product search
            top_count: Maximum number of results to show
            free_partnumber: Allow free-text part number entry
            include_revision: Include revision in selection
            include_serial_number: Include serial number in selection
            custom_text: Custom dialog text
            always_on_top: Keep dialog on top
            
        Returns:
            Selected Product or None if cancelled
            
        Raises:
            WATSAPIException: On API errors
        """
        request = IdentifyProductRequest(
            filter=filter_text,
            top_count=top_count,
            free_partnumber=free_partnumber,
            include_revision=include_revision,
            include_serial_number=include_serial_number,
            custom_text=custom_text,
            always_on_top=always_on_top
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Product/IdentifyProduct",
                request,
                response_type=Product
            )
            return response
        except Exception:
            return None
    
    def get_product(
        self,
        filter_text: str,
        top_count: int,
        include_non_serial: bool,
        include_revision: bool
    ) -> List[Product]:
        """
        Get products matching filter criteria.
        
        ?? INTERNAL API: This method uses internal WATS endpoints
        
        Args:
            filter_text: Filter string for product search
            top_count: Maximum number of results to return
            include_non_serial: Include non-serialized products
            include_revision: Include revision information
            
        Returns:
            List of Product objects matching criteria
            
        Raises:
            WATSAPIException: On API errors
        """
        params = {
            "filter": filter_text,
            "topCount": top_count,
            "includeNonSerial": include_non_serial,
            "includeRevision": include_revision
        }
        
        response = self._rest_get_json("/api/internal/Product/GetProduct")
        products_data = response.get("products", [])
        
        return [Product.parse_obj(item) for item in products_data]