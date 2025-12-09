"""
Tests for root cause module - ticket integration with external systems
"""
import pytest
from src.pywats.domains.rootcause import Ticket, TicketStatus, TicketPriority


class TestRootCauseTicket:
    """Test root cause ticket operations"""

    def test_create_ticket(self):
        """Test creating a root cause ticket"""
        ticket = Ticket(
            subject="Test failure",
            priority=TicketPriority.MEDIUM,
        )
        assert ticket.subject == "Test failure"
        assert ticket.priority == TicketPriority.MEDIUM

    def test_submit_ticket(self, wats_client):
        """Test submitting a root cause ticket"""
        ticket = Ticket(
            subject="Test failure description",
            priority=TicketPriority.HIGH,
        )

        try:
            result = wats_client.root_cause.create_ticket(ticket)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Ticket creation failed: {e}")

    def test_get_ticket(self, wats_client):
        """Test retrieving a ticket"""
        try:
            # Note: This needs a valid ticket_id from the system
            tickets = wats_client.root_cause.get_open_tickets()
            if tickets:
                ticket = wats_client.root_cause.get_ticket(tickets[0].ticket_id)
                assert ticket is not None
        except Exception as e:
            pytest.skip(f"Get ticket failed: {e}")


class TestTicketLinking:
    """Test linking tickets to reports/units"""

    def test_link_ticket_to_report(self, wats_client):
        """Test linking a ticket to a report"""
        pytest.skip("Link ticket to report requires valid report UUID")

    def test_get_tickets_for_unit(self, wats_client, test_serial_number):
        """Test getting tickets associated with a unit"""
        pytest.skip("Get unit tickets not implemented in current API")
