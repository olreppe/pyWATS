"""Tests for Manual Inspection service.

Uses a mocked repository to verify service-level logic:
model deserialization, parameter construction, and method delegation.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from pywats.domains.manual_inspection.async_service import (
    AsyncManualInspectionService,
)
from pywats.domains.manual_inspection.models import (
    TestSequenceDefinition,
    TestSequenceRelation,
    TestSequenceInstance,
    RelationConflict,
    MiSequence,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def mock_repository() -> AsyncMock:
    """Create a fully-mocked repository."""
    repo = AsyncMock()
    return repo


@pytest.fixture
def service(mock_repository: AsyncMock) -> AsyncManualInspectionService:
    """Create a service with mocked repository."""
    return AsyncManualInspectionService(repository=mock_repository)


# =============================================================================
# Definition Tests
# =============================================================================


class TestDefinitionService:
    """Tests for definition operations via the service layer."""

    @pytest.mark.asyncio
    async def test_list_definitions(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """list_definitions delegates to repository.get_definitions."""
        expected = [
            TestSequenceDefinition(name="Def A"),
            TestSequenceDefinition(name="Def B"),
        ]
        mock_repository.get_definitions.return_value = expected

        result = await service.list_definitions()

        assert result == expected
        mock_repository.get_definitions.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_definition(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """get_definition delegates to repository.get_definition."""
        defn_id = str(uuid4())
        expected = TestSequenceDefinition(name="Target")
        mock_repository.get_definition.return_value = expected

        result = await service.get_definition(defn_id)

        assert result == expected
        mock_repository.get_definition.assert_awaited_once_with(defn_id)

    @pytest.mark.asyncio
    async def test_create_definition_builds_payload(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """create_definition builds correct payload with PascalCase keys."""
        mock_repository.post_definition.return_value = TestSequenceDefinition(
            name="New Def"
        )

        result = await service.create_definition(
            name="New Def",
            description="A test definition",
            is_global=True,
            on_fail_goto_cleanup=True,
        )

        assert result is not None
        assert result.name == "New Def"

        # Verify the payload sent to repository
        call_args = mock_repository.post_definition.call_args
        payload = call_args.args[0]
        assert payload["Name"] == "New Def"
        assert payload["Description"] == "A test definition"
        assert payload["IsGlobal"] is True
        assert payload["OnFailGotoCleanup"] is True
        assert payload["OnFailRequireSubmit"] is False
        assert payload["OnFailRequireRepair"] == 0
        assert payload["AddChildUnits"] is False

    @pytest.mark.asyncio
    async def test_update_definition_includes_id(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """update_definition always includes definition ID in payload."""
        defn_id = str(uuid4())
        mock_repository.put_definition.return_value = TestSequenceDefinition(
            name="Updated"
        )

        await service.update_definition(defn_id, Name="Updated", Version=2)

        call_args = mock_repository.put_definition.call_args
        payload = call_args.args[0]
        assert payload["TestSequenceDefinitionId"] == defn_id
        assert payload["Name"] == "Updated"
        assert payload["Version"] == 2

    @pytest.mark.asyncio
    async def test_copy_definition(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """copy_definition delegates to repository.get_definition_copy."""
        defn_id = str(uuid4())
        mock_repository.get_definition_copy.return_value = TestSequenceDefinition(
            name="Copy"
        )

        result = await service.copy_definition(defn_id)
        assert result is not None
        assert result.name == "Copy"
        mock_repository.get_definition_copy.assert_awaited_once_with(defn_id)

    @pytest.mark.asyncio
    async def test_get_instances_count(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """get_instances_count delegates to repository."""
        mock_repository.get_instances_count.return_value = 15
        count = await service.get_instances_count("def-id")
        assert count == 15


# =============================================================================
# Relation Tests
# =============================================================================


class TestRelationService:
    """Tests for relation operations via the service layer."""

    @pytest.mark.asyncio
    async def test_list_relations(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """list_relations delegates to repository.get_relations."""
        defn_id = str(uuid4())
        expected = [TestSequenceRelation(entity_schema="Product")]
        mock_repository.get_relations.return_value = expected

        result = await service.list_relations(defn_id)
        assert result == expected
        mock_repository.get_relations.assert_awaited_once_with(defn_id)

    @pytest.mark.asyncio
    async def test_get_relation_conflicts_uses_new_endpoint(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """get_relation_conflicts should use the _new variant."""
        defn_id = str(uuid4())
        mock_repository.get_relation_conflicts_new.return_value = []

        await service.get_relation_conflicts(defn_id)

        mock_repository.get_relation_conflicts_new.assert_awaited_once_with(defn_id)
        # The legacy method should NOT be called
        mock_repository.get_relation_conflicts.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_relation_builds_payload(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """create_relation builds correct payload."""
        defn_id = str(uuid4())
        mock_repository.post_relation.return_value = TestSequenceRelation(
            entity_schema="Product", entity_name="WIDGET-001"
        )

        result = await service.create_relation(
            definition_id=defn_id,
            entity_schema="Product",
            entity_name="WIDGET-001",
            entity_value="PartNumber",
        )

        assert result is not None
        call_args = mock_repository.post_relation.call_args
        payload = call_args.args[0]
        assert payload["TestSequenceDefinitionId"] == defn_id
        assert payload["EntitySchema"] == "Product"
        assert payload["EntityName"] == "WIDGET-001"
        assert payload["EntityValue"] == "PartNumber"

    @pytest.mark.asyncio
    async def test_delete_relation_delegates(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """delete_relation delegates to repository."""
        payload = {"TestSequenceRelationId": str(uuid4())}
        mock_repository.delete_relation.return_value = True
        await service.delete_relation(payload)
        mock_repository.delete_relation.assert_awaited_once_with(payload)


# =============================================================================
# Sequence Tests
# =============================================================================


class TestSequenceService:
    """Tests for sequence operations via the service layer."""

    @pytest.mark.asyncio
    async def test_list_sequences(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """list_sequences delegates to repository."""
        expected = [MiSequence(name="Seq 1")]
        mock_repository.get_sequences.return_value = expected
        result = await service.list_sequences()
        assert result == expected

    @pytest.mark.asyncio
    async def test_delete_sequence(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """delete_sequence delegates with correct ID."""
        await service.delete_sequence("seq-123")
        mock_repository.delete_sequence.assert_awaited_once_with("seq-123")


# =============================================================================
# MI Details Tests
# =============================================================================


class TestMiDetailsService:
    """Tests for MI details via the service layer."""

    @pytest.mark.asyncio
    async def test_get_mi_details_uses_new_endpoint(
        self, service: AsyncManualInspectionService, mock_repository: AsyncMock
    ) -> None:
        """get_mi_details should use the _new variant (preferred)."""
        unit_id = str(uuid4())
        expected = TestSequenceInstance(serial_number="SN-001")
        mock_repository.get_mi_details_new.return_value = expected

        result = await service.get_mi_details(unit_id)

        assert result == expected
        mock_repository.get_mi_details_new.assert_awaited_once_with(unit_id)
