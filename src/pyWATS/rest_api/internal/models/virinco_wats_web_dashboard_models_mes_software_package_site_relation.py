from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage





T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesSoftwarePackageSiteRelation")



@_attrs_define
class VirincoWATSWebDashboardModelsMesSoftwarePackageSiteRelation:
    """ 
        Attributes:
            package_site_relation_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            site_code (Union[Unset, str]):
            package_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            package (Union[Unset, VirincoWATSWebDashboardModelsMesSoftwarePackage]):
     """

    package_site_relation_id: Union[Unset, UUID] = UNSET
    site_code: Union[Unset, str] = UNSET
    package_id: Union[Unset, UUID] = UNSET
    package: Union[Unset, 'VirincoWATSWebDashboardModelsMesSoftwarePackage'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
        package_site_relation_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_site_relation_id, Unset):
            package_site_relation_id = str(self.package_site_relation_id)

        site_code = self.site_code

        package_id: Union[Unset, str] = UNSET
        if not isinstance(self.package_id, Unset):
            package_id = str(self.package_id)

        package: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.package, Unset):
            package = self.package.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if package_site_relation_id is not UNSET:
            field_dict["PackageSiteRelationId"] = package_site_relation_id
        if site_code is not UNSET:
            field_dict["SiteCode"] = site_code
        if package_id is not UNSET:
            field_dict["PackageId"] = package_id
        if package is not UNSET:
            field_dict["Package"] = package

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_web_dashboard_models_mes_software_package import VirincoWATSWebDashboardModelsMesSoftwarePackage
        d = dict(src_dict)
        _package_site_relation_id = d.pop("PackageSiteRelationId", UNSET)
        package_site_relation_id: Union[Unset, UUID]
        if isinstance(_package_site_relation_id,  Unset):
            package_site_relation_id = UNSET
        else:
            package_site_relation_id = UUID(_package_site_relation_id)




        site_code = d.pop("SiteCode", UNSET)

        _package_id = d.pop("PackageId", UNSET)
        package_id: Union[Unset, UUID]
        if isinstance(_package_id,  Unset):
            package_id = UNSET
        else:
            package_id = UUID(_package_id)




        _package = d.pop("Package", UNSET)
        package: Union[Unset, VirincoWATSWebDashboardModelsMesSoftwarePackage]
        if isinstance(_package,  Unset):
            package = UNSET
        else:
            package = VirincoWATSWebDashboardModelsMesSoftwarePackage.from_dict(_package)




        virinco_wats_web_dashboard_models_mes_software_package_site_relation = cls(
            package_site_relation_id=package_site_relation_id,
            site_code=site_code,
            package_id=package_id,
            package=package,
        )


        virinco_wats_web_dashboard_models_mes_software_package_site_relation.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_software_package_site_relation

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
