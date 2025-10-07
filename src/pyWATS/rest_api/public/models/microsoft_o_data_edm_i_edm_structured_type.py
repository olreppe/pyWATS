from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_o_data_edm_i_edm_structured_type_type_kind import MicrosoftODataEdmIEdmStructuredTypeTypeKind
from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_property import MicrosoftODataEdmIEdmProperty





T = TypeVar("T", bound="MicrosoftODataEdmIEdmStructuredType")



@_attrs_define
class MicrosoftODataEdmIEdmStructuredType:
    """ 
        Attributes:
            is_abstract (Union[Unset, bool]):
            is_open (Union[Unset, bool]):
            base_type (Union[Unset, MicrosoftODataEdmIEdmStructuredType]):
            declared_properties (Union[Unset, list['MicrosoftODataEdmIEdmProperty']]):
            type_kind (Union[Unset, MicrosoftODataEdmIEdmStructuredTypeTypeKind]):
     """

    is_abstract: Union[Unset, bool] = UNSET
    is_open: Union[Unset, bool] = UNSET
    base_type: Union[Unset, 'MicrosoftODataEdmIEdmStructuredType'] = UNSET
    declared_properties: Union[Unset, list['MicrosoftODataEdmIEdmProperty']] = UNSET
    type_kind: Union[Unset, MicrosoftODataEdmIEdmStructuredTypeTypeKind] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_property import MicrosoftODataEdmIEdmProperty
        is_abstract = self.is_abstract

        is_open = self.is_open

        base_type: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.base_type, Unset):
            base_type = self.base_type.to_dict()

        declared_properties: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.declared_properties, Unset):
            declared_properties = []
            for declared_properties_item_data in self.declared_properties:
                declared_properties_item = declared_properties_item_data.to_dict()
                declared_properties.append(declared_properties_item)



        type_kind: Union[Unset, int] = UNSET
        if not isinstance(self.type_kind, Unset):
            type_kind = self.type_kind.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if is_abstract is not UNSET:
            field_dict["IsAbstract"] = is_abstract
        if is_open is not UNSET:
            field_dict["IsOpen"] = is_open
        if base_type is not UNSET:
            field_dict["BaseType"] = base_type
        if declared_properties is not UNSET:
            field_dict["DeclaredProperties"] = declared_properties
        if type_kind is not UNSET:
            field_dict["TypeKind"] = type_kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_property import MicrosoftODataEdmIEdmProperty
        d = dict(src_dict)
        is_abstract = d.pop("IsAbstract", UNSET)

        is_open = d.pop("IsOpen", UNSET)

        _base_type = d.pop("BaseType", UNSET)
        base_type: Union[Unset, MicrosoftODataEdmIEdmStructuredType]
        if isinstance(_base_type,  Unset):
            base_type = UNSET
        else:
            base_type = MicrosoftODataEdmIEdmStructuredType.from_dict(_base_type)




        declared_properties = []
        _declared_properties = d.pop("DeclaredProperties", UNSET)
        for declared_properties_item_data in (_declared_properties or []):
            declared_properties_item = MicrosoftODataEdmIEdmProperty.from_dict(declared_properties_item_data)



            declared_properties.append(declared_properties_item)


        _type_kind = d.pop("TypeKind", UNSET)
        type_kind: Union[Unset, MicrosoftODataEdmIEdmStructuredTypeTypeKind]
        if isinstance(_type_kind,  Unset):
            type_kind = UNSET
        else:
            type_kind = MicrosoftODataEdmIEdmStructuredTypeTypeKind(_type_kind)




        microsoft_o_data_edm_i_edm_structured_type = cls(
            is_abstract=is_abstract,
            is_open=is_open,
            base_type=base_type,
            declared_properties=declared_properties,
            type_kind=type_kind,
        )


        microsoft_o_data_edm_i_edm_structured_type.additional_properties = d
        return microsoft_o_data_edm_i_edm_structured_type

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
