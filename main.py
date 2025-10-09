"""
pyWATS Main Example - API Explorer

This file initializes the pyWATS 2.0 API for exploration.
"""

import sys
import os

from pyWATS.models.report.uut.steps.sequence_call import SequenceCall
from pyWATS.models.report.uut.uut_report import UUTReport

# Add src to path so we can import pyWATS
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pyWATS import WATSApi


def main():
    """
    Initialize the pyWATS API for exploration.
    """
    print("Initializing pyWATS API...")
    
    # Initialize API with example configuration
    api = WATSApi(
        base_url="https://ola.wats.com",
        token="cHlXQVRTOmdtQTVtTHo5N28yYWYwRm85MiY4cDhEUzdBcERRYQ=="
    )
    
    uut = api.report.create_uut_report("Ola","12345","1.0","SN123456","10","Seq.seq","1.0","STATION1","Drammen, Norway", "PythonTest")
      
    root = uut.get_root_sequence_call()
    root.add_numeric_step(name="MyNumericStep", value=42.0, unit="units")
    api.report.submit_report(report=uut)
    api.report.submit_pending_reports()

if __name__ == "__main__":
    api = main()