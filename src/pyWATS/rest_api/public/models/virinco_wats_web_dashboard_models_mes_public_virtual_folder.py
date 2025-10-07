from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSWebDashboardModelsMesPublicVirtualFolder")



@_attrs_define
class VirincoWATSWebDashboardModelsMesPublicVirtualFolder:
    """ 
        Attributes:
            id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            parent_id (Union[Unset, UUID]):  Example: 00000000-0000-0000-0000-000000000000.
            name (Union[Unset, str]):
            description (Union[Unset, str]):
     """

    id: Union[Unset, UUID] = UNSET
    parent_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        parent_id: Union[Unset, str] = UNSET
        if not isinstance(self.parent_id, Unset):
            parent_id = str(self.parent_id)

        name = self.name

        description = self.description


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if parent_id is not UNSET:
            field_dict["parentId"] = parent_id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _parent_id = d.pop("parentId", UNSET)
        parent_id: Union[Unset, UUID]
        if isinstance(_parent_id,  Unset):
            parent_id = UNSET
        else:
            parent_id = UUID(_parent_id)




        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        virinco_wats_web_dashboard_models_mes_public_virtual_folder = cls(
            id=id,
            parent_id=parent_id,
            name=name,
            description=description,
        )


        virinco_wats_web_dashboard_models_mes_public_virtual_folder.additional_properties = d
        return virinco_wats_web_dashboard_models_mes_public_virtual_folder

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
