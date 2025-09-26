"""
MES Product Test Utilities

Common utilities for MES product testing.
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import uuid


def generate_test_part_number(prefix: str = "TEST") -> str:
    """Generate a unique test part number"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_PART_{timestamp}"


def generate_test_bom(part_number: str, revision: str = "A", item_count: int = 3) -> Dict[str, Any]:
    """
    Generate a test BOM in WATS Standard BOM Format (WSBF)
    
    Args:
        part_number: Main part number for the BOM
        revision: Revision of the main part
        item_count: Number of BOM items to include
    
    Returns:
        Dictionary representing a BOM in WSBF format
    """
    bom_items = []
    
    for i in range(1, item_count + 1):
        item = {
            "itemNumber": i,
            "partNumber": f"{part_number}_COMP_{i:03d}",
            "revision": chr(64 + i),  # A, B, C, etc.
            "quantity": i,
            "description": f"Test Component {i}",
            "reference": f"C{i}" if i <= 10 else f"R{i-10}",
            "manufacturer": f"Test Mfg {i}",
            "manufacturerPartNumber": f"MFG_{part_number}_{i:03d}",
            "category": "Electronic Component"
        }
        bom_items.append(item)
    
    return {
        "partNumber": part_number,
        "revision": revision,
        "bomItems": bom_items,
        "createdBy": "ProductTestUtility",
        "createdDate": datetime.now().isoformat(),
        "bomId": str(uuid.uuid4()),
        "version": "1.0",
        "format": "WSBF",
        "totalItems": item_count,
        "metadata": {
            "testGenerated": True,
            "generator": "pyWATS MES Product Tests",
            "timestamp": datetime.now().isoformat()
        }
    }


def validate_product_response(response: Any, required_fields: List[str] = None) -> tuple[bool, str]:
    """
    Validate a product API response structure
    
    Args:
        response: The API response to validate
        required_fields: List of required fields to check for
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if required_fields is None:
        required_fields = ["PartNumber", "Revision", "ProductId"]
    
    if not response:
        return False, "Response is empty or None"
    
    if isinstance(response, list):
        if not response:
            return False, "Response list is empty"
        # Validate first item in list
        response = response[0]
    
    if not isinstance(response, dict):
        return False, f"Expected dict, got {type(response)}"
    
    missing_fields = []
    for field in required_fields:
        if field not in response:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, "Validation passed"


def validate_bom_response(response: Any) -> tuple[bool, str]:
    """
    Validate a BOM API response structure
    
    Args:
        response: The BOM API response to validate
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not response:
        return False, "BOM response is empty or None"
    
    if not isinstance(response, dict):
        return False, f"Expected dict, got {type(response)}"
    
    required_fields = ["partNumber", "bomItems"]
    missing_fields = []
    
    for field in required_fields:
        if field not in response:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required BOM fields: {', '.join(missing_fields)}"
    
    # Validate BOM items
    bom_items = response.get("bomItems", [])
    if not isinstance(bom_items, list):
        return False, "bomItems should be a list"
    
    if bom_items:
        # Check first BOM item structure
        first_item = bom_items[0]
        if not isinstance(first_item, dict):
            return False, "BOM items should be dictionaries"
        
        item_required_fields = ["itemNumber", "partNumber", "quantity"]
        item_missing_fields = []
        
        for field in item_required_fields:
            if field not in first_item:
                item_missing_fields.append(field)
        
        if item_missing_fields:
            return False, f"Missing BOM item fields: {', '.join(item_missing_fields)}"
    
    return True, "BOM validation passed"


def format_response_summary(response: Any, max_items: int = 5) -> str:
    """
    Format a response for summary display
    
    Args:
        response: API response to format
        max_items: Maximum number of items to show if response is a list
    
    Returns:
        Formatted string summary
    """
    if not response:
        return "Empty response"
    
    if isinstance(response, list):
        item_count = len(response)
        if item_count == 0:
            return "Empty list"
        
        summary = f"List with {item_count} item(s)"
        if item_count > 0 and isinstance(response[0], dict):
            first_item = response[0]
            keys = list(first_item.keys())[:3]  # Show first 3 keys
            summary += f", sample keys: {keys}"
        
        return summary
    
    elif isinstance(response, dict):
        key_count = len(response)
        keys = list(response.keys())[:5]  # Show first 5 keys
        return f"Dict with {key_count} key(s): {keys}"
    
    else:
        return f"{type(response).__name__}: {str(response)[:100]}"


def retry_operation(operation_func, max_retries: int = 3, delay: float = 1.0):
    """
    Retry an operation with exponential backoff
    
    Args:
        operation_func: Function to retry
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries (seconds)
    
    Returns:
        Result of the operation or raises the last exception
    """
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return operation_func()
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                print(f"    ⚠️ Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"    ❌ All {max_retries + 1} attempts failed")
    
    # If we get here, all attempts failed
    raise last_exception


def create_test_filters() -> List[str]:
    """Create a list of test filters for product searches"""
    return [
        "TEST",      # Find test parts
        "PCBA",      # Find PCBAs  
        "FAT",       # Find FAT parts
        "PROD",      # Find production parts
        "*",         # Get all (use with caution)
        "",          # Empty filter
        "NONEXISTENT"  # Should return empty
    ]


def log_test_step(step_number: int, description: str, result: Any = None):
    """Log a test step with consistent formatting"""
    print(f"[{step_number}] {description}")
    if result is not None:
        if hasattr(result, 'success'):
            # ProductTestResult object
            status = "✅" if result.success else "❌"
            print(f"    {status} {result.message}")
            if result.data and result.success:
                summary = format_response_summary(result.data)
                print(f"    📋 Data: {summary}")
        else:
            print(f"    📋 Result: {result}")


def print_test_header(title: str, width: int = 60):
    """Print a formatted test section header"""
    print("\n" + "=" * width)
    print(f" {title}")
    print("=" * width)