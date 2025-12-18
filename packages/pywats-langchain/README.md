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

- **WATSYieldTool** - Yield analysis with semantic perspectives

## Requirements

- Python 3.9+
- pywats-api
- pywats-agent
- langchain (optional, for full functionality)
- langchain-openai (for OpenAI agents)
