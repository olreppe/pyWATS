from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_additional_data_array_index import VirincoWATSSchemasWSJFAdditionalDataArrayIndex





T = TypeVar("T", bound="VirincoWATSSchemasWSJFAdditionalDataArray")



@_attrs_define
class VirincoWATSSchemasWSJFAdditionalDataArray:
    """ 
        Attributes:
            dimension (Union[Unset, int]): Dimension of array.
            type_ (Union[Unset, str]): Type of the values in the array.
            indexes (Union[Unset, list['VirincoWATSSchemasWSJFAdditionalDataArrayIndex']]): List of indexes in the array.
     """

    dimension: Union[Unset, int] = UNSET
    type_: Union[Unset, str] = UNSET
    indexes: Union[Unset, list['VirincoWATSSchemasWSJFAdditionalDataArrayIndex']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_additional_data_array_index import VirincoWATSSchemasWSJFAdditionalDataArrayIndex
        dimension = self.dimension

        type_ = self.type_

        indexes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.indexes, Unset):
            indexes = []
            for indexes_item_data in self.indexes:
                indexes_item = indexes_item_data.to_dict()
                indexes.append(indexes_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if dimension is not UNSET:
            field_dict["dimension"] = dimension
        if type_ is not UNSET:
            field_dict["type"] = type_
        if indexes is not UNSET:
            field_dict["indexes"] = indexes

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_additional_data_array_index import VirincoWATSSchemasWSJFAdditionalDataArrayIndex
        d = dict(src_dict)
        dimension = d.pop("dimension", UNSET)

        type_ = d.pop("type", UNSET)

        indexes = []
        _indexes = d.pop("indexes", UNSET)
        for indexes_item_data in (_indexes or []):
            indexes_item = VirincoWATSSchemasWSJFAdditionalDataArrayIndex.from_dict(indexes_item_data)



            indexes.append(indexes_item)


        virinco_wats_schemas_wsjf_additional_data_array = cls(
            dimension=dimension,
            type_=type_,
            indexes=indexes,
        )


        virinco_wats_schemas_wsjf_additional_data_array.additional_properties = d
        return virinco_wats_schemas_wsjf_additional_data_array

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
