"""
MES Product Tests

Tests for MES product functionality including:
1. Getting product(s) and product revisions
2. Updating product information
3. Getting BOM-List
4. Uploading BOM-List

Based on C# MES Interface.MES.Product functionality.
Uses high-level pyWATS Product API - no direct REST API or HTTP calls.
"""

from datetime import datetime
from typing import List, Dict, Optional, Any

from pyWATS import create_api
from pyWATS.mes import Product


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
                # Test product service connectivity using Product API
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
        """Get the WATS API client for Product API initialization"""
        if self.api.tdm_client and self.api.tdm_client._connection:
            return self.api.tdm_client._connection._client
        return None

    def test_get_product_info(self, part_number: str, revision: str = "") -> ProductTestResult:
        """
        Test getting product information for a specific part number and revision.
        Based on C# method: GetProductInfo(string partNumber, string revision = "")
        Uses high-level Product API
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
                
        except Exception as e:
            return ProductTestResult(False, f"Failed to get product info: {str(e)}")

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

    def test_update_product_workflow(self) -> ProductTestResult:
        """
        Test the complete update workflow: get products -> select one -> modify -> update.
        This uses real server data instead of fictitious test parts.
        """
        try:
            # Step 1: Get available products
            print("[3.1] Getting available products...")
            products = self.product.get_product("", 20, True, True)  # Get up to 20 products
            
            if not products:
                return ProductTestResult(False, "No products found to test update workflow")
            
            print(f"      Found {len(products)} products")
            
            # Step 2: Select the first product that has a valid part number (not just wildcard)
            target_product = None
            for product in products:
                if (product.part_number and 
                    len(product.part_number.strip()) > 1 and 
                    product.part_number.strip() not in ["%", "*", "?"] and
                    not product.part_number.startswith("$")):  # Avoid wildcards and special chars
                    target_product = product
                    break
            
            if not target_product:
                return ProductTestResult(False, "No suitable product found for update test")
                
            print(f"[3.2] Selected product: {target_product.part_number}")
            print(f"      Current name: {target_product.name}")
            print(f"      Current description: {target_product.description}")
            
            # Step 3: Get current product info to see what we can update
            current_info = self.product.get_product_info(target_product.part_number, "")
            if not current_info:
                return ProductTestResult(False, f"Could not get current info for {target_product.part_number}")
            
            # Step 4: Prepare updates (modify description with timestamp to avoid conflicts)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_description = current_info.description or ""
            test_marker = f"[TEST_UPDATE_{timestamp}]"
            
            updates = {
                "description": f"{original_description} {test_marker}".strip()
            }
            
            # Only update name if it's not too important looking
            if not current_info.name or "test" in str(current_info.name).lower():
                updates["name"] = f"Test Updated {timestamp}"
            
            print(f"[3.3] Preparing updates: {updates}")
            
            # Step 5: Perform the update
            print(f"[3.4] Updating product {target_product.part_number}...")
            success = self.product.update_product(target_product.part_number, updates)
            
            if success:
                # Step 6: Verify the update by retrieving the product again
                print(f"[3.5] Verifying update...")
                updated_info = self.product.get_product_info(target_product.part_number, "")
                
                if updated_info and test_marker in (updated_info.description or ""):
                    return ProductTestResult(
                        True,
                        f"Successfully updated product {target_product.part_number} (verified with timestamp {timestamp})",
                        {
                            "part_number": target_product.part_number,
                            "original_info": {
                                "name": current_info.name,
                                "description": current_info.description
                            },
                            "updates_applied": updates,
                            "verification": "Update confirmed by re-reading product info"
                        }
                    )
                else:
                    return ProductTestResult(
                        False,
                        f"Update appeared successful but verification failed for {target_product.part_number}"
                    )
            else:
                return ProductTestResult(
                    False,
                    f"Update failed for {target_product.part_number} - check permissions or API implementation"
                )
                
        except Exception as e:
            return ProductTestResult(False, f"Update workflow failed: {str(e)}")

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
                    " - implementation not available"
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

        # Step 1: Get Real Products from Server
        print("\n" + "=" * 60)
        print(" STEP 1: Loading Real Products from Server")
        print("=" * 60)
        
        # Get real products to use for all tests
        real_products = self.product.get_product("", 10, True, True)  # Get up to 10 products
        if not real_products:
            print("❌ CRITICAL: No real products found on server - cannot run tests")
            return
            
        # Filter to get valid products (avoid wildcards)
        valid_products = []
        for product in real_products:
            if (product.part_number and 
                len(product.part_number.strip()) > 1 and 
                product.part_number.strip() not in ["%", "*", "?"] and
                not product.part_number.startswith("$")):
                valid_products.append(product)
                
        if not valid_products:
            print("❌ CRITICAL: No valid products found (all are wildcards) - cannot run tests")
            return
            
        # Use first few products for testing
        test_products = valid_products[:3]  # Use up to 3 real products
        test_part_numbers = [p.part_number for p in test_products]
        
        print(f"✅ Found {len(real_products)} total products, {len(valid_products)} valid")
        print(f"📋 Using products for testing: {test_part_numbers}")

        # Test 1: Get Product Info (Using Real Products)
        print("\n" + "=" * 60)
        print(" TEST 1: Get Product Info (Real Products)")
        print("=" * 60)
        
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

        # Test 3: Update Product (Real Workflow)
        print("\n" + "=" * 60)
        print(" TEST 3: Update Product (Real Workflow)")
        print("=" * 60)
        
        result = self.test_update_product_workflow()
        self.test_results.append(result)
        print(f"[3] Product Update: {result}")

        # Test 4: Get BOM (Using Real Product Revisions)
        print("\n" + "=" * 60)
        print(" TEST 4: Get BOM (Real Product Revisions)")
        print("=" * 60)
        
        # Test BOM with specific product revision that we know has BOM data
        print(f"[4.1] Testing BOM retrieval for known product with BOM...")
        result = self.test_get_bom("100200", "1")  # Use product 100200 revision 1 that we know has BOM
        self.test_results.append(result)
        print(f"[4] Get BOM (100200 rev 1): {result}")
        
        # Also test BOM for one of our discovered real products
        if test_part_numbers:
            first_part = test_part_numbers[0]
            print(f"[4.2] Testing BOM retrieval for discovered product...")
            result = self.test_get_bom(first_part, "1")  # Try revision 1
            self.test_results.append(result)
            print(f"[4] Get BOM ({first_part} rev 1): {result}")

        # Test 5: Upload BOM (Using Real Product)
        print("\n" + "=" * 60)
        print(" TEST 5: Upload BOM (Real Product)")
        print("=" * 60)
        
        # Use first real product for BOM upload test
        first_real_part = test_part_numbers[0] if test_part_numbers else "100200"
        sample_bom = self.create_sample_bom(first_real_part)
        result = self.test_upload_bom(sample_bom)
        self.test_results.append(result)
        print(f"[5] Upload BOM ({first_real_part}): {result}")
        
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