from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import pytest

from pywats.domains.report.service import ReportService
from pywats.domains.report.models import WATSFilter, ReportHeader
from pywats.domains.report.report_models import UUTReport, UURReport


@dataclass
class DummyStation:
    name: str
    location: str
    purpose: str


class DummyReportRepository:
    def __init__(self):
        self.wsjf_calls: List[Any] = []
        self.latest_parameters: Dict[str, Any] = {}

    def query_headers(
        self,
        report_type: str = "uut",
        filter_data: Optional[Union[WATSFilter, Dict[str, Any]]] = None
    ) -> List[ReportHeader]:
        return []

    def query_headers_by_misc_info(
        self,
        description: str,
        string_value: str,
        top: Optional[int] = None
    ) -> List[ReportHeader]:
        return []

    def post_wsjf(
        self,
        report: Union[UUTReport, UURReport, Dict[str, Any]]
    ) -> Optional[str]:
        self.wsjf_calls.append(report)
        return "FAKE-ID"

    def get_wsjf(self, report_id: str) -> Optional[Union[UUTReport, UURReport]]:
        return None

    def post_wsxf(self, xml_content: str) -> Optional[str]:
        return None

    def get_wsxf(self, report_id: str) -> Optional[bytes]:
        return None

    def get_attachment(
        self,
        attachment_id: Optional[str] = None,
        step_id: Optional[str] = None
    ) -> Optional[bytes]:
        return None

    def get_attachments_as_zip(self, report_id: str) -> Optional[bytes]:
        return None

    def get_certificate(self, report_id: str) -> Optional[bytes]:
        return None


@pytest.fixture
def report_service() -> ReportService:
    repo = DummyReportRepository()
    station = DummyStation(name="Line1", location="PlantA", purpose="Production")
    return ReportService(repository=repo, station_provider=lambda: station)


def test_create_uut_report_resolves_station(report_service: ReportService):
    report = report_service.create_uut_report(
        operator="TestOp",
        part_number="PN-123",
        revision="B",
        serial_number="SN-001",
        operation_type=100
    )

    assert report.station_name == "Line1"
    assert report.location == "PlantA"
    assert report.purpose == "Production"
    assert report.process_code == 100
    assert report.info.operator == "TestOp"


def test_create_uur_report_from_uut_copies_sub_units(report_service: ReportService):
    uut = report_service.create_uut_report(
        operator="Operator",
        part_number="PN-123",
        revision="B",
        serial_number="SN-001",
        operation_type=100
    )
    uut.add_sub_unit(part_type="SubBoard", sn="SUBSN", pn="PN-SUB", rev="A")

    uur = report_service.create_uur_report(uut)

    assert uur.process_code == 500
    assert uur.uur_info.test_operation_code == 100
    assert uur.sub_units is not None
    assert any(sub.sn == "SUBSN" for sub in uur.sub_units)


def test_submit_report_uses_repository(report_service: ReportService):
    uut = report_service.create_uut_report(
        operator="TestOp",
        part_number="PN-321",
        revision="C",
        serial_number="SN-002",
        operation_type=200
    )

    report_id = report_service.submit_report(uut)

    assert report_id == "FAKE-ID"
    repo = report_service._repository
    assert repo.wsjf_calls[-1] is uut
