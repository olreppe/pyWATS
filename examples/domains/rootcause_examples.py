"""
Root Cause Analysis Examples

This example demonstrates root cause tracking in pyWATS.

DOMAIN KNOWLEDGE: Root Cause vs Symptom
========================================

1. SYMPTOM (What you see)
   - Example: "Unit failed voltage test"
   - Visible failure mode
   - Recorded in test reports

2. ROOT CAUSE (Why it happened)
   - Example: "Defective regulator IC from supplier"
   - Underlying reason for failure
   - Prevents recurrence

ROOT CAUSE WORKFLOW:
====================

1. Detect failure (test report)
2. Investigate (gather data)
3. Identify root cause (5 Whys, fishbone diagram)
4. Implement corrective action
5. Verify effectiveness
6. Prevent recurrence

ANALYSIS METHODS:
=================

- 5 Whys: Ask "why" 5 times to find root cause
- Fishbone Diagram: Categorize potential causes
- Pareto Analysis: Focus on most common issues
- Failure Mode Analysis: Systematic failure review

USE CASES:
==========

- Quality improvement
- Cost reduction (prevent waste)
- Compliance (CAPA - Corrective And Preventive Action)
- Knowledge management
"""

from pywats import pyWATS
from datetime import datetime
import os


def example_1_create_rca_case(api: pyWATS):
    """Create root cause analysis case."""
    print("=" * 60)
    print("EXAMPLE 1: Create RCA Case")
    print("=" * 60)
    
    print("Failure: Voltage test failures (15 units)")
    print("\nInvestigation:")
    print("  Why 1: Voltage out of spec")
    print("  Why 2: Regulator output incorrect")
    print("  Why 3: Wrong regulator part installed")
    print("  Why 4: Parts bin mislabeled")
    print("  Why 5: Label printer error")
    print("\nRoot Cause: Label printer malfunction")
    print("\nCorrective Action:")
    print("  1. Repair label printer")
    print("  2. Re-label all parts bins")
    print("  3. Add verification step to assembly")
    
    print("=" * 60)


def example_2_track_effectiveness(api: pyWATS):
    """Track corrective action effectiveness."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Corrective Action Tracking")
    print("=" * 60)
    
    print("Before: 15 failures in 500 units (3.0%)")
    print("Action: Implemented corrective action")
    print("After: 1 failure in 500 units (0.2%)")
    print("\n✓ Effective: 90% reduction in failures")
    
    print("=" * 60)


def example_3_rca_report(api: pyWATS):
    """Generate RCA summary report."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: RCA Summary Report")
    print("=" * 60)
    
    print("Period: January 2026")
    print("Total RCA Cases: 8")
    print("\nTop Root Causes:")
    print("  1. Supplier quality issues: 3")
    print("  2. Process errors: 2")
    print("  3. Equipment calibration: 2")
    print("  4. Training gaps: 1")
    
    print("=" * 60)


def main():
    """Run all rootcause examples."""
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("ROOT CAUSE ANALYSIS EXAMPLES")
    print("=" * 60)
    
    example_1_create_rca_case(api)
    example_2_track_effectiveness(api)
    example_3_rca_report(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
