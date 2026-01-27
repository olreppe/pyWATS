"""
Tests for Unit Flow analytics (internal API)

⚠️ INTERNAL API - SUBJECT TO CHANGE ⚠️

These tests make actual API calls to the WATS server using internal endpoints.
The internal /api/internal/UnitFlow endpoints may not be available on all servers.
"""
from typing import Any
from datetime import datetime, timedelta
import pytest


class TestUnitFlowBasic:
    """Test basic Unit Flow functionality"""

    def test_get_unit_flow_with_part_number(self, wats_client: Any) -> None:
        """Test getting unit flow for a specific part number"""
        print("\n=== GET UNIT FLOW ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(
            part_number="758877.874",
            date_from=datetime.now() - timedelta(days=7),
            date_to=datetime.now(),
            include_passed=True,
            include_failed=True
        )
        
        print(f"Filter: {filter_obj.model_dump(by_alias=True, exclude_none=True)}")
        
        result = wats_client.analytics.get_unit_flow(filter_obj)
        
        print(f"Result type: {type(result)}")
        print(f"Nodes: {len(result.nodes or [])}")
        print(f"Links: {len(result.links or [])}")
        if result.total_units is not None:
            print(f"Total units: {result.total_units}")
        
        if result.nodes:
            print("\nFlow Nodes:")
            for node in result.nodes[:5]:
                yield_pct = f"{node.yield_percent:.1f}%" if node.yield_percent is not None else "N/A"
                print(f"  - {node.name}: {node.unit_count or 0} units, {yield_pct} yield")
        
        if result.links:
            print("\nFlow Links:")
            for link in result.links[:5]:
                print(f"  - {link.source_name} -> {link.target_name}: {link.unit_count or 0} units")
        
        print("====================\n")
        
        assert result is not None
        assert hasattr(result, 'nodes')
        assert hasattr(result, 'links')

    def test_get_unit_flow_minimal_filter(self, wats_client: Any) -> None:
        """Test unit flow with minimal filter"""
        print("\n=== GET UNIT FLOW (MINIMAL) ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(part_number="758877.874")
        
        result = wats_client.analytics.get_unit_flow(filter_obj)
        
        print(f"Nodes: {len(result.nodes or [])}")
        print(f"Links: {len(result.links or [])}")
        print("===============================\n")
        
        assert result is not None


class TestUnitFlowNodes:
    """Test Unit Flow nodes endpoint"""

    def test_get_flow_nodes(self, wats_client: Any) -> None:
        """Test getting flow nodes"""
        print("\n=== GET FLOW NODES ===")
        
        from pywats import UnitFlowFilter
        
        # First establish flow context
        filter_obj = UnitFlowFilter(part_number="758877.874")
        wats_client.analytics.get_unit_flow(filter_obj)
        
        # Now get nodes
        nodes = wats_client.analytics.get_flow_nodes()
        
        print(f"Retrieved {len(nodes)} nodes")
        for node in nodes[:5]:
            print(f"  - {node.name}: {node.unit_count or 0} units")
        print("======================\n")
        
        assert isinstance(nodes, list)


class TestUnitFlowLinks:
    """Test Unit Flow links endpoint"""

    def test_get_flow_links(self, wats_client: Any) -> None:
        """Test getting flow links"""
        print("\n=== GET FLOW LINKS ===")
        
        from pywats import UnitFlowFilter
        
        # First establish flow context
        filter_obj = UnitFlowFilter(part_number="758877.874")
        wats_client.analytics.get_unit_flow(filter_obj)
        
        # Now get links
        links = wats_client.analytics.get_flow_links()
        
        print(f"Retrieved {len(links)} links")
        for link in links[:5]:
            print(f"  - {link.source_name} -> {link.target_name}: {link.unit_count or 0} units")
        print("======================\n")
        
        assert isinstance(links, list)


class TestUnitFlowUnits:
    """Test Unit Flow units endpoint"""

    def test_get_flow_units(self, wats_client: Any) -> None:
        """Test getting individual units from flow"""
        print("\n=== GET FLOW UNITS ===")
        
        from pywats import UnitFlowFilter
        
        # First establish flow context
        filter_obj = UnitFlowFilter(part_number="758877.874")
        wats_client.analytics.get_unit_flow(filter_obj)
        
        # Now get units
        units = wats_client.analytics.get_flow_units()
        
        print(f"Retrieved {len(units)} units")
        for unit in units[:5]:
            print(f"  - {unit.serial_number}: {unit.status}")
        print("======================\n")
        
        assert isinstance(units, list)


class TestUnitFlowTracing:
    """Test Unit Flow serial number tracing"""

    def test_trace_serial_numbers(self, wats_client: Any) -> None:
        """Test tracing specific serial numbers through the flow"""
        print("\n=== TRACE SERIAL NUMBERS ===")
        
        from pywats import UnitFlowFilter
        
        # First get some units to find serial numbers
        filter_obj = UnitFlowFilter(part_number="758877.874")
        initial_result = wats_client.analytics.get_unit_flow(filter_obj)
        
        # Get units to find serial numbers
        units = wats_client.analytics.get_flow_units()
        
        if units and len(units) > 0:
            # Take up to 3 serial numbers
            serial_numbers = [u.serial_number for u in units[:3] if u.serial_number]
            
            if serial_numbers:
                print(f"Tracing serial numbers: {serial_numbers}")
                
                result = wats_client.analytics.trace_serial_numbers(serial_numbers)
                
                print(f"Trace result - Nodes: {len(result.nodes or [])}, Links: {len(result.links or [])}")
                
                if result.units:
                    print("\nTraced units:")
                    for unit in result.units:
                        print(f"  - {unit.serial_number}: {unit.status}")
                        if unit.node_path:
                            print(f"    Path: {' -> '.join(unit.node_path)}")
                
                assert result is not None
            else:
                print("No serial numbers found to trace")
                pytest.skip("No serial numbers available")
        else:
            print("No units found")
            pytest.skip("No units in flow")
        
        print("============================\n")


class TestUnitFlowBottlenecks:
    """Test bottleneck identification"""

    def test_get_bottlenecks(self, wats_client: Any) -> None:
        """Test identifying bottlenecks in the flow"""
        print("\n=== GET BOTTLENECKS ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(
            part_number="758877.874",
            date_from=datetime.now() - timedelta(days=7)
        )
        
        bottlenecks = wats_client.analytics.get_bottlenecks(
            filter_data=filter_obj,
            min_yield_threshold=95.0
        )
        
        print(f"Found {len(bottlenecks)} bottlenecks (yield < 95%)")
        
        if bottlenecks:
            print("\n⚠️ Potential bottlenecks:")
            for node in bottlenecks:
                print(f"  - {node.name}: {node.yield_percent:.1f}% yield")
                if node.fail_count:
                    print(f"    Failures: {node.fail_count}")
        else:
            print("✅ No bottlenecks found (all operations >= 95% yield)")
        
        print("=======================\n")
        
        assert isinstance(bottlenecks, list)

    def test_get_bottlenecks_high_threshold(self, wats_client: Any) -> None:
        """Test bottlenecks with a high threshold (99%)"""
        print("\n=== GET BOTTLENECKS (99% threshold) ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(part_number="758877.874")
        
        bottlenecks = wats_client.analytics.get_bottlenecks(
            filter_data=filter_obj,
            min_yield_threshold=99.0
        )
        
        print(f"Bottlenecks with 99% threshold: {len(bottlenecks)}")
        for node in bottlenecks[:5]:
            print(f"  - {node.name}: {node.yield_percent:.1f}%")
        
        print("=======================================\n")
        
        assert isinstance(bottlenecks, list)


class TestUnitFlowSummary:
    """Test flow summary statistics"""

    def test_get_flow_summary(self, wats_client: Any) -> None:
        """Test getting flow summary statistics"""
        print("\n=== GET FLOW SUMMARY ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(
            part_number="758877.874",
            date_from=datetime.now() - timedelta(days=7)
        )
        
        summary = wats_client.analytics.get_flow_summary(filter_obj)
        
        print(f"\nFlow Statistics:")
        print(f"  Total nodes: {summary['total_nodes']}")
        print(f"  Total links: {summary['total_links']}")
        print(f"  Total units: {summary['total_units']}")
        print(f"  Passed units: {summary['passed_units']}")
        print(f"  Failed units: {summary['failed_units']}")
        print(f"  Average yield: {summary['avg_yield']:.1f}%")
        print(f"  Min yield: {summary['min_yield']:.1f}%")
        print(f"  Max yield: {summary['max_yield']:.1f}%")
        
        print("========================\n")
        
        assert isinstance(summary, dict)
        assert 'total_nodes' in summary
        assert 'avg_yield' in summary


class TestUnitFlowSplitBy:
    """Test flow splitting by dimension"""

    def test_split_flow_by_station(self, wats_client: Any) -> None:
        """Test splitting flow by station name"""
        print("\n=== SPLIT FLOW BY STATION ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(part_number="758877.874")
        
        result = wats_client.analytics.split_flow_by("stationName", filter_obj)
        
        print(f"Split result - Nodes: {len(result.nodes or [])}")
        
        if result.nodes:
            print("\nNodes by station:")
            for node in result.nodes[:10]:
                station = node.station_name or "Unknown"
                print(f"  - {station} / {node.name}: {node.unit_count or 0} units")
        
        print("=============================\n")
        
        assert result is not None

    def test_split_flow_by_location(self, wats_client: Any) -> None:
        """Test splitting flow by location"""
        print("\n=== SPLIT FLOW BY LOCATION ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(part_number="758877.874")
        
        result = wats_client.analytics.split_flow_by("location", filter_obj)
        
        print(f"Split by location - Nodes: {len(result.nodes or [])}")
        print("==============================\n")
        
        assert result is not None


class TestUnitFlowOrdering:
    """Test unit ordering in flow"""

    def test_set_unit_order_by_start_time(self, wats_client: Any) -> None:
        """Test ordering units by start time"""
        print("\n=== ORDER BY START TIME ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(part_number="758877.874")
        
        result = wats_client.analytics.set_unit_order("startTime", filter_obj)
        
        print(f"Ordered result - Nodes: {len(result.nodes or [])}")
        print("===========================\n")
        
        assert result is not None


class TestUnitFlowVisibility:
    """Test show/hide operations"""

    def test_expand_operations(self, wats_client: Any) -> None:
        """Test expanding operations"""
        print("\n=== EXPAND OPERATIONS ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(part_number="758877.874")
        
        result = wats_client.analytics.expand_operations(True, filter_obj)
        
        print(f"Expanded view - Nodes: {len(result.nodes or [])}")
        
        if result.nodes:
            print("\nExpanded nodes:")
            for node in result.nodes[:10]:
                level_indent = "  " * (node.level or 0)
                print(f"  {level_indent}- {node.name}")
        
        print("=========================\n")
        
        assert result is not None

    def test_collapse_operations(self, wats_client: Any) -> None:
        """Test collapsing operations"""
        print("\n=== COLLAPSE OPERATIONS ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(part_number="758877.874")
        
        result = wats_client.analytics.expand_operations(False, filter_obj)
        
        print(f"Collapsed view - Nodes: {len(result.nodes or [])}")
        print("===========================\n")
        
        assert result is not None


class TestUnitFlowDateRange:
    """Test flow queries with different date ranges"""

    def test_flow_last_24_hours(self, wats_client: Any) -> None:
        """Test flow for last 24 hours"""
        print("\n=== FLOW LAST 24 HOURS ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(
            part_number="758877.874",
            date_from=datetime.now() - timedelta(hours=24),
            date_to=datetime.now()
        )
        
        result = wats_client.analytics.get_unit_flow(filter_obj)
        
        print(f"Last 24 hours - Nodes: {len(result.nodes or [])}, Links: {len(result.links or [])}")
        print("==========================\n")
        
        assert result is not None

    def test_flow_last_30_days(self, wats_client: Any) -> None:
        """Test flow for last 30 days"""
        print("\n=== FLOW LAST 30 DAYS ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(
            part_number="758877.874",
            date_from=datetime.now() - timedelta(days=30),
            date_to=datetime.now()
        )
        
        result = wats_client.analytics.get_unit_flow(filter_obj)
        
        print(f"Last 30 days - Nodes: {len(result.nodes or [])}, Links: {len(result.links or [])}")
        
        # Get summary for this period
        summary = wats_client.analytics.get_flow_summary(filter_obj)
        print(f"Summary: {summary['total_units']} units, {summary['avg_yield']:.1f}% avg yield")
        
        print("=========================\n")
        
        assert result is not None


class TestUnitFlowStatusFilter:
    """Test filtering by pass/fail status"""

    def test_flow_passed_only(self, wats_client: Any) -> None:
        """Test flow with only passed units"""
        print("\n=== FLOW PASSED ONLY ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(
            part_number="758877.874",
            include_passed=True,
            include_failed=False
        )
        
        result = wats_client.analytics.get_unit_flow(filter_obj)
        
        print(f"Passed only - Nodes: {len(result.nodes or [])}")
        print("========================\n")
        
        assert result is not None

    def test_flow_failed_only(self, wats_client: Any) -> None:
        """Test flow with only failed units"""
        print("\n=== FLOW FAILED ONLY ===")
        
        from pywats import UnitFlowFilter
        
        filter_obj = UnitFlowFilter(
            part_number="758877.874",
            include_passed=False,
            include_failed=True
        )
        
        result = wats_client.analytics.get_unit_flow(filter_obj)
        
        print(f"Failed only - Nodes: {len(result.nodes or [])}")
        print("========================\n")
        
        assert result is not None
