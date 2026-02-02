RootCause Domain
================

The RootCause domain provides a comprehensive ticketing system for manufacturing issue tracking and resolution in WATS. It enables you to:

- Create and manage tickets for test failures and defects
- Track issue lifecycle with status workflows (Open, In Progress, Solved, etc.)
- Assign tickets to team members and track ownership
- Add comments and collaborate on issue resolution
- Attach files and supporting documentation
- Link tickets to specific test reports for traceability
- Archive solved tickets for record-keeping

**Use Cases:**
- Manufacturing defect tracking and management
- Test failure investigation and root cause analysis
- Collaborative problem-solving workflows
- Quality issue escalation and resolution
- Production line issue tracking
- Corrective action management
- Audit trail for quality issues

**Domain Health:** A- (52/60) - Very Good, production-ready

---

Quick Start
-----------

Creating a Simple Ticket
^^^^^^^^^^^^^^^^^^^^^^^^

Create a ticket to track a manufacturing issue:

.. code-block:: python

   from pywats import pyWATS
   from pywats.domains.rootcause import TicketPriority
   
   api = pyWATS(base_url="https://wats.example.com", token="token")
   
   # Create a ticket for a test failure
   ticket = api.rootcause.create_ticket(
       subject="5V Rail Test Failing - Line 2",
       priority=TicketPriority.HIGH,
       assignee="john.smith@company.com",
       team="Quality Engineering",
       initial_comment="Multiple units failing voltage check at 5V rail since 8am"
   )
   
   print(f"Created ticket #{ticket.ticket_number}")
   print(f"Ticket ID: {ticket.ticket_id}")
   print(f"Status: {ticket.status.name}")

Retrieving and Updating Tickets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get tickets assigned to you and update their status:

.. code-block:: python

   from pywats.domains.rootcause import TicketStatus, TicketView
   
   # Get all active tickets assigned to you
   active_tickets = api.rootcause.get_active_tickets(
       view=TicketView.ASSIGNED
   )
   
   print(f"You have {len(active_tickets)} active tickets")
   for ticket in active_tickets:
       print(f"  #{ticket.ticket_number}: {ticket.subject}")
   
   # Add a comment with progress update
   api.rootcause.add_comment(
       ticket_id,
       "Found issue - probe #3 on fixture needs replacement",
       assignee="john.smith@company.com"
   )
   
   # Change status to solved
   api.rootcause.change_status(
       ticket_id,
       TicketStatus.SOLVED,
       assignee="john.smith@company.com"
   )

---

Core Concepts
-------------

Type-Safe Enums
^^^^^^^^^^^^^^^

The RootCause domain provides type-safe enums for IDE autocomplete and validation:

.. code-block:: python

   from pywats.domains.rootcause import (
       TicketStatus,
       TicketPriority,
       TicketView
   )
   
   # Ticket status - can be combined with bitwise OR (|)
   TicketStatus.OPEN         # 1   - New/unassigned tickets
   TicketStatus.IN_PROGRESS  # 2   - Active investigation
   TicketStatus.ON_HOLD      # 4   - Temporarily paused
   TicketStatus.SOLVED       # 8   - Issue resolved
   TicketStatus.CLOSED       # 16  - Verified and closed
   TicketStatus.ARCHIVED     # 32  - Archived for records
   
   # Priority levels
   TicketPriority.LOW        # 0 - Low priority
   TicketPriority.MEDIUM     # 1 - Medium priority
   TicketPriority.HIGH       # 2 - High priority / urgent
   
   # View filters
   TicketView.ASSIGNED       # 0 - Tickets assigned to you
   TicketView.FOLLOWING      # 1 - Tickets you're following
   TicketView.ALL            # 2 - All tickets

Ticket Model
^^^^^^^^^^^^

The ``Ticket`` model represents a complete ticket with all metadata:

.. code-block:: python

   from pywats.domains.rootcause import Ticket
   
   # Ticket attributes
   ticket.ticket_id        # UUID - Unique identifier
   ticket.ticket_number    # int - Human-readable number
   ticket.subject          # str - Ticket subject/title
   ticket.status           # TicketStatus - Current status
   ticket.priority         # TicketPriority - Priority level
   ticket.assignee         # str - Assigned user
   ticket.team             # str - Assigned team
   ticket.report_uuid      # UUID - Linked test report
   ticket.created_utc      # datetime - Creation timestamp

---

API Reference
-------------

Main Service
^^^^^^^^^^^^

.. autoclass:: pywats.domains.rootcause.async_service.AsyncRootCauseService
   :members:
   :undoc-members:
   :show-inheritance:
   :member-order: bysource

Repository Layer
^^^^^^^^^^^^^^^^

.. note::
   Repository APIs are for advanced use cases. Most users should use the service layer above.

.. autoclass:: pywats.domains.rootcause.async_repository.AsyncRootCauseRepository
   :members:
   :undoc-members:
   :show-inheritance:

Models
------

Ticket
^^^^^^

.. autoclass:: pywats.domains.rootcause.models.Ticket
   :members:
   :undoc-members:
   :show-inheritance:

TicketUpdate
^^^^^^^^^^^^

.. autoclass:: pywats.domains.rootcause.models.TicketUpdate
   :members:
   :undoc-members:
   :show-inheritance:

TicketAttachment
^^^^^^^^^^^^^^^^

.. autoclass:: pywats.domains.rootcause.models.TicketAttachment
   :members:
   :undoc-members:
   :show-inheritance:

Enums
-----

.. automodule:: pywats.domains.rootcause.enums
   :members:
   :undoc-members:
   :show-inheritance:

---

Best Practices
--------------

1. **Always Preserve Assignee When Updating**
   Due to server limitations, always pass the ``assignee`` parameter explicitly to avoid validation errors.

2. **Use Type-Safe Enums**
   Always use ``TicketStatus``, ``TicketPriority``, and ``TicketView`` enums for better IDE support.

3. **Leverage Async for Batch Operations**
   When processing multiple tickets, use ``AsyncWATS`` and ``asyncio.gather()`` for performance.

4. **Link Tickets to Reports for Traceability**
   Always link tickets to relevant test reports using ``report_uuid`` parameter.

5. **Document Resolution Steps**
   Add detailed comments documenting investigation steps and corrective actions.

---

Related Documentation
---------------------

- :doc:`../usage/rootcause-domain` - Detailed usage guide
- :doc:`../domains/report` - Report domain
- :doc:`../domains/analytics` - Analytics domain
- :doc:`../getting-started` - Installation and setup

---

Domain Health
-------------

**Score:** 52/60 (A-) - Very Good, production-ready

**Strengths:**
- Perfect Service→Repository→HttpClient architecture
- 100% ErrorHandler coverage
- Type-safe enums for better developer experience
- Comprehensive ticket lifecycle management
- Strong test coverage (~84%)
