"""
pyWATS Main Example - API Explorer

This file initializes the pyWATS 2.0 API for exploration.
"""

import sys
import os

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
    
    print("API initialized successfully!")
    print(f"API: {api}")
    print()
    print("Available modules:")
    print(f"  - api.product: {type(api.product).__name__}")
    print(f"  - api.asset: {type(api.asset).__name__}")
    print(f"  - api.production: {type(api.production).__name__}")
    print(f"  - api.workflow: {type(api.workflow).__name__}")
    print(f"  - api.software: {type(api.software).__name__}")
    print(f"  - api.report: {type(api.report).__name__}")
    print(f"  - api.app: {type(api.app).__name__}")
    print()
    print("API ready for exploration. Use 'api' variable to access modules.")
    
    # Make api available for interactive exploration
    globals()['api'] = api
    
    api.product.get_product("ABD", 1, True, True)
    
    
    return api


if __name__ == "__main__":
    api = main()