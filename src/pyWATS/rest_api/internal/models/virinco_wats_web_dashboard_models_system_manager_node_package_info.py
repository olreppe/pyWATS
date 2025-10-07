from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo")



@_attrs_define
class VirincoWATSWebDashboardModelsSystemManagerNodePackageInfo:
    """ 
        Attributes:
            name (Union[Unset, str]):
            version (Union[Unset, int]):
            description (Union[Unset, str]):
            installed_date (Union[Unset, str]):
            is_dirty (Union[Unset, bool]):
            download_size (Union[Unset, int]):
            outdated (Union[Unset, bool]):
            available_version (Union[Unset, int]):
     """

    name: Union[Unset, str] = UNSET
    version: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    installed_date: Union[Unset, str] = UNSET
    is_dirty: Union[Unset, bool] = UNSET
    download_size: Union[Unset, int] = UNSET
    outdated: Union[Unset, bool] = UNSET
    available_version: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        version = self.version

        description = self.description

        installed_date = self.installed_date

        is_dirty = self.is_dirty

        download_size = self.download_size

        outdated = self.outdated

        available_version = self.available_version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if version is not UNSET:
            field_dict["version"] = version
        if description is not UNSET:
            field_dict["description"] = description
        if installed_date is not UNSET:
            field_dict["installedDate"] = installed_date
        if is_dirty is not UNSET:
            field_dict["isDirty"] = is_dirty
        if download_size is not UNSET:
            field_dict["downloadSize"] = download_size
        if outdated is not UNSET:
            field_dict["outdated"] = outdated
        if available_version is not UNSET:
            field_dict["availableVersion"] = available_version

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        version = d.pop("version", UNSET)

        description = d.pop("description", UNSET)

        installed_date = d.pop("installedDate", UNSET)

        is_dirty = d.pop("isDirty", UNSET)

        download_size = d.pop("downloadSize", UNSET)

        outdated = d.pop("outdated", UNSET)

        available_version = d.pop("availableVersion", UNSET)

        virinco_wats_web_dashboard_models_system_manager_node_package_info = cls(
            name=name,
            version=version,
            description=description,
            installed_date=installed_date,
            is_dirty=is_dirty,
            download_size=download_size,
            outdated=outdated,
            available_version=available_version,
        )


        virinco_wats_web_dashboard_models_system_manager_node_package_info.additional_properties = d
        return virinco_wats_web_dashboard_models_system_manager_node_package_info

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
