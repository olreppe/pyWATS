# Domain Examples

This folder contains runnable examples for each WATS domain. Each example is a complete, working script with comprehensive comments explaining domain concepts.

## Why Runnable Examples?

Instead of separate documentation files, these examples:
- ✅ **Always work** - They're tested code, not just documentation
- ✅ **Show real usage** - Actual patterns used in production
- ✅ **Preserve domain knowledge** - Comments explain WATS concepts
- ✅ **Easy to copy** - Copy-paste into your project and modify

## Examples by Domain

### Core Domains
- **[report_examples.py](report_examples.py)** - Test reports (UUT/UUR), all step types, querying
- **[product_examples.py](product_examples.py)** - Products, revisions, BOMs, box build templates
- **[asset_examples.py](asset_examples.py)** - Equipment tracking, calibration, hierarchy
- **[production_examples.py](production_examples.py)** - Serial numbers, units, assembly, phases

### Analysis & Tracking
- **[analytics_examples.py](analytics_examples.py)** - Yield analysis, measurements, Cpk statistics
- **[software_examples.py](software_examples.py)** - Package management, versioning, distribution
- **[rootcause_examples.py](rootcause_examples.py)** - Issue tracking, defect management, workflows
- **[process_examples.py](process_examples.py)** - Operation types, test/repair processes

### Advanced Workflows
- **[box_build_examples.py](box_build_examples.py)** - Multi-level assemblies, parent-child relationships
- **[report_builder_examples.py](report_builder_examples.py)** - Simple report building for converters

## Running Examples

All examples follow the same pattern:

```python
# 1. Set your WATS connection
api = pyWATS(
    base_url="https://your-wats-server.com",
    token="your-api-token"
)

# 2. Run the example function
example_function(api)
```

### Environment Variables

Set these to avoid hardcoding credentials:

```bash
export WATS_BASE_URL="https://your-wats-server.com"
export WATS_API_TOKEN="your-token"
```

Then in your code:

```python
import os
api = pyWATS(
    base_url=os.getenv("WATS_BASE_URL"),
    token=os.getenv("WATS_API_TOKEN")
)
```

## Example Structure

Each example file contains:

1. **Domain Concepts** - Comments explaining key WATS concepts
2. **Basic Operations** - Create, read, update, delete (CRUD)
3. **Common Patterns** - Real-world usage scenarios
4. **Advanced Features** - Complex workflows and edge cases
5. **Error Handling** - How to handle failures gracefully

## Learning Path

**New to WATS?** Start here:

1. [Getting Started Guide](../getting-started.md) - Basic concepts and setup
2. [WATS Concepts](../guides/wats-concepts.md) - Domain knowledge primer
3. [product_examples.py](product_examples.py) - Create products and revisions
4. [production_examples.py](production_examples.py) - Create units and track serial numbers
5. [report_examples.py](report_examples.py) - Submit test reports

**Ready for advanced topics?**

6. [box_build_examples.py](box_build_examples.py) - Multi-level assemblies
7. [analytics_examples.py](analytics_examples.py) - Yield analysis and statistics

## See Also

- [API Reference](../docs/api/) - Complete API documentation (auto-generated)
- [Architecture Guide](../guides/architecture.md) - System design and integration patterns
- [Integration Patterns](../guides/integration-patterns.md) - Practical workflow examples
- [Troubleshooting](../TROUBLESHOOTING.md) - Common issues and solutions
