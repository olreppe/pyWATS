# MES Product Tests

This directory contains comprehensive tests for MES (Manufacturing Execution System) product functionality.

## Test Structure

### Main Files
- `test_product_operations.py` - Main test runner with ProductTestRunner class
- `run_product_tests.py` - Simple entry point to run all tests
- `product_config.py` - Configuration settings and constants
- `product_utils.py` - Utility functions and helpers
- `test_data/` - Sample data files for testing

### Test Coverage

The tests cover the following MES product operations based on the C# Interface.MES.Product module:

1. **Get Product Info** (`test_get_product_info`)
   - API: `api/internal/Product/GetProductInfo`
   - Tests retrieval of product information by part number and revision

2. **Get Products** (`test_get_products`) 
   - API: `api/internal/Product/GetProducts`
   - Tests product search with filters and parameters

3. **Update Product** (`test_update_product`)
   - Simulated test for product updates (API endpoint TBD)

4. **Get BOM** (`test_get_bom`)
   - Tests BOM (Bill of Materials) retrieval
   - Tries multiple possible endpoints

5. **Upload BOM** (`test_upload_bom`)
   - API: `api/Product/BOM` (POST)
   - Tests BOM upload in WSBF (WATS Standard BOM Format)

## Running Tests

```bash
# From the product test directory
python run_product_tests.py

# Or run the main test file directly  
python test_product_operations.py
```

## Configuration

Update `product_config.py` to modify:
- Server URL and authentication
- Test part numbers and filters
- API endpoints
- Timeout settings

## Current Status

✅ **Test Structure Complete**
- All 5 test methods implemented
- Configuration and utilities ready
- Sample data available
- Proper error handling and reporting

🔧 **Known Issues to Debug**
- HTTP 401 authentication (needs proper token format/handling)
- API endpoint validation needed
- BOM format specifications may need refinement

## Next Steps

1. Fix authentication issues
2. Validate API endpoints with actual server
3. Refine BOM data format according to WATS specifications
4. Add more comprehensive test data sets
5. Implement any missing update endpoints

The test framework is ready - now we can debug specific issues one by one!