from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType





T = TypeVar("T", bound="MicrosoftODataUriParserODataPathSegment")



@_attrs_define
class MicrosoftODataUriParserODataPathSegment:
    """ 
        Attributes:
            edm_type (Union[Unset, MicrosoftODataEdmIEdmType]):
            identifier (Union[Unset, str]):
     """

    edm_type: Union[Unset, 'MicrosoftODataEdmIEdmType'] = UNSET
    identifier: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        edm_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.edm_type, Unset):
            edm_type = self.edm_type.to_dict()

        identifier = self.identifier


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if edm_type is not UNSET:
            field_dict["EdmType"] = edm_type
        if identifier is not UNSET:
            field_dict["Identifier"] = identifier

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        d = dict(src_dict)
        _edm_type = d.pop("EdmType", UNSET)
        edm_type: Union[Unset, MicrosoftODataEdmIEdmType]
        if isinstance(_edm_type,  Unset):
            edm_type = UNSET
        else:
            edm_type = MicrosoftODataEdmIEdmType.from_dict(_edm_type)




        identifier = d.pop("Identifier", UNSET)

        microsoft_o_data_uri_parser_o_data_path_segment = cls(
            edm_type=edm_type,
            identifier=identifier,
        )


        microsoft_o_data_uri_parser_o_data_path_segment.additional_properties = d
        return microsoft_o_data_uri_parser_o_data_path_segment

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
