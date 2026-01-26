# MCP Server Recommendations for pyWATS

## Background

An MCP (Model Context Protocol) server was previously implemented but removed due to critical architectural issues and limited value. This document provides guidance on whether and how to build a proper MCP server for pyWATS in the future.

## Should You Build an MCP Server?

### **TL;DR: Only if you have a specific AI assistant use case that requires real-time interactive access.**

### Good Use Cases for MCP

Build an MCP server if you need:

1. **Interactive AI Development Assistant**
   - AI helps debug test failures in real-time during development
   - AI generates UUT/UUR reports with domain-specific guidance
   - AI analyzes trends and suggests process improvements interactively

2. **Real-time AI Tooling Integration**
   - VS Code/Claude Desktop integration for developers
   - AI-powered dashboards that need live WATS data
   - Conversational interfaces for non-technical users

3. **Guided Workflow Automation**
   - AI walks users through complex report generation
   - AI provides context-aware suggestions based on current WATS state
   - AI helps with multi-step operations requiring decision points

### **Don't Build MCP If:**

- You just want to automate data processing → Use the Python API directly
- You need scheduled reports → Use the API in cron jobs/scripts
- You want CI/CD integration → Use the API in pipeline scripts
- You need a web interface → Build a proper web app with the API

**Key Insight:** MCP is for **interactive AI assistance**, not general automation. If a script would work, use a script.

---

## Critical Design Requirements

If you do build an MCP server, you **must** address these issues from the failed implementation:

### 1. **Use the Async API Properly**

**Problem:** The previous implementation used the synchronous `pyWATS` class inside async MCP tools, causing blocking calls that freeze the event loop.

**Solution:**
```python
# ❌ WRONG - Blocks the event loop
class MCPServer:
    def __init__(self):
        self.api = pyWATS(base_url, token)  # Sync API
    
    @tool
    async def get_product(self, name: str):
        return self.api.product.get_product(name)  # Blocks!

# ✅ CORRECT - Use async API
class MCPServer:
    def __init__(self):
        self.api = None  # Will be initialized in async context
    
    async def initialize(self):
        from pywats.async_service import AsyncProductService
        self.product_service = AsyncProductService(base_url, token)
    
    @tool
    async def get_product(self, name: str):
        return await self.product_service.get_product(name)
```

**Import from:**
- `from pywats.async_service import AsyncProductService`
- `from pywats.async_service import AsyncReportService`
- etc. for all async services

### 2. **Implement Proper Lifecycle Management**

**Problem:** No connection pooling, session management, or cleanup.

**Solution:**
```python
class MCPServer:
    def __init__(self):
        self.services = {}
        self.session = None
    
    async def __aenter__(self):
        """Initialize async resources"""
        import aiohttp
        self.session = aiohttp.ClientSession()
        
        # Initialize all services with shared session
        from pywats.async_service import AsyncProductService
        self.services['product'] = AsyncProductService(
            base_url=self.base_url,
            token=self.token,
            session=self.session  # Share session
        )
        return self
    
    async def __aexit__(self, *args):
        """Clean up resources"""
        if self.session:
            await self.session.close()
```

### 3. **Implement Pagination and Limits**

**Problem:** Tools returned unlimited data, causing massive payloads.

**Solution:**
```python
@tool
async def search_reports(
    self,
    query: str,
    limit: int = 10,      # Default reasonable limit
    offset: int = 0
) -> dict:
    """Search for reports with pagination
    
    Args:
        query: Search query
        limit: Max results (default 10, max 100)
        offset: Skip this many results
    """
    if limit > 100:
        limit = 100  # Enforce maximum
    
    # Implement pagination in API call
    results = await self.services['report'].search_reports(
        query=query,
        limit=limit,
        offset=offset
    )
    
    return {
        "results": results,
        "returned": len(results),
        "offset": offset,
        "query": query
    }
```

### 4. **Add Robust Error Handling**

**Problem:** No error handling - exceptions crash the server.

**Solution:**
```python
@tool
async def get_product(self, name: str) -> dict:
    """Get product by name with proper error handling"""
    try:
        product = await self.services['product'].get_product(name)
        if not product:
            return {
                "success": False,
                "error": f"Product '{name}' not found",
                "error_type": "NotFound"
            }
        return {
            "success": True,
            "product": product
        }
    
    except aiohttp.ClientError as e:
        return {
            "success": False,
            "error": f"Network error: {str(e)}",
            "error_type": "NetworkError"
        }
    
    except Exception as e:
        # Log the full traceback
        import logging
        logging.exception("Unexpected error in get_product")
        
        return {
            "success": False,
            "error": f"Internal error: {str(e)}",
            "error_type": "InternalError"
        }
```

### 5. **Validate Input Parameters**

**Problem:** No input validation - invalid data causes exceptions.

**Solution:**
```python
from pydantic import BaseModel, Field, field_validator

class ReportSearchParams(BaseModel):
    """Validated parameters for report search"""
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    
    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()

@tool
async def search_reports(self, params: ReportSearchParams) -> dict:
    """Search with validated parameters"""
    # params.query, params.limit, params.offset are all validated
    ...
```

---

## Recommended Architecture

If building an MCP server, use this architecture:

```
┌─────────────────────────────────────────┐
│         MCP Server (Separate Repo)      │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │
│  │   MCP Tools Layer                 │  │
│  │   - Input validation (Pydantic)   │  │
│  │   - Error handling                │  │
│  │   - Response formatting           │  │
│  │   - Pagination logic              │  │
│  └───────────────────────────────────┘  │
│              ↓                          │
│  ┌───────────────────────────────────┐  │
│  │   Domain Logic Layer              │  │
│  │   - UUT/UUR report generation     │  │
│  │   - Multi-step workflows          │  │
│  │   - Context management            │  │
│  └───────────────────────────────────┘  │
│              ↓                          │
│  ┌───────────────────────────────────┐  │
│  │   pyWATS Async Services           │  │
│  │   - AsyncProductService           │  │
│  │   - AsyncReportService            │  │
│  │   - Shared aiohttp session        │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
             ↓ HTTPS
┌─────────────────────────────────────────┐
│         WATS Server                      │
└─────────────────────────────────────────┘
```

### Why Separate Repository?

**Keep MCP server separate from pyWATS core:**

1. **Different Release Cycles:** MCP tools evolve with AI use cases, not API changes
2. **Optional Dependency:** Most users won't need MCP - don't bloat the core package
3. **Different Testing:** MCP needs LLM integration tests, different from API unit tests
4. **Clear Boundaries:** Core API stays focused on WATS integration, MCP handles AI layer

**Structure:**
```
pywats-mcp/  (separate repo)
├── pyproject.toml
│   dependencies: pywats-api>=0.1.0, mcp>=1.0.0
├── src/pywats_mcp/
│   ├── server.py          # MCP server implementation
│   ├── tools/             # MCP tool definitions
│   ├── workflows/         # Multi-step AI workflows
│   └── validators/        # Input validation
└── tests/
    ├── unit/              # Tool unit tests
    └── integration/       # E2E tests with WATS
```

---

## High-Value MCP Tools to Build

Focus on tools that **add value beyond the raw API**:

### 1. **UUT/UUR Report Generator** ⭐⭐⭐
```python
@tool
async def generate_uut_report(
    self,
    serial_number: str,
    include_attachments: bool = False,
    format: Literal["text", "json", "markdown"] = "markdown"
) -> str:
    """
    Generate a comprehensive UUT test report with domain context.
    
    This tool provides MORE than just API data:
    - Formats test results in human-readable structure
    - Explains test step outcomes in plain language
    - Highlights failures with context
    - Suggests common failure causes
    - Links related documentation
    
    Perfect for: AI-assisted debugging, failure analysis, customer reports
    """
```

**Why valuable:** Raw API returns JSON - this formats it, adds context, explains results.

### 2. **Trend Analysis Assistant** ⭐⭐⭐
```python
@tool
async def analyze_failure_trends(
    self,
    product_name: str,
    days: int = 7,
    min_failures: int = 3
) -> dict:
    """
    Identify recurring failure patterns with statistical analysis.
    
    Combines multiple API calls:
    1. Get product UURs from last N days
    2. Group by test step name
    3. Calculate failure rates
    4. Identify anomalies (sudden spikes)
    5. Suggest root causes based on patterns
    
    Perfect for: Quality engineers, production managers
    """
```

**Why valuable:** Requires multiple API calls + analysis logic. AI can then suggest actions.

### 3. **Multi-Step Workflow Helper** ⭐⭐
```python
@tool
async def setup_new_product_testing(
    self,
    product_name: str,
    test_steps: List[str],
    create_sequences: bool = True
) -> dict:
    """
    Guide through setting up a new product for testing.
    
    Multi-step workflow:
    1. Check if product exists (if not, explain how to create)
    2. Validate test step names
    3. Optionally create test sequences
    4. Verify configuration
    5. Provide next steps
    
    Perfect for: Onboarding new test engineers
    """
```

**Why valuable:** Guides users through complex multi-step processes with validation.

### 4. **Smart Search with Context** ⭐⭐
```python
@tool
async def search_reports_with_context(
    self,
    description: str,  # Natural language: "failed power tests yesterday"
    max_results: int = 10
) -> dict:
    """
    Convert natural language to precise API filters.
    
    Examples:
    - "failed power tests yesterday" → status=Failed, step contains "power", date=yesterday
    - "all UUTs for product X this week" → product=X, date_range=this_week
    - "reports with attachments" → has_attachments=true
    
    Perfect for: Non-technical users, exploratory analysis
    """
```

**Why valuable:** Natural language → structured API calls. AI can interpret intent.

---

## Don't Duplicate Simple API Calls

**❌ Don't build MCP tools that just wrap API methods 1:1:**

```python
# ❌ BAD - No added value
@tool
async def get_product(self, name: str) -> dict:
    """Get product by name"""
    return await self.product_service.get_product(name)

# This is just:
# api.product.get_product(name)
# No benefit for AI - it could call the API directly with a Python code tool
```

**✅ Build tools that add value:**
- Combine multiple API calls
- Add domain knowledge/context
- Format for human consumption
- Validate and guide workflows
- Provide explanations and suggestions

---

## Example: Proper MCP Tool Implementation

Here's a complete example showing all best practices:

```python
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
import aiohttp
from typing import Literal
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# Validated Input Models
# ============================================================================

class UUTReportParams(BaseModel):
    """Parameters for UUT report generation"""
    serial_number: str = Field(..., min_length=1, max_length=100)
    include_steps: bool = Field(default=True)
    include_measurements: bool = Field(default=True)
    format: Literal["markdown", "json", "text"] = Field(default="markdown")

# ============================================================================
# MCP Server
# ============================================================================

class PyWATSMCPServer:
    """MCP Server for WATS AI Integration"""
    
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
        self.session: aiohttp.ClientSession | None = None
        self.services = {}
        
    async def __aenter__(self):
        """Initialize async resources"""
        self.session = aiohttp.ClientSession()
        
        # Initialize async services
        from pywats.async_service import AsyncReportService
        self.services['report'] = AsyncReportService(
            base_url=self.base_url,
            token=self.token,
            session=self.session
        )
        
        logger.info("MCP Server initialized")
        return self
    
    async def __aexit__(self, *args):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        logger.info("MCP Server shut down")
    
    # ========================================================================
    # MCP Tools
    # ========================================================================
    
    @Tool(
        name="generate_uut_report",
        description="Generate comprehensive UUT test report with formatted results and failure analysis"
    )
    async def generate_uut_report(self, params: UUTReportParams) -> dict:
        """Generate formatted UUT test report
        
        Args:
            params: Validated parameters
            
        Returns:
            Success/error response with formatted report
        """
        try:
            # Validate serial number format (example)
            if not params.serial_number.isalnum():
                return {
                    "success": False,
                    "error": "Serial number must be alphanumeric",
                    "error_type": "ValidationError"
                }
            
            # Get UUT data from API
            uut = await self.services['report'].get_uut_report(
                params.serial_number
            )
            
            if not uut:
                return {
                    "success": False,
                    "error": f"UUT {params.serial_number} not found",
                    "error_type": "NotFound"
                }
            
            # Format based on requested format
            if params.format == "markdown":
                report = self._format_uut_markdown(uut, params)
            elif params.format == "json":
                report = uut  # Return raw data
            else:
                report = self._format_uut_text(uut, params)
            
            return {
                "success": True,
                "serial_number": params.serial_number,
                "report": report,
                "format": params.format
            }
        
        except aiohttp.ClientError as e:
            logger.error(f"Network error fetching UUT {params.serial_number}: {e}")
            return {
                "success": False,
                "error": f"Network error: {str(e)}",
                "error_type": "NetworkError"
            }
        
        except Exception as e:
            logger.exception(f"Unexpected error generating UUT report")
            return {
                "success": False,
                "error": f"Internal error: {str(e)}",
                "error_type": "InternalError"
            }
    
    # ========================================================================
    # Formatting Helpers (Add value beyond raw API)
    # ========================================================================
    
    def _format_uut_markdown(self, uut: dict, params: UUTReportParams) -> str:
        """Format UUT data as readable markdown"""
        lines = [
            f"# UUT Test Report: {uut['serial_number']}",
            "",
            f"**Status:** {uut['status']}",
            f"**Tested:** {uut['test_date']}",
            f"**Product:** {uut['product_name']}",
            "",
        ]
        
        if params.include_steps and 'steps' in uut:
            lines.append("## Test Steps")
            lines.append("")
            
            for step in uut['steps']:
                status_emoji = "✅" if step['passed'] else "❌"
                lines.append(f"{status_emoji} **{step['name']}**")
                
                if not step['passed']:
                    lines.append(f"   - Error: {step.get('error_message', 'N/A')}")
                
                if params.include_measurements and 'measurements' in step:
                    for meas in step['measurements']:
                        lines.append(f"   - {meas['name']}: {meas['value']} {meas['unit']}")
                
                lines.append("")
        
        if not uut['passed']:
            lines.append("## Failure Analysis")
            lines.append("")
            lines.append(self._suggest_failure_causes(uut))
        
        return "\n".join(lines)
    
    def _suggest_failure_causes(self, uut: dict) -> str:
        """Add domain knowledge - suggest common causes"""
        # This adds VALUE - it's not just API data
        suggestions = []
        
        failed_steps = [s for s in uut.get('steps', []) if not s['passed']]
        
        for step in failed_steps:
            name = step['name'].lower()
            if 'power' in name:
                suggestions.append("- Check power supply connections and voltage levels")
            elif 'communication' in name or 'comm' in name:
                suggestions.append("- Verify cable connections and communication settings")
            elif 'calibration' in name:
                suggestions.append("- Run calibration procedure or check reference values")
        
        if not suggestions:
            suggestions.append("- Review test step details and error messages above")
            suggestions.append("- Check for similar failures in recent UURs")
        
        return "\n".join(suggestions)
```

---

## Testing Strategy

**Test MCP tools properly:**

```python
# tests/test_uut_report_tool.py
import pytest
from pywats_mcp.server import PyWATSMCPServer

@pytest.mark.asyncio
async def test_generate_uut_report_success(mock_wats_server):
    """Test successful UUT report generation"""
    async with PyWATSMCPServer(
        base_url=mock_wats_server.url,
        token="test-token"
    ) as server:
        params = UUTReportParams(
            serial_number="TEST123",
            format="markdown"
        )
        
        result = await server.generate_uut_report(params)
        
        assert result["success"] is True
        assert "TEST123" in result["report"]
        assert "# UUT Test Report" in result["report"]

@pytest.mark.asyncio
async def test_generate_uut_report_not_found():
    """Test handling of missing UUT"""
    async with PyWATSMCPServer(...) as server:
        params = UUTReportParams(serial_number="NONEXISTENT")
        
        result = await server.generate_uut_report(params)
        
        assert result["success"] is False
        assert result["error_type"] == "NotFound"
        assert "not found" in result["error"].lower()
```

---

## Deployment Recommendations

1. **Separate Package:** `pywats-mcp` as its own PyPI package
2. **Version Pinning:** Pin to specific `pywats-api` versions
3. **Docker Image:** Provide official Docker image
4. **Documentation:** Comprehensive examples of AI assistant integration
5. **Monitoring:** Log all tool calls for debugging

---

## When to Revisit This

Build an MCP server when you have:

1. **Concrete use case:** "I want AI to help me generate failure analysis reports"
2. **User demand:** Customers/developers asking for AI integration
3. **Resources:** Time to build it properly (not a quick hack)

**Don't build it:**
- As a tech demo
- "Because MCP is cool"
- Without clear value proposition

---

## Summary

| Question | Answer |
|----------|---------|
| Should I build an MCP server? | Only for interactive AI assistance use cases |
| Can I reuse the old code? | No - it had critical async/sync bugs |
| What's the #1 priority? | Use async API properly (no blocking calls) |
| Where should it live? | Separate repository: `pywats-mcp` |
| What tools should I build? | UUT reports, trend analysis, workflows - not simple API wrappers |
| How do I test it? | Async unit tests + integration tests with mock WATS server |

**Final Advice:** Only build this if you have a specific AI assistant use case that will genuinely help users. If you do build it, do it properly - async all the way, proper error handling, pagination, and value-adding tools. The old implementation was fundamentally broken; start fresh if you go this route.
