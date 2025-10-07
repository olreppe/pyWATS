from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.microsoft_asp_net_o_data_query_order_by_node_direction import MicrosoftAspNetODataQueryOrderByNodeDirection
from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="MicrosoftAspNetODataQueryOrderByNode")



@_attrs_define
class MicrosoftAspNetODataQueryOrderByNode:
    """ 
        Attributes:
            direction (Union[Unset, MicrosoftAspNetODataQueryOrderByNodeDirection]):
     """

    direction: Union[Unset, MicrosoftAspNetODataQueryOrderByNodeDirection] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        direction: Union[Unset, int] = UNSET
        if not isinstance(self.direction, Unset):
            direction = self.direction.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if direction is not UNSET:
            field_dict["Direction"] = direction

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _direction = d.pop("Direction", UNSET)
        direction: Union[Unset, MicrosoftAspNetODataQueryOrderByNodeDirection]
        if isinstance(_direction,  Unset):
            direction = UNSET
        else:
            direction = MicrosoftAspNetODataQueryOrderByNodeDirection(_direction)




        microsoft_asp_net_o_data_query_order_by_node = cls(
            direction=direction,
        )


        microsoft_asp_net_o_data_query_order_by_node.additional_properties = d
        return microsoft_asp_net_o_data_query_order_by_node

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
