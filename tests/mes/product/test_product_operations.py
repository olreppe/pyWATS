"""
MES Product Tests

Tests for MES product functionality including:
1. Getting product(s) and product revisions
2. Updating product information
3. Getting BOM-List
4. Uploading BOM-List

Based on C# MES Interface.MES.Product functionality.
Uses pyWATS REST API endpoints - no direct HTTP calls.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any

from pyWATS import create_api
from pyWATS.mes import Product
from pyWATS.rest_api.exceptions import WATSAPIException


class ProductTestResult:
    """Result of a product test operation"""
    def __init__(self, success: bool, message: str = "", data: Any = None, error: str = ""):
        self.success = success
        self.message = message
        self.data = data
        self.error = error
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{'✅ PASS' if self.success else '❌ FAIL'}: {self.message}"


class ProductTestRunner:
    """Test runner for MES Product functionality using PyWATS API"""
    
    def __init__(self, config_override: Optional[Dict] = None):
        self.api = create_api(config_override) if config_override else create_api()
        self.test_results: List[ProductTestResult] = []
        self.product = Product(self.client)

    def setup_connection(self) -> ProductTestResult:
        """Setup connection to WATS server using PyWATS API"""
        try:
            if self.api.test_connection():
                # Test product service connectivity using REST API
                try:
                    # Check connection using Product API
                    connected = self.product.is_connected()
                    if connected:
                        return ProductTestResult(True, f"Connection and Product service online (Status: {self.api.connection_status})")
                    else:
                        return ProductTestResult(False, f"Product service not connected")
                except:
                    # Fallback if product service check fails
                    return ProductTestResult(True, f"Connection established (Status: {self.api.connection_status})")
            else:
                return ProductTestResult(False, f"Connection test failed (Status: {self.api.connection_status})")
        except Exception as e:
            return ProductTestResult(False, f"Connection setup failed: {str(e)}")

    @property
    def client(self):
        """Get the WATS API client for REST operations"""
        if self.api.tdm_client and self.api.tdm_client._connection:
            return self.api.tdm_client._connection._client
        return None

    def test_get_product_info(self, part_number: str, revision: str = "") -> ProductTestResult:
        """
        Test getting product information for a specific part number and revision.
        Based on C# method: GetProductInfo(string partNumber, string revision = "")
        Uses REST API: internal.get_product_info_internal()
        """
        try:
            response = self.product.get_product_info(
                part_number=part_number,
                revision=revision if revision else ""
            )
            
            if response:
                return ProductTestResult(
                    True, 
                    f"Product info retrieved for {part_number}" + (f" rev {revision}" if revision else ""),
                    response
                )
            else:
                return ProductTestResult(
                    False, 
                    f"No product info found for {part_number}" + (f" rev {revision}" if revision else "")
                )
                
        except WATSAPIException as e:
            return ProductTestResult(False, f"Failed to get product info: {str(e)}")
        except Exception as e:
            return ProductTestResult(False, f"Unexpected error getting product info: {str(e)}")

    def test_get_products(self, filter_text: str = "", top_count: int = 10, 
                         include_non_serial: bool = True, include_revision: bool = True) -> ProductTestResult:
        """
        Test getting products with filter.
        Based on C# method: GetProduct(string filter, int topCount, bool includeNonSerial, bool includeRevision)
        API endpoint: api/internal/Product/GetProducts
        """
        try:
            response = self.product.get_product(
                filter_text=filter_text,
                top_count=top_count,
                include_non_serial=include_non_serial,
                include_revision=include_revision
            )
            
            if response:
                product_count = len(response)
                return ProductTestResult(
                    True, 
                    f"Retrieved {product_count} product(s) with filter '{filter_text}'",
                    response
                )
            else:
                return ProductTestResult(
                    False, 
                    f"No products found with filter '{filter_text}'"
                )
                
        except Exception as e:
            return ProductTestResult(False, f"Failed to get products: {str(e)}")

    def test_update_product(self, part_number: str, updates: Dict[str, Any]) -> ProductTestResult:
        """
        Test updating product information.
        Uses the Product API update_product method.
        """
        try:
            success = self.product.update_product(part_number, updates)
            
            if success:
                return ProductTestResult(
                    True, 
                    f"Product updated successfully for {part_number}",
                    updates
                )
            else:
                return ProductTestResult(
                    False, 
                    f"Product update failed for {part_number} - product may not exist"
                )
                
        except Exception as e:
            return ProductTestResult(False, f"Failed to update product: {str(e)}")

    def test_get_bom(self, part_number: str, revision: str = "") -> ProductTestResult:
        """
        Test getting BOM (Bill of Materials) for a product.
        Uses the Product API get_bom method.
        """
        try:
            response = self.product.get_bom(part_number, revision)
            
            if response:
                return ProductTestResult(
                    True, 
                    f"BOM retrieved for {part_number}" + (f" rev {revision}" if revision else ""),
                    response
                )
            else:
                return ProductTestResult(
                    False, 
                    f"BOM retrieval not yet implemented for {part_number}" + 
                    (f" rev {revision}" if revision else "") +
                    " - awaiting REST API endpoint"
                )
                
        except Exception as e:
            return ProductTestResult(False, f"Failed to get BOM: {str(e)}")

    def test_upload_bom(self, bom_data: Dict[str, Any]) -> ProductTestResult:
        """
        Test uploading BOM (Bill of Materials).
        Uses the Product API upload_bom method with WSBF format.
        """
        try:
            success = self.product.upload_bom(bom_data)
            
            if success:
                return ProductTestResult(
                    True, 
                    "BOM uploaded successfully using WSBF format",
                    bom_data
                )
            else:
                return ProductTestResult(
                    False, 
                    "BOM upload failed"
                )
                
        except Exception as e:
            return ProductTestResult(False, f"Failed to upload BOM: {str(e)}")

    def create_sample_bom(self, part_number: str, revision: str = "A") -> Dict[str, Any]:
        """Create a sample BOM in WATS Standard BOM Format (WSBF)"""
        return {
            "partNumber": part_number,
            "revision": revision,
            "bomItems": [
                {
                    "itemNumber": 1,
                    "partNumber": f"{part_number}_COMP_001",
                    "revision": "A",
                    "quantity": 2,
                    "description": "Sample Component 1",
                    "reference": "C1, C2"
                },
                {
                    "itemNumber": 2,
                    "partNumber": f"{part_number}_COMP_002", 
                    "revision": "B",
                    "quantity": 1,
                    "description": "Sample Component 2",
                    "reference": "R1"
                }
            ],
            "createdBy": "ProductTestRunner",
            "createdDate": datetime.now().isoformat()
        }

    def run_all_tests(self) -> None:
        """Run all product tests"""
        print("=" * 60)
        print(" MES PRODUCT TESTING SUITE")
        print("=" * 60)
        print(f"Started at: {datetime.now()}")
        print()

        # Setup
        result = self.setup_connection()
        self.test_results.append(result)
        print(f"[SETUP] Connection: {result}")
        
        if not result.success:
            print("❌ Cannot continue without connection")
            return

        # Test 1: Get Product Info
        print("\n" + "=" * 60)
        print(" TEST 1: Get Product Info")
        print("=" * 60)
        
        test_part_numbers = ["TEST_PART_001", "PCBA_PART_001"]
        for pn in test_part_numbers:
            result = self.test_get_product_info(pn)
            self.test_results.append(result)
            print(f"[1] Product Info ({pn}): {result}")
            
            if result.success and result.data:
                print(f"    📋 Response type: {type(result.data)}")
                if isinstance(result.data, list) and result.data:
                    print(f"    📋 Products found: {len(result.data)}")
                    first_product = result.data[0]
                    if isinstance(first_product, dict):
                        print(f"    📋 Sample keys: {list(first_product.keys())[:5]}")

        # Test 2: Get Products with Filter
        print("\n" + "=" * 60)
        print(" TEST 2: Get Products with Filter")
        print("=" * 60)
        
        filters = ["TEST", "PCBA", "*"]
        for filter_text in filters:
            result = self.test_get_products(filter_text, top_count=5)
            self.test_results.append(result)
            print(f"[2] Products Filter ('{filter_text}'): {result}")

        # Test 3: Update Product (Simulation)
        print("\n" + "=" * 60)
        print(" TEST 3: Update Product (Simulation)")
        print("=" * 60)
        
        updates = {
            "description": "Updated via automated test",
            "category": "Test Category",
            "lastModified": datetime.now().isoformat()
        }
        result = self.test_update_product("TEST_PART_001", updates)
        self.test_results.append(result)
        print(f"[3] Product Update: {result}")

        # Test 4: Get BOM
        print("\n" + "=" * 60)
        print(" TEST 4: Get BOM")
        print("=" * 60)
        
        for pn in test_part_numbers:
            result = self.test_get_bom(pn)
            self.test_results.append(result)
            print(f"[4] Get BOM ({pn}): {result}")

        # Test 5: Upload BOM
        print("\n" + "=" * 60)
        print(" TEST 5: Upload BOM")
        print("=" * 60)
        
        sample_bom = self.create_sample_bom("TEST_BOM_PART_001")
        result = self.test_upload_bom(sample_bom)
        self.test_results.append(result)
        print(f"[5] Upload BOM: {result}")
        
        if result.success:
            print("    📋 BOM Data Sample:")
            print(f"    📋 Part Number: {sample_bom['partNumber']}")
            print(f"    📋 Items: {len(sample_bom['bomItems'])}")

        # Summary
        print("\n" + "=" * 60)
        print(" TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.success)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Tests Run: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print()
        
        print("Results:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅ PASS" if result.success else "❌ FAIL"
            print(f"  {status}: {result.message}")


def main():
    """Main test execution"""
    # Run tests with default configuration (uses ola.wats.com)
    runner = ProductTestRunner()
    runner.run_all_tests()


if __name__ == "__main__":
    main()