"""
Unit Tests for pywats_cfx - IPC-CFX Integration.

Tests for CFX message models, adapters, and transport.
"""

import pytest
from datetime import datetime
from uuid import uuid4

from pywats_events import Event, EventType

from pywats_cfx.models import (
    CFXMessage,
    UnitsTested,
    UnitsInspected,
    MaterialsInstalled,
    WorkStarted,
    WorkCompleted,
    FaultOccurred,
    StationStateChanged,
    TestedUnit,
    Test,
    Measurement,
    InstalledMaterial,
    UnitPosition,
    TestResult,
    InspectionResult,
    FaultSeverity,
    ResourceState,
    WorkResultState,
    parse_cfx_message,
    serialize_cfx_message,
)

from pywats_cfx.adapters import (
    CFXTestResultAdapter,
    CFXMaterialAdapter,
    CFXProductionAdapter,
    CFXResourceAdapter,
)

from pywats_cfx.config import (
    CFXConfig,
    AMQPConfig,
    EndpointConfig,
    ExchangeConfig,
)


# =============================================================================
# CFX Message Model Tests
# =============================================================================

class TestCFXMessageModels:
    """Tests for CFX Pydantic models."""
    
    def test_units_tested_model(self):
        """Should create UnitsTested message."""
        message = UnitsTested(
            TransactionId=uuid4(),
            TestMethod="ICT",
            TestedBy="Operator1",
            Tester="TestStation1",
            TestStartTime=datetime.now(),
            TestEndTime=datetime.now(),
            TestedUnits=[
                TestedUnit(
                    UnitIdentifier="SN-12345",
                    OverallResult=TestResult.PASSED,
                    Tests=[
                        Test(
                            TestName="Resistance Test",
                            Result=TestResult.PASSED,
                            Measurements=[
                                Measurement(
                                    MeasurementName="R1",
                                    MeasuredValue=99.5,
                                    ExpectedValue=100.0,
                                    MeasurementUnits="Ohm",
                                    LowerLimit=90.0,
                                    UpperLimit=110.0,
                                    Result=TestResult.PASSED,
                                )
                            ],
                        )
                    ],
                )
            ],
            RecipeName="ICT_RECIPE_V1",
        )
        
        assert message.MessageName == "CFX.Production.Testing.UnitsTested"
        assert message.TestMethod == "ICT"
        assert len(message.TestedUnits) == 1
        assert message.TestedUnits[0].OverallResult == TestResult.PASSED
    
    def test_units_inspected_model(self):
        """Should create UnitsInspected message."""
        message = UnitsInspected(
            TransactionId=uuid4(),
            InspectionMethod="AOI",
            InspectedBy="Operator2",
            Inspector="AOI-Station-1",
            InspectionStartTime=datetime.now(),
            InspectionEndTime=datetime.now(),
            InspectedUnits=[],
        )
        
        assert message.MessageName == "CFX.Production.Assembly.UnitsInspected"
        assert message.InspectionMethod == "AOI"
    
    def test_materials_installed_model(self):
        """Should create MaterialsInstalled message."""
        message = MaterialsInstalled(
            TransactionId=uuid4(),
            InstalledMaterials=[
                InstalledMaterial(
                    UnitIdentifier="UNIT-001",
                    InstalledComponents=[
                        {
                            "ReferenceDesignator": "R1",
                            "InternalPartNumber": "RES-100",
                        }
                    ],
                )
            ],
        )
        
        assert message.MessageName == "CFX.Production.Assembly.MaterialsInstalled"
        assert len(message.InstalledMaterials) == 1
    
    def test_station_state_changed_model(self):
        """Should create StationStateChanged message."""
        message = StationStateChanged(
            OldState=ResourceState.STANDBY,
            NewState=ResourceState.PROCESSING,
            OldStateDuration=120.5,
        )
        
        assert message.MessageName == "CFX.ResourcePerformance.StationStateChanged"
        assert message.OldState == ResourceState.STANDBY
        assert message.NewState == ResourceState.PROCESSING
    
    def test_fault_occurred_model(self):
        """Should create FaultOccurred message."""
        message = FaultOccurred(
            Fault={
                "Cause": "Temperature exceeded threshold",
                "Severity": "Error",
                "FaultCode": "TEMP_001",
            },
            Lane=1,
            Stage="Reflow",
        )
        
        assert message.MessageName == "CFX.ResourcePerformance.FaultOccurred"
        assert message.Fault["Cause"] == "Temperature exceeded threshold"


class TestCFXMessageParsing:
    """Tests for CFX message parsing and serialization."""
    
    def test_parse_units_tested(self):
        """Should parse UnitsTested from dict."""
        data = {
            "MessageName": "CFX.Production.Testing.UnitsTested",
            "TransactionId": str(uuid4()),
            "TestMethod": "FCT",
            "TestStartTime": datetime.now().isoformat(),
            "TestEndTime": datetime.now().isoformat(),
            "TestedUnits": [],
        }
        
        message = parse_cfx_message(data)
        
        assert isinstance(message, UnitsTested)
        assert message.TestMethod == "FCT"
    
    def test_parse_unknown_message_returns_base(self):
        """Unknown messages should return CFXMessage base."""
        data = {
            "MessageName": "CFX.Custom.UnknownMessage",
            "CustomField": "value",
        }
        
        message = parse_cfx_message(data)
        
        assert isinstance(message, CFXMessage)
        assert message.MessageName == "CFX.Custom.UnknownMessage"
    
    def test_serialize_message(self):
        """Should serialize message to dict."""
        message = WorkStarted(
            TransactionId=uuid4(),
            Lane=1,
            Stage="Assembly",
            Units=[
                UnitPosition(PositionNumber=1, UnitIdentifier="UNIT-001"),
            ],
        )
        
        data = serialize_cfx_message(message)
        
        assert data["MessageName"] == "CFX.Production.WorkStarted"
        assert data["Lane"] == 1
        assert len(data["Units"]) == 1


# =============================================================================
# CFX Adapter Tests
# =============================================================================

class TestCFXTestResultAdapter:
    """Tests for CFXTestResultAdapter."""
    
    def test_adapt_units_tested(self):
        """Should convert UnitsTested to TestResultEvents."""
        adapter = CFXTestResultAdapter(source_endpoint="test-station")
        
        message = UnitsTested(
            TransactionId=uuid4(),
            TestMethod="ICT",
            TestedBy="Operator1",
            Tester="Station1",
            TestStartTime=datetime.now(),
            TestEndTime=datetime.now(),
            TestedUnits=[
                TestedUnit(
                    UnitIdentifier="SN-001",
                    OverallResult=TestResult.PASSED,
                    Tests=[
                        Test(
                            TestName="Continuity",
                            Result=TestResult.PASSED,
                            Measurements=[],
                        )
                    ],
                ),
                TestedUnit(
                    UnitIdentifier="SN-002",
                    OverallResult=TestResult.FAILED,
                    Tests=[],
                ),
            ],
        )
        
        events = adapter.from_units_tested(message)
        
        assert len(events) == 2
        
        # Check first event
        assert events[0].event_type == EventType.TEST_RESULT
        payload = events[0].payload
        assert payload["unit_id"] == "SN-001"
        assert payload["passed"] == True
        assert payload["test_type"] == "ICT"
        
        # Check second event  
        assert events[1].payload["unit_id"] == "SN-002"
        assert events[1].payload["passed"] == False
    
    def test_adapt_with_measurements(self):
        """Should convert measurements correctly."""
        adapter = CFXTestResultAdapter()
        
        message = UnitsTested(
            TransactionId=uuid4(),
            TestMethod="FCT",
            TestStartTime=datetime.now(),
            TestEndTime=datetime.now(),
            TestedUnits=[
                TestedUnit(
                    UnitIdentifier="SN-100",
                    OverallResult=TestResult.PASSED,
                    Tests=[
                        Test(
                            TestName="Voltage Test",
                            Result=TestResult.PASSED,
                            Measurements=[
                                Measurement(
                                    MeasurementName="Vout",
                                    MeasuredValue=5.02,
                                    ExpectedValue=5.0,
                                    MeasurementUnits="V",
                                    LowerLimit=4.9,
                                    UpperLimit=5.1,
                                    Result=TestResult.PASSED,
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        
        events = adapter.from_units_tested(message)
        
        payload = events[0].payload
        assert len(payload["steps"]) == 1
        
        step = payload["steps"][0]
        assert step["name"] == "Voltage Test"
        assert len(step["measurements"]) == 1
        
        measurement = step["measurements"][0]
        assert measurement["name"] == "Vout"
        assert measurement["value"] == 5.02
        assert measurement["unit"] == "V"


class TestCFXMaterialAdapter:
    """Tests for CFXMaterialAdapter."""
    
    def test_adapt_materials_installed(self):
        """Should convert MaterialsInstalled to MaterialInstalledEvents."""
        adapter = CFXMaterialAdapter(source_endpoint="smt-line")
        
        message = MaterialsInstalled(
            TransactionId=uuid4(),
            InstalledMaterials=[
                InstalledMaterial(
                    UnitIdentifier="BOARD-001",
                    InstalledComponents=[
                        {
                            "ReferenceDesignator": "U1",
                            "InternalPartNumber": "MCU-123",
                            "Manufacturer": "STMicro",
                            "LotCode": "LOT-2024-001",
                        },
                        {
                            "ReferenceDesignator": "R1",
                            "InternalPartNumber": "RES-100",
                        },
                    ],
                )
            ],
        )
        
        events = adapter.from_materials_installed(message)
        
        assert len(events) == 1
        assert events[0].event_type == EventType.MATERIAL_INSTALLED
        
        payload = events[0].payload
        assert payload["unit_id"] == "BOARD-001"
        assert len(payload["components"]) == 2
        
        comp = payload["components"][0]
        assert comp["reference_designator"] == "U1"
        assert comp["part_number"] == "MCU-123"
        assert comp["manufacturer"] == "STMicro"


class TestCFXProductionAdapter:
    """Tests for CFXProductionAdapter."""
    
    def test_adapt_work_started(self):
        """Should convert WorkStarted to WorkStartedEvents."""
        adapter = CFXProductionAdapter(source_endpoint="assembly-station")
        
        message = WorkStarted(
            TransactionId=uuid4(),
            Lane=1,
            Stage="SMT",
            Units=[
                UnitPosition(PositionNumber=1, UnitIdentifier="PCB-001"),
                UnitPosition(PositionNumber=2, UnitIdentifier="PCB-002"),
            ],
        )
        
        events = adapter.from_work_started(message)
        
        assert len(events) == 2
        assert all(e.event_type == EventType.WORK_STARTED for e in events)
        
        assert events[0].payload["unit_id"] == "PCB-001"
        assert events[1].payload["unit_id"] == "PCB-002"
    
    def test_adapt_work_completed(self):
        """Should convert WorkCompleted to WorkCompletedEvents."""
        adapter = CFXProductionAdapter()
        
        message = WorkCompleted(
            TransactionId=uuid4(),
            Result=WorkResultState.COMPLETED,
            Lane=2,
            Stage="Assembly",
            Units=[
                UnitPosition(PositionNumber=1, UnitIdentifier="PCB-003"),
            ],
        )
        
        events = adapter.from_work_completed(message)
        
        assert len(events) == 1
        assert events[0].event_type == EventType.WORK_COMPLETED
        assert events[0].payload["result"] == "PASSED"


class TestCFXResourceAdapter:
    """Tests for CFXResourceAdapter."""
    
    def test_adapt_fault_occurred(self):
        """Should convert FaultOccurred to AssetFaultEvent."""
        adapter = CFXResourceAdapter(source_endpoint="oven-1")
        
        message = FaultOccurred(
            Fault={
                "Cause": "Zone temperature out of range",
                "Severity": "Error",
                "FaultCode": "TEMP_HIGH_Z3",
                "FaultOccurrenceId": "fault-123",
            },
            Lane=1,
            Stage="Reflow",
        )
        
        event = adapter.from_fault_occurred(message)
        
        assert event.event_type == EventType.ASSET_FAULT
        
        payload = event.payload
        assert payload["fault_code"] == "TEMP_HIGH_Z3"
        assert payload["severity"] == "error"
        assert payload["cleared"] == False
    
    def test_adapt_station_state_changed(self):
        """Should convert StationStateChanged to AssetStateChangedEvent."""
        adapter = CFXResourceAdapter(source_endpoint="printer-1")
        
        message = StationStateChanged(
            OldState=ResourceState.STANDBY,
            NewState=ResourceState.PROCESSING,
            OldStateDuration=300.0,
        )
        
        event = adapter.from_station_state_changed(message)
        
        assert event.event_type == EventType.ASSET_STATE_CHANGED
        
        payload = event.payload
        assert payload["old_state"] == "standby"
        assert payload["new_state"] == "processing"


# =============================================================================
# CFX Configuration Tests
# =============================================================================

class TestCFXConfig:
    """Tests for CFX configuration."""
    
    def test_default_config(self):
        """Should have sensible defaults."""
        config = CFXConfig()
        
        assert config.amqp.host == "localhost"
        assert config.amqp.port == 5672
        assert config.endpoint.vendor == "Virinco"
    
    def test_custom_amqp_config(self):
        """Should accept custom AMQP settings."""
        config = CFXConfig(
            amqp=AMQPConfig(
                host="broker.factory.com",
                port=5671,
                use_ssl=True,
            )
        )
        
        assert config.amqp.host == "broker.factory.com"
        assert config.amqp.use_ssl == True
    
    def test_endpoint_validation(self):
        """Should validate endpoint configuration."""
        endpoint = EndpointConfig(cfx_handle="//Virinco/WATS/Station1")
        endpoint.validate()  # Should not raise
        
        invalid = EndpointConfig(cfx_handle="InvalidHandle")
        with pytest.raises(ValueError):
            invalid.validate()
    
    def test_broker_url_generation(self):
        """Should generate correct broker URL."""
        amqp = AMQPConfig(
            host="broker.local",
            port=5672,
            username="user",
            password="pass",
        )
        
        assert "amqp://user:pass@broker.local:5672" in amqp.broker_url
    
    def test_config_from_dict(self):
        """Should create config from dictionary."""
        data = {
            "amqp": {
                "host": "cfx-broker.local",
                "port": 5672,
            },
            "endpoint": {
                "cfx_handle": "//Company/WATS/Station1",
                "vendor": "TestCo",
            },
            "exchange": {
                "exchange_name": "cfx.custom",
            },
        }
        
        config = CFXConfig.from_dict(data)
        
        assert config.amqp.host == "cfx-broker.local"
        assert config.endpoint.cfx_handle == "//Company/WATS/Station1"
        assert config.exchange.exchange_name == "cfx.custom"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
