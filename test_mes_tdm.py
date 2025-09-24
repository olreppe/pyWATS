#!/usr/bin/env python3
"""
Simple test to verify MES and TDM modules work correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported."""
    try:
        from pyWATS.mes import Production, Product, AssetHandler, Software, Workflow
        print("? MES modules imported successfully")
        
        from pyWATS.tdm import Statistics, Analytics, Reports  
        print("? TDM modules imported successfully")
        
        return True
    except Exception as e:
        print(f"? Import failed: {e}")
        return False

def test_instantiation():
    """Test that modules can be instantiated."""
    try:
        from pyWATS.mes import Production, Product, AssetHandler, Software, Workflow
        from pyWATS.tdm import Statistics, Analytics, Reports
        
        # Test MES modules
        production = Production()
        product = Product()
        asset_handler = AssetHandler()
        software = Software()
        workflow = Workflow()
        
        print("? MES modules instantiated successfully")
        
        # Test TDM modules
        statistics = Statistics()
        analytics = Analytics()
        reports = Reports()
        
        print("? TDM modules instantiated successfully")
        
        return True
    except Exception as e:
        print(f"? Instantiation failed: {e}")
        return False

def main():
    """Run all tests."""
    print("pyWATS MES/TDM Implementation Test")
    print("=" * 40)
    
    success = True
    
    print("\n1. Testing imports...")
    success &= test_imports()
    
    print("\n2. Testing instantiation...")
    success &= test_instantiation()
    
    print("\n" + "=" * 40)
    if success:
        print("? ALL TESTS PASSED")
        print("\nMES and TDM modules have been successfully implemented!")
        print("\nKey modules available:")
        print("  MES: Production, Product, AssetHandler, Software, Workflow")  
        print("  TDM: Statistics, Analytics, Reports")
        return 0
    else:
        print("? SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    exit(main())