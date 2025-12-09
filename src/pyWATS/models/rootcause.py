"""
RootCause (Ticketing) models for pyWATS

Models for the RootCause ticketing system which enables collaboration
on issue tracking and resolution.

Uses Pydantic 2 for validation and serialization.
Uses validation_alias for JSON deserialization from API responses while
keeping Python-style snake_case field names for __init__ and attribute access.
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import IntEnum, IntFlag
from pydantic import Field, AliasChoices

from .common import PyWATSModel, Setting


class TicketStatus(IntFlag):
    """
    Ticket status flags.
    
    Can be combined for filtering (e.g., OPEN | IN_PROGRESS)
    """
    OPEN = 1
    IN_PROGRESS = 2
    ON_HOLD = 4
    SOLVED = 8
    CLOSED = 16
    ARCHIVED = 32


class TicketPriority(IntEnum):
    """Ticket priority levels"""
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class TicketView(IntEnum):
    """Ticket view filter for listing tickets"""
    ASSIGNED = 0       # Tickets assigned to current user
    FOLLOWING = 1      # Tickets current user is following
    ALL = 2           # All tickets (requires "Manage All Tickets" permission)


class TicketUpdateType(IntEnum):
    """Type of ticket update/history entry"""
    CONTENT = 0        # Ticket content (text)
    PROGRESS = 1       # Progress changed
    PROPERTIES = 2     # Ticket properties (assignee, status, etc.)
    NOTIFICATION = 3   # Notification info (reminder/mail)


class TicketAttachment(PyWATSModel):
    """
    Represents an attachment in a RootCause ticket.
    
    Attributes:
        attachment_id: Unique identifier for the attachment
        filename: Name of the attached file
    """
    attachment_id: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices("attachmentId", "attachment_id"),
        serialization_alias="attachmentId"
    )
    filename: Optional[str] = Field(default=None)


class TicketUpdate(PyWATSModel):
    """
    Represents an update/history entry in a RootCause ticket.
    
    Attributes:
        update_id: Unique identifier for the update
        update_utc: Timestamp of the update (UTC)
        update_user: User who made the update
        content: Content/comment of the update
        update_type: Type of update (content, progress, properties,
                     notification)
        attachments: List of attachments added in this update
    """
    update_id: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices("updateId", "update_id"),
        serialization_alias="updateId"
    )
    update_utc: Optional[datetime] = Field(
        default=None,
        validation_alias=AliasChoices("updateUtc", "update_utc"),
        serialization_alias="updateUtc"
    )
    update_user: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("updateUser", "update_user"),
        serialization_alias="updateUser"
    )
    content: Optional[str] = Field(default=None)
    update_type: Optional[TicketUpdateType] = Field(
        default=None,
        validation_alias=AliasChoices("updateType", "update_type"),
        serialization_alias="updateType"
    )
    attachments: Optional[List[TicketAttachment]] = Field(default=None)


class Ticket(PyWATSModel):
    """
    Represents a RootCause ticket in WATS.
    
    Used for tracking issues, collaborating on solutions, and managing
    the resolution workflow.
    
    Attributes:
        ticket_id: Unique identifier for the ticket
        ticket_number: Human-readable ticket number
        progress: Progress information/notes
        owner: Username of the ticket owner
        assignee: Username of the assigned user
        subject: Ticket subject/title
        status: Current status (Open, In Progress, etc.)
        priority: Priority level (Low, Medium, High)
        report_uuid: UUID of the associated report (if any)
        created_utc: Ticket creation timestamp (UTC)
        updated_utc: Last update timestamp (UTC)
        team: Team assigned to the ticket
        origin: Origin/source of the ticket
        tags: List of tags/metadata
        history: List of historical updates
        update: Current/pending update
    """
    ticket_id: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices("ticketId", "ticket_id"),
        serialization_alias="ticketId"
    )
    ticket_number: Optional[int] = Field(
        default=None,
        validation_alias=AliasChoices("ticketNumber", "ticket_number"),
        serialization_alias="ticketNumber"
    )
    progress: Optional[str] = Field(default=None)
    owner: Optional[str] = Field(default=None)
    assignee: Optional[str] = Field(default=None)
    subject: Optional[str] = Field(default=None)
    status: Optional[TicketStatus] = Field(default=None)
    priority: Optional[TicketPriority] = Field(default=None)
    report_uuid: Optional[UUID] = Field(
        default=None,
        validation_alias=AliasChoices("reportUuid", "report_uuid"),
        serialization_alias="reportUuid"
    )
    created_utc: Optional[datetime] = Field(
        default=None,
        validation_alias=AliasChoices("createdUtc", "created_utc"),
        serialization_alias="createdUtc"
    )
    updated_utc: Optional[datetime] = Field(
        default=None,
        validation_alias=AliasChoices("updatedUtc", "updated_utc"),
        serialization_alias="updatedUtc"
    )
    team: Optional[str] = Field(default=None)
    origin: Optional[str] = Field(default=None)
    tags: Optional[List[Setting]] = Field(default=None)
    history: Optional[List[TicketUpdate]] = Field(default=None)
    update: Optional[TicketUpdate] = Field(default=None)
