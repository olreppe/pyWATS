"""
Analytics Domain: Advanced Yield Analysis with DimensionBuilder

This example demonstrates using type-safe Dimension and KPI enums for analytics queries.
"""
import os
from datetime import datetime, timedelta
from pywats import pyWATS
from pywats.domains.report import WATSFilter
from pywats.domains.analytics.enums import (
    Dimension,
    KPI,
    DimensionBuilder,
    DateGrouping
)

# =============================================================================
# Setup
# =============================================================================

api = pyWATS(
    base_url=os.environ.get("WATS_BASE_URL", "https://demo.wats.com"),
    token=os.environ.get("WATS_TOKEN", "")
)


# =============================================================================
# Using DimensionBuilder for Type-Safe Dimension Queries
# =============================================================================

# Build a dimension query with type safety
dims = DimensionBuilder() \
    .add(KPI.UNIT_COUNT, desc=True) \
    .add(KPI.FPY) \
    .add(Dimension.PART_NUMBER) \
    .add(Dimension.PERIOD) \
    .build()

# Use in WATSFilter
filter_data = WATSFilter(
    dimensions=dims,
    dateStart=datetime.now() - timedelta(days=30),
    dateStop=datetime.now(),
    dateGrouping=DateGrouping.DAY,
    periodCount=30
)

yield_data = api.analytics.get_dynamic_yield(filter_data)

print("Yield by Product (using DimensionBuilder):")
for point in yield_data[:10]:
    print(f"  {point.partNumber}: FPY={point.fpy:.1f}%, Units={point.unitCount}")


# =============================================================================
# Preset Dimension Builders
# =============================================================================

# Use preset builders for common patterns
dims = DimensionBuilder.yield_by_product(include_period=True).build()

filter_data = WATSFilter(
    dimensions=dims,
    dateStart=datetime.now() - timedelta(days=7),
    dateStop=datetime.now(),
    dateGrouping=DateGrouping.DAY
)

yield_data = api.analytics.get_dynamic_yield(filter_data)

print("\nYield by Product (preset builder):")
for point in yield_data[:5]:
    print(f"  {point.partNumber}: {point.fpy:.1f}% FPY")


# =============================================================================
# Yield by Station Analysis
# =============================================================================

dims = DimensionBuilder() \
    .add(KPI.UNIT_COUNT, desc=True) \
    .add(KPI.FPY) \
    .add(Dimension.STATION_NAME) \
    .build()

filter_data = WATSFilter(
    dimensions=dims,
    dateStart=datetime.now() - timedelta(days=7),
    dateStop=datetime.now()
)

yield_data = api.analytics.get_dynamic_yield(filter_data)

print("\nYield by Station:")
for point in yield_data[:10]:
    print(f"  {point.stationName}: FPY={point.fpy:.1f}%, Units={point.unitCount}")


# =============================================================================
# Top Failing Products Analysis
# =============================================================================

# Use preset for worst-yielding products
dims = DimensionBuilder.top_failing_products().build()

filter_data = WATSFilter(
    dimensions=dims,
    dateStart=datetime.now() - timedelta(days=7),
    dateStop=datetime.now()
)

yield_data = api.analytics.get_dynamic_yield(filter_data)

print("\nTop Failing Products (lowest FPY first):")
for i, point in enumerate(yield_data[:10], 1):
    print(f"  {i}. {point.partNumber}: FPY={point.fpy:.1f}%, Units={point.unitCount}")


# =============================================================================
# Multi-Dimensional Analysis
# =============================================================================

# Analyze by product, station, and time
dims = DimensionBuilder() \
    .add(Dimension.PART_NUMBER) \
    .add(Dimension.STATION_NAME) \
    .add(Dimension.PERIOD) \
    .add(KPI.FPY) \
    .add(KPI.UNIT_COUNT, desc=True) \
    .build()

filter_data = WATSFilter(
    dimensions=dims,
    dateStart=datetime.now() - timedelta(days=7),
    dateStop=datetime.now(),
    dateGrouping=DateGrouping.DAY
)

yield_data = api.analytics.get_dynamic_yield(filter_data)

print("\nMulti-Dimensional Analysis (Product + Station + Time):")
for point in yield_data[:10]:
    print(f"  {point.period} | {point.partNumber} | {point.stationName}: "
          f"FPY={point.fpy:.1f}%, Units={point.unitCount}")


# =============================================================================
# Operator Performance Analysis
# =============================================================================

dims = DimensionBuilder() \
    .add(KPI.UNIT_COUNT, desc=True) \
    .add(KPI.FPY) \
    .add(Dimension.OPERATOR) \
    .build()

filter_data = WATSFilter(
    dimensions=dims,
    dateStart=datetime.now() - timedelta(days=7),
    dateStop=datetime.now()
)

yield_data = api.analytics.get_dynamic_yield(filter_data)

print("\nYield by Operator:")
for point in yield_data[:10]:
    print(f"  {point.operator}: FPY={point.fpy:.1f}%, Units={point.unitCount}")


# =============================================================================
# Failure Analysis by Error Code
# =============================================================================

dims = DimensionBuilder() \
    .add(Dimension.ERROR_CODE) \
    .add(KPI.FP_FAIL_COUNT, desc=True) \
    .add(Dimension.PART_NUMBER) \
    .build()

filter_data = WATSFilter(
    dimensions=dims,
    dateStart=datetime.now() - timedelta(days=7),
    dateStop=datetime.now()
)

yield_data = api.analytics.get_dynamic_yield(filter_data)

print("\nFailures by Error Code:")
for point in yield_data[:10]:
    if hasattr(point, 'errorCode') and point.errorCode:
        fail_count = point.fpFailCount if hasattr(point, 'fpFailCount') else 0
        print(f"  {point.errorCode} ({point.partNumber}): {fail_count} failures")


# =============================================================================
# Available Dimensions Reference
# =============================================================================

print("\n" + "=" * 60)
print("Available Dimensions for Analysis:")
print("=" * 60)
print("\nProduct Dimensions:")
print(f"  - {Dimension.PART_NUMBER.value} (Part number)")
print(f"  - {Dimension.PRODUCT_NAME.value} (Product name)")
print(f"  - {Dimension.PRODUCT_GROUP.value} (Product group)")
print(f"  - {Dimension.REVISION.value} (Revision)")

print("\nLocation/Station Dimensions:")
print(f"  - {Dimension.STATION_NAME.value} (Station name)")
print(f"  - {Dimension.LOCATION.value} (Location)")
print(f"  - {Dimension.PURPOSE.value} (Purpose)")

print("\nOperation Dimensions:")
print(f"  - {Dimension.TEST_OPERATION.value} (Test operation)")
print(f"  - {Dimension.PROCESS_CODE.value} (Process code)")

print("\nTime Dimension:")
print(f"  - {Dimension.PERIOD.value} (Time period - requires dateGrouping)")

print("\nProduction Dimensions:")
print(f"  - {Dimension.OPERATOR.value} (Operator)")
print(f"  - {Dimension.BATCH_NUMBER.value} (Batch number)")
print(f"  - {Dimension.FIXTURE_ID.value} (Fixture ID)")

print("\nKey Performance Indicators (KPIs):")
print(f"  - {KPI.UNIT_COUNT.value} (Total units)")
print(f"  - {KPI.FPY.value} (First pass yield %)")
print(f"  - {KPI.SPY.value} (Second pass yield %)")
print(f"  - {KPI.TPY.value} (Third pass yield %)")
print(f"  - {KPI.LPY.value} (Last pass yield %)")
print(f"  - {KPI.FP_FAIL_COUNT.value} (First pass failures)")
print("=" * 60)
