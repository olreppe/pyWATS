from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSSchemasWSJFAttachment")



@_attrs_define
class VirincoWATSSchemasWSJFAttachment:
    """ 
        Attributes:
            name (Union[Unset, str]): Name of attachment.
            content_type (Union[Unset, str]): Content type of attachment.
            data (Union[Unset, str]): The data of attachment.
     """

    name: Union[Unset, str] = UNSET
    content_type: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        content_type = self.content_type

        data = self.data


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        content_type = d.pop("contentType", UNSET)

        data = d.pop("data", UNSET)

        virinco_wats_schemas_wsjf_attachment = cls(
            name=name,
            content_type=content_type,
            data=data,
        )


        virinco_wats_schemas_wsjf_attachment.additional_properties = d
        return virinco_wats_schemas_wsjf_attachment

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
