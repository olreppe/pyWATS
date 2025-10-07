from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="SystemCollectionsGenericKeyValuePairSystemStringSystemString")



@_attrs_define
class SystemCollectionsGenericKeyValuePairSystemStringSystemString:
    """ 
        Attributes:
            key (Union[Unset, str]):
            value (Union[Unset, str]):
     """

    key: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        key = self.key

        value = self.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if key is not UNSET:
            field_dict["Key"] = key
        if value is not UNSET:
            field_dict["Value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("Key", UNSET)

        value = d.pop("Value", UNSET)

        system_collections_generic_key_value_pair_system_string_system_string = cls(
            key=key,
            value=value,
        )


        system_collections_generic_key_value_pair_system_string_system_string.additional_properties = d
        return system_collections_generic_key_value_pair_system_string_system_string

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
