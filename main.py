"""
pyWATS Main Example - API Explorer

This file initializes the pyWATS 2.0 API for exploration.
"""

from pyWATS import WATSApi
from pyWATS.models.report.uut.steps.sequence_call import SequenceCall
from pyWATS.models.report.uut.uut_report import UUTReport


def main():
    """
    Initialize the pyWATS API for exploration.
    """
    print("Initializing pyWATS API...")
    
    # Initialize API with example configuration
    api = WATSApi(
        base_url="https://py.wats.com",
        token="cHlXQVRTX1Rlc3RpbmdfT2xhOmdHMVZMM0xvc3preDlOUTB3cDk0RjhHOFE5IWI0Vg=="
    )
    
    
    # Get any operation by name or code
    op = api.get_operation("SW Debug")
    op = api.get_operation(10)

    # Get specific operation type
    test_op = api.get_operation("Final Test", operation_type="test")
    repair_op = api.get_operation("Component Replacement", operation_type="repair")
    wip_op = api.get_operation("In Progress", operation_type="wip")

    # Get just the code (useful for API calls)
    code = api.get_operation_code("Final Test")  # Returns int
    code = api.get_operation_code("Final Test", operation_type="test", strict=True)  # Raises if not found

    # Validate a code exists
    validated_code = api.get_operation_code(10)  # Returns 10 if valid, raises if not

    # Get lists
    all_ops = api.get_all_operations()
    test_ops = api.get_all_operations(operation_type="test")
    repair_ops = api.get_all_operations(operation_type="repair")

    # Cache management
    api.refresh_operations(force=True)
    cache_age = api.get_operation_cache_age()
    
    # Create and submit UUT
    uut = api.report.create_uut_report("Ola","12345","1.0","SN123456","10","Seq.seq","1.0","STATION1","Drammen, Norway", "PythonTest")  
    root = uut.get_root_sequence_call()
    root.add_numeric_step(name="MyNumericStep", value=42.0, unit="units")
    api.report.submit_report(report=uut)
    
    # Load all products
    products = api.product.get_all()
    for product in products:
        print(f"Product: {product['partNumber']} (ID: {product['name']})")
        
    # Asset
    
    # Get multiple assets
    assets = api.asset.get_assets("assetID eq 'def43023-45d1-40d3-a0a5-6f35dae4ab75'")
    for asset_info in assets:
        print(f"Asset: {asset_info.asset_name} (Serial: {asset_info.serial_number})")
    
    
    
    return api

if __name__ == "__main__":
    main()  # Changed from api = main()