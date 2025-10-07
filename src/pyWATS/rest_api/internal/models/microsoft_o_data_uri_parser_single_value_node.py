from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_uri_parser_single_value_node_kind import MicrosoftODataUriParserSingleValueNodeKind
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference





T = TypeVar("T", bound="MicrosoftODataUriParserSingleValueNode")



@_attrs_define
class MicrosoftODataUriParserSingleValueNode:
    """ 
        Attributes:
            type_reference (Union[Unset, MicrosoftODataEdmIEdmTypeReference]):
            kind (Union[Unset, MicrosoftODataUriParserSingleValueNodeKind]):
     """

    type_reference: Union[Unset, 'MicrosoftODataEdmIEdmTypeReference'] = UNSET
    kind: Union[Unset, MicrosoftODataUriParserSingleValueNodeKind] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        type_reference: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.type_reference, Unset):
            type_reference = self.type_reference.to_dict()

        kind: Union[Unset, int] = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if type_reference is not UNSET:
            field_dict["TypeReference"] = type_reference
        if kind is not UNSET:
            field_dict["Kind"] = kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        d = dict(src_dict)
        _type_reference = d.pop("TypeReference", UNSET)
        type_reference: Union[Unset, MicrosoftODataEdmIEdmTypeReference]
        if isinstance(_type_reference,  Unset):
            type_reference = UNSET
        else:
            type_reference = MicrosoftODataEdmIEdmTypeReference.from_dict(_type_reference)




        _kind = d.pop("Kind", UNSET)
        kind: Union[Unset, MicrosoftODataUriParserSingleValueNodeKind]
        if isinstance(_kind,  Unset):
            kind = UNSET
        else:
            kind = MicrosoftODataUriParserSingleValueNodeKind(_kind)




        microsoft_o_data_uri_parser_single_value_node = cls(
            type_reference=type_reference,
            kind=kind,
        )


        microsoft_o_data_uri_parser_single_value_node.additional_properties = d
        return microsoft_o_data_uri_parser_single_value_node

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
