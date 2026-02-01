# IPC-CFX Integration Architecture Investigation

**Created:** 2026-01-26  
**Updated:** 2026-01-27  
**Status:** ✅ Architecture Study Complete  
**Priority:** Future (implement when customer demand exists)  
**Related:** [ADDITIONAL_STANDARD_CONVERTERS.md](ADDITIONAL_STANDARD_CONVERTERS.md)

---

## Status Summary (2026-01-27)

**Architecture Study:** ✅ Complete

**Key Decisions:**
1. ❌ **CFX is NOT a file converter** - It's a real-time AMQP messaging system
2. 💡 **Implement as separate project** - `pywats_cfx` when customer need arises
3. ⏱️ **Estimated effort:** 6-9 weeks for full implementation
4. 📋 **All architecture documented** - Ready to implement when needed

**When to Implement:**
- Customer specifically requests CFX integration
- Multiple customers using CFX-compatible equipment  
- Strategic partnership with CFX equipment vendor

**See:** ROADMAP.md Priority 4 for implementation phases

---

## Executive Summary

IPC-CFX (IPC-2591) is **NOT** a test result file format like ATML or STDF. It is a **real-time factory connectivity standard** for equipment-to-equipment and equipment-to-MES communication via AMQP message broker.

This document analyzes where IPC-CFX integration fits within pyWATS architecture and proposes a proper implementation strategy that aligns with our design principles.

### Key Findings

1. **IPC-CFX does NOT belong in the file converter framework.**
2. **The event system should be layered:** shared infrastructure + protocol-specific adapters
3. **CFX is just one potential integration** - design for extensibility

### Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    pywats_events (Shared Infrastructure)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  EventBus   │  │  Handlers   │  │   Routing   │  │  Lifecycle  │    │
│  │  (Core)     │  │  (Base)     │  │  (Rules)    │  │  (Mgmt)     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
         ▲                  ▲                  ▲                  ▲
         │                  │                  │                  │
┌────────┴───────┐ ┌───────┴────────┐ ┌───────┴────────┐ ┌───────┴───────┐
│  pywats_cfx    │ │ pywats_mqtt    │ │ pywats_webhook │ │ pywats_kafka  │
│  (IPC-CFX)     │ │ (IoT/IIoT)     │ │ (HTTP)         │ │ (Streaming)   │
│  ┌───────────┐ │ │ ┌───────────┐  │ │ ┌───────────┐  │ │ ┌───────────┐ │
│  │AMQP Client│ │ │ │MQTT Client│  │ │ │HTTP Server│  │ │ │Kafka Cons.│ │
│  │CFX Models │ │ │ │Topic Map  │  │ │ │Payload Map│  │ │ │Schema Reg │ │
│  │Handlers   │ │ │ │Handlers   │  │ │ │Handlers   │  │ │ │Handlers   │ │
│  └───────────┘ │ │ └───────────┘  │ │ └───────────┘  │ │ └───────────┘ │
└────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
```

---

## 1. What is IPC-CFX?

### 1.1 Standard Overview

| Property | Description |
|----------|-------------|
| **Standard** | IPC-2591 Connected Factory Exchange |
| **Type** | Real-time messaging protocol |
| **Transport** | AMQP 1.0 (message broker) |
| **Format** | JSON messages |
| **Communication** | Pub/Sub and Request/Response |
| **Scope** | Equipment ↔ Equipment, Equipment ↔ MES |

### 1.2 CFX Message Topics (Namespaces)

CFX organizes messages into topics that span the entire manufacturing domain:

```
CFX.Root                            # Endpoint identification, heartbeats
CFX.InformationSystem               # MES/ERP integration
CFX.InformationSystem.UnitValidation
CFX.Materials.Management            # Material tracking
CFX.Materials.Management.MSDManagement
CFX.Materials.Storage
CFX.Materials.Transport
CFX.Production                      # Work orders, unit processing
CFX.Production.Assembly             # Component placement, soldering
CFX.Production.TestAndInspection    # Test results, inspection results
CFX.Production.Application          # Adhesive, solder paste
CFX.ResourcePerformance             # Equipment status, OEE, faults
CFX.ResourcePerformance.THTInsertion
CFX.ResourcePerformance.SMTPlacement
```

### 1.3 Key Message Types Relevant to WATS

| CFX Message | Description | WATS Relevance |
|-------------|-------------|----------------|
| `UnitsTested` | Test execution results | **High** - Test reports |
| `UnitsInspected` | Inspection results (AOI, SPI, X-ray) | **High** - Inspection reports |
| `WorkStarted/WorkCompleted` | Unit processing lifecycle | **Medium** - Production tracking |
| `MaterialsInstalled` | Component placement | **Medium** - BOM/Box-build |
| `MaterialsConsumed` | Material usage | **Low** - Traceability |
| `FaultOccurred` | Equipment faults | **Medium** - Asset management |
| `MaintenancePerformed` | Equipment maintenance | **Medium** - Asset management |
| `GetEndpointInformation` | Equipment identification | **Low** - Discovery |

---

## 2. Why CFX is NOT a File Converter

### 2.1 Fundamental Differences

| Aspect | File Converter | IPC-CFX |
|--------|---------------|---------|
| **Trigger** | File created in folder | Message received from broker |
| **Timing** | Batch (after test complete) | Real-time (during test) |
| **Transport** | File system | AMQP message broker |
| **Scope** | Single file → Single report | Continuous event stream |
| **State** | Stateless per file | Stateful (transactions, work orders) |
| **Bidirectional** | No (read-only) | Yes (request/response) |

### 2.2 File Converter Limitations

The current `FileConverter` base class assumes:

```python
class FileConverter:
    def validate(self, source: ConverterSource, context) -> ValidationResult
    def convert(self, source: ConverterSource, context) -> ConverterResult
```

CFX would require:

```python
class CFXConnector:
    async def connect(self, broker_uri: str)
    async def subscribe(self, topics: List[str])
    async def on_message(self, topic: str, message: CFXMessage)
    async def publish(self, topic: str, message: CFXMessage)
    async def request(self, endpoint: str, message: CFXMessage) -> CFXMessage
```

These are fundamentally different paradigms.

---

## 3. pyWATS Architecture Analysis

### 3.1 Current Module Structure

```
pywats/                     # Core API library
├── domains/
│   ├── report/            # UUTReport, steps, submission
│   ├── asset/             # Equipment/station management
│   ├── product/           # Products, BOM, box-build
│   ├── production/        # Units, tracking, verification
│   ├── analytics/         # Measurements, analysis
│   └── ...
├── queue/                  # Report queuing
│   ├── QueueHooks         # Extensibility hooks
│   └── MemoryQueue
└── core/                   # HTTP client, auth, errors

pywats_client/              # Client application library
├── service/               # AsyncClientService, async components
├── converters/            # File converter framework
│   ├── file_converter.py  # Base class
│   └── standard/          # Built-in converters
├── gui/                   # GUI application
└── core/                  # Configuration, instances
```

### 3.2 Existing Hook/Event Patterns

#### QueueHooks (pywats/queue/memory_queue.py)

```python
class QueueHooks:
    """Hooks for queue operations."""
    
    def on_item_added(self, item: QueueItem) -> None: pass
    def on_item_updated(self, item: QueueItem) -> None: pass
    def on_item_removed(self, item_id: str) -> None: pass
    def on_item_completed(self, item: QueueItem) -> None: pass
    def on_item_failed(self, item: QueueItem) -> None: pass
```

This is a good pattern that could be extended for CFX integration.

#### File System Events (pywats_client/service/async_pending_queue.py)

```python
# File system events are handled via Watchdog with thread-safe signaling
# to the async event loop
class QueuedFileHandler(FileSystemEventHandler):
    def on_created(self, event): 
        loop.call_soon_threadsafe(event.set)  # Signal async code
```

File system event-based processing pattern (async-first architecture).

### 3.3 Architecture Gap

**Current:** File-triggered, batch processing
**CFX Needs:** Message-triggered, real-time processing

There is no current infrastructure for:
- AMQP broker connectivity
- Pub/sub messaging
- Real-time event handling
- Bidirectional communication
- State management (transactions, work orders)

---

## 4. Proposed Architecture

### 4.1 New Module: `pywats_cfx`

Create a dedicated CFX integration module, separate from file converters:

```
pywats_cfx/                 # New: CFX Integration Module
├── __init__.py
├── client/
│   ├── cfx_client.py      # AMQP client wrapper
│   ├── connection.py      # Connection management
│   └── message_router.py  # Topic routing
├── handlers/
│   ├── base_handler.py    # Base message handler
│   ├── test_handler.py    # UnitsTested → WATS Report
│   ├── inspection_handler.py  # UnitsInspected → WATS Report
│   ├── production_handler.py  # WorkStarted/Completed
│   ├── material_handler.py    # MaterialsInstalled → BOM
│   └── resource_handler.py    # Equipment events → Asset
├── models/
│   ├── cfx_messages.py    # CFX message models
│   └── mappings.py        # CFX ↔ WATS mappings
├── publishers/
│   ├── report_publisher.py    # Publish WATS reports to CFX
│   └── status_publisher.py    # Publish status updates
└── config/
    └── cfx_config.py      # CFX connection settings
```

### 4.2 Integration Points

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Factory Floor                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │  Tester  │  │   AOI    │  │  P&P     │  │   MES    │               │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│       │             │             │             │                       │
│       └─────────────┴─────────────┴─────────────┘                       │
│                           │ CFX (AMQP)                                  │
└───────────────────────────┼─────────────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────────────┐
│                      CFX Message Broker                                │
│                     (RabbitMQ/ActiveMQ)                               │
└───────────────────────────┬───────────────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────────────┐
│                       pywats_cfx Module                                │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                     CFXClient                                    │  │
│  │  - AMQP Connection                                              │  │
│  │  - Topic Subscriptions                                          │  │
│  │  - Message Routing                                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                            │                                           │
│    ┌───────────────────────┼───────────────────────┐                  │
│    ▼                       ▼                       ▼                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │ TestHandler  │   │MaterialHandler│   │ResourceHandler│             │
│  │UnitsTested   │   │MaterialsInstal│   │FaultOccurred │             │
│  │→ UUTReport   │   │→ BOM/BoxBuild│   │→ Asset Event │             │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘              │
│         │                  │                  │                       │
└─────────┼──────────────────┼──────────────────┼───────────────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌───────────────────────────────────────────────────────────────────────┐
│                         pywats Core                                    │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐              │
│  │ api.report   │   │ api.product  │   │  api.asset   │              │
│  │  .submit()   │   │  .update()   │   │  .create()   │              │
│  └──────────────┘   └──────────────┘   └──────────────┘              │
│                            │                                           │
│                            ▼                                           │
│                    ┌──────────────┐                                   │
│                    │  WATS API    │                                   │
│                    └──────────────┘                                   │
└───────────────────────────────────────────────────────────────────────┘
```

### 4.3 Message Handler Interface

```python
# pywats_cfx/handlers/base_handler.py

from abc import ABC, abstractmethod
from typing import List, Optional
from pywats_cfx.models import CFXMessage

class CFXMessageHandler(ABC):
    """Base class for CFX message handlers."""
    
    @property
    @abstractmethod
    def topics(self) -> List[str]:
        """CFX topics this handler subscribes to."""
        pass
    
    @abstractmethod
    async def handle(self, message: CFXMessage) -> Optional[Any]:
        """Process a CFX message."""
        pass
    
    async def on_connect(self) -> None:
        """Called when connected to broker."""
        pass
    
    async def on_disconnect(self) -> None:
        """Called when disconnected from broker."""
        pass
```

### 4.4 Test Results Handler Example

```python
# pywats_cfx/handlers/test_handler.py

from pywats_cfx.handlers.base_handler import CFXMessageHandler
from pywats.domains.report import UUTReport
from pywats.domains.report.report_models.uut.steps import CompOp

class TestResultsHandler(CFXMessageHandler):
    """Handler for CFX.Production.TestAndInspection.UnitsTested messages."""
    
    @property
    def topics(self) -> List[str]:
        return [
            "CFX.Production.TestAndInspection.UnitsTested",
            "CFX.Production.TestAndInspection.UnitsInspected",
        ]
    
    async def handle(self, message: CFXMessage) -> UUTReport:
        """Convert CFX test message to WATS UUTReport."""
        
        # Extract UUT info
        tested_unit = message.data['TestedUnits'][0]
        
        # Create UUTReport
        report = UUTReport(
            pn=tested_unit.get('UnitIdentifier', ''),
            sn=tested_unit.get('UnitIdentifier', ''),
            result='P' if tested_unit.get('OverallResult') == 'Passed' else 'F',
            start=message.timestamp,
        )
        
        # Map tests to steps
        root = report.get_root_sequence_call()
        for test in tested_unit.get('Tests', []):
            if test.get('Measurements'):
                for m in test['Measurements']:
                    root.add_numeric_step(
                        name=test.get('TestName', 'Test'),
                        value=m.get('MeasuredValue', 0),
                        unit=m.get('MeasurementUnits', '?'),
                        comp_op=CompOp.GELE,
                        low_limit=m.get('ExpectedValueMinimum'),
                        high_limit=m.get('ExpectedValueMaximum'),
                        status='P' if test.get('Result') == 'Passed' else 'F',
                    )
            else:
                root.add_pass_fail_step(
                    name=test.get('TestName', 'Test'),
                    status='P' if test.get('Result') == 'Passed' else 'F',
                )
        
        return report
```

---

## 5. CFX Relevance to WATS Domains

### 5.1 Domain Mapping

| WATS Domain | CFX Topics | Data Flow |
|-------------|------------|-----------|
| **Report** (Test Results) | `UnitsTested`, `UnitsInspected` | CFX → WATS |
| **Asset** (Equipment) | `FaultOccurred`, `MaintenancePerformed`, `StationStateChanged` | CFX → WATS |
| **Product** (BOM/Box-build) | `MaterialsInstalled`, `GetWorkOrderStatus` | CFX ↔ WATS |
| **Production** (Units) | `WorkStarted`, `WorkCompleted`, `UnitsDisqualified` | CFX ↔ WATS |
| **Analytics** | N/A (WATS-native) | - |

### 5.2 Bidirectional Opportunities

CFX supports request/response patterns, enabling:

| WATS → CFX | Use Case |
|------------|----------|
| `ValidateUnitsRequest` | Check unit routing before test |
| `GetWorkOrderStatus` | Retrieve work order details |
| `SendNotificationMessage` | Push status updates to MES |

This could enable:
- Pre-test unit validation from WATS
- Work order synchronization
- Status dashboard integration

---

## 6. Implementation Recommendations

### 6.1 Phase 1: Core Infrastructure (2-3 weeks)

1. **Create `pywats_cfx` module** with:
   - AMQP client wrapper (use `python-qpid-proton` or `aiormq`)
   - Configuration for broker connectivity
   - Basic message routing

2. **Implement base handler pattern**:
   - `CFXMessageHandler` abstract base
   - Message deserialization
   - Error handling and retry logic

3. **Add first handler**: `TestResultsHandler`
   - Map `UnitsTested` to `UUTReport`
   - Submit via `api.report.submit()`

### 6.2 Phase 2: Domain Handlers (2-3 weeks)

4. **Inspection handler**: `UnitsInspected` → Report
5. **Material handler**: `MaterialsInstalled` → Product/BOM
6. **Resource handler**: `FaultOccurred`, `MaintenancePerformed` → Asset

### 6.3 Phase 3: Bidirectional Integration (2-3 weeks)

7. **Publisher module**: WATS → CFX
8. **Request handlers**: Respond to CFX queries
9. **Unit validation**: Pre-test validation flow

### 6.4 Dependencies

| Library | Purpose | License |
|---------|---------|---------|
| `python-qpid-proton` | AMQP 1.0 client | Apache 2.0 |
| `aiormq` | Async AMQP | Apache 2.0 |
| `pydantic` | Message models | MIT |

---

## 7. Layered Event Architecture (CFX-Specific vs Shared)

> **Key Question:** Should CFX-specific functionality be separated from a shared event system to enable future integrations?

**Answer: Yes, absolutely.** This is the recommended approach.

### 7.1 Why Layered Architecture Matters

IPC-CFX is just **one** of many potential event integrations. Other protocols you might want to support in the future:

| Protocol | Use Case | Transport |
|----------|----------|-----------|
| **IPC-CFX** | Factory floor equipment | AMQP 1.0 |
| **MQTT** | IoT sensors, edge devices | MQTT 3.1/5.0 |
| **Webhooks** | SaaS integrations, CI/CD triggers | HTTP/HTTPS |
| **Kafka** | High-throughput streaming analytics | Kafka protocol |
| **OPC-UA** | Industrial automation | OPC-UA binary/XML |
| **Azure Service Bus** | Cloud-native messaging | AMQP/REST |
| **gRPC Streaming** | Real-time bidirectional | HTTP/2 |

Building CFX tightly coupled to WATS would mean **rewriting core infrastructure** for each new integration. Instead, invest in a **protocol-agnostic event layer**.

---

### 7.2 Proposed Layered Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LAYER 1: pywats_events (Core)                        │
│                    Protocol-Agnostic Event Infrastructure                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │   EventBus   │ │ EventRouter  │ │  Lifecycle   │ │   Metrics    │       │
│  │   (Pub/Sub)  │ │   (Rules)    │ │  (Start/Stop)│ │  (Telemetry) │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ BaseHandler  │ │  Serializer  │ │  ErrorPolicy │ │  RetryPolicy │       │
│  │  (Abstract)  │ │  (Pluggable) │ │  (Deadletter)│ │  (Backoff)   │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
            ┌─────────────────────────┼─────────────────────────┐
            │                         │                         │
            ▼                         ▼                         ▼
┌───────────────────────┐ ┌───────────────────────┐ ┌───────────────────────┐
│  LAYER 2a: pywats_cfx │ │ LAYER 2b: pywats_mqtt │ │LAYER 2c: pywats_webhook│
│  (Transport Adapter)  │ │  (Transport Adapter)  │ │  (Transport Adapter)  │
│  ┌─────────────────┐  │ │  ┌─────────────────┐  │ │  ┌─────────────────┐  │
│  │  AMQPTransport  │  │ │  │  MQTTTransport  │  │ │  │  HTTPTransport  │  │
│  │  CFXSerializer  │  │ │  │  TopicMapper    │  │ │  │  PayloadMapper  │  │
│  │  CFXModels      │  │ │  │  QoSHandler     │  │ │  │  SignatureAuth  │  │
│  └─────────────────┘  │ │  └─────────────────┘  │ │  └─────────────────┘  │
└───────────────────────┘ └───────────────────────┘ └───────────────────────┘
            │                         │                         │
            └─────────────────────────┼─────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   LAYER 3: Domain Handlers (Shared Logic)                    │
│     These handlers work identically regardless of which transport sent       │
│     the event - CFX, MQTT, webhook, or file watcher                         │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐            │
│  │  ReportHandler   │ │  AssetHandler    │ │  ProductHandler  │            │
│  │  (UUTReport)     │ │  (Equipment)     │ │  (BOM/BoxBuild)  │            │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘            │
│  ┌──────────────────┐ ┌──────────────────┐                                 │
│  │ProductionHandler │ │  CustomHandler   │                                 │
│  │  (WorkOrders)    │ │  (User-defined)  │                                 │
│  └──────────────────┘ └──────────────────┘                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LAYER 4: pywats API (pyWATS/AsyncWATS)               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ api.report   │ │  api.asset   │ │ api.product  │ │api.production│       │
│  │  .submit()   │ │  .create()   │ │  .update()   │ │  .start()    │       │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 7.3 Layer Responsibilities

#### Layer 1: `pywats_events` - Core Infrastructure (SHARED)

This is the **reusable foundation** - completely protocol-agnostic:

```
pywats_events/
├── __init__.py
├── bus/
│   ├── event_bus.py           # Pub/Sub event dispatcher
│   ├── async_event_bus.py     # Async variant for high-throughput
│   └── local_event_bus.py     # In-memory for testing
├── models/
│   ├── event.py               # Core Event class
│   ├── event_types.py         # Domain event type enum
│   └── event_metadata.py      # Tracing, correlation IDs
├── handlers/
│   ├── base_handler.py        # Abstract handler interface
│   ├── handler_registry.py    # Handler registration/discovery
│   └── handler_chain.py       # Middleware pattern
├── routing/
│   ├── router.py              # Event → Handler routing
│   ├── filter.py              # Event filtering rules
│   └── priority.py            # Handler priority ordering
├── policies/
│   ├── retry_policy.py        # Exponential backoff, max retries
│   ├── error_policy.py        # Dead letter, circuit breaker
│   └── idempotency.py         # Duplicate detection
├── serialization/
│   ├── serializer.py          # Abstract serializer interface
│   ├── json_serializer.py     # JSON (default)
│   └── avro_serializer.py     # Avro (for Kafka)
├── lifecycle/
│   ├── manager.py             # Start/stop/health
│   └── graceful_shutdown.py   # Drain handlers on shutdown
└── telemetry/
    ├── metrics.py             # Event counts, latencies
    └── tracing.py             # Distributed tracing support
```

#### Layer 2: Transport Adapters (PROTOCOL-SPECIFIC)

Each transport adapter is **isolated** and **pluggable**:

```
pywats_cfx/                         # CFX-SPECIFIC
├── __init__.py
├── transport/
│   ├── amqp_client.py             # AMQP 1.0 connection handling
│   ├── connection_pool.py         # Connection reuse
│   └── reconnection.py            # Auto-reconnect logic
├── serialization/
│   ├── cfx_serializer.py          # CFX JSON ↔ Event mapping
│   └── cfx_models.py              # CFX message dataclasses
├── routing/
│   ├── topic_mapper.py            # CFX topic → Event type
│   └── exchange_config.py         # AMQP exchange/queue setup
├── publishers/
│   ├── cfx_publisher.py           # Event → CFX message
│   └── response_handler.py        # Request/response patterns
└── config/
    └── cfx_settings.py            # Broker URL, auth, topics
```

```
pywats_mqtt/                        # MQTT-SPECIFIC (future)
├── __init__.py
├── transport/
│   ├── mqtt_client.py             # MQTT 5.0 client
│   └── qos_handler.py             # QoS levels
├── serialization/
│   └── mqtt_payload.py            # Custom payload formats
└── routing/
    └── topic_filter.py            # MQTT topic wildcards
```

```
pywats_webhook/                     # WEBHOOK-SPECIFIC (future)
├── __init__.py
├── transport/
│   ├── http_server.py             # Async HTTP endpoint
│   └── signature_verify.py        # HMAC signature validation
├── serialization/
│   └── payload_mapper.py          # Various webhook formats
└── routing/
    └── path_router.py             # URL path → Event type
```

#### Layer 3: Domain Handlers (SHARED LOGIC)

These handlers **don't care** where the event came from:

```python
# pywats_events/handlers/report_handler.py

class TestResultEvent(Event):
    """Normalized test result event - source-agnostic."""
    unit_id: str
    result: Literal["pass", "fail", "error"]
    tests: List[TestMeasurement]
    start_time: datetime
    end_time: datetime

class ReportDomainHandler(BaseHandler):
    """Handles test results from ANY source: CFX, MQTT, file, webhook."""
    
    event_types = [EventType.TEST_RESULT, EventType.INSPECTION_RESULT]
    
    def __init__(self, api: AsyncWATS):
        self.api = api
    
    async def handle(self, event: TestResultEvent) -> None:
        # Convert normalized event to UUTReport
        report = self._build_report(event)
        
        # Submit via existing pyWATS infrastructure
        await self.api.report.submit(report)
    
    def _build_report(self, event: TestResultEvent) -> UUTReport:
        report = UUTReport(
            sn=event.unit_id,
            result='P' if event.result == 'pass' else 'F',
            start=event.start_time,
        )
        # ... map tests to steps
        return report
```

---

### 7.4 Event Normalization Pattern

The key to separation is **normalizing** protocol-specific messages into **domain events**:

```
CFX Message                    Normalized Event              Domain Handler
───────────────────────────────────────────────────────────────────────────
CFX.Production.TestAndInspec   TestResultEvent               ReportDomainHandler
tion.UnitsTested               ├── unit_id                   ├── Creates UUTReport
                               ├── result                    ├── Maps measurements
                               └── tests[]                   └── Submits via API
                               
mqtt/factory/tester/result     TestResultEvent               ReportDomainHandler
(same JSON payload)            ├── unit_id                   (SAME handler!)
                               ├── result                    
                               └── tests[]                   
                               
POST /webhook/test-result      TestResultEvent               ReportDomainHandler
(HTTP payload)                 ├── unit_id                   (SAME handler!)
                               ├── result
                               └── tests[]
```

**CFX Adapter does this translation:**

```python
# pywats_cfx/adapters/test_adapter.py

class CFXTestResultAdapter:
    """Translates CFX UnitsTested → Normalized TestResultEvent."""
    
    def adapt(self, cfx_message: CFXUnitsTested) -> TestResultEvent:
        unit = cfx_message.tested_units[0]
        return TestResultEvent(
            event_type=EventType.TEST_RESULT,
            source="cfx",
            correlation_id=cfx_message.transaction_id,
            unit_id=unit.unit_identifier,
            result="pass" if unit.overall_result == "Passed" else "fail",
            tests=[
                TestMeasurement(
                    name=t.test_name,
                    value=t.measurements[0].measured_value if t.measurements else None,
                    unit=t.measurements[0].measurement_units if t.measurements else None,
                    status="pass" if t.result == "Passed" else "fail",
                )
                for t in unit.tests
            ],
            start_time=cfx_message.timestamp,
            end_time=cfx_message.timestamp,
        )
```

---

### 7.5 What's SHARED vs CFX-SPECIFIC

| Component | Location | Shared/Specific | Reused By |
|-----------|----------|-----------------|-----------|
| `EventBus` | `pywats_events` | ✅ Shared | All integrations |
| `BaseHandler` | `pywats_events` | ✅ Shared | All handlers |
| `RetryPolicy` | `pywats_events` | ✅ Shared | All transports |
| `ErrorPolicy` | `pywats_events` | ✅ Shared | All transports |
| `TestResultEvent` | `pywats_events` | ✅ Shared | CFX, MQTT, Webhook |
| `ReportDomainHandler` | `pywats_events` | ✅ Shared | Any test source |
| `AMQPClient` | `pywats_cfx` | ❌ CFX-specific | - |
| `CFXSerializer` | `pywats_cfx` | ❌ CFX-specific | - |
| `CFXUnitsTested` | `pywats_cfx` | ❌ CFX-specific | - |
| `CFXTestResultAdapter` | `pywats_cfx` | ❌ CFX-specific | - |

---

### 7.6 Benefits of This Separation

1. **Add new integrations without touching core:**
   ```
   # Adding MQTT support later:
   pip install pywats-mqtt
   
   # Just configure and register the transport:
   mqtt = MQTTTransport(broker="mqtt://...", topics=["factory/#"])
   event_bus.register_transport(mqtt)
   # Domain handlers automatically receive MQTT events!
   ```

2. **Test domain logic independently:**
   ```python
   # Unit test ReportDomainHandler without AMQP/network:
   def test_report_handler():
       handler = ReportDomainHandler(mock_report_service)
       event = TestResultEvent(unit_id="SN123", result="pass", ...)
       await handler.handle(event)
       mock_report_service.submit.assert_called_once()
   ```

3. **Swap transports without changing handlers:**
   ```python
   # Development: use mock transport
   bus.register_transport(MockTransport())
   
   # Production: use real CFX
   bus.register_transport(CFXTransport(broker="amqp://..."))
   
   # Same handlers work in both environments
   ```

4. **Mix multiple sources simultaneously:**
   ```python
   # Factory uses CFX for testers, MQTT for sensors
   bus.register_transport(CFXTransport())    # Test results
   bus.register_transport(MQTTTransport())   # Temperature sensors
   bus.register_transport(WebhookTransport()) # ERP notifications
   # All events flow to same domain handlers
   ```

---

### 7.7 Implementation Sequence

Given the layered approach, the recommended build order is:

```
Phase 0: Core Event System (FIRST - enables everything else)
├── pywats_events/bus/event_bus.py
├── pywats_events/models/event.py
├── pywats_events/handlers/base_handler.py
├── pywats_events/policies/retry_policy.py
└── Tests with MockTransport

Phase 1: CFX Transport Adapter
├── pywats_cfx/transport/amqp_client.py
├── pywats_cfx/serialization/cfx_models.py
├── pywats_cfx/adapters/test_adapter.py
└── Integration tests with RabbitMQ

Phase 2: Domain Handlers
├── pywats_events/handlers/report_handler.py
├── pywats_events/handlers/asset_handler.py
├── pywats_events/handlers/product_handler.py
└── End-to-end CFX → WATS tests

Phase 3: Future Transports (as needed)
├── pywats_mqtt/ (IoT integration)
├── pywats_webhook/ (SaaS integration)
└── pywats_kafka/ (analytics streaming)
```

---

### 7.8 Configuration Model

```yaml
# pywats_config.yaml

events:
  bus:
    type: async              # async | sync | local (testing)
    max_workers: 10
    
  transports:
    cfx:
      enabled: true
      broker: "amqp://cfx-broker.factory.local:5672"
      exchange: "cfx"
      topics:
        - "CFX.Production.TestAndInspection.*"
        - "CFX.Production.Assembly.*"
      credentials:
        type: "certificate"
        cert_path: "/etc/pywats/cfx-client.pem"
        
    mqtt:                    # Future: MQTT integration
      enabled: false
      broker: "mqtt://iot-hub.factory.local:1883"
      topics:
        - "factory/+/sensors/#"
        
    webhook:                 # Future: Webhook receiver
      enabled: false
      listen_port: 8080
      endpoints:
        - path: "/events/erp"
          auth: "hmac-sha256"
          
  handlers:
    report:
      enabled: true
      auto_submit: true
    asset:
      enabled: true
      fault_threshold: 3     # Alert after N faults
    product:
      enabled: false         # Enable when BOM feature ready
```

---

### 7.9 Summary: Answer to the Question

> "Should CFX-specific functionality be separated from shared event system for future integrations?"

**Yes. The recommended architecture is:**

| Layer | Package | Contains | Reusable? |
|-------|---------|----------|-----------|
| **Core** | `pywats_events` | EventBus, BaseHandler, Policies, Domain Events | ✅ 100% |
| **Transport** | `pywats_cfx` | AMQP Client, CFX Models, CFX→Event Adapters | ❌ CFX only |
| **Transport** | `pywats_mqtt` | MQTT Client, Topic Mappers | ❌ MQTT only |
| **Transport** | `pywats_webhook` | HTTP Server, Payload Mappers | ❌ Webhook only |
| **Domain** | `pywats_events.handlers` | ReportHandler, AssetHandler, ProductHandler | ✅ 100% |

**Investment vs Payoff:**
- **Extra effort now:** ~1-2 weeks to build core event infrastructure
- **Payoff later:** Each new integration is ~1 week instead of ~4 weeks
- **Risk mitigation:** Domain logic tested once, works everywhere

---

## 8. Conclusion

### Recommendation

**Do NOT implement IPC-CFX as a file converter.**

Instead:
1. Create a dedicated `pywats_cfx` module
2. Implement proper AMQP messaging infrastructure
3. Design handlers for each CFX message type → WATS domain mapping
4. Consider broader event system architecture for future extensibility

### Estimated Effort

| Phase | Description | Effort |
|-------|-------------|--------|
| Phase 1 | Core infrastructure + TestHandler | 2-3 weeks |
| Phase 2 | Domain handlers | 2-3 weeks |
| Phase 3 | Bidirectional integration | 2-3 weeks |
| **Total** | Complete CFX integration | **6-9 weeks** |

### Dependencies/Prerequisites

1. Sample CFX messages from real deployments
2. Access to CFX test broker (RabbitMQ)
3. Customer validation partner
4. Decision on general event system architecture

---

## Appendix A: CFX Message Examples

### UnitsTested Message

```json
{
  "$type": "CFX.Production.TestAndInspection.UnitsTested, CFX",
  "TransactionId": "2c24590d-39c5-4039-96a5-91900cecedfa",
  "TestMethod": "Automated",
  "Tester": {
    "OperatorIdentifier": "OP001",
    "ActorType": "Human"
  },
  "TestedUnits": [
    {
      "UnitIdentifier": "SN12345",
      "UnitPositionNumber": 1,
      "OverallResult": "Passed",
      "Tests": [
        {
          "UniqueIdentifier": "T001",
          "TestName": "PowerOnTest",
          "Result": "Passed",
          "Measurements": [
            {
              "MeasuredValue": 5.02,
              "MeasurementUnits": "V",
              "ExpectedValueMinimum": 4.9,
              "ExpectedValueMaximum": 5.1
            }
          ]
        }
      ]
    }
  ]
}
```

### MaterialsInstalled Message

```json
{
  "$type": "CFX.Production.Assembly.MaterialsInstalled, CFX",
  "TransactionId": "a1b2c3d4-...",
  "InstalledMaterials": [
    {
      "UnitIdentifier": "SN12345",
      "UnitPositionNumber": 1,
      "QuantityInstalled": 1,
      "Material": {
        "UniqueIdentifier": "MAT001",
        "InternalPartNumber": "RES-10K-0402"
      },
      "InstalledComponents": [
        {
          "ReferenceDesignator": "R1",
          "InstallationTimeStamp": "2024-01-15T10:30:00"
        }
      ]
    }
  ]
}
```

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-26 | Initial investigation document | AI Assistant |
| 2026-01-26 | Expanded Section 7: Layered event architecture design for reusability | AI Assistant |
