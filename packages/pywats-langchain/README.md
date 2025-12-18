# pyWATS LangChain

LangChain integration for pyWATS - provides native LangChain tools and agents for manufacturing analytics.

## Installation

```bash
pip install pywats-langchain[langchain]
```

## Quick Start

### Using Individual Tools

```python
from pywats import pyWATS
from pywats_langchain import WATSToolkit

api = pyWATS(base_url="https://your-wats-server.com", token="...")
toolkit = WATSToolkit(api)

# Get tools for your agent
tools = toolkit.get_tools()
```

### Pre-configured Agent

```python
from pywats import pyWATS
from pywats_langchain import create_wats_agent

api = pyWATS(base_url="https://your-wats-server.com", token="...")
agent = create_wats_agent(api, model_name="gpt-4")

# Natural language queries
result = agent.invoke({
    "input": "What's the yield for WIDGET-001 and which station is performing worst?"
})
print(result["output"])
```

### Analytics Chain

```python
from pywats_langchain import WATSAnalyticsChain

chain = WATSAnalyticsChain(api)

# Comprehensive product analysis
result = chain.analyze_product("WIDGET-001", days=30)
print(result["summary"])
```

## Available Tools

All tools are available through the `WATSToolkit`:

### Yield Analysis
- **WATSYieldTool** (`analyze_yield`) - Yield analysis with semantic perspectives

### Test Step Analysis
- **WATSTestStepAnalysisTool** (`analyze_test_steps`) - Step-level failure analysis and statistics

### Measurement Tools
- **WATSAggregatedMeasurementTool** (`get_measurement_statistics`) - Aggregated stats with Cpk/Cp
- **WATSMeasurementDataTool** (`get_measurement_data`) - Individual data points with timestamps

## Example Usage

```python
from pywats import pyWATS
from pywats_langchain import WATSToolkit
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI

# Setup
api = pyWATS(base_url="...", token="...")
toolkit = WATSToolkit(api)
tools = toolkit.get_tools()

# Create agent
llm = ChatOpenAI(model="gpt-4")
agent = create_react_agent(llm, tools, prompt_template)

# Natural language queries work with all tools:
# - "What's the yield for WIDGET-001 by station?"
# - "Show me test step failures for FCT operation"
# - "Get voltage measurement statistics for product X"
# - "Show me the last 100 temperature measurements"
```

## Direct Tool Access

```python
toolkit = WATSToolkit(api)

# Access individual tools
yield_tool = toolkit.yield_tool
step_tool = toolkit.test_step_analysis_tool
measurement_tool = toolkit.aggregated_measurement_tool
data_tool = toolkit.measurement_data_tool
```

## Requirements

- Python 3.10+
- pywats-api
- pywats-agent
- langchain (optional, for full functionality)
- langchain-openai (for OpenAI agents)
