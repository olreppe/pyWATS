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
        
    # Asset
    asset = api.asset.get_asset("FIX0001")
    
    # Get multiple assets
    assets = api.asset.get_assets("assetID eq 'def43023-45d1-40d3-a0a5-6f35dae4ab75'")
    
   
    
    
    
    
    
    
    return api

if __name__ == "__main__":
    main()  # Changed from api = main()