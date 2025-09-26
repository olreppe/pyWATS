"""
MES Product Module

Handles product information, part numbers, revisions, and product management.
This module mirrors the Interface.MES Product functionality.
"""

from typing import Optional, List, Union, Dict, Any
from io import BytesIO

from .base import MESBase
from .models import ProductInfo, Product as ProductModel, IdentifyProductRequest
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
        from ..rest_api.endpoints.internal import get_product_info_internal
        
        try:
            response = get_product_info_internal(
                part_number=part_number,
                revision=revision if revision else None,
                client=self._client
            )
            return ProductInfo.model_validate(response) if response else None
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
    ) -> Optional[ProductModel]:
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
            topCount=top_count,
            freePartnumber=free_partnumber,
            includeRevision=include_revision,
            includeSerialNumber=include_serial_number,
            customText=custom_text,
            alwaysOnTop=always_on_top
        )
        
        try:
            response = self._rest_post_json(
                "/api/internal/Product/IdentifyProduct",
                request,
                response_type=ProductModel
            )
            return response if isinstance(response, ProductModel) else ProductModel.model_validate(response) if response else None
        except Exception:
            return None
    
    def get_product(
        self,
        filter_text: str,
        top_count: int,
        include_non_serial: bool,
        include_revision: bool
    ) -> List[ProductModel]:
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
        from ..rest_api.endpoints.internal import get_products_internal
        
        try:
            response = get_products_internal(
                filter_text=filter_text,
                top_count=top_count,
                include_non_serial=include_non_serial,
                include_revision=include_revision,
                client=self._client
            )
            
            # The response should be a list of products directly
            if isinstance(response, list):
                return [ProductModel.model_validate(item) for item in response]
            return []
        except Exception:
            return []
    
    def update_product(self, part_number: str, updates: Dict[str, Any]) -> bool:
        """
        Update product information.
        
        Args:
            part_number: Product part number
            updates: Dictionary of fields to update
            
        Returns:
            True if update was successful, False otherwise
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.product import get_product, create_product
        from ..rest_api.models.product import Product as ProductRestModel
        
        try:
            # First get the existing product
            existing_product = get_product(part_number, client=self._client)
            
            # Update the fields
            product_dict = existing_product.dict()
            product_dict.update(updates)
            
            # Create updated product object
            updated_product = ProductRestModel(**product_dict)
            
            # Use create_product which can update existing products
            create_product(updated_product, client=self._client)
            
            return True
        except Exception:
            return False
    
    def get_bom(self, part_number: str, revision: str = "") -> Optional[Dict[str, Any]]:
        """
        Get BOM (Bill of Materials) for a product.
        
        Note: This functionality is not yet available in the REST API.
        A BOM retrieval endpoint would need to be implemented.
        
        Args:
            part_number: Product part number
            revision: Optional product revision
            
        Returns:
            BOM data or None if not available
        """
        # TODO: Implement when BOM retrieval REST API endpoint becomes available
        return None
    
    def upload_bom(self, bom_data: Union[str, Dict[str, Any]]) -> bool:
        """
        Upload BOM (Bill of Materials) using WSBF (WATS Standard BOM Format).
        
        Args:
            bom_data: BOM data as XML string or dictionary to convert to XML
            
        Returns:
            True if upload was successful, False otherwise
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.product import upload_bom as rest_upload_bom
        
        try:
            # Convert dictionary to XML if needed
            if isinstance(bom_data, dict):
                bom_xml = self._convert_bom_dict_to_xml(bom_data)
            else:
                bom_xml = bom_data
            
            # Upload BOM using REST API
            rest_upload_bom(bom_xml, client=self._client)
            
            return True
        except Exception:
            return False
    
    def _convert_bom_dict_to_xml(self, bom_dict: Dict[str, Any]) -> str:
        """
        Convert BOM dictionary to WSBF XML format.
        
        This is a basic implementation that would need to be expanded
        based on the actual WSBF specification.
        
        Args:
            bom_dict: BOM data as dictionary
            
        Returns:
            XML string in WSBF format
        """
        # Basic XML conversion - this would need to be properly implemented
        # according to WATS Standard BOM Format (WSBF) specification
        part_number = bom_dict.get("partNumber", "")
        revision = bom_dict.get("revision", "")
        bom_items = bom_dict.get("bomItems", [])
        
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<BOM>',
            f'  <PartNumber>{part_number}</PartNumber>',
            f'  <Revision>{revision}</Revision>',
            '  <Items>'
        ]
        
        for item in bom_items:
            xml_lines.extend([
                '    <Item>',
                f'      <ItemNumber>{item.get("itemNumber", "")}</ItemNumber>',
                f'      <PartNumber>{item.get("partNumber", "")}</PartNumber>',
                f'      <Revision>{item.get("revision", "")}</Revision>',
                f'      <Quantity>{item.get("quantity", 0)}</Quantity>',
                f'      <Description>{item.get("description", "")}</Description>',
                f'      <Reference>{item.get("reference", "")}</Reference>',
                '    </Item>'
            ])
        
        xml_lines.extend([
            '  </Items>',
            '</BOM>'
        ])
        
        return '\n'.join(xml_lines)