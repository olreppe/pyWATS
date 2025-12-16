from typing import List

import pytest

from pywats.domains.process.models import ProcessInfo
from pywats.domains.process.service import ProcessService


class DummyProcessRepository:
    def __init__(self) -> None:
        self.call_count = 0

    def get_processes(self) -> List[ProcessInfo]:
        self.call_count += 1
        return [
            ProcessInfo(code=100, name="End of line", is_test_operation=True),
            ProcessInfo(code=500, name="Repair", is_repair_operation=True),
            ProcessInfo(code=200, name="WIP", is_wip_operation=True),
        ]


@pytest.fixture
def process_service() -> ProcessService:
    repository = DummyProcessRepository()
    return ProcessService(repository=repository)


def test_refresh_populates_cache(process_service: ProcessService) -> None:
    repo = process_service._repository

    assert process_service.last_refresh is None
    process_service.refresh()

    assert repo.call_count == 1
    assert process_service.get_processes()
    assert process_service.last_refresh is not None


def test_get_test_operation_by_name(process_service: ProcessService) -> None:
    test_op = process_service.get_test_operation("End of line")

    assert test_op is not None
    assert test_op.code == 100


def test_get_default_repair_code(process_service: ProcessService) -> None:
    assert process_service.get_default_repair_code() == 500
