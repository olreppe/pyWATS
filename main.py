"""
pyWATS Main Example - API Explorer

This file initializes the pyWATS 2.0 API for exploration.
"""

from pyWATS import WATSApi
from pyWATS.models.report.uut.steps.sequence_call import SequenceCall
from pyWATS.models.report.uut.uut_report import UUTReport
from pyWATS.models.process import ProcessType


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

    # api.refresh_operations(force=True)
    
    
    # Get any operation by name or code
    op = api.get_process("SW Debug", ProcessType.TEST)

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