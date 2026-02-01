# Domain Examples

This folder contains runnable examples for each WATS domain. Each example is a complete, working script with comprehensive comments explaining domain concepts inline.

## Why Runnable Examples?

Instead of separate documentation files, these examples:
- ✅ **Always work** - They're tested code, not just documentation
- ✅ **Show real usage** - Actual patterns used in production
- ✅ **Preserve domain knowledge** - Comprehensive comments explain WATS concepts
- ✅ **Easy to copy** - Copy-paste into your project and modify

## Examples by Domain

### Core Domains

#### [report_examples.py](report_examples.py)
**Test Reports - UUT/UUR, All Step Types, Pass/Fail**

Covers:
- UUT vs UUR reports (Unit Under Test vs Unit Under Rework)
- All step types: NumericLimit, PassFail, MultipleNumeric, StringValue, MessageLog
- Creating passing and failing test reports
- Handling rework with UUR reports
- Querying report history by serial number

Run: `python report_examples.py`

---

#### [product_examples.py](product_examples.py)
**Products, Revisions, BOMs, Lifecycle Management**

Covers:
- Product hierarchy: Product → Revision → BOM
- Product lifecycle states: Development → Active → Obsolete
- Creating and managing Bills of Materials
- Product families and variants
- Querying and filtering products

Run: `python product_examples.py`

---

#### [production_examples.py](production_examples.py)
**Units, Serial Numbers, Operations, Tracking**

Covers:
- Units vs Products distinction (instance vs design)
- Creating production units with serial numbers
- Tracking units through multiple operations
- Batch production workflows
- Handling failures and rework
- Unit history and production statistics

Run: `python production_examples.py`

---

#### [box_build_examples.py](box_build_examples.py)
**Multi-Level Assemblies, Parent-Child Relationships**

Covers:
- **CRITICAL**: Templates (product domain) vs Units (production domain)
- Multi-level product assemblies
- Complete workflow: Products → Templates → Units → Assembly
- Building, querying, and disassembling units
- Parent-child unit relationships

Run: `python box_build_examples.py`

---

### Supporting Domains

#### [asset_examples.py](asset_examples.py)
**Equipment, Calibration, Maintenance Tracking**

Covers:
- Assets vs units (equipment vs products)
- Registering test and manufacturing equipment
- Calibration requirements and tracking
- Recording calibration events and certificates
- Preventive and corrective maintenance
- Asset utilization and location tracking
- Calibration expiration alerts

Run: `python asset_examples.py`

---

#### [analytics_examples.py](analytics_examples.py)
**Yield Analysis, Cpk, Statistical Process Control**

Covers:
- Yield calculation (pass rates)
- Yield by operation type (identify bottlenecks)
- Cpk (Process Capability Index) calculation
- Pareto analysis of failure modes
- Trend analysis over time
- Control charts (SPC - Statistical Process Control)
- First Pass Yield (FPY) and cost impact
- Executive dashboard reporting

Run: `python analytics_examples.py`

---

#### [software_examples.py](software_examples.py)
**Package Management, Versioning, Deployment**

Covers:
- Creating and registering software packages
- Firmware version control
- Deploying software to production units
- Tracking version history
- Software traceability and configuration management

Run: `python software_examples.py`

---

#### [rootcause_examples.py](rootcause_examples.py)
**Root Cause Analysis, CAPA, Defect Management**

Covers:
- Root cause vs symptom distinction
- Creating RCA (Root Cause Analysis) cases
- 5 Whys analysis methodology
- Implementing corrective actions
- Tracking effectiveness
- CAPA (Corrective And Preventive Action) workflows
- RCA reporting

Run: `python rootcause_examples.py`

---

#### [process_examples.py](process_examples.py)
**Operation Types, Routing, Bottleneck Analysis**

Covers:
- Operation types (manufacturing steps)
- Defining product routings (operation sequences)
- Process capacity analysis
- Identifying bottlenecks
- Cycle time tracking

Run: `python process_examples.py`

---

## Quick Reference Table

| Domain | File | Key Concepts |
|--------|------|--------------|
| **Report** | `report_examples.py` | UUT/UUR, test steps, pass/fail |
| **Product** | `product_examples.py` | Products, revisions, BOMs |
| **Production** | `production_examples.py` | Units, serials, operations |
| **Box Build** | `box_build_examples.py` | Templates vs units, assemblies |
| **Asset** | `asset_examples.py` | Equipment, calibration, maintenance |
| **Analytics** | `analytics_examples.py` | Yield, Cpk, SPC, trends |
| **Software** | `software_examples.py` | Firmware versions, deployment |
| **Root Cause** | `rootcause_examples.py` | RCA, CAPA, failure analysis |
| **Process** | `process_examples.py` | Operations, routing, bottlenecks |

## Running Examples

### Option 1: Direct Execution

All examples are standalone scripts:

```bash
python report_examples.py
python product_examples.py
python production_examples.py
# ... etc
```

### Option 2: Environment Variables

Set connection details via environment:

**Linux/Mac:**
```bash
export WATS_API_URL="http://localhost:8080"
export WATS_USERNAME="admin"
export WATS_PASSWORD="admin"
```

**Windows:**
```powershell
$env:WATS_API_URL="http://localhost:8080"
$env:WATS_USERNAME="admin"
$env:WATS_PASSWORD="admin"
```

Then run examples - they'll use these variables automatically.

### Option 3: Import and Use

Import specific examples in your code:

```python
from examples.domains.report_examples import example_1_create_simple_uut_report
from pywats import pyWATS

api = pyWATS("http://localhost:8080", "admin", "admin")
example_1_create_simple_uut_report(api)
```

## Example Structure

Each example file follows this format:

```python
"""
Domain Examples - Description

DOMAIN KNOWLEDGE: Critical Concept
===================================
Explanation of key distinction...

COMPLETE WORKFLOW:
==================
1. Step 1
2. Step 2
...
"""

def example_1_basic_concept(api: pyWATS):
    """
    Step 1: Simplest use case.
    
    Detailed explanation of what this example shows.
    """
    # Code with comprehensive inline comments
    pass

def example_2_intermediate(api: pyWATS):
    """
    Step 2: More complex scenario.
    """
    # Code with comprehensive inline comments
    pass

# ... progressive examples ...

def main():
    """Run all examples."""
    api = pyWATS(os.getenv("WATS_API_URL"), ...)
    example_1_basic_concept(api)
    example_2_intermediate(api)
    # ...

if __name__ == "__main__":
    main()
```

## Learning Path

### New to WATS?

Start with these in order:

1. **Read**: [docs/getting-started.md](../../docs/getting-started.md) - Basic concepts and setup
2. **Read**: [docs/guides/wats-concepts.md](../../docs/guides/wats-concepts.md) - Domain knowledge primer
3. **Run**: [product_examples.py](product_examples.py) - Create products and revisions
4. **Run**: [production_examples.py](production_examples.py) - Create units with serial numbers
5. **Run**: [report_examples.py](report_examples.py) - Submit test reports

### Ready for Advanced Topics?

6. **Run**: [box_build_examples.py](box_build_examples.py) - Multi-level assemblies
7. **Run**: [analytics_examples.py](analytics_examples.py) - Yield analysis and statistics
8. **Run**: [asset_examples.py](asset_examples.py) - Equipment and calibration tracking

### Building Test Converters?

- **Start with**: [report_examples.py](report_examples.py) - Understand test report structure
- **Then read**: [docs/guides/llm-converter-guide.md](../../docs/guides/llm-converter-guide.md) - Converter architecture
- **Reference**: All examples show proper API usage patterns

## Domain Knowledge Highlights

### Critical Distinctions

**Templates vs Units (Box Build)**
- Template = Design-time blueprint (product domain)
- Unit = Runtime assembly (production domain)
- See: [box_build_examples.py](box_build_examples.py)

**UUT vs UUR (Reports)**
- UUT = Unit Under Test (initial production test)
- UUR = Unit Under Rework (repair/re-test)
- See: [report_examples.py](report_examples.py)

**Assets vs Units**
- Assets = Equipment/tools you USE
- Units = Products you BUILD
- See: [asset_examples.py](asset_examples.py)

**Products vs Units**
- Product = Class/design (what you're building)
- Unit = Instance (specific serial number being built)
- See: [production_examples.py](production_examples.py)

## See Also

### Documentation
- [API Reference](../../docs/api/) - Complete API documentation (auto-generated)
- [Architecture Guide](../../docs/guides/architecture.md) - System design and integration
- [Integration Patterns](../../docs/guides/integration-patterns.md) - Practical workflows
- [WATS Concepts](../../docs/guides/wats-concepts.md) - Domain knowledge reference

### Help & Support
- [Troubleshooting](../../docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Type Hints Guide](../../docs/reference/type-hints.md) - IDE autocomplete setup
- [Getting Started](../../docs/getting-started.md) - Quick start guide

## Adding New Examples

When creating new domain examples:

1. **Follow the template**: Use existing files as reference
2. **Domain knowledge first**: Explain concepts in docstring header
3. **Progressive complexity**: Example 1 = simplest, Example N = most complex
4. **Comprehensive comments**: Explain WHY, not just WHAT
5. **Complete workflows**: Show end-to-end scenarios
6. **Make it runnable**: Ensure examples actually execute successfully
7. **Test it**: Run your example before committing

Remember: **Runnable code with comments > separate documentation files**

