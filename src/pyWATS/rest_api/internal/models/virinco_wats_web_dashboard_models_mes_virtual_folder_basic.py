from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesVirtualFolderBasic")



@_attrs_define
class VirincoWATSWebDashboardModelsMesVirtualFolderBasic:
    """ 
        Attributes:
            virtual_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_virtual_folder_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            description (Union[Unset, str]):
            type_ (Union[Unset, int]):
            virtual_folders (Union[Unset, list['VirincoWATSWebDashboardModelsMesVirtualFolderBasic']]):
     """

    virtual_folder_id: Union[Unset, UUID] = UNSET
    parent_virtual_folder_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    type_: Union[Unset, int] = UNSET
    virtual_folders: Union[Unset, list['VirincoWATSWebDashboardModelsMesVirtualFolderBasic']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        virtual_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.virtual_folder_id, Unset):
            virtual_folder_id = str(self.virtual_folder_id)

        parent_virtual_folder_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_virtual_folder_id, Unset):
            parent_virtual_folder_id = str(self.parent_virtual_folder_id)

        name = self.name

        description = self.description

        type_ = self.type_

        virtual_folders: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.virtual_folders, Unset):
            virtual_folders = []
            for virtual_folders_item_data in self.virtual_folders:
                virtual_folders_item = virtual_folders_item_data.to_dict()
                virtual_folders.append(virtual_folders_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if virtual_folder_id is not UNSET:
            field_dict["VirtualFolderId"] = virtual_folder_id
        if parent_virtual_folder_id is not UNSET:
            field_dict["ParentVirtualFolderId"] = parent_virtual_folder_id
        if name is not UNSET:
            field_dict["Name"] = name
        if description is not UNSET:
            field_dict["Description"] = description
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if virtual_folders is not UNSET:
            field_dict["VirtualFolders"] = virtual_folders

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _virtual_folder_id = d.pop("VirtualFolderId", UNSET)
        virtual_folder_id: Union[Unset, UUID]
        if isinstance(_virtual_folder_id,  Unset):
            virtual_folder_id = UNSET
        else:
            virtual_folder_id = UUID(_virtual_folder_id)




        _parent_virtual_folder_id = d.pop("ParentVirtualFolderId", UNSET)
        parent_virtual_folder_id: Union[Unset, UUID]
        if isinstance(_parent_virtual_folder_id,  Unset):
            parent_virtual_folder_id = UNSET
        else:
            parent_virtual_folder_id = UUID(_parent_virtual_folder_id)




        name = d.pop("Name", UNSET)

        description = d.pop("Description", UNSET)

        type_ = d.pop("Type", UNSET)

        virtual_folders = []
        _virtual_folders = d.pop("VirtualFolders", UNSET)
        for virtual_folders_item_data in (_virtual_folders or []):
            virtual_folders_item = VirincoWATSWebDashboardModelsMesVirtualFolderBasic.from_dict(virtual_folders_item_data)



            virtual_folders.append(virtual_folders_item)


        virinco_wats_web_dashboard_models_mes_virtual_folder_basic = cls(
            virtual_folder_id=virtual_folder_id,
            parent_virtual_folder_id=parent_virtual_folder_id,
            name=name,
            description=description,
            type_=type_,
            virtual_folders=virtual_folders,
        )


        virinco_wats_web_dashboard_models_mes_virtual_folder_basic.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_virtual_folder_basic

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
