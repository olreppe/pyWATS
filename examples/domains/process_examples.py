"""
Process Examples - Operation Types and Manufacturing Steps

This example demonstrates process/operation type management in pyWATS.

DOMAIN KNOWLEDGE: Operation Types
==================================

OPERATION TYPE = Manufacturing step/station

Examples:
- ASSEMBLY: Build the unit
- SOLDER: PCB soldering
- INSPECTION: Visual/quality check
- FINAL-TEST: Final verification
- BURN-IN: Stress testing
- CALIBRATION: Sensor calibration
- REWORK: Repair failed units
- PACKAGING: Final packaging

Purpose:
- Define manufacturing flow
- Track where units are in process
- Calculate yield by operation
- Identify bottlenecks

PROCESS WORKFLOW:
=================

1. Define operation types (manufacturing steps)
2. Create sequence (routing)
3. Track units through operations
4. Measure cycle time per operation
5. Identify bottlenecks
6. Optimize process flow

ROUTING:
========

Sequence of operations a unit goes through:

Example: Widget-2000 Routing
  1. ASSEMBLY
  2. SOLDER
  3. INITIAL-TEST
  4. BURN-IN
  5. FINAL-TEST
  6. PACKAGING

Units flow through this sequence.
"""

from pywats import pyWATS
from datetime import datetime
import os


def example_1_list_operation_types(api: pyWATS):
    """List all defined operation types."""
    print("=" * 60)
    print("EXAMPLE 1: Operation Types")
    print("=" * 60)
    
    operations = [
        {"name": "ASSEMBLY", "description": "Build unit"},
        {"name": "SOLDER", "description": "PCB soldering"},
        {"name": "INSPECTION", "description": "Visual check"},
        {"name": "INITIAL-TEST", "description": "Quick functional test"},
        {"name": "BURN-IN", "description": "48-hour stress test"},
        {"name": "CALIBRATION", "description": "Calibrate sensors"},
        {"name": "FINAL-TEST", "description": "Full verification"},
        {"name": "REWORK", "description": "Repair failures"},
        {"name": "PACKAGING", "description": "Final packaging"}
    ]
    
    print("Defined Operations:\n")
    for i, op in enumerate(operations, 1):
        print(f"{i}. {op['name']}")
        print(f"   {op['description']}")
    
    print("=" * 60)


def example_2_product_routing(api: pyWATS):
    """Define routing (sequence) for a product."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Product Routing")
    print("=" * 60)
    
    print("Product: WIDGET-2000")
    print("Manufacturing Sequence:\n")
    
    routing = [
        "ASSEMBLY",
        "SOLDER",
        "INITIAL-TEST",
        "BURN-IN",
        "FINAL-TEST",
        "PACKAGING"
    ]
    
    for i, step in enumerate(routing, 1):
        print(f"  {i}. {step}")
        if i < len(routing):
            print("     ↓")
    
    print("\nEstimated cycle time: 52 hours")
    
    print("=" * 60)


def example_3_bottleneck_analysis(api: pyWATS):
    """Identify process bottlenecks."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Bottleneck Analysis")
    print("=" * 60)
    
    operations_data = [
        {"name": "ASSEMBLY", "avg_time": "30 min", "capacity": 20},
        {"name": "SOLDER", "avg_time": "15 min", "capacity": 40},
        {"name": "INITIAL-TEST", "avg_time": "10 min", "capacity": 60},
        {"name": "BURN-IN", "avg_time": "48 hrs", "capacity": 5},  # BOTTLENECK
        {"name": "FINAL-TEST", "avg_time": "20 min", "capacity": 30},
        {"name": "PACKAGING", "avg_time": "5 min", "capacity": 120}
    ]
    
    print("Process Capacity Analysis:\n")
    
    min_capacity = min(op["capacity"] for op in operations_data)
    
    for op in operations_data:
        capacity_str = f"{op['capacity']} units/day"
        
        if op["capacity"] == min_capacity:
            indicator = "⚠ BOTTLENECK"
        else:
            indicator = "✓"
        
        print(f"{indicator} {op['name']}")
        print(f"    Time: {op['avg_time']}")
        print(f"    Capacity: {capacity_str}")
    
    print(f"\nOverall capacity limited by: BURN-IN")
    print(f"Maximum throughput: {min_capacity} units/day")
    
    print("=" * 60)


def main():
    """Run all process examples."""
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("PROCESS DOMAIN EXAMPLES")
    print("=" * 60)
    
    example_1_list_operation_types(api)
    example_2_product_routing(api)
    example_3_bottleneck_analysis(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
