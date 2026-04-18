"""Tests for Manual Inspection domain models.

Validates model creation, parsing from API responses, and serialization.
"""
import pytest
from uuid import UUID, uuid4
from datetime import datetime

from pywats.domains.manual_inspection.models import (
    TestSequenceDefinition,
    TestSequenceRelation,
    TestSequenceInstance,
    RelationConflict,
    MiSequence,
)


# =============================================================================
# TestSequenceDefinition
# =============================================================================


class TestTestSequenceDefinitionModel:
    """Tests for the TestSequenceDefinition model."""

    def test_create_minimal_definition(self) -> None:
        """Create a definition with only a name."""
        defn = TestSequenceDefinition(name="Visual Inspection")
        assert defn.name == "Visual Inspection"
        assert defn.test_sequence_definition_id is None
        assert defn.is_global is False
        assert defn.on_fail_goto_cleanup is False

    def test_create_full_definition(self) -> None:
        """Create a definition with all fields populated."""
        defn_id = uuid4()
        folder_id = uuid4()
        now = datetime(2026, 3, 21, 12, 0, 0)

        defn = TestSequenceDefinition(
            test_sequence_definition_id=defn_id,
            virtual_folder_id=folder_id,
            name="PCB Inspection",
            version=2,
            description="Visual inspection of PCB assembly",
            created=now,
            created_by="admin",
            created_by_site="00",
            released=now,
            released_by="admin",
            status=1,
            is_global=True,
            on_fail_goto_cleanup=True,
            on_fail_require_submit=True,
            on_fail_require_repair=1,
            add_child_units=True,
            log_operator=True,
            log_description=True,
            include_uur_misc_info_in_uut=True,
        )
        assert defn.test_sequence_definition_id == defn_id
        assert defn.virtual_folder_id == folder_id
        assert defn.name == "PCB Inspection"
        assert defn.version == 2
        assert defn.description == "Visual inspection of PCB assembly"
        assert defn.is_global is True
        assert defn.on_fail_goto_cleanup is True
        assert defn.on_fail_require_submit is True
        assert defn.on_fail_require_repair == 1
        assert defn.add_child_units is True
        assert defn.status == 1
        assert defn.released == now

    def test_parse_from_api_response(self) -> None:
        """Parse a definition from PascalCase API response."""
        defn_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        api_data = {
            "TestSequenceDefinitionId": defn_id,
            "Name": "Board Inspection",
            "Version": 3,
            "Description": "Standard board inspection",
            "Status": 2,
            "IsGlobal": False,
            "OnFailGotoCleanup": True,
            "OnFailRequireSubmit": False,
            "OnFailRequireRepair": 0,
            "AddChildUnits": False,
            "Created": "2026-03-20T10:00:00",
            "CreatedBy": "testuser",
        }
        defn = TestSequenceDefinition.model_validate(api_data)
        assert str(defn.test_sequence_definition_id) == defn_id
        assert defn.name == "Board Inspection"
        assert defn.version == 3
        assert defn.status == 2
        assert defn.on_fail_goto_cleanup is True
        assert defn.created_by == "testuser"

    def test_serialization_uses_pascal_case(self) -> None:
        """Model serialization uses PascalCase aliases for API compatibility."""
        defn = TestSequenceDefinition(name="Test", version=1, is_global=True)
        data = defn.model_dump(by_alias=True)
        assert data["Name"] == "Test"
        assert data["Version"] == 1
        assert data["IsGlobal"] is True

    def test_definition_defaults(self) -> None:
        """All boolean fields default to False, optional fields to None."""
        defn = TestSequenceDefinition()
        assert defn.name is None
        assert defn.is_global is False
        assert defn.on_fail_goto_cleanup is False
        assert defn.on_fail_require_submit is False
        assert defn.on_fail_require_repair == 0
        assert defn.add_child_units is False
        assert defn.repair_process_id is None


# =============================================================================
# TestSequenceRelation
# =============================================================================


class TestTestSequenceRelationModel:
    """Tests for the TestSequenceRelation model."""

    def test_create_relation(self) -> None:
        """Create a relation linking a definition to a product."""
        rel_id = uuid4()
        defn_id = uuid4()
        rel = TestSequenceRelation(
            test_sequence_relation_id=rel_id,
            test_sequence_definition_id=defn_id,
            entity_schema="Product",
            entity_name="WIDGET-001",
            entity_key="PartNumber",
            entity_value="WIDGET-001",
            status=1,
        )
        assert rel.test_sequence_relation_id == rel_id
        assert rel.test_sequence_definition_id == defn_id
        assert rel.entity_schema == "Product"
        assert rel.entity_name == "WIDGET-001"

    def test_parse_from_api_response(self) -> None:
        """Parse a relation from PascalCase API response."""
        api_data = {
            "TestSequenceRelationId": "11111111-2222-3333-4444-555555555555",
            "TestSequenceDefinitionId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "EntitySchema": "Process",
            "EntityName": "FCT",
            "EntityKey": "ProcessCode",
            "EntityValue": "100",
            "Status": 1,
        }
        rel = TestSequenceRelation.model_validate(api_data)
        assert rel.entity_schema == "Process"
        assert rel.entity_name == "FCT"
        assert rel.entity_value == "100"
        assert rel.status == 1

    def test_serialization_round_trip(self) -> None:
        """Serialize and re-parse a relation to verify round-trip."""
        rel = TestSequenceRelation(
            entity_schema="Product",
            entity_name="ABC-123",
            status=1,
        )
        data = rel.model_dump(by_alias=True, exclude_none=True)
        rel2 = TestSequenceRelation.model_validate(data)
        assert rel2.entity_schema == rel.entity_schema
        assert rel2.entity_name == rel.entity_name


# =============================================================================
# TestSequenceInstance
# =============================================================================


class TestTestSequenceInstanceModel:
    """Tests for the TestSequenceInstance model."""

    def test_create_instance(self) -> None:
        """Create an instance of a test sequence execution."""
        inst_id = uuid4()
        defn_id = uuid4()
        unit_id = uuid4()
        now = datetime(2026, 3, 21, 14, 30, 0)

        inst = TestSequenceInstance(
            test_sequence_instance_id=inst_id,
            test_sequence_definition_id=defn_id,
            unit_id=unit_id,
            serial_number="SN001",
            part_number="WIDGET-001",
            revision="A",
            created=now,
            last_event_time=now,
        )
        assert inst.test_sequence_instance_id == inst_id
        assert inst.serial_number == "SN001"
        assert inst.part_number == "WIDGET-001"
        assert inst.revision == "A"

    def test_parse_from_api_response(self) -> None:
        """Parse an instance from PascalCase API response."""
        api_data = {
            "TestSequenceInstanceId": "12345678-1234-1234-1234-123456789012",
            "TestSequenceDefinitionId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "SerialNumber": "SN-TEST-001",
            "PartNumber": "PART-001",
            "Revision": "B",
            "Created": "2026-03-20T08:00:00",
            "LastEventTime": "2026-03-20T09:15:00",
        }
        inst = TestSequenceInstance.model_validate(api_data)
        assert inst.serial_number == "SN-TEST-001"
        assert inst.part_number == "PART-001"
        assert inst.unit_id is None  # Not set in this response


# =============================================================================
# RelationConflict
# =============================================================================


class TestRelationConflictModel:
    """Tests for the RelationConflict model."""

    def test_create_conflict(self) -> None:
        """Create a relation conflict."""
        conflict = RelationConflict(
            test_sequence_definition_id=uuid4(),
            test_sequence_relation_id=uuid4(),
            name="Overlapping Inspection",
            entity_name="WIDGET-001",
            entity_value="PartNumber",
            status=1,
        )
        assert conflict.name == "Overlapping Inspection"
        assert conflict.entity_name == "WIDGET-001"

    def test_parse_from_api_response(self) -> None:
        """Parse a conflict from PascalCase API response."""
        api_data = {
            "TestSequenceDefinitionId": "11111111-1111-1111-1111-111111111111",
            "Name": "Conflict A",
            "EntityName": "PART-X",
            "Status": 2,
        }
        conflict = RelationConflict.model_validate(api_data)
        assert conflict.name == "Conflict A"
        assert conflict.entity_name == "PART-X"
        assert conflict.test_sequence_relation_id is None


# =============================================================================
# MiSequence
# =============================================================================


class TestMiSequenceModel:
    """Tests for the MiSequence model."""

    def test_create_sequence(self) -> None:
        """Create a sequence entry."""
        seq = MiSequence(
            test_sequence_definition_id=uuid4(),
            name="Step-by-step board inspection",
            version=1,
            status=1,
        )
        assert seq.name == "Step-by-step board inspection"
        assert seq.version == 1

    def test_parse_from_api_response(self) -> None:
        """Parse a sequence from PascalCase API response."""
        api_data = {
            "TestSequenceDefinitionId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "Name": "Assembly Check",
            "Version": 5,
            "Status": 1,
        }
        seq = MiSequence.model_validate(api_data)
        assert seq.name == "Assembly Check"
        assert seq.version == 5
        assert seq.status == 1
