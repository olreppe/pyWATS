"""Async Manual Inspection repository - data access layer.

Uses the WATS internal API endpoints for manual inspection operations.
All endpoints are defined in pywats.core.routes.Routes.ManualInspection.

⚠️ All methods use internal API endpoints that may change without notice.
"""
from typing import List, Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...core.async_client import AsyncHttpClient
    from ...core.exceptions import ErrorHandler

from ...core.routes import Routes
from .models import (
    TestSequenceDefinition,
    TestSequenceRelation,
    TestSequenceInstance,
    RelationConflict,
    MiSequence,
)


class AsyncManualInspectionRepository:
    """
    Async Manual Inspection data access layer.

    All endpoints are internal API (``/api/internal/ManualInspection/``).

    Internal API (⚠️ INTERNAL):
    - GET  GetTestSequenceDefinitions
    - GET  GetTestSequenceDefinition
    - GET  GetDefinitionCopy/{id}
    - GET  GetInstancesCount/{id}
    - GET  GetMiDetails/{id}  /  GetMiDetailsNew/{id}
    - GET  GetRelations/{id}
    - GET  GetRelationConflicts/{id}  /  GetRelationConflictsNew/{id}
    - GET  GetSequences
    - POST PostDefinition
    - POST PostRelation
    - PUT  PutDefinitionNew
    - PUT  PutRelation
    - PUT  PutSequence
    - PUT  DeleteRelationNew
    - PUT  ValidateMiscInfo
    - PUT  PutStringTest
    - DELETE DeleteSequence
    """

    def __init__(
        self,
        http_client: "AsyncHttpClient",
        error_handler: Optional["ErrorHandler"] = None,
        base_url: Optional[str] = None,
    ) -> None:
        """
        Initialize repository with async HTTP client.

        Args:
            http_client: AsyncHttpClient for making async HTTP requests
            error_handler: ErrorHandler for response handling
            base_url: Base URL for Referer header (required for internal API)
        """
        from ...core.exceptions import ErrorHandler, ErrorMode
        self._http_client = http_client
        self._error_handler = error_handler or ErrorHandler(ErrorMode.STRICT)
        self._base_url = (base_url or "").rstrip("/")

    # =========================================================================
    # Internal API Helpers
    # =========================================================================

    async def _internal_get(
        self,
        endpoint: str,
        operation: str = "internal_get",
        params: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Make an internal API GET request with Referer header."""
        response = await self._http_client.get(
            endpoint,
            params=params,
            headers={"Referer": self._base_url},
        )
        return self._error_handler.handle_response(
            response, operation=operation, allow_empty=True
        )

    async def _internal_post(
        self,
        endpoint: str,
        data: Any = None,
        operation: str = "internal_post",
    ) -> Any:
        """Make an internal API POST request with Referer header."""
        response = await self._http_client.post(
            endpoint,
            data=data,
            headers={"Referer": self._base_url},
        )
        return self._error_handler.handle_response(
            response, operation=operation, allow_empty=True
        )

    async def _internal_put(
        self,
        endpoint: str,
        data: Any = None,
        operation: str = "internal_put",
    ) -> Any:
        """Make an internal API PUT request with Referer header."""
        response = await self._http_client.put(
            endpoint,
            data=data,
            headers={"Referer": self._base_url},
        )
        return self._error_handler.handle_response(
            response, operation=operation, allow_empty=True
        )

    async def _internal_delete(
        self,
        endpoint: str,
        operation: str = "internal_delete",
    ) -> Any:
        """Make an internal API DELETE request with Referer header."""
        response = await self._http_client.delete(
            endpoint,
            headers={"Referer": self._base_url},
        )
        return self._error_handler.handle_response(
            response, operation=operation, allow_empty=True
        )

    # =========================================================================
    # Definitions
    # =========================================================================

    async def get_definitions(
        self, is_global: bool = False
    ) -> List[TestSequenceDefinition]:
        """
        Get test sequence definitions.

        GET /api/internal/ManualInspection/GetTestSequenceDefinitions?isGlobalDefinitions={bool}

        Args:
            is_global: If True, return global definitions (reusable by other sequences).
                       If False, return non-global (standard) definitions.

        Returns:
            List of TestSequenceDefinition objects
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.GET_DEFINITIONS,
            operation="get_definitions",
            params={"isGlobalDefinitions": str(is_global).lower()},
        )
        if data and isinstance(data, list):
            return [TestSequenceDefinition.model_validate(d) for d in data]
        return []

    async def get_definition(self, definition_id: str) -> Optional[TestSequenceDefinition]:
        """
        Get a single test sequence definition.

        GET /api/internal/ManualInspection/GetTestSequenceDefinition

        Args:
            definition_id: The definition GUID (passed as query parameter)

        Returns:
            TestSequenceDefinition or None
        """
        response = await self._http_client.get(
            Routes.ManualInspection.Internal.GET_DEFINITION,
            params={"definitionId": definition_id},
            headers={"Referer": self._base_url},
        )
        data = self._error_handler.handle_response(
            response, operation="get_definition", allow_empty=True
        )
        if data:
            return TestSequenceDefinition.model_validate(data)
        return None

    async def get_definition_copy(self, definition_id: str) -> Optional[TestSequenceDefinition]:
        """
        Get a copy of a test sequence definition.

        GET /api/internal/ManualInspection/GetDefinitionCopy/{id}

        Args:
            definition_id: The definition GUID

        Returns:
            Copied TestSequenceDefinition or None
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.get_definition_copy(definition_id),
            operation="get_definition_copy",
        )
        if data:
            return TestSequenceDefinition.model_validate(data)
        return None

    async def get_instances_count(self, definition_id: str) -> int:
        """
        Get the number of instances for a definition.

        GET /api/internal/ManualInspection/GetInstancesCount/{id}

        Args:
            definition_id: The definition GUID

        Returns:
            Instance count (0 if unavailable)
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.get_instances_count(definition_id),
            operation="get_instances_count",
        )
        if data is not None:
            return int(data)
        return 0

    async def post_definition(
        self, payload: Dict[str, Any]
    ) -> Optional[TestSequenceDefinition]:
        """
        Create a new test sequence definition.

        POST /api/internal/ManualInspection/PostDefinition

        Args:
            payload: Definition data dict

        Returns:
            Created TestSequenceDefinition or None
        """
        data = await self._internal_post(
            Routes.ManualInspection.Internal.POST_DEFINITION,
            data=payload,
            operation="post_definition",
        )
        if data:
            return TestSequenceDefinition.model_validate(data)
        return None

    async def put_definition(
        self, payload: Dict[str, Any]
    ) -> Optional[TestSequenceDefinition]:
        """
        Update an existing test sequence definition.

        PUT /api/internal/ManualInspection/PutDefinitionNew

        Args:
            payload: Updated definition data dict

        Returns:
            Updated TestSequenceDefinition or None
        """
        data = await self._internal_put(
            Routes.ManualInspection.Internal.PUT_DEFINITION,
            data=payload,
            operation="put_definition",
        )
        if data:
            return TestSequenceDefinition.model_validate(data)
        return None

    # =========================================================================
    # Relations
    # =========================================================================

    async def get_relations(self, definition_id: str) -> List[TestSequenceRelation]:
        """
        Get relations for a definition.

        GET /api/internal/ManualInspection/GetRelations/{id}

        Args:
            definition_id: The definition GUID

        Returns:
            List of TestSequenceRelation objects
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.get_relations(definition_id),
            operation="get_relations",
        )
        if data and isinstance(data, list):
            return [TestSequenceRelation.model_validate(r) for r in data]
        return []

    async def get_relation_conflicts(
        self, definition_id: str
    ) -> List[RelationConflict]:
        """
        Get relation conflicts (legacy endpoint).

        GET /api/internal/ManualInspection/GetRelationConflicts/{id}

        Args:
            definition_id: The definition GUID

        Returns:
            List of RelationConflict objects
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.get_relation_conflicts(definition_id),
            operation="get_relation_conflicts",
        )
        if data and isinstance(data, list):
            return [RelationConflict.model_validate(c) for c in data]
        return []

    async def get_relation_conflicts_new(
        self, definition_id: str
    ) -> List[RelationConflict]:
        """
        Get relation conflicts (preferred newer endpoint).

        GET /api/internal/ManualInspection/GetRelationConflictsNew/{id}

        Args:
            definition_id: The definition GUID

        Returns:
            List of RelationConflict objects
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.get_relation_conflicts_new(definition_id),
            operation="get_relation_conflicts_new",
        )
        if data and isinstance(data, list):
            return [RelationConflict.model_validate(c) for c in data]
        return []

    async def post_relation(
        self, payload: Dict[str, Any]
    ) -> Optional[TestSequenceRelation]:
        """
        Create a new relation.

        POST /api/internal/ManualInspection/PostRelation

        Args:
            payload: Relation data dict

        Returns:
            Created TestSequenceRelation or None
        """
        data = await self._internal_post(
            Routes.ManualInspection.Internal.POST_RELATION,
            data=payload,
            operation="post_relation",
        )
        if data:
            return TestSequenceRelation.model_validate(data)
        return None

    async def put_relation(
        self, payload: Dict[str, Any]
    ) -> Optional[TestSequenceRelation]:
        """
        Update an existing relation.

        PUT /api/internal/ManualInspection/PutRelation

        Args:
            payload: Updated relation data dict

        Returns:
            Updated TestSequenceRelation or None
        """
        data = await self._internal_put(
            Routes.ManualInspection.Internal.PUT_RELATION,
            data=payload,
            operation="put_relation",
        )
        if data:
            return TestSequenceRelation.model_validate(data)
        return None

    async def delete_relation(self, payload: Dict[str, Any]) -> Any:
        """
        Delete a relation (uses PUT, not DELETE).

        PUT /api/internal/ManualInspection/DeleteRelationNew

        Args:
            payload: Relation data identifying the relation to remove

        Returns:
            Server response data
        """
        return await self._internal_put(
            Routes.ManualInspection.Internal.DELETE_RELATION,
            data=payload,
            operation="delete_relation",
        )

    # =========================================================================
    # Sequences
    # =========================================================================

    async def get_sequences(self) -> List[MiSequence]:
        """
        Get all available sequences.

        GET /api/internal/ManualInspection/GetSequences

        Returns:
            List of MiSequence objects
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.GET_SEQUENCES,
            operation="get_sequences",
        )
        if data and isinstance(data, list):
            return [MiSequence.model_validate(s) for s in data]
        return []

    async def put_sequence(self, payload: Dict[str, Any]) -> Any:
        """
        Update a sequence.

        PUT /api/internal/ManualInspection/PutSequence

        Args:
            payload: Sequence data dict

        Returns:
            Server response data
        """
        return await self._internal_put(
            Routes.ManualInspection.Internal.PUT_SEQUENCE,
            data=payload,
            operation="put_sequence",
        )

    async def delete_sequence(self, sequence_id: str) -> Any:
        """
        Delete a sequence.

        DELETE /api/internal/ManualInspection/DeleteSequence/{id}

        Args:
            sequence_id: The sequence identifier

        Returns:
            Server response data
        """
        return await self._internal_delete(
            Routes.ManualInspection.Internal.delete_sequence(sequence_id),
            operation="delete_sequence",
        )

    # =========================================================================
    # Unit Details
    # =========================================================================

    async def get_mi_details(self, unit_id: str) -> Optional[TestSequenceInstance]:
        """
        Get MI details for a unit (legacy endpoint).

        GET /api/internal/ManualInspection/GetMiDetails/{id}

        Args:
            unit_id: The unit/instance identifier

        Returns:
            TestSequenceInstance or None
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.get_mi_details(unit_id),
            operation="get_mi_details",
        )
        if data:
            return TestSequenceInstance.model_validate(data)
        return None

    async def get_mi_details_new(self, unit_id: str) -> Optional[TestSequenceInstance]:
        """
        Get MI details for a unit (preferred newer endpoint).

        GET /api/internal/ManualInspection/GetMiDetailsNew/{id}

        Args:
            unit_id: The unit/instance identifier

        Returns:
            TestSequenceInstance or None
        """
        data = await self._internal_get(
            Routes.ManualInspection.Internal.get_mi_details_new(unit_id),
            operation="get_mi_details_new",
        )
        if data:
            return TestSequenceInstance.model_validate(data)
        return None

    # =========================================================================
    # Misc / Validation
    # =========================================================================

    # =========================================================================
    # XAML / WWF Content
    # =========================================================================

    async def get_xaml(self, definition_id: str) -> Any:
        """
        Get the XAML content for a test sequence definition.

        GET /api/internal/ManualInspection/GetTestSequenceDefinitionXaml

        Args:
            definition_id: The definition GUID

        Returns:
            XAML data (dict or string) from server
        """
        response = await self._http_client.get(
            Routes.ManualInspection.Internal.GET_XAML,
            params={"definitionId": definition_id},
            headers={"Referer": self._base_url},
        )
        return self._error_handler.handle_response(
            response, operation="get_xaml", allow_empty=True
        )

    async def put_xaml(self, payload: Dict[str, Any]) -> Any:
        """
        Save XAML content for a test sequence definition.

        PUT /api/internal/ManualInspection/PutTestSequenceDefinitionXaml

        Args:
            payload: XAML data dict

        Returns:
            Server response data
        """
        return await self._internal_put(
            Routes.ManualInspection.Internal.PUT_XAML,
            data=payload,
            operation="put_xaml",
        )

    async def get_wwf_content(self, definition_id: str) -> Any:
        """
        Get the Windows Workflow Foundation content for a definition.

        GET /api/internal/ManualInspection/GetWatswwfContent/{id}

        Args:
            definition_id: The definition GUID

        Returns:
            WWF content from server (may be binary/string)
        """
        return await self._internal_get(
            Routes.ManualInspection.Internal.get_wwf_content(definition_id),
            operation="get_wwf_content",
        )

    # =========================================================================
    # Misc / Validation
    # =========================================================================

    async def validate_misc_info(self, payload: Dict[str, Any]) -> Any:
        """
        Validate misc info fields.

        PUT /api/internal/ManualInspection/ValidateMiscInfo

        Args:
            payload: Data to validate

        Returns:
            Validation result from server
        """
        return await self._internal_put(
            Routes.ManualInspection.Internal.VALIDATE_MISC_INFO,
            data=payload,
            operation="validate_misc_info",
        )

    async def put_string_test(self, payload: Dict[str, Any]) -> Any:
        """
        Update a string test entry.

        PUT /api/internal/ManualInspection/PutStringTest

        Args:
            payload: String test data

        Returns:
            Server response data
        """
        return await self._internal_put(
            Routes.ManualInspection.Internal.PUT_STRING_TEST,
            data=payload,
            operation="put_string_test",
        )
