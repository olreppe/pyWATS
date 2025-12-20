# Agent Variants & Tool Profiles

> Safe experimentation with different tool configurations

## Overview

The variant system lets you create multiple "flavors" of the agent layer without risking the main codebase. This is useful for:

- **A/B testing** different tool prompts
- **Experimental features** you want to test in isolation
- **Focused agents** with only the tools needed for specific tasks
- **Rollback safety** - you can always switch back to known-good configurations

## Quick Start

```python
from pywats import pyWATS
from pywats_agent.tools import create_agent_tools, list_profiles

# Connect to WATS
api = pyWATS(base_url="https://your-wats-server/", token="...")

# See available profiles
print(list_profiles())
# ['full', 'yield', 'investigation', 'capability', 'minimal']

# Create tools with a specific profile
tools = create_agent_tools(api, profile="yield")

# Use a custom variant (defined in variant_config.py)
tools = create_agent_tools(api, variant="investigation_v2")
```

## Built-in Profiles

| Profile | Tools | Use Case |
|---------|-------|----------|
| `full` | All 11 tools | Complete agent capability |
| `yield` | 4 tools | Yield-focused analysis (trend, deviation, discovery) |
| `investigation` | 4 tools | Root cause investigation & dimensional analysis |
| `capability` | 4 tools | Process capability & measurement analysis |
| `minimal` | 1 tool | Just core yield analysis |

### Profile Details

```
📦 FULL
   All available tools - complete agent capability
   Tools: analyze_yield, analyze_yield_trend, analyze_yield_deviation,
          yield_discovery, analyze_root_cause, analyze_dimensions,
          analyze_process_capability, get_measurement_data,
          get_aggregated_measurements, analyze_test_steps, analyze_step

📦 YIELD
   Yield-focused analysis tools - trends, deviations, discovery
   Tools: analyze_yield, analyze_yield_trend, analyze_yield_deviation,
          yield_discovery

📦 INVESTIGATION
   Root cause investigation - dimensional analysis and failure modes
   Tools: analyze_yield, analyze_root_cause, analyze_dimensions,
          analyze_test_steps

📦 CAPABILITY
   Process capability and measurement analysis
   Tools: analyze_process_capability, get_measurement_data,
          get_aggregated_measurements, analyze_step

📦 MINIMAL
   Minimal tool set - just core yield analysis
   Tools: analyze_yield
```

## Creating Custom Variants

Edit `packages/pywats-agent/src/pywats_agent/tools/variant_config.py`:

```python
from pywats_agent.tools.variants import ExperimentalVariant, register_variant

# Your experiment
my_experiment = ExperimentalVariant(
    name="my_experiment",
    description="Testing something new",
    base_profile="yield",              # Start from yield profile
    include_tools=["analyze_root_cause"],  # Add extra tools
    exclude_tools=["yield_discovery"],     # Remove tools
)
register_variant(my_experiment)
```

Then use it:

```python
tools = create_agent_tools(api, variant="my_experiment")
```

## Variant Options

### 1. Start from a Base Profile

```python
variant = ExperimentalVariant(
    name="custom",
    base_profile="investigation",  # Start with investigation tools
)
```

### 2. Add/Remove Tools

```python
variant = ExperimentalVariant(
    name="custom",
    base_profile="yield",
    include_tools=["analyze_root_cause"],  # Add these
    exclude_tools=["yield_discovery"],      # Remove these
)
```

### 3. Override Tool Descriptions (A/B Testing)

```python
variant = ExperimentalVariant(
    name="prompt_test",
    base_profile="investigation",
    tool_overrides={
        "analyze_root_cause": {
            "description": "Your alternative prompt text here..."
        }
    }
)
```

### 4. Add Pre/Post Hooks

```python
def log_before(tool_name, params):
    print(f"About to run {tool_name}")
    return params  # Can modify params

def log_after(tool_name, result):
    print(f"Got result from {tool_name}")
    return result  # Can modify result

variant = ExperimentalVariant(
    name="instrumented",
    base_profile="full",
    pre_execute=log_before,
    post_execute=log_after,
)
```

## Debugging Variants

```python
from pywats_agent.tools import print_profiles, print_variant_diff

# See all profiles and registered variants
print_profiles()

# See what a variant changes from its base
print_variant_diff("my_experiment")
```

Output:
```
Variant: my_experiment (base: yield)
--------------------------------------------------
➕ Added:
   • analyze_root_cause
➖ Removed:
   • yield_discovery
```

## Getting Tool Definitions

For LLM integration, get OpenAI-format tool definitions:

```python
from pywats_agent.tools import get_tool_definitions

# From a profile
definitions = get_tool_definitions(profile="yield")

# From a variant
definitions = get_tool_definitions(variant="my_experiment")
```

## Complete Example: Testing a New Prompt

```python
# variant_config.py
from pywats_agent.tools.variants import ExperimentalVariant, register_variant

# Test whether a shorter prompt works better
shorter_prompt = ExperimentalVariant(
    name="short_yield_prompt",
    description="Testing shorter yield tool prompt",
    base_profile="yield",
    tool_overrides={
        "analyze_yield": {
            "description": (
                "Get yield statistics for a product. "
                "Requires part_number. Optional: days, station_name."
            )
        }
    }
)
register_variant(shorter_prompt)
```

```python
# In your agent code
from pywats_agent.tools import create_agent_tools, get_tool_definitions

# Production agent uses full profile
prod_tools = create_agent_tools(api, profile="full")
prod_defs = get_tool_definitions(profile="full")

# Experiment uses the shorter prompt
exp_tools = create_agent_tools(api, variant="short_yield_prompt")
exp_defs = get_tool_definitions(variant="short_yield_prompt")

# Now you can compare which works better!
```

## Safety Notes

1. **Variants don't modify the original tools** - they create wrapped instances
2. **Original profiles are immutable** - built-in profiles can't be changed
3. **Variants are registered at import time** - define them in `variant_config.py`
4. **Reset for testing**: `clear_variants()` removes all custom variants
