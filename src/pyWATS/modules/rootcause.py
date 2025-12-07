"""RootCause (Ticketing) Module for pyWATS

Provides high-level operations for managing RootCause tickets.
The RootCause module is essentially a ticketing system to collaborate and solve issues.
"""
from typing import List, Optional, Union
from uuid import UUID
from pathlib import Path

from ..models.rootcause import (
    Ticket, TicketStatus, TicketPriority, TicketView,
    TicketUpdate, TicketUpdateType, TicketAttachment
)
from ..rest_api import RootCauseApi


class RootCauseModule:
    """
    RootCause (Ticketing) management module.
    
    Provides operations for:
    - Creating and updating tickets
    - Querying tickets by status and view
    - Managing ticket attachments
    - Archiving solved tickets
    
    Usage:
        api = pyWATS("https://your-wats.com", "your-token")
        
        # Get all open tickets assigned to me
        tickets = api.rootcause.get_my_open_tickets()
        
        # Get a specific ticket
        ticket = api.rootcause.get_ticket("ticket-uuid")
        
        # Create a new ticket
        ticket = api.rootcause.create_ticket(
            subject="Test failure on Station A",
            priority=TicketPriority.HIGH,
            assignee="john.doe"
        )
        
        # Add a comment to a ticket
        api.rootcause.add_comment(ticket.ticket_id, "Found the root cause!")
        
        # Archive solved tickets
        api.rootcause.archive_tickets([ticket.ticket_id])
    """
    
    def __init__(self, api: RootCauseApi):
        """
        Initialize RootCauseModule with REST API client.
        
        Args:
            api: RootCauseApi instance for making HTTP requests
        """
        self._api = api
    
    # -------------------------------------------------------------------------
    # Get Operations
    # -------------------------------------------------------------------------
    
    def get_ticket(self, ticket_id: Union[str, UUID]) -> Optional[Ticket]:
        """
        Get a root cause ticket by ID.
        
        GET /api/RootCause/Ticket
        
        Args:
            ticket_id: The ticket ID (GUID)
            
        Returns:
            Ticket object if found, None otherwise
        """
        return self._api.get_ticket(ticket_id)
    
    def get_tickets(
        self,
        status: TicketStatus,
        view: TicketView = TicketView.ASSIGNED,
        search_string: Optional[str] = None
    ) -> List[Ticket]:
        """
        Get root cause tickets with a given status.
        
        GET /api/RootCause/Tickets
        
        Args:
            status: Ticket status flags (can be combined with |)
                    e.g., TicketStatus.OPEN | TicketStatus.IN_PROGRESS
            view: View filter (default: ASSIGNED)
                  - ASSIGNED: Tickets assigned to current user
                  - FOLLOWING: Tickets current user is following
                  - ALL: All tickets (requires "Manage All Tickets" permission)
            search_string: Optional search for subject, tags, or tag value
            
        Returns:
            List of Ticket objects matching the criteria
        """
        return self._api.get_tickets(status, view, search_string)
    
    def get_my_open_tickets(self) -> List[Ticket]:
        """
        Get all open tickets assigned to the current user.
        
        Convenience method for get_tickets with OPEN status and ASSIGNED view.
        
        Returns:
            List of open Ticket objects assigned to current user
        """
        return self._api.get_tickets(TicketStatus.OPEN, TicketView.ASSIGNED)
    
    def get_my_tickets_in_progress(self) -> List[Ticket]:
        """
        Get all tickets in progress assigned to the current user.
        
        Convenience method for get_tickets with IN_PROGRESS status and ASSIGNED view.
        
        Returns:
            List of in-progress Ticket objects assigned to current user
        """
        return self._api.get_tickets(TicketStatus.IN_PROGRESS, TicketView.ASSIGNED)
    
    def get_my_active_tickets(self) -> List[Ticket]:
        """
        Get all active tickets (open or in progress) assigned to the current user.
        
        Returns:
            List of active Ticket objects assigned to current user
        """
        return self._api.get_tickets(
            TicketStatus.OPEN | TicketStatus.IN_PROGRESS,
            TicketView.ASSIGNED
        )
    
    def get_all_open_tickets(self) -> List[Ticket]:
        """
        Get all open tickets in the system.
        
        Note: Requires "Manage All Tickets" permission.
        
        Returns:
            List of all open Ticket objects
        """
        return self._api.get_tickets(TicketStatus.OPEN, TicketView.ALL)
    
    def search_tickets(
        self,
        search_string: str,
        status: Optional[TicketStatus] = None,
        view: TicketView = TicketView.ALL
    ) -> List[Ticket]:
        """
        Search for tickets by subject, tags, or tag value.
        
        Args:
            search_string: Search query for subject, tags, or tag value
            status: Optional status filter (default: all active statuses)
            view: View filter (default: ALL, requires permission)
            
        Returns:
            List of matching Ticket objects
        """
        if status is None:
            # Search across all non-archived statuses by default
            status = (
                TicketStatus.OPEN | 
                TicketStatus.IN_PROGRESS | 
                TicketStatus.ON_HOLD | 
                TicketStatus.SOLVED | 
                TicketStatus.CLOSED
            )
        return self._api.get_tickets(status, view, search_string)
    
    # -------------------------------------------------------------------------
    # Create/Update Operations
    # -------------------------------------------------------------------------
    
    def create_ticket(
        self,
        subject: str,
        priority: TicketPriority = TicketPriority.MEDIUM,
        assignee: Optional[str] = None,
        team: Optional[str] = None,
        initial_comment: Optional[str] = None,
        report_uuid: Optional[Union[str, UUID]] = None
    ) -> Optional[Ticket]:
        """
        Create a new root cause ticket.
        
        POST /api/RootCause/Ticket
        
        Args:
            subject: Ticket subject/title (required)
            priority: Priority level (default: MEDIUM)
            assignee: Username to assign the ticket to
            team: Team to assign the ticket to
            initial_comment: Optional initial comment/description
            report_uuid: Optional UUID of associated report
            
        Returns:
            Created Ticket object with assigned ID and ticket number
        """
        ticket = Ticket(
            subject=subject,
            priority=priority,
            assignee=assignee,
            team=team,
            report_uuid=UUID(str(report_uuid)) if report_uuid else None
        )
        
        if initial_comment:
            ticket.update = TicketUpdate(
                content=initial_comment,
                update_type=TicketUpdateType.CONTENT
            )
        
        return self._api.create_ticket(ticket)
    
    def update_ticket(self, ticket: Ticket) -> Optional[Ticket]:
        """
        Update a root cause ticket.
        
        PUT /api/RootCause/Ticket
        
        Args:
            ticket: Ticket object with updated data.
                    The 'update' field can contain a new comment/update.
            
        Returns:
            Updated Ticket object
        """
        return self._api.update_ticket(ticket)
    
    def add_comment(
        self,
        ticket_id: Union[str, UUID],
        comment: str,
        attachment_ids: Optional[List[Union[str, UUID]]] = None
    ) -> Optional[Ticket]:
        """
        Add a comment to a ticket.
        
        Args:
            ticket_id: The ticket ID to comment on
            comment: The comment text
            attachment_ids: Optional list of previously uploaded attachment IDs
            
        Returns:
            Updated Ticket object
        """
        attachments = None
        if attachment_ids:
            attachments = [
                TicketAttachment(attachment_id=UUID(str(aid)))
                for aid in attachment_ids
            ]
        
        ticket = Ticket(
            ticket_id=UUID(str(ticket_id)),
            update=TicketUpdate(
                content=comment,
                update_type=TicketUpdateType.CONTENT,
                attachments=attachments
            )
        )
        return self._api.update_ticket(ticket)
    
    def change_status(
        self,
        ticket_id: Union[str, UUID],
        new_status: TicketStatus,
        comment: Optional[str] = None
    ) -> Optional[Ticket]:
        """
        Change the status of a ticket.
        
        Args:
            ticket_id: The ticket ID to update
            new_status: New status to set
            comment: Optional comment explaining the status change
            
        Returns:
            Updated Ticket object
        """
        update = None
        if comment:
            update = TicketUpdate(
                content=comment,
                update_type=TicketUpdateType.PROPERTIES
            )
        
        ticket = Ticket(
            ticket_id=UUID(str(ticket_id)),
            status=new_status,
            update=update
        )
        return self._api.update_ticket(ticket)
    
    def assign_ticket(
        self,
        ticket_id: Union[str, UUID],
        assignee: str,
        comment: Optional[str] = None
    ) -> Optional[Ticket]:
        """
        Assign a ticket to a user.
        
        Args:
            ticket_id: The ticket ID to assign
            assignee: Username to assign the ticket to
            comment: Optional comment explaining the assignment
            
        Returns:
            Updated Ticket object
        """
        update = None
        if comment:
            update = TicketUpdate(
                content=comment,
                update_type=TicketUpdateType.PROPERTIES
            )
        
        ticket = Ticket(
            ticket_id=UUID(str(ticket_id)),
            assignee=assignee,
            update=update
        )
        return self._api.update_ticket(ticket)
    
    def change_priority(
        self,
        ticket_id: Union[str, UUID],
        priority: TicketPriority,
        comment: Optional[str] = None
    ) -> Optional[Ticket]:
        """
        Change the priority of a ticket.
        
        Args:
            ticket_id: The ticket ID to update
            priority: New priority level
            comment: Optional comment explaining the priority change
            
        Returns:
            Updated Ticket object
        """
        update = None
        if comment:
            update = TicketUpdate(
                content=comment,
                update_type=TicketUpdateType.PROPERTIES
            )
        
        ticket = Ticket(
            ticket_id=UUID(str(ticket_id)),
            priority=priority,
            update=update
        )
        return self._api.update_ticket(ticket)
    
    # -------------------------------------------------------------------------
    # Archive Operations
    # -------------------------------------------------------------------------
    
    def archive_tickets(self, ticket_ids: List[Union[str, UUID]]) -> Optional[Ticket]:
        """
        Archive solved tickets.
        
        Only Solved tickets can be archived.
        Only ticket owner or users with "Manage All Tickets" permission can archive tickets.
        
        POST /api/RootCause/ArchiveTickets
        
        Args:
            ticket_ids: List of ticket IDs to archive
            
        Returns:
            Ticket object (typically the last archived ticket) or None
        """
        return self._api.archive_tickets(ticket_ids)
    
    def archive_ticket(self, ticket_id: Union[str, UUID]) -> Optional[Ticket]:
        """
        Archive a single solved ticket.
        
        Convenience method for archiving a single ticket.
        
        Args:
            ticket_id: The ticket ID to archive
            
        Returns:
            Archived Ticket object or None
        """
        return self._api.archive_tickets([ticket_id])
    
    # -------------------------------------------------------------------------
    # Attachment Operations
    # -------------------------------------------------------------------------
    
    def get_attachment(
        self,
        attachment_id: Union[str, UUID],
        filename: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Get root cause attachment content.
        
        GET /api/RootCause/Attachment
        
        Args:
            attachment_id: The attachment ID (GUID)
            filename: Optional filename for download.
                      Skip to display images (jpeg, png, bmp) with an HTML img tag.
            
        Returns:
            Attachment content as bytes, or None if not found
        """
        return self._api.get_attachment(attachment_id, filename)
    
    def download_attachment(
        self,
        attachment_id: Union[str, UUID],
        filename: str,
        save_path: Optional[Union[str, Path]] = None
    ) -> Optional[Path]:
        """
        Download an attachment and save it to disk.
        
        Args:
            attachment_id: The attachment ID (GUID)
            filename: The filename for the downloaded file
            save_path: Optional path to save the file.
                       If not provided, saves to current directory.
            
        Returns:
            Path to the saved file, or None if download failed
        """
        content = self._api.get_attachment(attachment_id, filename)
        if content is None:
            return None
        
        if save_path:
            file_path = Path(save_path) / filename
        else:
            file_path = Path(filename)
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(content)
        return file_path
    
    def upload_attachment(self, file_content: bytes, filename: str) -> Optional[UUID]:
        """
        Upload a root cause attachment.
        
        POST /api/RootCause/Attachment
        
        Args:
            file_content: The file content as bytes
            filename: The filename for the attachment
            
        Returns:
            UUID of the created attachment, or None if failed
        """
        return self._api.upload_attachment(file_content, filename)
    
    def upload_file(self, file_path: Union[str, Path]) -> Optional[UUID]:
        """
        Upload a file as an attachment.
        
        Convenience method that reads a file from disk and uploads it.
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            UUID of the created attachment, or None if failed
        """
        path = Path(file_path)
        if not path.exists():
            return None
        
        content = path.read_bytes()
        return self._api.upload_attachment(content, path.name)
