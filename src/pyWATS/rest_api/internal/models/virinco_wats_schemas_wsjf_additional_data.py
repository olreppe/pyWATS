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





T = TypeVar("T", bound="VirincoWATSSchemasWSJFAdditionalData")



@_attrs_define
class VirincoWATSSchemasWSJFAdditionalData:
    """ 
        Attributes:
            name (Union[Unset, str]): Name of additional data.
            props (Union[Unset, list['VirincoWATSSchemasWSJFAdditionalDataProperty']]): Properties of additional data.
     """

    name: Union[Unset, str] = UNSET
    props: Union[Unset, list['VirincoWATSSchemasWSJFAdditionalDataProperty']] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_additional_data_property import VirincoWATSSchemasWSJFAdditionalDataProperty
        name = self.name

        props: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.props, Unset):
            props = []
            for props_item_data in self.props:
                props_item = props_item_data.to_dict()
                props.append(props_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if props is not UNSET:
            field_dict["props"] = props

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_additional_data_property import VirincoWATSSchemasWSJFAdditionalDataProperty
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        props = []
        _props = d.pop("props", UNSET)
        for props_item_data in (_props or []):
            props_item = VirincoWATSSchemasWSJFAdditionalDataProperty.from_dict(props_item_data)



            props.append(props_item)


        virinco_wats_schemas_wsjf_additional_data = cls(
            name=name,
            props=props,
        )


        virinco_wats_schemas_wsjf_additional_data.additional_properties = d
        return virinco_wats_schemas_wsjf_additional_data

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
