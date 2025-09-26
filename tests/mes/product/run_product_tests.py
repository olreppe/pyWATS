"""
Simple MES Product Test Runner

Quick test runner for MES product operations.
Run this file directly to test product functionality.
"""

import sys
import os

# Add the current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from test_product_operations import ProductTestRunner


def main():
    """Run MES product tests"""
    print("🚀 Starting MES Product Tests...")
    print("📡 Using PyWATS API with default configuration")
    print()
    
    runner = ProductTestRunner()
    runner.run_all_tests()
    
    print()
    print("🏁 MES Product Tests Complete!")


if __name__ == "__main__":
    main()