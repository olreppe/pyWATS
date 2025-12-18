# pyWATS Agent - Usage Examples

## Basic Tool Execution

```python
from pywats import pyWATS
from pywats_agent import ToolExecutor

# Initialize
api = pyWATS(base_url="https://your-wats-server.com", token="your-token")
executor = ToolExecutor(api)

# List available tools
print(executor.list_tools())
# ['analyze_yield', 'analyze_test_steps', 'get_measurement_statistics', 'get_measurement_data']
```

## Yield Analysis Examples

### Overall Yield
```python
result = executor.execute("analyze_yield", {
    "part_number": "WIDGET-001",
    "days": 30
})
print(result.summary)
```

### Yield by Station
```python
result = executor.execute("analyze_yield", {
    "part_number": "WIDGET-001",
    "perspective": "by station",
    "days": 7
})
print(result.summary)
```

### Daily Yield Trend
```python
result = executor.execute("analyze_yield", {
    "part_number": "WIDGET-001",
    "perspective": "daily",
    "days": 14
})
print(result.summary)
```

### Compare Products
```python
result = executor.execute("analyze_yield", {
    "perspective": "by product",
    "days": 30
})
print(result.summary)
```

## Test Step Analysis Examples

### Basic Step Analysis
```python
result = executor.execute("analyze_test_steps", {
    "part_number": "WIDGET-001",
    "test_operation": "FCT",
    "days": 7
})
print(result.summary)
# Shows all steps with execution counts and failure rates
```

### Specific Revision
```python
result = executor.execute("analyze_test_steps", {
    "part_number": "WIDGET-001",
    "test_operation": "FCT",
    "revision": "A",
    "days": 30
})
print(result.summary)
```

### Extended Analysis Period
```python
result = executor.execute("analyze_test_steps", {
    "part_number": "PCBA-500",
    "test_operation": "EOL",
    "days": 90,
    "max_count": 50000
})
print(result.summary)
```

## Measurement Statistics Examples

### Basic Measurement Stats
```python
result = executor.execute("get_measurement_statistics", {
    "measurement_path": "Main/Voltage Test/Output Voltage",
    "part_number": "WIDGET-001",
    "days": 7
})
print(result.summary)
# Shows count, min, max, avg, Cpk
```

### Grouped by Station
```python
result = executor.execute("get_measurement_statistics", {
    "measurement_path": "Main/Voltage Test/Output Voltage",
    "part_number": "WIDGET-001",
    "grouping": "stationName",
    "days": 30
})
print(result.summary)
```

### Multiple Products
```python
result = executor.execute("get_measurement_statistics", {
    "measurement_path": "Main/Temperature Sensor/Temp",
    "grouping": "partNumber",
    "days": 30
})
print(result.summary)
```

## Measurement Data Examples

### Recent Measurements
```python
result = executor.execute("get_measurement_data", {
    "measurement_path": "Main/Voltage Test/Output Voltage",
    "part_number": "WIDGET-001",
    "top_count": 100,
    "days": 1
})
print(result.summary)
# Shows individual data points with serial numbers
```

### Specific Serial Number
```python
result = executor.execute("get_measurement_data", {
    "measurement_path": "Main/Voltage Test/Output Voltage",
    "serial_number": "SN12345",
    "days": 30
})
print(result.summary)
```

### Specific Station
```python
result = executor.execute("get_measurement_data", {
    "measurement_path": "Main/Voltage Test/Output Voltage",
    "part_number": "WIDGET-001",
    "station_name": "Line1-FCT",
    "top_count": 500,
    "days": 7
})
print(result.summary)
```

## OpenAI Integration Example

```python
from openai import OpenAI
import json

# Initialize
client = OpenAI()
executor = ToolExecutor(api)

# Get tool definitions
tools = executor.get_openai_tools()

# Natural language query
messages = [
    {"role": "system", "content": "You are a manufacturing data analyst."},
    {"role": "user", "content": "What's the yield for WIDGET-001 and which test steps are failing?"}
]

response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=tools
)

# Execute tool calls
for tool_call in response.choices[0].message.tool_calls:
    result = executor.execute_openai_tool_call(tool_call)
    print(f"\n{tool_call.function.name}:")
    print(result.summary)
    
    # Send result back to OpenAI
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result.to_openai_response()
    })

# Get final response
final_response = client.chat.completions.create(
    model="gpt-4",
    messages=messages
)
print(f"\nFinal Answer:\n{final_response.choices[0].message.content}")
```

## Direct Tool Access

```python
# Access tools directly
yield_tool = executor.yield_tool
step_tool = executor.test_step_analysis_tool
measurement_tool = executor.aggregated_measurement_tool

# Use with custom filters
from pywats_agent import YieldFilter, TestStepAnalysisFilter, MeasurementFilter

# Yield analysis
yield_filter = YieldFilter(
    part_number="WIDGET-001",
    perspective="by station",
    days=7
)
result = yield_tool.analyze(yield_filter)

# Test step analysis
step_filter = TestStepAnalysisFilter(
    part_number="WIDGET-001",
    test_operation="FCT",
    days=7
)
result = step_tool.analyze(step_filter)

# Measurement statistics
measurement_filter = MeasurementFilter(
    measurement_path="Main/Voltage Test/Output Voltage",
    part_number="WIDGET-001",
    days=7
)
result = measurement_tool.analyze(measurement_filter)
```

## Accessing Structured Data

All tools return `AgentResult` objects with both summary text and structured data:

```python
result = executor.execute("analyze_yield", {
    "part_number": "WIDGET-001",
    "perspective": "by station"
})

# Human-readable summary
print(result.summary)

# Structured data
if result.success:
    for station_data in result.data:
        print(f"Station: {station_data['station_name']}")
        print(f"  FPY: {station_data['fpy']}%")
        print(f"  Units: {station_data['count']}")
    
    # Metadata
    print(f"\nTotal records: {result.metadata['record_count']}")
    print(f"Dimensions used: {result.metadata['dimensions']}")
else:
    print(f"Error: {result.error}")
```
