from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesSoftwarePublicPackageFile")



@_attrs_define
class VirincoWATSWebDashboardModelsMesSoftwarePublicPackageFile:
    """ 
        Attributes:
            package_file_id (Union[Unset, str]):
            name (Union[Unset, str]):
            package_folder_name (Union[Unset, str]):
            attributes (Union[Unset, str]):
            description (Union[Unset, str]):
     """

    package_file_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    package_folder_name: Union[Unset, str] = UNSET
    attributes: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        package_file_id = self.package_file_id

        name = self.name

        package_folder_name = self.package_folder_name

        attributes = self.attributes

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if package_file_id is not UNSET:
            field_dict["packageFileId"] = package_file_id
        if name is not UNSET:
            field_dict["name"] = name
        if package_folder_name is not UNSET:
            field_dict["packageFolderName"] = package_folder_name
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if description is not UNSET:
            field_dict["Description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        package_file_id = d.pop("packageFileId", UNSET)

        name = d.pop("name", UNSET)

        package_folder_name = d.pop("packageFolderName", UNSET)

        attributes = d.pop("attributes", UNSET)

        description = d.pop("Description", UNSET)

        virinco_wats_web_dashboard_models_mes_software_public_package_file = cls(
            package_file_id=package_file_id,
            name=name,
            package_folder_name=package_folder_name,
            attributes=attributes,
            description=description,
        )


        virinco_wats_web_dashboard_models_mes_software_public_package_file.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_software_public_package_file

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
