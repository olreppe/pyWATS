"""Tests for Manual Inspection repository.

Uses mocked HTTP to verify correct URL construction, Referer headers,
and model deserialization from API responses.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from pywats.domains.manual_inspection.async_repository import (
    AsyncManualInspectionRepository,
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
def mock_http_client() -> AsyncMock:
    """Create a mock async HTTP client."""
    client = AsyncMock()
    return client


@pytest.fixture
def mock_error_handler() -> MagicMock:
    """Create a mock error handler that passes data through."""
    handler = MagicMock()
    handler.handle_response = MagicMock(side_effect=lambda resp, **kw: resp.data)
    return handler


@pytest.fixture
def base_url() -> str:
    return "https://test-wats.example.com"


@pytest.fixture
def repository(
    mock_http_client: AsyncMock,
    mock_error_handler: MagicMock,
    base_url: str,
) -> AsyncManualInspectionRepository:
    """Create a repository with mocked dependencies."""
    return AsyncManualInspectionRepository(
        http_client=mock_http_client,
        error_handler=mock_error_handler,
        base_url=base_url,
    )


def _make_response(data):
    """Create a mock response with .data attribute."""
    resp = MagicMock()
    resp.data = data
    return resp


# =============================================================================
# Definition Tests
# =============================================================================


class TestDefinitionOperations:
    """Tests for definition CRUD operations."""

    @pytest.mark.asyncio
    async def test_get_definitions_returns_list(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetTestSequenceDefinitions returns list of definitions."""
        defn_id = str(uuid4())
        mock_http_client.get.return_value = _make_response([
            {"TestSequenceDefinitionId": defn_id, "Name": "Def A", "Version": 1},
            {"TestSequenceDefinitionId": str(uuid4()), "Name": "Def B", "Version": 2},
        ])

        result = await repository.get_definitions()

        assert len(result) == 2
        assert isinstance(result[0], TestSequenceDefinition)
        assert result[0].name == "Def A"
        assert result[1].name == "Def B"

        # Verify isGlobalDefinitions param and Referer header
        call_kwargs = mock_http_client.get.call_args
        assert call_kwargs.kwargs["params"] == {"isGlobalDefinitions": "false"}
        assert call_kwargs.kwargs["headers"]["Referer"] == "https://test-wats.example.com"

    @pytest.mark.asyncio
    async def test_get_definitions_empty(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET returns empty list when no definitions exist."""
        mock_http_client.get.return_value = _make_response([])
        result = await repository.get_definitions()
        assert result == []

    @pytest.mark.asyncio
    async def test_get_definition_by_id(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetTestSequenceDefinition returns single definition."""
        defn_id = str(uuid4())
        mock_http_client.get.return_value = _make_response(
            {"TestSequenceDefinitionId": defn_id, "Name": "Target Def", "Status": 1}
        )

        result = await repository.get_definition(defn_id)

        assert result is not None
        assert result.name == "Target Def"
        # Verify query parameter was passed
        call_kwargs = mock_http_client.get.call_args
        assert call_kwargs.kwargs.get("params", {}).get("definitionId") == defn_id

    @pytest.mark.asyncio
    async def test_get_definition_not_found(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET returns None when definition not found."""
        mock_http_client.get.return_value = _make_response(None)
        result = await repository.get_definition(str(uuid4()))
        assert result is None

    @pytest.mark.asyncio
    async def test_get_definition_copy(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetDefinitionCopy/{id} returns a copy."""
        defn_id = str(uuid4())
        mock_http_client.get.return_value = _make_response(
            {"Name": "Copy of Def", "Version": 1}
        )

        result = await repository.get_definition_copy(defn_id)

        assert result is not None
        assert result.name == "Copy of Def"
        # Verify URL contains the ID
        call_args = mock_http_client.get.call_args
        assert defn_id in call_args.args[0]

    @pytest.mark.asyncio
    async def test_get_instances_count(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetInstancesCount/{id} returns integer count."""
        defn_id = str(uuid4())
        mock_http_client.get.return_value = _make_response(42)

        count = await repository.get_instances_count(defn_id)
        assert count == 42

    @pytest.mark.asyncio
    async def test_get_instances_count_none(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET returns 0 when count is unavailable."""
        mock_http_client.get.return_value = _make_response(None)
        count = await repository.get_instances_count(str(uuid4()))
        assert count == 0

    @pytest.mark.asyncio
    async def test_post_definition(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """POST PostDefinition creates a definition."""
        new_id = str(uuid4())
        mock_http_client.post.return_value = _make_response(
            {"TestSequenceDefinitionId": new_id, "Name": "New Def"}
        )

        payload = {"Name": "New Def"}
        result = await repository.post_definition(payload)

        assert result is not None
        assert result.name == "New Def"
        call_kwargs = mock_http_client.post.call_args
        assert call_kwargs.kwargs["headers"]["Referer"] == "https://test-wats.example.com"

    @pytest.mark.asyncio
    async def test_put_definition(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """PUT PutDefinitionNew updates a definition."""
        defn_id = str(uuid4())
        mock_http_client.put.return_value = _make_response(
            {"TestSequenceDefinitionId": defn_id, "Name": "Updated Def", "Version": 2}
        )

        payload = {"TestSequenceDefinitionId": defn_id, "Name": "Updated Def"}
        result = await repository.put_definition(payload)

        assert result is not None
        assert result.name == "Updated Def"


# =============================================================================
# Relation Tests
# =============================================================================


class TestRelationOperations:
    """Tests for relation CRUD operations."""

    @pytest.mark.asyncio
    async def test_get_relations(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetRelations/{id} returns list of relations."""
        defn_id = str(uuid4())
        mock_http_client.get.return_value = _make_response([
            {
                "TestSequenceRelationId": str(uuid4()),
                "TestSequenceDefinitionId": defn_id,
                "EntitySchema": "Product",
                "EntityName": "WIDGET-001",
            },
        ])

        result = await repository.get_relations(defn_id)

        assert len(result) == 1
        assert isinstance(result[0], TestSequenceRelation)
        assert result[0].entity_schema == "Product"
        assert defn_id in mock_http_client.get.call_args.args[0]

    @pytest.mark.asyncio
    async def test_get_relation_conflicts_new(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetRelationConflictsNew/{id} returns conflicts."""
        defn_id = str(uuid4())
        mock_http_client.get.return_value = _make_response([
            {"Name": "Conflict X", "EntityName": "PART-A", "Status": 1},
        ])

        result = await repository.get_relation_conflicts_new(defn_id)

        assert len(result) == 1
        assert isinstance(result[0], RelationConflict)
        assert result[0].name == "Conflict X"

    @pytest.mark.asyncio
    async def test_post_relation(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """POST PostRelation creates a relation."""
        mock_http_client.post.return_value = _make_response(
            {"EntitySchema": "Product", "EntityName": "NEW-PART"}
        )

        result = await repository.post_relation(
            {"EntitySchema": "Product", "EntityName": "NEW-PART"}
        )

        assert result is not None
        assert result.entity_name == "NEW-PART"

    @pytest.mark.asyncio
    async def test_delete_relation_uses_put(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """DELETE relation actually uses PUT (API design quirk)."""
        mock_http_client.put.return_value = _make_response(True)

        result = await repository.delete_relation({"TestSequenceRelationId": str(uuid4())})

        # Verify PUT was called (not DELETE)
        mock_http_client.put.assert_called_once()
        mock_http_client.delete.assert_not_called()


# =============================================================================
# Sequence Tests
# =============================================================================


class TestSequenceOperations:
    """Tests for sequence operations."""

    @pytest.mark.asyncio
    async def test_get_sequences(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetSequences returns list."""
        mock_http_client.get.return_value = _make_response([
            {"Name": "Seq 1", "Version": 1, "Status": 1},
            {"Name": "Seq 2", "Version": 2, "Status": 1},
        ])

        result = await repository.get_sequences()

        assert len(result) == 2
        assert isinstance(result[0], MiSequence)
        assert result[0].name == "Seq 1"

    @pytest.mark.asyncio
    async def test_delete_sequence(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """DELETE DeleteSequence/{id} calls delete with correct URL."""
        seq_id = str(uuid4())
        mock_http_client.delete.return_value = _make_response(True)

        await repository.delete_sequence(seq_id)

        call_args = mock_http_client.delete.call_args
        assert seq_id in call_args.args[0]
        assert call_args.kwargs["headers"]["Referer"] == "https://test-wats.example.com"


# =============================================================================
# MI Details Tests
# =============================================================================


class TestMiDetailsOperations:
    """Tests for MI details / instance operations."""

    @pytest.mark.asyncio
    async def test_get_mi_details_new(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET GetMiDetailsNew/{id} returns instance."""
        unit_id = str(uuid4())
        mock_http_client.get.return_value = _make_response({
            "TestSequenceInstanceId": str(uuid4()),
            "SerialNumber": "SN-001",
            "PartNumber": "PART-001",
        })

        result = await repository.get_mi_details_new(unit_id)

        assert result is not None
        assert isinstance(result, TestSequenceInstance)
        assert result.serial_number == "SN-001"

    @pytest.mark.asyncio
    async def test_get_mi_details_not_found(
        self, repository: AsyncManualInspectionRepository, mock_http_client: AsyncMock
    ) -> None:
        """GET returns None when no MI details found."""
        mock_http_client.get.return_value = _make_response(None)
        result = await repository.get_mi_details_new(str(uuid4()))
        assert result is None


# =============================================================================
# Referer Header Tests
# =============================================================================


class TestRefererHeader:
    """Verify all internal API calls include the Referer header."""

    @pytest.mark.asyncio
    async def test_get_definitions_sends_referer(
        self,
        repository: AsyncManualInspectionRepository,
        mock_http_client: AsyncMock,
        base_url: str,
    ) -> None:
        """Every GET call must include Referer header."""
        mock_http_client.get.return_value = _make_response([])
        await repository.get_definitions()
        call_kwargs = mock_http_client.get.call_args
        assert call_kwargs.kwargs["headers"]["Referer"] == base_url

    @pytest.mark.asyncio
    async def test_post_sends_referer(
        self,
        repository: AsyncManualInspectionRepository,
        mock_http_client: AsyncMock,
        base_url: str,
    ) -> None:
        """POST calls must include Referer header."""
        mock_http_client.post.return_value = _make_response(None)
        await repository.post_definition({"Name": "Test"})
        call_kwargs = mock_http_client.post.call_args
        assert call_kwargs.kwargs["headers"]["Referer"] == base_url

    @pytest.mark.asyncio
    async def test_put_sends_referer(
        self,
        repository: AsyncManualInspectionRepository,
        mock_http_client: AsyncMock,
        base_url: str,
    ) -> None:
        """PUT calls must include Referer header."""
        mock_http_client.put.return_value = _make_response(None)
        await repository.put_definition({"Name": "Test"})
        call_kwargs = mock_http_client.put.call_args
        assert call_kwargs.kwargs["headers"]["Referer"] == base_url

    @pytest.mark.asyncio
    async def test_delete_sends_referer(
        self,
        repository: AsyncManualInspectionRepository,
        mock_http_client: AsyncMock,
        base_url: str,
    ) -> None:
        """DELETE calls must include Referer header."""
        mock_http_client.delete.return_value = _make_response(None)
        await repository.delete_sequence("some-id")
        call_kwargs = mock_http_client.delete.call_args
        assert call_kwargs.kwargs["headers"]["Referer"] == base_url

    @pytest.mark.asyncio
    async def test_trailing_slash_stripped_from_base_url(self) -> None:
        """Base URL trailing slash should be stripped."""
        from pywats.core.exceptions import ErrorHandler, ErrorMode
        client = AsyncMock()
        client.get.return_value = _make_response([])
        handler = MagicMock()
        handler.handle_response = MagicMock(side_effect=lambda resp, **kw: resp.data)

        repo = AsyncManualInspectionRepository(
            http_client=client,
            error_handler=handler,
            base_url="https://example.com/wats/",
        )
        await repo.get_definitions()
        call_kwargs = client.get.call_args
        assert call_kwargs.kwargs["headers"]["Referer"] == "https://example.com/wats"
