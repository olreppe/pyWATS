#!/usr/bin/env python3
"""
Simple debugging test for VS Code F5 functionality.
This file can be used to test that debugging works correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_debugging():
    """Test function with breakpoint opportunities."""
    print("?? Starting debugging test...")
    
    # Test 1: Basic variables
    message = "Hello from pyWATS!"
    number = 42
    items = ["apple", "banana", "cherry"]
    
    print(f"?? Message: {message}")
    print(f"?? Number: {number}")
    print(f"?? Items: {items}")
    
    # Test 2: Loop (good for stepping through)
    print("\n?? Testing loop:")
    for i, item in enumerate(items):
        result = f"{i}: {item}"
        print(f"   {result}")
    
    # Test 3: Try importing pyWATS
    try:
        import pyWATS
        print(f"? pyWATS imported successfully")
        print(f"?? Version: {pyWATS.__version__}")
    except Exception as e:
        print(f"? Error importing pyWATS: {e}")
    
    # Test 4: Dictionary manipulation
    config = {
        "debug": True,
        "timeout": 30,
        "retries": 3
    }
    
    print(f"\n??  Config: {config}")
    
    # Set a breakpoint here for testing
    final_result = "Debugging test completed successfully!"
    return final_result

def main():
    """Main function for debugging test."""
    print("=" * 50)
    print("?? VS Code F5 Debugging Test")
    print("=" * 50)
    
    # Call test function
    result = test_debugging()
    
    print(f"\n?? Result: {result}")
    print("=" * 50)
    print("?? Tips:")
    print("   - Set breakpoints by clicking left of line numbers")
    print("   - Use F10 to step over, F11 to step into")
    print("   - Check Variables panel for variable values")
    print("   - Use Debug Console for interactive debugging")

if __name__ == "__main__":
    main()