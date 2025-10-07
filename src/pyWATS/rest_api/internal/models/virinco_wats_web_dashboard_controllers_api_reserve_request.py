from collections.abc import Mapping
from typing import Any, TypeVar, Optional, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union






T = TypeVar("T", bound="VirincoWATSWebDashboardControllersApiReserveRequest")



@_attrs_define
class VirincoWATSWebDashboardControllersApiReserveRequest:
    """ 
        Attributes:
            rule_name (Union[Unset, str]):
            max_items (Union[Unset, int]):
     """

    rule_name: Union[Unset, str] = UNSET
    max_items: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        rule_name = self.rule_name

        max_items = self.max_items


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if rule_name is not UNSET:
            field_dict["RuleName"] = rule_name
        if max_items is not UNSET:
            field_dict["MaxItems"] = max_items

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        rule_name = d.pop("RuleName", UNSET)

        max_items = d.pop("MaxItems", UNSET)

        virinco_wats_web_dashboard_controllers_api_reserve_request = cls(
            rule_name=rule_name,
            max_items=max_items,
        )


        virinco_wats_web_dashboard_controllers_api_reserve_request.additional_properties = d
        return virinco_wats_web_dashboard_controllers_api_reserve_request

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
