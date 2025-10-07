from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.microsoft_o_data_edm_edm_referential_constraint_property_pair import MicrosoftODataEdmEdmReferentialConstraintPropertyPair





T = TypeVar("T", bound="MicrosoftODataEdmIEdmReferentialConstraint")



@_attrs_define
class MicrosoftODataEdmIEdmReferentialConstraint:
    """ 
        Attributes:
            property_pairs (Union[Unset, list['MicrosoftODataEdmEdmReferentialConstraintPropertyPair']]):
     """

    property_pairs: Union[Unset, list['MicrosoftODataEdmEdmReferentialConstraintPropertyPair']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.microsoft_o_data_edm_edm_referential_constraint_property_pair import MicrosoftODataEdmEdmReferentialConstraintPropertyPair
        property_pairs: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.property_pairs, Unset):
            property_pairs = []
            for property_pairs_item_data in self.property_pairs:
                property_pairs_item = property_pairs_item_data.to_dict()
                property_pairs.append(property_pairs_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if property_pairs is not UNSET:
            field_dict["PropertyPairs"] = property_pairs

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.microsoft_o_data_edm_edm_referential_constraint_property_pair import MicrosoftODataEdmEdmReferentialConstraintPropertyPair
        d = dict(src_dict)
        property_pairs = []
        _property_pairs = d.pop("PropertyPairs", UNSET)
        for property_pairs_item_data in (_property_pairs or []):
            property_pairs_item = MicrosoftODataEdmEdmReferentialConstraintPropertyPair.from_dict(property_pairs_item_data)



            property_pairs.append(property_pairs_item)


        microsoft_o_data_edm_i_edm_referential_constraint = cls(
            property_pairs=property_pairs,
        )


        microsoft_o_data_edm_i_edm_referential_constraint.additional_properties = d
        return microsoft_o_data_edm_i_edm_referential_constraint

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
