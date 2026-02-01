"""
Analytics Examples - Yield Analysis, Cpk, and Statistical Process Control

This example demonstrates how to use analytics in pyWATS for production insights.

DOMAIN KNOWLEDGE: Analytics vs Raw Data
========================================

Understanding the purpose:

1. RAW DATA (Report/Production Domains)
   - Individual test results
   - Example: Unit SN-12345 tested voltage = 5.02V
   - Use: Recording what happened

2. ANALYTICS (Analytics Domain)
   - Aggregated insights from raw data
   - Example: 95% pass rate, Cpk = 1.67 for voltage tests
   - Use: Understanding trends, making decisions

Think of it as: Reports = Individual trees, Analytics = Forest view

KEY METRICS:
============

1. YIELD
   - Percentage of units passing
   - Formula: (Passed Units / Total Units) × 100
   - Example: 950 passed / 1000 total = 95% yield
   - Use: Overall process health

2. Cpk (Process Capability Index)
   - Measures process capability vs specification
   - Cpk ≥ 1.33: Process capable
   - Cpk < 1.00: Process not capable (many failures)
   - Example: Cpk = 1.67 means process well within spec
   - Use: Predict future performance

3. FIRST PASS YIELD (FPY)
   - Percentage passing without rework
   - Formula: (Passed First Time / Total Units) × 100
   - Example: 900 / 1000 = 90% FPY (100 needed rework)
   - Use: Manufacturing efficiency

4. PARETO ANALYSIS
   - Identify most common failure modes
   - 80/20 rule: 80% of failures from 20% of causes
   - Example: 3 failure types cause 80% of all failures
   - Use: Focus improvement efforts

STATISTICAL PROCESS CONTROL (SPC):
===================================

Monitor process stability over time:

- Control Charts: Plot measurements with limits
- Trends: Identify process drift
- Outliers: Detect abnormal results
- Alerts: Notify when process goes out of control

COMPLETE WORKFLOW:
==================
1. Collect test data (from Report domain)
2. Calculate yield by product/operation
3. Compute Cpk for critical parameters
4. Identify failure modes (Pareto)
5. Create control charts
6. Monitor trends over time
7. Generate management reports
"""

from pywats import pyWATS
from datetime import datetime, timedelta
import os
import statistics


def example_1_calculate_yield(api: pyWATS):
    """
    Step 1: Calculate yield (pass rate) for a product.
    
    Shows overall pass percentage.
    """
    print("=" * 60)
    print("EXAMPLE 1: Yield Calculation")
    print("=" * 60)
    
    product_name = "WIDGET-2000"
    
    # Get all production units for product
    units = api.production.get_units_by_product(product_name)
    
    print(f"Product: {product_name}")
    print(f"Total units: {len(units)}\n")
    
    # Calculate yield
    passed = [u for u in units if u.passed]
    failed = [u for u in units if not u.passed]
    
    if len(units) > 0:
        yield_percent = (len(passed) / len(units)) * 100
    else:
        yield_percent = 0
    
    print("Results:")
    print(f"  Passed: {len(passed)}")
    print(f"  Failed: {len(failed)}")
    print(f"  Yield: {yield_percent:.2f}%")
    
    # Grade yield
    if yield_percent >= 95:
        grade = "Excellent"
    elif yield_percent >= 90:
        grade = "Good"
    elif yield_percent >= 80:
        grade = "Fair"
    else:
        grade = "Needs Improvement"
    
    print(f"  Grade: {grade}")
    
    print("=" * 60)
    
    return yield_percent


def example_2_yield_by_operation(api: pyWATS):
    """
    Step 2: Break down yield by operation type.
    
    Identify which operations have lowest yield.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Yield by Operation Type")
    print("=" * 60)
    
    product_name = "WIDGET-2000"
    
    units = api.production.get_units_by_product(product_name)
    
    print(f"Product: {product_name}\n")
    print("Yield by Operation:")
    
    # Group by operation
    operations = {}
    for unit in units:
        op = unit.operation_type_name
        if op not in operations:
            operations[op] = {"total": 0, "passed": 0}
        operations[op]["total"] += 1
        if unit.passed:
            operations[op]["passed"] += 1
    
    # Sort by yield (worst first)
    sorted_ops = sorted(
        operations.items(),
        key=lambda x: (x[1]["passed"] / x[1]["total"]) if x[1]["total"] > 0 else 0
    )
    
    for op, stats in sorted_ops:
        if stats["total"] > 0:
            yield_pct = (stats["passed"] / stats["total"]) * 100
            failed = stats["total"] - stats["passed"]
            
            # Visual indicator
            if yield_pct >= 95:
                indicator = "✓"
            elif yield_pct >= 85:
                indicator = "⚡"
            else:
                indicator = "⚠"
            
            print(f"  {indicator} {op}:")
            print(f"      {stats['passed']}/{stats['total']} passed ({yield_pct:.1f}%)")
            print(f"      {failed} failures")
    
    # Identify bottleneck
    if sorted_ops:
        worst_op, worst_stats = sorted_ops[0]
        worst_yield = (worst_stats["passed"] / worst_stats["total"]) * 100 if worst_stats["total"] > 0 else 0
        print(f"\n⚠ Bottleneck: {worst_op} ({worst_yield:.1f}% yield)")
    
    print("=" * 60)


def example_3_calculate_cpk(api: pyWATS):
    """
    Step 3: Calculate Cpk (Process Capability Index).
    
    Measures how well process fits within specifications.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Cpk Calculation")
    print("=" * 60)
    
    # Example: 5V power supply measurements
    print("Parameter: 5V Rail Voltage")
    print("Specification: 4.9V - 5.1V (target: 5.0V)\n")
    
    # Simulate collected measurements (in practice, query from reports)
    measurements = [
        5.01, 5.02, 4.99, 5.00, 5.03,
        4.98, 5.01, 5.00, 4.99, 5.02,
        5.01, 5.00, 4.98, 5.03, 5.01,
        4.99, 5.02, 5.00, 5.01, 4.98
    ]
    
    # Specification limits
    lower_spec = 4.9
    upper_spec = 5.1
    target = 5.0
    
    # Calculate statistics
    mean = statistics.mean(measurements)
    stdev = statistics.stdev(measurements)
    
    # Calculate Cpk
    cpu = (upper_spec - mean) / (3 * stdev)  # Upper capability
    cpl = (mean - lower_spec) / (3 * stdev)  # Lower capability
    cpk = min(cpu, cpl)  # Cpk is the minimum
    
    print(f"Sample size: {len(measurements)}")
    print(f"Mean: {mean:.4f}V")
    print(f"Std Dev: {stdev:.4f}V")
    print(f"\nCpk = {cpk:.2f}")
    
    # Interpret Cpk
    if cpk >= 1.67:
        interpretation = "Excellent (5-sigma capable)"
    elif cpk >= 1.33:
        interpretation = "Good (4-sigma capable)"
    elif cpk >= 1.00:
        interpretation = "Adequate (3-sigma capable)"
    else:
        interpretation = "Poor (expect failures)"
    
    print(f"Interpretation: {interpretation}")
    
    # Show what Cpk means in practice
    if cpk >= 1.33:
        print(f"\n✓ Process is capable")
        print(f"  Expected defect rate: < 63 PPM")
    else:
        print(f"\n⚠ Process needs improvement")
        print(f"  Expect significant defects")
    
    print("=" * 60)
    
    return cpk


def example_4_pareto_analysis(api: pyWATS):
    """
    Step 4: Pareto analysis of failure modes.
    
    Identify the vital few causes of failures.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Pareto Analysis (Failure Modes)")
    print("=" * 60)
    
    # Simulate failure data (in practice, query from reports)
    failure_modes = {
        "Voltage out of spec": 45,
        "Component not seated": 28,
        "Solder defect": 15,
        "Visual defect": 8,
        "Firmware load failure": 3,
        "Connector damage": 1
    }
    
    total_failures = sum(failure_modes.values())
    
    print(f"Total failures analyzed: {total_failures}\n")
    print("Failure Mode Analysis:")
    
    # Sort by count (descending)
    sorted_failures = sorted(
        failure_modes.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    cumulative_pct = 0
    
    for i, (mode, count) in enumerate(sorted_failures, 1):
        percent = (count / total_failures) * 100
        cumulative_pct += percent
        
        # Bar chart visualization
        bar = "█" * int(percent / 2)  # Scale down for display
        
        print(f"{i}. {mode}")
        print(f"   Count: {count} ({percent:.1f}%)")
        print(f"   Cumulative: {cumulative_pct:.1f}%")
        print(f"   {bar}")
        
        # Mark 80% threshold
        if cumulative_pct >= 80 and i < len(sorted_failures):
            print(f"\n   ↑ 80% of failures (focus here)")
            print()
    
    # Recommendation
    top_3 = sorted_failures[:3]
    top_3_count = sum(f[1] for f in top_3)
    top_3_pct = (top_3_count / total_failures) * 100
    
    print(f"\n📊 Recommendation:")
    print(f"   Focus on top 3 failure modes")
    print(f"   Will address {top_3_pct:.1f}% of all failures:")
    for mode, _ in top_3:
        print(f"     • {mode}")
    
    print("=" * 60)


def example_5_trend_analysis(api: pyWATS):
    """
    Step 5: Analyze trends over time.
    
    Detect process drift or improvement.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Trend Analysis")
    print("=" * 60)
    
    # Simulate weekly yield data
    weeks = [
        {"week": "Week 1", "yield": 89.5},
        {"week": "Week 2", "yield": 91.2},
        {"week": "Week 3", "yield": 92.8},
        {"week": "Week 4", "yield": 94.1},
        {"week": "Week 5", "yield": 95.3},
        {"week": "Week 6", "yield": 96.0}
    ]
    
    print("Weekly Yield Trend:\n")
    
    for w in weeks:
        # Visual bar
        bar = "█" * int(w["yield"] / 2)
        print(f"{w['week']}: {w['yield']:.1f}%  {bar}")
    
    # Calculate trend
    first_yield = weeks[0]["yield"]
    last_yield = weeks[-1]["yield"]
    improvement = last_yield - first_yield
    
    print(f"\nTrend Analysis:")
    print(f"  Initial: {first_yield:.1f}%")
    print(f"  Current: {last_yield:.1f}%")
    print(f"  Improvement: +{improvement:.1f} percentage points")
    
    if improvement > 2:
        print(f"  Status: ✓ Positive trend (improving)")
    elif improvement < -2:
        print(f"  Status: ⚠ Negative trend (degrading)")
    else:
        print(f"  Status: → Stable")
    
    print("=" * 60)


def example_6_control_chart(api: pyWATS):
    """
    Step 6: Create statistical process control (SPC) chart.
    
    Monitor process stability with control limits.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Control Chart (SPC)")
    print("=" * 60)
    
    # Simulate voltage measurements over time
    measurements = [
        5.01, 5.02, 4.99, 5.00, 5.03,
        4.98, 5.01, 5.00, 4.99, 5.02,
        5.01, 5.00, 4.98, 5.03, 5.01,
        4.99, 5.02, 5.00, 5.01, 4.98,
        5.00, 5.01, 4.99, 5.02, 5.00
    ]
    
    print("Parameter: 5V Rail Voltage")
    print(f"Sample size: {len(measurements)}\n")
    
    # Calculate control limits
    mean = statistics.mean(measurements)
    stdev = statistics.stdev(measurements)
    
    ucl = mean + (3 * stdev)  # Upper Control Limit
    lcl = mean - (3 * stdev)  # Lower Control Limit
    
    print(f"Control Limits (±3σ):")
    print(f"  UCL: {ucl:.4f}V")
    print(f"  Mean: {mean:.4f}V")
    print(f"  LCL: {lcl:.4f}V")
    
    # Check for out-of-control points
    out_of_control = [m for m in measurements if m > ucl or m < lcl]
    
    print(f"\nProcess Status:")
    if len(out_of_control) == 0:
        print(f"  ✓ In Control")
        print(f"  All points within ±3σ limits")
    else:
        print(f"  ⚠ Out of Control")
        print(f"  {len(out_of_control)} points outside limits")
        print(f"  Action: Investigate special causes")
    
    # Simple visualization
    print(f"\nControl Chart:")
    print(f"  UCL ({ucl:.2f}) ┄┄┄┄┄┄┄┄┄┄┄┄┄")
    
    for i, m in enumerate(measurements[:10], 1):  # Show first 10
        offset = int((m - lcl) / (ucl - lcl) * 20)
        chart = " " * offset + "●"
        
        status = ""
        if m > ucl or m < lcl:
            status = " ⚠ OUT"
        
        print(f"  {i:2d}. {chart}  {m:.2f}V{status}")
    
    print(f"  ... ({len(measurements) - 10} more points)")
    print(f"  LCL ({lcl:.2f}) ┄┄┄┄┄┄┄┄┄┄┄┄┄")
    
    print("=" * 60)


def example_7_first_pass_yield(api: pyWATS):
    """
    Step 7: Calculate First Pass Yield (FPY).
    
    Measures efficiency (units passing without rework).
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 7: First Pass Yield (FPY)")
    print("=" * 60)
    
    # Simulate production data
    total_units = 1000
    passed_first_time = 920
    reworked_and_passed = 65
    scrapped = 15
    
    print(f"Production Summary:")
    print(f"  Total units started: {total_units}")
    print(f"  Passed first time: {passed_first_time}")
    print(f"  Reworked & passed: {reworked_and_passed}")
    print(f"  Scrapped: {scrapped}")
    
    # Calculate yields
    fpy = (passed_first_time / total_units) * 100
    final_yield = ((passed_first_time + reworked_and_passed) / total_units) * 100
    
    print(f"\nMetrics:")
    print(f"  First Pass Yield (FPY): {fpy:.1f}%")
    print(f"  Final Yield: {final_yield:.1f}%")
    print(f"  Rework Rate: {(reworked_and_passed / total_units) * 100:.1f}%")
    print(f"  Scrap Rate: {(scrapped / total_units) * 100:.1f}%")
    
    # Cost impact
    print(f"\nCost Impact:")
    print(f"  Units needing rework: {reworked_and_passed}")
    print(f"  If rework costs $50/unit:")
    print(f"    Rework cost: ${reworked_and_passed * 50:,}")
    
    # Improvement opportunity
    improvement_units = total_units - passed_first_time
    print(f"\nImprovement Opportunity:")
    print(f"  {improvement_units} units did not pass first time")
    print(f"  Improving FPY by 5% would save:")
    print(f"    50 reworks × $50 = $2,500 per 1000 units")
    
    print("=" * 60)


def example_8_dashboard_summary(api: pyWATS):
    """
    Step 8: Create executive dashboard summary.
    
    Combines key metrics for management reporting.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Executive Dashboard")
    print("=" * 60)
    
    # Simulate data from various analytics
    dashboard_data = {
        "period": "January 2026",
        "total_units": 4500,
        "yield": 95.2,
        "fpy": 91.5,
        "top_product": "WIDGET-2000",
        "top_product_yield": 96.8,
        "lowest_product": "SENSOR-100",
        "lowest_product_yield": 89.3,
        "critical_parameter": "5V Rail Voltage",
        "cpk": 1.67,
        "top_failure": "Voltage out of spec",
        "top_failure_count": 45
    }
    
    print(f"📊 Production Analytics Dashboard")
    print(f"   Period: {dashboard_data['period']}\n")
    
    print("=" * 60)
    print("PRODUCTION SUMMARY")
    print("=" * 60)
    print(f"Total Units Produced: {dashboard_data['total_units']:,}")
    print(f"Overall Yield: {dashboard_data['yield']:.1f}%")
    print(f"First Pass Yield: {dashboard_data['fpy']:.1f}%")
    
    print("\n" + "=" * 60)
    print("PRODUCT PERFORMANCE")
    print("=" * 60)
    print(f"Best Performer:")
    print(f"  {dashboard_data['top_product']}: {dashboard_data['top_product_yield']:.1f}% yield")
    print(f"\nNeeds Attention:")
    print(f"  {dashboard_data['lowest_product']}: {dashboard_data['lowest_product_yield']:.1f}% yield")
    
    print("\n" + "=" * 60)
    print("PROCESS CAPABILITY")
    print("=" * 60)
    print(f"Critical Parameter: {dashboard_data['critical_parameter']}")
    print(f"Cpk: {dashboard_data['cpk']:.2f} (Excellent)")
    print(f"Status: ✓ Process capable")
    
    print("\n" + "=" * 60)
    print("TOP FAILURE MODE")
    print("=" * 60)
    print(f"Issue: {dashboard_data['top_failure']}")
    print(f"Occurrences: {dashboard_data['top_failure_count']}")
    print(f"Action: Root cause analysis recommended")
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    print("1. Continue monitoring SENSOR-100 yield")
    print("2. Maintain current process for WIDGET-2000")
    print("3. Investigate voltage spec failures")
    print("4. Target 96% overall yield next month")
    
    print("=" * 60)


def main():
    """Run all analytics examples."""
    # Connect to WATS API
    api_url = os.getenv("WATS_API_URL", "http://localhost:8080")
    username = os.getenv("WATS_USERNAME", "admin")
    password = os.getenv("WATS_PASSWORD", "admin")
    
    print("Connecting to WATS API...")
    api = pyWATS(api_url, username, password)
    
    print("=" * 60)
    print("ANALYTICS DOMAIN EXAMPLES")
    print("Demonstrates yield, Cpk, and statistical analysis")
    print("=" * 60)
    
    # Run examples
    example_1_calculate_yield(api)
    example_2_yield_by_operation(api)
    example_3_calculate_cpk(api)
    example_4_pareto_analysis(api)
    example_5_trend_analysis(api)
    example_6_control_chart(api)
    example_7_first_pass_yield(api)
    example_8_dashboard_summary(api)
    
    print("\n" + "=" * 60)
    print("ALL EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
