from typing import List, Optional, Union
from uuid import UUID, uuid4

import pytest

from pywats.domains.rootcause.enums import TicketStatus, TicketView
from pywats.domains.rootcause.models import Ticket
from pywats.domains.rootcause.service import RootCauseService


class DummyRootCauseRepository:
    def __init__(self) -> None:
        self.created: Optional[Ticket] = None
        self.updated: Optional[Ticket] = None
        self.archived: List[Union[str, Ticket]] = []

    def get_ticket(self, ticket_id: Union[str, UUID]) -> Optional[Ticket]:
        return Ticket(ticket_id=uuid4(), subject="Existing")

    def get_tickets(self, status: TicketStatus, view: TicketView, search_string: Optional[str] = None) -> List[Ticket]:
        return [Ticket(ticket_id=uuid4(), subject="List")]

    def create_ticket(self, ticket: Ticket) -> Optional[Ticket]:
        self.created = ticket
        ticket.ticket_id = ticket.ticket_id or uuid4()
        return ticket

    def update_ticket(self, ticket: Ticket) -> Optional[Ticket]:
        self.updated = ticket
        return ticket

    def archive_tickets(self, ticket_ids: List[Union[str, UUID]]) -> Optional[Ticket]:
        self.archived.extend(ticket_ids)
        return Ticket(ticket_id=uuid4(), subject="Archived")

    def get_attachment(self, attachment_id: Union[str, UUID], filename: Optional[str] = None) -> Optional[bytes]:
        return b"data"

    def upload_attachment(self, file_content: bytes, filename: str) -> Optional[UUID]:
        return uuid4()


@pytest.fixture
def rootcause_service() -> RootCauseService:
    return RootCauseService(repository_or_client=DummyRootCauseRepository())


def test_create_ticket_routes_to_repository(rootcause_service: RootCauseService) -> None:
    service = rootcause_service
    ticket = service.create_ticket(subject="New Issue", assignee="user")

    assert ticket is not None
    assert service._repository.created is not None
    assert service._repository.created.subject == "New Issue"
    assert service._repository.created.assignee == "user"


def test_assign_ticket_updates_assignee(rootcause_service: RootCauseService) -> None:
    ticket_id = uuid4()

    result = rootcause_service.assign_ticket(ticket_id=ticket_id, assignee="assigned")

    assert result is not None
    assert rootcause_service._repository.updated is not None
    assert rootcause_service._repository.updated.assignee == "assigned"
*** End of file***