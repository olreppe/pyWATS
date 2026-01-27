# MQTT/IoT Integration for pyWATS

**Date:** 2026-01-26  
**Status:** 💡 Idea / Brainstorming  
**Author:** Copilot  

---

## Executive Summary

This document explores adding MQTT support to pyWATS for lightweight IoT device integration, complementing the existing IPC-CFX/AMQP implementation. While CFX targets MES-level factory integration, MQTT would enable edge devices, sensors, and embedded test equipment to communicate with WATS.

---

## Background: AMQP vs MQTT

### Why CFX Uses AMQP (Not Interchangeable)

The IPC-CFX standard **mandates AMQP 1.0** for specific reasons:

| Aspect | AMQP (CFX) | MQTT (IoT) |
|--------|------------|------------|
| **Standard** | IPC-CFX mandated | De facto IoT standard |
| **Message Model** | Advanced routing, exchanges, queues | Simple pub/sub topics |
| **Reliability** | Transactional, persistent | QoS 0/1/2 |
| **Payload Size** | Large (full reports, BOMs) | Optimized for small |
| **Typical Broker** | RabbitMQ, ActiveMQ | Mosquitto, HiveMQ |
| **Use Case** | MES/ERP enterprise integration | Edge devices, sensors |
| **Bandwidth** | Higher overhead | Minimal overhead |
| **Connection** | Persistent, stateful | Lightweight, reconnect-friendly |

### Complementary, Not Replacement

```
┌─────────────────────────────────────────────────────────────────────┐
│                    pyWATS Integration Landscape                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Enterprise/MES Layer                    Edge/IoT Layer            │
│   ┌─────────────────┐                    ┌─────────────────┐        │
│   │ Test Sequencer  │                    │ Embedded Tester │        │
│   │ (LabVIEW, NI)   │                    │ (Raspberry Pi)  │        │
│   └────────┬────────┘                    └────────┬────────┘        │
│            │ CFX/AMQP                             │ MQTT            │
│            ▼                                      ▼                 │
│   ┌─────────────────┐                    ┌─────────────────┐        │
│   │   RabbitMQ      │                    │  MQTT Broker    │        │
│   │   (CFX Hub)     │                    │  (Mosquitto)    │        │
│   └────────┬────────┘                    └────────┬────────┘        │
│            │                                      │                 │
│            ▼                                      ▼                 │
│   ┌─────────────────┐                    ┌─────────────────┐        │
│   │   pywats_cfx    │                    │   pywats_mqtt   │        │
│   │   (existing)    │                    │   (proposed)    │        │
│   └────────┬────────┘                    └────────┬────────┘        │
│            │                                      │                 │
│            └──────────────┬───────────────────────┘                 │
│                           ▼                                         │
│                   ┌───────────────┐                                 │
│                   │  pywats_events│                                 │
│                   │   EventBus    │                                 │
│                   └───────┬───────┘                                 │
│                           ▼                                         │
│                   ┌───────────────┐                                 │
│                   │    pyWATS     │                                 │
│                   │   API Client  │                                 │
│                   └───────┬───────┘                                 │
│                           ▼                                         │
│                   ┌───────────────┐                                 │
│                   │  WATS Server  │                                 │
│                   └───────────────┘                                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Use Cases for MQTT/IoT Integration

### 1. Asset Domain (High Value)

**Real-time asset telemetry from edge devices:**

| Data Type | MQTT Topic Pattern | WATS Mapping | Description |
|-----------|-------------------|--------------|-------------|
| Status heartbeat | `assets/{id}/status` | Asset state updates | Online/offline, running/idle |
| Counter updates | `assets/{id}/counters` | Running/total count | Cycle counts from PLCs |
| Environmental | `assets/{id}/environment` | Asset attributes | Temp, humidity, vibration |
| Calibration drift | `assets/{id}/calibration` | Calibration alerts | Measurement drift detection |
| Maintenance alerts | `assets/{id}/alerts` | Maintenance triggers | Predictive maintenance signals |
| Utilization | `assets/{id}/utilization` | OEE data | Uptime, availability metrics |

**Example payload:**
```json
{
  "asset_id": "FIXTURE-001",
  "timestamp": "2026-01-26T10:30:00Z",
  "counters": {
    "running_count": 1523,
    "total_count": 45000
  },
  "environment": {
    "temperature_c": 23.5,
    "humidity_pct": 45.2,
    "vibration_g": 0.02
  },
  "status": "running"
}
```

**WATS Integration:**
- Auto-increment `running_count` / `total_count`
- Trigger maintenance alarms when thresholds exceeded
- Feed environmental data into asset attributes
- Support predictive maintenance ML models

---

### 2. Software Domain (Medium Value)

**Edge device software version reporting:**

| Data Type | MQTT Topic Pattern | WATS Mapping | Description |
|-----------|-------------------|--------------|-------------|
| Version report | `devices/{id}/software` | Software inventory | Installed versions |
| Update status | `devices/{id}/updates` | Deployment tracking | OTA update progress |
| Config sync | `devices/{id}/config` | Settings distribution | Test parameters |

**Example payload:**
```json
{
  "device_id": "TESTER-042",
  "timestamp": "2026-01-26T10:30:00Z",
  "software": [
    {"name": "test_firmware", "version": "2.3.1", "hash": "abc123"},
    {"name": "calibration_data", "version": "2026.01", "hash": "def456"}
  ],
  "config_version": "prod-v5"
}
```

**WATS Integration:**
- Track software versions across edge fleet
- Verify test stations have correct software before testing
- Coordinate OTA updates with production schedules

---

### 3. Report Domain (High Value)

**Lightweight test results from embedded testers:**

| Data Type | MQTT Topic Pattern | WATS Mapping | Description |
|-----------|-------------------|--------------|-------------|
| Self-test results | `devices/{id}/selftest` | UUT reports | Station self-diagnostics |
| Simple pass/fail | `testers/{id}/results` | UUT reports | Basic test outcomes |
| Measurement streams | `testers/{id}/measurements` | Report steps | Continuous measurement data |
| Batch summaries | `lines/{id}/batch` | Analytics | Aggregated production data |

**Example payload (simple test):**
```json
{
  "device_id": "FIXTURE-001",
  "test_type": "self_test",
  "timestamp": "2026-01-26T06:00:00Z",
  "serial_number": "FIXTURE-001",
  "part_number": "TEST-FIXTURE-A",
  "result": "Passed",
  "duration_ms": 5230,
  "steps": [
    {"name": "Power Supply Check", "status": "P", "value": 5.02, "unit": "V", "low": 4.9, "high": 5.1},
    {"name": "Communication Test", "status": "P", "value": 1, "unit": "bool"},
    {"name": "Sensor Calibration", "status": "P", "value": 0.02, "unit": "offset"}
  ]
}
```

**Example payload (measurement stream):**
```json
{
  "device_id": "SENSOR-ARRAY-01",
  "timestamp": "2026-01-26T10:30:00.123Z",
  "serial_number": "UNIT-12345",
  "measurements": [
    {"path": "Temperature/Ambient", "value": 25.3, "unit": "°C"},
    {"path": "Temperature/DUT", "value": 42.1, "unit": "°C"},
    {"path": "Current/Main", "value": 1.234, "unit": "A"}
  ]
}
```

**WATS Integration:**
- Convert to UUT/UUR reports automatically
- Support streaming measurements during long tests
- Enable fixture self-test reporting (daily calibration checks)
- Aggregate edge data for analytics

---

### 4. Production Domain (Medium Value)

**Shop floor events from edge devices:**

| Data Type | MQTT Topic Pattern | WATS Mapping | Description |
|-----------|-------------------|--------------|-------------|
| Unit scanned | `lines/{id}/scan` | Unit tracking | Barcode/RFID events |
| Station entry/exit | `stations/{id}/unit` | Production flow | Unit location tracking |
| Operator login | `stations/{id}/operator` | Shift tracking | Badge scans |

**Example payload:**
```json
{
  "station_id": "LINE1-STATION3",
  "timestamp": "2026-01-26T10:30:00Z",
  "event": "unit_entered",
  "serial_number": "UNIT-12345",
  "part_number": "WIDGET-001",
  "operator": "john.doe"
}
```

---

## Proposed Architecture

### Package Structure

```
src/pywats_mqtt/
├── __init__.py
├── transport/
│   ├── __init__.py
│   ├── mqtt_transport.py      # Base MQTT transport
│   ├── mqtt_tls.py            # TLS/certificate handling
│   └── reconnect.py           # Reconnection logic
├── config/
│   ├── __init__.py
│   ├── mqtt_config.py         # Connection configuration
│   └── topic_config.py        # Topic patterns and routing
├── adapters/
│   ├── __init__.py
│   ├── asset_adapter.py       # Asset telemetry → pyWATS
│   ├── report_adapter.py      # Test results → UUT reports
│   ├── software_adapter.py    # Version reporting → software tracking
│   └── production_adapter.py  # Shop floor events → production
├── schemas/
│   ├── __init__.py
│   ├── asset_schemas.py       # JSON schemas for validation
│   ├── report_schemas.py
│   └── common_schemas.py
└── cli/
    └── mqtt_monitor.py        # CLI tool for debugging
```

### Configuration Model

```python
@dataclass
class MQTTConfig:
    """MQTT broker connection configuration."""
    
    # Connection
    broker: str = "localhost"
    port: int = 1883
    client_id: str = ""  # Auto-generated if empty
    
    # Authentication
    username: Optional[str] = None
    password: Optional[str] = None
    
    # TLS/SSL
    use_tls: bool = False
    ca_cert: Optional[str] = None
    client_cert: Optional[str] = None
    client_key: Optional[str] = None
    
    # QoS and reliability
    default_qos: int = 1  # 0=fire-forget, 1=at-least-once, 2=exactly-once
    clean_session: bool = True
    keepalive: int = 60
    
    # Reconnection
    auto_reconnect: bool = True
    reconnect_delay: float = 5.0
    max_reconnect_delay: float = 300.0


@dataclass
class TopicConfig:
    """Topic subscription and routing configuration."""
    
    # Topic patterns to subscribe
    asset_topics: List[str] = field(default_factory=lambda: ["assets/+/status", "assets/+/counters"])
    report_topics: List[str] = field(default_factory=lambda: ["testers/+/results", "devices/+/selftest"])
    software_topics: List[str] = field(default_factory=lambda: ["devices/+/software"])
    production_topics: List[str] = field(default_factory=lambda: ["lines/+/scan", "stations/+/unit"])
    
    # Topic templates for publishing
    alarm_topic: str = "wats/alarms/{alarm_type}"
    response_topic: str = "wats/responses/{request_id}"
```

### Transport Implementation

```python
class MQTTTransport(BaseTransport):
    """
    MQTT transport for IoT device integration.
    
    Lightweight alternative to CFX/AMQP for edge devices.
    """
    
    def __init__(
        self,
        config: MQTTConfig,
        topic_config: TopicConfig,
        on_event: Optional[Callable[[Event], None]] = None,
    ):
        super().__init__(name="mqtt-iot")
        self.config = config
        self.topic_config = topic_config
        self._on_event = on_event
        
        # Adapters for different data types
        self._asset_adapter = AssetMQTTAdapter()
        self._report_adapter = ReportMQTTAdapter()
        self._software_adapter = SoftwareMQTTAdapter()
    
    async def connect(self) -> None:
        """Connect to MQTT broker and subscribe to topics."""
        # Use aiomqtt or paho-mqtt
        ...
    
    async def _on_message(self, topic: str, payload: bytes) -> None:
        """Route incoming messages to appropriate adapter."""
        if topic.startswith("assets/"):
            event = self._asset_adapter.parse(topic, payload)
        elif topic.startswith("testers/") or topic.startswith("devices/"):
            event = self._report_adapter.parse(topic, payload)
        elif topic.startswith("software/"):
            event = self._software_adapter.parse(topic, payload)
        
        if event and self._on_event:
            self._on_event(event)
```

---

## Cloud IoT Platform Considerations

### AWS IoT Core

```python
@dataclass
class AWSIoTConfig(MQTTConfig):
    """AWS IoT Core specific configuration."""
    
    # AWS IoT endpoint
    endpoint: str = ""  # xxx.iot.region.amazonaws.com
    
    # Certificate-based auth (recommended)
    thing_name: str = ""
    
    # Cognito auth (alternative)
    cognito_identity_pool: Optional[str] = None
    
    # AWS IoT specific features
    use_websockets: bool = False
    shadow_topics: bool = True  # Device shadow support
```

### Azure IoT Hub

```python
@dataclass
class AzureIoTConfig(MQTTConfig):
    """Azure IoT Hub specific configuration."""
    
    # IoT Hub connection
    iot_hub_name: str = ""
    device_id: str = ""
    
    # Authentication
    connection_string: Optional[str] = None  # Device connection string
    sas_token: Optional[str] = None
    
    # Azure specific
    use_device_twin: bool = True
```

---

## Message Flow Examples

### Asset Heartbeat Flow

```
┌─────────────┐     MQTT      ┌─────────────┐    Event    ┌─────────────┐
│   Fixture   │──────────────▶│ MQTT Broker │────────────▶│ pywats_mqtt │
│   (Edge)    │               │ (Mosquitto) │             │  Transport  │
└─────────────┘               └─────────────┘             └──────┬──────┘
                                                                 │
      Topic: assets/FIXTURE-001/status                           │
      Payload: {"status": "running", "count": 1523}              ▼
                                                          ┌─────────────┐
                                                          │ AssetAdapter│
                                                          └──────┬──────┘
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │  EventBus   │
                                                          └──────┬──────┘
                                                                 │
                                                          AssetStatusEvent
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │   Handler   │
                                                          │ (API Call)  │
                                                          └──────┬──────┘
                                                                 │
                                              api.asset.set_running_count()
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │ WATS Server │
                                                          └─────────────┘
```

### Self-Test Report Flow

```
┌─────────────┐     MQTT      ┌─────────────┐    Event    ┌─────────────┐
│  Test Jig   │──────────────▶│ MQTT Broker │────────────▶│ pywats_mqtt │
│   (ESP32)   │               │             │             │  Transport  │
└─────────────┘               └─────────────┘             └──────┬──────┘
                                                                 │
      Topic: devices/JIG-001/selftest                            │
      Payload: {test result JSON}                                ▼
                                                          ┌─────────────┐
                                                          │ReportAdapter│
                                                          │ (→ UUTReport│
                                                          └──────┬──────┘
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │  EventBus   │
                                                          └──────┬──────┘
                                                                 │
                                                        TestResultEvent
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │   Handler   │
                                                          │ (Submit)    │
                                                          └──────┬──────┘
                                                                 │
                                                api.report.submit_uut()
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │ WATS Server │
                                                          └─────────────┘
```

---

## Implementation Phases

### Phase 1: Core Transport (MVP)

- [ ] Basic MQTT transport with Paho/aiomqtt
- [ ] Configuration models (MQTTConfig, TopicConfig)
- [ ] Simple asset status adapter
- [ ] Unit tests with mock broker

### Phase 2: Asset Integration

- [ ] Full asset telemetry support
- [ ] Counter auto-increment
- [ ] Environmental data to attributes
- [ ] Maintenance threshold alerts

### Phase 3: Report Integration

- [ ] Self-test report adapter
- [ ] Simple test result → UUT conversion
- [ ] Measurement streaming support
- [ ] Batch aggregation

### Phase 4: Cloud IoT

- [ ] AWS IoT Core adapter
- [ ] Azure IoT Hub adapter
- [ ] Certificate management
- [ ] Device shadow/twin support

### Phase 5: Advanced Features

- [ ] Bidirectional communication (commands to devices)
- [ ] Configuration distribution via MQTT
- [ ] Firmware update coordination
- [ ] Edge analytics aggregation

---

## Open Questions

1. **Message format standardization** - Define JSON schemas? Use existing standards (Sparkplug B)?
2. **QoS requirements** - Which data needs exactly-once delivery?
3. **Broker deployment** - Embedded in pyWATS Client? Separate service?
4. **Security** - Certificate provisioning for edge devices?
5. **Offline handling** - Local buffering when WATS unreachable?
6. **Rate limiting** - How to handle high-frequency sensor data?

---

## Related Documents

- [IPC-CFX and Electronics Test Asset Integration](IPC_CFX_and_Electronics_Test_Asset_Integration.md)
- [Electronics Test Log Formats and Standards](electronics_test_log_formats_and_standards_scan.md)
- [WATS Asset Systems Prioritized](wats_asset_systems_prioritized.md)

---

## References

- [MQTT 5.0 Specification](https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html)
- [Eclipse Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [AWS IoT Core](https://aws.amazon.com/iot-core/)
- [Azure IoT Hub](https://azure.microsoft.com/en-us/products/iot-hub/)
- [Sparkplug B Specification](https://sparkplug.eclipse.org/)
