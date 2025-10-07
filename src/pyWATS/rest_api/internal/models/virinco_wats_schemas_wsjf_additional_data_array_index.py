from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_additional_data_property import VirincoWATSSchemasWSJFAdditionalDataProperty





T = TypeVar("T", bound="VirincoWATSSchemasWSJFAdditionalDataArrayIndex")



@_attrs_define
class VirincoWATSSchemasWSJFAdditionalDataArrayIndex:
    """ 
        Attributes:
            text (Union[Unset, str]): The index as text.
            indexes (Union[Unset, list[int]]): List of indexes ordered by dimension.
            value (Union[Unset, VirincoWATSSchemasWSJFAdditionalDataProperty]):
     """

    text: Union[Unset, str] = UNSET
    indexes: Union[Unset, list[int]] = UNSET
    value: Union[Unset, 'VirincoWATSSchemasWSJFAdditionalDataProperty'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_additional_data_property import VirincoWATSSchemasWSJFAdditionalDataProperty
        text = self.text

        indexes: Union[Unset, list[int]] = UNSET
        if not isinstance(self.indexes, Unset):
            indexes = self.indexes



        value: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.value, Unset):
            value = self.value.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if text is not UNSET:
            field_dict["text"] = text
        if indexes is not UNSET:
            field_dict["indexes"] = indexes
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_additional_data_property import VirincoWATSSchemasWSJFAdditionalDataProperty
        d = dict(src_dict)
        text = d.pop("text", UNSET)

        indexes = cast(list[int], d.pop("indexes", UNSET))


        _value = d.pop("value", UNSET)
        value: Union[Unset, VirincoWATSSchemasWSJFAdditionalDataProperty]
        if isinstance(_value,  Unset):
            value = UNSET
        else:
            value = VirincoWATSSchemasWSJFAdditionalDataProperty.from_dict(_value)




        virinco_wats_schemas_wsjf_additional_data_array_index = cls(
            text=text,
            indexes=indexes,
            value=value,
        )


        virinco_wats_schemas_wsjf_additional_data_array_index.additional_properties = d
        return virinco_wats_schemas_wsjf_additional_data_array_index

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
