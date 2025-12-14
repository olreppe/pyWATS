"""
WATS MCP Server - Main server implementation.

Run with: python -m pywats_mcp
Or configure in Claude Desktop / VS Code settings.
"""

import os
import logging
from typing import Any
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceTemplate,
)

# Import pywats API
from pywats import pyWATS, WATSFilter

logger = logging.getLogger(__name__)

# Create server instance
server = Server("wats-mcp")

# Global API instance (configured on startup)
_api: pyWATS | None = None


def get_api() -> pyWATS:
    """Get or create the WATS API instance."""
    global _api
    if _api is None:
        base_url = os.environ.get("WATS_BASE_URL")
        token = os.environ.get("WATS_AUTH_TOKEN")
        
        if not base_url or not token:
            raise ValueError(
                "WATS_BASE_URL and WATS_AUTH_TOKEN environment variables required. "
                "Set them before running the MCP server."
            )
        
        _api = pyWATS(base_url=base_url, token=token)
    return _api


# =============================================================================
# Tools
# =============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available WATS tools."""
    return [
        Tool(
            name="wats_test_connection",
            description="Test the connection to the WATS server and get version info",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="wats_get_products",
            description="Get list of products (part numbers) from WATS. Returns product name, part number, and revision info.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of products to return (default 50)",
                        "default": 50
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="wats_get_reports",
            description="Query test reports (UUT/UUR) from WATS. Can filter by product, serial number, date range, and pass/fail status.",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Filter by product/part number"
                    },
                    "serial_number": {
                        "type": "string",
                        "description": "Filter by serial number"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["passed", "failed", "all"],
                        "description": "Filter by test status (default: all)"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Get reports from the last N days (default: 7)",
                        "default": 7
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of reports to return (default 100)",
                        "default": 100
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="wats_get_report_details",
            description="Get detailed information about a specific test report including all steps and measurements",
            inputSchema={
                "type": "object",
                "properties": {
                    "report_id": {
                        "type": "string",
                        "description": "The report ID (GUID) to retrieve"
                    }
                },
                "required": ["report_id"]
            }
        ),
        Tool(
            name="wats_get_failures",
            description="Get recent test failures with details about what failed",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Filter by product/part number"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Get failures from the last N days (default: 1)",
                        "default": 1
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of failures to return (default 50)",
                        "default": 50
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="wats_get_yield",
            description="Get yield statistics (pass rate) for a product or station",
            inputSchema={
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product/part number to get yield for"
                    },
                    "station": {
                        "type": "string",
                        "description": "Station name to get yield for"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Calculate yield over the last N days (default: 7)",
                        "default": 7
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="wats_get_assets",
            description="Get equipment/assets from WATS including calibration status",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_type": {
                        "type": "string",
                        "description": "Filter by asset type (e.g., 'Oscilloscope', 'DMM')"
                    },
                    "calibration_due": {
                        "type": "boolean",
                        "description": "Only show assets with calibration due soon"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of assets to return (default 50)",
                        "default": 50
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="wats_get_rootcause_tickets",
            description="Get RootCause tickets (issue tracking) from WATS",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["open", "closed", "all"],
                        "description": "Filter by ticket status (default: open)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of tickets to return (default 50)",
                        "default": 50
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="wats_search_serial",
            description="Search for all test history of a specific serial number",
            inputSchema={
                "type": "object",
                "properties": {
                    "serial_number": {
                        "type": "string",
                        "description": "The serial number to search for"
                    }
                },
                "required": ["serial_number"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute a WATS tool."""
    try:
        api = get_api()
        
        if name == "wats_test_connection":
            return await _tool_test_connection(api)
        elif name == "wats_get_products":
            return await _tool_get_products(api, arguments)
        elif name == "wats_get_reports":
            return await _tool_get_reports(api, arguments)
        elif name == "wats_get_report_details":
            return await _tool_get_report_details(api, arguments)
        elif name == "wats_get_failures":
            return await _tool_get_failures(api, arguments)
        elif name == "wats_get_yield":
            return await _tool_get_yield(api, arguments)
        elif name == "wats_get_assets":
            return await _tool_get_assets(api, arguments)
        elif name == "wats_get_rootcause_tickets":
            return await _tool_get_rootcause_tickets(api, arguments)
        elif name == "wats_search_serial":
            return await _tool_search_serial(api, arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
            
    except Exception as e:
        logger.exception(f"Error executing tool {name}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# =============================================================================
# Tool Implementations
# =============================================================================

async def _tool_test_connection(api: pyWATS) -> list[TextContent]:
    """Test WATS connection."""
    if api.test_connection():
        version = api.get_version()
        return [TextContent(
            type="text",
            text=f"✅ Connected to WATS server\nServer version: {version}\nBase URL: {api.base_url}"
        )]
    else:
        return [TextContent(type="text", text="❌ Connection failed")]


async def _tool_get_products(api: pyWATS, args: dict) -> list[TextContent]:
    """Get products list."""
    limit = args.get("limit", 50)
    
    products = api.product.get_products()
    
    if not products:
        return [TextContent(type="text", text="No products found")]
    
    lines = [f"Found {len(products)} products:\n"]
    for p in products[:limit]:
        name = getattr(p, 'name', 'Unknown')
        pn = getattr(p, 'partNumber', getattr(p, 'part_number', 'N/A'))
        lines.append(f"• {name} (PN: {pn})")
    
    return [TextContent(type="text", text="\n".join(lines))]


async def _tool_get_reports(api: pyWATS, args: dict) -> list[TextContent]:
    """Get test reports."""
    days = args.get("days", 7)
    limit = args.get("limit", 100)
    product = args.get("product")
    serial = args.get("serial_number")
    status = args.get("status", "all")
    
    # Build filter
    start_date = datetime.utcnow() - timedelta(days=days)
    
    filter_params = {
        "start": start_date.isoformat() + "Z",
    }
    
    if product:
        filter_params["partNumber"] = product
    if serial:
        filter_params["serialNumber"] = serial
    
    reports = api.report.query(top=limit, **filter_params)
    
    if not reports:
        return [TextContent(type="text", text=f"No reports found in the last {days} days")]
    
    # Filter by status if specified
    if status == "passed":
        reports = [r for r in reports if getattr(r, 'status', None) == 'Passed']
    elif status == "failed":
        reports = [r for r in reports if getattr(r, 'status', None) == 'Failed']
    
    lines = [f"Found {len(reports)} reports (last {days} days):\n"]
    for r in reports[:limit]:
        rid = getattr(r, 'id', 'N/A')
        sn = getattr(r, 'serialNumber', getattr(r, 'serial_number', 'N/A'))
        st = getattr(r, 'status', 'Unknown')
        pn = getattr(r, 'partNumber', getattr(r, 'part_number', 'N/A'))
        ts = getattr(r, 'startDateTime', getattr(r, 'start', 'N/A'))
        
        icon = "✅" if st == "Passed" else "❌" if st == "Failed" else "⚪"
        lines.append(f"{icon} SN: {sn} | PN: {pn} | {ts} | ID: {rid}")
    
    return [TextContent(type="text", text="\n".join(lines))]


async def _tool_get_report_details(api: pyWATS, args: dict) -> list[TextContent]:
    """Get detailed report info."""
    report_id = args.get("report_id")
    if not report_id:
        return [TextContent(type="text", text="Error: report_id is required")]
    
    report = api.report.get(report_id)
    
    if not report:
        return [TextContent(type="text", text=f"Report not found: {report_id}")]
    
    lines = [
        f"Report Details: {report_id}",
        "=" * 50,
        f"Serial Number: {getattr(report, 'serialNumber', 'N/A')}",
        f"Part Number: {getattr(report, 'partNumber', 'N/A')}",
        f"Status: {getattr(report, 'status', 'N/A')}",
        f"Start: {getattr(report, 'startDateTime', 'N/A')}",
        f"Station: {getattr(report, 'stationName', 'N/A')}",
        f"Operator: {getattr(report, 'operatorName', 'N/A')}",
        "",
        "Steps:",
        "-" * 30,
    ]
    
    # Get steps if available
    steps = getattr(report, 'steps', getattr(report, 'root', {}).get('steps', []))
    if steps:
        for step in steps[:20]:  # Limit steps shown
            step_name = getattr(step, 'name', getattr(step, 'stepName', 'Unknown'))
            step_status = getattr(step, 'status', 'Unknown')
            icon = "✅" if step_status == "Passed" else "❌" if step_status == "Failed" else "⚪"
            lines.append(f"  {icon} {step_name}")
    else:
        lines.append("  (No steps available)")
    
    return [TextContent(type="text", text="\n".join(lines))]


async def _tool_get_failures(api: pyWATS, args: dict) -> list[TextContent]:
    """Get recent failures."""
    days = args.get("days", 1)
    limit = args.get("limit", 50)
    product = args.get("product")
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    filter_params = {
        "start": start_date.isoformat() + "Z",
        "status": "Failed",
    }
    
    if product:
        filter_params["partNumber"] = product
    
    reports = api.report.query(top=limit, **filter_params)
    
    if not reports:
        return [TextContent(type="text", text=f"✅ No failures in the last {days} day(s)!")]
    
    lines = [f"❌ Found {len(reports)} failures (last {days} day(s)):\n"]
    for r in reports[:limit]:
        sn = getattr(r, 'serialNumber', 'N/A')
        pn = getattr(r, 'partNumber', 'N/A')
        ts = getattr(r, 'startDateTime', 'N/A')
        station = getattr(r, 'stationName', 'N/A')
        
        lines.append(f"• SN: {sn} | PN: {pn} | Station: {station} | {ts}")
    
    return [TextContent(type="text", text="\n".join(lines))]


async def _tool_get_yield(api: pyWATS, args: dict) -> list[TextContent]:
    """Calculate yield statistics."""
    days = args.get("days", 7)
    product = args.get("product")
    station = args.get("station")
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    filter_params = {
        "start": start_date.isoformat() + "Z",
    }
    
    if product:
        filter_params["partNumber"] = product
    
    # Get all reports for the period
    reports = api.report.query(top=1000, **filter_params)
    
    if not reports:
        return [TextContent(type="text", text=f"No data for yield calculation")]
    
    # Filter by station if specified
    if station:
        reports = [r for r in reports if getattr(r, 'stationName', '') == station]
    
    total = len(reports)
    passed = sum(1 for r in reports if getattr(r, 'status', '') == 'Passed')
    failed = total - passed
    yield_pct = (passed / total * 100) if total > 0 else 0
    
    context = []
    if product:
        context.append(f"Product: {product}")
    if station:
        context.append(f"Station: {station}")
    context_str = " | ".join(context) if context else "All products/stations"
    
    lines = [
        f"📊 Yield Statistics ({context_str})",
        f"Period: Last {days} days",
        "=" * 40,
        f"Total Tests: {total}",
        f"Passed: {passed} ✅",
        f"Failed: {failed} ❌",
        f"Yield: {yield_pct:.1f}%",
    ]
    
    return [TextContent(type="text", text="\n".join(lines))]


async def _tool_get_assets(api: pyWATS, args: dict) -> list[TextContent]:
    """Get assets/equipment."""
    limit = args.get("limit", 50)
    asset_type = args.get("asset_type")
    cal_due = args.get("calibration_due", False)
    
    assets = api.asset.get_assets()
    
    if not assets:
        return [TextContent(type="text", text="No assets found")]
    
    # Filter if needed
    if asset_type:
        assets = [a for a in assets if asset_type.lower() in getattr(a, 'type', '').lower()]
    
    if cal_due:
        now = datetime.utcnow()
        soon = now + timedelta(days=30)
        filtered = []
        for a in assets:
            cal_date = getattr(a, 'calibrationDueDate', None)
            if cal_date:
                # Parse date and check if due soon
                try:
                    if isinstance(cal_date, str):
                        cal_dt = datetime.fromisoformat(cal_date.replace('Z', '+00:00'))
                        if cal_dt.replace(tzinfo=None) <= soon:
                            filtered.append(a)
                except:
                    pass
        assets = filtered
    
    lines = [f"Found {len(assets)} assets:\n"]
    for a in assets[:limit]:
        name = getattr(a, 'name', 'Unknown')
        atype = getattr(a, 'type', 'N/A')
        serial = getattr(a, 'serialNumber', 'N/A')
        cal = getattr(a, 'calibrationDueDate', 'N/A')
        
        lines.append(f"• {name} ({atype}) | SN: {serial} | Cal Due: {cal}")
    
    return [TextContent(type="text", text="\n".join(lines))]


async def _tool_get_rootcause_tickets(api: pyWATS, args: dict) -> list[TextContent]:
    """Get RootCause tickets."""
    limit = args.get("limit", 50)
    status = args.get("status", "open")
    
    tickets = api.rootcause.get_tickets()
    
    if not tickets:
        return [TextContent(type="text", text="No tickets found")]
    
    # Filter by status
    if status == "open":
        tickets = [t for t in tickets if getattr(t, 'status', '').lower() != 'closed']
    elif status == "closed":
        tickets = [t for t in tickets if getattr(t, 'status', '').lower() == 'closed']
    
    lines = [f"Found {len(tickets)} tickets ({status}):\n"]
    for t in tickets[:limit]:
        tid = getattr(t, 'id', 'N/A')
        title = getattr(t, 'title', getattr(t, 'subject', 'No title'))
        tstatus = getattr(t, 'status', 'Unknown')
        created = getattr(t, 'createdDate', 'N/A')
        
        lines.append(f"• [{tstatus}] {title} (ID: {tid}, Created: {created})")
    
    return [TextContent(type="text", text="\n".join(lines))]


async def _tool_search_serial(api: pyWATS, args: dict) -> list[TextContent]:
    """Search test history for a serial number."""
    serial = args.get("serial_number")
    if not serial:
        return [TextContent(type="text", text="Error: serial_number is required")]
    
    reports = api.report.query(serialNumber=serial, top=100)
    
    if not reports:
        return [TextContent(type="text", text=f"No test history found for serial: {serial}")]
    
    lines = [f"Test history for serial: {serial}", f"Found {len(reports)} tests:\n"]
    
    for r in reports:
        rid = getattr(r, 'id', 'N/A')
        st = getattr(r, 'status', 'Unknown')
        pn = getattr(r, 'partNumber', 'N/A')
        ts = getattr(r, 'startDateTime', 'N/A')
        station = getattr(r, 'stationName', 'N/A')
        
        icon = "✅" if st == "Passed" else "❌" if st == "Failed" else "⚪"
        lines.append(f"{icon} {ts} | PN: {pn} | Station: {station} | ID: {rid}")
    
    return [TextContent(type="text", text="\n".join(lines))]


# =============================================================================
# Main Entry Point
# =============================================================================

async def main():
    """Run the WATS MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
