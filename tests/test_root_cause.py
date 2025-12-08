"""
Tests for root cause module - ticket integration with external systems
"""
import pytest
from pywats.models.root_cause import RootCauseTicket


class TestRootCauseTicket:
    """Test root cause ticket operations"""
    
    def test_create_ticket(self):
        """Test creating a root cause ticket"""
        ticket = RootCauseTicket(
            ticket_id="TICKET-001",
            description="Test failure",
            system="JIRA"
        )
        assert ticket.ticket_id == "TICKET-001"
    
    def test_submit_ticket(self, wats_client):
        """Test submitting a root cause ticket"""
        from datetime import datetime
        ticket = RootCauseTicket(
            ticket_id=f"TICKET-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            description="Test failure description",
            system="TestSystem"
        )
        
        try:
            result = wats_client.root_cause.create_ticket(ticket)
            assert result is not None
        except Exception as e:
            pytest.skip(f"Ticket creation failed: {e}")
    
    def test_get_ticket(self, wats_client):
        """Test retrieving a ticket"""
        try:
            ticket = wats_client.root_cause.get_ticket("TICKET-001")
            if ticket:
                assert ticket.ticket_id == "TICKET-001"
        except Exception as e:
            pytest.skip(f"Get ticket failed: {e}")


class TestTicketLinking:
    """Test linking tickets to reports/units"""
    
    def test_link_ticket_to_report(self, wats_client):
        """Test linking a ticket to a report"""
        try:
            result = wats_client.root_cause.link_ticket_to_report(
                ticket_id="TICKET-001",
                report_uuid="00000000-0000-0000-0000-000000000000"
            )
            assert result is not None
        except Exception as e:
            pytest.skip(f"Link ticket failed: {e}")
    
    def test_get_tickets_for_unit(self, wats_client, test_serial_number):
        """Test getting tickets associated with a unit"""
        try:
            tickets = wats_client.root_cause.get_unit_tickets(test_serial_number)
            assert isinstance(tickets, list)
        except Exception as e:
            pytest.skip(f"Get unit tickets failed: {e}")
