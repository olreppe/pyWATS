# pyWATS LangChain - Usage Examples

## Quick Start

```python
from pywats import pyWATS
from pywats_langchain import WATSToolkit
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Initialize
api = pyWATS(base_url="https://your-wats-server.com", token="your-token")
toolkit = WATSToolkit(api)
tools = toolkit.get_tools()

# Create agent
llm = ChatOpenAI(model="gpt-4")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a manufacturing data analyst. Use the available tools to answer questions about test data."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Query
result = agent_executor.invoke({
    "input": "What's the yield for WIDGET-001 and which stations are performing worst?"
})
print(result["output"])
```

## Using Individual Tools

### Yield Analysis Tool

```python
from pywats_langchain import WATSYieldTool

yield_tool = WATSYieldTool(api=api)

# Direct invocation
result = yield_tool.invoke({
    "part_number": "WIDGET-001",
    "perspective": "by station",
    "days": 7
})
print(result)
```

### Test Step Analysis Tool

```python
from pywats_langchain import WATSTestStepAnalysisTool

step_tool = WATSTestStepAnalysisTool(api=api)

result = step_tool.invoke({
    "part_number": "WIDGET-001",
    "test_operation": "FCT",
    "days": 7
})
print(result)
```

### Measurement Statistics Tool

```python
from pywats_langchain import WATSAggregatedMeasurementTool

measurement_tool = WATSAggregatedMeasurementTool(api=api)

result = measurement_tool.invoke({
    "measurement_path": "Main/Voltage Test/Output Voltage",
    "part_number": "WIDGET-001",
    "days": 7
})
print(result)
```

### Measurement Data Tool

```python
from pywats_langchain import WATSMeasurementDataTool

data_tool = WATSMeasurementDataTool(api=api)

result = data_tool.invoke({
    "measurement_path": "Main/Voltage Test/Output Voltage",
    "part_number": "WIDGET-001",
    "top_count": 100,
    "days": 1
})
print(result)
```

## Natural Language Queries

The agent can understand and route to the appropriate tools:

```python
# These queries automatically use the right tools:

# Yield analysis
agent_executor.invoke({"input": "What's the overall yield for WIDGET-001?"})
agent_executor.invoke({"input": "Compare yield by station for the past week"})
agent_executor.invoke({"input": "Show me daily yield trend for PCBA-500"})

# Test step analysis
agent_executor.invoke({"input": "Which test steps are failing for WIDGET-001 in FCT?"})
agent_executor.invoke({"input": "Show me step statistics for EOL testing"})

# Measurements
agent_executor.invoke({"input": "What's the average output voltage for WIDGET-001?"})
agent_executor.invoke({"input": "Show me Cpk for all voltage measurements"})
agent_executor.invoke({"input": "Get the last 100 temperature readings"})

# Multi-tool queries
agent_executor.invoke({
    "input": "Analyze WIDGET-001: show yield, identify failing steps, and get voltage statistics"
})
```

## Pre-configured Agent

```python
from pywats_langchain import create_wats_agent

# Simple setup
agent = create_wats_agent(api, model_name="gpt-4")

# Use it
result = agent.invoke({
    "input": "What's wrong with WIDGET-001 production?"
})
print(result["output"])
```

## Custom Agent with Memory

```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_tool_calling_agent

# Setup with memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a manufacturing data analyst."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    memory=memory,
    verbose=True
)

# Conversation with context
agent_executor.invoke({"input": "What's the yield for WIDGET-001?"})
agent_executor.invoke({"input": "Which stations are performing worst?"})
agent_executor.invoke({"input": "Now show me the failing test steps"})
```

## Using with LangGraph

```python
from langgraph.prebuilt import create_react_agent
from pywats_langchain import WATSToolkit

toolkit = WATSToolkit(api)
tools = toolkit.get_tools()

# Create LangGraph agent
graph = create_react_agent(llm, tools)

# Stream responses
for chunk in graph.stream({
    "messages": [("human", "Analyze yield for WIDGET-001 by station")]
}):
    print(chunk)
```

## Async Usage

```python
import asyncio

async def analyze_products():
    products = ["WIDGET-001", "WIDGET-002", "PCBA-500"]
    
    tasks = [
        agent_executor.ainvoke({
            "input": f"What's the yield for {product}?"
        })
        for product in products
    ]
    
    results = await asyncio.gather(*tasks)
    return results

# Run async
results = asyncio.run(analyze_products())
for result in results:
    print(result["output"])
```

## Toolkit Access Patterns

```python
toolkit = WATSToolkit(api)

# Get all tools
all_tools = toolkit.get_tools()

# Access specific tools
yield_tool = toolkit.yield_tool
step_tool = toolkit.test_step_analysis_tool
agg_meas_tool = toolkit.aggregated_measurement_tool
data_tool = toolkit.measurement_data_tool

# Use individually
result = yield_tool.invoke({
    "part_number": "WIDGET-001",
    "perspective": "by station"
})
```

## Error Handling

```python
try:
    result = agent_executor.invoke({
        "input": "Get yield for INVALID-PRODUCT"
    })
    print(result["output"])
except Exception as e:
    print(f"Error: {e}")
```

## Streaming Responses

```python
# Stream intermediate steps
for step in agent_executor.stream({
    "input": "Comprehensive analysis of WIDGET-001"
}):
    print(step)
```

## Custom System Prompts

```python
custom_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert manufacturing quality engineer.
    
When analyzing test data:
1. Always check yield first
2. If yield is low, investigate failing test steps
3. For measurement issues, check both statistics and recent data points
4. Provide actionable recommendations

Use the available tools to gather data, then synthesize insights."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, custom_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

result = agent_executor.invoke({
    "input": "Diagnose production issues with WIDGET-001"
})
```

## Production Monitoring Agent

```python
def create_monitoring_agent(api):
    """Create an agent for production monitoring."""
    toolkit = WATSToolkit(api)
    tools = toolkit.get_tools()
    
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a production monitoring assistant.
        
Monitor manufacturing metrics and alert on issues:
- Yield drops below 90%
- Test step failure rates increase
- Measurement Cpk falls below 1.33
        
Provide clear, actionable alerts."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools)

# Use the monitoring agent
monitor = create_monitoring_agent(api)

result = monitor.invoke({
    "input": "Check all critical products and alert on any issues"
})
print(result["output"])
```
