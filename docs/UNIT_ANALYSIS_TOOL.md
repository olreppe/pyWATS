# Unit Analysis Tool

The Unit Analysis tool provides comprehensive analysis of individual units or small sets of units in WATS.

## Key Concepts

### What is a Unit?

In WATS, a **unit** is uniquely identified by the combination of:
- **Part Number** - The product identifier
- **Serial Number** - The unique unit identifier

**Important**: Multiple revisions of the same serial number are considered the **same unit** (upgraded/reworked), not different units.

### Unit vs Production Unit

- **Unit** (Test History): Any serial number that has test records
- **Production Unit** (MES): A unit tracked in the production/MES system with phase management

Not all units have production tracking - many customers only use UUT reports without MES integration.

## Tool: `analyze_unit`

### Description

Analyzes a single unit's complete status, test history, and verification grade.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `serial_number` | string | Yes | - | The unit serial number to analyze |
| `part_number` | string | No | - | Product part number. Inferred from history if not provided. |
| `scope` | enum | No | `standard` | Analysis depth (see below) |
| `include_sub_units` | bool | No | `false` | Include sub-unit (component) history |
| `max_history` | int | No | `50` | Maximum historical records to retrieve |

### Scope Options

| Scope | Description | Use Case |
|-------|-------------|----------|
| `quick` | Last test status only | Fast status check |
| `standard` | Status + history summary + verification | Default for most queries |
| `full` | Everything including sub-units and full history | Detailed investigation |
| `history` | Focus on test history timeline | Debugging test sequence |
| `verify` | Focus on verification rules and grading | Quality gate checks |

### Output

The tool returns comprehensive unit information:

```json
{
  "serial_number": "SN12345",
  "part_number": "TEST-PN-001",
  "revision": "A",
  "status": "passing",
  "status_reason": "All tests passed",
  "test_summary": {
    "total_tests": 15,
    "passed": 14,
    "failed": 1,
    "error": 0,
    "first_test": "2024-01-15T08:30:00",
    "last_test": "2024-12-19T14:22:00",
    "first_pass": "2024-01-15T09:45:00",
    "processes_tested": ["ICT", "FCT", "Final_Test"],
    "stations_used": ["Station_01", "Station_02"]
  },
  "production": {
    "has_production_unit": true,
    "phase": "Finalized",
    "phase_id": 16,
    "batch_number": "BATCH-2024-001",
    "location": "Warehouse A"
  },
  "verification": {
    "has_rules": true,
    "status": "Passed",
    "grade": "A",
    "all_passed_first_run": false,
    "all_passed_last_run": true,
    "no_repairs": true
  },
  "sub_units": [
    {
      "part_type": "PCBA",
      "serial_number": "PCBA-001",
      "part_number": "PCBA-PN",
      "revision": "1.0"
    }
  ],
  "recent_tests": [...],
  "warnings": []
}
```

### Unit Status Values

| Status | Emoji | Description |
|--------|-------|-------------|
| `passing` | ✅ | All tests passed |
| `failing` | ❌ | Has failing tests |
| `in_progress` | 🔄 | Under production/test |
| `repaired` | 🔧 | Was failing, now repaired |
| `scrapped` | 🗑️ | Marked as scrapped |
| `unknown` | ❓ | No test data or unclear |

## Example Usage

### Quick Status Check

```python
# Just check if a unit is passing
result = tool.execute({
    "serial_number": "SN12345",
    "scope": "quick"
})
```

### Full Investigation

```python
# Complete analysis with sub-units
result = tool.execute({
    "serial_number": "SN12345",
    "part_number": "WIDGET-001",
    "scope": "full",
    "include_sub_units": True
})
```

### Verification Check

```python
# Check if unit passes verification rules
result = tool.execute({
    "serial_number": "SN12345",
    "scope": "verify"
})

if result.data["verification"]["has_rules"]:
    if result.data["verification"]["all_passed_last_run"]:
        print("✅ Unit is verified passing")
    else:
        print("❌ Unit fails verification")
else:
    print("⚠️ No verification rules configured")
```

## Data Sources

The Unit Analysis tool aggregates data from multiple WATS domains:

### 1. Analytics Domain
- **Serial Number History**: All UUT and UUR reports for a serial number
- Primary source for test history

### 2. Production Domain
- **Unit Info**: Phase, batch, location (if MES enabled)
- **Unit Verification**: Grade based on configured rules
- **Sub-units**: Child units from production tracking

### 3. Report Domain
- **Full Reports**: Detailed test data when needed
- **Sub-units**: Component information from test reports

## Unit Verification Rules

WATS supports configurable unit verification rules that automatically grade units based on test completion. When rules are configured:

- `all_processes_in_order`: Unit tested in correct process sequence
- `all_passed_first_run`: Unit passed each process on first attempt (FPY indicator)
- `all_passed_last_run`: Unit currently passing all processes
- `no_repairs`: Unit never required repair

If no rules are configured, the tool suggests creating them in WATS Control Panel.

## Sub-Unit Tracking

Sub-units represent components assembled into a parent unit. The tool retrieves sub-unit information from:

1. **Production Unit**: Direct sub-unit relationships (MES)
2. **Test Reports**: `sub_units` field in UUT reports

Common sub-unit types:
- PCBA (Printed Circuit Board Assembly)
- Power Supply
- Display Module
- Custom components

## Related Tools

- **YieldAnalysisTool**: Aggregate yield across many units
- **StepAnalysisTool**: Deep-dive into failing test steps
- **RootCauseAnalysisTool**: Investigate failure patterns

## Agent Profile

The `unit` profile provides focused unit analysis:

```python
from pywats_agent.tools.variants import create_agent_tools

# Create unit-focused tool set
tools = create_agent_tools(api, profile="unit")
# Includes: analyze_unit, analyze_yield
```
