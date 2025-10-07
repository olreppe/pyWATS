from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_i_edm_structural_property import MicrosoftODataEdmIEdmStructuralProperty





T = TypeVar("T", bound="MicrosoftODataEdmEdmReferentialConstraintPropertyPair")



@_attrs_define
class MicrosoftODataEdmEdmReferentialConstraintPropertyPair:
    """ 
        Attributes:
            dependent_property (Union[Unset, MicrosoftODataEdmIEdmStructuralProperty]):
            principal_property (Union[Unset, MicrosoftODataEdmIEdmStructuralProperty]):
     """

    dependent_property: Union[Unset, 'MicrosoftODataEdmIEdmStructuralProperty'] = UNSET
    principal_property: Union[Unset, 'MicrosoftODataEdmIEdmStructuralProperty'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_i_edm_structural_property import MicrosoftODataEdmIEdmStructuralProperty
        dependent_property: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.dependent_property, Unset):
            dependent_property = self.dependent_property.to_dict()

        principal_property: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.principal_property, Unset):
            principal_property = self.principal_property.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if dependent_property is not UNSET:
            field_dict["DependentProperty"] = dependent_property
        if principal_property is not UNSET:
            field_dict["PrincipalProperty"] = principal_property

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_i_edm_structural_property import MicrosoftODataEdmIEdmStructuralProperty
        d = dict(src_dict)
        _dependent_property = d.pop("DependentProperty", UNSET)
        dependent_property: Union[Unset, MicrosoftODataEdmIEdmStructuralProperty]
        if isinstance(_dependent_property,  Unset):
            dependent_property = UNSET
        else:
            dependent_property = MicrosoftODataEdmIEdmStructuralProperty.from_dict(_dependent_property)




        _principal_property = d.pop("PrincipalProperty", UNSET)
        principal_property: Union[Unset, MicrosoftODataEdmIEdmStructuralProperty]
        if isinstance(_principal_property,  Unset):
            principal_property = UNSET
        else:
            principal_property = MicrosoftODataEdmIEdmStructuralProperty.from_dict(_principal_property)




        microsoft_o_data_edm_edm_referential_constraint_property_pair = cls(
            dependent_property=dependent_property,
            principal_property=principal_property,
        )


        microsoft_o_data_edm_edm_referential_constraint_property_pair.additional_properties = d
        return microsoft_o_data_edm_edm_referential_constraint_property_pair

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
