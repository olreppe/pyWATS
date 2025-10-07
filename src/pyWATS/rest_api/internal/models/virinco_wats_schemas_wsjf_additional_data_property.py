from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Union

if TYPE_CHECKING:
  from ..models.virinco_wats_schemas_wsjf_additional_data_array import VirincoWATSSchemasWSJFAdditionalDataArray





T = TypeVar("T", bound="VirincoWATSSchemasWSJFAdditionalDataProperty")



@_attrs_define
class VirincoWATSSchemasWSJFAdditionalDataProperty:
    """ 
        Attributes:
            name (Union[Unset, str]): Name of property.
            type_ (Union[Unset, str]): Value type of property.
            flags (Union[Unset, int]): Bit flags of property.
            value (Union[Unset, str]): Value string of property.
            num_format (Union[Unset, str]): Number format for value with type Number.
            comment (Union[Unset, str]): Comment of property.
            props (Union[Unset, list['VirincoWATSSchemasWSJFAdditionalDataProperty']]): Array of sub-properties. Used for
                type Obj.
            array (Union[Unset, VirincoWATSSchemasWSJFAdditionalDataArray]):
     """

    name: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    flags: Union[Unset, int] = UNSET
    value: Union[Unset, str] = UNSET
    num_format: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    props: Union[Unset, list['VirincoWATSSchemasWSJFAdditionalDataProperty']] = UNSET
    array: Union[Unset, 'VirincoWATSSchemasWSJFAdditionalDataArray'] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.virinco_wats_schemas_wsjf_additional_data_array import VirincoWATSSchemasWSJFAdditionalDataArray
        name = self.name

        type_ = self.type_

        flags = self.flags

        value = self.value

        num_format = self.num_format

        comment = self.comment

        props: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.props, Unset):
            props = []
            for props_item_data in self.props:
                props_item = props_item_data.to_dict()
                props.append(props_item)



        array: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.array, Unset):
            array = self.array.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if flags is not UNSET:
            field_dict["flags"] = flags
        if value is not UNSET:
            field_dict["value"] = value
        if num_format is not UNSET:
            field_dict["numFormat"] = num_format
        if comment is not UNSET:
            field_dict["comment"] = comment
        if props is not UNSET:
            field_dict["props"] = props
        if array is not UNSET:
            field_dict["array"] = array

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.virinco_wats_schemas_wsjf_additional_data_array import VirincoWATSSchemasWSJFAdditionalDataArray
        d = dict(src_dict)
        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        flags = d.pop("flags", UNSET)

        value = d.pop("value", UNSET)

        num_format = d.pop("numFormat", UNSET)

        comment = d.pop("comment", UNSET)

        props = []
        _props = d.pop("props", UNSET)
        for props_item_data in (_props or []):
            props_item = VirincoWATSSchemasWSJFAdditionalDataProperty.from_dict(props_item_data)



            props.append(props_item)


        _array = d.pop("array", UNSET)
        array: Union[Unset, VirincoWATSSchemasWSJFAdditionalDataArray]
        if isinstance(_array,  Unset):
            array = UNSET
        else:
            array = VirincoWATSSchemasWSJFAdditionalDataArray.from_dict(_array)




        virinco_wats_schemas_wsjf_additional_data_property = cls(
            name=name,
            type_=type_,
            flags=flags,
            value=value,
            num_format=num_format,
            comment=comment,
            props=props,
            array=array,
        )


        virinco_wats_schemas_wsjf_additional_data_property.additional_properties = d
        return virinco_wats_schemas_wsjf_additional_data_property

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
