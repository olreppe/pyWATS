from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsSystemManagerNodeDisk")



@_attrs_define
class VirincoWATSWebDashboardModelsSystemManagerNodeDisk:
    """ 
        Attributes:
            name (Union[Unset, str]):
            display_name (Union[Unset, str]):
            drive_type (Union[Unset, str]):
            system_drive (Union[Unset, str]):
            volume_label (Union[Unset, str]):
            total_size (Union[Unset, str]):
            available_free_space (Union[Unset, str]):
            total_free_space (Union[Unset, str]):
            drive_format (Union[Unset, str]):
     """

    name: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    drive_type: Union[Unset, str] = UNSET
    system_drive: Union[Unset, str] = UNSET
    volume_label: Union[Unset, str] = UNSET
    total_size: Union[Unset, str] = UNSET
    available_free_space: Union[Unset, str] = UNSET
    total_free_space: Union[Unset, str] = UNSET
    drive_format: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        display_name = self.display_name

        drive_type = self.drive_type

        system_drive = self.system_drive

        volume_label = self.volume_label

        total_size = self.total_size

        available_free_space = self.available_free_space

        total_free_space = self.total_free_space

        drive_format = self.drive_format


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if drive_type is not UNSET:
            field_dict["driveType"] = drive_type
        if system_drive is not UNSET:
            field_dict["systemDrive"] = system_drive
        if volume_label is not UNSET:
            field_dict["volumeLabel"] = volume_label
        if total_size is not UNSET:
            field_dict["totalSize"] = total_size
        if available_free_space is not UNSET:
            field_dict["availableFreeSpace"] = available_free_space
        if total_free_space is not UNSET:
            field_dict["totalFreeSpace"] = total_free_space
        if drive_format is not UNSET:
            field_dict["driveFormat"] = drive_format

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        display_name = d.pop("displayName", UNSET)

        drive_type = d.pop("driveType", UNSET)

        system_drive = d.pop("systemDrive", UNSET)

        volume_label = d.pop("volumeLabel", UNSET)

        total_size = d.pop("totalSize", UNSET)

        available_free_space = d.pop("availableFreeSpace", UNSET)

        total_free_space = d.pop("totalFreeSpace", UNSET)

        drive_format = d.pop("driveFormat", UNSET)

        virinco_wats_web_dashboard_models_system_manager_node_disk = cls(
            name=name,
            display_name=display_name,
            drive_type=drive_type,
            system_drive=system_drive,
            volume_label=volume_label,
            total_size=total_size,
            available_free_space=available_free_space,
            total_free_space=total_free_space,
            drive_format=drive_format,
        )


        virinco_wats_web_dashboard_models_system_manager_node_disk.additional_properties = d
        return virinco_wats_web_dashboard_models_system_manager_node_disk

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
