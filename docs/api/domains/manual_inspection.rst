Manual Inspection Domain
========================

The Manual Inspection (MI) domain manages structured operator-driven inspection
sequences in WATS. Unlike automated test programs, MI sequences guide human
operators through visual checks, measurements, pass/fail decisions, and data
entry steps during manufacturing.

**Use Cases:**

- Define reusable inspection sequences (visual, dimensional, functional)
- Link definitions to products and processes via relations
- Track definition lifecycle (Draft → Pending → Released → Revoked)
- Query execution instances for traceability
- List available sequences for the operator interface

**Domain Health:** A (54/60) - Very Good, production-ready

---

Quick Start
-----------

List Definitions
^^^^^^^^^^^^^^^^

Retrieve all MI definitions configured in your WATS instance:

.. code-block:: python

   from pywats import pyWATS

   api = pyWATS(base_url="https://wats.example.com", token="...")

   definitions = api.manual_inspection.list_definitions()

   for defn in definitions:
       print(f"{defn.name} (v{defn.version}) - Status: {defn.status}")

Create an Inspection
^^^^^^^^^^^^^^^^^^^^

Create a new inspection sequence with fail-handling options:

.. code-block:: python

   # Using create_inspection (recommended)
   inspection = api.manual_inspection.create_inspection(
       name="PCB Visual Inspection",
       description="Solder joint and component placement inspection",
       on_fail_goto_cleanup=True,
       on_fail_require_submit=True,
       on_fail_require_repair=1,  # 0=Disabled, 1=Optional, 2=Required
   )

   print(f"Created: {inspection.name} ({inspection.test_sequence_definition_id})")

   # Alternatively, use create_definition (same functionality)
   defn = api.manual_inspection.create_definition(name="Alt Inspection", ...)

Link to a Product
^^^^^^^^^^^^^^^^^

Create a relation so the inspection appears for a specific product:

.. code-block:: python

   relation = api.manual_inspection.create_relation(
       definition_id=str(inspection.test_sequence_definition_id),
       entity_schema="product",
       entity_name="product",
       entity_key="partnumber",
       entity_value="CTRL-1000",  # Use "%" for wildcard
   )

   print(f"Linked to {relation.entity_value}")

Release for Production
^^^^^^^^^^^^^^^^^^^^^^

Move through the lifecycle to release for operator use:

.. code-block:: python

   defn_id = str(inspection.test_sequence_definition_id)

   # Move to Pending for testing
   api.manual_inspection.move_to_pending(defn_id)

   # Release for production
   released = api.manual_inspection.release_inspection(defn_id)
   print(f"Released: {released.name} v{released.version}")

---

Lifecycle Convenience Methods
-----------------------------

The MI domain provides convenience methods for managing the inspection lifecycle.
These methods wrap ``update_definition()`` with clearer semantics:

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - Method
     - Description
   * - ``create_inspection(...)``
     - Create a new MI definition (alias for ``create_definition``)
   * - ``get_inspection(id)``
     - Get an inspection by ID (alias for ``get_definition``)
   * - ``copy_inspection(id)``
     - Copy an inspection to create a new Draft version
   * - ``move_to_pending(id)``
     - Move from Draft to Pending (enables operator testing)
   * - ``move_to_draft(id)``
     - Move from Pending back to Draft (for edits)
   * - ``release_inspection(id)``
     - Release for production (Pending → Released)
   * - ``revoke_inspection(id)``
     - Manually revoke a released inspection

.. code-block:: python

   # Complete lifecycle example
   inspection = api.manual_inspection.create_inspection(
       name="Final Assembly Check",
       description="Pre-shipment verification",
   )
   defn_id = str(inspection.test_sequence_definition_id)

   # Add relations...
   api.manual_inspection.create_relation(
       definition_id=defn_id,
       entity_schema="product",
       entity_name="product",
       entity_key="partnumber",
       entity_value="ASSY-%",
   )

   # Lifecycle transitions
   api.manual_inspection.move_to_pending(defn_id)   # Draft → Pending
   api.manual_inspection.move_to_draft(defn_id)     # Pending → Draft (if issues)
   api.manual_inspection.move_to_pending(defn_id)   # Draft → Pending
   api.manual_inspection.release_inspection(defn_id) # Pending → Released

   # Later: modify by copying
   new_ver = api.manual_inspection.copy_inspection(defn_id)
   # Edit new_ver, then release (auto-revokes old version)

---

Core Concepts
-------------

Definition Lifecycle
^^^^^^^^^^^^^^^^^^^^

Every MI definition follows a strict lifecycle controlled by
:class:`~pywats.domains.manual_inspection.models.DefinitionStatus`:

.. code-block:: text

   Draft (0) <──> Pending (1) ──> Released (2)
                                       │
                           [auto-revokes previous version]
                                       │
                                Revoked (3)

- **Draft** — Editable. The sequence XAML, properties, and relations can be
  modified. Can advance to Pending or return from Pending.
- **Pending** — Test/review mode. Operators can execute the sequence for
  validation, but no edits are allowed. Can return to Draft or advance to
  Released.
- **Released** — Immutable. Active in production. To make changes, copy the
  definition (auto-incremented version) and edit the new Draft.
- **Revoked** — Automatically set on the previous Released version when a
  newer version of the same definition is Released.

.. code-block:: python

   from pywats.domains.manual_inspection import DefinitionStatus

   defn = api.manual_inspection.get_definition(defn_id)

   if defn.status == DefinitionStatus.DRAFT:
       # Safe to update
       api.manual_inspection.update_definition(
           defn_id, Description="Updated description"
       )
   elif defn.status == DefinitionStatus.RELEASED:
       # Must copy first — released definitions are immutable
       new_defn = api.manual_inspection.copy_definition(defn_id)
       api.manual_inspection.update_definition(
           str(new_defn.test_sequence_definition_id),
           Description="Updated in new version",
       )

Relations
^^^^^^^^^

Relations link MI definitions to manufacturing entities (products, processes)
so the correct inspection appears when an operator scans a unit.

A relation specifies:

- **entity_schema** — Entity type (e.g. ``"product"``)
- **entity_name** — Entity category (e.g. ``"product"``)
- **entity_key** — Matching field (e.g. ``"partnumber"``)
- **entity_value** — Value or wildcard pattern (``"CTRL-1000"`` or ``"%"``)

Wildcard matching uses SQL LIKE syntax: ``%`` matches any string,
``_`` matches a single character.

.. code-block:: python

   # Match all part numbers starting with "CTRL-"
   api.manual_inspection.create_relation(
       definition_id=defn_id,
       entity_schema="product",
       entity_name="product",
       entity_key="partnumber",
       entity_value="CTRL-%",
   )

   # Check for conflicts with other definitions
   conflicts = api.manual_inspection.get_relation_conflicts(defn_id)
   for c in conflicts:
       print(f"Conflict: {c.name} on {c.entity_value}")

Instances
^^^^^^^^^

An instance tracks a single execution of an inspection against a specific unit.
Instances are created automatically when an operator starts an inspection and
record the unit identity and timestamps.

.. code-block:: python

   # Get instance count for a definition
   count = api.manual_inspection.get_instances_count(defn_id)
   print(f"Executed {count} times")

   # Get MI details for a specific unit
   instance = api.manual_inspection.get_mi_details(unit_id)
   if instance:
       print(f"SN: {instance.serial_number}, PN: {instance.part_number}")

---

Common Use Cases
----------------

Browse and Filter Definitions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from pywats.domains.manual_inspection import DefinitionStatus

   # List all definitions
   all_defs = api.manual_inspection.list_definitions()

   # Filter to released only
   released = [d for d in all_defs if d.status == DefinitionStatus.RELEASED]
   print(f"{len(released)} released definitions")

   # Filter global definitions
   global_defs = api.manual_inspection.list_definitions(is_global=True)

Copy and Revise a Released Definition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Since released definitions are immutable, the copy-and-edit pattern is standard:

.. code-block:: python

   # Copy creates a new Draft version with incremented version number
   new_version = api.manual_inspection.copy_inspection(released_defn_id)

   print(f"New version: v{new_version.version} (Draft)")

   # Edit the new draft
   api.manual_inspection.update_definition(
       str(new_version.test_sequence_definition_id),
       Description="Added thermal check step",
   )

Full Lifecycle Workflow
^^^^^^^^^^^^^^^^^^^^^^^

Use the convenience methods for a complete lifecycle:

.. code-block:: python

   # 1. Create a new inspection (starts as Draft)
   inspection = api.manual_inspection.create_inspection(
       name="Board Visual Check",
       description="Solder joint and component inspection",
       on_fail_require_repair=1,  # Optional repair
   )
   defn_id = str(inspection.test_sequence_definition_id)

   # 2. Add product relations
   api.manual_inspection.create_relation(
       definition_id=defn_id,
       entity_schema="product",
       entity_name="product",
       entity_key="partnumber",
       entity_value="PCBA-%",
   )

   # 3. Move to Pending for operator testing
   api.manual_inspection.move_to_pending(defn_id)

   # 4. If testing reveals issues, move back to Draft
   api.manual_inspection.move_to_draft(defn_id)
   api.manual_inspection.update_definition(defn_id, Description="Fixed step order")
   api.manual_inspection.move_to_pending(defn_id)

   # 5. Release for production
   released = api.manual_inspection.release_inspection(defn_id)
   print(f"Released: {released.name} v{released.version}")

   # 6. To modify later, copy and release new version
   new_version = api.manual_inspection.copy_inspection(defn_id)
   # ... modify new_version ...
   api.manual_inspection.release_inspection(str(new_version.test_sequence_definition_id))
   # Old version is automatically revoked

Manage Relations with Conflict Detection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   # Add relation
   api.manual_inspection.create_relation(
       definition_id=defn_id,
       entity_schema="product",
       entity_name="product",
       entity_key="partnumber",
       entity_value="PCB-MAIN-%",
   )

   # Check for conflicts — overlap with other definitions
   conflicts = api.manual_inspection.get_relation_conflicts(defn_id)
   if conflicts:
       for c in conflicts:
           print(f"⚠ Overlaps with '{c.name}' on '{c.entity_value}'")
   else:
       print("No conflicts — safe to release")

   # List all relations
   relations = api.manual_inspection.list_relations(defn_id)
   for rel in relations:
       print(f"  {rel.entity_schema}/{rel.entity_key} = {rel.entity_value}")

List Operator Sequences
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   sequences = api.manual_inspection.list_sequences()
   for seq in sequences:
       print(f"{seq.name} v{seq.version} (status={seq.status})")

---

Fail-Handling Options
---------------------

MI definitions support configurable behaviour when an operator fails a step:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Property
     - Description
   * - ``on_fail_goto_cleanup``
     - Jump to cleanup steps on failure (skip remaining test steps)
   * - ``on_fail_require_submit``
     - Force the operator to submit the report even if failed
   * - ``on_fail_require_repair``
     - Repair requirement: ``0`` = Disabled, ``1`` = Optional, ``2`` = Required

.. code-block:: python

   from pywats.domains.manual_inspection import RepairOnFailed

   defn = api.manual_inspection.create_definition(
       name="Safety Critical Inspection",
       on_fail_goto_cleanup=True,
       on_fail_require_submit=True,
       on_fail_require_repair=RepairOnFailed.REQUIRED,
   )

---

API Reference
-------------

Service
^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.async_service.AsyncManualInspectionService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository
^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.async_repository.AsyncManualInspectionRepository
   :members:
   :undoc-members:
   :show-inheritance:

---

Models
------

TestSequenceDefinition
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.TestSequenceDefinition
   :members:
   :undoc-members:
   :show-inheritance:

TestSequenceRelation
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.TestSequenceRelation
   :members:
   :undoc-members:
   :show-inheritance:

TestSequenceProcessRelation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.TestSequenceProcessRelation
   :members:
   :undoc-members:
   :show-inheritance:

TestSequenceSiteRelation
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.TestSequenceSiteRelation
   :members:
   :undoc-members:
   :show-inheritance:

TestSequenceInstance
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.TestSequenceInstance
   :members:
   :undoc-members:
   :show-inheritance:

RelationConflict
^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.RelationConflict
   :members:
   :undoc-members:
   :show-inheritance:

MiSequence
^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.MiSequence
   :members:
   :undoc-members:
   :show-inheritance:

---

Enums
-----

DefinitionStatus
^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.DefinitionStatus
   :members:
   :undoc-members:
   :show-inheritance:

RepairOnFailed
^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.manual_inspection.models.RepairOnFailed
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Always check status before editing** — Only Draft definitions can be
   modified. Attempting to update a Released or Pending definition will fail.
   Use ``copy_definition()`` to create a new version.

2. **Use conflict detection** — Call ``get_relation_conflicts()`` before
   releasing to ensure your relations don't overlap with other definitions.

3. **Prefer specific wildcards** — Use ``"CTRL-1000%"`` over ``"%"`` to
   avoid accidentally matching unrelated products.

4. **Use the lifecycle enums** — Compare ``defn.status`` against
   ``DefinitionStatus.RELEASED`` rather than magic integers.

5. **Global vs. standard** — Mark a definition ``is_global=True`` only if
   it should be referenceable as a shared sub-sequence by other definitions.

---

Related Documentation
---------------------

- :doc:`report` — Submit UUT reports from completed inspections
- :doc:`product` — Product management (part numbers, BOMs)
- :doc:`process` — Test operations linked via relations
- :doc:`production` — Unit tracking and serial number management
