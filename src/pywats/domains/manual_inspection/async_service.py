"""Async Manual Inspection service - business logic layer.

Uses the WATS internal API for manual inspection operations.

⚠️ All methods use internal API endpoints that may change without notice.
"""
from typing import List, Optional, Dict, Any
from uuid import UUID
import logging
from pywats.core.logging import get_logger

from .async_repository import AsyncManualInspectionRepository
from .models import (
    TestSequenceDefinition,
    TestSequenceRelation,
    TestSequenceInstance,
    RelationConflict,
    MiSequence,
)

logger = get_logger(__name__)


class AsyncManualInspectionService:
    """
    Async Manual Inspection business logic layer.

    Provides typed, user-friendly methods for managing MI definitions,
    relations, sequences, and per-unit inspection details.

    Example:
        # List all definitions
        definitions = await api.manual_inspection.list_definitions()

        # Get a specific definition
        defn = await api.manual_inspection.get_definition(defn_id)

        # Create a definition
        new_defn = await api.manual_inspection.create_definition(
            name="Board Visual Inspection",
            description="Visual inspection for PCB assembly",
        )

        # Get MI details for a unit
        details = await api.manual_inspection.get_mi_details(unit_id)
    """

    def __init__(
        self,
        repository: AsyncManualInspectionRepository,
    ) -> None:
        """
        Initialize service with repository.

        Args:
            repository: AsyncManualInspectionRepository instance
        """
        self._repository = repository

    # =========================================================================
    # Definitions
    # =========================================================================

    async def list_definitions(
        self, is_global: bool = False
    ) -> List[TestSequenceDefinition]:
        """
        List test sequence definitions.

        Args:
            is_global: If True, return global definitions (reusable by other sequences).
                       If False, return non-global (standard) definitions.

        Returns:
            List of TestSequenceDefinition objects
        """
        return await self._repository.get_definitions(is_global=is_global)

    async def get_definition(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Get a single test sequence definition by ID.

        Args:
            definition_id: Definition GUID string

        Returns:
            TestSequenceDefinition or None if not found
        """
        return await self._repository.get_definition(definition_id)

    async def create_definition(
        self,
        name: str,
        description: Optional[str] = None,
        is_global: bool = False,
        on_fail_goto_cleanup: bool = False,
        on_fail_require_submit: bool = False,
        on_fail_require_repair: int = 0,
        add_child_units: bool = False,
        **extra_fields: Any,
    ) -> Optional[TestSequenceDefinition]:
        """
        Create a new test sequence definition.

        Args:
            name: Definition name
            description: Optional description
            is_global: Whether the definition is available to all sites
            on_fail_goto_cleanup: Jump to cleanup steps on failure
            on_fail_require_submit: Force submission on failure
            on_fail_require_repair: Repair requirement flag on failure
            add_child_units: Whether child units can be added
            **extra_fields: Additional fields to include in the payload

        Returns:
            Created TestSequenceDefinition or None
        """
        payload: Dict[str, Any] = {
            "Name": name,
            "IsGlobal": is_global,
            "OnFailGotoCleanup": on_fail_goto_cleanup,
            "OnFailRequireSubmit": on_fail_require_submit,
            "OnFailRequireRepair": on_fail_require_repair,
            "AddChildUnits": add_child_units,
        }
        if description is not None:
            payload["Description"] = description
        payload.update(extra_fields)
        logger.info("Creating MI definition: %s", name)
        return await self._repository.post_definition(payload)

    async def update_definition(
        self,
        definition_id: str,
        **fields: Any,
    ) -> Optional[TestSequenceDefinition]:
        """
        Update an existing test sequence definition.

        Args:
            definition_id: Definition GUID string
            **fields: Fields to update (PascalCase keys expected by server)

        Returns:
            Updated TestSequenceDefinition or None
        """
        payload: Dict[str, Any] = {"TestSequenceDefinitionId": definition_id}
        payload.update(fields)
        logger.info("Updating MI definition: %s", definition_id)
        return await self._repository.put_definition(payload)

    async def copy_definition(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Create a copy of an existing definition.

        Args:
            definition_id: Source definition GUID string

        Returns:
            Copied TestSequenceDefinition or None
        """
        return await self._repository.get_definition_copy(definition_id)

    async def get_instances_count(self, definition_id: str) -> int:
        """
        Get the count of execution instances for a definition.

        Args:
            definition_id: Definition GUID string

        Returns:
            Number of instances
        """
        return await self._repository.get_instances_count(definition_id)

    # =========================================================================
    # Relations
    # =========================================================================

    async def list_relations(
        self, definition_id: str
    ) -> List[TestSequenceRelation]:
        """
        List all relations for a test sequence definition.

        Args:
            definition_id: Definition GUID string

        Returns:
            List of TestSequenceRelation objects
        """
        return await self._repository.get_relations(definition_id)

    async def get_relation_conflicts(
        self, definition_id: str
    ) -> List[RelationConflict]:
        """
        Get relation conflicts for a definition (uses preferred newer endpoint).

        Args:
            definition_id: Definition GUID string

        Returns:
            List of RelationConflict objects
        """
        return await self._repository.get_relation_conflicts_new(definition_id)

    async def create_relation(
        self,
        definition_id: str,
        entity_schema: str,
        entity_name: str,
        entity_key: Optional[str] = None,
        entity_value: Optional[str] = None,
        **extra_fields: Any,
    ) -> Optional[TestSequenceRelation]:
        """
        Create a new relation linking a definition to an entity.

        Args:
            definition_id: Definition GUID string
            entity_schema: Schema type (e.g. "Product", "Process")
            entity_name: Entity name (e.g. part number)
            entity_key: Optional entity key
            entity_value: Optional entity value
            **extra_fields: Additional fields

        Returns:
            Created TestSequenceRelation or None
        """
        payload: Dict[str, Any] = {
            "TestSequenceDefinitionId": definition_id,
            "EntitySchema": entity_schema,
            "EntityName": entity_name,
        }
        if entity_key is not None:
            payload["EntityKey"] = entity_key
        if entity_value is not None:
            payload["EntityValue"] = entity_value
        payload.update(extra_fields)
        logger.info(
            "Creating MI relation: definition=%s, entity=%s/%s",
            definition_id, entity_schema, entity_name,
        )
        return await self._repository.post_relation(payload)

    async def update_relation(
        self, payload: Dict[str, Any]
    ) -> Optional[TestSequenceRelation]:
        """
        Update an existing relation.

        Args:
            payload: Updated relation data dict

        Returns:
            Updated TestSequenceRelation or None
        """
        return await self._repository.put_relation(payload)

    async def delete_relation(self, payload: Dict[str, Any]) -> Any:
        """
        Delete a relation.

        Note: The WATS API uses PUT (not DELETE) for this operation.

        Args:
            payload: Relation data identifying the relation to remove

        Returns:
            Server response data
        """
        return await self._repository.delete_relation(payload)

    # =========================================================================
    # Sequences
    # =========================================================================

    async def list_sequences(self) -> List[MiSequence]:
        """
        List all available MI sequences.

        Returns:
            List of MiSequence objects
        """
        return await self._repository.get_sequences()

    async def update_sequence(self, payload: Dict[str, Any]) -> Any:
        """
        Update a sequence.

        Args:
            payload: Sequence data dict

        Returns:
            Server response data
        """
        return await self._repository.put_sequence(payload)

    async def delete_sequence(self, sequence_id: str) -> Any:
        """
        Delete a sequence.

        Args:
            sequence_id: Sequence identifier

        Returns:
            Server response data
        """
        return await self._repository.delete_sequence(sequence_id)

    # =========================================================================
    # Unit Details
    # =========================================================================

    async def get_mi_details(
        self, unit_id: str
    ) -> Optional[TestSequenceInstance]:
        """
        Get MI details for a unit (uses preferred newer endpoint).

        Args:
            unit_id: Unit/instance identifier

        Returns:
            TestSequenceInstance or None
        """
        return await self._repository.get_mi_details_new(unit_id)

    # =========================================================================
    # XAML / WWF Content
    # =========================================================================

    async def get_xaml(self, definition_id: str) -> Any:
        """
        Get the XAML content for a test sequence definition.

        Args:
            definition_id: Definition GUID string

        Returns:
            XAML data from server (structure TBD — use inspect_sequences to discover)
        """
        return await self._repository.get_xaml(definition_id)

    async def put_xaml(self, payload: Dict[str, Any]) -> Any:
        """
        Save XAML content for a test sequence definition.

        Args:
            payload: XAML data dict (must include definition ID and XAML content)

        Returns:
            Server response data
        """
        return await self._repository.put_xaml(payload)

    async def get_wwf_content(self, definition_id: str) -> Any:
        """
        Get the Windows Workflow Foundation content for a definition.

        Args:
            definition_id: Definition GUID string

        Returns:
            WWF content from server
        """
        return await self._repository.get_wwf_content(definition_id)

    # =========================================================================
    # Validation / Misc
    # =========================================================================

    async def validate_misc_info(self, payload: Dict[str, Any]) -> Any:
        """
        Validate misc info fields.

        Args:
            payload: Data to validate

        Returns:
            Validation result from server
        """
        return await self._repository.validate_misc_info(payload)

    async def put_string_test(self, payload: Dict[str, Any]) -> Any:
        """
        Update a string test entry.

        Args:
            payload: String test data

        Returns:
            Server response data
        """
        return await self._repository.put_string_test(payload)

    # =========================================================================
    # Lifecycle Convenience Methods
    # =========================================================================

    async def create_inspection(
        self,
        name: str,
        description: Optional[str] = None,
        is_global: bool = False,
        on_fail_goto_cleanup: bool = False,
        on_fail_require_submit: bool = False,
        on_fail_require_repair: int = 0,
        add_child_units: bool = False,
        **extra_fields: Any,
    ) -> Optional[TestSequenceDefinition]:
        """
        Create a new manual inspection definition.

        Alias for :meth:`create_definition` with naming consistent
        with the report domain's ``create_uut_report()``.

        Args:
            name: Inspection name
            description: Optional description
            is_global: Whether the inspection is available to all sites
            on_fail_goto_cleanup: Jump to cleanup steps on failure
            on_fail_require_submit: Force submission on failure
            on_fail_require_repair: Repair requirement flag on failure
                (0=Disabled, 1=Optional, 2=Required)
            add_child_units: Whether child units can be added
            **extra_fields: Additional fields to include in the payload

        Returns:
            Created TestSequenceDefinition or None

        Example:
            >>> inspection = await api.manual_inspection.create_inspection(
            ...     name="PCB Visual Check",
            ...     description="Solder joint and component inspection",
            ...     on_fail_require_repair=1,  # Optional repair
            ... )
        """
        return await self.create_definition(
            name=name,
            description=description,
            is_global=is_global,
            on_fail_goto_cleanup=on_fail_goto_cleanup,
            on_fail_require_submit=on_fail_require_submit,
            on_fail_require_repair=on_fail_require_repair,
            add_child_units=add_child_units,
            **extra_fields,
        )

    async def get_inspection(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Get a manual inspection definition by ID.

        Alias for :meth:`get_definition`.

        Args:
            definition_id: Definition GUID string

        Returns:
            TestSequenceDefinition or None if not found
        """
        return await self.get_definition(definition_id)

    async def release_inspection(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Release a manual inspection (move from Pending to Released).

        Releasing makes the inspection active in production. Once released,
        the definition is immutable. To make changes, copy the definition
        (which creates a new Draft version) and edit the copy.

        Note: Releasing automatically revokes any previous Released version
        with the same name.

        Args:
            definition_id: Definition GUID string

        Returns:
            Updated TestSequenceDefinition or None

        Example:
            >>> # Move to pending first, then release
            >>> await api.manual_inspection.move_to_pending(defn_id)
            >>> released = await api.manual_inspection.release_inspection(defn_id)
            >>> print(f"Released: {released.name} v{released.version}")
        """
        logger.info("Releasing MI inspection: %s", definition_id)
        return await self.update_definition(definition_id, Status=2)

    async def move_to_pending(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Move a manual inspection to Pending status for testing.

        In Pending status, operators can execute the inspection for
        validation, but no edits are allowed. Can return to Draft
        or advance to Released.

        Args:
            definition_id: Definition GUID string

        Returns:
            Updated TestSequenceDefinition or None

        Example:
            >>> pending = await api.manual_inspection.move_to_pending(defn_id)
            >>> # Operators can now test the inspection
        """
        logger.info("Moving MI inspection to Pending: %s", definition_id)
        return await self.update_definition(definition_id, Status=1)

    async def move_to_draft(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Move a manual inspection back to Draft status for editing.

        Only inspections in Pending status can be moved back to Draft.
        Released inspections cannot be modified — copy them instead.

        Args:
            definition_id: Definition GUID string

        Returns:
            Updated TestSequenceDefinition or None

        Example:
            >>> # Found an issue during testing, move back to edit
            >>> draft = await api.manual_inspection.move_to_draft(defn_id)
            >>> await api.manual_inspection.update_definition(
            ...     defn_id, Description="Fixed step order"
            ... )
        """
        logger.info("Moving MI inspection to Draft: %s", definition_id)
        return await self.update_definition(definition_id, Status=0)

    async def revoke_inspection(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Revoke a released manual inspection.

        Revoking removes the inspection from active use. Typically
        this happens automatically when a newer version is released,
        but can also be done manually to retire an inspection.

        Args:
            definition_id: Definition GUID string

        Returns:
            Updated TestSequenceDefinition or None

        Example:
            >>> # Retire an old inspection
            >>> revoked = await api.manual_inspection.revoke_inspection(defn_id)
            >>> print(f"Revoked: {revoked.name}")
        """
        logger.info("Revoking MI inspection: %s", definition_id)
        return await self.update_definition(definition_id, Status=3)

    async def copy_inspection(
        self, definition_id: str
    ) -> Optional[TestSequenceDefinition]:
        """
        Create a copy of an existing inspection.

        The copy is created as a new Draft version with an incremented
        version number. Use this to modify a Released inspection.

        Alias for :meth:`copy_definition`.

        Args:
            definition_id: Source definition GUID string

        Returns:
            Copied TestSequenceDefinition (Draft status) or None

        Example:
            >>> # Modify a released inspection
            >>> copy = await api.manual_inspection.copy_inspection(released_id)
            >>> await api.manual_inspection.update_definition(
            ...     str(copy.test_sequence_definition_id),
            ...     Description="Added thermal check",
            ... )
        """
        return await self.copy_definition(definition_id)
