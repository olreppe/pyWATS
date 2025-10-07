from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from uuid import UUID






T = TypeVar("T", bound="VirincoWATSSchemasWSJFBinaryData")



@_attrs_define
class VirincoWATSSchemasWSJFBinaryData:
    """ 
        Attributes:
            content_type (Union[Unset, str]): Content type of attachment.
            data (Union[Unset, str]): The data of attachment.
            name (Union[Unset, str]): Name of attachment.
            id (Union[Unset, UUID]): Id of Binary data. Example: 00000000-0000-0000-0000-000000000000.
     """

    content_type: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    id: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        content_type = self.content_type

        data = self.data

        name = self.name

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if data is not UNSET:
            field_dict["data"] = data
        if name is not UNSET:
            field_dict["name"] = name
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_type = d.pop("contentType", UNSET)

        data = d.pop("data", UNSET)

        name = d.pop("name", UNSET)

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        virinco_wats_schemas_wsjf_binary_data = cls(
            content_type=content_type,
            data=data,
            name=name,
            id=id,
        )


        virinco_wats_schemas_wsjf_binary_data.additional_properties = d
        return virinco_wats_schemas_wsjf_binary_data

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
