"""Manual Inspection domain models.

Models for test sequence definitions, relations, sequences, instances,
and inspection detail results.

Based on C# reference models:
- TestSequenceDefinition
- TestSequenceRelation
- TestSequenceInstance
- TestSequenceDefinitionXaml
- TestSequenceDefinitionMedia
"""
from enum import IntEnum
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import Field

from ...shared.base_model import PyWATSModel


class DefinitionStatus(IntEnum):
    """Test sequence definition lifecycle status.

    Lifecycle::

        Draft (0) <--> Pending (1) --> Released (2)
                                           |
                               [auto-revokes old version]
                                           |
                                    Revoked (3)

    - **DRAFT**: Editable. Can move to Pending.
    - **PENDING**: Test mode. Can return to Draft or advance to Released.
    - **RELEASED**: Immutable. Cannot return to Pending or Draft.
      Releasing a new version automatically revokes the previous Released
      version with the same name.
    - **REVOKED**: Superseded by a newer Released version.

    Versioning: duplicating or creating a definition with an existing name
    increments the ``version`` number. The new version starts as Draft.
    """
    DRAFT = 0
    PENDING = 1
    RELEASED = 2
    REVOKED = 3


class RepairOnFailed(IntEnum):
    """Repair requirement when a test step fails.

    Controls whether the operator must initiate a repair workflow
    after a failed step.
    """
    DISABLED = 0
    OPTIONAL = 1
    REQUIRED = 2


class TestSequenceDefinition(PyWATSModel):
    """
    Manual Inspection test sequence definition.

    Represents an MI definition that defines a set of inspection steps.
    Maps to C# ``TestSequenceDefinition`` entity.

    Versioning:
        Definitions are versioned by name. Duplicating or creating a
        definition with an existing name increments the ``version`` number.
        The new version starts as Draft. Releasing it automatically revokes
        the previous Released version with the same name. See
        :class:`DefinitionStatus` for the full lifecycle.

    Attributes:
        test_sequence_definition_id: Unique definition identifier (GUID)
        virtual_folder_id: Folder for organising definitions
        name: Human-readable definition name
        version: Definition version number
        description: Optional description text
        created: Creation timestamp
        created_by: Username who created the definition
        created_by_site: Site code of the creator (e.g. "00")
        modified: Last modification timestamp
        modified_by: Username who last modified
        released: Release timestamp (None if not released)
        released_by: Username who released (None if not released)
        revoked: Revocation timestamp (None if not revoked)
        revoked_by: Username who revoked (None if not revoked)
        status: Lifecycle status (see :class:`DefinitionStatus`)
        is_global: Whether definition can be referenced by other sequences
        on_fail_goto_cleanup: Jump to cleanup steps on failure
        on_fail_require_submit: Force submission on failure
        on_fail_require_repair: Repair requirement flag on failure
        log_operator: Whether to log operator identity
        log_description: Whether to log step descriptions in report
        create_unsubmitted_report_on_failed_step: Auto-create report on failure
        repair_process_id: Optional linked repair process GUID
        add_child_units: Whether child units can be added during inspection
        include_uur_misc_info_in_uut: Copy UUR misc info into UUT report
        load_previous_misc_info: Pre-populate misc info from previous run
        relations: Inline relations list (populated on some responses)
        instances_count: Number of active instances for this definition
        xaml: Inline XAML content (populated on some responses)
    """
    test_sequence_definition_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceDefinitionId",
        serialization_alias="TestSequenceDefinitionId",
    )
    virtual_folder_id: Optional[UUID] = Field(
        default=None,
        validation_alias="VirtualFolderId",
        serialization_alias="VirtualFolderId",
    )
    name: Optional[str] = Field(
        default=None,
        validation_alias="Name",
        serialization_alias="Name",
    )
    version: Optional[int] = Field(
        default=None,
        validation_alias="Version",
        serialization_alias="Version",
    )
    description: Optional[str] = Field(
        default=None,
        validation_alias="Description",
        serialization_alias="Description",
    )
    created: Optional[datetime] = Field(
        default=None,
        validation_alias="Created",
        serialization_alias="Created",
    )
    created_by: Optional[str] = Field(
        default=None,
        validation_alias="CreatedBy",
        serialization_alias="CreatedBy",
    )
    created_by_site: Optional[str] = Field(
        default=None,
        validation_alias="CreatedBySite",
        serialization_alias="CreatedBySite",
    )
    modified: Optional[datetime] = Field(
        default=None,
        validation_alias="Modified",
        serialization_alias="Modified",
    )
    modified_by: Optional[str] = Field(
        default=None,
        validation_alias="ModifiedBy",
        serialization_alias="ModifiedBy",
    )
    released: Optional[datetime] = Field(
        default=None,
        validation_alias="Released",
        serialization_alias="Released",
    )
    released_by: Optional[str] = Field(
        default=None,
        validation_alias="ReleasedBy",
        serialization_alias="ReleasedBy",
    )
    revoked: Optional[datetime] = Field(
        default=None,
        validation_alias="Revoked",
        serialization_alias="Revoked",
    )
    revoked_by: Optional[str] = Field(
        default=None,
        validation_alias="RevokedBy",
        serialization_alias="RevokedBy",
    )
    status: Optional[int] = Field(
        default=None,
        validation_alias="Status",
        serialization_alias="Status",
    )
    is_global: bool = Field(
        default=False,
        validation_alias="IsGlobal",
        serialization_alias="IsGlobal",
    )
    on_fail_goto_cleanup: bool = Field(
        default=False,
        validation_alias="OnFailGotoCleanup",
        serialization_alias="OnFailGotoCleanup",
    )
    on_fail_require_submit: bool = Field(
        default=False,
        validation_alias="OnFailRequireSubmit",
        serialization_alias="OnFailRequireSubmit",
    )
    on_fail_require_repair: int = Field(
        default=0,
        validation_alias="OnFailRequireRepair",
        serialization_alias="OnFailRequireRepair",
    )
    log_operator: bool = Field(
        default=True,
        validation_alias="LogOperator",
        serialization_alias="LogOperator",
    )
    log_description: bool = Field(
        default=False,
        validation_alias="LogDescription",
        serialization_alias="LogDescription",
    )
    create_unsubmitted_report_on_failed_step: bool = Field(
        default=False,
        validation_alias="CreateUnsubmittedReportOnFailedStep",
        serialization_alias="CreateUnsubmittedReportOnFailedStep",
    )
    repair_process_id: Optional[UUID] = Field(
        default=None,
        validation_alias="RepairProcessId",
        serialization_alias="RepairProcessId",
    )
    add_child_units: bool = Field(
        default=False,
        validation_alias="AddChildUnits",
        serialization_alias="AddChildUnits",
    )
    include_uur_misc_info_in_uut: bool = Field(
        default=False,
        validation_alias="IncludeUURMiscInfoInUUT",
        serialization_alias="IncludeUURMiscInfoInUUT",
    )
    load_previous_misc_info: bool = Field(
        default=False,
        validation_alias="LoadPreviousMiscInfo",
        serialization_alias="LoadPreviousMiscInfo",
    )
    relations: Optional[List["TestSequenceRelation"]] = Field(
        default=None,
        validation_alias="Relations",
        serialization_alias="Relations",
    )
    instances_count: int = Field(
        default=0,
        validation_alias="InstancesCount",
        serialization_alias="InstancesCount",
    )
    xaml: Optional[str] = Field(
        default=None,
        validation_alias="XAML",
        serialization_alias="XAML",
    )

    model_config = {"populate_by_name": True}


class TestSequenceProcessRelation(PyWATSModel):
    """Link between a relation and a test process (test operation).

    Determines which test operations (e.g. "Manual Inspection",
    "Functional Test") the relation applies to.
    """
    test_sequence_process_relation_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceProcessRelationId",
        serialization_alias="TestSequenceProcessRelationId",
    )
    test_sequence_relation_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceRelationId",
        serialization_alias="TestSequenceRelationId",
    )
    process_id: Optional[UUID] = Field(
        default=None,
        validation_alias="ProcessId",
        serialization_alias="ProcessId",
    )

    model_config = {"populate_by_name": True}


class TestSequenceSiteRelation(PyWATSModel):
    """Link between a relation and a site restriction."""
    test_sequence_site_relation_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceSiteRelationId",
        serialization_alias="TestSequenceSiteRelationId",
    )
    test_sequence_relation_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceRelationId",
        serialization_alias="TestSequenceRelationId",
    )
    site_id: Optional[UUID] = Field(
        default=None,
        validation_alias="SiteId",
        serialization_alias="SiteId",
    )

    model_config = {"populate_by_name": True}


class TestSequenceRelation(PyWATSModel):
    """
    Relation linking a test sequence definition to a product/process entity.

    Maps to C# ``TestSequenceRelation`` entity.
    Relations use wildcard matching on ``entity_value`` (e.g. ``%`` for all
    part numbers, ``ABC123%`` for prefix match).

    Attributes:
        test_sequence_relation_id: Unique relation identifier (GUID)
        test_sequence_definition_id: Parent definition GUID
        entity_schema: Schema type (e.g. "product")
        entity_name: Entity name (e.g. "product")
        entity_key: Entity key field (e.g. "partnumber")
        entity_value: Wildcard value (e.g. "%" or "ABC123%")
        status: Active status (1 = active)
        product_name: Resolved product name (may be None)
        process_relations: Test operations this relation applies to
        site_relations: Site restrictions for this relation
    """
    test_sequence_relation_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceRelationId",
        serialization_alias="TestSequenceRelationId",
    )
    test_sequence_definition_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceDefinitionId",
        serialization_alias="TestSequenceDefinitionId",
    )
    entity_schema: Optional[str] = Field(
        default=None,
        validation_alias="EntitySchema",
        serialization_alias="EntitySchema",
    )
    entity_name: Optional[str] = Field(
        default=None,
        validation_alias="EntityName",
        serialization_alias="EntityName",
    )
    entity_key: Optional[str] = Field(
        default=None,
        validation_alias="EntityKey",
        serialization_alias="EntityKey",
    )
    entity_value: Optional[str] = Field(
        default=None,
        validation_alias="EntityValue",
        serialization_alias="EntityValue",
    )
    status: Optional[int] = Field(
        default=None,
        validation_alias="Status",
        serialization_alias="Status",
    )
    product_name: Optional[str] = Field(
        default=None,
        validation_alias="ProductName",
        serialization_alias="ProductName",
    )
    process_relations: Optional[List["TestSequenceProcessRelation"]] = Field(
        default=None,
        validation_alias="TestSequenceProcessRelations",
        serialization_alias="TestSequenceProcessRelations",
    )
    site_relations: Optional[List["TestSequenceSiteRelation"]] = Field(
        default=None,
        validation_alias="TestSequenceSiteRelations",
        serialization_alias="TestSequenceSiteRelations",
    )

    model_config = {"populate_by_name": True}


class TestSequenceInstance(PyWATSModel):
    """
    An execution instance of a test sequence for a specific unit.

    Maps to C# ``TestSequenceInstance`` entity.

    Attributes:
        test_sequence_instance_id: Unique instance identifier (GUID)
        test_sequence_definition_id: Parent definition GUID
        unit_id: Unit GUID being inspected (None if not yet linked)
        serial_number: Serial number of the unit
        part_number: Part number of the unit
        revision: Product revision
        created: Instance creation timestamp
        last_event_time: Timestamp of the last event on this instance
    """
    test_sequence_instance_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceInstanceId",
        serialization_alias="TestSequenceInstanceId",
    )
    test_sequence_definition_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceDefinitionId",
        serialization_alias="TestSequenceDefinitionId",
    )
    unit_id: Optional[UUID] = Field(
        default=None,
        validation_alias="UnitId",
        serialization_alias="UnitId",
    )
    serial_number: Optional[str] = Field(
        default=None,
        validation_alias="SerialNumber",
        serialization_alias="SerialNumber",
    )
    part_number: Optional[str] = Field(
        default=None,
        validation_alias="PartNumber",
        serialization_alias="PartNumber",
    )
    revision: Optional[str] = Field(
        default=None,
        validation_alias="Revision",
        serialization_alias="Revision",
    )
    created: Optional[datetime] = Field(
        default=None,
        validation_alias="Created",
        serialization_alias="Created",
    )
    last_event_time: Optional[datetime] = Field(
        default=None,
        validation_alias="LastEventTime",
        serialization_alias="LastEventTime",
    )

    model_config = {"populate_by_name": True}


class RelationConflict(PyWATSModel):
    """
    Conflict information when a relation overlaps with another definition.

    Returned by ``GetRelationConflicts`` / ``GetRelationConflictsNew``.
    """
    test_sequence_definition_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceDefinitionId",
        serialization_alias="TestSequenceDefinitionId",
    )
    test_sequence_relation_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceRelationId",
        serialization_alias="TestSequenceRelationId",
    )
    name: Optional[str] = Field(
        default=None,
        validation_alias="Name",
        serialization_alias="Name",
    )
    entity_name: Optional[str] = Field(
        default=None,
        validation_alias="EntityName",
        serialization_alias="EntityName",
    )
    entity_value: Optional[str] = Field(
        default=None,
        validation_alias="EntityValue",
        serialization_alias="EntityValue",
    )
    status: Optional[int] = Field(
        default=None,
        validation_alias="Status",
        serialization_alias="Status",
    )

    model_config = {"populate_by_name": True}


class MiSequence(PyWATSModel):
    """
    Inspection sequence entry returned by ``GetSequences``.

    A sequence represents an ordered list of inspection steps
    as defined by the XAML content inside a definition.
    """
    test_sequence_definition_id: Optional[UUID] = Field(
        default=None,
        validation_alias="TestSequenceDefinitionId",
        serialization_alias="TestSequenceDefinitionId",
    )
    name: Optional[str] = Field(
        default=None,
        validation_alias="Name",
        serialization_alias="Name",
    )
    version: Optional[int] = Field(
        default=None,
        validation_alias="Version",
        serialization_alias="Version",
    )
    status: Optional[int] = Field(
        default=None,
        validation_alias="Status",
        serialization_alias="Status",
    )

    model_config = {"populate_by_name": True}
