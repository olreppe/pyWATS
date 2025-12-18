# pyWATS Agent

AI agent tools for pyWATS - provides intelligent tool definitions for LLMs to interact with WATS manufacturing data.

## Installation

```bash
pip install pywats-agent
```

## Quick Start

```python
from pywats import pyWATS
from pywats_agent import ToolExecutor, YieldAnalysisTool

# Initialize
api = pyWATS(base_url="https://your-wats-server.com", token="...")
executor = ToolExecutor(api)

# Execute a tool call (as an LLM would)
result = executor.execute("analyze_yield", {
    "part_number": "WIDGET-001",
    "perspective": "by station",
    "days": 7
})

print(result.summary)
# "Yield analysis for product WIDGET-001 grouped by station (last 7 days):
# • Average FPY: 94.5%
# • Total units: 1,234
# • Best: Station-A (98.2%)
# • Worst: Station-E (89.1%)"
```

## Semantic Perspectives

The key feature is **semantic perspective mapping** - use natural language to specify how to analyze data:

| User Says | Perspective | WATS Dimensions |
|-----------|-------------|-----------------|
| "by station" | `BY_STATION` | `stationName` |
| "trending over time" | `TREND` | `period` |
| "compare products" | `BY_PRODUCT` | `partNumber` |
| "daily breakdown" | `DAILY` | `period` + `date_grouping=DAY` |
| "station trend" | `STATION_TREND` | `stationName;period` |

## OpenAI Function Calling

```python
from pywats_agent import get_yield_tool_definition

# Get OpenAI-compatible tool schema
tool_def = get_yield_tool_definition()

# Use with OpenAI
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "What's the yield for WIDGET-001 by station?"}],
    tools=[{"type": "function", "function": tool_def}]
)

# Execute the tool call
tool_call = response.choices[0].message.tool_calls[0]
result = executor.execute(
    tool_call.function.name,
    json.loads(tool_call.function.arguments)
)
```

## Available Tools

- **analyze_yield** - Flexible yield analysis with semantic perspectives

More tools coming soon (failure analysis, measurements, repair history).
