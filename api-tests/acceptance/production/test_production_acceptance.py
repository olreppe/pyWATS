from typing import List, Tuple

import pytest

from pywats.domains.production.enums import UnitPhaseFlag
from pywats.domains.production.models import Unit
from pywats.domains.production.service import ProductionService


class DummyProductionRepository:
    def __init__(self) -> None:
        self.saved_units: List[Unit] = []
        self.phase_calls: List[Tuple[str, str, int, str]] = []
        self.child_calls: List[Tuple[str, str, str, str]] = []

    def save_units(self, units: List[Unit]) -> List[Unit]:
        self.saved_units.extend(units)
        return units

    def set_unit_phase(
        self,
        serial_number: str,
        part_number: str,
        phase: int,
        comment: str | None = None
    ) -> bool:
        self.phase_calls.append((serial_number, part_number, phase, comment or ""))
        return True

    def add_child_unit(
        self,
        parent_serial: str,
        parent_part: str,
        child_serial: str,
        child_part: str
    ) -> bool:
        self.child_calls.append((parent_serial, parent_part, child_serial, child_part))
        return True


@pytest.fixture
def production_service() -> ProductionService:
    repository = DummyProductionRepository()
    return ProductionService(repository=repository)


def test_create_units_invokes_repository(production_service: ProductionService) -> None:
    units = [Unit(serial_number="SN-A", part_number="PN-A"), Unit(serial_number="SN-B", part_number="PN-B")]

    created = production_service.create_units(units)

    repo = production_service._repository
    assert created == units
    assert repo.saved_units == units


def test_set_unit_phase_accepts_enum(production_service: ProductionService) -> None:
    result = production_service.set_unit_phase(
        serial_number="SN-123",
        part_number="PN-123",
        phase=UnitPhaseFlag.FINALIZED
    )

    repo = production_service._repository
    assert result is True
    assert repo.phase_calls[-1][2] == int(UnitPhaseFlag.FINALIZED)


def test_add_child_unit_routes_call(production_service: ProductionService) -> None:
    success = production_service.add_child_to_assembly(
        parent_serial="SN-P",
        parent_part="PN-P",
        child_serial="SN-C",
        child_part="PN-C"
    )

    repo = production_service._repository
    assert success is True
    assert repo.child_calls[-1] == ("SN-P", "PN-P", "SN-C", "PN-C")
