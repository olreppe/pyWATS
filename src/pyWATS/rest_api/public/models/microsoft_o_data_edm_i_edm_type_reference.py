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





T = TypeVar("T", bound="MicrosoftODataEdmIEdmTypeReference")



@_attrs_define
class MicrosoftODataEdmIEdmTypeReference:
    """ 
        Attributes:
            is_nullable (Union[Unset, bool]):
            definition (Union[Unset, MicrosoftODataEdmIEdmType]):
     """

    is_nullable: Union[Unset, bool] = UNSET
    definition: Union[Unset, 'MicrosoftODataEdmIEdmType'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        is_nullable = self.is_nullable

        definition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.definition, Unset):
            definition = self.definition.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if is_nullable is not UNSET:
            field_dict["IsNullable"] = is_nullable
        if definition is not UNSET:
            field_dict["Definition"] = definition

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_type import MicrosoftODataEdmIEdmType
        d = dict(src_dict)
        is_nullable = d.pop("IsNullable", UNSET)

        _definition = d.pop("Definition", UNSET)
        definition: Union[Unset, MicrosoftODataEdmIEdmType]
        if isinstance(_definition,  Unset):
            definition = UNSET
        else:
            definition = MicrosoftODataEdmIEdmType.from_dict(_definition)




        microsoft_o_data_edm_i_edm_type_reference = cls(
            is_nullable=is_nullable,
            definition=definition,
        )


        microsoft_o_data_edm_i_edm_type_reference.additional_properties = d
        return microsoft_o_data_edm_i_edm_type_reference

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
