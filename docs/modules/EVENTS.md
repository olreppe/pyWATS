# Event Architecture

The pyWATS event system provides a protocol-agnostic way to integrate with external message sources (IPC-CFX, MQTT, webhooks) and route events to appropriate handlers.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                         External Sources                              │
│   CFX Broker    │    MQTT Broker    │    Webhooks    │    Files      │
└────────┬────────┴────────┬──────────┴───────┬────────┴───────┬───────┘
         │                 │                  │                │
         ▼                 ▼                  ▼                ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      Transport Adapters                               │
│  CFXTransport     MQTTTransport     WebhookTransport   FileWatcher   │
│  (pywats_cfx)     (pywats_mqtt)                                      │
└────────────────────────────┬─────────────────────────────────────────┘
                             │ Protocol-specific → Normalized Event
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      pywats_events Core                               │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────────────┐   │
│  │  Event   │───▶│   EventBus   │───▶│   HandlerRegistry        │   │
│  │  Model   │    │  (pub/sub)   │    │   (routing by type)      │   │
│  └──────────┘    └──────────────┘    └──────────────────────────┘   │
│                         │                          │                 │
│                  ┌──────┴──────┐           ┌──────┴──────┐          │
│                  │ RetryPolicy │           │ ErrorPolicy │          │
│                  │ (backoff)   │           │ (DLQ, CB)   │          │
│                  └─────────────┘           └─────────────┘          │
└──────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      WATS Handlers (planned)                          │
│  ReportHandler    │   AssetHandler    │   ProductionHandler          │
│  → ReportService  │   → AssetService  │   → ProductionService        │
└──────────────────────────────────────────────────────────────────────┘
```

## Packages

### pywats_events (Core)

The protocol-agnostic event system foundation:

```python
from pywats_events import Event, EventType, EventBus, BaseHandler

# Create an event
event = Event(
    event_type=EventType.TEST_RESULT,
    payload={"unit_id": "SN-123", "result": "pass"},
    source="test-station"
)

# Create a handler
class MyHandler(BaseHandler):
    @property
    def event_types(self):
        return [EventType.TEST_RESULT]
    
    async def handle(self, event):
        print(f"Processing: {event.payload['unit_id']}")

# Wire it up
bus = EventBus()
bus.subscribe(MyHandler())
bus.start()
bus.publish(event)
```

### pywats_cfx (IPC-CFX Adapter)

Adapter for IPC-CFX factory messaging standard:

```python
from pywats_cfx import CFXTransport, CFXConfig
from pywats_events import EventBus

# Configure CFX connection
config = CFXConfig(
    amqp=AMQPConfig(host="cfx-broker.factory.local"),
    endpoint=EndpointConfig(cfx_handle="//Company/WATS/Station1")
)

# Create transport and connect to event bus
transport = CFXTransport(config)
bus = EventBus()
bus.register_transport(transport)

# CFX messages automatically converted to domain events
bus.start()  # Starts receiving CFX messages
```

## Event Types

Events are categorized by domain:

| Category | Event Types | Description |
|----------|-------------|-------------|
| **Test** | `TEST_RESULT`, `TEST_STARTED`, `INSPECTION_RESULT` | Test and inspection results |
| **Asset** | `ASSET_FAULT`, `ASSET_STATE_CHANGED`, `ASSET_MAINTENANCE` | Equipment status and faults |
| **Material** | `MATERIAL_INSTALLED`, `MATERIAL_CONSUMED` | BOM and component tracking |
| **Production** | `WORK_STARTED`, `WORK_COMPLETED`, `UNIT_DISQUALIFIED` | Production flow events |
| **System** | `TRANSPORT_CONNECTED`, `HANDLER_ERROR`, `EVENT_DEAD_LETTER` | Internal system events |

## CFX Message Mapping

IPC-CFX messages are converted to normalized domain events:

| CFX Message | Domain Event | WATS Handler Action |
|-------------|--------------|---------------------|
| `UnitsTested` | `TestResultEvent` | `ReportService.submit()` |
| `UnitsInspected` | `TestResultEvent` | `ReportService.submit()` |
| `MaterialsInstalled` | `MaterialInstalledEvent` | Component traceability |
| `FaultOccurred` | `AssetFaultEvent` | `AssetService` fault logging |
| `StationStateChanged` | `AssetStateChangedEvent` | Equipment status |
| `WorkStarted/Completed` | `WorkStartedEvent/WorkCompletedEvent` | Production tracking |

## CFX Sample Explorer

Use the explorer CLI to understand CFX message formats:

```bash
# List all available samples
python -m pywats_cfx.explorer --list

# View raw CFX message
python -m pywats_cfx.explorer --sample units_tested_ict

# Convert to domain event with WATS mapping hints
python -m pywats_cfx.explorer --convert units_tested_ict
```

Available samples:
- **Test**: `units_tested_ict`, `units_tested_fct`, `units_inspected_aoi`, `units_inspected_spi`
- **Production**: `work_started`, `work_completed_pass`, `work_completed_fail`
- **Materials**: `materials_smt`, `materials_th`, `materials_loaded`
- **Faults**: `fault_temp`, `fault_feeder`, `fault_cleared`

## Policies

### Retry Policy

Configure retry behavior for failed handlers:

```python
from pywats_events.policies import RetryPolicy

policy = RetryPolicy(
    max_retries=3,
    initial_delay=1.0,      # 1 second
    max_delay=60.0,         # Max 60 seconds
    exponential_base=2.0,   # Exponential backoff
    jitter=True             # Add randomness
)

# Filter which exceptions to retry
policy.retry_on(ConnectionError, TimeoutError)
policy.no_retry_on(ValidationError)  # Never retry these
```

### Error Policy

Handle permanently failed events:

```python
from pywats_events.policies import ErrorPolicy, DeadLetterQueue, CircuitBreaker

dlq = DeadLetterQueue(max_size=1000)
cb = CircuitBreaker(
    failure_threshold=5,    # Open after 5 failures
    reset_timeout=30.0      # Try again after 30 seconds
)

policy = ErrorPolicy(dead_letter_queue=dlq, circuit_breaker=cb)

# Get failed events for analysis/replay
for entry in dlq.get_entries():
    print(f"Failed: {entry.event.id} - {entry.error}")
```

## Testing

Use `MockTransport` for testing without external dependencies:

```python
from pywats_events import EventBus, Event, EventType
from pywats_events.transports import MockTransport

def test_my_handler():
    bus = EventBus()
    transport = MockTransport()
    bus.register_transport(transport)
    
    received = []
    class TestHandler(BaseHandler):
        def event_types(self): return [EventType.TEST_RESULT]
        def handle(self, event): received.append(event)
    
    bus.subscribe(TestHandler())
    bus.start()
    
    # Inject test event
    transport.inject_event(Event(
        event_type=EventType.TEST_RESULT,
        payload={"unit_id": "TEST-123", "passed": True}
    ))
    
    assert len(received) == 1
```

## Next Steps

The WATS handlers that consume domain events and call pyWATS services are planned:

```python
# Future: WATS handlers (not yet implemented)
class ReportHandler(BaseHandler):
    def __init__(self, report_service: ReportService):
        self.report_service = report_service
    
    @property
    def event_types(self):
        return [EventType.TEST_RESULT]
    
    async def handle(self, event: Event):
        result = TestResultEvent(**event.payload)
        report = self._build_uut_report(result)
        await self.report_service.submit(report)
```

See the CFX explorer output for mapping hints when implementing handlers.
