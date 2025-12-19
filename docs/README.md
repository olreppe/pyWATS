# Documentation Index

## Getting Started

New to pyWATS? Start here:

1. **[README](../README.md)** - Installation and quick start
2. **[Architecture Overview](ARCHITECTURE.md)** - Understand the system design
3. **[Report Module Guide](usage/REPORT_MODULE.md)** - Most commonly used module ⭐

## Domain Knowledge (For AI Agents)

Essential understanding of WATS concepts for AI agents:

- **[WATS Domain Knowledge](WATS_DOMAIN_KNOWLEDGE.md)** ⭐ Critical for agents
  - Process/test_operation context
  - RTY (Rolled Throughput Yield)
  - Top runners
  - Unit verification rules
  - How to handle ambiguous yield questions

- **[Yield Metrics Guide](YIELD_METRICS_GUIDE.md)** ⭐ Helpdesk article
  - FPY, SPY, TPY, LPY (unit-based yield)
  - TRY (report-based yield)
  - RTY (rolled throughput yield)
  - Unit Inclusion Rule
  - Repair Line Problem
  - When to use each metric

## API Architecture

Understanding how pyWATS is built:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete architecture guide
  - Layered design (Facade → Service → Repository → Models)
  - Domain structure
  - Error handling
  - Best practices

## Module Usage Guides

Detailed guides for each domain module:

### Core Modules

- **[Report Module](usage/REPORT_MODULE.md)** ⭐ Most Important
  - Creating test reports with factory methods (`TestUUT`)
  - All step types (Numeric, Boolean, String, Chart, etc.)
  - UUR (repair) reports
  - Querying reports
  - **Start here for test automation**

- **[Product Module](usage/PRODUCT_MODULE.md)**
  - Product/part management
  - Revisions and states
  - BOM (Bill of Materials)
  - Box build templates
  - Product tags

- **[Production Module](usage/PRODUCTION_MODULE.md)**
  - Serial number management
  - Unit tracking and phases
  - Assembly operations
  - Production verification
  - Change history

### Supporting Modules

- **Asset Module** (coming soon) - Test equipment tracking
- **RootCause Module** (coming soon) - Issue ticketing
- **App Module** (coming soon) - Statistics and KPIs
- **Software Module** (coming soon) - Software distribution

## Technical Documentation

### API Design

- **[Connection Architecture](CONNECTION_ARCHITECTURE.md)**
  - HTTP client design
  - Authentication
  - Connection management
  - Retry logic

- **[Step Graph Model](STEP_GRAPH_MODEL.md)**
  - Test step hierarchy
  - Step types and structure
  - Report model design

### Converter System

- **[Converter Architecture](CONVERTER_ARCHITECTURE.md)**
  - File monitoring
  - Converter plugins
  - Queue management
  - Error handling

- **[Converter Quick Reference](../CONVERTER_QUICK_REFERENCE.md)**
  - Quick guide for converter development
  - Common patterns

### Client Application

- **[GUI Configuration](../src/pywats_client/GUI_CONFIGURATION.md)**
  - Tab visibility settings
  - Debug logging integration
  - Multi-instance support

- **[Headless Operation Guide](../src/pywats_client/control/HEADLESS_GUIDE.md)** ⭐
  - CLI commands reference
  - HTTP control API
  - Raspberry Pi setup
  - systemd service configuration
  - Docker deployment

### REST API

- **[REST API Instructions](REST_API_INSTRUCTION.md)**
  - Direct REST API usage
  - Endpoint reference
  - Authentication details

- **[API Specifications](api_specs/)**
  - OpenAPI/Swagger specs
  - Full endpoint documentation

## Quick References

- **[Quick Reference](../QUICK_REFERENCE.md)** - Common API patterns
- **[Timezone Solution](../TIMEZONE_SOLUTION.md)** - DateTime handling
- **[Critical Test Reference](../CRITICAL_TEST_REFERENCE.md)** - Important tests

## For AI Agents

If you're an AI agent helping with pyWATS:

### Most Important Documents

1. **[Report Module Guide](usage/REPORT_MODULE.md)** - Factory methods are KEY
   - Always use `TestUUT` factory, not manual report creation
   - Shows all step types with examples
   - Common patterns and troubleshooting

2. **[Architecture Guide](ARCHITECTURE.md)** - Understand the structure
   - Service/Repository pattern
   - Domain organization
   - Best practices

3. **[Production Module](usage/PRODUCTION_MODULE.md)** - Unit management
   - Serial number handling
   - Assembly operations
   - Verification

### Key Concepts

**Factory Pattern for Reports:**
```python
# ✓ ALWAYS use this
from pywats.tools.test_uut import TestUUT
uut = TestUUT(...)
root = uut.get_root()
root.add_numeric_step(...)
report = uut.to_report()

# ✗ NEVER create reports manually
report = UUTReport()  # Too complex, error-prone
```

**Domain Access:**
```python
# ✓ Access modules through facade
api = pyWATS(...)
api.report.send_uut_report(...)
api.product.get_product(...)

# ✗ Don't instantiate services directly
service = ReportService(...)  # Wrong
```

**Import Patterns:**
```python
# Main class
from pywats import pyWATS

# Common models
from pywats import Product, Asset, Unit

# Report models
from pywats.models import UUTReport, UURReport

# Factory (IMPORTANT!)
from pywats.tools.test_uut import TestUUT
```

## Examples

See the `examples/` directory for complete working examples:

- **[Basic Usage](examples/basic_usage.py)** - Simple API usage
- **Test Reports** - Coming soon
- **Production Workflow** - Coming soon
- **Assembly Operations** - Coming soon

## Development

### Running Tests

```bash
pytest                           # Run all tests
pytest tests/test_report.py      # Specific test file
pytest -m critical               # Critical tests only
pytest --cov=src                 # With coverage
```

### Contributing

When adding new features:

1. Follow the domain structure in `docs/ARCHITECTURE.md`
2. Add models to `domain/*/models.py`
3. Add business logic to `domain/*/service.py`
4. Add API calls to `domain/*/repository.py`
5. Export from `domain/*/__init__.py`
6. Update module usage guide in `docs/usage/`

## Need Help?

1. Check the **[Report Module Guide](usage/REPORT_MODULE.md)** - Solves 80% of questions
2. Review **[Architecture](ARCHITECTURE.md)** - Understand the design
3. Look at **[Examples](examples/)** - Working code samples
4. Check **[Quick Reference](../QUICK_REFERENCE.md)** - Common patterns

## Document Status

| Document | Status | Last Updated |
|----------|--------|--------------|
| ARCHITECTURE.md | ✅ Complete | 2025-12-12 |
| usage/REPORT_MODULE.md | ✅ Complete | 2025-12-12 |
| usage/PRODUCT_MODULE.md | ✅ Complete | 2025-12-12 |
| usage/PRODUCTION_MODULE.md | ✅ Complete | 2025-12-12 |
| usage/ASSET_MODULE.md | 🚧 Planned | - |
| usage/ROOTCAUSE_MODULE.md | 🚧 Planned | - |
| usage/APP_MODULE.md | 🚧 Planned | - |
