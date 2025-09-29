"""
MES Product Module

Handles product information, part numbers, revisions, and product management.
This module mirrors the Interface.MES Product functionality.
"""

from typing import Optional, List, Union, Dict, Any
from io import BytesIO

from pyWATS import rest_api

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
        
        This method uses the standard product REST API endpoints.
        
        Args:
            part_number: Product part number
            revision: Optional product revision (if provided, gets specific revision info)
            
        Returns:
            ProductInfo object or None if not found
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.product import get_product, get_product_revision
        
        try:
            if revision:
                # Get specific product revision
                product_rev = get_product_revision(
                    part_number=part_number,
                    revision=revision,
                    client=self._client
                )
                # Convert ProductRevision to ProductInfo
                return ProductInfo(
                    partNumber=product_rev.part_number or part_number,
                    revision=product_rev.revision,
                    name=product_rev.name,
                    description=product_rev.description,
                    productGroup=None,
                    createdDate=None,
                    updatedDate=None
                )
            else:
                # Get product (without specific revision)
                product = get_product(
                    part_number=part_number,
                    client=self._client
                )
                # Convert Product to ProductInfo  
                return ProductInfo(
                    partNumber=product.part_number or part_number,
                    revision=None,
                    name=product.name,
                    description=product.description,
                    productGroup=None,
                    createdDate=None,
                    updatedDate=None
                )
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
        
        
        
        request = None
        
        # IdentifyProductRequest(
        #     filter=filter_text,
        #     topCount=top_count,
        #     freePartnumber=free_partnumber,
        #     includeRevision=include_revision,
        #     includeSerialNumber=include_serial_number,
        #     customText=custom_text,
        #     alwaysOnTop=always_on_top
        # )
        
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
        
        Uses the standard query_products REST API endpoint with OData filtering.
        
        Args:
            filter_text: Filter string for product search
            top_count: Maximum number of results to return
            include_non_serial: Include non-serialized products (not used in current API)
            include_revision: Include revision information (not used in current API)
            
        Returns:
            List of Product objects matching criteria
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.product import query_products
        
        try:
            # Convert filter_text to OData filter if needed
            odata_filter = None
            if filter_text and filter_text.strip():
                if filter_text == "*":
                    odata_filter = None  # No filter, get all
                else:
                    # Create OData filter for part number contains
                    odata_filter = f"contains(PartNumber, '{filter_text}')"
            
            # Use query_products which returns ProductView objects
            product_views = query_products(
                odata_filter=odata_filter,
                odata_top=top_count,
                client=self._client
            )
            
            # Convert ProductView to ProductModel
            results = []
            for pv in product_views:
                if pv.part_number:  # Only include products with valid part numbers
                    product_model = ProductModel(
                        productId=getattr(pv, "product_id", None),
                        partNumber=pv.part_number,
                        revision=None,  # ProductView doesn't include revision
                        name=pv.name,
                        description=None,
                        nonSerial=getattr(pv, "non_serial", False),
                        xmlData=getattr(pv, "xml_data", None),
                        productCategoryId=getattr(pv, "product_category_id", None),
                        productCategoryName=getattr(pv, "product_category_name", None),
                        productGroup=getattr(pv, "product_group", None),
                        createdDate=getattr(pv, "created_date", None),
                        updatedDate=getattr(pv, "updated_date", None),
                        includeRevision=include_revision,
                        includeSerialNumber=False
                    )
                    results.append(product_model)
            
            return results
        except Exception as e:
            # Return empty list on error
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
            
            # Update the fields - use model_dump with mode='json' for proper UUID serialization
            if hasattr(existing_product, 'model_dump'):
                product_dict = existing_product.model_dump(mode='json')
            else:
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
        Get BOM (Bill of Materials) for a product revision.
        
        Note: BOM is associated with ProductRevision, not Product directly.
        This method requires both part_number and revision.
        
        Args:
            part_number: Product part number
            revision: Product revision (required for BOM operations)
            
        Returns:
            BOM data or None if not available/implemented
        """
        if not revision:
            # BOM operations require a specific product revision
            return None
            
        try:
            # Use the REST API endpoint to get BOM data
            from ..rest_api.endpoints.product import get_bom as rest_get_bom
            return rest_get_bom(part_number, revision, client=self._client)
        except Exception as e:
            # Return None if BOM retrieval fails (product may not have BOM)
            return None
    
    def upload_bom(self, bom_data: Union[str, Dict[str, Any]], part_number: Optional[str] = None, revision: Optional[str] = None) -> bool:
        """
        Upload BOM (Bill of Materials) using WSBF (WATS Standard BOM Format).
        
        Note: BOM is associated with ProductRevision, not Product directly.
        The BOM data should specify the target product and revision.
        
        Args:
            bom_data: BOM data as XML string or dictionary to convert to XML
            part_number: Target product part number (optional, can be in bom_data)
            revision: Target product revision (optional, can be in bom_data)
            
        Returns:
            True if upload was successful, False otherwise
            
        Raises:
            WATSAPIException: On API errors
        """
        from ..rest_api.endpoints.product import upload_bom as rest_upload_bom
        
        try:
            # Convert dictionary to XML if needed
            if isinstance(bom_data, dict):
                # Ensure part_number and revision are set
                if part_number:
                    bom_data["partNumber"] = part_number
                if revision:
                    bom_data["revision"] = revision
                    
                bom_xml = self._convert_bom_dict_to_xml(bom_data)
            else:
                bom_xml = bom_data
            
            # Upload BOM using REST API
            rest_upload_bom(bom_xml, client=self._client)
            
            return True
        except Exception:
            return False

    def get_product_revisions(self, part_number: str) -> List[Dict[str, Any]]:
        """
        Get all revisions for a specific product.
        
        Args:
            part_number: Product part number
            
        Returns:
            List of revision information
        """
        from ..rest_api.endpoints.product import get_product
        
        try:
            product = get_product(part_number=part_number, client=self._client)
            revisions = []
            
            for rev in (product.revisions or []):
                revisions.append({
                    "revision": rev.revision,
                    "name": rev.name,
                    "description": rev.description,
                    "state": rev.state,
                    "product_revision_id": str(rev.product_revision_id),
                    "part_number": rev.part_number
                })
            
            return revisions
        except Exception:
            return []
    
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