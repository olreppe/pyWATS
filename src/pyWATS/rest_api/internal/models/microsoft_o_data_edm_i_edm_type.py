from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_edm_i_edm_type_type_kind import MicrosoftODataEdmIEdmTypeTypeKind
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftODataEdmIEdmType")



@_attrs_define
class MicrosoftODataEdmIEdmType:
    """ 
        Attributes:
            type_kind (Union[Unset, MicrosoftODataEdmIEdmTypeTypeKind]):
     """

    type_kind: Union[Unset, MicrosoftODataEdmIEdmTypeTypeKind] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_kind: Union[Unset, int] = UNSET
        if not isinstance(self.type_kind, Unset):
            type_kind = self.type_kind.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_kind is not UNSET:
            field_dict["TypeKind"] = type_kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _type_kind = d.pop("TypeKind", UNSET)
        type_kind: Union[Unset, MicrosoftODataEdmIEdmTypeTypeKind]
        if isinstance(_type_kind,  Unset):
            type_kind = UNSET
        else:
            type_kind = MicrosoftODataEdmIEdmTypeTypeKind(_type_kind)




        microsoft_o_data_edm_i_edm_type = cls(
            type_kind=type_kind,
        )


        microsoft_o_data_edm_i_edm_type.additional_properties = d
        return microsoft_o_data_edm_i_edm_type

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
