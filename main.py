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
    uut = api.report.create_uut_report("Ola","12345","1.0","SN123456","10","Seq.seq","1.0","STATION1","Drammen, Norway", "PythonTest")
      
    root = uut.get_root_sequence_call()
    root.add_numeric_step(name="MyNumericStep", value=42.0, unit="units")
    api.report.submit_report(report=uut)
    
    return api

if __name__ == "__main__":
    main()  # Changed from api = main()