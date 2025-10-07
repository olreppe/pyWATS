from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_edm_i_edm_structural_property_property_kind import MicrosoftODataEdmIEdmStructuralPropertyPropertyKind
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
  from ..models.microsoft_o_data_edm_i_edm_structured_type import MicrosoftODataEdmIEdmStructuredType





T = TypeVar("T", bound="MicrosoftODataEdmIEdmStructuralProperty")



@_attrs_define
class MicrosoftODataEdmIEdmStructuralProperty:
    """ 
        Attributes:
            default_value_string (Union[Unset, str]):
            property_kind (Union[Unset, MicrosoftODataEdmIEdmStructuralPropertyPropertyKind]):
            type_ (Union[Unset, MicrosoftODataEdmIEdmTypeReference]):
            declaring_type (Union[Unset, MicrosoftODataEdmIEdmStructuredType]):
            name (Union[Unset, str]):
     """

    default_value_string: Union[Unset, str] = UNSET
    property_kind: Union[Unset, MicrosoftODataEdmIEdmStructuralPropertyPropertyKind] = UNSET
    type_: Union[Unset, 'MicrosoftODataEdmIEdmTypeReference'] = UNSET
    declaring_type: Union[Unset, 'MicrosoftODataEdmIEdmStructuredType'] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        from ..models.microsoft_o_data_edm_i_edm_structured_type import MicrosoftODataEdmIEdmStructuredType
        default_value_string = self.default_value_string

        property_kind: Union[Unset, int] = UNSET
        if not isinstance(self.property_kind, Unset):
            property_kind = self.property_kind.value


        type_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.to_dict()

        declaring_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.declaring_type, Unset):
            declaring_type = self.declaring_type.to_dict()

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if default_value_string is not UNSET:
            field_dict["DefaultValueString"] = default_value_string
        if property_kind is not UNSET:
            field_dict["PropertyKind"] = property_kind
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if declaring_type is not UNSET:
            field_dict["DeclaringType"] = declaring_type
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_type_reference import MicrosoftODataEdmIEdmTypeReference
        from ..models.microsoft_o_data_edm_i_edm_structured_type import MicrosoftODataEdmIEdmStructuredType
        d = dict(src_dict)
        default_value_string = d.pop("DefaultValueString", UNSET)

        _property_kind = d.pop("PropertyKind", UNSET)
        property_kind: Union[Unset, MicrosoftODataEdmIEdmStructuralPropertyPropertyKind]
        if isinstance(_property_kind,  Unset):
            property_kind = UNSET
        else:
            property_kind = MicrosoftODataEdmIEdmStructuralPropertyPropertyKind(_property_kind)




        _type_ = d.pop("Type", UNSET)
        type_: Union[Unset, MicrosoftODataEdmIEdmTypeReference]
        if isinstance(_type_,  Unset):
            type_ = UNSET
        else:
            type_ = MicrosoftODataEdmIEdmTypeReference.from_dict(_type_)




        _declaring_type = d.pop("DeclaringType", UNSET)
        declaring_type: Union[Unset, MicrosoftODataEdmIEdmStructuredType]
        if isinstance(_declaring_type,  Unset):
            declaring_type = UNSET
        else:
            declaring_type = MicrosoftODataEdmIEdmStructuredType.from_dict(_declaring_type)




        name = d.pop("Name", UNSET)

        microsoft_o_data_edm_i_edm_structural_property = cls(
            default_value_string=default_value_string,
            property_kind=property_kind,
            type_=type_,
            declaring_type=declaring_type,
            name=name,
        )


        microsoft_o_data_edm_i_edm_structural_property.additional_properties = d
        return microsoft_o_data_edm_i_edm_structural_property

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
