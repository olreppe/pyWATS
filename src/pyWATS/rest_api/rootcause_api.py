"""
RootCause (Ticketing) API Endpoints

Provides all REST API calls for the RootCause ticketing system.
All methods return typed model objects instead of raw responses.

Public API Endpoints (from Swagger):
- POST /api/RootCause/ArchiveTickets - Archive solved tickets
- GET /api/RootCause/Attachment - Get attachment content
- POST /api/RootCause/Attachment - Upload attachment
- GET /api/RootCause/Ticket - Get a ticket by ID
- POST /api/RootCause/Ticket - Create a new ticket
- PUT /api/RootCause/Ticket - Update a ticket
- GET /api/RootCause/Tickets - Get tickets by status
"""

from typing import Optional, List, Union, Dict, Any, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from ..http_client import HttpClient

from ..models.rootcause import (
    Ticket, TicketStatus, TicketView, TicketAttachment
)


class RootCauseApi:
    """
    RootCause (Ticketing) API endpoints.
    
    Endpoints for managing tickets in the RootCause ticketing system,
    enabling collaboration on issue tracking and resolution.
    All methods return typed model objects.
    """
    
    def __init__(self, http: 'HttpClient'):
        self._http = http
    
    # =========================================================================
    # Ticket Operations
    # =========================================================================
    
    def get_ticket(self, ticket_id: Union[str, UUID]) -> Optional[Ticket]:
        """
        Get a root cause ticket by ID.
        
        GET /api/RootCause/Ticket
        
        Args:
            ticket_id: The ticket ID (GUID)
            
        Returns:
            Ticket object or None if not found
        """
        response = self._http.get(
            "/api/RootCause/Ticket",
            params={"ticketId": str(ticket_id)}
        )
        if response.is_success and response.data:
            return Ticket.model_validate(response.data)
        return None
    
    def get_tickets(
        self,
        status: TicketStatus,
        view: TicketView,
        search_string: Optional[str] = None
    ) -> List[Ticket]:
        """
        Get root cause tickets with a given status.
        
        GET /api/RootCause/Tickets
        
        Args:
            status: Ticket status flags (can be combined with |)
                    e.g., TicketStatus.OPEN | TicketStatus.IN_PROGRESS
            view: View filter (ASSIGNED=0, FOLLOWING=1, ALL=2)
                  Note: ALL view requires "Manage All Tickets" permission
            search_string: Optional search for subject, tags, or tag value
            
        Returns:
            List of Ticket objects matching the criteria
        """
        params: Dict[str, Any] = {
            "status": int(status),
            "view": int(view)
        }
        if search_string:
            params["searchString"] = search_string
        
        response = self._http.get("/api/RootCause/Tickets", params=params)
        if response.is_success and response.data:
            return [Ticket.model_validate(item) for item in response.data]
        return []
    
    def create_ticket(self, ticket: Ticket) -> Optional[Ticket]:
        """
        Create a new root cause ticket.
        
        POST /api/RootCause/Ticket
        
        Args:
            ticket: Ticket object with the new ticket data.
                    Required fields: subject
                    Optional: priority, assignee, team, tags, update (initial comment)
            
        Returns:
            Created Ticket object with assigned ID and ticket number
        """
        response = self._http.post(
            "/api/RootCause/Ticket",
            json=ticket.model_dump(by_alias=True, exclude_none=True)
        )
        if response.is_success and response.data:
            return Ticket.model_validate(response.data)
        return None
    
    def update_ticket(self, ticket: Ticket) -> Optional[Ticket]:
        """
        Update a root cause ticket.
        
        PUT /api/RootCause/Ticket
        
        Args:
            ticket: Ticket object with updated data.
                    Required: ticket_id
                    The 'update' field can contain a new comment/update
            
        Returns:
            Updated Ticket object
        """
        response = self._http.put(
            "/api/RootCause/Ticket",
            json=ticket.model_dump(by_alias=True, exclude_none=True)
        )
        if response.is_success and response.data:
            return Ticket.model_validate(response.data)
        return None
    
    def archive_tickets(self, ticket_ids: List[Union[str, UUID]]) -> Optional[Ticket]:
        """
        Archive tickets.
        
        Only Solved tickets can be archived.
        Only ticket owner or users with "Manage All Tickets" permission can archive tickets.
        
        POST /api/RootCause/ArchiveTickets
        
        Args:
            ticket_ids: List of ticket IDs to archive
            
        Returns:
            Ticket object (typically the last archived ticket) or None
        """
        ids = [str(tid) for tid in ticket_ids]
        response = self._http.post("/api/RootCause/ArchiveTickets", json=ids)
        if response.is_success and response.data:
            return Ticket.model_validate(response.data)
        return None
    
    # =========================================================================
    # Attachment Operations
    # =========================================================================
    
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
        params = {"attachmentId": str(attachment_id)}
        if filename:
            params["fileName"] = filename
        
        response = self._http.get("/api/RootCause/Attachment", params=params)
        if response.is_success:
            # Return raw bytes for attachment
            return response.raw
        return None
    
    def upload_attachment(self, file_content: bytes, filename: str) -> Optional[UUID]:
        """
        Upload root cause attachment and return attachment ID.
        
        POST /api/RootCause/Attachment
        
        Args:
            file_content: The file content as bytes
            filename: The filename for the attachment
            
        Returns:
            UUID of the created attachment, or None if failed
        """
        # Upload as multipart form data
        files = {"file": (filename, file_content)}
        response = self._http.post(
            "/api/RootCause/Attachment",
            files=files
        )
        if response.is_success and response.data:
            # Response is a UUID string
            return UUID(response.data) if isinstance(response.data, str) else None
        return None
