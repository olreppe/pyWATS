from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pytest

from pywats.domains.app.models import ProcessInfo, YieldData
from pywats.domains.app.service import AppService
from pywats.domains.report.models import WATSFilter, ReportHeader


class DummyAppRepository:
    def __init__(self) -> None:
        self.process_calls: int = 0
        self.last_filter: Optional[WATSFilter] = None
        self.headers_requested: bool = False

    def get_version(self) -> Dict[str, Any]:
        return {"build": "1.0"}

    def get_processes(self) -> List[ProcessInfo]:
        self.process_calls += 1
        return [ProcessInfo(code=100, name="Test", is_test_operation=True)]

    def get_dynamic_yield(
        self,
        filter_data: Optional[WATSFilter] = None,
    ) -> List[YieldData]:
        self.last_filter = filter_data
        return [YieldData(part_number="PN-1", fpy=99.0)]

    def get_serial_number_history(self, filter_data: WATSFilter) -> List[ReportHeader]:
        self.headers_requested = True
        return [ReportHeader(report_id="ID-001", serial_number="SN-1")]

    def get_uut_reports(self, filter_data: Optional[WATSFilter] = None, **kwargs: Any) -> List[ReportHeader]:
        return [ReportHeader(report_id="ID-002", serial_number="SN-2")]


@pytest.fixture
def app_service() -> AppService:
    repository = DummyAppRepository()
    return AppService(repository=repository)


def test_get_processes_uses_repository(app_service: AppService) -> None:
    repo = app_service._repository

    processes = app_service.get_processes()

    assert len(processes) == 1
    assert processes[0].code == 100
    assert repo.process_calls == 1


def test_get_dynamic_yield_passes_filters(app_service: AppService) -> None:
    repo = app_service._repository
    filter_data = WATSFilter(part_number="PN-1")

    result = app_service.get_dynamic_yield(filter_data)

    assert result
    assert repo.last_filter is filter_data


def test_get_serial_number_history_forwards_filters(app_service: AppService) -> None:
    filter_data = WATSFilter(serial_number="SN-ABC")

    headers = app_service.get_serial_number_history(filter_data)

    assert app_service._repository.headers_requested
