from typing import List, Optional, Tuple, Union
from uuid import UUID, uuid4

import pytest

from pywats.domains.software.enums import PackageStatus
from pywats.domains.software.models import Package, PackageTag
from pywats.domains.software.service import SoftwareService
from pywats.domains.software.repository import SoftwareRepository


class DummySoftwareRepository(SoftwareRepository):
    def __init__(self) -> None:
        self.created: Optional[Package] = None
        self.status_updates: List[Tuple[Union[str, UUID], PackageStatus]] = []  # Need Tuple import
        self.deleted: List[Union[str, UUID]] = []

    def get_packages(self) -> List[Package]:
        pkg = Package(name="Existing")
        pkg.package_id = uuid4()
        return [pkg]

    def create_package(self, package: Package) -> Optional[Package]:
        self.created = package
        package.package_id = uuid4()
        return package

    def update_package_status(self, package_id: Union[str, UUID], status: PackageStatus) -> bool:
        self.status_updates.append((package_id, status))
        return True

    def delete_package(self, package_id: Union[str, UUID]) -> bool:
        self.deleted.append(package_id)
        return True


@pytest.fixture
def software_service() -> SoftwareService:
    return SoftwareService(repository_or_client=DummySoftwareRepository())


def test_create_package_calls_repository(software_service: SoftwareService) -> None:
    repo = software_service._repository

    tags = [PackageTag(key="env", value="prod")]
    pkg = software_service.create_package(
        name="NewPkg",
        description="Test",
        tags=tags,
    )

    assert pkg is not None
    assert pkg.tags == tags
    assert repo.created is pkg


def test_submit_for_review_updates_status(software_service: SoftwareService) -> None:
    pkg_id = uuid4()

    result = software_service.submit_for_review(pkg_id)

    assert result is True
    repo = software_service._repository
    assert repo.status_updates
    assert repo.status_updates[-1] == (pkg_id, PackageStatus.PENDING)
