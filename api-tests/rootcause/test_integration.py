"""
Tests for root cause module - ticket management for issue collaboration

These tests make actual API calls to the WATS server.
"""
from typing import Any
from datetime import datetime, timezone
import pytest
from pywats.domains.rootcause import Ticket, TicketStatus, TicketPriority


class TestTicketModel:
    """Test Ticket model creation (no server)"""

    def test_create_ticket_model(self) -> None:
        """Test creating a ticket model object"""
        ticket = Ticket(
            subject="Test failure",
            priority=TicketPriority.MEDIUM,
        )
        assert ticket.subject == "Test failure"
        assert ticket.priority == TicketPriority.MEDIUM

    def test_create_ticket_with_progress(self) -> None:
        """Test creating a ticket with progress notes"""
        ticket = Ticket(
            subject="Component failure",
            progress="Initial investigation started",
            priority=TicketPriority.HIGH,
        )
        assert ticket.subject == "Component failure"
        assert ticket.progress == "Initial investigation started"


class TestTicketRetrieval:
    """Test retrieving tickets from server"""

    def test_get_all_tickets(self, wats_client: Any) -> None:
        """Test getting all tickets"""
        print("\n=== GET ALL TICKETS ===")
        
        tickets = wats_client.rootcause.get_tickets()
        
        print(f"Retrieved {len(tickets)} tickets")
        for t in tickets[:5]:
            print(f"  - {t.ticket_id}: {t.subject}")
        print("=======================\n")
        
        assert isinstance(tickets, list)

    def test_get_open_tickets(self, wats_client: Any) -> None:
        """Test getting open tickets"""
        print("\n=== GET OPEN TICKETS ===")
        
        tickets = wats_client.rootcause.get_open_tickets()
        
        print(f"Retrieved {len(tickets)} open tickets")
        print("========================\n")
        
        assert isinstance(tickets, list)

    def test_get_active_tickets(self, wats_client: Any) -> None:
        """Test getting active tickets"""
        print("\n=== GET ACTIVE TICKETS ===")
        
        tickets = wats_client.rootcause.get_active_tickets()
        
        print(f"Retrieved {len(tickets)} active tickets")
        print("==========================\n")
        
        assert isinstance(tickets, list)


class TestTicketCreation:
    """Test creating tickets on server"""

    def test_create_ticket(self, wats_client: Any) -> None:
        """Test creating a new ticket"""
        timestamp = datetime.now().astimezone().strftime('%Y%m%d%H%M%S')
        
        print("\n=== CREATE TICKET ===")
        
        subject = f"PyTest Ticket {timestamp}"
        
        print(f"Creating ticket: {subject}")
        
        result = wats_client.rootcause.create_ticket(
            subject=subject,
            priority=TicketPriority.LOW,
            initial_comment="Created by pytest automated tests"
        )
        
        print(f"Create result: {result}")
        print("=====================\n")
        
        assert result is not None


class TestTicketOperations:
    """Test ticket operations"""

    def test_get_ticket_by_id(self, wats_client: Any) -> None:
        """Test getting a specific ticket"""
        print("\n=== GET TICKET BY ID ===")
        
        # First get list of tickets
        tickets = wats_client.rootcause.get_tickets()
        if not tickets:
            pytest.skip("No tickets available")
        
        ticket_id = tickets[0].ticket_id
        print(f"Looking up ticket: {ticket_id}")
        
        ticket = wats_client.rootcause.get_ticket(ticket_id)
        
        print(f"Found: {ticket}")
        print("========================\n")
        
        assert ticket is not None
